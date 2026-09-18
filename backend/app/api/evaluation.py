from __future__ import annotations

import asyncio
import json
import shutil
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, Query, Request, UploadFile
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
from ..core.browser_evidence import save_browser_evidence
from ..core.database import session_scope
from ..core.remote_video import ALLOWED_VIDEO_EXT, download_remote_video
from ..core.cloud_drives import inspect_share
from ..core.upload_sessions import (
    complete_session,
    create_session,
    remove_session,
    save_part,
    session_status,
)
from ..core.uploads import record_upload, save_user_upload
from ..core.material_storage import material_reference, purge_deleted_oss_files, release_uploaded_paths, task_material_reference
from ..schemas import (
    EvaluationTaskCreateForm,
    RemoteSourceForm,
    TranscriptForm,
    UploadSessionCompleteForm,
    UploadSessionCreateForm,
)
from ..workers.tasks import STEP_LABELS

router = APIRouter(prefix="/api/evaluation", tags=["教学视频质量评估"])
from .evaluation_followup import router as followup_router
router.include_router(followup_router)

ALLOWED_EXT = ALLOWED_VIDEO_EXT
SYLLABUS_MAX_BYTES = 30 * 1024 * 1024
COURSEWARE_MAX_BYTES = 80 * 1024 * 1024
SCRIPT_MAX_BYTES = 30 * 1024 * 1024


@router.post("/remote-source")
async def inspect_remote_source(form: RemoteSourceForm, user: dict = Depends(current_user)) -> dict:
    return await inspect_share(form.url, form.password, form.path)


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


