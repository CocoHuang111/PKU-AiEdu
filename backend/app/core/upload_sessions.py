from __future__ import annotations

import asyncio
import hashlib
import json
import math
import os
import secrets
import shutil
import zipfile
from collections.abc import AsyncIterable
from pathlib import Path
from typing import Any

from fastapi import HTTPException

from ai_engine.config import settings

from .browser_evidence import (
    AUDIO_EXT,
    AUDIO_MAX_BYTES,
    MAX_UNPACKED_BYTES,
    parse_manifest,
)
from .storage import get_storage, random_filename, user_task_key


DEFAULT_CHUNK_BYTES = 8 * 1024 * 1024
MAX_CHUNK_BYTES = 12 * 1024 * 1024
MAX_ORIGINAL_BYTES = 20 * 1024 * 1024 * 1024
MAX_FRAME_ARCHIVE_BYTES = 150 * 1024 * 1024
SESSION_VERSION = 1


def _task_dir(user_id: str, task_id: str) -> Path:
    root = settings.upload_dir.resolve()
    path = (root / user_id / task_id).resolve()
    if path.parent != (root / user_id).resolve():
        raise HTTPException(400, "非法上传任务路径")
    return path


def _session_dir(user_id: str, task_id: str) -> Path:
    return _task_dir(user_id, task_id) / ".resumable"


def _session_path(user_id: str, task_id: str) -> Path:
    return _session_dir(user_id, task_id) / "session.json"


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{secrets.token_hex(6)}.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(409, "上传会话已损坏，请重新创建任务") from exc
    if not isinstance(value, dict):
        raise HTTPException(409, "上传会话已损坏，请重新创建任务")
    return value


def _part_dir(user_id: str, task_id: str, kind: str) -> Path:
    return _session_dir(user_id, task_id) / kind


def _part_path(user_id: str, task_id: str, kind: str, index: int) -> Path:
    return _part_dir(user_id, task_id, kind) / f"{index:06d}.part"


def _part_meta_path(user_id: str, task_id: str, kind: str, index: int) -> Path:
    return _part_dir(user_id, task_id, kind) / f"{index:06d}.json"


def _allowed_kinds(session: dict[str, Any]) -> set[str]:
    return {"video"} if session["mode"] == "original" else {"audio", "frames"}


