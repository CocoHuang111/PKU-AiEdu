"""检索：多查询 × 多语料库，合并去重后按分数排序。"""

from __future__ import annotations

from typing import Any

from ..config import settings
from ..providers import get_embedder, get_reranker
from . import store


def _dedup_key(hit: dict[str, Any]) -> str:
    return hit["text"][:120]


def search(
    queries: list[str],
    corpora: list[str],
    top_k: int | None = None,
    rerank_query: str | None = None,
    user_id: str | None = None,
    eval_task_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    """对每条 query 在每个 corpus 里检索，合并结果。

    同一段文本被多条 query 命中时保留最高分——被反复命中说明更相关。
    eval_task_ids 只约束 eval_reports：None=该用户全部报告，空列表=跳过该库。
    """
    if not queries or not corpora:
        return []

    top_k = top_k or settings.section("rag").get("top_k", 5)
    embedder = get_embedder()
    query_vectors = embedder.embed(queries)

    merged: dict[str, dict[str, Any]] = {}
    for vector in query_vectors:
        for corpus in corpora:
            where = None
            if corpus == "eval_reports":
                if not user_id:
                    continue
                if eval_task_ids is not None and not eval_task_ids:
                    continue
                where = {"user_id": user_id}
                if eval_task_ids:
                    where = {
                        "$and": [
                            {"user_id": user_id},
                            {"task_id": {"$in": list(eval_task_ids)}},
                        ]
                    }
            for hit in store.query(corpus, vector, top_k=top_k, where=where):
                key = _dedup_key(hit)
                if key not in merged or hit["score"] > merged[key]["score"]:
                    merged[key] = hit

    hits = sorted(merged.values(), key=lambda h: h["score"], reverse=True)

    if rerank_query and hits:
        reranker = get_reranker()
        ranked = reranker.rerank(rerank_query, [h["text"] for h in hits])
        # IdentityRerank 会原样返回，此时保持向量分数序
        hits = [hits[r.index] for r in ranked]

    return hits


def filter_hits(
    hits: list[dict[str, Any]],
    score_threshold: float | None = None,
    max_hits: int | None = None,
) -> list[dict[str, Any]]:
    """按相似度阈值过滤并截断条数。低于阈值的块丢弃，不降级补入弱相关结果。"""
    rag = settings.section("rag")
    threshold = score_threshold if score_threshold is not None else rag.get(
        "score_threshold", 0.5
    )
    limit = max_hits if max_hits is not None else rag.get("max_hits", 12)
    passed = [h for h in hits if h.get("score", 0) >= threshold]
    passed.sort(key=lambda h: h["score"], reverse=True)
    return passed[:limit]


def build_contexts(
    hits: list[dict[str, Any]], max_chars: int | None = None
) -> list[dict[str, Any]]:
    """把检索结果整理成可以直接喂进提示词的上下文，并按总字数截断。"""
    max_chars = max_chars or settings.section("rag").get("max_context_chars", 6000)

    contexts = []
    used = 0
    for hit in hits:
        text = hit["text"]
        if used + len(text) > max_chars:
            if used == 0:  # 第一条就超限，截一段进去总比空手好
                text = text[:max_chars]
            else:
                break
        meta = hit.get("metadata", {})
        contexts.append(
            {
                "text": text,
                "corpus": hit["corpus"],
                "corpus_label": settings.corpus_meta(hit["corpus"]).get(
                    "label", hit["corpus"]
                ),
                "source": meta.get("source", "未知来源"),
                "score": hit["score"],
            }
        )
        used += len(text)
    return contexts


def merge_contexts(
    pinned: list[dict[str, Any]],
    retrieved: list[dict[str, Any]],
    max_chars: int | None = None,
) -> list[dict[str, Any]]:
    """勾选的评估报告用单独额度，检索结果再用 max_context_chars。"""
    rag = settings.section("rag")
    rag_cap = max_chars or rag.get("max_context_chars", 6000)
    pin_cap = rag.get("pinned_eval_max_chars", 12000)
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()

    used_pin = 0
    for item in pinned or []:
        text = (item.get("text") or "").strip()
        if not text:
            continue
        key = text[:120]
        if key in seen:
            continue
        if used_pin + len(text) > pin_cap:
            remain = pin_cap - used_pin
            if remain <= 200:
                break
            text = text[:remain]
        merged.append({**item, "text": text, "pinned": True})
        seen.add(key)
        used_pin += len(text)

    used_rag = 0
    for item in retrieved or []:
        text = (item.get("text") or "").strip()
        if not text:
            continue
        key = text[:120]
        if key in seen:
            continue
        if used_rag + len(text) > rag_cap:
            if used_rag == 0:
                text = text[:rag_cap]
            else:
                break
        merged.append({**item, "text": text})
        seen.add(key)
        used_rag += len(text)
        if used_rag >= rag_cap:
            break
    return merged
