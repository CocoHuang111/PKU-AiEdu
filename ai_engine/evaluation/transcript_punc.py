"""Whisper 中文转写后补标点。学 Atmos：ASR 仍用 Whisper，再用现成 LLM 只加标点。

不改字、不删字、不加字，片段起止时间不变。问句落在片段末尾时，等待时间才能对上。
LLM 不可用或行数对不上时，退回规则断句，评估不中断。
"""

from __future__ import annotations

import re
import hashlib
import json
import time
from dataclasses import replace
from pathlib import Path

from .. import checkpoints
from ..config import settings

from ..providers import ASRResult, ASRSegment, ChatMessage, ProviderError, get_llm
from .text_features import CHINESE_CHAR

CN_PUNCT = re.compile(r"[。！？；，、]")
HANZI = CHINESE_CHAR
NUMBERED = re.compile(r"^\s*(\d+)[\.、:：)]\s*(.*)$")
CHUNK_CHARS = 1500
# 每百汉字少于约 1.5 个中文标点，视为缺标点
PUNCT_RATIO = 0.015

SYSTEM = (
    "你是中文课堂转写的标点校对助手。"
    "只补标点，不改写内容。"
)

USER_TMPL = """下面每行是一段语音识别原文，可能没有标点。
请只补中文标点（。，、？！：；），不要改字、不要删字、不要加字，不要合并或拆分行。
问句用问号。直接按同样的行号输出正文，不要解释，不要用 markdown 代码块。

{body}
"""


def needs_punctuation(text: str, min_zh: int = 8) -> bool:
    """英文 Whisper 通常已有标点；中文墙字才需要补。

    阈值用 8 个汉字：Whisper 一段常常只有十几个字，用 20 会整段被跳过。
    """
    if not (text or "").strip():
        return False
    zh = HANZI.findall(text)
    if len(zh) < min_zh:
        return False
    return len(CN_PUNCT.findall(text)) / max(len(zh), 1) < PUNCT_RATIO


def _hanzi_only(text: str) -> str:
    return "".join(HANZI.findall(text or ""))


def _same_wording(old: str, new: str) -> bool:
    a, b = _hanzi_only(old), _hanzi_only(new)
    if not a:
        return bool(new.strip())
    if not b:
        return False
    # 允许极少量繁简/同形差，不允许改写讲课内容
    if a == b:
        return True
    return abs(len(a) - len(b)) <= 2 and (
        a in b or b in a or _overlap_ratio(a, b) >= 0.92
    )


def _overlap_ratio(a: str, b: str) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    same = sum(1 for x, y in zip(a, b) if x == y)
    return same / max(len(a), len(b))


def parse_numbered_lines(raw: str, n: int) -> list[str] | None:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    numbered: list[tuple[int, str]] = []
    plain: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if m := NUMBERED.match(s):
            numbered.append((int(m.group(1)), m.group(2).strip()))
        else:
            plain.append(s)

    if len(numbered) == n:
        numbered.sort(key=lambda x: x[0])
        if [i for i, _ in numbered] == list(range(1, n + 1)):
            return [t for _, t in numbered]
    if len(plain) == n:
        return plain
    return None


def rule_punctuate(text: str) -> str:
    """LLM 不可用时的断句兜底，口径对齐 Atmos 的规则后处理，只补标点。"""
    text = (text or "").strip()
    if not text:
        return text
    if not needs_punctuation(text):
        return text

    enders = ("了", "的", "吧", "呢", "啊", "嘛", "呀", "吗", "呗", "哦", "哈")
    markers = (
        "但是", "然后", "所以", "因为", "如果", "虽然", "而且", "或者",
        "那么", "不过", "另外", "同时", "首先", "其次", "最后", "总之",
        "比如", "例如", "也就是说", "换句话说",
    )
    for marker in markers:
        text = text.replace(marker, f"，{marker}")

    out: list[str] = []
    since = 0
    for i, ch in enumerate(text):
        out.append(ch)
        since += 1
        if ch in "，。？！、；：":
            since = 0
            continue
        if since >= 25 and ch in enders:
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if nxt not in "，。？！、；：\n":
                out.append("？" if ch in ("吗", "呢") else "。")
                since = 0
    processed = re.sub(r"，{2,}", "，", "".join(out))
    processed = processed.lstrip("，")
    if processed and processed[-1] not in "，。？！、；：":
        processed += "？" if processed[-1] in ("吗", "呢") else "。"
    return processed


