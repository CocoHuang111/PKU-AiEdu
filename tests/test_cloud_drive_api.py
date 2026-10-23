import unittest
from unittest.mock import AsyncMock, patch

import httpx
from fastapi import FastAPI, HTTPException

from backend.app.api import evaluation


class CloudDriveApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.app = FastAPI()
        self.app.include_router(evaluation.router)
        self.app.dependency_overrides[evaluation.current_user] = lambda: {"id": "user"}
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_inspection_passes_share_code_and_path(self):
        result = {"provider": "pku", "files": [{"id": "file", "name": "lesson.mp4"}]}
        with patch.object(evaluation, "inspect_share", AsyncMock(return_value=result)) as inspect:
            response = await self.client.post("/api/evaluation/remote-source", json={"url": "https://disk.pku.edu.cn/link/ABC123", "password": "1234", "path": ["folder"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
        inspect.assert_awaited_once_with("https://disk.pku.edu.cn/link/ABC123", "1234", ["folder"])

    async def test_inspection_requires_authentication(self):
        def unauthenticated():
            raise HTTPException(401, "需要登录")
        self.app.dependency_overrides[evaluation.current_user] = unauthenticated
        with patch.object(evaluation, "inspect_share", AsyncMock()) as inspect:
            response = await self.client.post("/api/evaluation/remote-source", json={"url": "https://disk.pku.edu.cn/link/ABC123"})
        self.assertEqual(response.status_code, 401)
        inspect.assert_not_awaited()

    async def test_oversized_path_rejected_before_network(self):
        with patch.object(evaluation, "inspect_share", AsyncMock()) as inspect:
            response = await self.client.post("/api/evaluation/remote-source", json={"url": "https://disk.pku.edu.cn/link/ABC123", "path": ["folder"] * 13})
        self.assertEqual(response.status_code, 422)
        inspect.assert_not_awaited()

    async def test_materials_passes_selected_file_to_downloader_workflow(self):
        with patch.object(evaluation, "_store_task_materials", AsyncMock(return_value={"status": "uploaded"})) as store:
            response = await self.client.post("/api/evaluation/tasks/task/materials", data={
                "video_url": "https://disk.pku.edu.cn/link/ABC123", "share_password": "1234",
                "share_file_id": "video", "share_path": '["folder"]',
            })
        self.assertEqual(response.status_code, 200)
        args = store.await_args.args
        self.assertEqual(args[:2], ("task", {"id": "user"}))
        self.assertEqual(args[-4:], ("https://disk.pku.edu.cn/link/ABC123", "1234", "video", '["folder"]'))
