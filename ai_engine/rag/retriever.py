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
) -> list[dict[str, Any]]:
    """对每条 query 在每个 corpus 里检索，合并结果。

    同一段文本被多条 query 命中时保留最高分——被反复命中说明更相关。
    """
    if not queries or not corpora:
        return []

    top_k = top_k or settings.section("rag").get("top_k", 5)
    embedder = get_embedder()
    query_vectors = embedder.embed(queries)

    merged: dict[str, dict[str, Any]] = {}
    for vector in query_vectors:
        for corpus in corpora:
            for hit in store.query(corpus, vector, top_k=top_k):
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