def _received(user_id: str, task_id: str, session: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for kind in sorted(_allowed_kinds(session)):
        items: list[dict[str, Any]] = []
        part_root = _part_dir(user_id, task_id, kind)
        if part_root.is_dir():
            for metadata_path in sorted(part_root.glob("*.json")):
                try:
                    index = int(metadata_path.stem)
                    metadata = _read_json(metadata_path)
                    part = _part_path(user_id, task_id, kind, index)
                    size = int(metadata.get("size", -1))
                    digest = str(metadata.get("sha256") or "")
                    if part.is_file() and part.stat().st_size == size and len(digest) == 64:
                        items.append({"index": index, "size": size, "sha256": digest})
                except (HTTPException, OSError, ValueError):
                    continue
        result[kind] = items
    return result


def session_status(user_id: str, task_id: str) -> dict[str, Any]:
    path = _session_path(user_id, task_id)
    if not path.is_file():
        raise HTTPException(404, "上传会话不存在")
    session = _read_json(path)
    received = _received(user_id, task_id, session)
    uploaded_bytes = sum(item["size"] for values in received.values() for item in values)
    return {
        **session,
        "received": received,
        "uploaded_bytes": uploaded_bytes,
    }


def create_session(
    user_id: str,
    task_id: str,
    *,
    mode: str,
    fingerprint: str,
    original_filename: str,
    original_size: int,
    audio_filename: str | None = None,
    audio_mime: str | None = None,
) -> dict[str, Any]:
    if mode not in {"original", "evidence"}:
        raise HTTPException(400, "不支持的上传模式")
    if not 1 <= original_size <= MAX_ORIGINAL_BYTES:
        raise HTTPException(400, "原视频大小无效或超过20GB")
    if len(fingerprint) != 64 or any(c not in "0123456789abcdef" for c in fingerprint.lower()):
        raise HTTPException(400, "文件指纹无效")
    if mode == "evidence":
        suffix = Path(audio_filename or "").suffix.lower()
        if suffix not in AUDIO_EXT:
            raise HTTPException(400, "快速上传的音频格式无效")

    path = _session_path(user_id, task_id)
    identity = {
        "mode": mode,
        "fingerprint": fingerprint.lower(),
        "original_filename": Path(original_filename).name,
        "original_size": original_size,
        "audio_filename": Path(audio_filename).name if audio_filename else None,
        "audio_mime": (audio_mime or "application/octet-stream")[:128] if audio_filename else None,
    }
    if path.is_file():
        existing = _read_json(path)
        if all(existing.get(key) == value for key, value in identity.items()):
            return session_status(user_id, task_id)
        raise HTTPException(409, "任务已有另一个上传会话，请重新创建任务")

    data = {
        "version": SESSION_VERSION,
        "session_id": secrets.token_urlsafe(24),
        "chunk_size": DEFAULT_CHUNK_BYTES,
        **identity,
    }
    if mode == "original":
        data["video_parts"] = math.ceil(original_size / DEFAULT_CHUNK_BYTES)
    _atomic_json(path, data)
    return session_status(user_id, task_id)


def _validate_session_token(session: dict[str, Any], token: str | None) -> None:
    if not token or not secrets.compare_digest(str(session.get("session_id") or ""), token):
        raise HTTPException(409, "上传会话已变化，请刷新后重试")


async def save_part(
    user_id: str,
    task_id: str,
    *,
    kind: str,
    index: int,
    session_token: str | None,
    expected_sha256: str,
    chunks: AsyncIterable[bytes],
) -> dict[str, Any]:
    session = session_status(user_id, task_id)
    _validate_session_token(session, session_token)
    if kind not in _allowed_kinds(session):
        raise HTTPException(400, "该上传模式不接受这种分片")
    if index < 0 or index > 100_000:
        raise HTTPException(400, "分片序号无效")
    if kind == "video" and index >= int(session["video_parts"]):
        raise HTTPException(400, "原视频分片序号超出范围")
    digest_text = expected_sha256.lower()
    if len(digest_text) != 64 or any(c not in "0123456789abcdef" for c in digest_text):
        raise HTTPException(400, "分片校验值无效")

    final_path = _part_path(user_id, task_id, kind, index)
    metadata_path = _part_meta_path(user_id, task_id, kind, index)
    if final_path.is_file() and metadata_path.is_file():
        existing = _read_json(metadata_path)
        if existing.get("sha256") == digest_text and final_path.stat().st_size == existing.get("size"):
            return {"ok": True, "duplicate": True, "index": index, **existing}

    final_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = final_path.with_name(f".{final_path.name}.{secrets.token_hex(6)}.tmp")
    digest = hashlib.sha256()
    size = 0
    try:
        with temporary.open("wb") as target:
            async for chunk in chunks:
                if not chunk:
                    continue
                size += len(chunk)
                if size > MAX_CHUNK_BYTES:
                    raise HTTPException(413, "单个上传分片超过12MB")
                digest.update(chunk)
                target.write(chunk)
        if size <= 0:
            raise HTTPException(400, "上传分片为空")
        if kind == "video":
            chunk_size = int(session["chunk_size"])
            expected_size = min(
                chunk_size,
                int(session["original_size"]) - index * chunk_size,
            )
            if size != expected_size:
                raise HTTPException(400, "原视频分片大小与会话不一致")
        if digest.hexdigest() != digest_text:
            raise HTTPException(400, "上传分片校验失败，请重试")
        os.replace(temporary, final_path)
        metadata = {"size": size, "sha256": digest_text}
        _atomic_json(metadata_path, metadata)
        status = session_status(user_id, task_id)
        kind_total = sum(item["size"] for item in status["received"][kind])
        kind_limit = {
            "video": int(session["original_size"]),
            "audio": AUDIO_MAX_BYTES,
            "frames": MAX_FRAME_ARCHIVE_BYTES,
        }[kind]
        if kind_total > kind_limit:
            final_path.unlink(missing_ok=True)
            metadata_path.unlink(missing_ok=True)
            raise HTTPException(413, "上传分片累计大小超过限制")
        return {"ok": True, "duplicate": False, "index": index, **metadata}
    finally:
        temporary.unlink(missing_ok=True)


def _require_parts(
    user_id: str,
    task_id: str,
    session: dict[str, Any],
    kind: str,
    count: int,
    max_bytes: int,
) -> tuple[list[Path], int]:
    received = {item["index"]: item for item in _received(user_id, task_id, session)[kind]}
    expected = set(range(count))
    if set(received) != expected:
        missing = sorted(expected - set(received))[:5]
        raise HTTPException(409, f"上传尚未完成，缺少 {kind} 分片：{missing}")
    total = sum(received[index]["size"] for index in range(count))
    if total <= 0 or total > max_bytes:
        raise HTTPException(400, "分片合计大小无效")
    return [_part_path(user_id, task_id, kind, index) for index in range(count)], total


def _assemble(parts: list[Path], destination: Path) -> None:
    temporary = destination.with_name(f".{destination.name}.assembling")
    temporary.unlink(missing_ok=True)
    try:
        with temporary.open("wb") as target:
            for part in parts:
                with part.open("rb") as source:
                    shutil.copyfileobj(source, target, length=1024 * 1024)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _extract_frame_batches(
    archives: list[Path], frame_root: Path, manifest: dict[str, Any]
) -> None:
    expected = set(manifest.pop("expected_names"))
    seen: set[str] = set()
    unpacked = 0
    frame_root.mkdir(parents=True, exist_ok=False)
    paths: dict[str, str] = {}
    try:
        for archive in archives:
            try:
                bundle = zipfile.ZipFile(archive)
            except zipfile.BadZipFile as exc:
                raise HTTPException(400, "浏览器画面分片已损坏") from exc
            with bundle:
                for item in bundle.infolist():
                    if item.is_dir():
                        continue
                    name = item.filename
                    if name not in expected or name in seen or item.file_size <= 0:
                        raise HTTPException(400, "浏览器画面分片与清单不一致")
                    unpacked += item.file_size
                    if unpacked > MAX_UNPACKED_BYTES:
                        raise HTTPException(400, "浏览器画面证据解压后过大")
                    category, filename = name.split("/", 1)
                    destination = frame_root / category / filename
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.open(item) as source, destination.open("wb") as target:
                        shutil.copyfileobj(source, target, length=1024 * 1024)
                    seen.add(name)
                    paths[name] = str(destination)
        if seen != expected:
            raise HTTPException(409, "浏览器画面分片尚未上传完整")
    except Exception:
        shutil.rmtree(frame_root, ignore_errors=True)
        raise

    for group in ("dense_frames", "keyframes"):
        for item in manifest[group]:
            item["path"] = paths[item["name"]]


def complete_session(
    user_id: str,
    task_id: str,
    *,
    session_token: str | None,
    audio_parts: int | None = None,
    frame_parts: int | None = None,
    raw_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    session = session_status(user_id, task_id)
    _validate_session_token(session, session_token)
    storage = get_storage("local")
    frame_root: Path | None = None
    destination: Path | None = None
    manifest_path: Path | None = None
    try:
        if session["mode"] == "original":
            count = int(session["video_parts"])
            parts, total = _require_parts(
                user_id, task_id, session, "video", count, MAX_ORIGINAL_BYTES
            )
            if total != int(session["original_size"]):
                raise HTTPException(400, "原视频分片总大小与文件不一致")
            suffix = Path(session["original_filename"]).suffix.lower()
            filename = random_filename(suffix)
            key = user_task_key(user_id, task_id, filename)
            destination = storage.path_for(key)
            destination.parent.mkdir(parents=True, exist_ok=True)
            _assemble(parts, destination)
            result = {
                "path": str(destination),
                "storage_key": key,
                "original_filename": session["original_filename"],
                "mime_type": None,
                "mode": "original",
                "size": total,
            }
        else:
            if not audio_parts or not frame_parts or not raw_manifest:
                raise HTTPException(400, "快速上传完成信息不完整")
            manifest = parse_manifest(json.dumps(raw_manifest, ensure_ascii=False))
            if manifest["original_filename"] != session["original_filename"]:
                raise HTTPException(400, "快速上传清单与会话不一致")
            if int(manifest["original_size"]) != int(session["original_size"]):
                raise HTTPException(400, "快速上传清单与原视频大小不一致")
            audio, audio_size = _require_parts(
                user_id, task_id, session, "audio", audio_parts, AUDIO_MAX_BYTES
            )
            frames, _ = _require_parts(
                user_id, task_id, session, "frames", frame_parts, MAX_FRAME_ARCHIVE_BYTES
            )
            suffix = Path(session["audio_filename"]).suffix.lower()
            filename = random_filename(suffix)
            key = user_task_key(user_id, task_id, filename)
            destination = storage.path_for(key)
            destination.parent.mkdir(parents=True, exist_ok=True)
            _assemble(audio, destination)
            frame_root = settings.frame_dir / destination.stem
            _extract_frame_batches(frames, frame_root, manifest)
            manifest_path = destination.parent / "browser-evidence.json"
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            result = {
                "path": str(destination),
                "storage_key": key,
                "original_filename": session["original_filename"],
                "mime_type": session["audio_mime"],
                "mode": "evidence",
                "size": audio_size,
            }
        return result
    except Exception:
        if destination:
            destination.unlink(missing_ok=True)
        if manifest_path:
            manifest_path.unlink(missing_ok=True)
        if frame_root:
            shutil.rmtree(frame_root, ignore_errors=True)
        raise


async def remove_session(user_id: str, task_id: str) -> None:
    await asyncio.to_thread(shutil.rmtree, _session_dir(user_id, task_id), True)
