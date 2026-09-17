"""Share-page adapters. Tokens and download URLs never leave the server.

Only share-listed files may be selected. Account credentials are opt-in admin
configuration, sent to fixed provider API origins, never arbitrary redirects.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from http.cookies import SimpleCookie
from pathlib import PurePosixPath
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit

import httpx
from fastapi import HTTPException

from .remote_video import (
    ALLOWED_VIDEO_EXT, PublicNetworkTransport, _content_length, _safe_filename,
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


class Baidu(Adapter):
    base = "https://pan.baidu.com"

    def auth(self):
        cookie = os.getenv("BAIDU_NETDISK_COOKIE", "").strip()
        return {"User-Agent": "netdisk", **({"Cookie": cookie} if cookie else {})}

    async def api(self, method, path, **kwargs):
        data = await self.json(method, self.base + path, headers=self.auth(), **kwargs)
        if data.get("errno") != 0:
            self.fail("分享验证失败，请检查提取码、有效期和账号权限；如需验证码，请在网盘完成验证后重试")
        return data

    async def list(self, folder=None):
        entries = []
        for page in range(1, 21):
            result = await self.api("POST", "/share/wxlist?channel=weixin&version=2.2.2&clienttype=25&web=1",
                                   data={"shorturl": self.source.share_id, "pwd": self.source.password,
                                         "root": "0" if folder else "1", "dir": folder.private["path"] if folder else "",
                                         "page": str(page), "num": "100", "order": "time"})
            data = result.get("data") or {}
            if folder is None:
                self.share = {**getattr(self, "share", {}), **data}
            values = data.get("list") or []
            entries.extend(ShareFile(str(v["fs_id"]), _name(v["server_filename"]), v.get("size"),
                                     str(v.get("isdir")) == "1", v) for v in values)
            if not (data.get("has_more") or data.get("more")):
                return entries
            if not values:
                break
        self.fail("目录文件过多，请分享视频文件或较小的子目录")

    async def download(self, item):
        if not os.getenv("BAIDU_NETDISK_COOKIE", "").strip():
            self.fail("已识别分享，下载需要管理员配置百度网盘导入账号；也可下载后本地上传", 503)
        data = await self.api("GET", "/share/tplconfig", params={"surl": self.source.share_id,
                              "fields": "sign,timestamp", "channel": "chunlei", "web": "1", "app_id": "250528", "clienttype": "0"})
        sign = data.get("data") or {}
        if not sign.get("sign") or not self.share.get("shareid"):
            self.fail("无法获得下载凭证，请更新导入账号授权")
        result = await self.api("POST", "/api/sharedownload", params={"sign": sign["sign"], "timestamp": sign["timestamp"],
                                "app_id": "250528", "channel": "chunlei", "clienttype": "12", "web": "1"},
                                data={"encrypt": "0", "extra": json.dumps({"sekey": self.share.get("seckey", "")}),
                                      "fid_list": json.dumps([int(item.id)]), "primaryid": str(self.share["shareid"]),
                                      "product": "share", "type": "nolimit", "uk": str(self.share["uk"])})
        links = result.get("list") or []
        if not links or not links[0].get("dlink"):
            self.fail("网盘没有授予下载地址，请检查账号或分享的下载权限")
        return Download(links[0]["dlink"], item.name, {"User-Agent": "netdisk"})


class Quark(Adapter):
    base = "https://drive-pc.quark.cn/1/clouddrive"

    def account_cookie(self):
        parsed = SimpleCookie()
        parsed.load(os.getenv("QUARK_NETDISK_COOKIE", "").strip())
        values = {key: morsel.value for key, morsel in parsed.items()}
        # Quark refreshes __puus on API responses. Use that provider-scoped
        # update during this import; never persist it or expose it to the UI.
        for cookie in self.client.cookies.jar:
            domain = cookie.domain.lstrip(".").lower()
            if domain == "quark.cn" or domain.endswith(".quark.cn"):
                if cookie.name in values:
                    values[cookie.name] = cookie.value
        return "; ".join(f"{key}={value}" for key, value in values.items())

    async def api(self, method, path, authenticated=False, **kwargs):
        headers = {"Referer": "https://pan.quark.cn/"}
        if authenticated:
            headers["Cookie"] = self.account_cookie()
        data = await self.json(method, self.base + path, headers=headers,
                               params={"pr": "ucpro", "fr": "pc", **kwargs.pop("params", {})}, **kwargs)
        if data.get("code") != 0:
            self.fail("请求未获网盘许可，请检查提取码、链接有效期、账号登录状态或验证码")
        return data

    async def list(self, folder=None):
        if not hasattr(self, "token"):
            result = await self.api("POST", "/share/sharepage/token", json={"pwd_id": self.source.share_id, "passcode": self.source.password})
            self.token = (result.get("data") or {}).get("stoken")
            if not self.token:
                self.fail("无法获得分享凭证，请检查提取码")
        entries = []
        for page in range(1, 21):
            result = await self.api("GET", "/share/sharepage/detail", params={"pwd_id": self.source.share_id,
                        "stoken": self.token, "pdir_fid": folder.id if folder else "0", "force": "0",
                        "_page": page, "_size": 50, "_fetch_total": 1, "_sort": "file_type:asc,updated_at:desc", "ver": 2})
            values = (result.get("data") or {}).get("list") or []
            entries.extend(ShareFile(str(v["fid"]), _name(v["file_name"]), v.get("size"), bool(v.get("dir")), v) for v in values)
            total = (result.get("metadata") or {}).get("_total")
            if not values or (total is not None and len(entries) >= int(total)):
                return entries
        self.fail("目录文件过多，请分享视频文件或较小的子目录")

    async def download(self, item):
        folder = os.getenv("QUARK_IMPORT_FOLDER_ID", "").strip()
        cookie = os.getenv("QUARK_NETDISK_COOKIE", "").strip()
        if not folder or not cookie:
            self.fail("已识别分享，下载需要管理员配置夸克导入账号和专用转存目录", 503)
        if not item.private.get("share_fid_token"):
            self.fail("该分享未授予转存权限")
        result = await self.api("POST", "/share/sharepage/save", authenticated=True, json={
            "fid_list": [item.id], "fid_token_list": [item.private["share_fid_token"]],
            "to_pdir_fid": folder, "pwd_id": self.source.share_id, "stoken": self.token,
            "pdir_fid": str(item.private.get("pdir_fid", "0")), "scene": "link"})
        task = (result.get("data") or {}).get("task_id")
        if not task:
            self.fail("转存未创建成功，请检查导入账号剩余空间")
        for attempt in range(30):
            result = await self.api("GET", "/task", authenticated=True, params={"task_id": task, "retry_index": attempt})
            data = result.get("data") or {}
            saved = (data.get("save_as") or {}).get("save_as_top_fids") or []
            if saved:
                result = await self.api("POST", "/file/download", authenticated=True, json={"fids": [saved[0]]})
                links = result.get("data") or []
                if not links or not links[0].get("download_url"):
                    self.fail("转存成功，但网盘未授予下载地址")
                url = links[0]["download_url"]
                p = urlsplit(url)
                # Account cookies are never forwarded to arbitrary download origins.
                trusted = p.scheme == "https" and (p.hostname or "").endswith(".quark.cn")
                return Download(url, item.name, {"User-Agent": UA, "Referer": "https://pan.quark.cn/"},
                                f"https://{p.netloc}" if trusted else "", {"Cookie": self.account_cookie()} if trusted else {})
            if data.get("status") in {2, 3}:
                self.fail("转存任务结束但未返回文件，请检查账号权限或存储空间")
            await asyncio.sleep(1)
        self.fail("转存尚未完成，请稍后重试；文件可能已保存到导入目录")


class GoogleForm(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active, self.action, self.fields = False, "", {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form" and attrs.get("id") == "download-form":
            self.active, self.action = True, attrs.get("action", "")
        if self.active and tag == "input" and attrs.get("name") and attrs.get("type") == "hidden":
            self.fields[attrs["name"]] = attrs.get("value", "")

    def handle_endtag(self, tag):
        if tag == "form":
            self.active = False


class GoogleFolderPage(HTMLParser):
    """Read file links from Google's public embedded folder view, without JS."""
    def __init__(self):
        super().__init__()
        self.links, self.href, self.label = [], None, []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href, self.label = dict(attrs).get("href"), []

    def handle_data(self, data):
        if self.href:
            self.label.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            self.links.append((self.href, "".join(self.label).strip()))
            self.href = None


