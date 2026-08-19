"""课件时序特征：用本地帧差检测板书/课件的切换时刻，算停留时长与讲授同步率。

对应三条时间敏感的三级指标：「板书/课件停留充分」「课件切换与讲授同步」
「多媒体切换使用熟练」。这些指标 12 张关键帧根本覆盖不到（45 分钟课约每
3.75 分钟一帧），必须靠密集抽帧。好在帧差比对是纯 numpy，零 API 成本。

已知局限：机位同时拍到板书和投影时，画面差异无法区分「翻页」与「教师走动」，
所以切换次数是上界而非精确值。要更准需要先框定屏幕区域再比对。
"""

from __future__ import annotations

import statistics

from ..pedagogy.loader import load_yaml
from . import media
from .text_features import _lexicon


BLANK_STD_THRESHOLD = 8.0


def _scan_frames(frame_iter, threshold: float) -> tuple[int, list[int], int]:
    """单趟扫描帧流，同时得到总帧数、切换位置、纯色帧数。

    只保留上一帧，内存占用与视频长度无关。
    """
    import numpy as np

    changes: list[int] = []
    total = blank = 0
    prev = None
    for frame in frame_iter:
        if frame.std() < BLANK_STD_THRESHOLD:
            blank += 1
        if prev is not None:
            diff = float(np.abs(frame.astype(np.int16) - prev).mean()) / 255.0
            if diff > threshold:
                changes.append(total)
        prev = frame.astype(np.int16)
        total += 1
    return total, changes, blank


def _sync_ratio(
    change_times: list[float], segments: list, window: float
) -> float | None:
    """切换时刻附近是否有过渡衔接话语，用来看「切换与讲授是否同步」。

    只能说明切换和话语节奏对得上，不能说明讲的内容和页面内容一致——
    后者需要语义判断，留给 Judge。
    """
    if not change_times or not segments:
        return None

    lex = _lexicon()
    markers = lex["transition_markers"]
    matched = 0
    for t in change_times:
        lo, hi = t - window, t + window
        nearby = [
            s for s in segments if float(s.end) >= lo and float(s.start) <= hi
        ]
        if any(any(m in s.text for m in markers) for s in nearby):
            matched += 1
    return round(100.0 * matched / len(change_times), 1)


def extract_slide_features(
    video_path: str,
    asr_segments: list | None = None,
    interval_sec: float = 3.0,
    change_threshold: float = 0.08,
) -> dict[str, float]:
    total, changes, blank = _scan_frames(
        media.iter_gray_frames(video_path, interval_sec=interval_sec),
        change_threshold,
    )
    total_min = total * interval_sec / 60.0

    thresholds = load_yaml("feature_lexicon.yaml")["slide_thresholds"]
    dwell_min = float(thresholds["dwell_min_sec"])
    window = float(thresholds["sync_window_sec"])

    features: dict[str, float] = {
        "slide_change_count": len(changes),
        "slide_change_per_10min": round(10.0 * len(changes) / max(total_min, 1.0), 1),
        "blank_frame_ratio": round(100.0 * blank / total, 1),
    }

    # 停留时长 = 相邻两次切换之间的间隔，首尾两段一并计入
    boundaries = [0, *changes, total]
    dwells = [
        (boundaries[i + 1] - boundaries[i]) * interval_sec
        for i in range(len(boundaries) - 1)
    ]
    dwells = [d for d in dwells if d > 0]
    if dwells:
        features["dwell_median_sec"] = round(statistics.median(dwells), 1)
        features["dwell_short_ratio"] = round(
            100.0 * sum(1 for d in dwells if d < dwell_min) / len(dwells), 1
        )

    change_times = [i * interval_sec for i in changes]
    if (sync := _sync_ratio(change_times, asr_segments or [], window)) is not None:
        features["slide_sync_ratio"] = sync

    return features
