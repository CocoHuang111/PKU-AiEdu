"""Durable upload references; local files are processing scratch, not the source of truth."""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from ai_engine.config import settings
from .database import session_scope
from .storage import LocalStorageBackend, get_storage, sha256_file
from ..models.files import StoredFile

PREFIX = "oss://"
EVIDENCE_PREFIX = "oss-evidence://"


def is_oss_reference(reference: str) -> bool:
    return reference.startswith((PREFIX, EVIDENCE_PREFIX))


def upload_backend() -> str:
    backend = os.getenv("UPLOAD_STORAGE_BACKEND", "local").strip().lower()
    if backend not in {"local", "oss"}:
        raise ValueError("UPLOAD_STORAGE_BACKEND 只能为 local 或 oss")
    return backend


def material_reference(path: str | None, key: str | None = None, *, evidence=False) -> str | None:
    if not path or upload_backend() == "local":
        return path
    if key is None:
        key = Path(path).resolve().relative_to(settings.upload_dir.resolve()).as_posix()
    get_storage("local").path_for(key)  # reject path escapes before persisting a reference
    return (EVIDENCE_PREFIX if evidence else PREFIX) + key


def object_key(reference: str, *, owner: str | None = None, task_id: str | None = None) -> str:
    if not is_oss_reference(reference):
        raise ValueError("不是 OSS 材料引用")
    key = reference[len(EVIDENCE_PREFIX if reference.startswith(EVIDENCE_PREFIX) else PREFIX):]
    from .oss_storage import OSSStorageBackend
    OSSStorageBackend._key(key)
    if owner is not None and not key.startswith(f"{owner}/"):
        raise ValueError("材料不属于当前用户")
    if task_id is not None and not key.startswith(f"{owner}/{task_id}/"):
        raise ValueError("材料不属于当前任务")
    return key


def persist_file(key: str, path: str) -> bool:
    storage = get_storage("oss")
    with Path(path).open("rb") as source:
        try:
            storage.save(key, source)
        except Exception as error:
            # Completion may be retried after the DB update failed. Never overwrite.
            if getattr(error, "status", None) != 409:
                raise
            try:
                if sha256_file(storage.path_for(key)) != sha256_file(Path(path)):
                    raise ValueError("OSS 材料已存在且内容不同") from None
            finally:
                storage.evict_cache(key)
            return False
    return True


def evidence_bundle(path: str) -> Path | None:
    media = Path(path)
    manifest_path = media.parent / "browser-evidence.json"
    if not manifest_path.is_file():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    from .browser_evidence import parse_manifest
    normalized = parse_manifest(json.dumps(manifest))
    normalized.pop("expected_names")
    frame_root = settings.frame_dir.resolve()
    fd, name = tempfile.mkstemp(prefix="oss-evidence-", suffix=".zip", dir=media.parent)
    os.close(fd)
    bundle = Path(name)
    try:
        with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.writestr("manifest.json", json.dumps(normalized, ensure_ascii=False))
            for group in ("dense_frames", "keyframes"):
                for item in manifest[group]:
                    frame = Path(item["path"]).resolve()
                    if not frame.is_relative_to(frame_root) or not frame.is_file():
                        raise ValueError("浏览器证据画面缺失或路径非法")
                    archive.write(frame, item["name"])
        return bundle
    except Exception:
        bundle.unlink(missing_ok=True)
        raise


def restore_evidence(key: str, media: Path) -> None:
    from .browser_evidence import _extract_archive, parse_manifest, MAX_UNPACKED_BYTES
    storage = get_storage("oss")
    bundle_key = key + ".evidence.zip"
    bundle = storage.path_for(bundle_key)  # missing quick-upload evidence is an error, not silent fallback
    try:
        with zipfile.ZipFile(bundle) as archive:
            info = archive.getinfo("manifest.json")
            if info.file_size > 2 * 1024 * 1024:
                raise ValueError("浏览器证据清单过大")
            manifest = parse_manifest(archive.read(info).decode("utf-8"))
            names = set(manifest["expected_names"])
            if set(archive.namelist()) != names | {"manifest.json"}:
                raise ValueError("浏览器证据包内容不一致")
            # Reuse the hardened extractor after stripping the companion manifest.
            if sum(i.file_size for i in archive.infolist()) > MAX_UNPACKED_BYTES + info.file_size:
                raise ValueError("浏览器证据包过大")
            with tempfile.TemporaryDirectory(prefix="oss-frames-", dir=media.parent) as tmp:
                images = Path(tmp) / "images.zip"
                with zipfile.ZipFile(images, "w", compression=zipfile.ZIP_STORED) as target:
                    for name in names:
                        target.writestr(name, archive.read(name))
                frame_root = settings.frame_dir / media.stem
                # Unique random media keys isolate each task's frames.
                if frame_root.is_dir():
                    shutil.rmtree(frame_root)
                _extract_archive(str(images), frame_root, manifest)
                target = media.parent / "browser-evidence.json"
                temporary = Path(tmp) / "manifest.json"
                temporary.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
                os.replace(temporary, target)
    finally:
        storage.evict_cache(bundle_key)


