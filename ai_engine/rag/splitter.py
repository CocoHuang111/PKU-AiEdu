"""文本分块：按段落聚合，超长段落再按中文句号切，块间保留 overlap。"""

from __future__ import annotations

import re

from ..config import settings

_SENT_END = re.compile(r"(?<=[。！？；!?;])")


def _split_sentences(text: str) -> list[str]:
    parts = [p for p in _SENT_END.split(text) if p.strip()]
    return parts or [text]


def _hard_wrap(text: str, size: int) -> list[str]:
    """段落本身就超长时，按句子边界硬切。"""
    chunks: list[str] = []
    buf = ""
    for sent in _split_sentences(text):
        if len(buf) + len(sent) > size and buf:
            chunks.append(buf)
            buf = sent
        else:
            buf += sent
        # 单句就超长（比如没有标点的公式串），直接截断
        while len(buf) > size:
            chunks.append(buf[:size])
            buf = buf[size:]
    if buf:
        chunks.append(buf)
    return chunks


def split_text(
    text: str, chunk_size: int | None = None, overlap: int | None = None
) -> list[str]:
    rag = settings.section("rag")
    chunk_size = chunk_size or rag.get("chunk_size", 500)
    overlap = overlap if overlap is not None else rag.get("chunk_overlap", 80)

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    buf = ""
    for para in paragraphs:
        if len(para) > chunk_size:
            if buf:
                chunks.append(buf)
                buf = ""
            chunks.extend(_hard_wrap(para, chunk_size))
        elif len(buf) + len(para) + 1 > chunk_size:
            chunks.append(buf)
            buf = para
        else:
            buf = f"{buf}\n{para}" if buf else para
    if buf:
        chunks.append(buf)

    if overlap <= 0 or len(chunks) < 2:
        return chunks

    # 给每块前面补上一块的尾巴，避免答案正好卡在切分边界上
    merged = [chunks[0]]
    for prev, cur in zip(chunks, chunks[1:]):
        merged.append(prev[-overlap:] + cur)
    return merged