def _validate_video_filename(filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(
            400, f"不支持的视频格式 {suffix}，支持：{', '.join(sorted(ALLOWED_EXT))}"
        )


def _cleanup_task_uploads(user_id: str, task_id: str) -> None:
    root = settings.upload_dir.resolve()
    task_dir = (root / user_id / task_id).resolve()
    if task_dir.parent == root / user_id and task_dir.is_dir():
        shutil.rmtree(task_dir)


@router.post("/tasks")
async def create_upload_task(
    form: EvaluationTaskCreateForm, user: dict = Depends(current_user)
) -> dict:
    _validate_video_filename(form.filename)
    task_id = await db.create_task(
        form.filename, user_id=user["id"], status="uploading"
    )
    task = await db.get_task(task_id, user_id=user["id"])
    return task or {"id": task_id, "status": "uploading", "filename": form.filename}


def _uploadable_task(task: dict | None) -> dict:
    if not task:
        raise HTTPException(404, "任务不存在")
    if task["status"] not in {"uploading", "upload_failed"}:
        raise HTTPException(409, f"任务当前状态为 {task['status']}，不能继续上传")
    return task


@router.post("/upload-probe")
async def upload_probe(request: Request, _: dict = Depends(current_user)) -> dict:
    """接收一个小型随机请求，仅用于测量浏览器到本服务的真实上行速度。"""
    received = 0
    async for chunk in request.stream():
        received += len(chunk)
        if received > 2 * 1024 * 1024:
            raise HTTPException(413, "测速数据超过2MB")
    if received <= 0:
        raise HTTPException(400, "测速数据为空")
    return {"received_bytes": received}


@router.post("/tasks/{task_id}/upload-session")
async def create_task_upload_session(
    task_id: str,
    form: UploadSessionCreateForm,
    user: dict = Depends(current_user),
) -> dict:
    task = _uploadable_task(await db.get_task(task_id, user_id=user["id"]))
    if await task_material_reference(user["id"], task_id):
        return {"complete": True, "task": task}
    if Path(form.original_filename).name != task.get("filename"):
        raise HTTPException(400, "上传文件名与任务不一致")
    return await asyncio.to_thread(
        create_session,
        user["id"],
        task_id,
        mode=form.mode,
        fingerprint=form.fingerprint,
        original_filename=form.original_filename,
        original_size=form.original_size,
        audio_filename=form.audio_filename,
        audio_mime=form.audio_mime,
    )


@router.get("/tasks/{task_id}/upload-session")
async def get_task_upload_session(
    task_id: str, user: dict = Depends(current_user)
) -> dict:
    task = _uploadable_task(await db.get_task(task_id, user_id=user["id"]))
    if await task_material_reference(user["id"], task_id):
        return {"complete": True, "task": task}
    return await asyncio.to_thread(session_status, user["id"], task_id)


@router.delete("/tasks/{task_id}/upload-session")
async def reset_task_upload_session(
    task_id: str, user: dict = Depends(current_user)
) -> dict:
    task = _uploadable_task(await db.get_task(task_id, user_id=user["id"]))
    if await task_material_reference(user["id"], task_id):
        raise HTTPException(409, "视频已经上传完成，不能重置上传会话")
    await remove_session(user["id"], task_id)
    return {"ok": True}


@router.put("/tasks/{task_id}/upload-session/parts/{kind}/{index}")
async def upload_task_part(
    task_id: str,
    kind: str,
    index: int,
    request: Request,
    x_upload_session: str | None = Header(None),
    x_part_sha256: str | None = Header(None),
    user: dict = Depends(current_user),
) -> dict:
    _uploadable_task(await db.get_task(task_id, user_id=user["id"]))
    result = await save_part(
        user["id"],
        task_id,
        kind=kind,
        index=index,
        session_token=x_upload_session,
        expected_sha256=x_part_sha256 or "",
        chunks=request.stream(),
    )
    status = await asyncio.to_thread(session_status, user["id"], task_id)
    progress = None
    if status["mode"] == "original":
        progress = min(99, round(status["uploaded_bytes"] / status["original_size"] * 100))
    await db.update_task(
        task_id,
        progress=progress if progress is not None else 0,
        current_step="uploading",
        step_detail={
            "phase": "chunk_upload",
            "mode": status["mode"],
            "uploaded_bytes": status["uploaded_bytes"],
        },
    )
    return {**result, "uploaded_bytes": status["uploaded_bytes"]}


@router.post("/tasks/{task_id}/upload-session/complete")
async def complete_task_upload_session(
    task_id: str,
    form: UploadSessionCompleteForm,
    user: dict = Depends(current_user),
) -> dict:
    task = _uploadable_task(await db.get_task(task_id, user_id=user["id"]))
    if await task_material_reference(user["id"], task_id):
        return task
    result = await asyncio.to_thread(
        complete_session,
        user["id"],
        task_id,
        session_token=form.session_id,
        audio_parts=form.audio_parts,
        frame_parts=form.frame_parts,
        raw_manifest=form.manifest,
    )
    try:
        await record_upload(
            user_id=user["id"],
            purpose="video",
            original_name=result["original_filename"],
            storage_key=result["storage_key"],
            mime_type=result["mime_type"],
            path=result["path"],
        )
        saved = await db.set_task_materials(
            task_id,
            user["id"],
            filename=result["original_filename"],
            video_path=material_reference(result["path"], result["storage_key"], evidence=result["mode"] == "evidence"),
        )
        if not saved:
            raise HTTPException(409, "任务已取消或当前状态不允许上传")
        await remove_session(user["id"], task_id)
        await release_uploaded_paths(user["id"], task_id, result["path"])
        return saved
    except Exception:
        Path(result["path"]).unlink(missing_ok=True)
        if result["mode"] == "evidence":
            (Path(result["path"]).parent / "browser-evidence.json").unlink(missing_ok=True)
            shutil.rmtree(settings.frame_dir / Path(result["path"]).stem, ignore_errors=True)
        raise


@router.post("/tasks/{task_id}/aux-materials")
async def upload_task_aux_materials(
    task_id: str,
    reference: str | None = Form(None),
    syllabus: UploadFile | None = File(None),
    courseware: UploadFile | None = File(None),
    transcript: UploadFile | None = File(None),
    transcript_text: str | None = Form(None),
    user: dict = Depends(current_user),
) -> dict:
    _uploadable_task(await db.get_task(task_id, user_id=user["id"]))
    script_body = (transcript_text or "").strip() or None
    if script_body and len(script_body) < 10:
        raise HTTPException(400, "讲稿过短，请补充内容或改传文件")
    fields: dict[str, str] = {}
    if (reference or "").strip():
        fields["reference"] = reference.strip()
    if script_body:
        fields["transcript"] = script_body
    saved_paths: list[Path] = []
    try:
        for upload, purpose, allowed, max_bytes, label, field in (
            (syllabus, "syllabus", SYLLABUS_EXT, SYLLABUS_MAX_BYTES, "课程大纲", "syllabus_path"),
            (courseware, "courseware", COURSEWARE_EXT, COURSEWARE_MAX_BYTES, "课件", "courseware_path"),
            (transcript, "transcript", SCRIPT_EXT, SCRIPT_MAX_BYTES, "讲稿", "transcript_path"),
        ):
            if not _has_upload(upload):
                continue
            path, key = await asyncio.to_thread(
                _save_upload,
                upload,
                user_id=user["id"],
                task_id=task_id,
                purpose=purpose,
                allowed=allowed,
                max_bytes=max_bytes,
                kind_label=label,
            )
            saved_paths.append(Path(path))
            fields[field] = path
            await record_upload(
                user_id=user["id"],
                purpose=purpose,
                original_name=upload.filename or purpose,
                storage_key=key,
                mime_type=upload.content_type,
                path=path,
            )
            fields[field] = material_reference(path, key)
        saved = await db.set_task_materials(task_id, user["id"], **fields)
        if not saved:
            raise HTTPException(409, "任务已取消或当前状态不允许上传")
        await release_uploaded_paths(user["id"], task_id, *(str(path) for path in saved_paths))
        return saved
    except Exception:
        for path in saved_paths:
            path.unlink(missing_ok=True)
        raise
    finally:
        for upload in (syllabus, courseware, transcript):
            if upload is not None:
                await upload.close()


async def _store_task_materials(
    task_id: str,
    user: dict,
    file: UploadFile | None,
    reference: str | None,
    syllabus: UploadFile | None,
    courseware: UploadFile | None,
    transcript: UploadFile | None,
    transcript_text: str | None,
    evidence_audio: UploadFile | None = None,
    evidence_archive: UploadFile | None = None,
    evidence_manifest: str | None = None,
    video_url: str | None = None,
    share_password: str = "",
    share_file_id: str = "",
    share_path: str = "[]",
) -> dict:
    task = await db.get_task(task_id, user_id=user["id"])
    if not task:
        raise HTTPException(404, "任务不存在")
    if task["status"] not in {"uploading", "upload_failed"}:
        raise HTTPException(409, f"任务当前状态为 {task['status']}，不能上传材料")
    script_body = (transcript_text or "").strip() or None
    has_video = _has_upload(file)
    evidence_parts = (
        _has_upload(evidence_audio),
        _has_upload(evidence_archive),
        bool((evidence_manifest or "").strip()),
    )
    has_evidence = all(evidence_parts)
    remote_url = (video_url or "").strip()
    has_remote = bool(remote_url)
    try:
        if any(evidence_parts) and not has_evidence:
            raise HTTPException(400, "浏览器证据包不完整，请重新处理后上传")
        if sum((has_video, has_evidence, has_remote)) > 1:
            raise HTTPException(400, "原视频、浏览器证据包和视频链接只能选择一种")
        if not any((has_video, has_evidence, has_remote)):
            raise HTTPException(400, "请上传原视频、完整的浏览器证据包或填写视频直链")
        _validate_video_filename(task.get("filename") or (file.filename if file else ""))
        if script_body and len(script_body) < 10:
            raise HTTPException(400, "讲稿过短，请补充内容或改传文件")
    except HTTPException as exc:
        await db.update_task(
            task_id,
            status="upload_failed",
            current_step="upload_failed",
            error=str(exc.detail),
        )
        raise

    dest = None
    video_key = None
    syllabus_path = None
    courseware_path = None
    transcript_path = None
    original_video_name = task.get("filename") or (file.filename if file else "教学视频")
    video_mime_type = None
    try:
        if has_evidence:
            dest, video_key, _ = await asyncio.to_thread(
                save_browser_evidence,
                audio=evidence_audio,
                archive=evidence_archive,
                raw_manifest=evidence_manifest,
                user_id=user["id"],
                task_id=task_id,
            )
            video_mime_type = evidence_audio.content_type
        elif has_remote:
            try:
                parsed_path = json.loads(share_path)
                if not isinstance(parsed_path, list):
                    raise ValueError()
                source_form = RemoteSourceForm(url=remote_url, password=share_password, path=parsed_path)
                if len(share_file_id) > 2048:
                    raise ValueError()
            except (ValueError, TypeError):
                raise HTTPException(400, "网盘选择参数无效，请重新读取链接") from None

            async def remote_progress(downloaded: int, total: int | None) -> None:
                current = await db.get_task(task_id, user_id=user["id"])
                if not current or current["status"] == "cancelled":
                    raise HTTPException(409, "导入已取消")
                if total:
                    progress = min(95, max(1, round(downloaded / total * 95)))
                else:
                    progress = min(90, max(1, round(downloaded / (128 * 1024 * 1024))))
                await db.update_task(
                    task_id,
                    progress=progress,
                    current_step="remote_downloading",
                    step_detail={
                        "phase": "download",
                        "downloaded_bytes": downloaded,
                        "total_bytes": total,
                    },
                )

            await db.update_task(
                task_id,
                progress=1,
                current_step="remote_downloading",
                step_detail={"phase": "connecting"},
            )
            remote = await download_remote_video(
                remote_url,
                user_id=user["id"],
                task_id=task_id,
                on_progress=remote_progress,
                share_password=source_form.password,
                share_file_id=share_file_id,
                share_path=source_form.path,
            )
            dest = remote.path
            video_key = remote.storage_key
            original_video_name = remote.filename
            video_mime_type = remote.mime_type
            await db.update_task(
                task_id,
                progress=97,
                current_step="remote_downloading",
                step_detail={
                    "phase": "validating",
                    "downloaded_bytes": remote.size_bytes,
                    "total_bytes": remote.size_bytes,
                },
            )
        else:
            dest, video_key = await asyncio.to_thread(
                save_user_upload,
                file,
                user_id=user["id"],
                task_id=task_id,
                purpose="video",
                allowed=ALLOWED_EXT,
                max_bytes=2 * 1024 * 1024 * 1024,
                kind_label="视频",
            )
            video_mime_type = file.content_type
        current = await db.get_task(task_id, user_id=user["id"])
        if not current or current["status"] == "cancelled":
            raise HTTPException(409, "上传已取消")

        for upload, purpose, allowed, max_bytes, label in (
            (syllabus, "syllabus", SYLLABUS_EXT, SYLLABUS_MAX_BYTES, "课程大纲"),
            (courseware, "courseware", COURSEWARE_EXT, COURSEWARE_MAX_BYTES, "课件"),
            (transcript, "transcript", SCRIPT_EXT, SCRIPT_MAX_BYTES, "讲稿"),
        ):
            if not _has_upload(upload):
                continue
            saved_path, storage_key = await asyncio.to_thread(
                _save_upload,
                upload,
                user_id=user["id"],
                task_id=task_id,
                purpose=purpose,
                allowed=allowed,
                max_bytes=max_bytes,
                kind_label=label,
            )
            if purpose == "syllabus":
                syllabus_path = saved_path
            elif purpose == "courseware":
                courseware_path = saved_path
            else:
                transcript_path = saved_path
            await record_upload(
                user_id=user["id"],
                purpose=purpose,
                original_name=upload.filename or purpose,
                storage_key=storage_key,
                mime_type=upload.content_type,
                path=saved_path,
            )

        await record_upload(
            user_id=user["id"],
            purpose="video",
            original_name=original_video_name,
            storage_key=video_key,
            mime_type=video_mime_type,
            path=dest,
        )
        saved = await db.set_task_materials(
            task_id,
            user["id"],
            filename=original_video_name,
            video_path=material_reference(dest, video_key, evidence=has_evidence),
            reference=(reference or "").strip() or None,
            syllabus_path=material_reference(syllabus_path),
            courseware_path=material_reference(courseware_path),
            transcript=script_body,
            transcript_path=material_reference(transcript_path),
        )
        if not saved:
            raise HTTPException(409, "任务已取消或当前状态不允许上传")
        await release_uploaded_paths(user["id"], task_id, dest, syllabus_path, courseware_path, transcript_path)
        return saved
    except Exception as exc:
        _cleanup_task_uploads(user["id"], task_id)
        if dest and has_evidence:
            shutil.rmtree(settings.frame_dir / Path(dest).stem, ignore_errors=True)
        current = await db.get_task(task_id, user_id=user["id"])
        if current and current["status"] != "cancelled":
            await db.update_task(
                task_id,
                status="upload_failed",
                current_step="upload_failed",
                error=str(getattr(exc, "detail", exc)),
            )
        raise
    finally:
        for upload in (file, syllabus, courseware, transcript, evidence_audio, evidence_archive):
            if upload is not None:
                await upload.close()


@router.post("/tasks/{task_id}/materials")
async def upload_task_materials(
    task_id: str,
    file: UploadFile | None = File(None, description="教学视频"),
    reference: str | None = Form(None),
    syllabus: UploadFile | None = File(None),
    courseware: UploadFile | None = File(None),
    transcript: UploadFile | None = File(None),
    transcript_text: str | None = Form(None),
    evidence_audio: UploadFile | None = File(None),
    evidence_archive: UploadFile | None = File(None),
    evidence_manifest: str | None = Form(None),
    video_url: str | None = Form(None),
    share_password: str = Form(""),
    share_file_id: str = Form(""),
    share_path: str = Form("[]"),
    user: dict = Depends(current_user),
) -> dict:
    return await _store_task_materials(
        task_id,
        user,
        file,
        reference,
        syllabus,
        courseware,
        transcript,
        transcript_text,
        evidence_audio,
        evidence_archive,
        evidence_manifest,
        video_url,
        share_password,
        share_file_id,
        share_path,
    )


@router.post("/tasks/{task_id}/submit")
async def submit_upload_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    result = await db.submit_task(task_id, user["id"])
    if result.get("reason") == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        detail = (
            "视频尚未上传"
            if result["reason"] == "missing_video"
            else f"任务当前状态为 {result['reason']}，不能提交"
        )
        raise HTTPException(409, detail)
    return result["task"]


@router.post("/upload_video")
async def upload_video(
    file: UploadFile = File(...),
    reference: str | None = Form(None),
    syllabus: UploadFile | None = File(None),
    courseware: UploadFile | None = File(None),
    transcript: UploadFile | None = File(None),
    transcript_text: str | None = Form(None),
    user: dict = Depends(current_user),
) -> dict:
    """兼容旧客户端；新客户端应使用 create -> materials -> submit。"""
    _validate_video_filename(file.filename or "")
    task_id = await db.create_task(
        file.filename or "教学视频", user_id=user["id"], status="uploading"
    )
    await _store_task_materials(
        task_id, user, file, reference, syllabus, courseware, transcript, transcript_text
    )
    result = await db.submit_task(task_id, user["id"])
    if not result["ok"]:
        raise HTTPException(409, f"任务当前状态为 {result['reason']}，不能提交")
    return {"task_id": task_id, **result["task"]}


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
    ".m4a": "audio/mp4",
    ".mp3": "audio/mpeg",
    ".flac": "audio/flac",
    ".wav": "audio/wav",
    ".mka": "audio/x-matroska",
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
    # Authorize against the owned task before creating any OSS download capability.
    from ..core.material_storage import is_oss_reference, object_key
    from ..core.storage import get_storage
    from fastapi.responses import RedirectResponse
    reference = await task_material_reference(user["id"], task_id, kind)
    if reference and is_oss_reference(reference):
        key = object_key(reference, owner=user["id"], task_id=task_id)
        url = await asyncio.to_thread(get_storage("oss").signed_download_url, key, 300)
        async with session_scope() as session:
            await audit(session, None, action="download", actor_user_id=user["_id"],
                        resource_type="eval_file", resource_id=task_id, details={"kind": kind})
        return RedirectResponse(url, status_code=302, headers={"Cache-Control": "no-store"})
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
    task = await db.get_task(task_id, user_id=user["id"])
    result = await db.request_cancel(task_id, user_id=user["id"])
    if result.get("reason") == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        raise HTTPException(
            409, f"任务当前状态为 {result['reason']}，无法停止"
        )
    if result["status"] == "cancelled" and task and task.get("status") == "uploading":
        _cleanup_task_uploads(user["id"], task_id)
    return {"ok": True, "status": result["status"]}


@router.delete("/task/{task_id}")
async def delete_task(task_id: str, user: dict = Depends(current_user)) -> dict:
    result = await db.delete_task(task_id, user_id=user["id"])
    if result.get("reason") == "not_found":
        raise HTTPException(404, "任务不存在")
    if not result["ok"]:
        raise HTTPException(409, "任务尚未结束，请先停止任务并等待其完全退出")
    await purge_deleted_oss_files()
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
