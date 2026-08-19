from __future__ import annotations

import asyncio
import shutil
import time
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Query, UploadFile
from fastapi.responses import Response

from ai_engine.config import settings
from ai_engine.syllabus import ExportError, detect_output_format, export_syllabus
from ai_engine.syllabus.export import content_disposition, export_filename

from ..core import db
from ..schemas import SyllabusTextForm
from ..workers.syllabus_tasks import STEP_LABELS, run_syllabus_optimization

router = APIRouter(prefix="/api/syllabus", tags=["教学大纲优化"])

ALLOWED_EXT = {".pdf", ".docx", ".doc", ".txt", ".md"}


@router.post("/optimize")
async def optimize_from_text(
    background: BackgroundTasks, form: SyllabusTextForm
) -> dict:
    if len(form.text.strip()) < 10:
        raise HTTPException(400, "大纲内容过短")
    task_id = await db.create_syllabus_task(
        filename="粘贴文本",
        prompt_mode=form.prompt_mode,
        source_text=form.text.strip(),
    )
    background.add_task(run_syllabus_optimization, task_id)
    return {"task_id": task_id, "status": "queued", "filename": "粘贴文本"}


@router.post("/optimize_file")
async def optimize_from_file(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    prompt_mode: str | None = Query(
        None,
        description="adaptive | schema | markdown | markdown_schema",
    ),
) -> dict:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(
            400, f"不支持的文档格式 {suffix}，支持：{', '.join(sorted(ALLOWED_EXT))}"
        )

    dest = settings.upload_dir / f"{int(time.time())}_{Path(file.filename).name}"
    try:
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
    finally:
        await file.close()

    task_id = await db.create_syllabus_task(
        filename=file.filename or "上传文件",
        prompt_mode=prompt_mode,
        source_path=str(dest),
    )
    background.add_task(run_syllabus_optimization, task_id)
    return {"task_id": task_id, "status": "queued", "filename": file.filename}


@router.get("/tasks")
async def list_tasks() -> list[dict]:
    tasks = await db.list_syllabus_tasks()
    for task in tasks:
        task["step_label"] = STEP_LABELS.get(task["current_step"], task["current_step"])
    return tasks


@router.get("/task/{task_id}")
async def get_task(task_id: str) -> dict:
    task = await db.get_syllabus_task(task_id)
    if not task:
        raise HTTPException(404, "任务不存在")
    task["step_label"] = STEP_LABELS.get(task["current_step"], task["current_step"])
    return task


@router.post("/task/{task_id}/cancel")
async def cancel_task(task_id: str) -> dict:
    result = await db.request_cancel_syllabus_task(task_id)
    if result["reason"] == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        raise HTTPException(
            409, f"任务当前状态为 {result['reason']}，无法停止"
        )
    return {"ok": True, "status": "cancelled"}


@router.get("/history")
async def history() -> list[dict]:
    return await db.list_syllabi()


@router.get("/record/{record_id}")
async def get_record(record_id: str) -> dict:
    record = await db.get_syllabus(record_id)
    if not record:
        raise HTTPException(404, "记录不存在")
    record["output_format"] = detect_output_format(record.get("xml") or "")
    return record


@router.get("/download/{record_id}")
async def download(record_id: str) -> Response:
    record = await db.get_syllabus(record_id)
    if not record:
        raise HTTPException(404, "记录不存在")
    name = (record["course_name"] or "syllabus").replace("/", "_")
    content = record["xml"]
    output_format = detect_output_format(content or "")
    if output_format == "markdown":
        return Response(
            content=content,
            media_type="text/markdown; charset=utf-8",
            headers={
                "Content-Disposition": f'attachment; filename="{record_id[:8]}.md"',
                "X-Course-Name": name.encode("utf-8").hex(),
            },
        )
    return Response(
        content=content,
        media_type="application/xml",
        headers={
            "Content-Disposition": f'attachment; filename="{record_id[:8]}.xml"',
            "X-Course-Name": name.encode("utf-8").hex(),
        },
    )


@router.get("/export/{record_id}")
async def export_record(
    record_id: str,
    format: str = Query(..., pattern="^(markdown|docx|pdf)$"),
) -> Response:
    record = await db.get_syllabus(record_id)
    if not record:
        raise HTTPException(404, "记录不存在")
    if not record.get("valid"):
        raise HTTPException(400, "大纲校验未通过，请先修复后再导出")

    try:
        content, media_type, suffix = await asyncio.to_thread(
            export_syllabus, record["xml"], format
        )
    except ExportError as e:
        raise HTTPException(400, str(e)) from e
    except Exception as e:
        raise HTTPException(500, f"导出失败：{e}") from e

    filename = export_filename(record.get("course_name") or "syllabus", suffix)
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": content_disposition(filename)},
    )
