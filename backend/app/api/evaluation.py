from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, Response

from ai_engine.config import settings
from ai_engine.evaluation import evaluate_transcript
from ai_engine.evaluation.materials import COURSEWARE_EXT, SCRIPT_EXT, SYLLABUS_EXT
from ai_engine.evaluation.pipeline import strip_report_digest
from ai_engine.syllabus import ExportError, export_syllabus
from ai_engine.syllabus.export import content_disposition, export_filename

from ..core import db
from ..core.audit import audit
from ..core.auth import current_user
from ..core.database import session_scope
from ..core.uploads import new_task_id, record_upload, save_user_upload
from ..schemas import TranscriptForm
from ..workers.tasks import STEP_LABELS, run_evaluation

router = APIRouter(prefix="/api/evaluation", tags=["教学视频质量评估"])

ALLOWED_EXT = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v"}
SYLLABUS_MAX_BYTES = 30 * 1024 * 1024
COURSEWARE_MAX_BYTES = 80 * 1024 * 1024
SCRIPT_MAX_BYTES = 30 * 1024 * 1024


def _has_upload(upload: UploadFile | None) -> bool:
    return upload is not None and bool(upload.filename)


def _save_upload(
    upload: UploadFile,
    *,
    user_id: str,
    task_id: str,
    purpose: str,
    allowed: set[str],
    max_bytes: int,
    kind_label: str,
) -> tuple[str, str]:
    return save_user_upload(
        upload,
        user_id=user_id,
        task_id=task_id,
        purpose=purpose,
        allowed=allowed,
        max_bytes=max_bytes,
        kind_label=kind_label,
    )


@router.post("/upload_video")
async def upload_video(
    background: BackgroundTasks,
    file: UploadFile = File(..., description="教学视频（必填）"),
    reference: str | None = Form(
        None, description="课程大纲文本（选填）。上传大纲文件时以文件为准"
    ),
    syllabus: UploadFile | None = File(None, description="课程大纲文件（选填）"),
    courseware: UploadFile | None = File(None, description="课件文件（选填）"),
    transcript: UploadFile | None = File(None, description="讲稿文件（选填），后端当作转写"),
    transcript_text: str | None = Form(None, description="讲稿纯文本（选填），后端当作转写"),
    user: dict = Depends(current_user),
) -> dict:
    has_script_file = _has_upload(transcript)
    script_body = (transcript_text or "").strip() or None
    if script_body and len(script_body) < 10:
        raise HTTPException(400, "讲稿过短，请补充内容或改传文件")

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(
            400, f"不支持的视频格式 {suffix}，支持：{', '.join(sorted(ALLOWED_EXT))}"
        )
    task_id = new_task_id()
    dest, video_key = save_user_upload(
        file,
        user_id=user["id"],
        task_id=task_id,
        purpose="video",
        allowed=ALLOWED_EXT,
        max_bytes=2 * 1024 * 1024 * 1024,
        kind_label="视频",
    )
    dest_path = Path(dest)
    await file.close()

    syllabus_path = None
    courseware_path = None
    transcript_path = None
    try:
        if _has_upload(syllabus):
            syllabus_path, syllabus_key = _save_upload(
                syllabus,
                user_id=user["id"],
                task_id=task_id,
                purpose="syllabus",
                allowed=SYLLABUS_EXT,
                max_bytes=SYLLABUS_MAX_BYTES,
                kind_label="课程大纲",
            )
            await record_upload(
                user_id=user["id"],
                purpose="syllabus",
                original_name=syllabus.filename or "syllabus",
                storage_key=syllabus_key,
                mime_type=syllabus.content_type,
                path=syllabus_path,
            )
        if _has_upload(courseware):
            courseware_path, courseware_key = _save_upload(
                courseware,
                user_id=user["id"],
                task_id=task_id,
                purpose="courseware",
                allowed=COURSEWARE_EXT,
                max_bytes=COURSEWARE_MAX_BYTES,
                kind_label="课件",
            )
            await record_upload(
                user_id=user["id"],
                purpose="courseware",
                original_name=courseware.filename or "courseware",
                storage_key=courseware_key,
                mime_type=courseware.content_type,
                path=courseware_path,
            )
        if has_script_file:
            transcript_path, script_key = _save_upload(
                transcript,
                user_id=user["id"],
                task_id=task_id,
                purpose="transcript",
                allowed=SCRIPT_EXT,
                max_bytes=SCRIPT_MAX_BYTES,
                kind_label="讲稿",
            )
            await record_upload(
                user_id=user["id"],
                purpose="transcript",
                original_name=transcript.filename or "transcript",
                storage_key=script_key,
                mime_type=transcript.content_type,
                path=transcript_path,
            )
    except HTTPException:
        dest_path.unlink(missing_ok=True)
        if syllabus_path:
            Path(syllabus_path).unlink(missing_ok=True)
        if courseware_path:
            Path(courseware_path).unlink(missing_ok=True)
        raise
    finally:
        if syllabus is not None:
            await syllabus.close()
        if courseware is not None:
            await courseware.close()
        if transcript is not None:
            await transcript.close()

    await record_upload(
        user_id=user["id"],
        purpose="video",
        original_name=file.filename or dest_path.name,
        storage_key=video_key,
        mime_type=file.content_type,
        path=dest,
    )
    ref = (reference or "").strip() or None
    filename = file.filename or dest_path.name
    video_path = dest
    await db.create_task(
        filename,
        video_path,
        ref,
        syllabus_path=syllabus_path,
        courseware_path=courseware_path,
        transcript=script_body,
        transcript_path=transcript_path,
        user_id=user["id"],
        task_id=task_id,
    )
    background.add_task(
        run_evaluation,
        task_id,
        video_path,
        ref,
        syllabus_path,
        courseware_path,
        script_body,
        transcript_path,
    )
    return {
        "task_id": task_id,
        "status": "queued",
        "filename": filename,
        "has_reference": bool(ref or syllabus_path),
        "has_syllabus": bool(ref or syllabus_path),
        "has_courseware": bool(courseware_path),
        "has_script": bool(script_body or transcript_path),
    }


