"""四个 GB 对照实验的共用拟合：同一份 2022 预测集，只换特征/任务。

划分写在 dataset/gb_split.json。第一次训练生成，之后四个脚本都读这一份。
"""
from __future__ import annotations

import json
import math
import pickle
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ai_engine.config import ROOT
from ai_engine.evaluation.gb import (
    AVG_COL,
    GB_PARAMS,
    GROUP_COL,
    HOLD_YEAR,
    ID_COL,
    LABEL_COL,
    SPLIT_SEED,
    TEST_FRACTION,
    avg_to_score5,
    classify_bins,
    clip_score5,
    drop_all_missing,
    feature_columns,
    is_invalid_label,
    label_to_score5,
    score100_to_score5,
    score_100_to_avg,
    SCORE_MAPPING_VERSION,
    score_to_label,
)

MISSING_INDICATOR_MIN = 0.05
SPLIT_PATH = ROOT / "dataset" / "gb_split.json"
DATA_DEFAULT = ROOT / "dataset" / "training_gb_all.csv"
ALIGNMENT_DEFAULT = ROOT / "dataset" / "alignment_all.csv"

VARIANTS: dict[str, dict[str, Any]] = {
    "obj_reg": {
        "title": "客观特征+五维 回归",
        "features": "all",
        "task": "regress",
        "n_classes": None,
    },
    "llm_reg": {
        "title": "五维 回归",
        "features": "llm",
        "task": "regress",
        "n_classes": None,
    },
    "llm_cls5": {
        "title": "五维 5分类",
        "features": "llm",
        "task": "classify",
        "n_classes": 5,
    },
    "llm_cls8": {
        "title": "五维 8分类",
        "features": "llm",
        "task": "classify",
        "n_classes": 8,
    },
    "obj_only_reg": {
        "title": "只用客观特征 回归",
        "features": "objective",
        "task": "regress",
        "n_classes": None,
    },
    "ind_reg": {
        "title": "只用二级指标 回归",
        "features": "indicators",
        "task": "regress",
        "n_classes": None,
    },
}


def _require_sklearn() -> None:
    try:
        import pandas  # noqa: F401
        import sklearn  # noqa: F401
    except ImportError:
        print("需要 pandas 和 scikit-learn：pip install pandas scikit-learn", file=sys.stderr)
        raise SystemExit(1)


def _rmse(y_true, y_pred) -> float:
    err = [(float(a) - float(b)) ** 2 for a, b in zip(y_true, y_pred)]
    return math.sqrt(sum(err) / len(err)) if err else float("nan")


def _mae(y_true, y_pred) -> float:
    err = [abs(float(a) - float(b)) for a, b in zip(y_true, y_pred)]
    return sum(err) / len(err) if err else float("nan")


def load_table(path: Path):
    import pandas as pd

    if not path.exists():
        raise SystemExit(f"找不到训练表 {path}")
    df = pd.read_csv(path)
    if ID_COL not in df.columns or LABEL_COL not in df.columns:
        raise SystemExit(f"{path} 缺少 {ID_COL} 或 {LABEL_COL}")
    return df


def drop_invalid(df):
    import pandas as pd

    dropped: list[str] = []
    keep = []
    for i, row in df.iterrows():
        avg = row[AVG_COL] if AVG_COL in df.columns else None
        total = row[LABEL_COL]
        avg_f = None if pd.isna(avg) else float(avg)
        total_f = None if pd.isna(total) else float(total)
        if is_invalid_label(avg_f, total_f):
            dropped.append(str(row[ID_COL]))
        else:
            keep.append(i)
    out = df.loc[keep].reset_index(drop=True)
    return out, dropped


