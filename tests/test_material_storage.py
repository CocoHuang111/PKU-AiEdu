from __future__ import annotations

import asyncio
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from backend.app.core import material_storage as materials
from backend.app.core import uploads
from backend.app.core.oss_storage import OSSStorageError
from backend.app.core.storage import LocalStorageBackend
from backend.app.core.browser_evidence import parse_manifest, _extract_archive


class FakeOSS:
    def __init__(self, root):
        self.objects = {}
        self.cache = LocalStorageBackend(root)
        self.config = SimpleNamespace(min_free_bytes=0)
        self.evicted = []

    def save(self, key, stream):
        if key in self.objects:
            error = OSSStorageError("conflict")
            error.status = 409
            raise error
        self.objects[key] = stream.read()

    def path_for(self, key):
        if key not in self.objects:
            raise FileNotFoundError(key)
        self.cache.save(key, io.BytesIO(self.objects[key]))
        return self.cache.path_for(key)

    def evict_cache(self, key):
        self.evicted.append(key)
        self.cache.delete(key)


class MaterialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.owner, self.task = "user", "task"
        self.key = "user/task/unique.mp4"
        self.oss = FakeOSS(self.root / "cache")
        self.settings = SimpleNamespace(upload_dir=self.root / "uploads", frame_dir=self.root / "frames")
        self.local = LocalStorageBackend(self.settings.upload_dir)
        patches = [patch.dict(os.environ, {"UPLOAD_STORAGE_BACKEND": "oss"}),
                   patch.object(materials, "settings", self.settings),
                   patch("backend.app.core.browser_evidence.settings", self.settings),
                   patch.object(materials, "get_storage", side_effect=lambda name: self.oss if name == "oss" else self.local)]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)

    def test_local_default_and_explicit_reference_ownership(self):
        path = str(self.local.path_for(self.key))
        ref = materials.material_reference(path, self.key)
        self.assertEqual(ref, "oss://" + self.key)
        self.assertEqual(materials.object_key(ref, owner="user", task_id="task"), self.key)
        for wrong in ("oss://other/task/a.mp4", "oss://user/other/a.mp4", "oss://user/task/../x"):
            with self.assertRaises(ValueError):
                materials.object_key(wrong, owner="user", task_id="task")
        with patch.dict(os.environ, {"UPLOAD_STORAGE_BACKEND": "local"}):
            self.assertEqual(materials.material_reference(path, self.key), path)

    def test_source_restores_without_staged_copy_and_survives_local_mode_rollback(self):
        self.oss.objects[self.key] = b"video"
        with patch.dict(os.environ, {"UPLOAD_STORAGE_BACKEND": "local"}):
            path = materials.resolve_material("oss://" + self.key, owner="user", task_id="task")
        self.assertEqual(Path(path).read_bytes(), b"video")
        materials.clear_staged_material("oss://" + self.key, owner="user", task_id="task")
        self.assertFalse(Path(path).exists())
        self.assertIn(self.key, self.oss.objects)
        self.assertEqual(materials.resolve_material("/legacy/file.mp4", owner="user", task_id="task"), "/legacy/file.mp4")

    def test_missing_source_never_serves_stale_staging(self):
        self.local.save(self.key, io.BytesIO(b"stale"))
        with self.assertRaises(FileNotFoundError):
            materials.resolve_material("oss://" + self.key, owner="user", task_id="task")

    def test_idempotent_save_does_not_overwrite_changed_content(self):
        self.local.save(self.key, io.BytesIO(b"original"))
        path = str(self.local.path_for(self.key))
        self.assertTrue(materials.persist_file(self.key, path))
        self.assertFalse(materials.persist_file(self.key, path))
        self.local.save(self.key, io.BytesIO(b"changed"))
        with self.assertRaises(ValueError):
            materials.persist_file(self.key, path)
        self.assertEqual(self.oss.objects[self.key], b"original")

    def test_evidence_bundle_restores_images_and_manifest_after_local_loss(self):
        self.key = "user/task/audio.m4a"
        audio = self.local.path_for(self.key)
        self.local.save(self.key, io.BytesIO(b"audio"))
        raw = {"version": 1, "original_filename": "lesson.mp4", "original_size": 100,
               "duration_sec": 6, "interval_sec": 3, "audio_codec": "aac",
               "dense_frames": [{"name": f"dense/{i:05d}.jpg", "time_sec": i * 3} for i in range(2)],
               "keyframes": [{"name": f"key/{i:02d}.jpg", "time_sec": .3 + i * .49} for i in range(12)]}
        manifest = parse_manifest(json.dumps(raw))
        images = self.root / "input.zip"
        with zipfile.ZipFile(images, "w") as archive:
            for name in manifest["expected_names"]:
                archive.writestr(name, b"jpeg")
        _extract_archive(str(images), self.settings.frame_dir / audio.stem, manifest)
        sidecar = audio.parent / "browser-evidence.json"
        sidecar.write_text(json.dumps(manifest))
        bundle = materials.evidence_bundle(str(audio))
        self.oss.objects[self.key] = b"audio"
        self.oss.objects[self.key + ".evidence.zip"] = bundle.read_bytes()
        audio.unlink()
        sidecar.unlink()
        import shutil
        shutil.rmtree(self.settings.frame_dir / audio.stem)
        ref = materials.material_reference(str(audio), self.key, evidence=True)
        self.assertEqual(ref, "oss-evidence://" + self.key)
        restored = materials.resolve_material(ref, owner="user", task_id="task")
        self.assertEqual(Path(restored).read_bytes(), b"audio")
        result = json.loads(sidecar.read_text())
        for item in result["dense_frames"] + result["keyframes"]:
            self.assertEqual(Path(item["path"]).read_bytes(), b"jpeg")
        del self.oss.objects[self.key + ".evidence.zip"]
        with self.assertRaises(FileNotFoundError):
            materials.resolve_material(ref, owner="user", task_id="task")

    def test_record_writes_metadata_before_upload_and_marks_failure_for_retry_cleanup(self):
        disk = self.root / "sample.mp4"
        disk.write_bytes(b"video")
        create = AsyncMock(return_value="file-id")
        remove = AsyncMock()
        def fail(key, path):
            self.assertTrue(create.await_count)
            raise OSSStorageError("failed")
        with patch.object(uploads.db, "create_stored_file", create), \
             patch.object(uploads.db, "soft_delete_stored_file", remove), \
             patch.object(uploads, "evidence_bundle", return_value=None), \
             patch.object(uploads, "persist_file", side_effect=fail):
            with self.assertRaises(OSSStorageError):
                asyncio.run(uploads.record_upload(user_id="user", purpose="video", original_name="video.mp4",
                                                storage_key=self.key, mime_type="video/mp4", path=str(disk)))
        self.assertEqual(create.call_args.kwargs["storage_backend"], "oss")
        remove.assert_awaited_once_with("file-id", user_id="user")

    def test_local_record_does_not_contact_oss(self):
        disk = self.root / "sample.pdf"
        disk.write_bytes(b"pdf")
        with patch.dict(os.environ, {"UPLOAD_STORAGE_BACKEND": "local"}), \
             patch.object(uploads.db, "create_stored_file", AsyncMock(return_value="id")) as create, \
             patch.object(uploads, "persist_file") as persist:
            result = asyncio.run(uploads.record_upload(user_id="user", purpose="syllabus", original_name="x.pdf",
                                                      storage_key=self.key, mime_type=None, path=str(disk)))
        self.assertEqual(result, "id")
        self.assertEqual(create.call_args.kwargs["storage_backend"], "local")
        persist.assert_not_called()

    def test_terminal_cleanup_removes_large_audio_but_keeps_report_frames(self):
        self.local.save(self.key, io.BytesIO(b"video"))
        wav = self.settings.upload_dir / "unique.wav"
        wav.write_bytes(b"wav")
        frames = self.settings.frame_dir / "unique"
        frames.mkdir(parents=True)
        (frames / "report.jpg").write_bytes(b"image")
        materials.clear_staged_material("oss://" + self.key, owner="user", task_id="task", processing=True)
        self.assertFalse(wav.exists())
        self.assertTrue((frames / "report.jpg").exists())

    def test_deleted_objects_retry_and_active_duplicate_protection(self):
        row = SimpleNamespace(id="old", user_id="user", storage_key=self.key)
        session = SimpleNamespace(scalars=AsyncMock(return_value=SimpleNamespace(all=lambda: [row])),
                                  scalar=AsyncMock(return_value=None), delete=AsyncMock())
        class Scope:
            async def __aenter__(self):
                return session
            async def __aexit__(self, *args):
                return False
        fake = SimpleNamespace(delete=lambda key: (_ for _ in ()).throw(OSSStorageError("failed")))
        with patch.object(materials, "session_scope", return_value=Scope()), \
             patch.object(materials, "get_storage", return_value=fake):
            asyncio.run(materials.purge_deleted_oss_files())
        session.delete.assert_not_awaited()
        session.scalar.return_value = "live-metadata-record"
        with patch.object(materials, "session_scope", return_value=Scope()), \
             patch.object(materials, "get_storage") as storage:
            asyncio.run(materials.purge_deleted_oss_files())
        storage.assert_not_called()
        session.delete.assert_awaited_once_with(row)


if __name__ == "__main__":
    unittest.main()
