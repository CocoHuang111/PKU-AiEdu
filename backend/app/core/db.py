"""SQLite 存储层。三张表：评估任务、问答会话、大纲记录。

JSON 字段统一以 TEXT 存储，读出时反序列化，避免为演进中的结构频繁改表。
"""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any

import aiosqlite

from ai_engine.config import settings

DB_PATH: Path = settings.root / "data" / "app.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS eval_tasks (
    id            TEXT PRIMARY KEY,
    filename      TEXT,
    video_path    TEXT,
    reference     TEXT,                -- 解析后的课程大纲文本（选填）
    syllabus_path TEXT,                -- 教师上传的课程大纲文件
    courseware_path TEXT,              -- 教师上传的课件文件
    transcript    TEXT,                -- 教师上传的讲稿文本（对应转写）
    transcript_path TEXT,              -- 教师上传的讲稿文件
    status        TEXT NOT NULL,       -- queued | processing | completed | failed | cancelled
    progress      INTEGER DEFAULT 0,
    current_step  TEXT,
    step_detail   TEXT,
    result        TEXT,                -- JSON
    error         TEXT,
    created_at    REAL NOT NULL,
    updated_at    REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS qa_sessions (
    id          TEXT PRIMARY KEY,
    title       TEXT,
    history     TEXT NOT NULL,         -- JSON: [{role, content, citations?}]
    created_at  REAL NOT NULL,
    updated_at  REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS syllabus_records (
    id            TEXT PRIMARY KEY,
    filename      TEXT,
    course_name   TEXT,
    original_text TEXT,
    xml           TEXT,
    valid         INTEGER DEFAULT 0,
    created_at    REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_eval_created ON eval_tasks(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_qa_updated   ON qa_sessions(updated_at DESC);

CREATE TABLE IF NOT EXISTS syllabus_tasks (
    id            TEXT PRIMARY KEY,
    filename      TEXT,
    source_path   TEXT,
    source_text   TEXT,
    prompt_mode   TEXT,
    status        TEXT NOT NULL,
    progress      INTEGER DEFAULT 0,
    current_step  TEXT,
    step_detail   TEXT,
    result        TEXT,
    record_id     TEXT,
    error         TEXT,
    created_at    REAL NOT NULL,
    updated_at    REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_syllabus_task_created ON syllabus_tasks(created_at DESC);
"""


def new_id() -> str:
    return uuid.uuid4().hex


# CREATE TABLE IF NOT EXISTS 不会给已存在的表补列，所以新增列要单独走这里
MIGRATIONS = [
    ("eval_tasks", "reference", "TEXT"),
    ("eval_tasks", "syllabus_path", "TEXT"),
    ("eval_tasks", "courseware_path", "TEXT"),
    ("eval_tasks", "transcript", "TEXT"),
    ("eval_tasks", "transcript_path", "TEXT"),
    ("qa_sessions", "pinned", "INTEGER NOT NULL DEFAULT 0"),
]


async def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        for table, column, coltype in MIGRATIONS:
            cur = await db.execute(f"PRAGMA table_info({table})")
            existing = {row[1] for row in await cur.fetchall()}
            if column not in existing:
                await db.execute(
                    f"ALTER TABLE {table} ADD COLUMN {column} {coltype}"
                )
        await db.commit()


def _loads(value: Any, default: Any = None) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default


def _row_get(row: aiosqlite.Row, key: str, default: Any = None) -> Any:
    try:
        value = row[key]
    except (KeyError, IndexError):
        return default
    return default if value is None else value


# ---------------------------------------------------------------- 评估任务


async def create_task(
    filename: str,
    video_path: str | None = None,
    reference: str | None = None,
    syllabus_path: str | None = None,
    courseware_path: str | None = None,
    transcript: str | None = None,
    transcript_path: str | None = None,
) -> str:
    task_id = new_id()
    now = time.time()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO eval_tasks (id, filename, video_path, reference, "
            "syllabus_path, courseware_path, transcript, transcript_path, status, "
            "progress, current_step, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                task_id,
                filename,
                video_path or "",
                reference,
                syllabus_path,
                courseware_path,
                transcript,
                transcript_path,
                "queued",
                0,
                "queued",
                now,
                now,
            ),
        )
        await db.commit()
    return task_id


async def update_task(task_id: str, **fields) -> None:
    if not fields:
        return
    if "result" in fields and not isinstance(fields["result"], (str, type(None))):
        fields["result"] = json.dumps(fields["result"], ensure_ascii=False)
    if "step_detail" in fields and not isinstance(
        fields["step_detail"], (str, type(None))
    ):
        fields["step_detail"] = json.dumps(fields["step_detail"], ensure_ascii=False)
    fields["updated_at"] = time.time()
    cols = ", ".join(f"{k} = ?" for k in fields)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"UPDATE eval_tasks SET {cols} WHERE id = ?", (*fields.values(), task_id)
        )
        await db.commit()


def _task_row(row: aiosqlite.Row, with_result: bool = True) -> dict[str, Any]:
    task = {
        "id": row["id"],
        "filename": row["filename"],
        "status": row["status"],
        "progress": row["progress"],
        "current_step": row["current_step"],
        "step_detail": _loads(row["step_detail"], {}),
        "error": row["error"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "has_syllabus": bool(row["reference"] or _row_get(row, "syllabus_path")),
        "has_courseware": bool(_row_get(row, "courseware_path")),
        "has_script": bool(_row_get(row, "transcript") or _row_get(row, "transcript_path")),
    }
    if with_result:
        task["result"] = _loads(row["result"])
        task["reference"] = row["reference"]
    else:
        # 列表页只带摘要，避免把完整报告塞进列表响应
        result = _loads(row["result"]) or {}
        overall = result.get("overall") if isinstance(result, dict) else None
        task["summary"] = overall
    return task


async def get_task(task_id: str) -> dict[str, Any] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM eval_tasks WHERE id = ?", (task_id,))
        row = await cur.fetchone()
    return _task_row(row) if row else None


async def list_tasks(limit: int = 50) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM eval_tasks ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cur.fetchall()
    return [_task_row(r, with_result=False) for r in rows]


async def delete_task(task_id: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("DELETE FROM eval_tasks WHERE id = ?", (task_id,))
        await db.commit()
        return cur.rowcount > 0


def is_task_cancelled(task_id: str) -> bool:
    """同步读取取消状态，供评估工作线程在 progress 回调里轮询。"""
    with sqlite3.connect(DB_PATH) as db:
        cur = db.execute("SELECT status FROM eval_tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
    return row is not None and row[0] == "cancelled"


async def request_cancel(task_id: str) -> dict[str, Any]:
    task = await get_task(task_id)
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


# ---------------------------------------------------------------- 大纲优化任务


async def create_syllabus_task(
    *,
    filename: str,
    prompt_mode: str | None,
    source_path: str | None = None,
    source_text: str | None = None,
) -> str:
    task_id = new_id()
    now = time.time()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO syllabus_tasks (id, filename, source_path, source_text, "
            "prompt_mode, status, progress, current_step, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                task_id,
                filename,
                source_path,
                source_text,
                prompt_mode,
                "queued",
                0,
                "queued",
                now,
                now,
            ),
        )
        await db.commit()
    return task_id


async def update_syllabus_task(task_id: str, **fields) -> None:
    if not fields:
        return
    if "result" in fields and not isinstance(fields["result"], (str, type(None))):
        fields["result"] = json.dumps(fields["result"], ensure_ascii=False)
    if "step_detail" in fields and not isinstance(
        fields["step_detail"], (str, type(None))
    ):
        fields["step_detail"] = json.dumps(fields["step_detail"], ensure_ascii=False)
    fields["updated_at"] = time.time()
    cols = ", ".join(f"{k} = ?" for k in fields)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"UPDATE syllabus_tasks SET {cols} WHERE id = ?", (*fields.values(), task_id)
        )
        await db.commit()


def _syllabus_task_row(
    row: aiosqlite.Row,
    *,
    with_result: bool = True,
    include_source: bool = False,
) -> dict[str, Any]:
    task = {
        "id": row["id"],
        "filename": row["filename"],
        "prompt_mode": row["prompt_mode"],
        "status": row["status"],
        "progress": row["progress"],
        "current_step": row["current_step"],
        "step_detail": _loads(row["step_detail"], {}),
        "record_id": row["record_id"],
        "error": row["error"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
    if include_source:
        task["source_path"] = row["source_path"]
        task["source_text"] = row["source_text"]
    if with_result:
        task["result"] = _loads(row["result"])
    else:
        result = _loads(row["result"]) or {}
        task["summary"] = {
            "course_name": result.get("course_name") if isinstance(result, dict) else None,
            "valid": result.get("valid") if isinstance(result, dict) else None,
        }
    return task


async def get_syllabus_task(
    task_id: str, *, include_source: bool = False
) -> dict[str, Any] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM syllabus_tasks WHERE id = ?", (task_id,))
        row = await cur.fetchone()
    return (
        _syllabus_task_row(row, include_source=include_source) if row else None
    )


async def list_syllabus_tasks(limit: int = 20) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM syllabus_tasks ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cur.fetchall()
    return [_syllabus_task_row(r, with_result=False) for r in rows]


def is_syllabus_task_cancelled(task_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as db:
        cur = db.execute("SELECT status FROM syllabus_tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
    return row is not None and row[0] == "cancelled"


async def request_cancel_syllabus_task(task_id: str) -> dict[str, Any]:
    task = await get_syllabus_task(task_id)
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


# ---------------------------------------------------------------- 问答会话


async def save_session(
    session_id: str | None, history: list[dict], title: str | None = None
) -> str:
    now = time.time()
    payload = json.dumps(history, ensure_ascii=False)
    async with aiosqlite.connect(DB_PATH) as db:
        if session_id:
            cur = await db.execute(
                "SELECT id FROM qa_sessions WHERE id = ?", (session_id,)
            )
            if await cur.fetchone():
                await db.execute(
                    "UPDATE qa_sessions SET history = ?, updated_at = ? WHERE id = ?",
                    (payload, now, session_id),
                )
                await db.commit()
                return session_id
        session_id = session_id or new_id()
        first = next((h["content"] for h in history if h["role"] == "user"), "新会话")
        await db.execute(
            "INSERT INTO qa_sessions (id, title, history, created_at, updated_at) "
            "VALUES (?,?,?,?,?)",
            (session_id, title or first[:40], payload, now, now),
        )
        await db.commit()
    return session_id


async def get_session(session_id: str) -> dict[str, Any] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM qa_sessions WHERE id = ?", (session_id,))
        row = await cur.fetchone()
    if not row:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "history": _loads(row["history"], []),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "pinned": bool(_row_get(row, "pinned", 0)),
    }


async def list_sessions(limit: int = 50) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, title, created_at, updated_at, pinned FROM qa_sessions "
            "ORDER BY pinned DESC, updated_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "pinned": bool(_row_get(r, "pinned", 0)),
        }
        for r in rows
    ]


async def update_session(
    session_id: str, *, title: str | None = None, pinned: bool | None = None
) -> dict[str, Any] | None:
    session = await get_session(session_id)
    if not session:
        return None
    fields: list[str] = []
    values: list[Any] = []
    if title is not None:
        fields.append("title = ?")
        values.append(title)
    if pinned is not None:
        fields.append("pinned = ?")
        values.append(1 if pinned else 0)
    if not fields:
        return session
    values.append(session_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"UPDATE qa_sessions SET {', '.join(fields)} WHERE id = ?",
            values,
        )
        await db.commit()
    return await get_session(session_id)


async def delete_session(session_id: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("DELETE FROM qa_sessions WHERE id = ?", (session_id,))
        await db.commit()
        return cur.rowcount > 0


# ---------------------------------------------------------------- 大纲记录


async def save_syllabus(
    filename: str, course_name: str, original_text: str, xml: str, valid: bool
) -> str:
    record_id = new_id()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO syllabus_records (id, filename, course_name, original_text, "
            "xml, valid, created_at) VALUES (?,?,?,?,?,?,?)",
            (
                record_id,
                filename,
                course_name,
                original_text,
                xml,
                int(valid),
                time.time(),
            ),
        )
        await db.commit()
    return record_id


async def list_syllabi(limit: int = 50) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT id, filename, course_name, valid, created_at FROM syllabus_records "
            "ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()
    return [dict(r) for r in rows]


async def get_syllabus(record_id: str) -> dict[str, Any] | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM syllabus_records WHERE id = ?", (record_id,)
        )
        row = await cur.fetchone()
    return dict(row) if row else None
