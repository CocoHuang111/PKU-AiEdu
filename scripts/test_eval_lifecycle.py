"""视频评估 PostgreSQL 状态机集成测试。"""

from __future__ import annotations

import os
import tempfile
import unittest
import uuid
from pathlib import Path

_uploads = tempfile.TemporaryDirectory()
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("SESSION_SECRET", "test-session-secret")
os.environ.setdefault("UPLOAD_ROOT", _uploads.name)
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://pku2:pku2@127.0.0.1:5432/pku2",
)

from sqlalchemy import create_engine, text  # noqa: E402

from backend.app.core import db  # noqa: E402
from backend.app.core.app_settings import get_app_settings  # noqa: E402
from backend.app.core.database import session_scope  # noqa: E402
from backend.app.models import User  # noqa: E402


def _postgres_ready() -> bool:
    try:
        engine = create_engine(get_app_settings().database_url_sync)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except Exception:
        return False


@unittest.skipUnless(_postgres_ready(), "PostgreSQL 未启动，跳过评估状态机测试")
class EvaluationLifecycleTest(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from alembic import command
        from alembic.config import Config

        command.upgrade(Config("alembic.ini"), "head")

    @classmethod
    def tearDownClass(cls) -> None:
        _uploads.cleanup()

    async def asyncSetUp(self) -> None:
        self.user_id = uuid.uuid4()
        async with session_scope() as session:
            session.add(
                User(
                    id=self.user_id,
                    role="user",
                    status="active",
                    display_name="评估测试",
                )
            )

    async def _create_and_submit(self) -> tuple[str, Path]:
        task_id = await db.create_task(
            "lesson.mp4", user_id=self.user_id, status="uploading"
        )
        created = await db.get_task(task_id, user_id=str(self.user_id))
        self.assertEqual(created["status"], "uploading")

        task_dir = Path(_uploads.name) / str(self.user_id) / task_id
        task_dir.mkdir(parents=True)
        video_path = task_dir / "lesson.mp4"
        video_path.write_bytes(b"fake-video")
        uploaded = await db.set_task_materials(
            task_id,
            str(self.user_id),
            video_path=str(video_path),
        )
        self.assertEqual(uploaded["status"], "uploading")

        submitted = await db.submit_task(task_id, str(self.user_id))
        self.assertTrue(submitted["ok"])
        self.assertEqual(submitted["task"]["status"], "queued")
        return task_id, task_dir

    async def test_upload_queue_cancel_and_terminal_delete(self):
        task_id, task_dir = await self._create_and_submit()
        self.assertFalse((await db.delete_task(task_id, str(self.user_id)))["ok"])

        stopped = await db.request_cancel(task_id, str(self.user_id))
        self.assertEqual(stopped, {"ok": True, "status": "cancelled"})
        self.assertTrue((await db.delete_task(task_id, str(self.user_id)))["ok"])
        self.assertFalse(task_dir.exists())

    async def test_claim_processing_requires_cooperative_stop_before_delete(self):
        task_id, _ = await self._create_and_submit()
        claimed = await db.claim_next_eval_task("test-worker")
        self.assertEqual(claimed["id"], task_id)

        stopped = await db.request_cancel(task_id, str(self.user_id))
        self.assertEqual(stopped, {"ok": True, "status": "cancel_requested"})
        self.assertFalse((await db.delete_task(task_id, str(self.user_id)))["ok"])

        self.assertFalse(await db.complete_eval_task(task_id, {"should": "not win"}))
        self.assertTrue(await db.finalize_eval_cancellation(task_id))
        self.assertTrue((await db.delete_task(task_id, str(self.user_id)))["ok"])


if __name__ == "__main__":
    unittest.main()
