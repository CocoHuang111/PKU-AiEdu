"""Private OSS objects, ECS role credentials and atomic local processing cache.

This synchronous adapter is called in a worker thread, not on the API event loop.
The application must check ownership before resolving an object or signing a URL.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

from .app_settings import get_app_settings
from .storage import LocalStorageBackend


class OSSStorageError(RuntimeError):
    """Safe error text: never include credentials, request headers or signed URLs."""


@dataclass(frozen=True)
class OSSConfig:
    bucket: str
    region: str
    role_name: str
    cache_root: Path
    internal: bool = True
    max_object_bytes: int = 10 * 1024 ** 3
    min_free_bytes: int = 5 * 1024 ** 3

    def __post_init__(self):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,61}[a-z0-9]", self.bucket):
            raise ValueError("OSS_BUCKET 必须为有效 Bucket 名称")
        if not re.fullmatch(r"[a-z][a-z0-9-]{2,40}", self.region):
            raise ValueError("OSS_REGION 必须为有效地域 ID")
        if not re.fullmatch(r"[A-Za-z0-9@._-]{1,64}", self.role_name):
            raise ValueError("OSS_RAM_ROLE_NAME 必须为有效 RAM 角色名称")
        if self.max_object_bytes <= 0 or self.min_free_bytes < 0:
            raise ValueError("OSS 缓存大小配置无效")

    @classmethod
    def from_env(cls):
        internal = os.getenv("OSS_USE_INTERNAL", "true").strip().lower()
        if internal not in {"true", "false"}:
            raise ValueError("OSS_USE_INTERNAL 只能为 true 或 false")
        root = os.getenv("OSS_CACHE_ROOT")
        return cls(
            bucket=os.getenv("OSS_BUCKET", "").strip(),
            region=os.getenv("OSS_REGION", "").strip(),
            role_name=os.getenv("OSS_RAM_ROLE_NAME", "").strip(),
            cache_root=Path(root) if root else get_app_settings().upload_root / ".oss-cache",
            internal=internal == "true",
            max_object_bytes=int(os.getenv("OSS_MAX_OBJECT_BYTES", str(10 * 1024 ** 3))),
            min_free_bytes=int(os.getenv("OSS_CACHE_MIN_FREE_BYTES", str(5 * 1024 ** 3))),
        )

    def endpoint(self, *, public=False):
        internal = "-internal" if self.internal and not public else ""
        return f"https://oss-{self.region}{internal}.aliyuncs.com"


def _make_auth(role_name):
    import oss2
    from alibabacloud_credentials.client import Client
    from alibabacloud_credentials.models import Config
    from oss2.credentials import Credentials

    client = Client(Config(type="ecs_ram_role", role_name=role_name,
                           enable_imds_v2=True, disable_imds_v1=True,
                           timeout=5000, connect_timeout=3000))

    class RoleProvider(oss2.CredentialsProvider):
        def __init__(self):
            self.lock = threading.Lock()

        def get_credentials(self):
            with self.lock:
                credential = client.get_credential()
            return Credentials(credential.access_key_id, credential.access_key_secret,
                               credential.security_token)

    return oss2.ProviderAuthV4(RoleProvider())


class OSSStorageBackend:
    name = "oss"

    def __init__(self, config: OSSConfig | None = None, *, bucket=None, public_bucket=None):
        self.config = config or OSSConfig.from_env()
        # Bucket isolation prevents an old cache being reused after reconfiguration.
        self.cache = LocalStorageBackend(self.config.cache_root / self.config.region / self.config.bucket)
        self._bucket, self._public_bucket = bucket, public_bucket
        self._auth = None
        self._init_lock = threading.Lock()

    @property
    def bucket(self):
        if self._bucket is None:
            with self._init_lock:
                if self._bucket is None:
                    import oss2
                    self._auth = _make_auth(self.config.role_name)
                    self._bucket = oss2.Bucket(self._auth, self.config.endpoint(), self.config.bucket,
                                              region=self.config.region, connect_timeout=30, enable_crc=True)
        return self._bucket

    @staticmethod
    def _key(key):
        if (not isinstance(key, str) or not key or len(key.encode("utf-8")) > 1024
                or "\\" in key or any(ord(ch) < 32 for ch in key)
                or any(part in {"", ".", ".."} for part in key.split("/"))):
            raise ValueError("非法 OSS 存储路径")
        return key

    @staticmethod
    def _call(operation, action):
        try:
            return action()
        except Exception as exc:
            status = getattr(exc, "status", None)
            code = getattr(exc, "code", "")
            if status == 404 and code == "NoSuchKey":
                raise FileNotFoundError("OSS 文件不存在") from None
            suffix = f"（HTTP {status}）" if isinstance(status, int) else ""
            raise OSSStorageError(f"OSS {operation}失败{suffix}，请检查角色权限、网络和配置") from None

    def save(self, key: str, stream: BinaryIO) -> int:
        key = self._key(key)
        size = 0

        def chunks():
            nonlocal size
            while data := stream.read(1024 * 1024):
                size += len(data)
                if size > self.config.max_object_bytes:
                    raise ValueError("文件超过 OSS 大小限制")
                yield data

        # Keys are immutable/random: do not silently overwrite an existing object.
        self._call("上传", lambda: self.bucket.put_object(
            key, chunks(), headers={"x-oss-forbid-overwrite": "true"}))
        self.evict_cache(key)
        return size

    def _paths(self, key):
        key = self._key(key)
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        suffix = Path(key).suffix
        if not re.fullmatch(r"\.[A-Za-z0-9]{1,15}", suffix):
            suffix = ".bin"
        # Separate namespaces avoid collisions between objects and cache metadata.
        return (self.cache.path_for(f"data/{digest}{suffix}"),
                self.cache.path_for(f"metadata/{digest}.json"))

    def path_for(self, key: str) -> Path:
        path, meta_path = self._paths(key)
        head = self._call("读取文件信息", lambda: self.bucket.head_object(key))
        size, etag = int(head.content_length), str(head.etag)
        if size < 0 or size > self.config.max_object_bytes or not etag:
            raise OSSStorageError("OSS 文件信息无效或超过大小限制")
        expected = {"etag": etag, "size": size}
        try:
            if path.is_file() and path.stat().st_size == size and json.loads(meta_path.read_text()) == expected:
                return path
        except (OSError, ValueError):
            pass
        path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        if shutil.disk_usage(path.parent).free < size + self.config.min_free_bytes:
            raise OSSStorageError("OSS 解析缓存磁盘空间不足")
        data_fd, data_name = tempfile.mkstemp(prefix=".oss-part-", dir=path.parent)
        meta_fd, meta_name = tempfile.mkstemp(prefix=".oss-meta-", dir=meta_path.parent)
        os.close(data_fd)
        os.close(meta_fd)
        try:
            self._call("下载", lambda: self.bucket.get_object_to_file(
                key, data_name, headers={"If-Match": etag}))
            if Path(data_name).stat().st_size != size:
                raise OSSStorageError("OSS 下载文件大小不匹配")
            Path(meta_name).write_text(json.dumps(expected), encoding="utf-8")
            os.replace(data_name, path)
            os.replace(meta_name, meta_path)
            return path
        finally:
            Path(data_name).unlink(missing_ok=True)
            Path(meta_name).unlink(missing_ok=True)

    def evict_cache(self, key: str) -> None:
        path, meta = self._paths(key)
        path.unlink(missing_ok=True)
        meta.unlink(missing_ok=True)

    def delete(self, key: str) -> None:
        key = self._key(key)
        self._call("删除", lambda: self.bucket.delete_object(key))
        self.evict_cache(key)

    def signed_download_url(self, key: str, expires=300) -> str:
        key = self._key(key)
        if type(expires) is not int or not 1 <= expires <= 900:
            raise ValueError("下载链接有效期必须为 1–900 秒")
        if self._public_bucket is None:
            # Signing must use the public endpoint, even if processing uses the internal endpoint.
            self.bucket
            import oss2
            self._public_bucket = oss2.Bucket(self._auth, self.config.endpoint(public=True),
                                             self.config.bucket, region=self.config.region)
        return self._call("生成下载凭证", lambda: self._public_bucket.sign_url("GET", key, expires))
