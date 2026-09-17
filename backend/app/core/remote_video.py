"""安全地把公网视频直链拉取到本地任务存储。

链接可能含有短期签名，因此这个模块不记录、不返回也不持久化原始 URL。
"""

from __future__ import annotations

import asyncio
import ipaddress
import json
import os
import shutil
import socket
import subprocess
import time
from dataclasses import dataclass
from email.message import Message
from pathlib import Path
from typing import Awaitable, Callable
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

import httpx
from fastapi import HTTPException

from .storage import get_storage, random_filename, user_task_key

ALLOWED_VIDEO_EXT = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"}
VIDEO_MIME_EXT = {
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "video/x-matroska": ".mkv",
    "video/x-msvideo": ".avi",
    "video/webm": ".webm",
    "video/x-flv": ".flv",
    "video/x-ms-wmv": ".wmv",
}
REDIRECT_CODES = {301, 302, 303, 307, 308}
DEFAULT_MAX_BYTES = 10 * 1024 * 1024 * 1024
DEFAULT_MIN_FREE_BYTES = 5 * 1024 * 1024 * 1024
DEFAULT_MAX_DURATION_SEC = 4 * 60 * 60
CHUNK_BYTES = 1024 * 1024

ProgressCallback = Callable[[int, int | None], Awaitable[None]]


@dataclass(frozen=True)
class RemoteVideo:
    path: str
    storage_key: str
    filename: str
    mime_type: str | None
    size_bytes: int
    duration_sec: float


def _env_int(name: str, default: int) -> int:
    try:
        value = int((os.getenv(name) or "").strip() or default)
    except ValueError:
        return default
    return value if value > 0 else default


def _public_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
        address = address.ipv4_mapped
    return address.is_global


