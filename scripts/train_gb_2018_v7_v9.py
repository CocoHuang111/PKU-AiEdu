"""在 2018 v7.1 / v9 上各训六种 GB，共用年内划分后对照。

v9 / v7.1 旧 training_gb.csv 没有二级指标列，这里先按对应缓存重新 merge。

    python -m scripts.train_gb_2018_v7_v9
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.config import ROOT as PROJ
from ai_engine.evaluation.gb_fit import SIX_KEYS, VARIANTS, run_variant
from scripts.build_eval_dataset import cmd_merge
from scripts.compare_gb import SHORT, compare

BATCH = PROJ / "dataset" / "2018_spring"
SPLIT = BATCH / "gb_split.json"
CROSS_CSV = BATCH / "v7_1_vs_v9_gb.csv"
CROSS_JSON = BATCH / "v7_1_vs_v9_gb.json"

BATCHES = (
    {
        "name": "v7.1",
        "scores_cache": "cache_goal_effect_v7_1",
        "output_dir": BATCH / "goal_effect_v7_1",
        "out_dir": PROJ / "models" / "2018_goal_effect_v7_1",
        "pred_csv": BATCH / "goal_effect_v7_1" / "gb_predictions.csv",
        "title": "2018 v7.1（goal-effect-fallback）",
    },
    {
        "name": "v9",
        "scores_cache": "cache_v9",
        "output_dir": BATCH / "v9",
        "out_dir": PROJ / "models" / "2018_v9",
        "pred_csv": BATCH / "v9" / "gb_predictions.csv",
        "title": "2018 v9（calibrated）",
    },
)


def _merge(batch: dict) -> None:
    class Args:
        dir = str(BATCH)
        scores_cache = batch["scores_cache"]
        output_dir = str(batch["output_dir"])

    print(f"merge {batch['name']} ← {batch['scores_cache']}")
    if cmd_merge(Args()) != 0:
        raise SystemExit(f"merge {batch['name']} 失败")


def _print_cross(summaries: list[tuple[str, dict]]) -> dict:
    print("\n" + "=" * 72)
    print("v7.1 vs v9（MAE 0–5，越小越好；同一 5 人预测集）")
    print("=" * 72)
    names = [s[0] for s in summaries]
    header = f"{'':<16}" + "".join(f" {n:>14}" for n in names)
    print(header)
    print(f"{'Judge':<16}" + "".join(f" {s[1].get('judge_mae', float('nan')):14.3f}" for s in summaries))
    rows = []
    for key in SIX_KEYS:
        title = SHORT.get(key, key)
        cells = []
        rec = {"variant": key, "title": VARIANTS[key]["title"]}
        for name, summary in summaries:
            mae = summary[key]["mae"]
            cells.append(f"{mae:14.3f}")
            rec[f"mae_{name}"] = mae
            rec[f"rmse_{name}"] = summary[key]["rmse"]
            rec[f"acc_{name}"] = summary[key]["acc"]
        print(f"{title:<16}" + "".join(f" {c}" for c in cells))
        rows.append(rec)

    CROSS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with CROSS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    payload = {
        "test_ids": summaries[0][1].get("test_ids"),
        "summaries": {name: s for name, s in summaries},
        "rows": rows,
    }
    CROSS_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n对照表 {CROSS_CSV}")
    return payload


def main() -> int:
    if not SPLIT.exists():
        raise SystemExit(f"找不到划分 {SPLIT}，不要在这里重划")

    summaries: list[tuple[str, dict]] = []
    for batch in BATCHES:
        print("\n" + "=" * 72)
        print(batch["title"])
        print("=" * 72)
        _merge(batch)
        data = batch["output_dir"] / "training_gb.csv"
        alignment = batch["output_dir"] / "alignment.csv"
        for key in SIX_KEYS:
            run_variant(
                key,
                data=data,
                alignment=alignment,
                split_path=SPLIT,
                out_dir=batch["out_dir"],
                force_split=False,
                hold_year="within",
            )
        summaries.append(
            (
                batch["name"],
                compare(
                    batch["out_dir"],
                    batch["pred_csv"],
                    title=batch["title"],
                    keys=SIX_KEYS,
                ),
            )
        )

    _print_cross(summaries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
