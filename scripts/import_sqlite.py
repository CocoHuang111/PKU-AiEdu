"""可选：把旧 SQLite 业务记录挂到指定 PostgreSQL 用户下。不改、不删 data/app.db。"""

from __future__ import annotations

import argparse
import asyncio
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from backend.app.core.database import session_scope
from backend.app.models import EvalTask, QASession, SyllabusRecord, SyllabusTask


def _uid(raw: str | None) -> uuid.UUID | None:
    if not raw:
        return None
    try:
        return uuid.UUID(str(raw))
    except ValueError:
        return uuid.uuid4()


def _ts(raw) -> datetime:
    if raw is None:
        return datetime.now(timezone.utc)
    try:
        return datetime.fromtimestamp(float(raw), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return datetime.now(timezone.utc)


def _json(raw, default):
    if raw is None or raw == "":
        return default
    if isinstance(raw, (dict, list)):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return default


def _row_get(row: sqlite3.Row, key: str, default=None):
    return row[key] if key in row.keys() else default


async def main() -> None:
    parser = argparse.ArgumentParser(description="从旧 SQLite 导入业务记录")
    parser.add_argument("--db", default="data/app.db")
    parser.add_argument("--user-id", required=True, help="导入后的归属用户 UUID")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    dry_run = not args.execute
    user_id = uuid.UUID(args.user_id)
    path = Path(args.db)
    if not path.is_file():
        raise SystemExit(f"找不到 {path}；本工具不会创建或修改它")

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    counts = {
        table: conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in ("eval_tasks", "qa_sessions", "syllabus_records", "syllabus_tasks")
    }
    print(
        json.dumps(
            {"db": str(path), "user_id": str(user_id), "dry_run": dry_run, "counts": counts},
            ensure_ascii=False,
            indent=2,
        )
    )
    if dry_run:
        print("这是预览。确认归属用户后加 --execute")
        return

    imported = {key: 0 for key in counts}
    async with session_scope() as session:
        for row in conn.execute("SELECT * FROM eval_tasks"):
            task_id = _uid(row["id"])
            if await session.get(EvalTask, task_id):
                continue
            session.add(
                EvalTask(
                    id=task_id,
                    user_id=user_id,
                    filename=row["filename"],
                    video_path=row["video_path"],
                    reference=_row_get(row, "reference"),
                    syllabus_path=_row_get(row, "syllabus_path"),
                    courseware_path=_row_get(row, "courseware_path"),
                    transcript=_row_get(row, "transcript"),
                    transcript_path=_row_get(row, "transcript_path"),
                    status=row["status"] or "queued",
                    progress=int(row["progress"] or 0),
                    current_step=row["current_step"],
                    step_detail=_json(_row_get(row, "step_detail"), {}),
                    result=_json(row["result"], None),
                    error=row["error"],
                    created_at=_ts(row["created_at"]),
                    updated_at=_ts(row["updated_at"]),
                )
            )
            imported["eval_tasks"] += 1

        for row in conn.execute("SELECT * FROM qa_sessions"):
            session_id = _uid(row["id"])
            if await session.get(QASession, session_id):
                continue
            session.add(
                QASession(
                    id=session_id,
                    user_id=user_id,
                    title=row["title"],
                    history=_json(row["history"], []),
                    pinned=bool(_row_get(row, "pinned", 0)),
                    created_at=_ts(row["created_at"]),
                    updated_at=_ts(row["updated_at"]),
                )
            )
            imported["qa_sessions"] += 1

        record_ids: dict[str, uuid.UUID] = {}
        for row in conn.execute("SELECT * FROM syllabus_records"):
            record_id = _uid(row["id"])
            record_ids[row["id"]] = record_id
            if await session.get(SyllabusRecord, record_id):
                continue
            session.add(
                SyllabusRecord(
                    id=record_id,
                    user_id=user_id,
                    filename=row["filename"],
                    course_name=row["course_name"],
                    original_text=row["original_text"],
                    xml=row["xml"],
                    valid=bool(row["valid"]),
                    created_at=_ts(row["created_at"]),
                )
            )
            imported["syllabus_records"] += 1

        for row in conn.execute("SELECT * FROM syllabus_tasks"):
            task_id = _uid(row["id"])
            if await session.get(SyllabusTask, task_id):
                continue
            raw_record = _row_get(row, "record_id")
            session.add(
                SyllabusTask(
                    id=task_id,
                    user_id=user_id,
                    filename=row["filename"],
                    source_path=_row_get(row, "source_path"),
                    source_text=_row_get(row, "source_text"),
                    prompt_mode=_row_get(row, "prompt_mode"),
                    status=row["status"] or "queued",
                    progress=int(row["progress"] or 0),
                    current_step=row["current_step"],
                    step_detail=_json(_row_get(row, "step_detail"), {}),
                    result=_json(_row_get(row, "result"), None),
                    record_id=record_ids.get(raw_record) if raw_record else None,
                    error=row["error"],
                    created_at=_ts(row["created_at"]),
                    updated_at=_ts(row["updated_at"]),
                )
            )
            imported["syllabus_tasks"] += 1

    print(json.dumps({"imported": imported}, ensure_ascii=False, indent=2))
    print("导入完成。原 SQLite 文件未修改。")


if __name__ == "__main__":
    asyncio.run(main())
