"""导出全样本五维、四个 GB 总分与专家分对照。"""
from __future__ import annotations

import argparse
import csv
import json
import pickle
from pathlib import Path

from ai_engine.evaluation.gb import (
    SCORE_MAPPING_VERSION,
    avg_to_score5,
    clip_score5,
    label_to_score5,
    score100_to_score5,
)
from ai_engine.evaluation.gb_fit import CORE_KEYS, VARIANTS, _prepare_X, load_table

DIMENSIONS = (
    ("llm_dim_teaching_attitude", "教学态度"),
    ("llm_dim_teaching_content", "教学内容"),
    ("llm_dim_teaching_method", "教学方法"),
    ("llm_dim_teaching_effect", "教学效果"),
    ("llm_dim_teaching_quality", "教学素质"),
)


def _alignment(path: Path) -> dict[str, float]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {
            row["video_id"]: float(row["llm_overall"])
            for row in csv.DictReader(f)
            if row.get("llm_overall")
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--alignment", type=Path, required=True)
    parser.add_argument("--split", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    df = load_table(args.data)
    split = json.loads(args.split.read_text(encoding="utf-8"))
    test_ids = {str(x) for x in split.get("test_ids") or []}
    judge = _alignment(args.alignment)
    predictions: dict[str, list[float]] = {}

    for key in CORE_KEYS:
        config = VARIANTS[key]
        with (args.model_dir / f"gb_{key}.pkl").open("rb") as f:
            bundle = pickle.load(f)
        if bundle.get("score_mapping_version") != SCORE_MAPPING_VERSION:
            raise SystemExit(f"{key} 是旧分制模型，请重新训练")
        X, _, _ = _prepare_X(df, config["features"])
        expected = list(bundle["feature_names"])
        missing = [name for name in expected if name not in X.columns]
        if missing:
            raise SystemExit(f"{key} 缺模型特征：{missing}")
        raw = bundle["pipeline"].predict(X[expected])
        if config["task"] == "classify":
            values = [label_to_score5(int(v), step=float(bundle["step"])) for v in raw]
        else:
            values = [clip_score5(float(v)) for v in raw]
        predictions[key] = values

    rows = []
    for i, source in df.iterrows():
        video_id = str(source["video_id"])
        expert_avg = float(source["expert_avg"])
        expert5 = avg_to_score5(expert_avg)
        row = {
            "video_id": video_id,
            "split": "test" if video_id in test_ids else "train",
            **{label: source[key] for key, label in DIMENSIONS},
            "Judge总分_5": round(score100_to_score5(judge[video_id]), 4),
            "客观特征加五维回归_5": round(predictions["obj_reg"][i], 4),
            "五维回归_5": round(predictions["llm_reg"][i], 4),
            "五维5分类_5": round(predictions["llm_cls5"][i], 4),
            "五维8分类_5": round(predictions["llm_cls8"][i], 4),
            "专家原分_4": round(expert_avg, 4),
            "专家等值分_5": round(expert5, 4),
            "专家百分制": round(float(source["expert_total_100"]), 2),
            "score_mapping_version": SCORE_MAPPING_VERSION,
        }
        rows.append(row)

    rows.sort(key=lambda row: (row["split"] != "test", row["video_id"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"导出 {len(rows)} 人 → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
