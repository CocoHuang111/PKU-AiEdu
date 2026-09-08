"""本地文件存储。预留对象存储接口，本次只实现 local。"""

from __future__ import annotations

import hashlib
import secrets
import shutil
from pathlib import Path
from typing import BinaryIO, Protocol

from .app_settings import get_app_settings


class StorageBackend(Protocol):
    name: str

    def save(self, key: str, stream: BinaryIO) -> int: ...

    def path_for(self, key: str) -> Path: ...

    def delete(self, key: str) -> None: ...


class LocalStorageBackend:
    name = "local"

    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or get_app_settings().upload_root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, key: str) -> Path:
        if not key or key.startswith("/") or ".." in Path(key).parts:
            raise ValueError("非法存储路径")
        path = (self.root / key).resolve()
        if not str(path).startswith(str(self.root)):
            raise ValueError("非法存储路径")
        return path

    def save(self, key: str, stream: BinaryIO) -> int:
        dest = self.path_for(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        size = 0
        with open(dest, "wb") as f:
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
        return size

    def delete(self, key: str) -> None:
        path = self.path_for(key)
        path.unlink(missing_ok=True)


class ObjectStorageBackend:
    """S3 / MinIO / OSS 预留。本次不接入。"""

    name = "object"

    def save(self, key: str, stream: BinaryIO) -> int:
        raise NotImplementedError("对象存储尚未接入")

    def path_for(self, key: str) -> Path:
        raise NotImplementedError("对象存储尚未接入")

    def delete(self, key: str) -> None:
        raise NotImplementedError("对象存储尚未接入")


def get_storage(backend: str = "local") -> StorageBackend:
    if backend == "local":
        return LocalStorageBackend()
    if backend in {"s3", "minio", "oss", "object"}:
        return ObjectStorageBackend()
    raise ValueError(f"未知存储后端: {backend}")


def random_filename(suffix: str) -> str:
    ext = suffix.lower() if suffix.startswith(".") else (f".{suffix.lower()}" if suffix else "")
    if "/" in ext or "\\" in ext or ".." in ext:
        raise ValueError("非法文件扩展名")
    return f"{secrets.token_hex(16)}{ext}"


def user_task_key(user_id: str, task_id: str, filename: str) -> str:
    return f"{user_id}/{task_id}/{filename}"


def user_avatar_key(user_id: str, filename: str) -> str:
    return f"{user_id}/avatars/{filename}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_into(key: str, source: Path, backend: str = "local") -> int:
    storage = get_storage(backend)
    with open(source, "rb") as stream:
        return storage.save(key, stream)


def remove_tree_if_empty(path: Path) -> None:
    try:
        if path.is_dir() and not any(path.iterdir()):
            shutil.rmtree(path, ignore_errors=True)
    except OSError:
        return
