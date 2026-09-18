"""声学特征页的图：波形、响度、基频、提问等待样本。

用 matplotlib 出 PNG。新任务把曲线和 wait_samples 写进 raw_features；
旧任务没有采样时，波形/响度/基频按均值生成示意，等待图留空。
"""

from __future__ import annotations

import math
from typing import Any

from .pace_charts import (
    BAND,
    BAND_EDGE,
    GRID,
    MUTED,
    RED,
    _feat,
    _setup,
    _to_png,
    _zh_font,
)

WAIT_GOOD = (3.0, 6.0)


def _audio(result: dict[str, Any]) -> dict[str, Any]:
    return ((result.get("raw_features") or {}).get("audio") or {})


def _timeline(result: dict[str, Any]) -> dict[str, Any]:
    return ((result.get("raw_features") or {}).get("timeline") or {})


def _duration(result: dict[str, Any]) -> float:
    audio = _audio(result)
    dur = audio.get("audio_duration_sec")
    if dur:
        return float(dur)
    minutes = ((result.get("overall") or {}).get("duration_minutes"))
    if minutes:
        return float(minutes) * 60
    segs = (result.get("transcript") or {}).get("segments") or []
    if segs:
        end = segs[-1].get("end_sec")
        if end:
            return float(end)
    return 1.0


def _clock(sec: float) -> str:
    m, s = divmod(max(int(sec), 0), 60)
    return f"{m:02d}:{s:02d}"


def _wait_samples(result: dict[str, Any]) -> list[float]:
    raw = _timeline(result).get("wait_samples")
    if isinstance(raw, list) and raw:
        out = []
        for v in raw:
            try:
                out.append(float(v))
            except (TypeError, ValueError):
                continue
        return out
    return []


def _synth_envelope(result: dict[str, Any], n: int = 360) -> list[float]:
    loud = _feat(result, "audio", "loudness_db") or -22.0
    silence = _feat(result, "audio", "silence_ratio") or 14.0
    snr = _feat(result, "audio", "snr_estimate") or 18.0
    seed = abs(loud)
    energy = min(1.0, max(0.28, (abs(loud) + 45) / 50))
    quiet = min(0.55, silence / 100)
    jitter = min(1.2, max(0.6, snr / 22))
    env = []
    for i in range(n):
        t = i / n * math.pi * 12 + seed * 0.17
        envelope = math.sin(i / n * math.pi) * (1 - quiet * 0.65)
        wiggle = math.sin(t) * 0.55 + math.sin(t * 2.15) * 0.28 + math.sin(t * 0.4 + seed) * 0.18
        env.append(max(0.02, envelope * energy * (0.35 + abs(wiggle) * jitter)))
    return env


def _synth_curve(mean: float, std: float, duration: float, n: int = 80) -> list[list[float]]:
    out = []
    for i in range(n):
        t = duration * i / max(n - 1, 1)
        wobble = math.sin(i / n * math.pi * 5.5) * 0.65 + math.sin(i / n * math.pi * 1.7) * 0.35
        out.append([t, mean + std * wobble])
    return out


def render_audio_wave(result: dict[str, Any]) -> bytes:
    plt = _setup()
    font = _zh_font()
    duration = _duration(result)
    fig, ax = plt.subplots(figsize=(7.2, 1.85), layout="constrained")
    env = _audio(result).get("wave_envelope")
    has_audio = _feat(result, "audio", "loudness_db") is not None
    if not isinstance(env, list) or len(env) < 8:
        env = _synth_envelope(result) if has_audio else []
    if not env:
        ax.text(0.5, 0.5, "暂无音轨", ha="center", va="center", fontproperties=font, color=MUTED)
        ax.set_axis_off()
        return _to_png(fig)
    ys = [max(0.0, float(v)) for v in env]
    xs = [duration * i / max(len(ys) - 1, 1) for i in range(len(ys))]
    ax.fill_between(xs, ys, [-v for v in ys], color=RED, linewidth=0, alpha=0.92, zorder=2)
    pauses = _audio(result).get("long_pause_times") or []
    shown = 0
    for t in pauses:
        try:
            sec = float(t)
        except (TypeError, ValueError):
            continue
        if sec < 0 or sec > duration:
            continue
        ax.axvline(sec, color="#c0c4cc", linestyle="--", linewidth=0.8, zorder=3)
        if shown < 6:
            ax.text(
                sec,
                1.16,
                f"长停顿 {_clock(sec)}",
                ha="center",
                va="bottom",
                fontsize=8,
                color=MUTED,
                fontproperties=font,
                clip_on=False,
            )
            shown += 1
    ax.set_xlim(0, duration)
    ax.set_ylim(-1.15, 1.42)
    ax.set_yticks([])
    ticks = [0, duration / 2, duration]
    ax.set_xticks(ticks)
    ax.set_xticklabels([_clock(t) for t in ticks], fontproperties=font, fontsize=8)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    return _to_png(fig)


def _nice_ceil(value: float, step: float) -> float:
    return math.ceil(value / step) * step


