"""大纲优化的异步任务。"""

from __future__ import annotations

import asyncio
import traceback

from ai_engine.rag import UnsupportedDocument
from ai_engine.syllabus.exceptions import SyllabusCancelled
from ai_engine.syllabus.optimizer import optimize_file, optimize_text

from ..core import db

STEP_LABELS = {
    "queued": "排队中",
    "starting": "准备中",
    "parsing": "解析文档",
    "generating": "模型生成",
    "validating": "校验结构",
    "repairing": "自动修复",
    "done": "完成",
    "failed": "失败",
    "cancelled": "已停止",
}


async def _heartbeat(task_id: str, stop: asyncio.Event) -> None:
    """LLM 单轮生成期间平滑推进进度条（协作式，可被 stop 终止）。"""
    while not stop.is_set():
        await asyncio.sleep(30)
        if stop.is_set() or db.is_syllabus_task_cancelled(task_id):
            return
        task = await db.get_syllabus_task(task_id)
        if not task or task["status"] != "processing":
            return
        if task["current_step"] != "generating" or task["progress"] >= 75:
            continue
        await db.update_syllabus_task(
            task_id, progress=min(task["progress"] + 4, 75)
        )


async def run_syllabus_optimization(task_id: str) -> None:
    if db.is_syllabus_task_cancelled(task_id):
        return

    task = await db.get_syllabus_task(task_id, include_source=True)
    if not task:
        return

    await db.update_syllabus_task(
        task_id, status="processing", progress=2, current_step="starting"
    )

    loop = asyncio.get_running_loop()
    prompt_mode = task.get("prompt_mode")
    source_path = task.get("source_path")
    source_text = task.get("source_text") or ""

    def progress(pct: int, step: str, detail: dict | None = None) -> None:
        if db.is_syllabus_task_cancelled(task_id):
            raise SyllabusCancelled()
        asyncio.run_coroutine_threadsafe(
            db.update_syllabus_task(
                task_id, progress=pct, current_step=step, step_detail=detail or {}
            ),
            loop,
        )

    def is_cancelled() -> bool:
        return db.is_syllabus_task_cancelled(task_id)

    stop = asyncio.Event()
    heartbeat = asyncio.create_task(_heartbeat(task_id, stop))

    try:
        if source_path:
            result = await asyncio.to_thread(
                optimize_file,
                source_path,
                prompt_mode=prompt_mode,
                progress=progress,
                is_cancelled=is_cancelled,
            )
        elif source_text.strip():
            progress(5, "parsing", {"chars": len(source_text)})
            result = await asyncio.to_thread(
                optimize_text,
                source_text,
                prompt_mode=prompt_mode,
                progress=progress,
                is_cancelled=is_cancelled,
            )
        else:
            raise ValueError("任务缺少 source_path 或 source_text，无法解析大纲")

        if db.is_syllabus_task_cancelled(task_id):
            return

        await db.update_syllabus_task(task_id, progress=97, current_step="saving")
        record_id = await db.save_syllabus(
            filename=task.get("filename") or "粘贴文本",
            course_name=result["course_name"],
            original_text=result["original_text"],
            xml=result["xml"],
            valid=result["valid"],
            user_id=task.get("user_id"),
        )
        payload = {**result, "id": record_id}
        await db.update_syllabus_task(
            task_id,
            status="completed",
            progress=100,
            current_step="done",
            result=payload,
            record_id=record_id,
            error=None,
        )
    except SyllabusCancelled:
        await db.update_syllabus_task(
            task_id,
            status="cancelled",
            current_step="cancelled",
            step_detail={},
            error=None,
        )
    except UnsupportedDocument as e:
        await db.update_syllabus_task(
            task_id, status="failed", current_step="failed", error=str(e)
        )
    except Exception as e:
        if db.is_syllabus_task_cancelled(task_id):
            return
        traceback.print_exc()
        await db.update_syllabus_task(
            task_id, status="failed", current_step="failed", error=str(e)
        )
    finally:
        stop.set()
        heartbeat.cancel()
        try:
            await heartbeat
        except asyncio.CancelledError:
            pass
