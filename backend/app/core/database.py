"""SQLAlchemy 2.x：异步给 FastAPI，同步给工作线程里的取消轮询。

异步引擎按请求创建并销毁，避免 TestClient / --reload 换 event loop 时
asyncpg 连接绑在旧 loop 上。
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from .app_settings import get_app_settings

_sync_engine = None
_sync_session_factory = None


def get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        settings = get_app_settings()
        _sync_engine = create_engine(
            settings.database_url_sync,
            pool_pre_ping=True,
            pool_size=3,
            max_overflow=5,
        )
    return _sync_engine


def sync_session_factory():
    global _sync_session_factory
    if _sync_session_factory is None:
        _sync_session_factory = sessionmaker(
            get_sync_engine(),
            expire_on_commit=False,
        )
    return _sync_session_factory


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(
        get_app_settings().database_url,
        poolclass=NullPool,
    )
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    session = factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
        await engine.dispose()


@contextmanager
def sync_session_scope() -> Session:
    session = sync_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def get_db() -> AsyncIterator[AsyncSession]:
    async with session_scope() as session:
        yield session


def reset_engines() -> None:
    global _sync_engine, _sync_session_factory
    if _sync_engine is not None:
        _sync_engine.dispose()
    _sync_engine = None
    _sync_session_factory = None