def _format_batch(texts: list[str]) -> str:
    return "\n".join(f"{i}. {t}" for i, t in enumerate(texts, start=1))


def _apply_batch(old: list[str], new: list[str] | None) -> list[str]:
    if not new or len(new) != len(old):
        return [rule_punctuate(t) for t in old]
    out = []
    for src, dst in zip(old, new):
        dst = re.sub(r"\n+", "", (dst or "").strip())
        out.append(dst if _same_wording(src, dst) else rule_punctuate(src))
    return out


def punctuate_texts(
    texts: list[str],
    llm_fn=None,
    chunk_chars: int = CHUNK_CHARS,
    progress_callback=None,
    budget_seconds: float = 180,
    checkpoint_dir: Path | None = None,
) -> list[str]:
    """给若干片段补标点，顺序与条数不变。"""
    if not texts:
        return []
    if not any(needs_punctuation(t) for t in texts):
        if progress_callback:
            progress_callback(len(texts), len(texts), {"skipped": True})
        return list(texts)

    started = time.monotonic()

    def call_llm(prompt: str) -> str:
        if llm_fn:
            return llm_fn(prompt)
        return get_llm().chat(
            [ChatMessage("system", SYSTEM), ChatMessage("user", prompt)],
            temperature=0.1,
            timeout=max(1, min(60, budget_seconds - (time.monotonic() - started))),
        )

    result = list(texts)
    i = 0
    batch_index = 0
    while i < len(texts):
        batch: list[str] = []
        idxs: list[int] = []
        size = 0
        while i < len(texts) and (not batch or size + len(texts[i]) <= chunk_chars):
            batch.append(texts[i])
            idxs.append(i)
            size += len(texts[i])
            i += 1
        signature = hashlib.sha256(json.dumps(
            [2, batch, budget_seconds, settings.mode, settings.section("llm")],
            ensure_ascii=False, sort_keys=True,
        ).encode()).hexdigest()
        path = checkpoint_dir / f"{batch_index:05d}.json" if checkpoint_dir else None
        saved = checkpoints.read(path, signature) if path else None
        detail = {"batch": batch_index + 1}
        if saved is not None:
            filled = saved["texts"]
            detail.update(saved["detail"], cached=True)
        elif not any(needs_punctuation(t) for t in batch):
            filled = batch
            detail["skipped"] = True
        else:
            parsed = None
            if time.monotonic() - started < budget_seconds:
                try:
                    raw = call_llm(USER_TMPL.format(body=_format_batch(batch)))
                    parsed = parse_numbered_lines(raw, len(batch))
                except Exception:
                    pass
            else:
                detail["budget_exhausted"] = True
            filled = _apply_batch(batch, parsed)
            detail["rule_fallback"] = parsed is None
        if path and saved is None:
            checkpoints.write(path, signature, {"texts": filled, "detail": detail})
        for j, text in zip(idxs, filled):
            result[j] = text
        batch_index += 1
        if progress_callback:
            progress_callback(i, len(texts), detail)
    return result


def punctuate_asr_result(result: ASRResult, llm_fn=None, **kwargs) -> ASRResult:
    """补片段文本里的标点，重拼 full_text；时间戳与置信度不动。"""
    if not result.segments:
        text = result.text or ""
        if not needs_punctuation(text):
            return result
        filled = punctuate_texts([text], llm_fn=llm_fn, **kwargs)[0]
        return replace(result, text=filled)

    old = [s.text for s in result.segments]
    if not any(needs_punctuation(t) for t in old) and not needs_punctuation(result.text or ""):
        return result
    new_texts = punctuate_texts(old, llm_fn=llm_fn, **kwargs)
    segments = [
        replace(seg, text=text) for seg, text in zip(result.segments, new_texts)
    ]
    return replace(result, segments=segments, text="".join(s.text for s in segments))
