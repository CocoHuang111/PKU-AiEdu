"""四年拼表后，在 v7.1 / v9 上各训用户指定的六种 GB，共用 2022 预测集。

六种方法为：五维回归、五维+客观特征回归、五维5分类、五维+客观特征5分类、
纯客观特征5分类、纯二级指标5分类。

各年 cache_v9 / cache_goal_effect_v7_1 已齐。先按年 merge，再拼总表。
batch 列用年份名（2018_spring），不是版本子目录名。

    python -m scripts.train_gb_all_v7_v9
"""
from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.config import ROOT as PROJ
from ai_engine.evaluation.gb_fit import SIX_KEYS, VARIANTS, run_variant
from scripts.build_eval_dataset import cmd_merge
from scripts.compare_gb import SHORT, compare
from scripts.eval_dataset.inventory import read_csv, write_csv

YEARS = ("2018_spring", "2019_spring", "2022_spring", "2024_spring")
SPLIT = PROJ / "dataset" / "gb_split.json"
SPLIT_SNAPSHOT = PROJ / "dataset" / "eval_snapshots" / "v4" / "global" / "gb_split.json"
CROSS_CSV = PROJ / "dataset" / "all_v7_1_vs_v9_gb.csv"
CROSS_JSON = PROJ / "dataset" / "all_v7_1_vs_v9_gb.json"

VERSIONS = (
    {
        "name": "v7.1",
        "scores_cache": "cache_goal_effect_v7_1",
        "year_subdir": "goal_effect_v7_1",
        "combine_dir": PROJ / "dataset" / "all_v7_1",
        "out_dir": PROJ / "models" / "all_v7_1",
        "pred_csv": PROJ / "dataset" / "all_v7_1" / "gb_predictions.csv",
        "title": "四年 v7.1（2022 留出）",
    },
    {
        "name": "v9",
        "scores_cache": "cache_v9",
        "year_subdir": "v9",
        "combine_dir": PROJ / "dataset" / "all_v9",
        "out_dir": PROJ / "models" / "all_v9",
        "pred_csv": PROJ / "dataset" / "all_v9" / "gb_predictions.csv",
        "title": "四年 v9（2022 留出）",
    },
)


def _ensure_split() -> None:
    if SPLIT.exists():
        print(f"沿用划分 {SPLIT}")
        return
    if not SPLIT_SNAPSHOT.exists():
        raise SystemExit(f"找不到四年划分 {SPLIT} 和快照 {SPLIT_SNAPSHOT}")
    SPLIT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SPLIT_SNAPSHOT, SPLIT)
    print(f"从快照恢复划分 {SPLIT}")


def _merge_year(year: str, cache_name: str, subdir: str) -> Path:
    out = PROJ / "dataset" / year / subdir

    class Args:
        dir = str(PROJ / "dataset" / year)
        scores_cache = cache_name
        output_dir = str(out)

    print(f"merge {year} ← {cache_name} → {out}")
    if cmd_merge(Args()) != 0:
        raise SystemExit(f"merge {year} {scores_cache} 失败")
    return out


def _combine(year_subdir: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    versions: set[str] = set()
    for kind in ("training_gb", "training_detail", "alignment"):
        rows: list[dict] = []
        for year in YEARS:
            path = PROJ / "dataset" / year / year_subdir / f"{kind}.csv"
            if not path.exists():
                raise SystemExit(f"缺 {path}，请先 merge")
            for row in read_csv(path):
                rec = dict(row)
                rec["batch"] = year
                if rec.get("prompt_version"):
                    versions.add(rec["prompt_version"])
                rows.append(rec)
        write_csv(dest / f"{kind}.csv", rows)
        print(f"combine {len(rows)} 条 → {dest / (kind + '.csv')}")
    print(f"prompt_version={sorted(versions)}")


def _print_cross(summaries: list[tuple[str, dict]]) -> None:
    print("\n" + "=" * 72)
    print("四年 v7.1 vs v9（MAE 0–5；预测集=2022 留出 14 人）")
    print("=" * 72)
    names = [s[0] for s in summaries]
    print(f"{'':<16}" + "".join(f" {n:>14}" for n in names))
    print(
        f"{'Judge':<16}"
        + "".join(f" {s[1].get('judge_mae', float('nan')):14.3f}" for s in summaries)
    )
    rows = []
    for key in SIX_KEYS:
        title = SHORT.get(key, key)
        rec = {"variant": key, "title": VARIANTS[key]["title"]}
        cells = []
        for name, summary in summaries:
            mae = summary[key]["mae"]
            cells.append(f"{mae:14.3f}")
            rec[f"mae_{name}"] = mae
            rec[f"rmse_{name}"] = summary[key]["rmse"]
            rec[f"acc_{name}"] = summary[key]["acc"]
        print(f"{title:<16}" + "".join(f" {c}" for c in cells))
        rows.append(rec)
    with CROSS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    CROSS_JSON.write_text(
        json.dumps(
            {
                "test_ids": summaries[0][1].get("test_ids"),
                "summaries": {name: s for name, s in summaries},
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n对照表 {CROSS_CSV}")


def main() -> int:
    _ensure_split()
    summaries: list[tuple[str, dict]] = []
    for ver in VERSIONS:
        print("\n" + "=" * 72)
        print(ver["title"])
        print("=" * 72)
        for year in YEARS:
            _merge_year(year, ver["scores_cache"], ver["year_subdir"])
        _combine(ver["year_subdir"], ver["combine_dir"])
        for key in SIX_KEYS:
            run_variant(
                key,
                data=ver["combine_dir"] / "training_gb.csv",
                alignment=ver["combine_dir"] / "alignment.csv",
                split_path=SPLIT,
                out_dir=ver["out_dir"],
                force_split=False,
                hold_year="2022_spring",
            )
        summaries.append(
            (
                ver["name"],
                compare(
                    ver["out_dir"],
                    ver["pred_csv"],
                    title=ver["title"],
                    keys=SIX_KEYS,
                ),
            )
        )
    _print_cross(summaries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
