"""Run four isolated v9 regression experiments without touching production models.

    python -m scripts.train_gb_regression_experiments
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import LeaveOneGroupOut, RepeatedStratifiedKFold

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.evaluation.gb import AVG_COL, GROUP_COL, ID_COL, avg_to_score5
from ai_engine.evaluation.gb_fit import _select, drop_invalid, load_table, make_or_load_split
from ai_engine.evaluation.regression_experiments import experiment_estimators


DATA = ROOT / "dataset" / "all_v9" / "training_gb.csv"
SPLIT = ROOT / "dataset" / "gb_split.json"
MODEL_DIR = ROOT / "models" / "all_v9_regression_experiments"
RESULT_DIR = ROOT / "dataset" / "all_v9" / "regression_experiments"


def _mae(y, pred) -> float:
    return float(np.mean(np.abs(np.asarray(y, dtype=float) - np.asarray(pred, dtype=float))))


def _rmse(y, pred) -> float:
    return float(math.sqrt(np.mean((np.asarray(y, dtype=float) - np.asarray(pred, dtype=float)) ** 2)))


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _repeated_cv(estimator, X, y, *, seed: int, repeats: int) -> dict:
    bins = pd.qcut(pd.Series(y), q=5, labels=False, duplicates="drop").astype(int).to_numpy()
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=repeats, random_state=seed)
    fold_mae: list[float] = []
    fold_rmse: list[float] = []
    for train_idx, test_idx in cv.split(X, bins):
        model = clone(estimator)
        model.fit(X.iloc[train_idx], y[train_idx])
        pred = np.clip(model.predict(X.iloc[test_idx]), 0.0, 5.0)
        fold_mae.append(_mae(y[test_idx], pred))
        fold_rmse.append(_rmse(y[test_idx], pred))
    return {
        "folds": len(fold_mae),
        "mae_mean": round(float(np.mean(fold_mae)), 4),
        "mae_std": round(float(np.std(fold_mae, ddof=1)), 4),
        "rmse_mean": round(float(np.mean(fold_rmse)), 4),
        "rmse_std": round(float(np.std(fold_rmse, ddof=1)), 4),
    }


def _batch_holdout(estimator, X, y, groups) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for train_idx, test_idx in LeaveOneGroupOut().split(X, y, groups):
        batch = str(groups.iloc[test_idx[0]])
        model = clone(estimator)
        model.fit(X.iloc[train_idx], y[train_idx])
        pred = np.clip(model.predict(X.iloc[test_idx]), 0.0, 5.0)
        out[batch] = {
            "n": int(len(test_idx)),
            "mae": round(_mae(y[test_idx], pred), 4),
            "rmse": round(_rmse(y[test_idx], pred), 4),
        }
    return out


def _model_feature_count(key: str, estimator) -> int:
    if key == "ridge5":
        return 5
    if key == "huber5agg":
        return 15
    if key == "monotonic_gam":
        basis = estimator.best_estimator_.named_steps["monotone_basis"]
        return int(sum(len(cuts) for cuts in basis.thresholds_))
    if key == "residual_gb":
        selected = estimator.residual_model_.named_steps["select"].get_support().sum()
        return 15 + int(selected)
    raise KeyError(key)


def run(*, data: Path, split_path: Path, model_dir: Path, result_dir: Path, repeats: int) -> dict:
    frame, dropped = drop_invalid(load_table(data))
    spec = make_or_load_split(frame, path=split_path, force=False, dropped_ids=dropped)
    train_df = _select(frame, spec["train_ids"])
    test_df = _select(frame, spec["test_ids"])
    y_all = frame[AVG_COL].astype(float).map(avg_to_score5).to_numpy(dtype=float)
    y_train = train_df[AVG_COL].astype(float).map(avg_to_score5).to_numpy(dtype=float)
    y_test = test_df[AVG_COL].astype(float).map(avg_to_score5).to_numpy(dtype=float)
    groups = frame[GROUP_COL].astype(str)

    experiments = experiment_estimators(frame.columns)
    model_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    predictions = [
        {"video_id": vid, "expert_score_5": round(float(score), 4)}
        for vid, score in zip(test_df[ID_COL].astype(str), y_test)
    ]
    summary: dict[str, dict] = {}

    for key, cfg in experiments.items():
        columns = list(cfg["columns"])
        estimator = clone(cfg["estimator"])
        print(
            f"\n【{cfg['title']}】fixed train={len(train_df)} test={len(test_df)} "
            f"input_columns={len(columns)}"
        )
        estimator.fit(train_df[columns], y_train)
        model_features = _model_feature_count(key, estimator)
        print(f"  模型实际特征={model_features}")
        fixed_pred = np.clip(estimator.predict(test_df[columns]), 0.0, 5.0)
        fixed = {
            "mae": round(_mae(y_test, fixed_pred), 4),
            "rmse": round(_rmse(y_test, fixed_pred), 4),
        }
        print(f"  固定测试集 MAE={fixed['mae']:.4f} RMSE={fixed['rmse']:.4f}")

        cv = _repeated_cv(cfg["estimator"], frame[columns], y_all, seed=42, repeats=repeats)
        print(
            f"  重复5折 MAE={cv['mae_mean']:.4f}±{cv['mae_std']:.4f} "
            f"RMSE={cv['rmse_mean']:.4f}±{cv['rmse_std']:.4f}"
        )
        batch = _batch_holdout(cfg["estimator"], frame[columns], y_all, groups)
        print("  按批次留出 " + "  ".join(f"{b}:{m['mae']:.3f}" for b, m in batch.items()))

        bundle = {
            "variant": key,
            "title": cfg["title"],
            "columns": columns,
            "n_model_features": model_features,
            "estimator": estimator,
            "split": spec,
            "fixed_test": fixed,
            "repeated_cv": cv,
            "batch_holdout": batch,
        }
        with (model_dir / f"{key}.pkl").open("wb") as f:
            pickle.dump(bundle, f)
        metadata = {k: v for k, v in bundle.items() if k != "estimator"}
        (model_dir / f"{key}.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        for row, pred in zip(predictions, fixed_pred):
            row[f"pred_{key}"] = round(float(pred), 4)
            row[f"error_{key}"] = round(float(pred) - float(row["expert_score_5"]), 4)
        summary[key] = {
            "title": cfg["title"],
            "n_input_columns": len(columns),
            "n_model_features": model_features,
            "fixed_test": fixed,
            "repeated_cv": cv,
            "batch_holdout": batch,
        }

    _write_csv(result_dir / "predictions.csv", predictions)
    rows = []
    for key, result in summary.items():
        rows.append(
            {
                "variant": key,
                "title": result["title"],
                "n_input_columns": result["n_input_columns"],
                "n_model_features": result["n_model_features"],
                "fixed_mae": result["fixed_test"]["mae"],
                "fixed_rmse": result["fixed_test"]["rmse"],
                "cv_mae_mean": result["repeated_cv"]["mae_mean"],
                "cv_mae_std": result["repeated_cv"]["mae_std"],
                "cv_rmse_mean": result["repeated_cv"]["rmse_mean"],
                "cv_rmse_std": result["repeated_cv"]["rmse_std"],
            }
        )
    _write_csv(result_dir / "summary.csv", rows)
    (result_dir / "summary.json").write_text(
        json.dumps(
            {
                "data": str(data),
                "dropped": dropped,
                "n_valid": len(frame),
                "n_train": len(train_df),
                "n_test": len(test_df),
                "cv_repeats": repeats,
                "results": summary,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\n汇总 {result_dir / 'summary.csv'}")
    print(f"逐人 {result_dir / 'predictions.csv'}")
    print(f"模型 {model_dir}")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="v9 四种小样本回归实验")
    parser.add_argument("--data", type=Path, default=DATA)
    parser.add_argument("--split", type=Path, default=SPLIT)
    parser.add_argument("--model-dir", type=Path, default=MODEL_DIR)
    parser.add_argument("--result-dir", type=Path, default=RESULT_DIR)
    parser.add_argument("--cv-repeats", type=int, default=10)
    args = parser.parse_args()
    run(
        data=args.data,
        split_path=args.split,
        model_dir=args.model_dir,
        result_dir=args.result_dir,
        repeats=args.cv_repeats,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
