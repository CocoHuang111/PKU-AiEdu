from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from fastapi import HTTPException

from backend.app.core.remote_video import (
    _safe_filename,
    download_remote_video,
    validate_remote_url,
)
from backend.app.core.storage import LocalStorageBackend


class RemoteUrlValidationTests(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_local_and_private_addresses(self) -> None:
        for url in (
            "http://127.0.0.1/video.mp4",
            "http://localhost/video.mp4",
            "http://10.0.0.8/video.mp4",
            "file:///tmp/video.mp4",
        ):
            with self.subTest(url=url), self.assertRaises(HTTPException):
                await validate_remote_url(url)

    async def test_accepts_public_https_and_drops_fragment(self) -> None:
        with patch(
            "backend.app.core.remote_video._resolve_public_addresses",
            AsyncMock(return_value=["203.0.113.10"]),
        ):
            value = await validate_remote_url("HTTPS://video.example/lesson.mp4?token=abc#preview")
        self.assertEqual(value, "https://video.example/lesson.mp4?token=abc")

    def test_rejects_share_page_response(self) -> None:
        response = httpx.Response(
            200,
            headers={"content-type": "text/html"},
        )
        with self.assertRaises(HTTPException):
            _safe_filename(response, "https://example.com/share/lesson.mp4")


class RemoteVideoDownloadTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.sample = self.root / "sample.mp4"
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                "color=c=black:s=160x90:d=1",
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(self.sample),
            ],
            capture_output=True,
            timeout=30,
        )
        if result.returncode != 0:
            self.fail(result.stderr.decode("utf-8", errors="replace")[-1000:])

    async def asyncTearDown(self) -> None:
        self.tmp.cleanup()

    async def test_streams_video_to_task_storage_and_reports_progress(self) -> None:
        payload = self.sample.read_bytes()

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                headers={
                    "content-type": "video/mp4",
                    "content-disposition": 'attachment; filename="lesson.mp4"',
                    "content-length": str(len(payload)),
                },
                content=payload,
            )

        progress: list[tuple[int, int | None]] = []

        async def on_progress(done: int, total: int | None) -> None:
            progress.append((done, total))

        with (
            patch(
                "backend.app.core.remote_video._resolve_public_addresses",
                AsyncMock(return_value=["203.0.113.10"]),
            ),
            patch(
                "backend.app.core.remote_video.get_storage",
                return_value=LocalStorageBackend(self.root / "uploads"),
            ),
            patch.dict(os.environ, {"REMOTE_VIDEO_MIN_FREE_BYTES": "1"}),
        ):
            saved = await download_remote_video(
                "https://video.example/download?id=1",
                user_id="user-1",
                task_id="task-1",
                on_progress=on_progress,
                transport=httpx.MockTransport(handler),
            )

        self.assertEqual(saved.filename, "lesson.mp4")
        self.assertEqual(saved.size_bytes, len(payload))
        self.assertGreater(saved.duration_sec, 0)
        self.assertEqual(Path(saved.path).read_bytes(), payload)
        self.assertEqual(progress[-1], (len(payload), len(payload)))

    async def test_revalidates_redirect_target_and_rejects_localhost(self) -> None:
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(302, headers={"location": "http://127.0.0.1/private.mp4"})

        with (
            patch(
                "backend.app.core.remote_video._resolve_public_addresses",
                AsyncMock(return_value=["203.0.113.10"]),
            ),
            self.assertRaises(HTTPException),
        ):
            await download_remote_video(
                "https://video.example/start",
                user_id="user-1",
                task_id="task-1",
                transport=httpx.MockTransport(handler),
            )

    async def test_removes_partial_file_when_progress_callback_cancels(self) -> None:
        payload = self.sample.read_bytes()

        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                headers={"content-type": "video/mp4", "content-length": str(len(payload))},
                content=payload,
            )

        async def cancelled(done: int, total: int | None) -> None:
            raise HTTPException(409, "导入已取消")

        upload_root = self.root / "cancelled-uploads"
        with (
            patch(
                "backend.app.core.remote_video._resolve_public_addresses",
                AsyncMock(return_value=["203.0.113.10"]),
            ),
            patch(
                "backend.app.core.remote_video.get_storage",
                return_value=LocalStorageBackend(upload_root),
            ),
            patch.dict(os.environ, {"REMOTE_VIDEO_MIN_FREE_BYTES": "1"}),
            self.assertRaises(HTTPException),
        ):
            await download_remote_video(
                "https://video.example/cancelled.mp4",
                user_id="user-1",
                task_id="task-1",
                on_progress=cancelled,
                transport=httpx.MockTransport(handler),
            )

        self.assertEqual(list(upload_root.rglob("*.mp4")), [])


if __name__ == "__main__":
    unittest.main()
