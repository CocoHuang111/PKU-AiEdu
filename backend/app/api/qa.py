from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ai_engine.config import settings
from ai_engine.qa import ask, ask_stream, public_modes
from ai_engine.rag import collection_stats

from ..core import db
from ..core.audit import audit
from ..core.auth import current_user
from ..core.database import session_scope
from ..core.execution import run_qa
from ..schemas import QAForm, SessionPatch

router = APIRouter(prefix="/api/qa", tags=["教学智能问答"])

# 生成任务跟请求脱钩：客户端断开 SSE 后，线程里的 LLM 仍跑完并落库
_background_jobs: set[asyncio.Task] = set()


def _spawn(coro) -> asyncio.Task:
    task = asyncio.create_task(coro)
    _background_jobs.add(task)
    task.add_done_callback(_background_jobs.discard)
    return task


def _pending_history(history: list[dict], question: str, mode: str) -> list[dict]:
    return list(history) + [
        {"role": "user", "content": question, "mode": mode},
        {
            "role": "assistant",
            "content": "",
            "mode": mode,
            "pending": True,
            "citations": [],
            "plan": None,
        },
    ]


def _complete_history(
    history: list[dict],
    question: str,
    *,
    answer: str,
    citations: list | None = None,
    plan: dict | None = None,
    mode: str = "ask",
) -> list[dict]:
    assistant: dict = {
        "role": "assistant",
        "content": answer,
        "mode": mode,
        "citations": citations or [],
    }
    if plan is not None:
        assistant["plan"] = plan
    return list(history) + [
        {"role": "user", "content": question, "mode": mode},
        assistant,
    ]


@router.get("/modes")
async def list_modes(user: dict = Depends(current_user)) -> list[dict]:
    """返回前端可选工作模式；提示词内部指令不对外暴露。"""
    valid_corpora = set(settings.corpus_names(include_auto=False))
    result = public_modes()
    for mode in result:
        mode["default_corpora"] = [
            name for name in mode["default_corpora"] if name in valid_corpora
        ]
    return result


@router.get("/corpora")
async def list_corpora(user: dict = Depends(current_user)) -> list[dict]:
    """语料库列表 + 各库当前文本块数量，前端用来渲染勾选框。

    eval_reports 的 count 改成当前用户已完成评估份数，而不是 Chroma 全库块数。
    """
    stats = await asyncio.to_thread(collection_stats)
    reports = await db.list_tasks(
        user_id=user["id"], status="completed", limit=200
    )
    return [
        {
            "name": c["name"],
            "label": c.get("label", c["name"]),
            "description": c.get("description", ""),
            "auto": c.get("auto", False),
            "count": (
                len(reports) if c["name"] == "eval_reports" else stats.get(c["name"], 0)
            ),
        }
        for c in settings.corpora
    ]


async def _owned_eval_task_ids(
    user_id: str, requested: list[str] | None
) -> list[str] | None:
    if requested is None:
        return None
    tasks = await db.list_tasks(user_id=user_id, status="completed", limit=200)
    allowed = {t["id"] for t in tasks}
    return [tid for tid in requested if tid in allowed]


def _format_eval_context(task: dict) -> dict | None:
    result = task.get("result") or {}
    report = (result.get("report") or "").strip()
    overall = result.get("overall") if isinstance(result.get("overall"), dict) else {}
    if not report and overall.get("score") is None:
        return None
    dims = "、".join(
        f"{d.get('label')}{d.get('score')}分"
        for d in (result.get("dimensions") or [])
        if isinstance(d, dict) and d.get("assessed")
    )
    name = task.get("filename") or result.get("video_file") or "未命名"
    grade = overall.get("grade")
    grade_label = overall.get("grade_label")
    grade_text = f"，等级 {grade}（{grade_label}）" if grade else ""
    dim_text = f"五维得分：{dims}。\n" if dims else ""
    text = (
        f"教学视频评估报告（{name}）\n"
        f"综合得分 {overall.get('score', '—')}/100{grade_text}。\n"
        f"{dim_text}\n"
        f"{report}"
    )
    meta = settings.corpus_meta("eval_reports")
    return {
        "text": text.strip(),
        "corpus": "eval_reports",
        "corpus_label": meta.get("label", "历史评估报告"),
        "source": f"评估报告-{name}",
        "score": 1.0,
        "pinned": True,
    }


async def _pinned_eval_contexts(
    user_id: str, eval_task_ids: list[str] | None
) -> list[dict]:
    if not eval_task_ids:
        return []
    items = []
    for tid in eval_task_ids:
        task = await db.get_task(tid, user_id=user_id)
        if not task or task.get("status") != "completed":
            continue
        ctx = _format_eval_context(task)
        if ctx:
            items.append(ctx)
    return items


