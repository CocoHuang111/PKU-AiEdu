from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ai_engine.config import settings
from ai_engine.qa import ask, ask_stream
from ai_engine.rag import collection_stats

from ..core import db
from ..schemas import QAForm, SessionPatch

router = APIRouter(prefix="/api/qa", tags=["教学智能问答"])


@router.get("/corpora")
async def list_corpora() -> list[dict]:
    """语料库列表 + 各库当前文本块数量，前端用来渲染勾选框。"""
    stats = await asyncio.to_thread(collection_stats)
    return [
        {
            "name": c["name"],
            "label": c.get("label", c["name"]),
            "description": c.get("description", ""),
            "auto": c.get("auto", False),
            "count": stats.get(c["name"], 0),
        }
        for c in settings.corpora
    ]


async def _load_history(session_id: str | None) -> list[dict]:
    if not session_id:
        return []
    session = await db.get_session(session_id)
    return session["history"] if session else []


@router.post("/ask")
async def ask_once(form: QAForm) -> dict:
    history = await _load_history(form.session_id)
    result = await asyncio.to_thread(ask, form.question, history, form.corpora)

    history = history + [
        {"role": "user", "content": form.question},
        {
            "role": "assistant",
            "content": result["answer"],
            "citations": result["citations"],
        },
    ]
    session_id = await db.save_session(form.session_id, history)
    return {**result, "session_id": session_id}


@router.post("/ask/stream")
async def ask_streaming(form: QAForm) -> StreamingResponse:
    history = await _load_history(form.session_id)

    async def event_stream() -> AsyncIterator[str]:
        queue: asyncio.Queue = asyncio.Queue()
        loop = asyncio.get_running_loop()

        def produce() -> None:
            try:
                for event in ask_stream(form.question, history, form.corpora):
                    loop.call_soon_threadsafe(queue.put_nowait, event)
            except Exception as e:
                loop.call_soon_threadsafe(
                    queue.put_nowait, {"type": "error", "data": str(e)}
                )
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)

        # 生成器里有阻塞的 HTTP 调用，丢到线程里跑，通过队列把事件搬回事件循环
        task = asyncio.create_task(asyncio.to_thread(produce))

        final: dict | None = None
        try:
            while True:
                event = await queue.get()
                if event is None:
                    break
                if event["type"] == "done":
                    final = event
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        finally:
            await task

        if final:
            new_history = history + [
                {"role": "user", "content": form.question},
                {
                    "role": "assistant",
                    "content": final["answer"],
                    "citations": final["citations"],
                },
            ]
            session_id = await db.save_session(form.session_id, new_history)
            yield f"data: {json.dumps({'type': 'session', 'session_id': session_id}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/sessions")
async def list_sessions() -> list[dict]:
    return await db.list_sessions()


@router.get("/session/{session_id}")
async def get_session(session_id: str) -> dict:
    session = await db.get_session(session_id)
    if not session:
        raise HTTPException(404, "会话不存在")
    return session


@router.patch("/session/{session_id}")
async def patch_session(session_id: str, form: SessionPatch) -> dict:
    if form.title is None and form.pinned is None:
        raise HTTPException(400, "没有要修改的字段")
    title = form.title.strip() if form.title is not None else None
    if title is not None and not title:
        raise HTTPException(400, "名称不能为空")
    session = await db.update_session(session_id, title=title, pinned=form.pinned)
    if not session:
        raise HTTPException(404, "会话不存在")
    session.pop("history", None)
    return session


@router.delete("/session/{session_id}")
async def delete_session(session_id: str) -> dict:
    if not await db.delete_session(session_id):
        raise HTTPException(404, "会话不存在")
    return {"ok": True}
