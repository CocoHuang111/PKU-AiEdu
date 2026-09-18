import asyncio
import unittest
from contextlib import ExitStack
from unittest.mock import AsyncMock, Mock, patch

from backend.app.workers import tasks


class EvaluationProgressTests(unittest.IsolatedAsyncioTestCase):
    async def test_restore_progress_does_not_block_event_loop(self):
        complete = AsyncMock(return_value=True)
        updates = AsyncMock()
        with self.mocks(complete=complete, update=updates):
            await asyncio.wait_for(tasks._run_evaluation('test', 'video'), timeout=3)
        self.assertTrue(any(c.kwargs.get('current_step') == 'restore_materials' for c in updates.call_args_list))
        report = complete.call_args.args[1]
        self.assertIn('restore_materials', report['_stage_seconds'])

    async def test_empty_timeout_has_explicit_error(self):
        fail = AsyncMock(return_value=True)
        with self.mocks(fail=fail), patch.object(tasks, 'resolve_material', side_effect=TimeoutError()):
            await asyncio.wait_for(tasks._run_evaluation('test', 'video'), timeout=3)
        self.assertIn('TimeoutError', fail.call_args.args[1])
        self.assertIn('restore_materials', fail.call_args.args[1])

    def mocks(self, complete=None, update=None, fail=None):
        stack = ExitStack()
        values = {
            'is_task_cancelled': Mock(return_value=False),
            'update_task': update or AsyncMock(),
            'get_task': AsyncMock(return_value={'user_id': 'owner'}),
            'complete_eval_task': complete or AsyncMock(return_value=True),
            'fail_eval_task': fail or AsyncMock(return_value=True),
        }
        for name, value in values.items():
            stack.enter_context(patch.object(tasks.db, name, value))
        stack.enter_context(patch.object(tasks, 'resolve_material', side_effect=lambda ref, **kw: ref))
        stack.enter_context(patch.object(tasks, 'evaluate_session', return_value={}))
        stack.enter_context(patch.object(tasks, 'index_report'))
        stack.enter_context(patch.object(tasks, 'clear_eval_scratch'))
        stack.enter_context(patch.object(tasks, 'clear_staged_material'))
        stack.enter_context(patch.object(tasks, 'is_oss_reference', return_value=False))
        return stack
