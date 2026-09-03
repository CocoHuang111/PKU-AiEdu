"""在 2018 的 fixed_prompt / effect_inferred 两套表上训四种 GB，共用同一划分。

    python -m scripts.train_gb_2018_prompts
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.config import ROOT as PROJ
from ai_engine.evaluation.gb_fit import VARIANTS, run_variant
from scripts.compare_gb import compare

SPLIT = PROJ / "dataset" / "2018_spring" / "gb_split.json"
BATCHES = (
    {
        "name": "fixed_prompt",
        "data": PROJ / "dataset" / "2018_spring" / "fixed_prompt" / "training_gb.csv",
        "alignment": PROJ / "dataset" / "2018_spring" / "fixed_prompt" / "alignment.csv",
        "out_dir": PROJ / "models" / "2018_fixed_prompt",
        "pred_csv": PROJ / "dataset" / "2018_spring" / "fixed_prompt" / "gb_predictions.csv",
        "title": "2018 fixed_prompt（v5-rules17）",
    },
    {
        "name": "effect_inferred",
        "data": PROJ / "dataset" / "2018_spring" / "effect_inferred" / "training_gb.csv",
        "alignment": PROJ / "dataset" / "2018_spring" / "effect_inferred" / "alignment.csv",
        "out_dir": PROJ / "models" / "2018_effect_inferred",
        "pred_csv": PROJ / "dataset" / "2018_spring" / "effect_inferred" / "gb_predictions.csv",
        "title": "2018 effect_inferred（v6）",
    },
)


def main() -> int:
    first = True
    summaries = []
    for batch in BATCHES:
        print("\n" + "=" * 60)
        print(batch["title"])
        print("=" * 60)
        for key in VARIANTS:
            run_variant(
                key,
                data=batch["data"],
                alignment=batch["alignment"],
                split_path=SPLIT,
                out_dir=batch["out_dir"],
                force_split=first,
                hold_year="within",
            )
            first = False
        summaries.append(
            (batch["title"], compare(batch["out_dir"], batch["pred_csv"], title=batch["title"]))
        )

    print("\n" + "=" * 60)
    print("两套 prompt 对照（MAE 0–5，越小越好）")
    print("=" * 60)
    print(f"{'':<22} {'Judge':>7} {'客+五回归':>8} {'五维回归':>8} {'五维5类':>8} {'五维8类':>8}")
    for title, s in summaries:
        row = [
            f"{title:<22}",
            f"{s.get('judge_mae', float('nan')):7.3f}",
        ]
        for key in VARIANTS:
            row.append(f"{s[key]['mae']:8.3f}")
        print(" ".join(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