def make_or_load_split(
    df,
    *,
    path: Path = SPLIT_PATH,
    seed: int = SPLIT_SEED,
    hold_year: str = HOLD_YEAR,
    test_fraction: float = TEST_FRACTION,
    force: bool = False,
    dropped_ids: list[str] | None = None,
) -> dict[str, Any]:
    """划预测集。默认从 hold_year 留出；hold_year=within 则在全表内 8:2（单年批次用）。"""
    from sklearn.model_selection import train_test_split

    ids = df[ID_COL].astype(str)
    if path.exists() and not force:
        spec = json.loads(path.read_text(encoding="utf-8"))
        known = set(ids)
        spec["train_ids"] = [i for i in spec["train_ids"] if i in known]
        spec["test_ids"] = [i for i in spec["test_ids"] if i in known]
        print(
            f"沿用划分 {path}：train={len(spec['train_ids'])}  "
            f"test={len(spec['test_ids'])}（{spec.get('hold_year')} 的 {spec.get('test_fraction')}）"
        )
        return spec

    within = hold_year in ("", "within", "all") or GROUP_COL not in df.columns
    if within:
        hold = [True] * len(df)
        hold_ids = ids.tolist()
        rest_ids = []
        hold_year = "within"
    else:
        hold = df[GROUP_COL].astype(str) == hold_year
        hold_ids = ids[hold].tolist()
        rest_ids = ids[~hold].tolist()
    if len(hold_ids) < 5:
        raise SystemExit(f"{hold_year} 只有 {len(hold_ids)} 人，划不出预测集")

    avgs = df.loc[hold, AVG_COL].astype(float) if not within else df[AVG_COL].astype(float)
    raw = [score_to_label(float(a), n_classes=5) for a in avgs]
    counts = Counter(raw)
    majority = counts.most_common(1)[0][0]
    strat = [majority if counts[c] < 2 else c for c in raw]
    use_strat = min(Counter(strat).values()) >= 2
    hold_train, hold_test = train_test_split(
        hold_ids,
        test_size=test_fraction,
        random_state=seed,
        stratify=strat if use_strat else None,
    )
    spec = {
        "hold_year": hold_year,
        "seed": seed,
        "test_fraction": test_fraction,
        "dropped_ids": dropped_ids or [],
        "train_ids": rest_ids + list(hold_train),
        "test_ids": list(hold_test),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"新划分 {path}：{hold_year} {len(hold_ids)} 人中划出 {len(hold_test)} 作预测集，"
        f"训练 {len(spec['train_ids'])}（含其他年份 {len(rest_ids)}）"
    )
    return spec


def _prepare_X(df, features: str):
    import pandas as pd

    raw_cols = feature_columns(df.columns, mode=features)
    if not raw_cols:
        raise SystemExit(f"features={features} 没有可用列")
    X = df[raw_cols].apply(pd.to_numeric, errors="coerce")
    kept, all_nan = drop_all_missing(X, raw_cols)
    X = X[kept].copy()
    indicator_src: list[str] = []
    for col in list(X.columns):
        rate = float(X[col].isna().mean())
        if rate >= MISSING_INDICATOR_MIN:
            X[f"{col}__missing"] = X[col].isna().astype(int)
            indicator_src.append(col)
    return X, all_nan, indicator_src


def _estimator(task: str):
    from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline

    model = (
        GradientBoostingClassifier(**GB_PARAMS)
        if task == "classify"
        else GradientBoostingRegressor(**GB_PARAMS)
    )
    return Pipeline([("impute", SimpleImputer(strategy="median")), ("gb", model)])


def _join_llm_overall(ids, alignment_path: Path | None) -> dict[str, float]:
    import pandas as pd

    if alignment_path is None or not alignment_path.exists():
        return {}
    al = pd.read_csv(alignment_path)
    if ID_COL not in al.columns or "llm_overall" not in al.columns:
        return {}
    out: dict[str, float] = {}
    for _, row in al.iterrows():
        if pd.isna(row["llm_overall"]):
            continue
        out[str(row[ID_COL])] = float(row["llm_overall"])
    return out


def _select(df, id_list: list[str]):
    order = {vid: i for i, vid in enumerate(id_list)}
    sub = df[df[ID_COL].astype(str).isin(order)].copy()
    sub["_ord"] = sub[ID_COL].astype(str).map(order)
    return sub.sort_values("_ord").drop(columns="_ord").reset_index(drop=True)


