from __future__ import annotations

import asyncio
import contextvars
import os
import threading
import unittest
from contextlib import ExitStack
from unittest.mock import AsyncMock, patch

from backend.app.api import qa
from backend.app.core import execution
from backend.app.core.app_settings import AppSettings
from backend.app.schemas import QAForm
from backend.app.workers import syllabus_tasks


class ExecutionIsolationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.pools = execution.ExecutionPools(qa_workers=1, syllabus_workers=1)
        self.pool_patch = patch.object(execution, "_pools", self.pools)
        self.pool_patch.start()
        self.release = threading.Event()
        self.jobs = []

    async def asyncTearDown(self):
        self.release.set()
        await asyncio.gather(*self.jobs, return_exceptions=True)
        if qa._background_jobs:
            await asyncio.gather(*tuple(qa._background_jobs), return_exceptions=True)
        await self.pools.shutdown()
        self.pool_patch.stop()

    async def occupy(self, runner):
        started = asyncio.Event()
        loop = asyncio.get_running_loop()

        def block():
            loop.call_soon_threadsafe(started.set)
            if not self.release.wait(5):
                raise TimeoutError("test worker was not released")

        job = asyncio.create_task(runner(block))
        self.jobs.append(job)
        await asyncio.wait_for(started.wait(), 2)
        return job

    async def test_saturated_syllabus_pool_does_not_block_qa_or_default_pool(self):
        await self.occupy(execution.run_syllabus)
        queued = asyncio.create_task(execution.run_syllabus(lambda: "second"))
        self.jobs.append(queued)
        self.assertEqual(await asyncio.wait_for(execution.run_qa(lambda: "qa"), 2), "qa")
        self.assertEqual(await asyncio.wait_for(asyncio.to_thread(lambda: "default"), 2), "default")
        self.assertFalse(queued.done())
        self.release.set()
        self.assertEqual(await asyncio.wait_for(queued, 2), "second")

    async def test_saturated_qa_pool_does_not_block_syllabus(self):
        await self.occupy(execution.run_qa)
        self.assertEqual(await asyncio.wait_for(execution.run_syllabus(lambda: "ok"), 2), "ok")

    async def test_context_kwargs_and_failure_do_not_lose_worker(self):
        marker = contextvars.ContextVar("request_marker")
        marker.set("user-a")
        self.assertEqual(await execution.run_qa(lambda *, suffix: marker.get() + suffix, suffix="!"), "user-a!")

        def fail():
            raise ValueError("model failed")

        with self.assertRaisesRegex(ValueError, "model failed"):
            await execution.run_syllabus(fail)
        self.assertEqual(await execution.run_syllabus(lambda: 42), 42)

    async def test_syllabus_queue_status_and_cancellation_before_model_call(self):
        await self.occupy(execution.run_syllabus)
        fetched = asyncio.Event()
        state = {"status": "queued", "source_text": "test syllabus"}

        async def get_task(*args, **kwargs):
            fetched.set()
            return dict(state)

        async def claim(*args):
            if state["status"] != "queued":
                return False
            state["status"] = "processing"
            return True

        with patch.object(syllabus_tasks.db, "get_syllabus_task", side_effect=get_task), \
             patch.object(syllabus_tasks.db, "start_syllabus_task", side_effect=claim) as start, \
             patch.object(syllabus_tasks.db, "update_syllabus_task", new_callable=AsyncMock) as update, \
             patch.object(syllabus_tasks, "optimize_text") as optimize:
            job = asyncio.create_task(syllabus_tasks.run_syllabus_optimization("task"))
            self.jobs.append(job)
            await asyncio.wait_for(fetched.wait(), 2)
            self.assertEqual(state["status"], "queued")
            start.assert_not_called()
            update.assert_not_called()
            state["status"] = "cancelled"
            self.release.set()
            await asyncio.wait_for(job, 2)
            optimize.assert_not_called()
            update.assert_not_called()
            self.assertEqual(state["status"], "cancelled")

    async def test_syllabus_completion_runs_in_dedicated_pool(self):
        result = {"course_name": "course", "original_text": "source", "xml": "output", "valid": True}

        def optimize(*args, **kwargs):
            self.assertTrue(threading.current_thread().name.startswith("syllabus"))
            return result

        with patch.object(syllabus_tasks.db, "get_syllabus_task", new_callable=AsyncMock,
                          return_value={"status": "queued", "source_text": "source"}), \
             patch.object(syllabus_tasks.db, "start_syllabus_task", new_callable=AsyncMock, return_value=True), \
             patch.object(syllabus_tasks.db, "is_syllabus_task_cancelled", return_value=False), \
             patch.object(syllabus_tasks.db, "update_syllabus_task", new_callable=AsyncMock) as update, \
             patch.object(syllabus_tasks.db, "save_syllabus", new_callable=AsyncMock, return_value="record"), \
             patch.object(syllabus_tasks, "optimize_text", side_effect=optimize):
            await asyncio.wait_for(syllabus_tasks.run_syllabus_optimization("task"), 2)
            self.assertEqual(update.call_args.kwargs["status"], "completed")

    async def test_heartbeat_survives_waiting_in_queue(self):
        stop = asyncio.Event()

        async def update(*args, **kwargs):
            stop.set()

        with patch.object(syllabus_tasks.asyncio, "sleep", new_callable=AsyncMock), \
             patch.object(syllabus_tasks.db, "get_syllabus_task", new_callable=AsyncMock,
                          side_effect=[{"status": "queued"},
                                       {"status": "processing", "current_step": "generating", "progress": 10}]), \
             patch.object(syllabus_tasks.db, "update_syllabus_task", side_effect=update) as updated:
            await syllabus_tasks._heartbeat("task", stop)
            updated.assert_awaited_once_with("task", progress=14)

    async def test_both_qa_endpoints_work_while_syllabus_full_and_stream_persists_after_disconnect(self):
        await self.occupy(execution.run_syllabus)
        answer = {"answer": "answer", "citations": []}

        def ask(*args):
            self.assertTrue(threading.current_thread().name.startswith("qa"))
            return answer

        def stream(*args):
            self.assertTrue(threading.current_thread().name.startswith("qa"))
            yield {"type": "done", **answer}

        with ExitStack() as stack:
            for name in ("_load_history", "_owned_eval_task_ids", "_pinned_eval_contexts"):
                stack.enter_context(patch.object(qa, name, new_callable=AsyncMock, return_value=[]))
            save = stack.enter_context(patch.object(qa.db, "save_session", new_callable=AsyncMock, return_value="session"))
            stack.enter_context(patch.object(qa, "ask", side_effect=ask))
            stack.enter_context(patch.object(qa, "ask_stream", side_effect=stream))
            form = QAForm(question="how to teach?")
            result = await asyncio.wait_for(qa.ask_once(form, {"id": "user"}), 2)
            self.assertEqual(result["answer"], "answer")
            response = await qa.ask_streaming(form, {"id": "user"})
            await anext(response.body_iterator)
            await response.body_iterator.aclose()
            await asyncio.wait_for(asyncio.gather(*tuple(qa._background_jobs)), 2)
            history = save.call_args.args[1]
            self.assertEqual(history[-1]["content"], "answer")
            self.assertNotIn("pending", history[-1])

    async def test_shutdown_drains_worker_without_blocking_event_loop(self):
        await self.occupy(execution.run_syllabus)
        closing = asyncio.create_task(execution.shutdown_execution_pools())
        self.jobs.append(closing)
        asyncio.get_running_loop().call_later(0.02, self.release.set)
        await asyncio.wait_for(closing, 2)
        self.assertIsNone(execution._pools)


class ConcurrencySettingsTests(unittest.TestCase):
    def test_configuration_and_invalid_limits(self):
        with patch.dict(os.environ, {"QA_MAX_CONCURRENCY": "7", "SYLLABUS_MAX_CONCURRENCY": "3"}):
            settings = AppSettings()
            self.assertEqual((settings.qa_max_concurrency, settings.syllabus_max_concurrency), (7, 3))
        for name in ("QA_MAX_CONCURRENCY", "SYLLABUS_MAX_CONCURRENCY"):
            for value in ("0", "-1", "abc"):
                with self.subTest(name=name, value=value), patch.dict(os.environ, {name: value}):
                    with self.assertRaisesRegex(ValueError, name):
                        AppSettings()
