"""Share-page adapters. Tokens and download URLs never leave the server.

Only anonymous public PKU shares and ordinary video direct URLs are enabled.
Only share-listed files may be selected; authentication is never bypassed.
"""
from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from urllib.parse import parse_qs, urlsplit

import httpx
from fastapi import HTTPException

from .remote_video import (
    ALLOWED_VIDEO_EXT, PublicNetworkTransport,
    validate_remote_url,
)

NAMES = {"pku": "北大网盘", "baidu": "百度网盘", "quark": "夸克网盘", "google": "Google Drive", "direct": "视频直链"}
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
MAX_PAGE_BYTES = 4 * 1024 * 1024


@dataclass
class Source:
    provider: str
    url: str = field(repr=False)
    share_id: str = ""
    password: str = field(default="", repr=False)
    resource_key: str = field(default="", repr=False)
    folder: bool = False


def parse_source(text: str, password: str = "") -> Source:
    if not text or len(text) > 8192 or len(password) > 128:
        raise HTTPException(400, "分享链接或提取码过长")
    matches = re.findall(r'https?://[^\s<>"，。；）]+', text, flags=re.I)
    if len(matches) != 1:
        raise HTTPException(400, "请一次填写一个 HTTP/HTTPS 视频链接")
    url = matches[0] if matches[0] == text.strip() else matches[0].rstrip(")]")
    try:
        p = urlsplit(url)
        if p.username or p.password or p.port not in (None, 80, 443):
            raise ValueError()
    except ValueError:
        raise HTTPException(400, "分享链接格式不正确") from None
    host = (p.hostname or "").lower()
    query = parse_qs(p.query)
    code = re.search(r"(?:提取码|访问码|密码)\s*[:：]?\s*([\w-]{1,32})", text)
    password = password.strip() or query.get("pwd", [""])[0] or (code[1] if code else "")
    provider, identity, folder = "direct", "", False
    if host == "disk.pku.edu.cn":
        provider = "pku"
        match = re.fullmatch(r"/(?:anyshare/(?:[A-Za-z]{2}(?:-[A-Za-z]{2})?/)?)?link/([A-Za-z0-9_-]+)/*", p.path)
        identity = match[1] if match else ""
    elif host in {"pan.baidu.com", "yun.baidu.com"}:
        provider = "baidu"
        match = re.fullmatch(r"/s/1([A-Za-z0-9_-]+)/*", p.path)
        identity = match[1] if match else query.get("surl", [""])[0]
    elif host == "pan.quark.cn":
        provider = "quark"
        match = re.fullmatch(r"/s/([A-Za-z0-9_-]+)/*", p.path)
        identity = match[1] if match else ""
    elif host in {"drive.google.com", "docs.google.com"}:
        provider = "google"
        match = re.search(r"/(?:file/d|drive/(?:u/\d+/)?folders)/([A-Za-z0-9_-]+)", p.path)
        identity = match[1] if match else query.get("id", [""])[0]
        folder = "/folders/" in p.path
    if provider not in {"pku", "direct"}:
        raise HTTPException(400, f"暂不支持{NAMES[provider]}，请使用北大网盘公开分享或本地上传")
    if provider != "direct" and not re.fullmatch(r"[A-Za-z0-9_-]{1,200}", identity):
        raise HTTPException(400, f"无法识别{NAMES[provider]}分享地址，请复制完整分享链接")
    return Source(provider, url, identity, password, query.get("resourcekey", [""])[0], folder)


@dataclass
class ShareFile:
    id: str
    name: str
    size: int | None = None
    is_dir: bool = False
    private: dict = field(default_factory=dict, repr=False)

    def public(self):
        return {"id": self.id, "name": self.name, "size": self.size, "is_dir": self.is_dir,
                "is_video": not self.is_dir and PurePosixPath(self.name).suffix.lower() in ALLOWED_VIDEO_EXT}


@dataclass
class Download:
    url: str = field(repr=False)
    filename: str = ""
    headers: dict = field(default_factory=dict, repr=False)
    # Sensitive headers are allowed only on this exact origin. Redirects lose them.
    credential_origin: str = ""
    credentials: dict = field(default_factory=dict, repr=False)
    allowed_origins: frozenset[str] = frozenset()

    def headers_for(self, url: str) -> dict:
        p = urlsplit(url)
        origin = f"{p.scheme}://{p.netloc}"
        return {**self.headers, **(self.credentials if origin == self.credential_origin else {})}


def _name(value):
    return PurePosixPath(str(value).replace("\\", "/")).name[:180]