@router.get("/tasks")
async def list_tasks(
    user: dict = Depends(current_user),
    status: str | None = None,
    limit: int = 50,
) -> list[dict]:
    tasks = await db.list_tasks(
        user_id=user["id"],
        status=status,
        limit=min(max(limit, 1), 200),
    )
    for t in tasks:
        t["step_label"] = STEP_LABELS.get(t["current_step"], t["current_step"])
    return tasks


@router.get("/task/{task_id}")
async def get_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    task = await db.get_task(task_id, user_id=user["id"])
    if not task:
        raise HTTPException(404, "任务不存在")
    task["step_label"] = STEP_LABELS.get(task["current_step"], task["current_step"])
    return task


_MODALITY_LABEL = {"audio": "音频", "text": "文本", "vision": "图像"}


def _report_title(task: dict) -> str:
    return f"{Path(task.get('filename') or '课堂').stem} · 教学评估报告"


def _format_local_time(ts) -> str:
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError, OSError):
        return ""


def _build_export_markdown(task: dict, report: str) -> str:
    """导出前补标题、日期、得分等页头；不改库里存的报告正文。"""
    result = task.get("result") or {}
    overall = result.get("overall") or {}
    lines = [f"# {_report_title(task)}", ""]

    generated = _format_local_time(task.get("created_at") or task.get("updated_at"))
    if generated:
        lines.append(f"- **生成日期**：{generated}")

    score = overall.get("score")
    if score is not None:
        grade = overall.get("grade") or ""
        label = overall.get("grade_label") or ""
        extra = ""
        if grade:
            extra = f"（{grade} 级"
            if label:
                extra += f" · {label}"
            extra += "）"
        lines.append(f"- **综合得分**：{score} / 100{extra}")

    minutes = overall.get("duration_minutes")
    if minutes not in (None, ""):
        lines.append(f"- **课堂时长**：{minutes} 分钟")

    source = "讲稿评估" if result.get("source") == "transcript" else "视频评估"
    lines.append(f"- **评估方式**：{source}")

    mods = [
        _MODALITY_LABEL.get(m, m)
        for m in (overall.get("modalities") or [])
        if m
    ]
    if mods:
        lines.append(f"- **可用模态**：{'、'.join(mods)}")

    used: list[str] = []
    if result.get("transcript_source") == "script" or task.get("has_script"):
        used.append("讲稿")
    if result.get("has_syllabus") or task.get("has_syllabus"):
        used.append("课程大纲")
    if result.get("has_courseware") or task.get("has_courseware"):
        used.append("上传课件")
    if used:
        lines.append(f"- **对照材料**：{'、'.join(used)}")

    lines.extend(["", "---", "", strip_report_digest(report).strip(), ""])
    return "\n".join(lines)


_FILE_MEDIA = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".mkv": "video/x-matroska",
    ".avi": "video/x-msvideo",
    ".webm": "video/webm",
    ".m4v": "video/mp4",
    ".pdf": "application/pdf",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".html": "text/html",
}