def resolve_material(reference: str | None, *, owner: str, task_id: str) -> str | None:
    if not reference or not is_oss_reference(reference):
        return reference  # pre-switch tasks remain local
    key = object_key(reference, owner=owner, task_id=task_id)
    dest = LocalStorageBackend(settings.upload_dir).path_for(key)
    storage = get_storage("oss")
    # Always validate against OSS, including when a staged copy still exists.
    cached = storage.path_for(key)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(dest.parent).free < cached.stat().st_size + storage.config.min_free_bytes:
        storage.evict_cache(key)
        raise ValueError("OSS 解析临时文件磁盘空间不足")
    fd, name = tempfile.mkstemp(prefix=".restore-", dir=dest.parent)
    os.close(fd)
    try:
        shutil.copyfile(cached, name)
        os.replace(name, dest)
    finally:
        Path(name).unlink(missing_ok=True)
        storage.evict_cache(key)
    if reference.startswith(EVIDENCE_PREFIX):
        restore_evidence(key, dest)
    return str(dest)


def clear_staged_material(reference: str | None, *, owner: str, task_id: str, processing=False) -> None:
    if reference and is_oss_reference(reference):
        key = object_key(reference, owner=owner, task_id=task_id)
        LocalStorageBackend(settings.upload_dir).path_for(key).unlink(missing_ok=True)
        get_storage("oss").evict_cache(key)
        if processing:
            # Large audio/checkpoints are scratch. Keep report frames until task deletion.
            root = settings.upload_dir.resolve()
            wav = root / (Path(key).stem + ".wav")
            wav.unlink(missing_ok=True)
            for suffix in (".audio-source.json", ".audio-features.json"):
                wav.with_suffix(suffix).unlink(missing_ok=True)
            for suffix in (".asr-checkpoint", ".audio-checkpoint", ".punctuation-checkpoint"):
                folder = wav.with_suffix(suffix)
                if folder.parent == root and folder.is_dir():
                    shutil.rmtree(folder)


async def mark_task_files_deleted(owner: str, task_id: str) -> None:
    async with session_scope() as session:
        rows = (await session.scalars(select(StoredFile).where(
            StoredFile.user_id == uuid.UUID(owner),
            StoredFile.storage_key.like(f"{owner}/{task_id}/%"),
            StoredFile.deleted_at.is_(None),
        ))).all()
        for row in rows:
            row.deleted_at = datetime.now(timezone.utc)


async def purge_deleted_oss_files(limit: int = 10) -> None:
    """Idempotent deletion queue: retain tombstones until OSS deletion succeeds."""
    async with session_scope() as session:
        rows = (await session.scalars(select(StoredFile).where(
            StoredFile.storage_backend == "oss", StoredFile.deleted_at.is_not(None),
        ).order_by(StoredFile.deleted_at).limit(limit))).all()
        for row in rows:
            active = await session.scalar(select(StoredFile.id).where(
                StoredFile.user_id == row.user_id, StoredFile.storage_key == row.storage_key,
                StoredFile.storage_backend == "oss", StoredFile.deleted_at.is_(None),
            ).limit(1))
            if active is not None:
                await session.delete(row)
                continue
            try:
                await asyncio.to_thread(get_storage("oss").delete, row.storage_key)
            except Exception:
                print("[storage] OSS 删除暂未完成，将保留记录并重试", flush=True)
                continue
            await session.delete(row)


async def release_uploaded_paths(owner: str, task_id: str, *paths: str | None) -> None:
    for path in paths:
        try:
            ref = material_reference(path)
            await asyncio.to_thread(clear_staged_material, ref, owner=owner, task_id=task_id)
        except Exception:
            print("[storage] 持久化成功后的临时文件清理失败", flush=True)


async def task_material_reference(owner: str, task_id: str, kind: str = "video") -> str | None:
    from ..models import EvalTask
    try:
        uid, tid = uuid.UUID(owner), uuid.UUID(task_id)
    except ValueError:
        return None
    field = {"video": "video_path", "courseware": "courseware_path",
             "syllabus": "syllabus_path", "script": "transcript_path"}.get(kind)
    if field is None:
        return None
    async with session_scope() as session:
        row = await session.scalar(select(EvalTask).where(EvalTask.id == tid, EvalTask.user_id == uid))
        return getattr(row, field, None)
