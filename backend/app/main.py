from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_engine.config import settings

from .api import admin, auth, evaluation, qa, syllabus
from .core.app_settings import get_app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_settings = get_app_settings()
    print(
        "北大问教 2.0 后端启动 | "
        f"AI 模式: {settings.mode} | "
        f"认证: {app_settings.auth_mode} | "
        f"环境: {app_settings.app_env}"
    )
    yield


app = FastAPI(
    title="北大问教 2.0",
    description="面向高校教师的智能教学支持系统：视频质量评估 / 大纲优化 / 教学问答",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(evaluation.router)
app.include_router(syllabus.router)
app.include_router(qa.router)


@app.get("/api/health", tags=["系统"])
async def health() -> dict:
    from ai_engine.rag import collection_stats

    stats = await asyncio.to_thread(collection_stats)
    llm_conf = settings.provider_config("llm")
    app_settings = get_app_settings()
    return {
        "status": "ok",
        "mode": settings.mode,
        "auth_mode": app_settings.auth_mode,
        "llm_backend": llm_conf.get("provider", "openai_compat"),
        "llm_model": llm_conf.get("model"),
        "vlm_model": settings.provider_config("vlm").get("model"),
        "embedding_model": settings.provider_config("embedding").get("model"),
        "asr_backend": "faster_whisper",
        "asr_model": settings.flat_config("asr").get("model"),
        "corpora": stats,
    }
