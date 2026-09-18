"""时序特征：从带时间戳的 ASR 片段里计算转写置信度。

该项不需要 librosa，也不需要重新解码音频，只用 ASR 已经产出的
时间戳和解码指标，所以不受 config.yaml 的 audio_enabled 开关影响。
"""

from __future__ import annotations

from ..pedagogy.loader import load_yaml


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
    return extract_asr_confidence(segments)