class Google(Adapter):
    async def list(self, folder=None):
        if self.source.folder:
            params = {"id": folder.id if folder else self.source.share_id}
            key = (folder.private.get("resource_key") if folder else self.source.resource_key)
            if key:
                params["resourcekey"] = key
            response = await self.request("GET", "https://drive.google.com/embeddedfolderview", params=params)
            if response.status_code != 200:
                self.fail("文件夹需要登录，请将分享设置为知道链接的人可查看")
            parser = GoogleFolderPage()
            parser.feed(response.text)
            entries = {}
            for url, name in parser.links:
                p = urlsplit(url)
                if p.scheme != "https" or p.hostname != "drive.google.com":
                    continue
                if not re.search(r"/(?:file/d|drive/(?:u/\d+/)?folders)/[A-Za-z0-9_-]+", p.path):
                    continue
                child = parse_source(url)
                entries[child.share_id] = ShareFile(child.share_id, _name(name), is_dir=child.folder,
                                                  private={"resource_key": child.resource_key})
            if not entries:
                self.fail("未读取到文件；文件夹可能为空、未公开或页面格式已变化")
            return list(entries.values())
        item = ShareFile(self.source.share_id, "")
        resolved, size = await self.resolve_download(item)
        return [ShareFile(item.id, resolved.filename, size, private={"resolved": resolved})]

    async def download(self, item):
        if item.private.get("resolved"):
            return item.private["resolved"]
        return (await self.resolve_download(item))[0]

    async def resolve_download(self, item):
        params = {"id": item.id, "export": "download"}
        key = item.private.get("resource_key") or self.source.resource_key
        if key:
            params["resourcekey"] = key
        current = "https://drive.usercontent.google.com/download?" + urlencode(params)
        for _ in range(6):
            if self.on_activity:
                await self.on_activity()
            await validate_remote_url(current)
            p = urlsplit(current)
            if p.scheme != "https" or not (p.hostname in {"drive.google.com", "docs.google.com", "drive.usercontent.google.com"}
                                           or (p.hostname or "").endswith(".googleusercontent.com")):
                self.fail("下载确认页返回了非 Google 地址，已拒绝访问")
            async with self.client.stream("GET", current, headers={"User-Agent": UA}) as response:
                if response.is_redirect:
                    current = urljoin(current, response.headers.get("location", ""))
                    continue
                if response.status_code != 200:
                    self.fail(f"无法下载（HTTP {response.status_code}），请将文件设为知道链接的人可查看并允许下载")
                content_type = response.headers.get("content-type", "").lower()
                if "text/html" not in content_type:
                    filename, _ = _safe_filename(response, current, item.name)
                    size = _content_length(response)
                    cookie = self.client.build_request("GET", current).headers.get("cookie", "")
                    return Download(current, filename, {"User-Agent": UA},
                                    f"{p.scheme}://{p.netloc}", {"Cookie": cookie} if cookie else {}), size
                body = bytearray()
                async for chunk in response.aiter_bytes(64 * 1024):
                    body.extend(chunk)
                    if len(body) > MAX_PAGE_BYTES:
                        self.fail("下载确认页过大")
            page = body.decode("utf-8", errors="replace")
            parser = GoogleForm()
            parser.feed(page)
            if parser.action:
                current = urljoin(current, unescape(parser.action))
                current += ("&" if "?" in current else "?") + urlencode(parser.fields)
                continue
            href = re.search(r'href=["\'](/uc\?export=download[^"\']+)', page)
            embedded = re.search(r'"downloadUrl"\s*:\s*("(?:\\.|[^"\\])*")', page)
            if href:
                current = urljoin("https://docs.google.com", unescape(href[1]))
            elif embedded:
                current = json.loads(embedded[1])
            else:
                self.fail("文件未开放下载、需要登录或已达到下载配额，请检查分享设置")
        self.fail("下载确认或重定向次数过多")


