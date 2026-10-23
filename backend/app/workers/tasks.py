"""视频评估执行器。任务由独立 Worker 从 PostgreSQL 领取。"""

from __future__ import annotations

import asyncio
import traceback
import time
from pathlib import Path

from ai_engine.evaluation import evaluate_session, index_report
from ai_engine.evaluation.exceptions import EvaluationCancelled

from ..core import db
from ..core.material_storage import (
    clear_eval_scratch,
    clear_staged_material,
    is_oss_reference,
    resolve_material,
)


STEP_LABELS = {
    "uploading": "上传中",
    "remote_downloading": "服务器下载中",
    "upload_failed": "上传失败",
    "queued": "排队中",
    "starting": "准备中",
    "restore_materials": "读取材料",
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
    started = time.monotonic()
    last_write = 0.0
    last_log = 0.0
    last_step = None
    stage_started = started
    timed_stage = 'starting'
    stage_seconds = {}
    timing_finished = False

    def finish_stage(now):
        nonlocal stage_started
        stage_seconds[timed_stage] = stage_seconds.get(timed_stage, 0.0) + now - stage_started
        stage_started = now

    def progress(pct: int, step: str, detail: dict | None = None) -> None:
        nonlocal last_write, last_log, last_step, timed_stage
        if db.is_task_cancelled(task_id):
            raise EvaluationCancelled()
        now = time.monotonic()
        phase = (detail or {}).get('phase')
        stage = f'{step}:{phase}' if phase else step
        if stage != timed_stage:
            finish_stage(now)
            timed_stage = stage
        if step != last_step or now - last_log >= 30:
            memory = "unknown"
            try:
                memory_stat = dict(line.split() for line in Path('/sys/fs/cgroup/memory.stat').read_text().splitlines())
                memory = f"{int(memory_stat['anon']) / 1024**2:.0f}MiB-anon"
            except (OSError, ValueError):
                pass
            print(f"[evaluation] task={task_id} step={step} progress={pct} elapsed={now-started:.1f}s memory={memory} detail={detail}", flush=True)
            last_log = now
        if step == last_step and now - last_write < 1 and pct < 100:
            return
        last_step, last_write = step, now
        # 等写库完成再继续，保证最后的 completed 不会被迟到的进度更新覆盖。
        future = asyncio.run_coroutine_threadsafe(
            db.update_task(
                task_id, progress=pct, current_step=step, step_detail=detail or {}
            ),
            loop,
        )
        future.result(timeout=30)

    try:
        task = await db.get_task(task_id)
        owner = (task or {}).get("user_id")
        if not owner:
            raise ValueError("任务缺少文件所有者")
        references = (video_path, syllabus_path, courseware_path, transcript_path)
        # progress waits synchronously for the event loop: never call it on that loop.
        await asyncio.to_thread(progress, 2, 'restore_materials')
        video_path, syllabus_path, courseware_path, transcript_path = await asyncio.to_thread(
            lambda: tuple(resolve_material(ref, owner=owner, task_id=task_id) for ref in references)
        )
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
        result["_processing_seconds"] = round(time.monotonic() - started, 2)
        finish_stage(time.monotonic())
        timing_finished = True
        result['_stage_seconds'] = {k: round(v, 2) for k, v in stage_seconds.items()}
        print(f'[evaluation-timing] task={task_id} stages={result["_stage_seconds"]}', flush=True)
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
        error_message = str(e).strip() or f'{type(e).__name__}：评估阶段 {timed_stage} 执行失败'
        if not await db.fail_eval_task(task_id, error_message):
            await db.finalize_eval_cancellation(task_id)
    finally:
        if not timing_finished:
            finish_stage(time.monotonic())
        print(f'[evaluation-timing-final] task={task_id} elapsed={time.monotonic()-started:.2f}s stages={stage_seconds}', flush=True)
        if "references" in locals() and owner:
            for ref in references:
                try:
                    if ref and is_oss_reference(ref):
                        await asyncio.to_thread(
                            clear_staged_material, ref, owner=owner, task_id=task_id, processing=True
                        )
                    else:
                        await asyncio.to_thread(clear_eval_scratch, ref)
                except Exception:
                    print("[storage] 解析临时文件清理失败，源文件仍保留到 OSS 归档", flush=True)
