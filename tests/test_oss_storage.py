from __future__ import annotations

import hashlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from backend.app.core.oss_storage import OSSConfig, OSSStorageBackend, OSSStorageError, _make_auth
from backend.app.core.storage import LocalStorageBackend, get_storage


class ProviderError(Exception):
    def __init__(self, status, code):
        super().__init__("SECRET token https://example.invalid/?signature=SECRET")
        self.status, self.code = status, code


class FakeBucket:
    def __init__(self):
        self.objects = {}
        self.downloads = 0
        self.fail_download = False
        self.truncate_download = False
        self.last_signed = None

    def put_object(self, key, stream, headers):
        if key in self.objects and headers.get("x-oss-forbid-overwrite") == "true":
            raise ProviderError(409, "FileAlreadyExists")
        self.objects[key] = b"".join(stream)
        return SimpleNamespace(status=200)

    def head_object(self, key):
        if key not in self.objects:
            raise ProviderError(404, "NoSuchKey")
        body = self.objects[key]
        return SimpleNamespace(content_length=len(body), etag=hashlib.md5(body).hexdigest())

    def get_object_to_file(self, key, filename, headers):
        self.downloads += 1
        self.expected_if_match = headers.get("If-Match")
        if self.fail_download:
            Path(filename).write_bytes(b"partial")
            raise ProviderError(403, "AccessDenied")
        body = self.objects[key]
        Path(filename).write_bytes(body[:-1] if self.truncate_download else body)

    def delete_object(self, key):
        self.objects.pop(key, None)
        return SimpleNamespace(status=204)

    def sign_url(self, method, key, expires):
        self.last_signed = (method, key, expires)
        return "https://pku-askedu.oss-cn-beijing.aliyuncs.com/file?signature=SECRET"


class OSSStorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = OSSConfig("pku-askedu", "cn-beijing", "AskEduOssServerRole", self.root,
                                max_object_bytes=10 * 1024 ** 2, min_free_bytes=0)
        self.bucket = FakeBucket()
        self.public_bucket = FakeBucket()
        self.storage = OSSStorageBackend(self.config, bucket=self.bucket, public_bucket=self.public_bucket)

    def test_stream_upload_and_no_silent_overwrite(self):
        data = b"abc" * (1024 ** 2)
        self.assertEqual(self.storage.save("user/task/video.mp4", io.BytesIO(data)), len(data))
        self.assertEqual(self.bucket.objects["user/task/video.mp4"], data)
        with self.assertRaises(OSSStorageError):
            self.storage.save("user/task/video.mp4", io.BytesIO(b"replacement"))
        self.assertEqual(self.bucket.objects["user/task/video.mp4"], data)

    def test_cache_reuse_and_remote_version_change(self):
        key = "user/task/video.mp4"
        self.storage.save(key, io.BytesIO(b"video"))
        path = self.storage.path_for(key)
        self.assertEqual(path.suffix, ".mp4")
        self.assertEqual(path.read_bytes(), b"video")
        self.assertEqual(self.storage.path_for(key), path)
        self.assertEqual(self.bucket.downloads, 1)
        self.assertEqual(self.bucket.expected_if_match, self.bucket.head_object(key).etag)
        self.bucket.objects[key] = b"other"
        self.assertEqual(self.storage.path_for(key).read_bytes(), b"other")
        self.assertEqual(self.bucket.downloads, 2)

    def test_bad_cache_metadata_or_size_is_refetched(self):
        key = "user/task/audio.m4a"
        self.storage.save(key, io.BytesIO(b"audio"))
        path = self.storage.path_for(key)
        _, metadata = self.storage._paths(key)
        metadata.write_text("not json")
        self.storage.path_for(key)
        path.write_bytes(b"a")
        self.storage.path_for(key)
        self.assertEqual(self.bucket.downloads, 3)

    def test_failed_or_truncated_download_not_published(self):
        key = "user/task/video.mp4"
        self.storage.save(key, io.BytesIO(b"video"))
        self.bucket.fail_download = True
        with self.assertRaises(OSSStorageError) as failure:
            self.storage.path_for(key)
        self.assertNotIn("SECRET", str(failure.exception))
        path, meta = self.storage._paths(key)
        self.assertFalse(path.exists())
        self.assertFalse(meta.exists())
        self.assertEqual(list(self.root.rglob(".oss-part-*")), [])
        self.bucket.fail_download = False
        self.bucket.truncate_download = True
        with self.assertRaises(OSSStorageError):
            self.storage.path_for(key)
        self.assertFalse(path.exists())

    def test_failed_refresh_preserves_complete_old_cache(self):
        key = "video.mp4"
        self.storage.save(key, io.BytesIO(b"old"))
        path = self.storage.path_for(key)
        self.bucket.objects[key] = b"new"
        self.bucket.fail_download = True
        with self.assertRaises(OSSStorageError):
            self.storage.path_for(key)
        self.assertEqual(path.read_bytes(), b"old")

    def test_missing_remote_object_not_served_from_stale_cache(self):
        self.storage.save("video.mp4", io.BytesIO(b"video"))
        self.storage.path_for("video.mp4")
        self.bucket.objects.clear()
        with self.assertRaises(FileNotFoundError):
            self.storage.path_for("video.mp4")

    def test_delete_and_cache_only_eviction(self):
        self.storage.save("video.mp4", io.BytesIO(b"video"))
        path = self.storage.path_for("video.mp4")
        self.storage.evict_cache("video.mp4")
        self.assertFalse(path.exists())
        self.assertIn("video.mp4", self.bucket.objects)
        self.storage.path_for("video.mp4")
        self.storage.delete("video.mp4")
        self.assertNotIn("video.mp4", self.bucket.objects)
        self.assertFalse(path.exists())
        self.storage.delete("video.mp4")

    def test_invalid_keys_never_reach_provider(self):
        for key in ["", "/x", "../x", "user/../x", "user//x", "user/./x", "a\\b", "x\n"]:
            for operation in [self.storage.path_for, self.storage.delete, self.storage.signed_download_url]:
                with self.subTest(key=key), self.assertRaises(ValueError):
                    operation(key)
        self.assertEqual(self.bucket.objects, {})

    def test_cache_object_metadata_names_cannot_collide(self):
        for key in ["file", "file.oss-meta.json"]:
            self.storage.save(key, io.BytesIO(key.encode()))
            self.assertEqual(self.storage.path_for(key).read_bytes(), key.encode())

    def test_disk_and_object_limits_checked_before_download(self):
        self.storage.save("video.mp4", io.BytesIO(b"video"))
        with patch("backend.app.core.oss_storage.shutil.disk_usage", return_value=SimpleNamespace(free=1)):
            with self.assertRaises(OSSStorageError):
                self.storage.path_for("video.mp4")
        self.bucket.objects["huge"] = b"x" * (self.config.max_object_bytes + 1)
        with self.assertRaises(OSSStorageError):
            self.storage.path_for("huge")
        with self.assertRaises(OSSStorageError):
            self.storage.save("huge-upload", io.BytesIO(self.bucket.objects["huge"]))
        self.assertEqual(self.bucket.downloads, 0)

    def test_public_download_signature_and_ttl(self):
        self.assertIn("https://", self.storage.signed_download_url("video.mp4", 300))
        self.assertEqual(self.public_bucket.last_signed, ("GET", "video.mp4", 300))
        for ttl in [0, -1, 901, "300", True]:
            with self.assertRaises(ValueError):
                self.storage.signed_download_url("video.mp4", ttl)
        self.assertIn("-internal.", self.config.endpoint())
        self.assertNotIn("-internal.", self.config.endpoint(public=True))

    def test_config_and_storage_selection_no_default_switch(self):
        env = {"OSS_BUCKET": "pku-askedu", "OSS_REGION": "cn-beijing",
               "OSS_RAM_ROLE_NAME": "AskEduOssServerRole", "OSS_CACHE_ROOT": str(self.root)}
        with patch.dict(os.environ, env):
            self.assertEqual(get_storage("oss").name, "oss")
            self.assertEqual(get_storage().name, "local")
            for name, bad in [("OSS_BUCKET", "https://evil"), ("OSS_REGION", "../cn-beijing"),
                              ("OSS_RAM_ROLE_NAME", "role/../../x"), ("OSS_USE_INTERNAL", "maybe")]:
                with patch.dict(os.environ, {name: bad}), self.assertRaises(ValueError):
                    OSSConfig.from_env()

    def test_local_symlink_cannot_escape_to_sibling_prefix(self):
        local = LocalStorageBackend(self.root / "uploads")
        sibling = self.root / "uploads-other"
        sibling.mkdir()
        (local.root / "escape").symlink_to(sibling, target_is_directory=True)
        with self.assertRaises(ValueError):
            local.path_for("escape/file")

    def test_ecs_provider_uses_v2_and_refreshes_credentials(self):
        with patch("alibabacloud_credentials.client.Client") as client:
            client.return_value.get_credential.side_effect = [
                SimpleNamespace(access_key_id="id1", access_key_secret="secret1", security_token="token1"),
                SimpleNamespace(access_key_id="id2", access_key_secret="secret2", security_token="token2")]
            auth = _make_auth("AskEduOssServerRole")
            config = client.call_args.args[0]
            self.assertEqual(config.type, "ecs_ram_role")
            self.assertTrue(config.enable_imds_v2)
            self.assertTrue(config.disable_imds_v1)
            self.assertEqual(auth.credentials_provider.get_credentials().get_security_token(), "token1")
            self.assertEqual(auth.credentials_provider.get_credentials().get_security_token(), "token2")

    def test_real_sdk_factory_and_public_endpoint(self):
        fake = FakeBucket()
        with patch("backend.app.core.oss_storage._make_auth", return_value=object()), \
                patch("oss2.Bucket", return_value=fake) as factory:
            storage = OSSStorageBackend(self.config)
            self.assertEqual(storage.save("video.mp4", io.BytesIO(b"video")), 5)
            self.assertEqual(factory.call_args.args[1], self.config.endpoint())
            self.assertTrue(factory.call_args.kwargs["enable_crc"])
            storage.signed_download_url("video.mp4")
            self.assertEqual(factory.call_args.args[1], self.config.endpoint(public=True))

    def test_credential_failure_is_sanitized(self):
        with patch("backend.app.core.oss_storage._make_auth", side_effect=RuntimeError("SECRET credential")):
            storage = OSSStorageBackend(self.config)
            with self.assertRaises(OSSStorageError) as failure:
                storage.save("video.mp4", io.BytesIO(b"video"))
            self.assertNotIn("SECRET", str(failure.exception))


if __name__ == "__main__":
    unittest.main()
