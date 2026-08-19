"""时序特征：从带时间戳的 ASR 片段里算提问等待时间与转写置信度。

这两项都不需要 librosa，也不需要重新解码音频，只用 ASR 已经产出的
时间戳和解码指标，所以不受 config.yaml 的 audio_enabled 开关影响。
"""

from __future__ import annotations

import statistics

from ..pedagogy.loader import load_yaml
from .text_features import _lexicon, _split_sentences, is_question


def _ends_with_question(text: str, lex: dict) -> bool:
    """判断片段是否以提问收尾。

    只认「问句落在片段末尾」的样本：Whisper 的片段是 5–30 秒的块，提问句若在
    片段中间，片段之间的间隔测的就不是提问后的停顿，算进来只会污染统计。
    """
    stripped = text.rstrip()
    if not stripped:
        return False
    if stripped.endswith(("?", "？")):
        return True
    sentences = _split_sentences(stripped)
    return bool(sentences) and is_question(sentences[-1], lex)


def extract_wait_time_features(segments: list) -> dict[str, float]:
    """提问后的思考等待时间。

    对应三级指标「提问后保留有效思考等待时间」。教育研究里 3 秒是分界线
    （Rowe 的 wait-time 实验），所以除了均值还单独报达标比例。
    """
    if len(segments) < 2:
        return {}

    lex = _lexicon()
    conf = load_yaml("feature_lexicon.yaml")["timeline_thresholds"]
    effective = float(conf["wait_time_effective_sec"])
    cap = float(conf["wait_time_cap_sec"])

    gaps: list[float] = []
    for cur, nxt in zip(segments, segments[1:]):
        if not _ends_with_question(cur.text, lex):
            continue
        gap = float(nxt.start) - float(cur.end)
        if gap < 0:
            continue
        gaps.append(min(gap, cap))

    if not gaps:
        return {"wait_time_sample_count": 0}

    return {
        "wait_time_sample_count": len(gaps),
        "wait_time_mean": round(statistics.fmean(gaps), 1),
        "wait_time_median": round(statistics.median(gaps), 1),
        "wait_time_effective_ratio": round(
            100.0 * sum(1 for g in gaps if g >= effective) / len(gaps), 1
        ),
    }


def extract_asr_confidence(segments: list) -> dict[str, float]:
    """转写置信度，作为「口齿清晰」的弱代理。

    按片段时长加权：长片段更能代表整堂课的发音状况，等权平均会让
    一句「嗯」和一段三十秒的讲授占同样分量。
    """
    scored = [
        (s, float(s.avg_logprob))
        for s in segments
        if getattr(s, "avg_logprob", None) is not None
    ]
    if not scored:
        return {}

    threshold = float(
        load_yaml("feature_lexicon.yaml")["timeline_thresholds"][
            "asr_low_confidence_logprob"
        ]
    )

    total_dur = sum(max(float(s.end) - float(s.start), 0.0) for s, _ in scored)
    if total_dur <= 0:
        return {}

    weighted = sum(
        lp * max(float(s.end) - float(s.start), 0.0) for s, lp in scored
    )
    low_dur = sum(
        max(float(s.end) - float(s.start), 0.0)
        for s, lp in scored
        if lp < threshold
    )

    return {
        "asr_confidence": round(weighted / total_dur, 3),
        "asr_low_confidence_ratio": round(100.0 * low_dur / total_dur, 1),
    }


def extract_timeline_features(segments: list) -> dict[str, float]:
    if not segments:
        return {}
    features = dict(extract_wait_time_features(segments))
    features.update(extract_asr_confidence(segments))
    return features
