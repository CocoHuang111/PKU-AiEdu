"""课件时序特征：用本地帧差检测板书/课件的切换时刻，算停留时长与讲授同步率。

对应三条时间敏感的三级指标：「板书/课件停留充分」「课件切换与讲授同步」
「多媒体切换使用熟练」。这些指标 12 张关键帧根本覆盖不到（45 分钟课约每
3.75 分钟一帧），必须靠密集抽帧。好在帧差比对是纯 numpy，零 API 成本。

有 VLM 时先在关键帧上框出投影/板书，密集轨只比对框内；框不到则退回整幅
8×5 格子。格子看「变化最大的那一格」，候选还要等下一采样定住才计入
（翻页后画面会停，走动则下一拍仍在变）。

仍不是精确页数：框偏了、投影极暗、人在框里停住时仍会漏报或多记。
"""

from __future__ import annotations

import statistics

from ..pedagogy.loader import load_yaml
from . import media
from .text_features import _lexicon


BLANK_STD_THRESHOLD = 8.0
GRID_COLS = 8
GRID_ROWS = 5
# 跳变格子在下一采样的平均差低于 threshold × 此系数，才认定画面已定住
SETTLE_RATIO = 0.5
ROI_PAD = 0.08


def _cell_means(frame, cols: int, rows: int):
    """把灰度帧切成 cols×rows 格，返回每格均值，shape (rows, cols)。"""
    import numpy as np

    h, w = frame.shape[:2]
    ys = np.linspace(0, h, rows + 1, dtype=int)
    xs = np.linspace(0, w, cols + 1, dtype=int)
    out = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        for j in range(cols):
            out[i, j] = float(frame[ys[i] : ys[i + 1], xs[j] : xs[j + 1]].mean())
    return out


def _pad_box(box: dict, pad: float = ROI_PAD) -> dict:
    x, y, w, h = (float(box["x"]), float(box["y"]), float(box["w"]), float(box["h"]))
    x0 = max(0.0, x - w * pad)
    y0 = max(0.0, y - h * pad)
    x1 = min(1.0, x + w * (1.0 + pad))
    y1 = min(1.0, y + h * (1.0 + pad))
    out = {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}
    if box.get("kind"):
        out["kind"] = box["kind"]
    return out


def _crop_box(frame, box: dict):
    h, w = frame.shape[:2]
    x0 = int(round(float(box["x"]) * w))
    y0 = int(round(float(box["y"]) * h))
    x1 = int(round((float(box["x"]) + float(box["w"])) * w))
    y1 = int(round((float(box["y"]) + float(box["h"])) * h))
    x0 = max(0, min(x0, w - 2))
    x1 = max(x0 + 2, min(x1, w))
    y0 = max(0, min(y0, h - 2))
    y1 = max(y0 + 2, min(y1, h))
    return frame[y0:y1, x0:x1]


def _roi_crops(frame, rois: list[dict]):
    crops = []
    for box in rois:
        crop = _crop_box(frame, _pad_box(box))
        if crop.size >= 16:
            crops.append(crop)
    return crops


def _signature(frame, rois: list[dict] | None):
    """一帧的比对向量：有框则只取框内格子，否则用整幅 8×5。"""
    import numpy as np

    if rois:
        parts = []
        for crop in _roi_crops(frame, rois):
            ch, cw = crop.shape[:2]
            cols = min(GRID_COLS, max(2, cw // 8))
            rows = min(GRID_ROWS, max(2, ch // 8))
            parts.append(_cell_means(crop, cols, rows).ravel())
        if parts:
            return np.concatenate(parts)
    return _cell_means(frame, GRID_COLS, GRID_ROWS).ravel()


def _scan_frames(
    frame_iter,
    threshold: float,
    rois: list[dict] | None = None,
) -> tuple[int, list[int], int]:
    """单趟扫描帧流，同时得到总帧数、切换位置、纯色帧数。

    只保留上一帧的格子均值和一帧未确认的候选，内存占用与视频长度无关。
    切换记在「新画面出现」的那一帧；下一帧格子已稳住才写入结果。
    片尾还在动的候选丢掉，避免走动持续到结束时多记一次。
    """
    import numpy as np

    boxes = list(rois or [])
    changes: list[int] = []
    total = blank = 0
    prev_means = None
    pending: tuple[int, object] | None = None

    for frame in frame_iter:
        crops = _roi_crops(frame, boxes) if boxes else [frame]
        if crops and all(c.std() < BLANK_STD_THRESHOLD for c in crops):
            blank += 1
        means = _signature(frame, boxes or None)
        if prev_means is not None and means.shape == prev_means.shape:
            cell_diff = np.abs(means - prev_means) / 255.0
            jumped = cell_diff > threshold

            if pending is not None:
                idx, mask = pending
                settled = (
                    mask.any()
                    and float(cell_diff[mask].mean()) < threshold * SETTLE_RATIO
                )
                if settled:
                    changes.append(idx)
                pending = None

            if jumped.any():
                pending = (total, jumped)

        prev_means = means
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
    rois: list[dict] | None = None,
) -> dict[str, float]:
    return _extract_slide_features_from_iter(
        media.iter_gray_frames(video_path, interval_sec=interval_sec),
        asr_segments=asr_segments,
        interval_sec=interval_sec,
        change_threshold=change_threshold,
        rois=rois,
    )


def extract_slide_features_from_images(
    image_paths: list[str],
    asr_segments: list | None = None,
    interval_sec: float = 3.0,
    change_threshold: float = 0.08,
    rois: list[dict] | None = None,
) -> dict[str, float]:
    """用浏览器上传的密集画面计算课件切换特征。"""
    return _extract_slide_features_from_iter(
        media.iter_gray_image_files(image_paths),
        asr_segments=asr_segments,
        interval_sec=interval_sec,
        change_threshold=change_threshold,
        rois=rois,
    )


def _extract_slide_features_from_iter(
    frame_iter,
    *,
    asr_segments: list | None,
    interval_sec: float,
    change_threshold: float,
    rois: list[dict] | None,
) -> dict[str, float]:
    boxes = [b for b in (rois or []) if isinstance(b, dict) and "x" in b]
    total, changes, blank = _scan_frames(
        frame_iter,
        change_threshold,
        rois=boxes or None,
    )
    if total < 2:
        raise media.MediaError(f"密集画面不足（得到 {total} 帧）")
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
        features["dwell_samples"] = [round(d, 1) for d in dwells]

    change_times = [i * interval_sec for i in changes]
    features["slide_change_times"] = [round(t, 1) for t in change_times]
    if (sync := _sync_ratio(change_times, asr_segments or [], window)) is not None:
        features["slide_sync_ratio"] = sync

    return features
