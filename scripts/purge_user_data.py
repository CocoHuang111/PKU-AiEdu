"""清理指定用户的测试数据。默认 --dry-run，不会自动在切换认证模式时执行。"""

from __future__ import annotations

import argparse
import asyncio
import json
import uuid

from sqlalchemy import select

from backend.app.core.database import session_scope
from backend.app.models import (
    AuditLog,
    AuthIdentity,
    AuthSession,
    EvalTask,
    QASession,
    StoredFile,
    SyllabusRecord,
    SyllabusTask,
    User,
    UserProfile,
    UserSettings,
)


async def main() -> None:
    parser = argparse.ArgumentParser(description="清理指定用户数据")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--execute", action="store_true", default=False)
    args = parser.parse_args()
    dry_run = not args.execute
    user_id = uuid.UUID(args.user_id)

    async with session_scope() as session:
        user = await session.get(User, user_id)
        if not user:
            raise SystemExit("用户不存在")
        counts = {
            "eval_tasks": len((await session.scalars(select(EvalTask).where(EvalTask.user_id == user_id))).all()),
            "syllabus_tasks": len((await session.scalars(select(SyllabusTask).where(SyllabusTask.user_id == user_id))).all()),
            "syllabus_records": len((await session.scalars(select(SyllabusRecord).where(SyllabusRecord.user_id == user_id))).all()),
            "qa_sessions": len((await session.scalars(select(QASession).where(QASession.user_id == user_id))).all()),
            "stored_files": len((await session.scalars(select(StoredFile).where(StoredFile.user_id == user_id))).all()),
            "identities": len((await session.scalars(select(AuthIdentity).where(AuthIdentity.user_id == user_id))).all()),
            "sessions": len((await session.scalars(select(AuthSession).where(AuthSession.user_id == user_id))).all()),
        }
        report = {"user_id": str(user_id), "dry_run": dry_run, "counts": counts}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if dry_run:
            print("这是预览。确认后加 --execute")
            return
        for model in (
            EvalTask,
            SyllabusTask,
            SyllabusRecord,
            QASession,
            StoredFile,
            AuthSession,
            AuthIdentity,
            UserProfile,
            UserSettings,
        ):
            rows = (await session.scalars(select(model).where(getattr(model, "user_id") == user_id))).all()
            for row in rows:
                await session.delete(row)
        session.add(
            AuditLog(
                action="purge_user_data",
                resource_type="user",
                resource_id=str(user_id),
                details=counts,
            )
        )
        await session.delete(user)
        print("已删除")


if __name__ == "__main__":
    asyncio.run(main())
