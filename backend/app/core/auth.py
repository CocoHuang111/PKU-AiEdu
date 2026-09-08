"""鉴权依赖。业务接口用 get_current_user / require_admin，不信任前端角色。"""

from __future__ import annotations

from ..auth.sessions import get_current_user, public_user, require_admin

# 旧代码里的名字，三个业务 API 仍在用
current_user = get_current_user

__all__ = [
    "current_user",
    "get_current_user",
    "public_user",
    "require_admin",
]
