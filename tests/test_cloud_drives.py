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
    def test_all_providers_and_share_text(self):
        for url, provider in [(PKU, "pku"), (BAIDU, "baidu"), (QUARK, "quark"), (GOOGLE, "google"),
                              ("https://example.com/a.mp4?token=a%2Bb", "direct")]:
            self.assertEqual(parse_source(url).provider, provider)
        self.assertEqual(parse_source("我分享的视频 " + QUARK + " 提取码：abcd").password, "abcd")
        self.assertEqual(parse_source(BAIDU).password, "1234")
        self.assertEqual(parse_source(BAIDU, "override").password, "override")
        self.assertEqual(parse_source("https://pan.baidu.com/share/init?surl=abc").share_id, "abc")
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

    def baidu_handler(self, request):
        if request.url.path.endswith("wxlist"):
            form = parse_qs(request.content.decode(), keep_blank_values=True)
            self.assertEqual(form["pwd"], ["1234"])
            return httpx.Response(200, json={"errno": 0, "data": {"uk": "8", "shareid": "9", "seckey": "secret",
                      "list": [{"fs_id": 123, "server_filename": "lecture.mp4", "isdir": 0, "size": 10, "path": "/lecture.mp4"}]}})
        self.assertEqual(request.headers.get("cookie"), "BDUSS=test")
        if request.url.path.endswith("tplconfig"):
            return httpx.Response(200, json={"errno": 0, "data": {"sign": "sig", "timestamp": 123}})
        if request.url.path.endswith("sharedownload"):
            form = parse_qs(request.content.decode())
            self.assertEqual(json.loads(form["fid_list"][0]), [123])
            self.assertEqual(json.loads(form["extra"][0]), {"sekey": "secret"})
            return httpx.Response(200, json={"errno": 0, "list": [{"dlink": "https://cdn.example/lesson.mp4"}]})
        self.fail("unexpected endpoint")

    async def test_baidu_requires_explicit_account_and_resolves(self):
        info = await inspect_share(BAIDU, transport=httpx.MockTransport(self.baidu_handler))
        self.assertEqual(info["files"][0]["id"], "123")
        self.assertFalse(info["download_ready"])
        self.assertIn("管理员", info["configuration_message"])
        with self.assertRaises(HTTPException) as error:
            await self.resolve(BAIDU, self.baidu_handler)
        self.assertEqual(error.exception.status_code, 503)
        with patch.dict(os.environ, {"BAIDU_NETDISK_COOKIE": "BDUSS=test"}):
            result = await self.resolve(BAIDU, self.baidu_handler)
        self.assertNotIn("Cookie", result.headers_for(result.url))

    def quark_handler(self, request):
        path = request.url.path
        if path.endswith("/token"):
            return httpx.Response(200, json={"code": 0, "data": {"stoken": "token"}})
        if path.endswith("/detail"):
            return httpx.Response(200, json={"code": 0, "metadata": {"_total": 1}, "data": {"list": [
                {"fid": "vid", "file_name": "lesson.mp4", "dir": False, "size": 100, "share_fid_token": "filetoken"}]}})
        self.assertEqual(request.headers.get("cookie"), "__uid=test")
        if path.endswith("/save"):
            form = json.loads(request.content)
            self.assertEqual(form["fid_list"], ["vid"])
            self.assertEqual(form["to_pdir_fid"], "dedicated")
            return httpx.Response(200, json={"code": 0, "data": {"task_id": "job"}})
        if path.endswith("/task"):
            return httpx.Response(200, json={"code": 0, "data": {"status": 2, "save_as": {"save_as_top_fids": ["saved"]}}})
        if path.endswith("/download"):
            self.assertEqual(json.loads(request.content)["fids"], ["saved"])
            return httpx.Response(200, json={"code": 0, "data": [{"download_url": "https://cdn.example/a"}]})
        self.fail("unexpected endpoint")

    async def test_quark_transfer_requires_config_and_is_scoped(self):
        with self.assertRaises(HTTPException) as error:
            await self.resolve(QUARK, self.quark_handler)
        self.assertEqual(error.exception.status_code, 503)
        with patch.dict(os.environ, {"QUARK_NETDISK_COOKIE": "__uid=test", "QUARK_IMPORT_FOLDER_ID": "dedicated"}):
            result = await self.resolve(QUARK, self.quark_handler)
        self.assertNotIn("Cookie", result.headers_for(result.url))

    async def test_cancellation_prevents_quark_transfer(self):
        requests = []
        calls = 0
        async def activity():
            nonlocal calls
            calls += 1
            if calls == 3:
                raise HTTPException(409, "导入已取消")
        def handler(request):
            requests.append(request.url.path)
            return self.quark_handler(request)
        with patch.dict(os.environ, {"QUARK_NETDISK_COOKIE": "__uid=test", "QUARK_IMPORT_FOLDER_ID": "dedicated"}):
            async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
                adapter = adapter_for(parse_source(QUARK), client, on_activity=activity)
                selected = await adapter.select([], "")
                with self.assertRaises(HTTPException) as error:
                    await adapter.download(selected)
        self.assertEqual(error.exception.status_code, 409)
        self.assertFalse(any(path.endswith("/save") for path in requests))

    async def test_quark_cookie_refresh_is_used_only_for_provider(self):
        from backend.app.core.cloud_drives import Quark
        with patch.dict(os.environ, {"QUARK_NETDISK_COOKIE": "__uid=test; __puus=old"}):
            async with httpx.AsyncClient() as client:
                client.cookies.set("__puus", "refreshed", domain="drive-pc.quark.cn")
                client.cookies.set("__uid", "foreign", domain="evil.example")
                adapter = Quark(parse_source(QUARK), client)
                self.assertEqual(adapter.account_cookie(), "__uid=test; __puus=refreshed")

    async def test_wrong_codes_and_malformed_responses(self):
        for url, payload in [(BAIDU, {"errno": -9}), (QUARK, {"code": 41004}), (PKU, {"wrong": "shape"}), (BAIDU, [])]:
            with self.assertRaises(HTTPException):
                await inspect_share(url, transport=httpx.MockTransport(lambda r: httpx.Response(200, json=payload)))

    async def test_google_confirmation_and_resource_key(self):
        def handler(request):
            self.assertEqual(request.url.params.get("resourcekey"), "rk")
            if request.url.params.get("confirm") == "t":
                return httpx.Response(200, headers={"content-type": "video/mp4"})
            return httpx.Response(200, headers={"content-type": "text/html"}, text='''<form id="download-form" action="https://drive.usercontent.google.com/download">
                <input type="hidden" name="id" value="abc"><input type="hidden" name="confirm" value="t">
                <input type="hidden" name="resourcekey" value="rk"></form>''')
        result = await self.resolve(GOOGLE + "?resourcekey=rk", handler)
        self.assertIn("confirm=t", result.url)

    async def test_google_rejects_foreign_confirmation(self):
        seen = []
        def handler(request):
            seen.append(request.url.host)
            return httpx.Response(200, headers={"content-type": "text/html"}, text='<form id="download-form" action="https://evil.example/steal"></form>')
        with self.assertRaises(HTTPException):
            await self.resolve(GOOGLE, handler)
        self.assertEqual(seen, ["drive.usercontent.google.com"])

    async def test_google_inspection_reads_real_filename_and_size(self):
        def handler(request):
            return httpx.Response(200, headers={"content-type": "application/octet-stream",
                "content-disposition": 'attachment; filename="lecture.webm"', "content-length": "1000"})
        result = await inspect_share(GOOGLE, transport=httpx.MockTransport(handler))
        self.assertEqual(result["files"][0]["name"], "lecture.webm")
        self.assertEqual(result["files"][0]["size"], 1000)
        self.assertNotIn("resolved", json.dumps(result))

    async def test_google_inaccessible_file_is_not_invented_as_video(self):
        for headers, content in [({"content-type": "text/html"}, b"permission required"),
                                 ({"content-type": "application/pdf", "content-disposition": 'attachment; filename="a.pdf"'}, b"pdf")]:
            with self.assertRaises(HTTPException):
                await inspect_share(GOOGLE, transport=httpx.MockTransport(lambda r: httpx.Response(200, headers=headers, content=content)))

    async def test_google_legacy_confirmation_formats_are_supported(self):
        pages = ['<a href="/uc?export=download&amp;id=abc&amp;confirm=t">Download</a>',
                 '{"downloadUrl":"https://drive.usercontent.google.com/download?id=abc\\u0026confirm=t"}']
        for page in pages:
            def handler(request):
                if request.url.params.get("confirm") == "t":
                    return httpx.Response(200, headers={"content-type": "video/mp4"})
                return httpx.Response(200, headers={"content-type": "text/html"}, text=page)
            result = await self.resolve(GOOGLE, handler)
            self.assertIn("confirm=t", result.url)

    async def test_google_folder_membership(self):
        def handler(request):
            self.assertEqual(request.url.params.get("id"), "folder")
            return httpx.Response(200, text='<title>Folder</title><a href="https://drive.google.com/file/d/video/view">课.mp4</a><a href="https://evil.example/file/d/evil/view">evil.mp4</a>')
        result = await inspect_share("https://drive.google.com/drive/folders/folder", transport=httpx.MockTransport(handler))
        self.assertEqual([f["id"] for f in result["files"]], ["video"])

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
