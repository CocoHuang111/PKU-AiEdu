"""功能③ 教学智能问答。

流程：LLM 生成检索关键词 → 全库（或用户限定库）向量检索 → 阈值过滤 → LLM 生成带引用答案。
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from typing import Any

from ..config import settings
from ..pedagogy.loader import render_prompt
from ..providers import ChatMessage, ProviderError, get_llm
from ..rag import build_contexts, filter_hits, merge_contexts, search

JSON_BLOCK = re.compile(r"\{[\s\S]*\}")
MAX_HISTORY_TURNS = 6


def _parse_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    parsed: Any = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        if match := JSON_BLOCK.search(text):
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                pass

    if not isinstance(parsed, dict):
        raise ValueError("检索规划输出不是合法 JSON 对象")
    return parsed


def _resolve_corpora(forced_corpora: list[str] | None) -> list[str]:
    """None = 全库；传入列表（可为空）= 只查这些。"""
    valid = settings.corpus_names(include_auto=True)
    if forced_corpora is not None:
        return [c for c in forced_corpora if c in valid]
    return valid


def plan_retrieval(
    question: str,
    history: list[dict] | None = None,
    forced_corpora: list[str] | None = None,
    eval_selected: bool = False,
) -> dict[str, Any]:
    """LLM 生成检索 query；语料库范围由代码决定，不由 LLM 路由。"""
    rag = settings.section("rag")
    corpora = _resolve_corpora(forced_corpora)
    prompt = render_prompt(
        "qa_keywords.j2",
        question=question,
        history=(history or [])[-MAX_HISTORY_TURNS:],
        eval_selected=eval_selected,
    )

    fallback = {
        "standalone_question": question,
        "queries": [question],
        "corpora": corpora,
        "need_retrieval": True,
        "score_threshold": rag.get("score_threshold", 0.5),
        "max_hits": rag.get("max_hits", 12),
        "planner": "fallback",
    }

    try:
        raw = get_llm().chat(
            [
                ChatMessage("system", "你只输出合法 JSON，不输出任何解释文字。"),
                ChatMessage("user", prompt),
            ]
        )
        plan = _parse_json(raw)
    except (ValueError, ProviderError):
        return fallback

    queries = [q for q in plan.get("queries", []) if isinstance(q, str) and q.strip()]

    return {
        "standalone_question": plan.get("standalone_question") or question,
        "queries": queries or [question],
        "corpora": corpora,
        "need_retrieval": bool(plan.get("need_retrieval", True)),
        "score_threshold": rag.get("score_threshold", 0.5),
        "max_hits": rag.get("max_hits", 12),
        "planner": "llm",
    }


def retrieve(
    plan: dict[str, Any],
    user_id: str | None = None,
    eval_task_ids: list[str] | None = None,
    skip_eval_reports: bool = False,
) -> list[dict[str, Any]]:
    if not plan["need_retrieval"]:
        return []
    corpora = list(plan.get("corpora") or [])
    if skip_eval_reports or (
        "eval_reports" in corpora and eval_task_ids is not None and not eval_task_ids
    ):
        corpora = [c for c in corpora if c != "eval_reports"]
        if not skip_eval_reports:
            plan["corpora"] = corpora
    plan["eval_task_ids"] = eval_task_ids
    if not corpora:
        return []
    hits = search(
        queries=plan["queries"],
        corpora=corpora,
        rerank_query=plan["standalone_question"],
        user_id=user_id,
        eval_task_ids=None if skip_eval_reports else eval_task_ids,
    )
    hits = filter_hits(
        hits,
        score_threshold=plan.get("score_threshold"),
        max_hits=plan.get("max_hits"),
    )
    return build_contexts(hits)


def _assemble_contexts(
    plan: dict[str, Any],
    user_id: str | None,
    eval_task_ids: list[str] | None,
    pinned_contexts: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    pinned = [c for c in (pinned_contexts or []) if c.get("text")]
    if pinned:
        names = list(plan.get("corpora") or [])
        if "eval_reports" not in names:
            names.append("eval_reports")
        plan["corpora"] = names
        plan["pinned_eval_reports"] = len(pinned)
    plan["eval_task_ids"] = eval_task_ids
    retrieved = retrieve(
        plan,
        user_id=user_id,
        eval_task_ids=eval_task_ids,
        skip_eval_reports=bool(pinned),
    )
    return merge_contexts(pinned, retrieved)


def _build_messages(
    question: str, contexts: list[dict], history: list[dict] | None
) -> list[ChatMessage]:
    pinned = [c for c in contexts if c.get("pinned")]
    retrieved = [c for c in contexts if not c.get("pinned")]
    prompt = render_prompt(
        "qa_answer.j2",
        contexts=contexts,
        pinned_contexts=pinned,
        retrieved_contexts=retrieved,
        question=question,
        history=(history or [])[-MAX_HISTORY_TURNS:],
    )
    return [
        ChatMessage("system", "你是面向高校教师的教学支持助手「北大问教」。"),
        ChatMessage("user", prompt),
    ]


def _citations(contexts: list[dict]) -> list[dict]:
    return [
        {
            "index": i + 1,
            "corpus": c["corpus"],
            "corpus_label": c["corpus_label"],
            "source": c["source"],
            "source_url": c.get("source_url", ""),
            "score": c["score"],
            "snippet": c["text"][:200],
            "pinned": bool(c.get("pinned")),
        }
        for i, c in enumerate(contexts)
    ]


def ask(
    question: str,
    history: list[dict] | None = None,
    corpora: list[str] | None = None,
    user_id: str | None = None,
    eval_task_ids: list[str] | None = None,
    pinned_contexts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    plan = plan_retrieval(
        question,
        history,
        corpora,
        eval_selected=bool(pinned_contexts),
    )
    contexts = _assemble_contexts(plan, user_id, eval_task_ids, pinned_contexts)
    try:
        answer = get_llm().chat(
            _build_messages(plan["standalone_question"], contexts, history)
        )
    except ProviderError as e:
        answer = f"回答生成失败：{e}"

    return {
        "answer": answer,
        "citations": _citations(contexts),
        "plan": plan,
    }


def ask_stream(
    question: str,
    history: list[dict] | None = None,
    corpora: list[str] | None = None,
    user_id: str | None = None,
    eval_task_ids: list[str] | None = None,
    pinned_contexts: list[dict[str, Any]] | None = None,
) -> Iterator[dict[str, Any]]:
    """流式问答。先把检索规划和引用推给前端，再逐字推答案。"""
    plan = plan_retrieval(
        question,
        history,
        corpora,
        eval_selected=bool(pinned_contexts),
    )
    contexts = _assemble_contexts(plan, user_id, eval_task_ids, pinned_contexts)
    yield {"type": "plan", "data": plan}
    yield {"type": "citations", "data": _citations(contexts)}

    parts: list[str] = []
    try:
        for chunk in get_llm().stream_chat(
            _build_messages(plan["standalone_question"], contexts, history)
        ):
            parts.append(chunk)
            yield {"type": "chunk", "data": chunk}
    except ProviderError as e:
        message = f"\n\n（回答生成失败：{e}）"
        parts.append(message)
        yield {"type": "chunk", "data": message}

    yield {
        "type": "done",
        "answer": "".join(parts),
        "citations": _citations(contexts),
        "plan": plan,
    }
