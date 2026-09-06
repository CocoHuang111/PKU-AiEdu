"""比较四个 GB 在同一预测集上的结果。

    python -m scripts.compare_gb
    python -m scripts.compare_gb --pred-dir models/2018_fixed_prompt \\
        --out dataset/2018_spring/fixed_prompt/gb_predictions.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.config import ROOT as PROJ
from ai_engine.evaluation.gb import SCORE_MAPPING_VERSION
from ai_engine.evaluation.gb_fit import VARIANTS

DEFAULT_KEYS = ("obj_reg", "llm_reg", "llm_cls5", "llm_cls8")
SHORT = {
    "obj_reg": "客+五回归",
    "llm_reg": "五维回归",
    "llm_cls5": "五维5类",
    "llm_cls8": "五维8类",
    "obj_cls5": "客+五5类",
    "obj_only_cls5": "客观5类",
    "ind_cls5": "二级5类",
    "obj_only_reg": "客观回归",
    "ind_reg": "二级回归",
}


def _mae(a, b) -> float:
    err = [abs(x - y) for x, y in zip(a, b)]
    return sum(err) / len(err) if err else float("nan")


def _rmse(a, b) -> float:
    err = [(x - y) ** 2 for x, y in zip(a, b)]
    return math.sqrt(sum(err) / len(err)) if err else float("nan")


def _load_pred(pred_dir: Path, key: str) -> dict[str, dict]:
    path = pred_dir / f"gb_{key}_pred.csv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return {r["video_id"]: r for r in csv.DictReader(f)}


def compare(
    pred_dir: Path,
    out_csv: Path,
    title: str = "",
    keys: tuple[str, ...] | list[str] = DEFAULT_KEYS,
) -> dict:
    keys = tuple(keys)
    unknown = [k for k in keys if k not in VARIANTS]
    if unknown:
        raise SystemExit(f"未知实验：{', '.join(unknown)}")
    tables = {k: _load_pred(pred_dir, k) for k in keys}
    missing = [k for k, t in tables.items() if not t]
    if missing:
        raise SystemExit(f"还没有预测文件：{', '.join(missing)}。目录 {pred_dir}")
    stale = [
        k
        for k, table in tables.items()
        if any(r.get("score_mapping_version") != SCORE_MAPPING_VERSION for r in table.values())
    ]
    if stale:
        raise SystemExit(
            "检测到旧专家分制预测，不能与修正后的标签混用："
            f"{', '.join(stale)}。请重新训练四个 GB。"
        )

    ids = list(tables[keys[0]].keys())
    for k in keys[1:]:
        if list(tables[k].keys()) != ids:
            print(f"警告：{k} 的预测集 id 与 {keys[0]} 不一致，将按 {keys[0]} 对齐")
            ids = [i for i in ids if i in tables[k]]

    expert = [float(tables[keys[0]][i]["expert_score_5"]) for i in ids]
    judge_raw = [tables[keys[0]][i].get("llm_overall_5") or "" for i in ids]
    judge = [float(v) for v in judge_raw if v != ""]
    expert_j = [
        float(tables[keys[0]][ids[n]]["expert_score_5"])
        for n, v in enumerate(judge_raw)
        if v != ""
    ]

    head = title or "同一预测集"
    print(f"\n{head} n={len(ids)}（分数为 0–5）\n")
    print(f"{'模型':<18} {'MAE':>7} {'RMSE':>7} {'Acc':>7} {'相对Judge MAE':>14}")
    print("-" * 58)

    rows_out = []
    judge_mae = _mae(expert_j, judge) if judge else float("nan")
    if judge:
        print(
            f"{'Judge 总分':<18} {judge_mae:7.3f} {_rmse(expert_j, judge):7.3f} "
            f"{'—':>7} {'(基线)':>14}"
        )

    summary: dict = {
        "n_test": len(ids),
        "test_ids": ids,
        "score_mapping_version": SCORE_MAPPING_VERSION,
    }
    if judge:
        summary["judge_mae"] = round(judge_mae, 3)
        summary["judge_rmse"] = round(_rmse(expert_j, judge), 3)
    for key in keys:
        pred = [float(tables[key][i]["pred_5"]) for i in ids]
        mae = _mae(expert, pred)
        rmse = _rmse(expert, pred)
        acc = ""
        true_l = [tables[key][i].get("true_label") or "" for i in ids]
        pred_l = [tables[key][i].get("pred_label") or "" for i in ids]
        if all(true_l) and all(x != "" for x in pred_l):
            acc_v = sum(int(a) == int(b) for a, b in zip(true_l, pred_l)) / len(ids)
            acc = f"{acc_v:.3f}"
        delta = f"{mae - judge_mae:+.3f}" if judge else ""
        print(f"{VARIANTS[key]['title']:<18} {mae:7.3f} {rmse:7.3f} {acc:>7} {delta:>14}")
        summary[key] = {"mae": round(mae, 3), "rmse": round(rmse, 3), "acc": acc}

    print("\n逐人预测（0–5 分）：")
    header = f"{'video_id':<10} {'专家':>6} {'Judge':>6}"
    for key in keys:
        header += f" {SHORT.get(key, key):>8}"
    print(header)
    for i in ids:
        r0 = tables[keys[0]][i]
        j = r0.get("llm_overall_5") or "—"
        line = {
            "video_id": i,
            "score_mapping_version": SCORE_MAPPING_VERSION,
            "expert_avg": r0.get("expert_avg") or "",
            "expert_score_5": r0["expert_score_5"],
            "llm_overall_5": r0.get("llm_overall_5") or "",
        }
        cells = [
            f"{i:<10}",
            f"{float(r0['expert_score_5']):6.2f}",
            f"{float(j):6.2f}" if j not in ("—", "") else f"{'—':>6}",
        ]
        for key in keys:
            p = float(tables[key][i]["pred_5"])
            cells.append(f"{p:8.2f}")
            line[f"pred_{key}"] = round(p, 4)
        print(" ".join(cells))
        rows_out.append(line)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows_out)
    print(f"\n宽表已写 {out_csv}")
    (pred_dir / "gb_compare.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description="比较四个 GB 在同一预测集上的结果")
    ap.add_argument("--pred-dir", default=str(PROJ / "models"))
    ap.add_argument("--out", default=str(PROJ / "dataset" / "gb_predictions.csv"))
    ap.add_argument("--title", default="")
    ap.add_argument(
        "--keys",
        default=",".join(DEFAULT_KEYS),
        help="逗号分隔的实验 key，默认原来的四个",
    )
    args = ap.parse_args()
    keys = tuple(k.strip() for k in args.keys.split(",") if k.strip())
    compare(Path(args.pred_dir), Path(args.out), title=args.title, keys=keys)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