@router.get("/task/{task_id}/export")
async def export_report(
    task_id: str,
    format: str = Query(..., pattern="^(markdown|docx|pdf)$"),
    user: dict = Depends(current_user),
) -> Response:
    """诊断报告导出。Markdown 源走大纲同一套 export_syllabus（docx / pdf 也复用）。"""
    task = await db.get_task(task_id, user_id=user["id"])
    if not task:
        raise HTTPException(404, "任务不存在")
    if task.get("status") != "completed":
        raise HTTPException(400, "评估尚未完成")
    report = ((task.get("result") or {}).get("report") or "").strip()
    if not report:
        raise HTTPException(400, "没有可导出的诊断报告")
    markdown = _build_export_markdown(task, report)
    try:
        content, media_type, suffix = await asyncio.to_thread(
            export_syllabus, markdown, format
        )
    except ExportError as e:
        raise HTTPException(400, str(e)) from e
    except Exception as e:
        raise HTTPException(500, f"导出失败：{e}") from e
    filename = export_filename(_report_title(task), suffix)
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": content_disposition(filename)},
    )


@router.get("/task/{task_id}/chart/{name}")
async def task_chart(
    task_id: str, name: str, user: dict = Depends(current_user)
) -> Response:
    """授课内容 / 声学 / 工具调度页图表。matplotlib 按该任务结果现画 PNG。"""
    from ai_engine.evaluation.audio_charts import CHARTS as AUDIO_CHARTS
    from ai_engine.evaluation.pace_charts import CHARTS as PACE_CHARTS
    from ai_engine.evaluation.tools_charts import CHARTS as TOOLS_CHARTS

    charts = {**PACE_CHARTS, **AUDIO_CHARTS, **TOOLS_CHARTS}
    if name not in charts:
        raise HTTPException(404, "没有这张图")
    task = await db.get_task(task_id, user_id=user["id"])
    if not task:
        raise HTTPException(404, "任务不存在")
    if task.get("status") != "completed" or not task.get("result"):
        raise HTTPException(400, "评估尚未完成")
    try:
        png = await asyncio.to_thread(charts[name], task["result"])
    except Exception as e:
        raise HTTPException(500, f"出图失败：{e}") from e
    return Response(content=png, media_type="image/png")


@router.get("/task/{task_id}/file/{kind}")
async def get_task_file(
    task_id: str, kind: str, user: dict = Depends(current_user)
) -> FileResponse:
    if kind not in {"video", "courseware", "syllabus", "script"}:
        raise HTTPException(400, "不支持的文件类型")
    path = await db.get_task_file_path(task_id, kind, user_id=user["id"])
    if not path:
        raise HTTPException(404, "文件不存在")
    async with session_scope() as session:
        await audit(
            session,
            None,
            action="download",
            actor_user_id=user["_id"],
            resource_type="eval_file",
            resource_id=task_id,
            details={"kind": kind},
        )
    media = _FILE_MEDIA.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path, media_type=media, filename=path.name)


@router.post("/task/{task_id}/cancel")
async def cancel_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    """请求停止排队中或进行中的评估任务（协作式取消）。"""
    result = await db.request_cancel(task_id, user_id=user["id"])
    if result.get("reason") == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        raise HTTPException(
            409, f"任务当前状态为 {result['reason']}，无法停止"
        )
    return {"ok": True, "status": "cancelled"}


@router.delete("/task/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    if not await db.delete_task(task_id, user_id=user["id"]):
        raise HTTPException(404, "任务不存在")
    async with session_scope() as session:
        await audit(
            session,
            None,
            action="delete",
            actor_user_id=user["_id"],
            resource_type="eval_task",
            resource_id=task_id,
        )
    return {"ok": True}


@router.post("/transcript")
async def evaluate_text(
    form: TranscriptForm, user: dict = Depends(current_user)
) -> dict:
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
async def get_frame(
    video_stem: str, filename: str, user: dict = Depends(current_user)
) -> FileResponse:
    """关键帧或课件渲染页。用 resolve 后的前缀检查防止路径穿越。"""
    frame_root = settings.frame_dir.resolve()
    path = (frame_root / video_stem / filename).resolve()
    if not str(path).startswith(str(frame_root)) or not path.is_file():
        raise HTTPException(404, "关键帧不存在")
    if not await db.user_owns_video_stem(user["id"], video_stem):
        raise HTTPException(404, "关键帧不存在")
    return FileResponse(path, media_type="image/jpeg")


@router.get("/rubric")
async def get_rubric_config(user: dict = Depends(current_user)) -> dict:
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
