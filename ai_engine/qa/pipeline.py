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
from .case_loader import hit_belongs_to_cases, hydrate_matched_cases
from .modes import QAMode, get_mode

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


def _resolve_corpora(
    forced_corpora: list[str] | None, mode: QAMode | None = None
) -> list[str]:
    """None = 模式默认库；传入列表（可为空）= 用户显式限定。"""
    valid = settings.corpus_names(include_auto=True)
    if forced_corpora is not None:
        return [c for c in forced_corpora if c in valid]
    if mode is not None:
        return [c for c in mode.default_corpora if c in valid]
    return valid


def plan_retrieval(
    question: str,
    history: list[dict] | None = None,
    forced_corpora: list[str] | None = None,
    eval_selected: bool = False,
    mode: str = "ask",
) -> dict[str, Any]:
    """LLM 生成检索 query；语料库范围由代码决定，不由 LLM 路由。"""
    rag = settings.section("rag")
    mode_config = get_mode(mode)
    corpora = _resolve_corpora(forced_corpora, mode_config)
    max_hits = rag.get("max_hits", 12)
    if mode_config.retrieval_strategy in {"course_match", "case_match"}:
        max_hits = max(max_hits, 30)
    prompt = render_prompt(
        "qa_keywords.j2",
        question=question,
        history=(history or [])[-MAX_HISTORY_TURNS:],
        eval_selected=eval_selected,
        mode=mode_config,
    )

    fallback = {
        "standalone_question": question,
        "queries": [question],
        "corpora": corpora,
        "need_retrieval": True,
        "score_threshold": rag.get("score_threshold", 0.5),
        "max_hits": max_hits,
        "planner": "fallback",
        "mode": mode_config.name,
        "mode_label": mode_config.label,
        "retrieval_strategy": mode_config.retrieval_strategy,
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
        "max_hits": max_hits,
        "planner": "llm",
        "mode": mode_config.name,
        "mode_label": mode_config.label,
        "retrieval_strategy": mode_config.retrieval_strategy,
    }


def retrieve(
    plan: dict[str, Any],
    user_id: str | None = None,
    eval_task_ids: list[str] | None = None,
    skip_eval_reports: bool = False,
) -> list[dict[str, Any]]:
    return build_contexts(
        _retrieve_hits(plan, user_id, eval_task_ids, skip_eval_reports)
    )


def _retrieve_hits(
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
    return hits


def _assemble_contexts(
    plan: dict[str, Any],
    user_id: str | None,
    eval_task_ids: list[str] | None,
    pinned_contexts: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    pinned = [c for c in (pinned_contexts or []) if c.get("text")]
    eval_pinned = [c for c in pinned if c.get("context_type") == "eval_report"]
    attachment_pinned = [c for c in pinned if c.get("context_type") == "attachment"]
    if eval_pinned:
        names = list(plan.get("corpora") or [])
        if "eval_reports" not in names:
            names.append("eval_reports")
        plan["corpora"] = names
        plan["pinned_eval_reports"] = len(eval_pinned)
    if attachment_pinned:
        plan["pinned_attachments"] = len(attachment_pinned)
        plan["attachment_names"] = [c.get("source") for c in attachment_pinned]
    plan["eval_task_ids"] = eval_task_ids
    hits = _retrieve_hits(
        plan,
        user_id=user_id,
        eval_task_ids=eval_task_ids,
        skip_eval_reports=bool(eval_pinned),
    )
    strategy = str(plan.get("retrieval_strategy") or "chunk")
    case_contexts, matched_cases, consumed = hydrate_matched_cases(hits, strategy)
    if matched_cases:
        plan["matched_cases"] = matched_cases
    remaining_hits = [
        hit for hit in hits if not hit_belongs_to_cases(hit, consumed)
    ]
    supplementary = build_contexts(remaining_hits)
    retrieved = case_contexts + supplementary
    # 专用模式的完整文档需要比通用切片 RAG 更大的上下文额度。
    context_cap = 52000 if case_contexts else None
    return merge_contexts(pinned, retrieved, max_chars=context_cap)


def _image_blocks(contexts: list[dict]) -> list[dict]:
    """把已内联的图片接到 user 消息末尾。图片不进入提示词正文。"""
    blocks: list[dict] = []
    for context in contexts:
        if context.get("media_type") != "image":
            continue
        url = context.get("image_data_url") or ""
        source = context.get("source") or "图片"
        if not str(url).startswith("data:image/"):
            raise ProviderError(f"图片「{source}」无法读取，请重新上传")
        blocks.append({"type": "image_url", "image_url": {"url": url}})
    if blocks and settings.mode != "cloud":
        raise ProviderError(
            "当前是本地文本模型，不能理解图片。请使用云端 deepseek-flash。"
        )
    return blocks


def _build_messages(
    question: str,
    contexts: list[dict],
    history: list[dict] | None,
    mode: str = "ask",
) -> list[ChatMessage]:
    mode_config = get_mode(mode)
    pinned = [c for c in contexts if c.get("context_type") == "eval_report"]
    attachments = [c for c in contexts if c.get("context_type") == "attachment"]
    retrieved = [c for c in contexts if not c.get("pinned")]
    prompt = render_prompt(
        "qa_answer.j2",
        contexts=contexts,
        pinned_contexts=pinned,
        attachment_contexts=attachments,
        retrieved_contexts=retrieved,
        question=question,
        history=(history or [])[-MAX_HISTORY_TURNS:],
        mode=mode_config,
    )
    images = _image_blocks(contexts)
    user_content: str | list = (
        [{"type": "text", "text": prompt}, *images] if images else prompt
    )
    return [
        ChatMessage(
            "system",
            f"你是面向高校教师的教学支持助手「北大问教」，"
            f"当前工作模式为「{mode_config.label}」。",
        ),
        ChatMessage("user", user_content),
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
            "context_type": c.get("context_type", ""),
            "whole_case": bool(c.get("whole_case")),
            "documents": c.get("documents", []),
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
    mode: str = "ask",
) -> dict[str, Any]:
    plan = plan_retrieval(
        question,
        history,
        corpora,
        eval_selected=any(
            c.get("context_type") == "eval_report" for c in (pinned_contexts or [])
        ),
        mode=mode,
    )
    contexts = _assemble_contexts(plan, user_id, eval_task_ids, pinned_contexts)
    try:
        answer = get_llm().chat(
            _build_messages(plan["standalone_question"], contexts, history, mode)
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
    mode: str = "ask",
) -> Iterator[dict[str, Any]]:
    """流式问答。先把检索规划和引用推给前端，再逐字推答案。"""
    plan = plan_retrieval(
        question,
        history,
        corpora,
        eval_selected=any(
            c.get("context_type") == "eval_report" for c in (pinned_contexts or [])
        ),
        mode=mode,
    )
    contexts = _assemble_contexts(plan, user_id, eval_task_ids, pinned_contexts)
    yield {"type": "plan", "data": plan}
    yield {"type": "citations", "data": _citations(contexts)}

    parts: list[str] = []
    try:
        for chunk in get_llm().stream_chat(
            _build_messages(plan["standalone_question"], contexts, history, mode)
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
