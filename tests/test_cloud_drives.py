from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from urllib.parse import parse_qs

import httpx
from fastapi import HTTPException

from backend.app.core.cloud_drives import (
    Download, adapter_for, inspect_share, parse_source,
)
from backend.app.core.remote_video import download_remote_video, validate_remote_url
from backend.app.core.storage import LocalStorageBackend

PKU = "https://disk.pku.edu.cn/link/ABC123"
BAIDU = "https://pan.baidu.com/s/1abc?pwd=1234"
QUARK = "https://pan.quark.cn/s/abc"
GOOGLE = "https://drive.google.com/file/d/abc/view"


class SourceTests(unittest.TestCase):
    def test_supported_sources_and_share_text(self):
        self.assertEqual(parse_source(PKU).provider, "pku")
        self.assertEqual(parse_source("https://example.com/a.mp4?token=a%2Bb").provider, "direct")
        self.assertEqual(parse_source("我分享的视频 " + PKU + " 提取码：abcd").password, "abcd")
        for prefix in ["anyshare/", "anyshare/zh-cn/", "anyshare/en-us/", "anyshare/en/"]:
            self.assertEqual(parse_source("https://disk.pku.edu.cn/" + prefix + "link/ABC123?title=lesson.mp4").share_id, "ABC123")
        signed = "https://example.com/a.mp4?signature=abc)"
        self.assertEqual(parse_source(signed).url, signed)

    def test_invalid_urls_and_lookalikes(self):
        for url in ["file:///etc/passwd", PKU + " " + QUARK, "https://user:pass@disk.pku.edu.cn/link/a",
                    "https://pan.quark.cn/unknown", "https://pan.baidu.com:9999/s/1abc"]:
            with self.subTest(url=url), self.assertRaises(HTTPException):
                parse_source(url)
        self.assertEqual(parse_source("https://disk.pku.edu.cn.evil.example/link/a").provider, "direct")

    def test_sensitive_headers_are_origin_bound(self):
        data = Download("https://cdn.example/a", credentials={"Cookie": "secret"}, credential_origin="https://cdn.example")
        self.assertEqual(data.headers_for("https://cdn.example/b")["Cookie"], "secret")
        for url in ["https://other.example/a", "http://cdn.example/a", "https://cdn.example.evil/a"]:
            self.assertNotIn("Cookie", data.headers_for(url))


class AdapterTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.dns = patch("backend.app.core.remote_video._resolve_public_addresses", AsyncMock(return_value=["1.1.1.1"]))
        self.dns.start()
        self.env = patch.dict(os.environ, {"BAIDU_NETDISK_COOKIE": "", "QUARK_NETDISK_COOKIE": "", "QUARK_IMPORT_FOLDER_ID": ""})
        self.env.start()
        self.addCleanup(self.dns.stop)
        self.addCleanup(self.env.stop)

    async def resolve(self, url, handler, path=None, file_id=""):
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler), follow_redirects=False) as client:
            adapter = adapter_for(parse_source(url), client)
            selected = await adapter.select(path or [], file_id)
            return await adapter.download(selected)

    def pku_handler(self, request):
        path = request.url.path
        if path.startswith("/api/shared-link/"):
            return httpx.Response(200, json={"type": "anonymous", "password_required": False})
        if path.startswith("/link/"):
            return httpx.Response(302, headers={"set-cookie": "link_token:ABC123=secret; Path=/", "location": "/anyshare/link/ABC123"})
        self.assertEqual(request.headers.get("authorization"), "Bearer secret")
        if path.endswith("entry-item"):
            return httpx.Response(200, json=[{"id": "video", "name": "private\\lesson.mp4", "size": 100, "type": "file", "rev": "r1"}])
        if path.endswith("osdownload"):
            self.assertEqual(json.loads(request.content)["docid"], "video")
            return httpx.Response(200, json={"authrequest": ["GET", "https://cdn.example/signed"], "need_watermark": False})
        self.fail("unexpected endpoint")

    async def test_pku_inspect_and_resolve(self):
        info = await inspect_share(PKU, transport=httpx.MockTransport(self.pku_handler))
        self.assertEqual(info["files"][0]["name"], "lesson.mp4")
        self.assertNotIn("secret", json.dumps(info))
        self.assertNotIn("rev", json.dumps(info))
        link = await self.resolve(PKU, self.pku_handler)
        self.assertEqual(link.filename, "lesson.mp4")

    async def test_pku_protected_share_not_bypassed(self):
        for meta in [{"type": "realname"}, {"type": "anonymous", "verify_mobile": True},
                     {"type": "anonymous", "password_required": True}]:
            with self.assertRaises(HTTPException):
                await inspect_share(PKU, transport=httpx.MockTransport(lambda r: httpx.Response(200, json=meta)))

    async def test_selection_must_belong_to_share(self):
        for path, file_id in [(["unrelated-folder"], ""), ([], "unrelated-file")]:
            with self.assertRaises(HTTPException):
                await self.resolve(PKU, self.pku_handler, path, file_id)

    async def test_pku_directory_navigation_and_selection(self):
        def handler(request):
            if request.url.path.endswith("entry-item"):
                return httpx.Response(200, json=[{"id": "folder", "name": "课程", "type": "dir"}])
            if request.url.path.endswith("dir/list"):
                self.assertEqual(json.loads(request.content)["docid"], "folder")
                return httpx.Response(200, json={"dirs": [], "files": [
                    {"id": "video", "name": "lesson.mp4", "size": 100, "rev": "r1"},
                    {"id": "slides", "name": "slides.pdf", "size": 20}]})
            return self.pku_handler(request)
        root = await inspect_share(PKU, transport=httpx.MockTransport(handler))
        self.assertTrue(root["files"][0]["is_dir"])
        child = await inspect_share(PKU, path=["folder"], transport=httpx.MockTransport(handler))
        self.assertEqual([f["id"] for f in child["files"]], ["video"])
        self.assertTrue(child["download_ready"])
        self.assertEqual((await self.resolve(PKU, handler, ["folder"], "video")).filename, "lesson.mp4")

    async def test_pku_watermark_download_is_rejected(self):
        def handler(request):
            if request.url.path.endswith("osdownload"):
                return httpx.Response(200, json={"authrequest": ["GET", "https://cdn.example/signed"],
                                                "need_watermark": True})
            return self.pku_handler(request)
        with self.assertRaises(HTTPException):
            await self.resolve(PKU, handler)

    async def test_cancellation_prevents_pku_download_resolution(self):
        calls = []
        async def cancelled():
            raise HTTPException(409, "导入已取消")
        def handler(request):
            calls.append(request.url)
            return self.pku_handler(request)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            adapter = adapter_for(parse_source(PKU), client, on_activity=cancelled)
            with self.assertRaises(HTTPException) as error:
                await adapter.select([], "")
        self.assertEqual(error.exception.status_code, 409)
        self.assertEqual(calls, [])

    async def test_malformed_pku_response(self):
        for payload in [{"wrong": "shape"}, []]:
            with self.assertRaises(HTTPException):
                await inspect_share(PKU, transport=httpx.MockTransport(lambda r: httpx.Response(200, json=payload)))

    async def test_unsupported_drives_rejected_without_network(self):
        requests = []
        def handler(request):
            requests.append(request.url)
            return httpx.Response(200, json={})
        for url in [BAIDU, QUARK, GOOGLE]:
            with self.subTest(url=url):
                for action in [inspect_share, download_remote_video]:
                    with self.assertRaises(HTTPException) as error:
                        kwargs = {"user_id": "user", "task_id": "task"} if action is download_remote_video else {}
                        await action(url, transport=httpx.MockTransport(handler), **kwargs)
                    self.assertEqual(error.exception.status_code, 400)
                    self.assertIn("暂不支持", error.exception.detail)
        self.assertEqual(requests, [])

    async def test_provider_page_size_is_bounded(self):
        from backend.app.core import cloud_drives
        with patch.object(cloud_drives, "MAX_PAGE_BYTES", 20), self.assertRaises(HTTPException):
            await inspect_share(PKU, transport=httpx.MockTransport(lambda r: httpx.Response(200, content=b"x" * 30)))

    async def test_pku_storage_port_exception_is_exact_and_opt_in(self):
        allowed = frozenset({"https://diskasu.pku.edu.cn:10002"})
        url = "https://diskasu.pku.edu.cn:10002/signed"
        with self.assertRaises(HTTPException):
            await validate_remote_url(url)
        self.assertEqual(await validate_remote_url(url, allowed_origins=allowed), url)
        for denied in ["http://diskasu.pku.edu.cn:10002/a", "https://evil.example:10002/a", "https://diskasu.pku.edu.cn:10003/a"]:
            with self.assertRaises(HTTPException):
                await validate_remote_url(denied, allowed_origins=allowed)

    async def test_download_integration_no_bearer_or_cookie_leak(self):
        def handler(request):
            if request.url.host == "cdn.example":
                self.assertNotIn("authorization", request.headers)
                self.assertNotIn("cookie", request.headers)
                return httpx.Response(200, headers={"content-type": "application/octet-stream"}, content=b"video")
            return self.pku_handler(request)
        with tempfile.TemporaryDirectory() as tmp, patch("backend.app.core.remote_video.get_storage", return_value=LocalStorageBackend(Path(tmp))), \
             patch("backend.app.core.remote_video._probe_video", return_value=1.0), patch.dict(os.environ, {"REMOTE_VIDEO_MIN_FREE_BYTES": "1"}):
            result = await download_remote_video(PKU, user_id="user", task_id="task", transport=httpx.MockTransport(handler))
            self.assertEqual(result.filename, "lesson.mp4")
            self.assertEqual(Path(result.path).read_bytes(), b"video")


if __name__ == "__main__":
    unittest.main()
