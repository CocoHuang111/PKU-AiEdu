from __future__ import annotations

import asyncio
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import Response

from ai_engine.syllabus import ExportError, detect_output_format, export_syllabus
from ai_engine.syllabus.export import content_disposition, export_filename

from ..core import db
from ..core.audit import audit
from ..core.auth import current_user
from ..core.database import session_scope
from ..core.uploads import new_task_id, record_upload, save_user_upload
from ..core.material_storage import material_reference, mark_task_files_deleted, purge_deleted_oss_files, release_uploaded_paths
from ..schemas import SyllabusTextForm
from ..workers.syllabus_tasks import STEP_LABELS, run_syllabus_optimization

router = APIRouter(prefix="/api/syllabus", tags=["教学大纲优化"])

ALLOWED_EXT = {".pdf", ".docx", ".doc", ".txt", ".md"}


@router.post("/optimize")
async def optimize_from_text(
    background: BackgroundTasks,
    form: SyllabusTextForm,
    user: dict = Depends(current_user),
) -> dict:
    if len(form.text.strip()) < 10:
        raise HTTPException(400, "大纲内容过短")
    task_id = await db.create_syllabus_task(
        filename="粘贴文本",
        prompt_mode=form.prompt_mode,
        source_text=form.text.strip(),
        user_id=user["id"],
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
    user: dict = Depends(current_user),
) -> dict:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(
            400, f"不支持的文档格式 {suffix}，支持：{', '.join(sorted(ALLOWED_EXT))}"
        )

    task_id = new_task_id()
    dest, key = await asyncio.to_thread(save_user_upload,
        file,
        user_id=user["id"],
        task_id=task_id,
        purpose="syllabus",
        allowed=ALLOWED_EXT,
        max_bytes=30 * 1024 * 1024,
        kind_label="大纲",
    )
    await file.close()
    await record_upload(
        user_id=user["id"],
        purpose="syllabus",
        original_name=file.filename or "upload",
        storage_key=key,
        mime_type=file.content_type,
        path=dest,
    )
    await db.create_syllabus_task(
        filename=file.filename or "上传文件",
        prompt_mode=prompt_mode,
        source_path=material_reference(dest, key),
        user_id=user["id"],
        task_id=task_id,
    )
    await release_uploaded_paths(user["id"], task_id, dest)
    background.add_task(run_syllabus_optimization, task_id)
    return {"task_id": task_id, "status": "queued", "filename": file.filename}


@router.get("/tasks")
async def list_tasks(user: dict = Depends(current_user)) -> list[dict]:
    tasks = await db.list_syllabus_tasks(user_id=user["id"])
    for task in tasks:
        task["step_label"] = STEP_LABELS.get(task["current_step"], task["current_step"])
    return tasks


@router.get("/task/{task_id}")
async def get_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    task = await db.get_syllabus_task(task_id, user_id=user["id"])
    if not task:
        raise HTTPException(404, "任务不存在")
    task["step_label"] = STEP_LABELS.get(task["current_step"], task["current_step"])
    return task


@router.post("/task/{task_id}/cancel")
async def cancel_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    result = await db.request_cancel_syllabus_task(task_id, user_id=user["id"])
    if result.get("reason") == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        raise HTTPException(
            409, f"任务当前状态为 {result['reason']}，无法停止"
        )
    return {"ok": True, "status": "cancelled"}


@router.delete("/task/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    if not await db.delete_syllabus_task(task_id, user_id=user["id"]):
        raise HTTPException(404, "任务不存在")
    await mark_task_files_deleted(user["id"], task_id)
    await purge_deleted_oss_files()
    async with session_scope() as session:
        await audit(
            session,
            None,
            action="delete",
            actor_user_id=user["_id"],
            resource_type="syllabus_task",
            resource_id=task_id,
        )
    return {"ok": True}


@router.get("/history")
async def history(user: dict = Depends(current_user)) -> list[dict]:
    return await db.list_syllabi(user_id=user["id"])


@router.get("/record/{record_id}")
async def get_record(
    record_id: str, user: dict = Depends(current_user)
) -> dict:
    record = await db.get_syllabus(record_id, user_id=user["id"])
    if not record:
        raise HTTPException(404, "记录不存在")
    record["output_format"] = detect_output_format(record.get("xml") or "")
    return record


@router.get("/download/{record_id}")
async def download(
    record_id: str, user: dict = Depends(current_user)
) -> Response:
    record = await db.get_syllabus(record_id, user_id=user["id"])
    if not record:
        raise HTTPException(404, "记录不存在")
    async with session_scope() as session:
        await audit(
            session,
            None,
            action="download",
            actor_user_id=user["_id"],
            resource_type="syllabus_record",
            resource_id=record_id,
        )
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
    user: dict = Depends(current_user),
) -> Response:
    record = await db.get_syllabus(record_id, user_id=user["id"])
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
