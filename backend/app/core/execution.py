"""Separate per-process execution pools for interactive QA and syllabus jobs."""

from __future__ import annotations

import asyncio
import contextvars
import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, ParamSpec, TypeVar

from .app_settings import get_app_settings

P = ParamSpec("P")
T = TypeVar("T")


class ExecutionPools:
    def __init__(self, qa_workers: int, syllabus_workers: int) -> None:
        self.qa = ThreadPoolExecutor(max_workers=qa_workers, thread_name_prefix="qa")
        self.syllabus = ThreadPoolExecutor(
            max_workers=syllabus_workers, thread_name_prefix="syllabus"
        )

    async def shutdown(self) -> None:
        # Keep the event loop alive for worker progress callbacks while draining.
        await asyncio.gather(
            asyncio.to_thread(self.qa.shutdown, wait=True),
            asyncio.to_thread(self.syllabus.shutdown, wait=True),
        )


_pools: ExecutionPools | None = None


def get_execution_pools() -> ExecutionPools:
    global _pools
    if _pools is None:
        settings = get_app_settings()
        _pools = ExecutionPools(settings.qa_max_concurrency, settings.syllabus_max_concurrency)
    return _pools


async def shutdown_execution_pools() -> None:
    global _pools
    if _pools is not None:
        await _pools.shutdown()
        _pools = None


async def _run(pool: ThreadPoolExecutor, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    # Match asyncio.to_thread's ContextVar propagation and cancellation semantics.
    context = contextvars.copy_context()
    call = functools.partial(context.run, func, *args, **kwargs)
    return await asyncio.get_running_loop().run_in_executor(pool, call)


async def run_qa(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return await _run(get_execution_pools().qa, func, *args, **kwargs)


async def run_syllabus(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    return await _run(get_execution_pools().syllabus, func, *args, **kwargs)
