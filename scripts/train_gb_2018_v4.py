"""恢复 2018 v4 评分缓存，merge 后训原四路 + 客观特征 / 二级指标。

默认 cache/ 里的 scores.json 已被 v5 覆盖；证据仍在。
v4 分数从 eval_snapshots/v4/2018_spring/cache 拷到 cache_v4，
不调用当前 Judge（当前规则已是 v9，重打分不再是 v4）。

    python -m scripts.train_gb_2018_v4
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.config import ROOT as PROJ
from ai_engine.evaluation.gb_fit import CORE_KEYS, run_variant
from scripts.build_eval_dataset import cmd_merge
from scripts.compare_gb import compare

BATCH = PROJ / "dataset" / "2018_spring"
SNAPSHOT = PROJ / "dataset" / "eval_snapshots" / "v4" / "2018_spring" / "cache"
CACHE_V4 = "cache_v4"
OUT_DIR = BATCH / "v4"
SPLIT = BATCH / "gb_split.json"
MODELS = PROJ / "models" / "2018_v4"
KEYS = CORE_KEYS + ("obj_only_reg", "ind_reg")


def restore_v4_cache() -> int:
    src = SNAPSHOT
    if not src.is_dir():
        raise SystemExit(f"找不到 v4 快照 {src}")
    n = 0
    for person in sorted(p for p in src.iterdir() if p.is_dir()):
        src_scores = person / "scores.json"
        if not src_scores.exists():
            continue
        dest = BATCH / CACHE_V4 / person.name
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_scores, dest / "scores.json")
        n += 1
    print(f"已从快照恢复 {n} 份 v4 scores.json → {BATCH / CACHE_V4}")
    return n


def main() -> int:
    n = restore_v4_cache()
    if n < 5:
        raise SystemExit("恢复的 v4 分数太少，无法训练")

    class Args:
        dir = str(BATCH)
        scores_cache = CACHE_V4
        output_dir = str(OUT_DIR)

    print("merge 2018 v4 …")
    if cmd_merge(Args()) != 0:
        return 1

    data = OUT_DIR / "training_gb.csv"
    alignment = OUT_DIR / "alignment.csv"
    if not SPLIT.exists():
        raise SystemExit(f"找不到划分 {SPLIT}，不要在这里重划")
    for key in KEYS:
        run_variant(
            key,
            data=data,
            alignment=alignment,
            split_path=SPLIT,
            out_dir=MODELS,
            force_split=False,
            hold_year="within",
        )

    compare(
        MODELS,
        OUT_DIR / "gb_predictions.csv",
        title="2018 v4（快照恢复）",
        keys=KEYS,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
