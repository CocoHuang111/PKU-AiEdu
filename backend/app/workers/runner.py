"""PostgreSQL-backed single-concurrency evaluation worker."""

from __future__ import annotations

import asyncio
import os
import socket
import uuid

from ..core import db
from ..core.material_storage import purge_deleted_oss_files
from .tasks import run_evaluation

POLL_SECONDS = max(0.5, float(os.getenv("EVALUATION_WORKER_POLL_SECONDS") or "2"))
HEARTBEAT_SECONDS = max(5, int(os.getenv("EVALUATION_HEARTBEAT_SECONDS") or "15"))
LEASE_SECONDS = max(30, int(os.getenv("EVALUATION_LEASE_SECONDS") or "120"))
UPLOAD_MAX_AGE_SECONDS = max(300, int(os.getenv("EVALUATION_UPLOAD_MAX_AGE_SECONDS") or "7200"))


async def _heartbeat(task_id: str, worker_id: str) -> None:
    while True:
        await asyncio.sleep(HEARTBEAT_SECONDS)
        if not await db.heartbeat_eval_task(task_id, worker_id):
            return


async def main() -> None:
    worker_id = f"{socket.gethostname()}-{uuid.uuid4().hex[:10]}"
    recovered = await db.recover_stale_eval_tasks(LEASE_SECONDS)
    await db.expire_stale_uploads(UPLOAD_MAX_AGE_SECONDS)
    if recovered:
        print(f"[worker] recovered {recovered} stale evaluation task(s)", flush=True)

    idle_cycles = 0
    while True:
        task = await db.claim_next_eval_task(worker_id)
        if not task:
            idle_cycles += 1
            if idle_cycles * POLL_SECONDS >= LEASE_SECONDS:
                await db.recover_stale_eval_tasks(LEASE_SECONDS)
                await db.expire_stale_uploads(UPLOAD_MAX_AGE_SECONDS)
                await purge_deleted_oss_files()
                idle_cycles = 0
            await asyncio.sleep(POLL_SECONDS)
            continue

        idle_cycles = 0
        task_id = task["id"]
        beat = asyncio.create_task(_heartbeat(task_id, worker_id))
        try:
            await run_evaluation(
                task_id,
                task["video_path"],
                task["reference"],
                task["syllabus_path"],
                task["courseware_path"],
                task["transcript"],
                task["transcript_path"],
            )
        finally:
            beat.cancel()
            try:
                await beat
            except asyncio.CancelledError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
