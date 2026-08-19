from __future__ import annotations

import asyncio
import shutil
import time
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ai_engine.config import settings
from ai_engine.evaluation import evaluate_transcript
from ai_engine.evaluation.materials import COURSEWARE_EXT, SYLLABUS_EXT

from ..core import db
from ..schemas import TranscriptForm
from ..workers.tasks import STEP_LABELS, run_evaluation

router = APIRouter(prefix="/api/evaluation", tags=["教学视频质量评估"])

ALLOWED_EXT = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"}
SYLLABUS_MAX_BYTES = 30 * 1024 * 1024
COURSEWARE_MAX_BYTES = 80 * 1024 * 1024


def _save_upload(
    upload: UploadFile,
    prefix: str,
    allowed: set[str],
    max_bytes: int,
    kind_label: str,
) -> str:
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(
            400,
            f"不支持的{kind_label}格式 {suffix}，支持：{', '.join(sorted(allowed))}",
        )
    safe_name = f"{int(time.time())}_{prefix}_{Path(upload.filename).name}"
    dest = settings.upload_dir / safe_name
    size = 0
    try:
        with open(dest, "wb") as f:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    dest.unlink(missing_ok=True)
                    raise HTTPException(
                        400, f"{kind_label}超过大小限制（{max_bytes // (1024 * 1024)} MB）"
                    )
                f.write(chunk)
    finally:
        pass
    if size == 0:
        dest.unlink(missing_ok=True)
        raise HTTPException(400, f"上传的{kind_label}为空")
    return str(dest)


@router.post("/upload_video")
async def upload_video(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    reference: str | None = Form(
        None, description="课程大纲文本（选填）。上传大纲文件时以文件为准"
    ),
    syllabus: UploadFile | None = File(None, description="课程大纲文件（选填）"),
    courseware: UploadFile | None = File(None, description="课件文件（选填）"),
) -> dict:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(
            400, f"不支持的视频格式 {suffix}，支持：{', '.join(sorted(ALLOWED_EXT))}"
        )

    safe_name = f"{int(time.time())}_{Path(file.filename).name}"
    dest = settings.upload_dir / safe_name
    try:
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
    finally:
        await file.close()

    if dest.stat().st_size == 0:
        dest.unlink(missing_ok=True)
        raise HTTPException(400, "上传的文件为空")

    syllabus_path = None
    courseware_path = None
    try:
        if syllabus is not None and syllabus.filename:
            syllabus_path = _save_upload(
                syllabus, "syllabus", SYLLABUS_EXT, SYLLABUS_MAX_BYTES, "课程大纲"
            )
        if courseware is not None and courseware.filename:
            courseware_path = _save_upload(
                courseware, "courseware", COURSEWARE_EXT, COURSEWARE_MAX_BYTES, "课件"
            )
    except HTTPException:
        dest.unlink(missing_ok=True)
        if syllabus_path:
            Path(syllabus_path).unlink(missing_ok=True)
        raise
    finally:
        if syllabus is not None:
            await syllabus.close()
        if courseware is not None:
            await courseware.close()

    ref = (reference or "").strip() or None
    task_id = await db.create_task(
        file.filename,
        str(dest),
        ref,
        syllabus_path=syllabus_path,
        courseware_path=courseware_path,
    )
    background.add_task(
        run_evaluation,
        task_id,
        str(dest),
        ref,
        syllabus_path,
        courseware_path,
    )
    return {
        "task_id": task_id,
        "status": "queued",
        "filename": file.filename,
        "has_reference": bool(ref or syllabus_path),
        "has_syllabus": bool(ref or syllabus_path),
        "has_courseware": bool(courseware_path),
    }


@router.get("/tasks")
async def list_tasks() -> list[dict]:
    tasks = await db.list_tasks()
    for t in tasks:
        t["step_label"] = STEP_LABELS.get(t["current_step"], t["current_step"])
    return tasks


@router.get("/task/{task_id}")
async def get_task(task_id: str) -> dict:
    task = await db.get_task(task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    task["step_label"] = STEP_LABELS.get(task["current_step"], task["current_step"])
    return task


@router.post("/task/{task_id}/cancel")
async def cancel_task(task_id: str) -> dict:
    """请求停止排队中或进行中的评估任务（协作式取消）。"""
    result = await db.request_cancel(task_id)
    if result["reason"] == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        raise HTTPException(
            409, f"任务当前状态为 {result['reason']}，无法停止"
        )
    return {"ok": True, "status": "cancelled"}


@router.delete("/task/{task_id}")
async def delete_task(task_id: str) -> dict:
    if not await db.delete_task(task_id):
        raise HTTPException(404, "任务不存在")
    return {"ok": True}


@router.post("/transcript")
async def evaluate_text(form: TranscriptForm) -> dict:
    """纯文本快速通道：跳过 ASR 与视觉分析，用于联调五维打分链路。"""
    try:
        return await asyncio.to_thread(
            evaluate_transcript,
            form.text,
            form.duration_sec,
            reference=(form.reference or "").strip() or None,
        )
    except Exception as e:
        raise HTTPException(500, f"评估失败：{e}") from e


@router.get("/frame/{video_stem}/{filename}")
async def get_frame(video_stem: str, filename: str) -> FileResponse:
    """关键帧或课件渲染页。用 resolve 后的前缀检查防止路径穿越。"""
    frame_root = settings.frame_dir.resolve()
    path = (frame_root / video_stem / filename).resolve()
    if not str(path).startswith(str(frame_root)) or not path.is_file():
        raise HTTPException(404, "关键帧不存在")
    return FileResponse(path, media_type="image/jpeg")


@router.get("/rubric")
async def get_rubric_config() -> dict:
    """返回指标体系，前端用它渲染维度标签和雷达图坐标轴。"""
    from ai_engine.pedagogy.loader import get_rubric

    rubric = get_rubric()
    return {
        "dimensions": [
            {
                "key": d["key"],
                "label": d["label"],
                "description": d["description"],
                "indicators": [
                    {
                        "key": i["key"],
                        "label": i["label"],
                        "modalities": i["modalities"],
                    }
                    for i in d["indicators"]
                ],
            }
            for d in rubric["dimensions"]
        ]
    }
