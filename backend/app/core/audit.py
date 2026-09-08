"""最小审计写入。details 只放脱敏字段，不写密码和令牌。"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import AuditLog


def client_ip(request: Request | None) -> str | None:
    if request is None:
        return None
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()[:64]
    if request.client:
        return request.client.host
    return None


def client_ua(request: Request | None) -> str | None:
    if request is None:
        return None
    return (request.headers.get("user-agent") or "")[:512] or None


def _as_uuid(value: str | uuid.UUID | None) -> uuid.UUID | None:
    if value is None:
        return None
    if isinstance(value, uuid.UUID):
        return value
    return uuid.UUID(str(value))


async def write_audit(
    session: AsyncSession,
    *,
    action: str,
    actor_user_id: str | uuid.UUID | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    target_user_id: str | uuid.UUID | None = None,
    ip_address: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    session.add(
        AuditLog(
            actor_user_id=_as_uuid(actor_user_id),
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id is not None else None,
            target_user_id=_as_uuid(target_user_id),
            ip_address=ip_address,
            details=details,
        )
    )


async def audit(
    session: AsyncSession,
    request: Request | None,
    *,
    action: str,
    actor_user_id: str | uuid.UUID | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    target_user_id: str | uuid.UUID | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    await write_audit(
        session,
        action=action,
        actor_user_id=actor_user_id,
        resource_type=resource_type,
        resource_id=resource_id,
        target_user_id=target_user_id,
        ip_address=client_ip(request),
        details=details,
    )
