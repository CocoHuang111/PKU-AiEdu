"""工具调度页：分段切换频次条。

切换时刻来自 raw_features.slides.slide_change_times；旧任务没有时刻则留空。
"""

from __future__ import annotations

import math
from typing import Any

from .pace_charts import BAND, GRID, MUTED, RED, _feat, _setup, _to_png, _zh_font

BIN_SEC = 5 * 60
BAND_LO = 1.5  # 对应每 10 分钟 3 次
BAND_HI = 2.5  # 对应每 10 分钟 5 次


def _duration(result: dict[str, Any]) -> float:
    minutes = ((result.get("overall") or {}).get("duration_minutes"))
    if minutes:
        return float(minutes) * 60
    times = _change_times(result)
    if times:
        return max(times[-1] * 1.08, BIN_SEC)
    return BIN_SEC


def _change_times(result: dict[str, Any]) -> list[float]:
    raw = ((result.get("raw_features") or {}).get("slides") or {}).get("slide_change_times")
    if not isinstance(raw, list):
        return []
    out = []
    for v in raw:
        try:
            sec = float(v)
        except (TypeError, ValueError):
            continue
        if sec >= 0:
            out.append(sec)
    return sorted(out)


def render_slide_freq(result: dict[str, Any]) -> bytes:
    plt = _setup()
    font = _zh_font()
    duration = _duration(result)
    times = _change_times(result)
    n_bins = max(1, math.ceil(duration / BIN_SEC))
    counts = [0] * n_bins
    for t in times:
        idx = min(int(t // BIN_SEC), n_bins - 1)
        counts[idx] += 1

    fig, ax = plt.subplots(figsize=(5.6, 2.45), layout="constrained")
    if not times and _feat(result, "slides", "slide_change_count") is None:
        ax.text(0.5, 0.5, "暂无切换时刻", ha="center", va="center", fontproperties=font, color=MUTED)
        ax.set_axis_off()
        return _to_png(fig)

    xs = list(range(n_bins))
    ax.axhspan(BAND_LO, BAND_HI, color=BAND, zorder=0)
    ax.bar(xs, counts, width=0.62, color=RED, alpha=0.88, zorder=2)
    ax.plot(xs, counts, color=RED, linewidth=1.4, marker="o", markersize=4.5, zorder=3)
    ymax = max(8, max(counts, default=0) + 1)
    ax.set_ylim(0, ymax)
    ax.set_xlim(-0.6, max(n_bins - 0.4, 0.6))
    labels = [f"{i * 5}-{i * 5 + 5}" for i in xs]
    if n_bins > 10:
        labels = [lab if i % 2 == 0 or i == n_bins - 1 else "" for i, lab in enumerate(labels)]
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontproperties=font, fontsize=8)
    ax.set_ylabel("次 / 5分钟", fontproperties=font, fontsize=9, color=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    return _to_png(fig)


CHARTS = {
    "slide_freq": render_slide_freq,
}
