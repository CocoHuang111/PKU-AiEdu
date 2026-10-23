import uuid
import unittest
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
from sqlalchemy.dialects import postgresql
from backend.app.core import material_storage as storage


class ArchiveQueueTests(unittest.IsolatedAsyncioTestCase):
    async def test_terminal_filter_and_failed_retry_backoff(self):
        task = SimpleNamespace(id=uuid.uuid4(), user_id=uuid.uuid4())
        result = Mock()
        result.all.return_value = [task]
        session = SimpleNamespace(scalars=AsyncMock(return_value=result))

        @asynccontextmanager
        async def scope():
            yield session

        retry = {}
        with patch.object(storage, 'upload_backend', return_value='oss'), patch.object(storage, 'session_scope', scope), patch.object(storage, 'archive_eval_task_materials', new_callable=AsyncMock, side_effect=OSError('offline')):
            await storage.archive_pending_eval_materials(limit=1, retry_after=retry)
            self.assertIn(str(task.id), retry)
            await storage.archive_pending_eval_materials(limit=1, retry_after=retry)
        query = str(session.scalars.call_args.args[0].compile(dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True}))
        self.assertIn("'completed', 'failed', 'cancelled'", query)
        self.assertIn(str(task.id), query)
        self.assertIn('NOT IN', query)
        self.assertIn('syllabus_path', query)

    async def test_success_clears_retry_entry(self):
        task = SimpleNamespace(id=uuid.uuid4(), user_id=uuid.uuid4())
        result = Mock()
        result.all.return_value = [task]
        session = SimpleNamespace(scalars=AsyncMock(return_value=result))

        @asynccontextmanager
        async def scope():
            yield session

        retry = {str(task.id): 0}
        with patch.object(storage, 'upload_backend', return_value='oss'), patch.object(storage, 'session_scope', scope), patch.object(storage, 'archive_eval_task_materials', new_callable=AsyncMock):
            await storage.archive_pending_eval_materials(limit=1, retry_after=retry)
        self.assertEqual(retry, {})
