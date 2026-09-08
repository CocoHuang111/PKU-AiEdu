from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from ai_engine.config import settings

from . import db
from .storage import get_storage, random_filename, sha256_file, user_avatar_key, user_task_key


def _suffix(filename: str | None, allowed: set[str], kind_label: str) -> str:
    suffix = Path(filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(
            400,
            f"不支持的{kind_label}格式 {suffix}，支持：{', '.join(sorted(allowed))}",
        )
    return suffix


def save_user_upload(
    upload: UploadFile,
    *,
    user_id: str,
    task_id: str,
    purpose: str,
    allowed: set[str],
    max_bytes: int,
    kind_label: str,
) -> tuple[str, str]:
    suffix = _suffix(upload.filename, allowed, kind_label)
    filename = random_filename(suffix)
    key = user_task_key(user_id, task_id, filename)
    storage = get_storage("local")
    dest = storage.path_for(key)
    dest.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    try:
        with open(dest, "wb") as f:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    dest.unlink(missing_ok=True)
                    raise HTTPException(
                        400, f"{kind_label}超过大小限制（{max_bytes // (1024 * 1024)} MB）"
                    )
                f.write(chunk)
    finally:
        pass
    if size == 0:
        dest.unlink(missing_ok=True)
        raise HTTPException(400, f"上传的{kind_label}为空")
    return str(dest), key


async def record_upload(
    *,
    user_id: str,
    purpose: str,
    original_name: str,
    storage_key: str,
    mime_type: str | None,
    path: str,
) -> str:
    disk = Path(path)
    return await db.create_stored_file(
        user_id=user_id,
        purpose=purpose,
        original_name=original_name or disk.name,
        storage_key=storage_key,
        mime_type=mime_type,
        size_bytes=disk.stat().st_size if disk.is_file() else 0,
        sha256=sha256_file(disk) if disk.is_file() else None,
    )


def save_avatar(upload: UploadFile, user_id: str) -> tuple[str, str]:
    suffix = _suffix(
        upload.filename,
        {".png", ".jpg", ".jpeg", ".webp"},
        "头像",
    )
    filename = random_filename(suffix)
    key = user_avatar_key(user_id, filename)
    storage = get_storage("local")
    dest = storage.path_for(key)
    dest.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    with open(dest, "wb") as f:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > 2 * 1024 * 1024:
                dest.unlink(missing_ok=True)
                raise HTTPException(400, "头像请小于 2MB")
            f.write(chunk)
    if size == 0:
        dest.unlink(missing_ok=True)
        raise HTTPException(400, "上传的头像为空")
    return str(dest), key


def new_task_id() -> str:
    return str(uuid.uuid4())


def upload_root() -> Path:
    return settings.upload_dir.resolve()