async def _resolve_public_addresses(hostname: str, port: int) -> list[str]:
    try:
        records = await asyncio.to_thread(
            socket.getaddrinfo,
            hostname,
            port,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise HTTPException(400, "视频链接的域名无法解析") from exc
    addresses = sorted({str(record[4][0]) for record in records})
    if not addresses:
        raise HTTPException(400, "视频链接的域名无法解析")
    if any(not _public_ip(address) for address in addresses):
        raise HTTPException(400, "为了安全，不能从本机或内网地址导入视频")
    return addresses


async def validate_remote_url(raw_url: str, *, allowed_origins: frozenset[str] = frozenset()) -> str:
    value = (raw_url or "").strip()
    if not value or len(value) > 2048:
        raise HTTPException(400, "请填写有效的视频直链（最长 2048 个字符）")
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise HTTPException(400, "视频链接格式不正确") from exc
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise HTTPException(400, "只支持 HTTP/HTTPS 视频直链")
    if parsed.username or parsed.password:
        raise HTTPException(400, "视频链接不能在地址中携带账号或密码")
    effective_port = port or (443 if parsed.scheme.lower() == "https" else 80)
    origin = f"{parsed.scheme.lower()}://{parsed.hostname.lower()}:{effective_port}"
    if effective_port not in {80, 443} and origin not in allowed_origins:
        raise HTTPException(400, "视频链接只支持标准 HTTP/HTTPS 端口")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise HTTPException(400, "为了安全，不能从本机或内网地址导入视频")
    await _resolve_public_addresses(hostname, effective_port)
    # 片段标识不会发给服务器，也不应影响重定向基址。
    return urlunsplit((parsed.scheme.lower(), parsed.netloc, parsed.path or "/", parsed.query, ""))


def _safe_filename(response: httpx.Response, url: str, fallback: str = "") -> tuple[str, str]:
    content_type = (response.headers.get("content-type") or "").split(";", 1)[0].strip().lower()
    disposition = response.headers.get("content-disposition") or ""
    filename = ""
    if disposition:
        message = Message()
        message["content-disposition"] = disposition
        filename = message.get_filename() or ""
    if not filename:
        filename = fallback or unquote(Path(urlsplit(url).path).name)
    filename = Path(filename.replace("\\", "/")).name.strip().strip(".")
    filename = "".join(char for char in filename if char >= " " and char != "\x7f")[:180]
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_VIDEO_EXT:
        suffix = VIDEO_MIME_EXT.get(content_type, "")
        stem = Path(filename).stem.strip() if filename else ""
        filename = f"{stem or '链接视频'}{suffix}"
    if suffix not in ALLOWED_VIDEO_EXT:
        raise HTTPException(400, "链接未提供可识别的视频格式")
    if content_type.startswith("text/") or content_type in {
        "application/json",
        "application/xml",
        "application/xhtml+xml",
    }:
        raise HTTPException(
            400, "该地址返回的是网页而不是视频，请使用可直接下载的链接"
        )
    return filename, content_type or None


def _content_length(response: httpx.Response) -> int | None:
    raw = (response.headers.get("content-length") or "").strip()
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value >= 0 else None


def _probe_video(path: Path, max_duration_sec: int) -> float:
    if not shutil.which("ffprobe"):
        raise RuntimeError("服务器未安装 ffprobe，无法校验链接视频")
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-print_format",
                "json",
                "-show_entries",
                "format=duration:stream=codec_type",
                str(path),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        payload = json.loads(result.stdout or "{}")
        duration = float((payload.get("format") or {}).get("duration") or 0)
        has_video = any(item.get("codec_type") == "video" for item in payload.get("streams") or [])
    except (
        OSError,
        subprocess.SubprocessError,
        ValueError,
        TypeError,
        json.JSONDecodeError,
    ) as exc:
        raise HTTPException(400, "无法读取链接中的视频，文件可能已损坏") from exc
    if result.returncode != 0 or not has_video or duration <= 0:
        raise HTTPException(400, "链接内容不是可用的视频文件")
    if duration > max_duration_sec:
        raise HTTPException(400, f"链接视频超过 {max_duration_sec // 3600} 小时限制")
    return duration


async def download_remote_video(
    raw_url: str,
    *,
    user_id: str,
    task_id: str,
    on_progress: ProgressCallback | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
    share_password: str = "",
    share_path: list[str] | None = None,
    share_file_id: str = "",
) -> RemoteVideo:
    """跟随至多 5 次安全重定向，边下载边落盘。

    transport 仅供单元测试注入。
    """
    from .cloud_drives import Download, adapter_for, parse_source

    source = parse_source(raw_url, share_password)
    current_url = await validate_remote_url(source.url)
    max_bytes = _env_int("REMOTE_VIDEO_MAX_BYTES", DEFAULT_MAX_BYTES)
    min_free_bytes = _env_int("REMOTE_VIDEO_MIN_FREE_BYTES", DEFAULT_MIN_FREE_BYTES)
    max_duration_sec = _env_int("REMOTE_VIDEO_MAX_DURATION_SEC", DEFAULT_MAX_DURATION_SEC)
    timeout = httpx.Timeout(connect=20, read=120, write=30, pool=20)
    headers = {
        "Accept": "video/*,application/octet-stream;q=0.8,*/*;q=0.1",
        "Accept-Encoding": "identity",
        "User-Agent": "PKU-AskEdu-Video-Importer/1.0",
    }
    dest: Path | None = None
    completed = False
    try:
        async with httpx.AsyncClient(
            follow_redirects=False,
            timeout=timeout,
            trust_env=False,
            transport=transport,
        ) as client:
            resolved = Download(current_url)
            if source.provider != "direct":
                if on_progress:
                    await on_progress(0, None)
                async with asyncio.timeout(120):
                    try:
                        adapter = adapter_for(source, client)
                        selected = await adapter.select(share_path or [], share_file_id)
                        if selected.size is not None and selected.size > max_bytes:
                            raise HTTPException(400, f"链接视频超过 {max_bytes // (1024 ** 3)} GB 限制")
                        resolved = await adapter.download(selected)
                    except (KeyError, TypeError, ValueError, AttributeError):
                        raise HTTPException(400, "网盘返回的下载信息不完整或格式已变化") from None
                current_url = await validate_remote_url(resolved.url, allowed_origins=resolved.allowed_origins)
                if on_progress:
                    await on_progress(0, selected.size)
            # API cookies must never accompany a CDN request or a cross-origin redirect.
            client.cookies.clear()
            for redirect_count in range(6):
                async with client.stream("GET", current_url, headers={**headers, **resolved.headers_for(current_url)}) as response:
                    if response.status_code in REDIRECT_CODES:
                        location = response.headers.get("location")
                        if not location:
                            raise HTTPException(400, "视频链接重定向缺少目标地址")
                        if redirect_count >= 5:
                            raise HTTPException(400, "视频链接重定向次数过多")
                        current_url = await validate_remote_url(urljoin(current_url, location), allowed_origins=resolved.allowed_origins)
                        continue
                    if response.status_code != 200:
                        raise HTTPException(
                            400, f"视频地址下载失败（HTTP {response.status_code}）"
                        )

                    filename, mime_type = _safe_filename(response, current_url, resolved.filename)
                    total = _content_length(response)
                    if total == 0:
                        raise HTTPException(400, "链接中的视频文件为空")
                    if total is not None and total > max_bytes:
                        raise HTTPException(
                            400, f"链接视频超过 {max_bytes // (1024 ** 3)} GB 限制"
                        )

                    storage = get_storage("local")
                    storage_key = user_task_key(
                        user_id,
                        task_id,
                        random_filename(Path(filename).suffix.lower()),
                    )
                    dest = storage.path_for(storage_key)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    free_bytes = shutil.disk_usage(dest.parent).free
                    required = (total or 0) + min_free_bytes
                    if total is not None and free_bytes < required:
                        raise HTTPException(
                            507, "服务器存储空间不足，暂时无法导入该视频"
                        )

                    downloaded = 0
                    last_reported_at = 0.0
                    with open(dest, "wb") as output:
                        async for chunk in response.aiter_bytes(CHUNK_BYTES):
                            if not chunk:
                                continue
                            downloaded += len(chunk)
                            if downloaded > max_bytes:
                                raise HTTPException(
                                    400,
                                    f"链接视频超过 {max_bytes // (1024 ** 3)} GB 限制",
                                )
                            if shutil.disk_usage(dest.parent).free < min_free_bytes:
                                raise HTTPException(
                                    507, "服务器存储空间不足，已停止导入"
                                )
                            output.write(chunk)
                            now = time.monotonic()
                            if on_progress and (
                                now - last_reported_at >= 0.8 or downloaded == total
                            ):
                                await on_progress(downloaded, total)
                                last_reported_at = now
                    if downloaded == 0:
                        raise HTTPException(400, "链接中的视频文件为空")
                    if total is not None and downloaded != total:
                        raise HTTPException(400, "视频下载不完整，请稍后重试")
                    duration = await asyncio.to_thread(_probe_video, dest, max_duration_sec)
                    completed = True
                    return RemoteVideo(
                        path=str(dest),
                        storage_key=storage_key,
                        filename=filename,
                        mime_type=mime_type,
                        size_bytes=downloaded,
                        duration_sec=duration,
                    )
            raise HTTPException(400, "视频链接重定向次数过多")
    except (httpx.TimeoutException, TimeoutError) as exc:
        raise HTTPException(408, "服务器下载视频超时，请检查链接后重试") from exc
    except httpx.RequestError as exc:
        raise HTTPException(400, "服务器无法连接该视频地址") from exc
    finally:
        if dest is not None and not completed:
            dest.unlink(missing_ok=True)
