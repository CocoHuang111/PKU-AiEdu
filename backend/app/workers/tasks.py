"""视频评估的异步任务。

用 FastAPI BackgroundTasks + asyncio.to_thread 起步。评估是 CPU/IO 混合的长任务，
放线程里跑，事件循环仍能响应轮询请求。以后要换 Celery，只需替换 run_evaluation 的调度方式。
"""

from __future__ import annotations

import asyncio
import os
import traceback

from ai_engine.evaluation import evaluate_session, index_report
from ai_engine.evaluation.exceptions import EvaluationCancelled

from ..core import db


def _evaluation_concurrency() -> int:
    try:
        return max(1, int(os.getenv("EVALUATION_MAX_CONCURRENCY") or "1"))
    except ValueError:
        return 1


# 2 核内测服务器只允许一个视频流水线占用 CPU。等待信号量期间任务保持 queued，
# 避免多个 faster-whisper / ffmpeg 同时运行导致整台服务器失去响应。
_EVALUATION_SEMAPHORE = asyncio.Semaphore(_evaluation_concurrency())

STEP_LABELS = {
    "queued": "排队中",
    "starting": "准备中",
    "extracting_audio": "抽取音频",
    "parse_materials": "解析大纲与课件",
    "keyframe_sampling": "抽取关键帧",
    "asr": "语音识别",
    "objective_features": "客观特征提取",
    "slide_detection": "课件切换检测",
    "diarization": "说话人分离",
    "vlm_describe": "视觉分析",
    "llm_judge": "五维评分",
    "report": "生成报告",
    "done": "完成",
    "failed": "失败",
    "cancelled": "已停止",
}


async def run_evaluation(
    task_id: str,
    video_path: str | None = None,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript_text: str | None = None,
    transcript_path: str | None = None,
) -> None:
    async with _EVALUATION_SEMAPHORE:
        await _run_evaluation(
            task_id,
            video_path,
            reference,
            syllabus_path,
            courseware_path,
            transcript_text,
            transcript_path,
        )


async def _run_evaluation(
    task_id: str,
    video_path: str | None = None,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript_text: str | None = None,
    transcript_path: str | None = None,
) -> None:
    if db.is_task_cancelled(task_id):
        return

    await db.update_task(task_id, status="processing", progress=2, current_step="starting")

    loop = asyncio.get_running_loop()

    def progress(pct: int, step: str, detail: dict | None = None) -> None:
        if db.is_task_cancelled(task_id):
            raise EvaluationCancelled()
        # 在工作线程里被调用，用 run_coroutine_threadsafe 把写库调度回事件循环
        asyncio.run_coroutine_threadsafe(
            db.update_task(
                task_id, progress=pct, current_step=step, step_detail=detail or {}
            ),
            loop,
        )

    try:
        result = await asyncio.to_thread(
            evaluate_session,
            video_path,
            progress,
            reference,
            syllabus_path,
            courseware_path,
            transcript_text,
            transcript_path,
        )
        if db.is_task_cancelled(task_id):
            return
        await db.update_task(
            task_id,
            status="completed",
            progress=100,
            current_step="done",
            result=result,
            error=None,
        )
        # 报告回流到向量库，供问答引用；失败不影响任务状态
        task = await db.get_task(task_id)
        await asyncio.to_thread(
            index_report, task_id, result, (task or {}).get("user_id")
        )
    except EvaluationCancelled:
        await db.update_task(
            task_id,
            status="cancelled",
            current_step="cancelled",
            step_detail={},
            error=None,
        )
    except Exception as e:
        if db.is_task_cancelled(task_id):
            return
        traceback.print_exc()
        await db.update_task(
            task_id, status="failed", current_step="failed", error=str(e)
        )
