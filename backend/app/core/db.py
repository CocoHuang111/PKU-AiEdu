"""PostgreSQL 业务仓储。对外函数名尽量保持原样，前端时间字段仍返回 Unix 秒。"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_engine.config import settings

from ..models import EvalTask, QASession, StoredFile, SyllabusRecord, SyllabusTask
from .database import session_scope, sync_session_scope
from .storage import get_storage


def new_id() -> str:
    return str(uuid.uuid4())


def _uid(value: str | uuid.UUID) -> uuid.UUID:
    return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))


def _sid(value: str | uuid.UUID | None) -> str | None:
    if value is None:
        return None
    return str(value)


def _ts(value: datetime | None) -> float | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.timestamp()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _as_json(value: Any, default: Any = None) -> Any:
    if value is None:
        return default
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default
    return default


def _owned(stmt: Select, model, user_id: str | uuid.UUID | None) -> Select:
    if user_id is None:
        return stmt
    return stmt.where(model.user_id == _uid(user_id))


# ---------------------------------------------------------------- 评估任务


def _original_name(stored: str, kind: str | None = None) -> str:
    name = Path(stored).name
    return name


def _material_entry(
    path: str | None,
    *,
    fallback: str | None = None,
    kind: str | None = None,
) -> dict[str, Any] | None:
    if not path and not fallback:
        return None
    name = fallback or "未命名"
    size = 0
    if path:
        p = Path(path)
        name = _original_name(p.name, kind) or fallback or p.name
        try:
            if p.is_file():
                size = p.stat().st_size
        except OSError:
            pass
    return {"name": name, "size": size}


def _task_materials(row: EvalTask) -> dict[str, Any]:
    video = _material_entry(row.video_path, fallback=row.filename, kind="video")
    syllabus = _material_entry(row.syllabus_path, kind="syllabus")
    if not syllabus and row.reference:
        syllabus = {"name": "课程大纲文本", "size": 0}
    script = _material_entry(row.transcript_path, kind="script")
    if not script and row.transcript:
        script = {"name": "讲稿文本", "size": 0}
    return {
        "video": video,
        "courseware": _material_entry(row.courseware_path, kind="courseware"),
        "syllabus": syllabus,
        "script": script,
    }


def _task_row(row: EvalTask, with_result: bool = True) -> dict[str, Any]:
    task = {
        "id": str(row.id),
        "user_id": str(row.user_id),
        "filename": row.filename,
        "status": row.status,
        "progress": row.progress,
        "current_step": row.current_step,
        "step_detail": _as_json(row.step_detail, {}),
        "error": row.error,
        "created_at": _ts(row.created_at),
        "updated_at": _ts(row.updated_at),
        "has_syllabus": bool(row.reference or row.syllabus_path),
        "has_courseware": bool(row.courseware_path),
        "has_script": bool(row.transcript or row.transcript_path),
        "materials": _task_materials(row),
    }
    if with_result:
        task["result"] = _as_json(row.result)
        task["reference"] = row.reference
    else:
        result = _as_json(row.result) or {}
        overall = result.get("overall") if isinstance(result, dict) else None
        task["summary"] = overall
    return task


async def create_task(
    filename: str,
    video_path: str | None = None,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript: str | None = None,
    transcript_path: str | None = None,
    user_id: str | uuid.UUID | None = None,
    task_id: str | uuid.UUID | None = None,
) -> str:
    if not user_id:
        raise ValueError("创建评估任务必须有 user_id")
    row = EvalTask(
        id=_uid(task_id) if task_id else uuid.uuid4(),
        user_id=_uid(user_id),
        filename=filename,
        video_path=video_path or "",
        reference=reference,
        syllabus_path=syllabus_path,
        courseware_path=courseware_path,
        transcript=transcript,
        transcript_path=transcript_path,
        status="queued",
        progress=0,
        current_step="queued",
    )
    async with session_scope() as session:
        session.add(row)
        await session.flush()
        return str(row.id)


async def update_task(task_id: str, **fields) -> None:
    if not fields:
        return
    if "result" in fields and isinstance(fields["result"], str):
        fields["result"] = _as_json(fields["result"])
    if "step_detail" in fields and isinstance(fields["step_detail"], str):
        fields["step_detail"] = _as_json(fields["step_detail"], {})
    fields["updated_at"] = _now()
    async with session_scope() as session:
        row = await session.get(EvalTask, _uid(task_id))
        if not row:
            return
        for key, value in fields.items():
            if hasattr(row, key):
                setattr(row, key, value)


async def get_task(task_id: str, user_id: str | None = None) -> dict[str, Any] | None:
    async with session_scope() as session:
        stmt = _owned(select(EvalTask).where(EvalTask.id == _uid(task_id)), EvalTask, user_id)
        row = await session.scalar(stmt)
        return _task_row(row) if row else None


async def list_tasks(
    limit: int = 50,
    user_id: str | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    async with session_scope() as session:
        stmt = _owned(select(EvalTask), EvalTask, user_id)
        if status:
            stmt = stmt.where(EvalTask.status == status)
        stmt = stmt.order_by(EvalTask.created_at.desc()).limit(limit)
        rows = (await session.scalars(stmt)).all()
        return [_task_row(row, with_result=False) for row in rows]


async def delete_task(task_id: str, user_id: str | None = None) -> bool:
    async with session_scope() as session:
        stmt = _owned(select(EvalTask).where(EvalTask.id == _uid(task_id)), EvalTask, user_id)
        row = await session.scalar(stmt)
        if not row:
            return False
        owner = str(row.user_id)
        await session.delete(row)
    try:
        from ai_engine.rag.store import delete_eval_report_chunks

        delete_eval_report_chunks(task_id, owner)
    except Exception as exc:
        print(f"[warn] 删除评估报告向量失败: {exc}")
    return True


def is_task_cancelled(task_id: str) -> bool:
    with sync_session_scope() as session:
        row = session.get(EvalTask, _uid(task_id))
    return row is not None and row.status == "cancelled"


async def request_cancel(
    task_id: str, user_id: str | None = None
) -> dict[str, Any]:
    task = await get_task(task_id, user_id=user_id)
    if not task:
        return {"ok": False, "reason": "not_found"}
    if task["status"] in ("completed", "failed", "cancelled"):
        return {"ok": False, "reason": task["status"]}
    await update_task(
        task_id,
        status="cancelled",
        current_step="cancelled",
        step_detail={},
        error=None,
    )
    return {"ok": True}


_FILE_COLS = {
    "video": "video_path",
    "courseware": "courseware_path",
    "syllabus": "syllabus_path",
    "script": "transcript_path",
}


async def user_owns_video_stem(user_id: str, video_stem: str) -> bool:
    if not video_stem or ".." in video_stem or "/" in video_stem:
        return False
    async with session_scope() as session:
        stmt = select(EvalTask).where(
            EvalTask.user_id == _uid(user_id),
            EvalTask.video_path.ilike(f"%{video_stem}%"),
        )
        return (await session.scalar(stmt)) is not None


async def get_task_file_path(
    task_id: str, kind: str, user_id: str | None = None
) -> Path | None:
    col = _FILE_COLS.get(kind)
    if not col:
        return None
    async with session_scope() as session:
        stmt = _owned(select(EvalTask).where(EvalTask.id == _uid(task_id)), EvalTask, user_id)
        row = await session.scalar(stmt)
        if not row:
            return None
        raw = getattr(row, col)
    if not raw:
        return None
    path = Path(raw).resolve()
    root = settings.upload_dir.resolve()
    if not str(path).startswith(str(root)) or not path.is_file():
        return None
    return path


# ---------------------------------------------------------------- 大纲优化任务


def _syllabus_task_row(
    row: SyllabusTask,
    *,
    with_result: bool = True,
    include_source: bool = False,
) -> dict[str, Any]:
    task = {
        "id": str(row.id),
        "user_id": str(row.user_id),
        "filename": row.filename,
        "prompt_mode": row.prompt_mode,
        "status": row.status,
        "progress": row.progress,
        "current_step": row.current_step,
        "step_detail": _as_json(row.step_detail, {}),
        "record_id": _sid(row.record_id),
        "error": row.error,
        "created_at": _ts(row.created_at),
        "updated_at": _ts(row.updated_at),
    }
    if include_source:
        task["source_path"] = row.source_path
        task["source_text"] = row.source_text
    if with_result:
        task["result"] = _as_json(row.result)
    else:
        result = _as_json(row.result) or {}
        task["summary"] = {
            "course_name": result.get("course_name") if isinstance(result, dict) else None,
            "valid": result.get("valid") if isinstance(result, dict) else None,
        }
    return task


async def create_syllabus_task(
    *,
    filename: str,
    prompt_mode: str | None,
    source_path: str | None = None,
    source_text: str | None = None,
    user_id: str | uuid.UUID | None = None,
    task_id: str | uuid.UUID | None = None,
) -> str:
    if not user_id:
        raise ValueError("创建大纲任务必须有 user_id")
    row = SyllabusTask(
        id=_uid(task_id) if task_id else uuid.uuid4(),
        user_id=_uid(user_id),
        filename=filename,
        source_path=source_path,
        source_text=source_text,
        prompt_mode=prompt_mode,
        status="queued",
        progress=0,
        current_step="queued",
    )
    async with session_scope() as session:
        session.add(row)
        await session.flush()
        return str(row.id)


async def update_syllabus_task(task_id: str, **fields) -> None:
    if not fields:
        return
    if "result" in fields and isinstance(fields["result"], str):
        fields["result"] = _as_json(fields["result"])
    if "step_detail" in fields and isinstance(fields["step_detail"], str):
        fields["step_detail"] = _as_json(fields["step_detail"], {})
    if "record_id" in fields and fields["record_id"]:
        fields["record_id"] = _uid(fields["record_id"])
    fields["updated_at"] = _now()
    async with session_scope() as session:
        row = await session.get(SyllabusTask, _uid(task_id))
        if not row:
            return
        for key, value in fields.items():
            if hasattr(row, key):
                setattr(row, key, value)


async def get_syllabus_task(
    task_id: str,
    *,
    include_source: bool = False,
    user_id: str | None = None,
) -> dict[str, Any] | None:
    async with session_scope() as session:
        stmt = _owned(
            select(SyllabusTask).where(SyllabusTask.id == _uid(task_id)),
            SyllabusTask,
            user_id,
        )
        row = await session.scalar(stmt)
        return (
            _syllabus_task_row(row, include_source=include_source) if row else None
        )


async def list_syllabus_tasks(
    limit: int = 50, user_id: str | None = None
) -> list[dict[str, Any]]:
    async with session_scope() as session:
        stmt = _owned(select(SyllabusTask), SyllabusTask, user_id).order_by(
            SyllabusTask.created_at.desc()
        ).limit(limit)
        rows = (await session.scalars(stmt)).all()
        return [_syllabus_task_row(row, with_result=False) for row in rows]


def is_syllabus_task_cancelled(task_id: str) -> bool:
    with sync_session_scope() as session:
        row = session.get(SyllabusTask, _uid(task_id))
    return row is not None and row.status == "cancelled"


async def request_cancel_syllabus_task(
    task_id: str, user_id: str | None = None
) -> dict[str, Any]:
    task = await get_syllabus_task(task_id, user_id=user_id)
    if not task:
        return {"ok": False, "reason": "not_found"}
    if task["status"] in ("completed", "failed", "cancelled"):
        return {"ok": False, "reason": task["status"]}
    await update_syllabus_task(
        task_id,
        status="cancelled",
        current_step="cancelled",
        step_detail={},
        error=None,
    )
    return {"ok": True}


async def delete_syllabus_task(
    task_id: str, user_id: str | None = None
) -> bool:
    async with session_scope() as session:
        stmt = _owned(
            select(SyllabusTask).where(SyllabusTask.id == _uid(task_id)),
            SyllabusTask,
            user_id,
        )
        task = await session.scalar(stmt)
        if not task:
            return False
        if task.record_id:
            record = await session.get(SyllabusRecord, task.record_id)
            if record and (user_id is None or record.user_id == _uid(user_id)):
                await session.delete(record)
        await session.delete(task)
        return True


# ---------------------------------------------------------------- 问答会话


def _history_pending(history: list | None) -> bool:
    if not history:
        return False
    last = history[-1]
    return isinstance(last, dict) and last.get("role") == "assistant" and bool(
        last.get("pending")
    )


def _session_row(row: QASession, include_history: bool = True) -> dict[str, Any]:
    history = _as_json(row.history, [])
    payload = {
        "id": str(row.id),
        "user_id": str(row.user_id),
        "title": row.title,
        "created_at": _ts(row.created_at),
        "updated_at": _ts(row.updated_at),
        "pinned": bool(row.pinned),
        "pending": _history_pending(history),
    }
    if include_history:
        payload["history"] = history
    return payload


async def save_session(
    session_id: str | None,
    history: list[dict],
    title: str | None = None,
    user_id: str | uuid.UUID | None = None,
) -> str:
    if not user_id:
        raise ValueError("保存问答会话必须有 user_id")
    now = _now()
    async with session_scope() as session:
        if session_id:
            stmt = _owned(
                select(QASession).where(QASession.id == _uid(session_id)),
                QASession,
                user_id,
            )
            row = await session.scalar(stmt)
            if row:
                row.history = history
                row.updated_at = now
                return str(row.id)
        first = next((h["content"] for h in history if h["role"] == "user"), "新会话")
        row = QASession(
            id=_uid(session_id) if session_id else uuid.uuid4(),
            user_id=_uid(user_id),
            title=title or first[:40],
            history=history,
            created_at=now,
            updated_at=now,
        )
        session.add(row)
        await session.flush()
        return str(row.id)


async def get_session(
    session_id: str, user_id: str | None = None
) -> dict[str, Any] | None:
    async with session_scope() as session:
        stmt = _owned(
            select(QASession).where(QASession.id == _uid(session_id)),
            QASession,
            user_id,
        )
        row = await session.scalar(stmt)
        return _session_row(row) if row else None


async def list_sessions(
    limit: int = 50, user_id: str | None = None
) -> list[dict[str, Any]]:
    async with session_scope() as session:
        stmt = _owned(select(QASession), QASession, user_id).order_by(
            QASession.pinned.desc(), QASession.updated_at.desc()
        ).limit(limit)
        rows = (await session.scalars(stmt)).all()
        return [_session_row(row, include_history=False) for row in rows]


async def update_session(
    session_id: str,
    *,
    title: str | None = None,
    pinned: bool | None = None,
    user_id: str | None = None,
) -> dict[str, Any] | None:
    async with session_scope() as session:
        stmt = _owned(
            select(QASession).where(QASession.id == _uid(session_id)),
            QASession,
            user_id,
        )
        row = await session.scalar(stmt)
        if not row:
            return None
        if title is not None:
            row.title = title
        if pinned is not None:
            row.pinned = pinned
        return _session_row(row)


async def delete_session(
    session_id: str, user_id: str | None = None
) -> bool:
    async with session_scope() as session:
        stmt = _owned(
            select(QASession).where(QASession.id == _uid(session_id)),
            QASession,
            user_id,
        )
        row = await session.scalar(stmt)
        if not row:
            return False
        await session.delete(row)
        return True


# ---------------------------------------------------------------- 大纲记录


async def save_syllabus(
    filename: str,
    course_name: str,
    original_text: str,
    xml: str,
    valid: bool,
    user_id: str | uuid.UUID | None = None,
) -> str:
    if not user_id:
        raise ValueError("保存大纲记录必须有 user_id")
    row = SyllabusRecord(
        user_id=_uid(user_id),
        filename=filename,
        course_name=course_name,
        original_text=original_text,
        xml=xml,
        valid=bool(valid),
    )
    async with session_scope() as session:
        session.add(row)
        await session.flush()
        return str(row.id)


async def list_syllabi(
    limit: int = 50, user_id: str | None = None
) -> list[dict[str, Any]]:
    async with session_scope() as session:
        stmt = _owned(select(SyllabusRecord), SyllabusRecord, user_id).order_by(
            SyllabusRecord.created_at.desc()
        ).limit(limit)
        rows = (await session.scalars(stmt)).all()
        return [
            {
                "id": str(r.id),
                "filename": r.filename,
                "course_name": r.course_name,
                "valid": bool(r.valid),
                "created_at": _ts(r.created_at),
            }
            for r in rows
        ]


async def get_syllabus(
    record_id: str, user_id: str | None = None
) -> dict[str, Any] | None:
    async with session_scope() as session:
        stmt = _owned(
            select(SyllabusRecord).where(SyllabusRecord.id == _uid(record_id)),
            SyllabusRecord,
            user_id,
        )
        row = await session.scalar(stmt)
        if not row:
            return None
        return {
            "id": str(row.id),
            "user_id": str(row.user_id),
            "filename": row.filename,
            "course_name": row.course_name,
            "original_text": row.original_text,
            "xml": row.xml,
            "valid": bool(row.valid),
            "created_at": _ts(row.created_at),
        }


# ---------------------------------------------------------------- 文件元数据


async def create_stored_file(
    *,
    user_id: str | uuid.UUID,
    purpose: str,
    original_name: str,
    storage_key: str,
    mime_type: str | None,
    size_bytes: int,
    sha256: str | None = None,
    storage_backend: str = "local",
) -> str:
    row = StoredFile(
        user_id=_uid(user_id),
        purpose=purpose,
        original_name=original_name,
        storage_backend=storage_backend,
        storage_key=storage_key,
        mime_type=mime_type,
        size_bytes=size_bytes,
        sha256=sha256,
    )
    async with session_scope() as session:
        session.add(row)
        await session.flush()
        return str(row.id)


async def get_stored_file(
    file_id: str, user_id: str | None = None
) -> dict[str, Any] | None:
    async with session_scope() as session:
        stmt = select(StoredFile).where(
            StoredFile.id == _uid(file_id),
            StoredFile.deleted_at.is_(None),
        )
        stmt = _owned(stmt, StoredFile, user_id)
        row = await session.scalar(stmt)
        if not row:
            return None
        return {
            "id": str(row.id),
            "user_id": str(row.user_id),
            "purpose": row.purpose,
            "original_name": row.original_name,
            "storage_backend": row.storage_backend,
            "storage_key": row.storage_key,
            "mime_type": row.mime_type,
            "size_bytes": row.size_bytes,
            "sha256": row.sha256,
        }


async def soft_delete_stored_file(file_id: str, user_id: str | None = None) -> bool:
    async with session_scope() as session:
        stmt = select(StoredFile).where(
            StoredFile.id == _uid(file_id),
            StoredFile.deleted_at.is_(None),
        )
        stmt = _owned(stmt, StoredFile, user_id)
        row = await session.scalar(stmt)
        if not row:
            return False
        row.deleted_at = _now()
        return True


def stored_file_disk_path(storage_key: str, backend: str = "local") -> Path:
    return get_storage(backend).path_for(storage_key)


async def count_tasks_by_user(session: AsyncSession, user_id: uuid.UUID) -> dict[str, int]:
    eval_count = await session.scalar(
        select(func.count()).select_from(EvalTask).where(EvalTask.user_id == user_id)
    )
    syllabus_count = await session.scalar(
        select(func.count()).select_from(SyllabusTask).where(SyllabusTask.user_id == user_id)
    )
    qa_count = await session.scalar(
        select(func.count()).select_from(QASession).where(QASession.user_id == user_id)
    )
    return {
        "eval_tasks": int(eval_count or 0),
        "syllabus_tasks": int(syllabus_count or 0),
        "qa_sessions": int(qa_count or 0),
    }
