"""授课内容页的两张图：语速折线、提问结构条。

用 matplotlib 出 PNG，前端按任务数据现取。没有音轨采样，语速点来自分段转写。
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

RED = "#a61b1b"
GRAY = "#c0c4cc"
TEXT = "#303133"
MUTED = "#8a8a8a"
GRID = "#f0f0f0"
BAND = "#e7f4ea"
BAND_EDGE = "#2e8b57"

_FONT_FILES = (
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
)


def _zh_font():
    from matplotlib import font_manager

    for path in _FONT_FILES:
        if path.is_file():
            return font_manager.FontProperties(fname=str(path))
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("PingFang SC", "Heiti SC", "Microsoft YaHei", "Noto Sans CJK SC", "SimHei"):
        if name in available:
            return font_manager.FontProperties(family=name)
    return font_manager.FontProperties()


def _setup():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#e8e8e8",
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "text.color": TEXT,
            "axes.unicode_minus": False,
        }
    )
    return plt


def _to_png(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight", pad_inches=0.18)
    import matplotlib.pyplot as plt

    plt.close(fig)
    return buf.getvalue()


def _feat(result: dict[str, Any], group: str, key: str) -> float | None:
    for row in (result.get("objective_features") or {}).get(group) or []:
        if row.get("key") == key:
            try:
                return float(row.get("value"))
            except (TypeError, ValueError):
                return None
    raw = ((result.get("raw_features") or {}).get(group) or {}).get(key)
    try:
        return float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None


def speech_series(result: dict[str, Any]) -> list[tuple[float, float, str]]:
    """(start_sec, rate, x_label)。"""
    segs = (result.get("transcript") or {}).get("segments") or []
    out: list[tuple[float, float, str]] = []
    used: set[int] = set()
    for seg in segs:
        start = seg.get("start_sec")
        rate = (seg.get("features") or {}).get("speech_rate")
        if start is None or rate is None:
            continue
        start_f = float(start)
        lo = int(start_f // 60 // 5) * 5
        while lo in used:
            lo += 5
        used.add(lo)
        out.append((start_f, float(rate), f"{lo}-{lo + 5}"))
    if out:
        last = out[-1]
        out[-1] = (last[0], last[1], f"{last[2]} 分钟")
    return out


def _pct(value: float | None) -> float | None:
    if value is None:
        return None
    return value * 100.0 if 0 <= value <= 1 else value


def render_speech_rate(result: dict[str, Any]) -> bytes:
    plt = _setup()
    font = _zh_font()
    series = speech_series(result)
    fig, ax = plt.subplots(figsize=(5.4, 2.35))
    if not series:
        ax.text(0.5, 0.5, "暂无分段语速", ha="center", va="center", fontproperties=font, color=MUTED)
        ax.set_axis_off()
        return _to_png(fig)

    xs = list(range(len(series)))
    ys = [p[1] for p in series]
    labels = [p[2] for p in series]
    if len(labels) > 12:
        labels = [lab if i % 2 == 0 or i == len(labels) - 1 else "" for i, lab in enumerate(labels)]
    ax.axhspan(200, 280, color=BAND, zorder=0)
    ax.plot(
        xs,
        ys,
        color=RED,
        linewidth=2.0,
        marker="o",
        markersize=6.5,
        markerfacecolor="white",
        markeredgecolor=RED,
        markeredgewidth=1.6,
        zorder=2,
    )
    ax.set_ylim(0, 400)
    ax.set_yticks([0, 100, 200, 300, 400])
    ax.set_xlim(-0.35, max(len(xs) - 0.65, 0.65))
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontproperties=font, fontsize=8)
    ax.set_ylabel("字/分钟", fontproperties=font, fontsize=10, color=MUTED)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.annotate(
        "推荐区间 200-280",
        xy=(1.01, 240),
        xycoords=("axes fraction", "data"),
        va="center",
        color=BAND_EDGE,
        fontsize=9,
        fontproperties=font,
        annotation_clip=False,
    )
    fig.subplots_adjust(right=0.82)
    return _to_png(fig)


def render_question_structure(result: dict[str, Any]) -> bytes:
    plt = _setup()
    font = _zh_font()
    rows = [
        ("开放性问题", _pct(_feat(result, "text", "open_question_ratio")), RED),
        ("高阶问题", _pct(_feat(result, "text", "higher_order_question_ratio")), RED),
        ("无提问段落", _pct(_feat(result, "text", "question_free_segment_ratio")), GRAY),
    ]
    fig, ax = plt.subplots(figsize=(5.4, 2.35))
    present = [(name, val if val is not None else 0.0, color) for name, val, color in rows]
    if all(v == 0 for _, v, _ in present) and all(row[1] is None for row in rows):
        ax.text(0.5, 0.5, "暂无提问结构", ha="center", va="center", fontproperties=font, color=MUTED)
        ax.set_axis_off()
        return _to_png(fig)

    names = [p[0] for p in present][::-1]
    vals = [p[1] for p in present][::-1]
    colors = [p[2] for p in present][::-1]
    height = 0.28
    gap = 0.5
    step = height + gap
    ys = [i * step for i in range(len(vals))]
    bars = ax.barh(ys, vals, color=colors, height=height)
    extra = ((len(vals) - 1) * step + height) * 0.35
    ax.set_ylim(ys[0] - height / 2 - extra, ys[-1] + height / 2 + extra)
    ax.set_yticks(ys)
    ax.set_yticklabels(names)
    ax.set_xlim(0, 118)
    ax.set_xticks([])
    ax.tick_params(left=False)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font)
        tick.set_fontsize(11)
        tick.set_color(TEXT)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    for bar, val in zip(bars, vals):
        ax.text(
            val + 2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:g}%",
            va="center",
            ha="left",
            fontproperties=font,
            fontsize=11,
            color=TEXT,
        )
    return _to_png(fig)


CHARTS = {
    "speech_rate": render_speech_rate,
    "question_structure": render_question_structure,
}


def render_chart(name: str, result: dict[str, Any]) -> bytes:
    if name not in CHARTS:
        raise KeyError(name)
    return CHARTS[name](result)
