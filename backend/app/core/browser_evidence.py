from __future__ import annotations

import json
import math
import shutil
import zipfile
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile

from ai_engine.config import settings

from .uploads import save_user_upload


AUDIO_EXT = {".m4a", ".webm", ".mp3", ".flac", ".wav", ".mka"}
ARCHIVE_MAX_BYTES = 100 * 1024 * 1024
AUDIO_MAX_BYTES = 1024 * 1024 * 1024
MAX_DURATION_SEC = 4 * 60 * 60
MAX_DENSE_FRAMES = 5000
MAX_UNPACKED_BYTES = 150 * 1024 * 1024


def _number(value: Any, name: str, *, minimum: float, maximum: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise HTTPException(400, f"证据清单中的 {name} 无效") from exc
    if not minimum <= number <= maximum:
        raise HTTPException(400, f"证据清单中的 {name} 超出允许范围")
    return number


def parse_manifest(raw: str | None) -> dict[str, Any]:
    try:
        manifest = json.loads(raw or "")
    except json.JSONDecodeError as exc:
        raise HTTPException(400, "浏览器证据清单不是有效JSON") from exc
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise HTTPException(400, "不支持的浏览器证据清单版本")

    filename = str(manifest.get("original_filename") or "").strip()
    if not filename or len(filename) > 512:
        raise HTTPException(400, "浏览器证据清单缺少原视频文件名")
    duration = _number(
        manifest.get("duration_sec"),
        "duration_sec",
        minimum=1,
        maximum=MAX_DURATION_SEC,
    )
    interval = _number(
        manifest.get("interval_sec"),
        "interval_sec",
        minimum=1,
        maximum=15,
    )
    original_size = int(
        _number(
            manifest.get("original_size"),
            "original_size",
            minimum=1,
            maximum=20 * 1024 * 1024 * 1024,
        )
    )

    dense = manifest.get("dense_frames")
    keys = manifest.get("keyframes")
    expected_dense_count = min(math.ceil(duration / interval), MAX_DENSE_FRAMES)
    if not isinstance(dense, list) or len(dense) != expected_dense_count:
        raise HTTPException(400, "浏览器证据包的密集画面数量无效")
    if not isinstance(keys, list) or len(keys) != 12:
        raise HTTPException(400, "浏览器证据包的关键画面数量无效")

    expected_dense = []
    normalized_dense = []
    for index, item in enumerate(dense):
        if not isinstance(item, dict):
            raise HTTPException(400, "浏览器证据包的密集画面信息无效")
        name = f"dense/{index:05d}.jpg"
        if item.get("name") != name:
            raise HTTPException(400, "浏览器证据包的密集画面顺序无效")
        timestamp = _number(item.get("time_sec"), "time_sec", minimum=0, maximum=duration)
        if abs(timestamp - index * interval) > 0.05:
            raise HTTPException(400, "浏览器证据包的密集画面时间戳无效")
        expected_dense.append(name)
        normalized_dense.append({"name": name, "time_sec": timestamp})

    expected_keys = []
    normalized_keys = []
    previous_timestamp = -1.0
    for index, item in enumerate(keys):
        if not isinstance(item, dict):
            raise HTTPException(400, "浏览器证据包的关键画面信息无效")
        name = f"key/{index:02d}.jpg"
        if item.get("name") != name:
            raise HTTPException(400, "浏览器证据包的关键画面顺序无效")
        timestamp = _number(item.get("time_sec"), "time_sec", minimum=0, maximum=duration)
        if timestamp <= previous_timestamp:
            raise HTTPException(400, "浏览器证据包的关键画面时间戳顺序无效")
        previous_timestamp = timestamp
        expected_keys.append(name)
        normalized_keys.append({"name": name, "time_sec": timestamp})

    return {
        "version": 1,
        "original_filename": Path(filename).name,
        "original_size": original_size,
        "duration_sec": duration,
        "interval_sec": interval,
        "audio_codec": str(manifest.get("audio_codec") or "unknown")[:32],
        "dense_frames": normalized_dense,
        "keyframes": normalized_keys,
        "expected_names": expected_dense + expected_keys,
    }


def _extract_archive(archive_path: str, frame_root: Path, manifest: dict[str, Any]) -> None:
    expected = set(manifest.pop("expected_names"))
    try:
        with zipfile.ZipFile(archive_path) as bundle:
            members = [item for item in bundle.infolist() if not item.is_dir()]
            names = {item.filename for item in members}
            if names != expected or len(members) != len(expected):
                raise HTTPException(400, "浏览器证据压缩包与清单不一致")
            if any(item.file_size <= 0 for item in members):
                raise HTTPException(400, "浏览器证据压缩包包含空图片")
            if sum(item.file_size for item in members) > MAX_UNPACKED_BYTES:
                raise HTTPException(400, "浏览器证据压缩包解压后过大")

            frame_root.mkdir(parents=True, exist_ok=False)
            paths: dict[str, str] = {}
            for item in members:
                category, filename = item.filename.split("/", 1)
                destination_dir = frame_root / category
                destination_dir.mkdir(exist_ok=True)
                destination = destination_dir / filename
                with bundle.open(item) as source, destination.open("wb") as target:
                    shutil.copyfileobj(source, target, length=1024 * 1024)
                paths[item.filename] = str(destination)
    except zipfile.BadZipFile as exc:
        raise HTTPException(400, "浏览器证据压缩包已损坏") from exc

    for group in ("dense_frames", "keyframes"):
        for item in manifest[group]:
            item["path"] = paths[item["name"]]


def save_browser_evidence(
    *,
    audio: UploadFile,
    archive: UploadFile,
    raw_manifest: str | None,
    user_id: str,
    task_id: str,
) -> tuple[str, str, dict[str, Any]]:
    manifest = parse_manifest(raw_manifest)
    audio_path: str | None = None
    archive_path: str | None = None
    frame_root: Path | None = None
    try:
        audio_path, audio_key = save_user_upload(
            audio,
            user_id=user_id,
            task_id=task_id,
            purpose="video",
            allowed=AUDIO_EXT,
            max_bytes=AUDIO_MAX_BYTES,
            kind_label="原始音轨",
        )
        archive_path, _ = save_user_upload(
            archive,
            user_id=user_id,
            task_id=task_id,
            purpose="browser_evidence",
            allowed={".zip"},
            max_bytes=ARCHIVE_MAX_BYTES,
            kind_label="浏览器画面证据包",
        )
        frame_root = settings.frame_dir / Path(audio_path).stem
        _extract_archive(archive_path, frame_root, manifest)
        manifest_path = Path(audio_path).parent / "browser-evidence.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        Path(archive_path).unlink(missing_ok=True)
        return audio_path, audio_key, manifest
    except Exception:
        if audio_path:
            Path(audio_path).unlink(missing_ok=True)
        if archive_path:
            Path(archive_path).unlink(missing_ok=True)
        if frame_root and frame_root.is_dir():
            shutil.rmtree(frame_root, ignore_errors=True)
        raise
