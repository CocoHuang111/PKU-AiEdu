from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import normalize_username, verify_password
from ..models import AuthIdentity
from .base import AuthIdentityInfo


class LocalAuthProvider:
    name = "local"

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def authenticate(self, **credentials: Any) -> AuthIdentityInfo:
        username = normalize_username(str(credentials.get("username") or ""))
        password = str(credentials.get("password") or "")
        identity = await self.get_identity(username)
        row = await self.session.scalar(
            select(AuthIdentity).where(
                AuthIdentity.provider == "local",
                AuthIdentity.subject == username,
            )
        )
        if not row or not row.password_hash or not verify_password(password, row.password_hash):
            raise HTTPException(401, "工号或密码错误")
        return identity

    async def get_identity(self, subject: str) -> AuthIdentityInfo:
        username = normalize_username(subject)
        row = await self.session.scalar(
            select(AuthIdentity).where(
                AuthIdentity.provider == "local",
                AuthIdentity.subject == username,
            )
        )
        if not row:
            raise HTTPException(401, "工号或密码错误")
        return AuthIdentityInfo(
            provider="local",
            subject=username,
            username=row.username or username,
            display_name=row.username or username,
            provider_data={},
        )
