"""用 matplotlib 画出声学特征页的波形、响度和基频。

默认用稿子上的示意数据；传 --from-task 则读评估结果 JSON。

    python scripts/draw_audio_page.py
    python scripts/draw_audio_page.py --from-task data/demo_result.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_engine.evaluation.audio_charts import CHARTS


def _demo_result() -> dict:
    duration = 21 * 60 + 18
    n = 360
    env = []
    for i in range(n):
        t = i / n
        bump = 0.55 + 0.45 * abs(math.sin(t * 12.6)) * (0.35 + abs(math.sin(t * 3.1)))
        quiet = 0.12 if (0.18 < t < 0.22) or (0.57 < t < 0.62) or (0.83 < t < 0.88) else 1.0
        env.append(round(min(1.0, bump * quiet), 4))
    loud = []
    pitch = []
    for i in range(90):
        t = duration * i / 89
        wobble = math.sin(i / 90 * 6.2)
        loud.append([round(t, 1), round(-22.4 + 6.5 * wobble, 1)])
        pitch.append([round(t, 1), round(176 + 22 * math.sin(i / 90 * 4.8), 1)])
    return {
        "overall": {"duration_minutes": round(duration / 60, 1)},
        "raw_features": {
            "audio": {
                "audio_duration_sec": duration,
                "loudness_db": -22.4,
                "loudness_std": 4.2,
                "snr_estimate": 20.8,
                "silence_ratio": 14.0,
                "pitch_median": 176,
                "pitch_std": 18,
                "wave_envelope": env,
                "loudness_curve": loud,
                "pitch_curve": pitch,
                "long_pause_times": [253, 747, 1076],
            },
        },
        "objective_features": {
            "audio": [
                {"key": "loudness_db", "value": -22.4},
                {"key": "snr_estimate", "value": 20.8},
                {"key": "pitch_median", "value": 176},
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="生成声学特征页图表 PNG")
    parser.add_argument("--out", type=Path, default=Path("design-mockups/audio-page"))
    parser.add_argument("--from-task", type=Path, default=None, help="评估结果 JSON")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result = json.loads(args.from_task.read_text(encoding="utf-8")) if args.from_task else _demo_result()
    names = []
    for name, fn in CHARTS.items():
        (args.out / f"{name}.png").write_bytes(fn(result))
        names.append(f"{name}.png")
    print(f"wrote {' '.join(names)} to {args.out}")


if __name__ == "__main__":
    main()
