"""用 matplotlib 画出授课内容页的语速折线和提问条。

默认用稿子上的示意数据；传 --from-task 则读评估结果 JSON。

    python scripts/draw_pace_page.py
    python scripts/draw_pace_page.py --from-task data/demo_result.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_engine.evaluation.pace_charts import render_chart


def _demo_result() -> dict:
    segs = []
    rates = [210, 228, 246, 236, 252, 241, 258, 233, 229]
    for i, rate in enumerate(rates):
        start = i * 300
        segs.append(
            {
                "start_sec": start,
                "end_sec": start + 300,
                "features": {"speech_rate": rate},
            }
        )
    return {
        "transcript": {"segments": segs},
        "objective_features": {
            "text": [
                {"key": "open_question_ratio", "value": 44},
                {"key": "higher_order_question_ratio", "value": 38},
                {"key": "question_free_segment_ratio", "value": 12.5},
            ]
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="生成授课内容页图表 PNG")
    parser.add_argument("--out", type=Path, default=Path("design-mockups/pace-page"))
    parser.add_argument("--from-task", type=Path, default=None, help="评估结果 JSON")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result = json.loads(args.from_task.read_text(encoding="utf-8")) if args.from_task else _demo_result()
    for name in ("speech_rate", "question_structure"):
        (args.out / f"{name}.png").write_bytes(render_chart(name, result))
    print(f"wrote speech_rate.png question_structure.png to {args.out}")


if __name__ == "__main__":
    main()
