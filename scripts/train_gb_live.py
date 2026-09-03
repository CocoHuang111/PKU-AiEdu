"""用 2018 v9 全量五维训线上 5 分类 GB，并顺带写出年内留出对照。

    python -m scripts.train_gb_live
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.config import ROOT as PROJ
from ai_engine.evaluation.gb import LIVE_GB_DIR, LIVE_VARIANT
from ai_engine.evaluation.gb_fit import run_variant
from scripts.compare_gb import compare

V9_DATA = PROJ / "dataset" / "2018_spring" / "v9" / "training_gb.csv"
V9_ALIGN = PROJ / "dataset" / "2018_spring" / "v9" / "alignment.csv"
V9_SPLIT = PROJ / "dataset" / "2018_spring" / "gb_split.json"
HOLDOUT_DIR = PROJ / "models" / "2018_v9"
HOLDOUT_PRED = PROJ / "dataset" / "2018_spring" / "v9" / "gb_predictions.csv"


def main() -> int:
    print("=" * 60)
    print("2018 v9 年内留出：五维 5 分类（只作对照，不接线上）")
    print("=" * 60)
    holdout = run_variant(
        LIVE_VARIANT,
        data=V9_DATA,
        alignment=V9_ALIGN if V9_ALIGN.exists() else None,
        split_path=V9_SPLIT,
        out_dir=HOLDOUT_DIR,
        hold_year="within",
    )
    compare(
        HOLDOUT_DIR,
        HOLDOUT_PRED,
        title="2018 v9 五维5分类（年内留出）",
        keys=(LIVE_VARIANT,),
    )

    print("\n" + "=" * 60)
    print("2018 v9 全量：五维 5 分类 → 线上模型")
    print("=" * 60)
    live = run_variant(
        LIVE_VARIANT,
        data=V9_DATA,
        alignment=V9_ALIGN if V9_ALIGN.exists() else None,
        split_path=V9_SPLIT,
        out_dir=LIVE_GB_DIR,
        fit_all=True,
    )
    print(
        f"\n线上模型 {LIVE_GB_DIR / f'gb_{LIVE_VARIANT}.pkl'}"
        f"（全量 n={live['n_train']}，留出对照 MAE={holdout['mae_5']:.3f}）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
