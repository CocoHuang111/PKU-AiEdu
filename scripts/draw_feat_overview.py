"""画出客观特征总览四张卡里的示意图，供前端对照。

语速折线和切换点用真实统计；波形没有音轨采样，按响度/静音/信噪比生成示意。
前端 Evaluation.vue 用同一套规则现场画，本脚本只生成可对照的 SVG。

    python scripts/draw_feat_overview.py --out design-mockups/objective-feature-four-groups
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def pace_chart(
    points: list[tuple[float, float]], duration_sec: float, width: int = 320, height: int = 112
) -> str:
    left, top, bottom = 28, 8, 22
    inner_w = width - left - 8
    inner_h = height - top - bottom
    t_max = max(duration_sec, max((t for t, _ in points), default=1), 1)
    v_max = max(300.0, max((v for _, v in points), default=0))

    def x_of(t: float) -> float:
        return left + t / t_max * inner_w

    def y_of(v: float) -> float:
        return top + (1 - v / v_max) * inner_h

    dots = [(x_of(t), y_of(v)) for t, v in points]
    path = " ".join(
        f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(dots)
    )
    mins = max(1, round(t_max / 60))
    y_ticks = [0, round(v_max / 2), round(v_max)]
    ticks = "".join(
        f'<text x="{left - 4}" y="{y_of(v) + 3:.1f}" text-anchor="end" '
        f'fill="#b0b3b8" font-size="9">{v}</text>'
        for v in y_ticks
    )
    circles = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#a61b1b"/>' for x, y in dots
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <line x1="{left}" y1="{height - bottom}" x2="{width - 8}" y2="{height - bottom}" stroke="#ececec"/>
  <line x1="{left}" y1="8" x2="{left}" y2="{height - bottom}" stroke="#ececec"/>
  {ticks}
  <text x="{left}" y="{height - 4}" fill="#b0b3b8" font-size="9">0</text>
  <text x="{left + inner_w / 2:.1f}" y="{height - 4}" text-anchor="middle" fill="#b0b3b8" font-size="9">{round(mins / 2)}</text>
  <text x="{width - 8}" y="{height - 4}" text-anchor="end" fill="#b0b3b8" font-size="9">{mins}</text>
  <path d="{path}" fill="none" stroke="#a61b1b" stroke-width="1.8"/>
  {circles}
</svg>
"""


def wave_chart(
    loud: float = -22.4, silence: float = 14.0, snr: float = 20.8, width: int = 320, height: int = 72
) -> str:
    mid = height / 2
    seed = abs(loud)
    energy = min(1.0, max(0.28, (abs(loud) + 45) / 50))
    quiet = min(0.55, silence / 100)
    jitter = min(1.2, max(0.6, snr / 22))
    n = 96
    coords = []
    for i in range(n + 1):
        x = i / n * width
        t = i / n * math.pi * 12 + seed * 0.17
        envelope = math.sin(i / n * math.pi) * (1 - quiet * 0.65)
        wiggle = math.sin(t) * 0.55 + math.sin(t * 2.15) * 0.28 + math.sin(t * 0.4 + seed) * 0.18
        y = mid - envelope * energy * 30 * (0.35 + abs(wiggle) * jitter)
        coords.append((x, y))
    path = " ".join(
        f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(coords)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <path d="{path}" fill="none" stroke="#a61b1b" stroke-width="1.6"/>
</svg>
"""


def gaze_bar(parts: list[tuple[str, float, str]], width: int = 320, height: int = 48) -> str:
    total = sum(p for _, p, _ in parts) or 1
    x = 0.0
    segs = []
    legends = []
    lx = 0
    for label, pct, color in parts:
        w = width * (pct / total)
        segs.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="10" fill="{color}"/>')
        legends.append(
            f'<circle cx="{lx + 4}" cy="28" r="4" fill="{color}"/>'
            f'<text x="{lx + 12}" y="32" fill="#8a8a8a" font-size="11">{label} {pct:g}%</text>'
        )
        x += w
        lx += 78
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {''.join(segs)}
  {''.join(legends)}
</svg>
"""


def slide_dots(
    times: list[float], duration_sec: float, width: int = 320, height: int = 64
) -> str:
    dur = duration_sec if duration_sec > 0 else 1
    pcts = [min(98, max(2, t / dur * 100)) for t in times]
    mins = max(1, round(dur / 60))
    marks = "".join(
        f'<circle cx="{p / 100 * width:.1f}" cy="22" r="4" fill="#a61b1b"/>' for p in pcts
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <line x1="0" y1="22" x2="{width}" y2="22" stroke="#ececec" stroke-width="2"/>
  {marks}
  <text x="0" y="{height - 4}" fill="#b0b3b8" font-size="11">0</text>
  <text x="{width / 2:.1f}" y="{height - 4}" text-anchor="middle" fill="#b0b3b8" font-size="11">{round(mins / 2)}</text>
  <text x="{width}" y="{height - 4}" text-anchor="end" fill="#b0b3b8" font-size="11">{mins}</text>
</svg>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="生成客观特征总览示意图 SVG")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("design-mockups/objective-feature-four-groups"),
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pace = [
        (0, 210),
        (300, 228),
        (600, 246),
        (900, 236),
        (1200, 252),
        (1500, 241),
        (1800, 258),
        (2100, 233),
        (2400, 248),
        (2700, 229),
    ]
    (args.out / "pace-line.svg").write_text(
        pace_chart(pace, 2700), encoding="utf-8"
    )
    (args.out / "audio-wave.svg").write_text(wave_chart(), encoding="utf-8")
    (args.out / "vision-gaze.svg").write_text(
        gaze_bar(
            [
                ("看学生", 58, "#a61b1b"),
                ("看讲稿", 17, "#e6a23c"),
                ("看屏幕", 21, "#67c23a"),
                ("无法判断", 4, "#c0c4cc"),
            ]
        ),
        encoding="utf-8",
    )
    (args.out / "tools-dots.svg").write_text(
        slide_dots([120, 280, 510, 760, 990, 1320, 1680, 2010, 2340, 2580], 2700),
        encoding="utf-8",
    )
    print(f"wrote 4 svgs to {args.out}")


if __name__ == "__main__":
    main()
