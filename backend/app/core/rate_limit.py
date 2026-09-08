from __future__ import annotations

import time
from collections import defaultdict

from fastapi import HTTPException

from .app_settings import get_app_settings

_failures: dict[str, list[float]] = defaultdict(list)


def check_login_rate(key: str) -> None:
    settings = get_app_settings()
    now = time.time()
    window = settings.login_rate_window_sec
    hits = [ts for ts in _failures[key] if now - ts < window]
    _failures[key] = hits
    if len(hits) >= settings.login_rate_limit:
        raise HTTPException(429, "登录尝试过于频繁，请稍后再试")


def record_login_failure(key: str) -> None:
    _failures[key].append(time.time())


def clear_login_failures(key: str) -> None:
    _failures.pop(key, None)
