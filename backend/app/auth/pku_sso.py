"""北京大学统一身份认证适配层。

在拿到官方协议文档、Client ID、密钥和测试环境之前，不猜测 OIDC / OAuth / CAS / SAML，
也不编写不可验证的伪生产认证代码。真实接入应只改这个模块。
"""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from fastapi import HTTPException

from ..core.app_settings import get_app_settings
from .base import AuthIdentityInfo


class PKUSSONotConfigured(RuntimeError):
    pass


class PKUSSOAuthProvider:
    name = "pku_sso"

    def __init__(self, *, allow_mock: bool = False) -> None:
        self.allow_mock = allow_mock
        self.settings = get_app_settings()

    def start_url(self, state: str) -> str:
        if not self.settings.pku_sso_configured:
            raise PKUSSONotConfigured("北大统一身份认证尚未配置官方地址和密钥")
        # 具体 query 参数以官方文档为准；这里只预留授权入口。
        query = urlencode(
            {
                "client_id": self.settings.pku_sso_client_id,
                "redirect_uri": self.settings.pku_sso_redirect_uri,
                "state": state,
                "response_type": "code",
            }
        )
        return f"{self.settings.pku_sso_authorize_url}?{query}"

    async def authenticate(self, **credentials: Any) -> AuthIdentityInfo:
        if credentials.get("mock") and (self.allow_mock or not self.settings.is_production):
            subject = str(credentials.get("subject") or "").strip()
            if not subject:
                raise HTTPException(400, "mock SSO 缺少 subject")
            return await self.get_identity(subject)
        raise HTTPException(
            503,
            "北大统一身份认证尚未接入官方文档，当前不能完成真实登录",
        )

    async def get_identity(self, subject: str) -> AuthIdentityInfo:
        subject = (subject or "").strip()
        if not subject:
            raise HTTPException(400, "缺少北大统一身份标识")
        return AuthIdentityInfo(
            provider="pku_sso",
            subject=subject,
            username=None,
            display_name="",
            provider_data={"source": "pku_sso"},
        )

    async def exchange_callback(self, **payload: Any) -> AuthIdentityInfo:
        """官方回调验证入口。未拿到文档前拒绝真实回调。"""
        if payload.get("mock"):
            return await self.authenticate(**payload)
        raise HTTPException(
            503,
            "北大统一身份认证回调尚未实现。请先补齐官方协议文档后再接入。",
        )