def run_variant(
    key: str,
    *,
    data: Path = DATA_DEFAULT,
    alignment: Path | None = ALIGNMENT_DEFAULT,
    split_path: Path = SPLIT_PATH,
    out_dir: Path | None = None,
    force_split: bool = False,
    hold_year: str = HOLD_YEAR,
) -> dict[str, Any]:
    _require_sklearn()
    if key not in VARIANTS:
        raise SystemExit(f"未知实验 {key}，可选 {list(VARIANTS)}")
    cfg = VARIANTS[key]
    out_dir = out_dir or (ROOT / "models")
    out_dir.mkdir(parents=True, exist_ok=True)

    df, dropped = drop_invalid(load_table(data))
    print(f"【{cfg['title']}】读入后剔除 {dropped or '无'}，剩余 {len(df)}")
    spec = make_or_load_split(
        df, path=split_path, force=force_split, dropped_ids=dropped, hold_year=hold_year
    )
    train_df = _select(df, spec["train_ids"])
    test_df = _select(df, spec["test_ids"])
    X_all, all_nan, ind_src = _prepare_X(df, cfg["features"])
    if all_nan:
        print(f"丢掉整列缺失 {len(all_nan)} 个：{', '.join(all_nan)}")
    X_all = X_all.copy()
    X_all[ID_COL] = df[ID_COL].astype(str)
    X_tr = _select(X_all, spec["train_ids"]).drop(columns=[ID_COL])
    X_te = _select(X_all, spec["test_ids"]).drop(columns=[ID_COL])

    task = cfg["task"]
    n_classes = cfg["n_classes"]
    step = classify_bins(n_classes)[0] if n_classes else None
    y_tr_reg = train_df[AVG_COL].astype(float).map(avg_to_score5)
    y_te_reg = test_df[AVG_COL].astype(float).map(avg_to_score5)
    if task == "classify":
        y_tr = [
            score_to_label(float(s), step=step, n_classes=n_classes) for s in train_df[AVG_COL]
        ]
        y_te_label = [
            score_to_label(float(s), step=step, n_classes=n_classes) for s in test_df[AVG_COL]
        ]
    else:
        y_tr = y_tr_reg
        y_te_label = None

    print(f"特征 {X_tr.shape[1]} 维  train={len(X_tr)}  test={len(X_te)}  标签=专家 0–5")
    pipe = _estimator(task)
    pipe.fit(X_tr, y_tr)
    pred_raw = pipe.predict(X_te)

    if task == "classify":
        pred_5 = [label_to_score5(int(v), step=step) for v in pred_raw]
        pred_label = [int(v) for v in pred_raw]
    else:
        pred_5 = [clip_score5(float(v)) for v in pred_raw]
        pred_label = [None] * len(pred_raw)

    llm_map = _join_llm_overall(test_df[ID_COL].astype(str), alignment)
    judge_5 = [
        score100_to_score5(llm_map[str(i)]) if str(i) in llm_map else float("nan")
        for i in test_df[ID_COL]
    ]
    y5 = [float(v) for v in y_te_reg]
    metrics: dict[str, Any] = {
        "variant": key,
        "title": cfg["title"],
        "scale": "0-5",
        "n_train": int(len(X_tr)),
        "n_test": int(len(X_te)),
        "mae_5": round(_mae(y5, pred_5), 3),
        "rmse_5": round(_rmse(y5, pred_5), 3),
    }
    judge_ok = [(a, b) for a, b in zip(y5, judge_5) if b == b]
    if judge_ok:
        metrics["judge_mae_5"] = round(_mae([a for a, _ in judge_ok], [b for _, b in judge_ok]), 3)
        metrics["judge_rmse_5"] = round(_rmse([a for a, _ in judge_ok], [b for _, b in judge_ok]), 3)

    if task == "classify":
        from sklearn.metrics import accuracy_score, f1_score

        metrics["acc"] = round(float(accuracy_score(y_te_label, pred_label)), 3)
        metrics["f1"] = round(
            float(f1_score(y_te_label, pred_label, average="weighted", zero_division=0)), 3
        )
        j_labs = []
        y_labs = []
        for vid, lab in zip(test_df[ID_COL].astype(str), y_te_label):
            if vid not in llm_map:
                continue
            j_labs.append(
                score_to_label(score_100_to_avg(llm_map[vid]), step=step, n_classes=n_classes)
            )
            y_labs.append(lab)
        if j_labs:
            metrics["judge_acc"] = round(float(accuracy_score(y_labs, j_labs)), 3)

    gb = pipe.named_steps["gb"]
    imp = list(zip(list(X_tr.columns), [float(v) for v in gb.feature_importances_]))
    imp.sort(key=lambda x: -x[1])
    metrics["feature_importance"] = [[n, round(v, 4)] for n, v in imp[:10]]

    print(
        f"  预测集 MAE={metrics['mae_5']:.3f}  RMSE={metrics['rmse_5']:.3f}（0–5 分）"
        + (f"  Acc={metrics['acc']:.3f}  F1={metrics['f1']:.3f}" if "acc" in metrics else "")
        + (
            f"  | Judge MAE={metrics['judge_mae_5']:.3f}"
            if "judge_mae_5" in metrics
            else ""
        )
    )
    print("  特征重要性：")
    for name, val in imp[:8]:
        print(f"    {val:.3f}  {name}")

    bundle = {
        "variant": key,
        "config": cfg,
        "pipeline": pipe,
        "feature_names": list(X_tr.columns),
        "dropped_all_nan": all_nan,
        "indicator_src": ind_src,
        "split": {k: spec[k] for k in ("hold_year", "seed", "test_fraction", "train_ids", "test_ids")},
        "metrics": metrics,
        "hyperparams": GB_PARAMS,
        "n_classes": n_classes,
        "step": step,
        "label_scale": "0-5",
        "score_mapping_version": SCORE_MAPPING_VERSION,
    }
    pkl_path = out_dir / f"gb_{key}.pkl"
    with open(pkl_path, "wb") as f:
        pickle.dump(bundle, f)
    pred_rows = []
    for i, vid in enumerate(test_df[ID_COL].astype(str)):
        pred_rows.append(
            {
                "video_id": vid,
                "variant": key,
                "score_mapping_version": SCORE_MAPPING_VERSION,
                "expert_avg": float(test_df[AVG_COL].iloc[i]),
                "expert_score_5": round(y5[i], 4),
                "pred_5": round(pred_5[i], 4),
                "pred_label": "" if pred_label[i] is None else pred_label[i],
                "true_label": "" if y_te_label is None else y_te_label[i],
                "llm_overall_5": "" if judge_5[i] != judge_5[i] else round(judge_5[i], 4),
            }
        )
    pred_path = out_dir / f"gb_{key}_pred.csv"
    _write_csv(pred_path, pred_rows)
    meta = {k: v for k, v in bundle.items() if k != "pipeline"}
    (out_dir / f"gb_{key}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  模型 {pkl_path}")
    print(f"  预测 {pred_path}")
    return metrics


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    import csv

    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main_for(key: str) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=VARIANTS[key]["title"])
    ap.add_argument("--data", default=str(DATA_DEFAULT))
    ap.add_argument("--alignment", default=str(ALIGNMENT_DEFAULT))
    ap.add_argument("--split", default=str(SPLIT_PATH))
    ap.add_argument("--out-dir", default=str(ROOT / "models"))
    ap.add_argument("--resplit", action="store_true", help="扔掉已有划分文件重新抽预测集")
    ap.add_argument(
        "--hold-year",
        default=HOLD_YEAR,
        help="从哪一年留出预测集；within=在本表内 8:2（单年、无 batch 列时用）",
    )
    args = ap.parse_args()
    align = Path(args.alignment)
    run_variant(
        key,
        data=Path(args.data),
        alignment=align if align.exists() else None,
        split_path=Path(args.split),
        out_dir=Path(args.out_dir),
        force_split=args.resplit,
        hold_year=args.hold_year,
    )
    return 0
