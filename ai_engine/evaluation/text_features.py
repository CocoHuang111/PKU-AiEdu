"""文本客观特征：从 ASR 转写里统计可量化的事实，作为 Judge 的证据。

这些数字是"事实层"，LLM 只负责在事实基础上做"判断层"，
避免大模型对语速、提问次数这类可精确计算的量凭感觉打分。
"""

from __future__ import annotations

import re
import statistics

from ..pedagogy.loader import load_yaml

CHINESE_CHAR = re.compile(r"[\u4e00-\u9fff]")
SENTENCE_SPLIT = re.compile(r"[。！？!?；;\n]+")
# 年份引用：只认 2000-2099，避免把「1+1」这类数字或学号误当年份
YEAR_REF = re.compile(r"20\d{2}")


def _lexicon() -> dict:
    return load_yaml("feature_lexicon.yaml")


def _count_markers(text: str, markers: list[str]) -> int:
    return sum(text.count(m) for m in markers)


def _split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def is_question(sentence: str, lex: dict | None = None) -> bool:
    """判断一句话是否为提问。judge 之外的模块（等待时间统计）也要用同一口径。"""
    lex = lex or _lexicon()
    return (
        "?" in sentence
        or "？" in sentence
        or any(m in sentence for m in lex["question_markers"])
    )


def extract_text_features(text: str, duration_sec: float) -> dict[str, float]:
    """duration_sec 为课堂总时长，用于把绝对计数换算成速率。"""
    lex = _lexicon()
    minutes = max(duration_sec / 60.0, 1.0)
    char_count = len(CHINESE_CHAR.findall(text))
    sentences = _split_sentences(text)

    question_sentences = [s for s in sentences if is_question(s, lex)]
    open_questions = [
        s
        for s in question_sentences
        if any(m in s for m in lex["open_question_markers"])
    ]

    question_count = len(question_sentences)
    filler_count = _count_markers(text, lex["filler_markers"])

    # 认知层级：两表都没命中的提问不计入分母，避免比例虚高
    higher = sum(
        1
        for s in question_sentences
        if any(m in s for m in lex["bloom_higher_markers"])
    )
    lower = sum(
        1
        for s in question_sentences
        if not any(m in s for m in lex["bloom_higher_markers"])
        and any(m in s for m in lex["bloom_lower_markers"])
    )
    classified = higher + lower

    return {
        "duration_minutes": round(minutes, 1),
        "total_chars": char_count,
        "sentence_count": len(sentences),
        "speech_rate": round(char_count / minutes, 1),
        "question_count": question_count,
        "open_question_count": len(open_questions),
        "open_question_ratio": round(
            100.0 * len(open_questions) / question_count, 1
        )
        if question_count
        else 0.0,
        "question_per_10min": round(10.0 * question_count / minutes, 1),
        "higher_order_question_count": higher,
        "higher_order_question_ratio": round(100.0 * higher / classified, 1)
        if classified
        else 0.0,
        "classified_question_count": classified,
        "interaction_count": _count_markers(text, lex["interaction_markers"]),
        "discipline_count": _count_markers(text, lex["discipline_markers"]),
        "inspire_count": _count_markers(text, lex["inspire_markers"]),
        "transition_count": _count_markers(text, lex["transition_markers"]),
        "case_count": _count_markers(text, lex["case_markers"]),
        "recency_count": _count_markers(text, lex["recency_markers"]),
        "year_ref_count": len(YEAR_REF.findall(text)),
        "filler_count": filler_count,
        "filler_density": round(100.0 * filler_count / max(char_count, 1), 2),
        "student_speech_count": _count_markers(text, lex["student_speech_markers"]),
    }


def segment_transcript(
    segments: list, minutes_per_chunk: float = 5.0
) -> list[dict]:
    """把带时间戳的 ASR 片段按时长聚合成分段，用于观察课堂节奏变化。"""
    if not segments:
        return []

    window = minutes_per_chunk * 60.0
    chunks: list[dict] = []
    buf: list = []
    chunk_start = segments[0].start

    for seg in segments:
        if seg.end - chunk_start > window and buf:
            chunks.append(_build_chunk(buf, len(chunks)))
            buf = []
            chunk_start = seg.start
        buf.append(seg)
    if buf:
        chunks.append(_build_chunk(buf, len(chunks)))
    return chunks


def _gini(values: list[float]) -> float:
    """基尼系数：0 = 完全均匀，1 = 全部集中在一处。用于看提问是否只堆在某一段。

    归一化到 [0, 1]（乘 n/(n-1)），否则段数少时上界达不到 1，不同课之间不可比。
    """
    n = len(values)
    if n < 2 or sum(values) <= 0:
        return 0.0
    mean = sum(values) / n
    diff_sum = sum(abs(a - b) for a in values for b in values)
    gini = diff_sum / (2 * n * n * mean)
    return min(1.0, gini * n / (n - 1))


def summarize_segments(chunks: list[dict]) -> dict[str, float]:
    """把分段特征汇总成整堂课的节奏指标。

    分段数据本来只用于前端画图，但「语速是否稳定」「提问分布是否均匀」
    「有没有前松后紧」只能从段间差异看出来，从全局均值里是看不到的。
    """
    if len(chunks) < 2:
        return {}

    rates = [c["features"]["speech_rate"] for c in chunks]
    questions = [float(c["features"]["question_count"]) for c in chunks]
    mean_rate = statistics.fmean(rates)

    summary: dict[str, float] = {
        "segment_count": len(chunks),
        "speech_rate_cv": round(
            100.0 * statistics.pstdev(rates) / mean_rate, 1
        )
        if mean_rate > 0
        else 0.0,
        "question_gini": round(_gini(questions), 3),
        "question_free_segment_ratio": round(
            100.0 * sum(1 for q in questions if q == 0) / len(questions), 1
        ),
    }

    # 前松后紧的检测：比较前 1/3 与后 1/3 段的平均语速。
    # 取三分之一而不是首尾单段，单段容易被一次口误或一段视频噪声带偏。
    third = max(len(chunks) // 3, 1)
    early = statistics.fmean(rates[:third])
    late = statistics.fmean(rates[-third:])
    if early > 0:
        summary["speech_rate_late_ratio"] = round(late / early, 2)

    return summary


def _build_chunk(segs: list, index: int) -> dict:
    text = "".join(s.text for s in segs)
    start, end = segs[0].start, segs[-1].end
    return {
        "index": index,
        "start_sec": round(start, 1),
        "end_sec": round(end, 1),
        "time_range": f"{_fmt(start)} - {_fmt(end)}",
        "text": text,
        "features": extract_text_features(text, max(end - start, 1.0)),
    }


def _fmt(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"