def _strip_pending_turn(history: list[dict] | None) -> list[dict]:
    items = list(history or [])
    if items and items[-1].get("role") == "assistant" and items[-1].get("pending"):
        items.pop()
        if items and items[-1].get("role") == "user":
            items.pop()
    return items


async def _load_history(session_id: str | None, user_id: str) -> list[dict]:
    if not session_id:
        return []
    session = await db.get_session(session_id, user_id=user_id)
    if not session:
        raise HTTPException(404, "会话不存在")
    return _strip_pending_turn(session.get("history") or [])


@router.post("/ask")
async def ask_once(form: QAForm, user: dict = Depends(current_user)) -> dict:
    history = await _load_history(form.session_id, user["id"])
    eval_task_ids = await _owned_eval_task_ids(user["id"], form.eval_task_ids)
    pinned = await _pinned_eval_contexts(user["id"], eval_task_ids)
    result = await run_qa(
        ask,
        form.question,
        history,
        form.corpora,
        user["id"],
        eval_task_ids,
        pinned,
        form.mode,
    )

    history = history + [
        {"role": "user", "content": form.question, "mode": form.mode},
        {
            "role": "assistant",
            "content": result["answer"],
            "mode": form.mode,
            "citations": result["citations"],
            "plan": result.get("plan"),
        },
    ]
    session_id = await db.save_session(
        form.session_id, history, user_id=user["id"]
    )
    return {**result, "session_id": session_id}


@router.post("/ask/stream")
async def ask_streaming(
    form: QAForm, user: dict = Depends(current_user)
) -> StreamingResponse:
    history = await _load_history(form.session_id, user["id"])
    pending = _pending_history(history, form.question, form.mode)
    session_id = await db.save_session(
        form.session_id, pending, user_id=user["id"]
    )
    eval_task_ids = await _owned_eval_task_ids(user["id"], form.eval_task_ids)
    pinned = await _pinned_eval_contexts(user["id"], eval_task_ids)

    queue: asyncio.Queue = asyncio.Queue()
    loop = asyncio.get_running_loop()
    result: dict = {"final": None, "error": None}

    def produce() -> None:
        try:
            for event in ask_stream(
                form.question,
                history,
                form.corpora,
                user["id"],
                eval_task_ids,
                pinned,
                form.mode,
            ):
                if event["type"] == "done":
                    result["final"] = event
                elif event["type"] == "error":
                    result["error"] = event.get("data") or "生成失败"
                loop.call_soon_threadsafe(queue.put_nowait, event)
        except Exception as e:
            result["error"] = str(e)
            loop.call_soon_threadsafe(
                queue.put_nowait, {"type": "error", "data": str(e)}
            )

    async def persist_job() -> None:
        try:
            await run_qa(produce)
            final = result["final"]
            if final:
                new_history = _complete_history(
                    history,
                    form.question,
                    answer=final.get("answer") or "",
                    citations=final.get("citations"),
                    plan=final.get("plan"),
                    mode=form.mode,
                )
            else:
                err = result["error"] or "生成失败"
                new_history = _complete_history(
                    history,
                    form.question,
                    answer=f"（请求失败：{err}）",
                    mode=form.mode,
                )
            await db.save_session(session_id, new_history, user_id=user["id"])
        finally:
            await queue.put(None)

    _spawn(persist_job())

    async def event_stream() -> AsyncIterator[str]:
        yield f"data: {json.dumps({'type': 'session', 'session_id': session_id}, ensure_ascii=False)}\n\n"
        try:
            while True:
                event = await queue.get()
                if event is None:
                    break
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
        except asyncio.CancelledError:
            return

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/sessions")
async def list_sessions(user: dict = Depends(current_user)) -> list[dict]:
    return await db.list_sessions(user_id=user["id"])


@router.get("/session/{session_id}")
async def get_session(
    session_id: str, user: dict = Depends(current_user)
) -> dict:
    session = await db.get_session(session_id, user_id=user["id"])
    if not session:
        raise HTTPException(404, "会话不存在")
    return session


@router.patch("/session/{session_id}")
async def patch_session(
    session_id: str, form: SessionPatch, user: dict = Depends(current_user)
) -> dict:
    if form.title is None and form.pinned is None:
        raise HTTPException(400, "没有要修改的字段")
    title = form.title.strip() if form.title is not None else None
    if title is not None and not title:
        raise HTTPException(400, "名称不能为空")
    session = await db.update_session(
        session_id, title=title, pinned=form.pinned, user_id=user["id"]
    )
    if not session:
        raise HTTPException(404, "会话不存在")
    session.pop("history", None)
    return session


@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str, user: dict = Depends(current_user)
) -> dict:
    if not await db.delete_session(session_id, user_id=user["id"]):
        raise HTTPException(404, "会话不存在")
    async with session_scope() as session:
        await audit(
            session,
            None,
            action="delete",
            actor_user_id=user["_id"],
            resource_type="qa_session",
            resource_id=session_id,
        )
    return {"ok": True}
