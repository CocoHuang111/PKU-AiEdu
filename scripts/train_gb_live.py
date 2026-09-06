"""用四年 v9 全量「客观特征+五维」训线上 5 分类 GB。

先在 2022 留出上对照，再把 103 人全部拟合到 models/live。

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

V9_ALL = PROJ / "dataset" / "all_v9" / "training_gb.csv"
V9_ALIGN = PROJ / "dataset" / "all_v9" / "alignment.csv"
SPLIT = PROJ / "dataset" / "gb_split.json"
HOLDOUT_DIR = PROJ / "models" / "all_v9"
HOLDOUT_PRED = PROJ / "dataset" / "all_v9" / "gb_live_holdout.csv"


def main() -> int:
    if not V9_ALL.exists():
        raise SystemExit(f"找不到 {V9_ALL}。请先运行 make train-gb-all-v7-v9")
    if not SPLIT.exists():
        raise SystemExit(f"找不到 {SPLIT}")

    print("=" * 60)
    print("四年 v9：客观特征+五维 5 分类（2022 留出，只作对照）")
    print("=" * 60)
    holdout = run_variant(
        LIVE_VARIANT,
        data=V9_ALL,
        alignment=V9_ALIGN if V9_ALIGN.exists() else None,
        split_path=SPLIT,
        out_dir=HOLDOUT_DIR,
        hold_year="2022_spring",
    )
    compare(
        HOLDOUT_DIR,
        HOLDOUT_PRED,
        title="四年 v9 客+五 5分类（2022 留出）",
        keys=(LIVE_VARIANT,),
    )

    print("\n" + "=" * 60)
    print("四年 v9 全量：客观特征+五维 5 分类 → 线上模型")
    print("=" * 60)
    live = run_variant(
        LIVE_VARIANT,
        data=V9_ALL,
        alignment=V9_ALIGN if V9_ALIGN.exists() else None,
        split_path=SPLIT,
        out_dir=LIVE_GB_DIR,
        fit_all=True,
    )
    mae4 = holdout["mae_5"] * 4 / 5
    print(
        f"\n线上模型 {LIVE_GB_DIR / f'gb_{LIVE_VARIANT}.pkl'}"
        f"（全量 n={live['n_train']}，留出 MAE 0–5={holdout['mae_5']:.3f} / 4分制={mae4:.3f}）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
