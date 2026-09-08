"""Chroma 向量库封装：一个语料库对应一个 collection。

不使用 Chroma 内置的 embedding function，统一走 providers.get_embedder()，
这样云端/本地切换对向量库是透明的。
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from typing import Any

from ..config import settings
from ..providers import get_embedder


@lru_cache(maxsize=1)
def _client():
    import chromadb
    from chromadb.config import Settings as ChromaSettings

    persist_dir = settings.chroma_dir
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(persist_dir),
        settings=ChromaSettings(anonymized_telemetry=False, allow_reset=True),
    )


def _collection(name: str):
    return _client().get_or_create_collection(
        name=name, metadata={"hnsw:space": "cosine"}
    )


def doc_id(
    corpus: str,
    source: str,
    index: int,
    user_id: str | None = None,
    task_id: str | None = None,
) -> str:
    raw = f"{corpus}::{user_id or ''}::{task_id or ''}::{source}::{index}"
    return hashlib.md5(raw.encode()).hexdigest()


def reset_collection(name: str) -> None:
    try:
        _client().delete_collection(name)
    except Exception:
        pass
    _collection(name)


def add_chunks(
    corpus: str, chunks: list[str], metadatas: list[dict[str, Any]]
) -> int:
    """写入前先算向量。metadata 必须是扁平的标量，Chroma 不接受嵌套。"""
    if not chunks:
        return 0

    embeddings = get_embedder().embed(chunks)
    flat_metas = [
        {k: v for k, v in m.items() if isinstance(v, (str, int, float, bool))}
        for m in metadatas
    ]
    ids = [
        doc_id(
            corpus,
            str(m.get("source", "unknown")),
            int(m.get("chunk_index", i)),
            user_id=str(m.get("user_id") or "") or None,
            task_id=str(m.get("task_id") or "") or None,
        )
        for i, m in enumerate(flat_metas)
    ]

    col = _collection(corpus)
    try:
        col.upsert(
            ids=ids, documents=chunks, embeddings=embeddings, metadatas=flat_metas
        )
    except Exception as e:
        # 换过 embedding 模型后维度对不上，Chroma 会报错。清库重建。
        if "dimension" in str(e).lower():
            print(f"  [提示] {corpus} 向量维度变化，重建该 collection")
            reset_collection(corpus)
            _collection(corpus).upsert(
                ids=ids, documents=chunks, embeddings=embeddings, metadatas=flat_metas
            )
        else:
            raise
    return len(chunks)


def query(
    corpus: str,
    query_embedding: list[float],
    top_k: int = 5,
    where: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    col = _collection(corpus)
    if col.count() == 0:
        return []

    kwargs: dict[str, Any] = {
        "query_embeddings": [query_embedding],
        "n_results": min(top_k, col.count()),
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        kwargs["where"] = where
    res = col.query(**kwargs)
    hits = []
    for text, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        hits.append(
            {
                "text": text,
                "metadata": meta or {},
                "corpus": corpus,
                "score": round(1.0 - float(dist), 4),  # cosine 距离转相似度
            }
        )
    return hits


def delete_eval_report_chunks(task_id: str, user_id: str | None = None) -> None:
    where: dict[str, Any] = {"task_id": task_id}
    if user_id:
        where = {"$and": [{"task_id": task_id}, {"user_id": user_id}]}
    try:
        _collection("eval_reports").delete(where=where)
    except Exception as exc:
        print(f"[warn] 删除 eval_reports 失败: {exc}")


def collection_stats() -> dict[str, int]:
    stats = {}
    for c in settings.corpora:
        try:
            stats[c["name"]] = _collection(c["name"]).count()
        except Exception:
            stats[c["name"]] = 0
    return stats
