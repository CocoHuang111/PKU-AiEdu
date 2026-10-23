import unittest
from unittest.mock import AsyncMock, patch

import httpx
from fastapi import HTTPException

from backend.app.core.remote_video import PublicNetworkTransport, _resolve_public_addresses


class PublicNetworkTests(unittest.IsolatedAsyncioTestCase):
    async def test_connects_to_validated_ip_preserving_host_and_sni(self):
        seen = []
        def handler(request):
            seen.append(request)
            return httpx.Response(200, content=b"ok")
        with patch("backend.app.core.remote_video._resolve_public_addresses", AsyncMock(return_value=["2606:4700:4700::1111", "1.1.1.1"])) as resolve, \
             patch("backend.app.core.remote_video.httpx.AsyncHTTPTransport", return_value=httpx.MockTransport(handler)):
            async with httpx.AsyncClient(transport=PublicNetworkTransport()) as client:
                response = await client.post("https://disk.pku.edu.cn:10002/api", json={"test": True})
        resolve.assert_awaited_once_with("disk.pku.edu.cn", 10002)
        self.assertEqual(seen[0].url.host, "1.1.1.1")
        self.assertEqual(seen[0].url.port, 10002)
        self.assertEqual(seen[0].headers["host"], "disk.pku.edu.cn:10002")
        self.assertEqual(seen[0].extensions["sni_hostname"], "disk.pku.edu.cn")
        self.assertEqual(response.request.url.host, "disk.pku.edu.cn")
        self.assertIn(b"true", seen[0].content)

    async def test_cdns_with_same_ip_do_not_share_tls_pool(self):
        with patch("backend.app.core.remote_video._resolve_public_addresses", AsyncMock(return_value=["1.1.1.1"])), \
             patch("backend.app.core.remote_video.httpx.AsyncHTTPTransport", side_effect=lambda **kw: httpx.MockTransport(lambda r: httpx.Response(200))) as pool:
            transport = PublicNetworkTransport()
            async with httpx.AsyncClient(transport=transport) as client:
                await client.get("https://one.example/a")
                await client.get("https://two.example/b")
                await client.get("https://one.example/c")
                self.assertEqual(len(transport.pools), 2)
            self.assertEqual(pool.call_count, 2)
            self.assertEqual(transport.pools, {})

    async def test_rebinding_is_checked_at_connection_time(self):
        with patch("backend.app.core.remote_video.socket.getaddrinfo", return_value=[(2, 1, 6, "", ("127.0.0.1", 443))]), \
             patch("backend.app.core.remote_video.httpx.AsyncHTTPTransport") as pool:
            async with httpx.AsyncClient(transport=PublicNetworkTransport()) as client:
                with self.assertRaises(HTTPException):
                    await client.get("https://looks-public.example/video.mp4")
            pool.assert_not_called()

    async def test_mixed_public_private_dns_answer_is_rejected(self):
        values = [(2, 1, 6, "", (address, 443)) for address in ["1.1.1.1", "10.0.0.1"]]
        with patch("backend.app.core.remote_video.socket.getaddrinfo", return_value=values), self.assertRaises(HTTPException):
            await _resolve_public_addresses("example.com", 443)