def adapter_for(source, client, on_activity=None):
    return {"pku": Pku, "baidu": Baidu, "quark": Quark, "google": Google}[source.provider](source, client, on_activity)


def import_readiness(provider):
    if provider == "baidu" and not os.getenv("BAIDU_NETDISK_COOKIE", "").strip():
        return False, "暂未连接百度网盘导入账号，请联系管理员，或下载视频后本地上传"
    if provider == "quark" and not (os.getenv("QUARK_NETDISK_COOKIE", "").strip() and os.getenv("QUARK_IMPORT_FOLDER_ID", "").strip()):
        return False, "暂未连接夸克网盘导入账号，请联系管理员，或下载视频后本地上传"
    return True, ""


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
            if source.provider == "quark":
                notice = "导入时会转存至管理员配置的夸克专用目录，转存文件将保留在该账号中"
            ready, message = import_readiness(source.provider)
            return {"provider": source.provider, "provider_name": NAMES[source.provider],
                    "files": [f.public() for f in files if f.is_dir or f.public()["is_video"]], "notice": notice,
                    "download_ready": ready, "configuration_message": message}
    except (httpx.RequestError, TimeoutError):
        raise HTTPException(408, "网盘连接失败或超时，请稍后重试") from None
    except (KeyError, TypeError, ValueError, AttributeError):
        raise HTTPException(400, "网盘返回的文件信息不完整或格式已变化，请稍后重试") from None