def _nice_floor(value: float, step: float) -> float:
    return math.floor(value / step) * step


def _pitch_axis(series: list[list[float]]) -> tuple[tuple[float, float], list[float]]:
    """默认 80–280 Hz（常见说话区间）；峰值或谷值超出则按数据撑开。"""
    ymin, ymax = 80.0, 280.0
    ys = [float(p[1]) for p in series if len(p) >= 2]
    if ys:
        lo, hi = min(ys), max(ys)
        if lo < ymin:
            ymin = max(0.0, _nice_floor(lo - 8, 20))
        if hi > ymax:
            ymax = _nice_ceil(hi * 1.08, 20 if hi < 400 else 50)
    span = ymax - ymin or 1
    ticks = [round(ymin), round(ymin + span / 2), round(ymax)]
    return (ymin, ymax), ticks


def _line_chart(result: dict[str, Any], series: list[list[float]], ylabel: str, ylim: tuple[float, float], yticks: list[float]) -> bytes:
    plt = _setup()
    font = _zh_font()
    duration = _duration(result)
    fig, ax = plt.subplots(figsize=(7.2, 1.85), layout="constrained")
    if not series:
        ax.text(0.5, 0.5, "暂无曲线", ha="center", va="center", fontproperties=font, color=MUTED)
        ax.set_axis_off()
        return _to_png(fig)
    xs = [float(p[0]) for p in series]
    ys = [float(p[1]) for p in series]
    ax.plot(xs, ys, color=RED, linewidth=1.6, zorder=2)
    ax.set_xlim(0, duration)
    ax.set_ylim(*ylim)
    ax.set_yticks(yticks)
    ticks = [0, duration / 2, duration]
    ax.set_xticks(ticks)
    ax.set_xticklabels([_clock(t) for t in ticks], fontproperties=font, fontsize=8)
    ax.set_ylabel(ylabel, fontproperties=font, fontsize=9, color=MUTED, labelpad=6)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=8, pad=3)
    return _to_png(fig)


def render_loudness_series(result: dict[str, Any]) -> bytes:
    series = _audio(result).get("loudness_curve")
    if not isinstance(series, list) or len(series) < 4:
        mean = _feat(result, "audio", "loudness_db")
        std = _feat(result, "audio", "loudness_std") or 4.0
        series = _synth_curve(mean or -22.0, std, _duration(result)) if mean is not None else []
    return _line_chart(result, series, "dB", (-60, 0), [0, -30, -60])


def render_pitch_series(result: dict[str, Any]) -> bytes:
    series = _audio(result).get("pitch_curve")
    if not isinstance(series, list) or len(series) < 4:
        mean = _feat(result, "audio", "pitch_median")
        std = _feat(result, "audio", "pitch_std") or 18.0
        series = _synth_curve(mean or 180.0, std, _duration(result)) if mean else []
    ylim, yticks = _pitch_axis(series)
    return _line_chart(result, series, "Hz", ylim, yticks)


def render_wait_samples(result: dict[str, Any]) -> bytes:
    plt = _setup()
    font = _zh_font()
    samples = _wait_samples(result)
    fig, ax = plt.subplots(figsize=(7.2, 1.45), layout="constrained")
    if not samples:
        ax.text(0.5, 0.5, "暂无逐次等待样本", ha="center", va="center", fontproperties=font, color=MUTED)
        ax.set_axis_off()
        return _to_png(fig)

    xs = list(range(1, len(samples) + 1))
    peak = max(samples)
    ymax = max(7.0, peak * 1.2)
    ax.axhspan(WAIT_GOOD[0], WAIT_GOOD[1], color=BAND, zorder=0)
    ax.vlines(xs, 0, samples, colors=RED, linewidth=1.4, zorder=1)
    ax.scatter(xs, samples, s=28, facecolors="white", edgecolors=RED, linewidths=1.5, zorder=2)
    labels = [f"Q{i}" for i in xs]
    if len(labels) > 12:
        labels = [lab if i % 2 == 0 or i == len(labels) - 1 else "" for i, lab in enumerate(labels)]
    ax.set_xlim(0.4, len(xs) + 0.6)
    ax.set_ylim(0, ymax)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontproperties=font, fontsize=8)
    ax.set_ylabel("秒", fontproperties=font, fontsize=9, color=MUTED, labelpad=6)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.text(
        len(xs) + 0.35,
        (WAIT_GOOD[0] + WAIT_GOOD[1]) / 2,
        "推荐区间 3-6秒",
        ha="right",
        va="center",
        color=BAND_EDGE,
        fontsize=8,
        fontproperties=font,
        clip_on=False,
    )
    return _to_png(fig)


CHARTS = {
    "audio_wave": render_audio_wave,
    "loudness_series": render_loudness_series,
    "pitch_series": render_pitch_series,
    "wait_samples": render_wait_samples,
}


def render_chart(name: str, result: dict[str, Any]) -> bytes:
    if name not in CHARTS:
        raise KeyError(name)
    return CHARTS[name](result)
