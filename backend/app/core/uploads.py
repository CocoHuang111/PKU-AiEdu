from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from ai_engine.config import settings

from . import db
from .storage import get_storage, random_filename, sha256_file, user_avatar_key, user_task_key
from .material_storage import upload_backend, persist_file, evidence_bundle


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
    persist_now: bool = True,
) -> str:
    disk = Path(path)
    digest = await asyncio.to_thread(sha256_file, disk) if disk.is_file() else None
    backend = upload_backend()
    # Evaluation videos stay local until scoring finishes. Other uploads still
    # persist immediately so small files (avatars, syllabi) do not occupy ECS.
    store_backend = "local" if not persist_now or backend == "local" else "oss"
    file_id = await db.create_stored_file(
        user_id=user_id,
        purpose=purpose,
        original_name=original_name or disk.name,
        storage_key=storage_key,
        mime_type=mime_type,
        size_bytes=disk.stat().st_size if disk.is_file() else 0,
        sha256=digest,
        storage_backend=store_backend,
    )
    if store_backend == "local":
        return file_id
    bundle = None
    companion_id = None
    try:
        bundle = await asyncio.to_thread(evidence_bundle, path) if purpose == "video" else None
        await asyncio.to_thread(persist_file, storage_key, path)
        if bundle is not None:
            companion_key = storage_key + ".evidence.zip"
            companion_id = await db.create_stored_file(
                user_id=user_id, purpose="browser_evidence", original_name="evidence.zip",
                storage_key=companion_key, storage_backend="oss", mime_type="application/zip",
                size_bytes=bundle.stat().st_size,
                sha256=await asyncio.to_thread(sha256_file, bundle),
            )
            await asyncio.to_thread(persist_file, companion_key, str(bundle))
        return file_id
    except Exception:
        await db.soft_delete_stored_file(file_id, user_id=user_id)
        if companion_id:
            await db.soft_delete_stored_file(companion_id, user_id=user_id)
        raise
    finally:
        if bundle is not None:
            bundle.unlink(missing_ok=True)


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
