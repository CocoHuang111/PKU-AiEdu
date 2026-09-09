"""视频评估执行器。任务由独立 Worker 从 PostgreSQL 领取。"""

from __future__ import annotations

import asyncio
import traceback

from ai_engine.evaluation import evaluate_session, index_report
from ai_engine.evaluation.exceptions import EvaluationCancelled

from ..core import db


STEP_LABELS = {
    "uploading": "上传中",
    "upload_failed": "上传失败",
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
    "cancel_requested": "正在停止",
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
    """兼容旧调用；新部署由 runner 领取任务后调用此函数。"""
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
        await db.finalize_eval_cancellation(task_id)
        return

    await db.update_task(task_id, progress=2, current_step="starting")

    loop = asyncio.get_running_loop()

    def progress(pct: int, step: str, detail: dict | None = None) -> None:
        if db.is_task_cancelled(task_id):
            raise EvaluationCancelled()
        # 等写库完成再继续，保证最后的 completed 不会被迟到的进度更新覆盖。
        future = asyncio.run_coroutine_threadsafe(
            db.update_task(
                task_id, progress=pct, current_step=step, step_detail=detail or {}
            ),
            loop,
        )
        future.result(timeout=30)

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
            await db.finalize_eval_cancellation(task_id)
            return
        if not await db.complete_eval_task(task_id, result):
            await db.finalize_eval_cancellation(task_id)
            return
        # 报告回流到向量库，供问答引用；失败不影响任务状态
        task = await db.get_task(task_id)
        await asyncio.to_thread(
            index_report, task_id, result, (task or {}).get("user_id")
        )
    except EvaluationCancelled:
        await db.finalize_eval_cancellation(task_id)
    except Exception as e:
        if db.is_task_cancelled(task_id):
            await db.finalize_eval_cancellation(task_id)
            return
        traceback.print_exc()
        if not await db.fail_eval_task(task_id, str(e)):
            await db.finalize_eval_cancellation(task_id)