class Adapter:
    def __init__(self, source: Source, client: httpx.AsyncClient, on_activity=None):
        self.source, self.client = source, client
        self.calls = 0
        self.on_activity = on_activity

    def fail(self, message, status=400):
        raise HTTPException(status, f"{NAMES[self.source.provider]}：{message}")

    async def request(self, method, url, **kwargs):
        if self.on_activity:
            await self.on_activity()
        self.calls += 1
        if self.calls > 100:
            self.fail("目录过大或请求过多，请分享较小的子目录")
        url = await validate_remote_url(url)
        headers = {"User-Agent": UA, **kwargs.pop("headers", {})}
        async with self.client.stream(method, url, headers=headers, **kwargs) as response:
            body = bytearray()
            async for chunk in response.aiter_bytes(64 * 1024):
                body.extend(chunk)
                if len(body) > MAX_PAGE_BYTES:
                    self.fail("分享页面过大，暂时无法解析")
            if response.status_code not in {200, 301, 302, 303, 307, 308}:
                self.fail(f"请求失败（HTTP {response.status_code}），请检查分享权限或稍后重试")
            headers = dict(response.headers)
            headers.pop("content-encoding", None)
            headers.pop("content-length", None)
            return httpx.Response(response.status_code, headers=headers, content=bytes(body), request=response.request)

    async def json(self, method, url, **kwargs):
        response = await self.request(method, url, **kwargs)
        try:
            result = response.json()
            if not isinstance(result, (dict, list)):
                raise ValueError()
            return result
        except ValueError:
            self.fail("未返回文件信息，可能需要登录或验证码")

    async def list(self, folder=None):
        raise NotImplementedError

    async def walk(self, path):
        if len(path) > 12 or any(not isinstance(v, str) or len(v) > 2048 for v in path):
            self.fail("目录路径无效或过深")
        entries = await self.list()
        for identity in path:
            item = next((f for f in entries if f.id == identity and f.is_dir), None)
            if item is None:
                self.fail("所选目录不属于此分享，请重新读取链接")
            entries = await self.list(item)
        return entries

    async def select(self, path, file_id):
        entries = [f for f in await self.walk(path) if f.public()["is_video"]]
        if file_id:
            entries = [f for f in entries if f.id == file_id]
        if len(entries) != 1:
            self.fail("请先读取链接并选择一个视频文件")
        return entries[0]


class Pku(Adapter):
    base = "https://disk.pku.edu.cn"

    async def start(self):
        meta = await self.json("GET", f"{self.base}/api/shared-link/v1/links/{self.source.share_id}")
        if meta.get("verify_mobile") or meta.get("type") != "anonymous":
            self.fail("该分享需要身份验证，请使用已获授权的公开分享或上传本地文件")
        if meta.get("password_required"):
            self.fail("该分享需要访问密码；密码验证接口尚待验证，请暂时上传本地文件")
        await self.request("GET", f"{self.base}/link/{self.source.share_id}")
        token = self.client.cookies.get("link_token:" + self.source.share_id)
        if not token:
            self.fail("无法获得分享访问凭证，链接可能已失效或需要登录")
        self.auth = {"Authorization": "Bearer " + token}

    async def list(self, folder=None):
        if not hasattr(self, "auth"):
            await self.start()
        if folder is None:
            raw = await self.json("GET", self.base + "/api/efast/v1/entry-item", headers=self.auth)
        else:
            raw = await self.json("POST", self.base + "/api/efast/v1/dir/list", headers=self.auth,
                                  json={"docid": folder.id, "by": "name", "sort": "asc"})
            raw = [*({**v, "type": "dir"} for v in raw.get("dirs", [])),
                   *({**v, "type": "file"} for v in raw.get("files", []))]
        return [ShareFile(str(v.get("id") or v.get("docid")), _name(v["name"]), v.get("size"),
                          v.get("type") in {"dir", "folder"} or "size" not in v, v) for v in raw]

    async def download(self, item):
        data = await self.json("POST", self.base + "/api/efast/v1/file/osdownload", headers=self.auth,
                               json={"docid": item.id, "authtype": "QUERY_STRING", "savename": item.name,
                                     "usehttps": True, "rev": item.private.get("rev", "")})
        request = data.get("authrequest") or []
        if len(request) < 2 or request[0] != "GET" or data.get("need_watermark"):
            self.fail("此文件不允许原文件下载或需要网盘水印处理")
        # Verified AnyShare object storage endpoint. This exception is not
        # available to raw/direct URL inputs or other providers.
        return Download(request[1], item.name, allowed_origins=frozenset({"https://diskasu.pku.edu.cn:10002"}))




def adapter_for(source, client, on_activity=None):
    if source.provider != "pku":
        raise HTTPException(400, "网盘导入目前仅支持北大网盘公开分享")
    return Pku(source, client, on_activity)




async def inspect_share(raw_url, password="", path=None, *, transport=None):
    source = parse_source(raw_url, password)
    try:
        network = transport if transport is not None else PublicNetworkTransport()
        async with asyncio.timeout(90), httpx.AsyncClient(follow_redirects=False, trust_env=False, timeout=20, transport=network) as client:
            if source.provider == "direct":
                await validate_remote_url(source.url)
                return {"provider": "direct", "provider_name": NAMES["direct"], "files": [], "notice": "服务器将在导入时检查视频格式和大小", "download_ready": True, "configuration_message": ""}
            files = await adapter_for(source, client).walk(path or [])
            notice = "请选择要导入的视频"
            return {"provider": source.provider, "provider_name": NAMES[source.provider],
                    "files": [f.public() for f in files if f.is_dir or f.public()["is_video"]], "notice": notice,
                    "download_ready": True, "configuration_message": ""}
    except (httpx.RequestError, TimeoutError):
        raise HTTPException(408, "网盘连接失败或超时，请稍后重试") from None
    except (KeyError, TypeError, ValueError, AttributeError):
        raise HTTPException(400, "网盘返回的文件信息不完整或格式已变化，请稍后重试") from None
