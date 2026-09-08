"""创建或提升本地管理员。不要做成公开注册接口。

用法：
  python -m scripts.create_admin --username admin --display-name 管理员
  python -m scripts.create_admin --username admin --password '...' --display-name 管理员
"""

from __future__ import annotations

import argparse
import asyncio
import getpass

from sqlalchemy import select

from backend.app.core.database import session_scope
from backend.app.core.security import hash_password, validate_password, validate_username
from backend.app.models import AuthIdentity, User, UserProfile, UserSettings


async def main() -> None:
    parser = argparse.ArgumentParser(description="创建本地管理员账号")
    parser.add_argument("--username", required=True)
    parser.add_argument("--display-name", default="管理员")
    parser.add_argument("--password", default="")
    args = parser.parse_args()

    username = validate_username(args.username)
    password = args.password or getpass.getpass("管理员密码: ")
    password = validate_password(password)

    async with session_scope() as session:
        identity = await session.scalar(
            select(AuthIdentity).where(
                AuthIdentity.provider == "local",
                AuthIdentity.subject == username,
            )
        )
        if identity:
            user = await session.get(User, identity.user_id)
            if not user:
                raise SystemExit("身份存在但用户不存在")
            user.role = "admin"
            user.status = "active"
            identity.password_hash = hash_password(password)
            print(f"已将现有用户提升为管理员：{username} ({user.id})")
            return

        user = User(display_name=args.display_name, role="admin", status="active")
        session.add(user)
        await session.flush()
        session.add(
            AuthIdentity(
                user_id=user.id,
                provider="local",
                subject=username,
                username=username,
                password_hash=hash_password(password),
            )
        )
        session.add(UserProfile(user_id=user.id, name=args.display_name, staff_id=username))
        session.add(UserSettings(user_id=user.id, settings={}))
        print(f"已创建管理员：{username} ({user.id})")


if __name__ == "__main__":
    asyncio.run(main())
