"""GB 评分校准：特征列约定、无效标签剔除、离散化映射、线上总分推理。

对照实验仍走 gb_fit.py。线上视频评估的五维仍由 Judge 打（v7.1 prompt），总分改用
四年 v7.1 全量训出的「客观特征+五维 5 分类」模型（见 LIVE_GB_PATH）。
"""
from __future__ import annotations

import math
import pickle
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from ai_engine.config import ROOT

ID_COL = "video_id"
LABEL_COL = "expert_total_100"
AVG_COL = "expert_avg"
GROUP_COL = "batch"
LEAK_COLS = frozenset(
    {
        ID_COL,
        LABEL_COL,
        AVG_COL,
        GROUP_COL,
        "prompt_version",
        "judge_fingerprint",
        "name",
        "comment",
    }
)

# 与 1.0 同一组浅树超参：样本少，深度 3 防过拟合。
GB_PARAMS: dict[str, Any] = {
    "n_estimators": 200,
    "max_depth": 3,
    "learning_rate": 0.08,
    "min_samples_split": 4,
    "min_samples_leaf": 2,
    "subsample": 0.8,
    "random_state": 42,
}

THESIS_SCORE_MIN = 2.0
THESIS_SCORE_MAX = 4.0
SCORE5_MAX = 5.0
SCORE_MAPPING_VERSION = "expert-4pt-direct-v2"
HOLD_YEAR = "2022_spring"
TEST_FRACTION = 0.2
SPLIT_SEED = 42


def is_invalid_label(avg: float | None, total: float | None) -> bool:
    """专家均分缺失、非正，或百分制越界。"""
    try:
        total_value = float(total) if total is not None else float("nan")
    except (TypeError, ValueError):
        return True
    if not math.isfinite(total_value) or not 0 <= total_value <= 100:
        return True
    try:
        avg_value = float(avg) if avg is not None else None
    except (TypeError, ValueError):
        return True
    if avg_value is not None and (
        not math.isfinite(avg_value) or avg_value <= 0 or avg_value > THESIS_SCORE_MAX
    ):
        return True
    return False


def classify_bins(n_classes: int) -> tuple[float, int]:
    """把 [2, 4) 均分成 n 档。5 类 step=0.4（1.0）；8 类 step=0.25；10 类 step=0.2（论文）。"""
    if n_classes < 2:
        raise ValueError("n_classes 至少为 2")
    return 2.0 / n_classes, n_classes


def score_to_label(
    score: float,
    *,
    score_min: float = THESIS_SCORE_MIN,
    step: float | None = None,
    n_classes: int = 5,
) -> int:
    """专家均分 → 离散类别：⌊(score − 2.0) / step⌋。"""
    if step is None:
        step, n_classes = classify_bins(n_classes)
    if step <= 0:
        raise ValueError("step 必须为正")
    label = int(math.floor((float(score) - score_min) / step))
    return max(0, min(n_classes - 1, label))


def label_to_score(
    label: int,
    *,
    score_min: float = THESIS_SCORE_MIN,
    step: float = 0.4,
) -> float:
    """类别中点还原到 2–4 分。"""
    return score_min + int(label) * step + step / 2.0


def label_to_score_100(
    label: int,
    *,
    score_min: float = THESIS_SCORE_MIN,
    step: float = 0.4,
) -> float:
    """类别中点还原到专家百分制，便于和回归、Judge 比 MAE。"""
    avg = label_to_score(label, score_min=score_min, step=step)
    return avg / THESIS_SCORE_MAX * 100.0


def avg_to_score5(
    avg: float,
    *,
    score_min: float = THESIS_SCORE_MIN,
    score_max: float = THESIS_SCORE_MAX,
) -> float:
    """专家 4 分制 → 0–5。2.0→2.5，4.0→5，与正确百分制 / 20 相同。"""
    return float(avg) / score_max * SCORE5_MAX


def score100_to_score5(total: float) -> float:
    """Judge / 专家百分制 → 0–5。"""
    return float(total) / 20.0


def clip_score5(value: float) -> float:
    return max(0.0, min(SCORE5_MAX, float(value)))


def label_to_score5(
    label: int,
    *,
    score_min: float = THESIS_SCORE_MIN,
    step: float = 0.4,
) -> float:
    """类别中点还原到 0–5。"""
    return clip_score5(score100_to_score5(label_to_score_100(label, score_min=score_min, step=step)))


def score_100_to_avg(total: float, *, score_max: float = THESIS_SCORE_MAX) -> float:
    """百分制 → 2–4 均分（与 inventory.expert_total_100 互逆）。"""
    return float(total) / 100.0 * score_max


OBJECTIVE_PREFIXES = (
    "text__",
    "audio__",
    "timeline__",
    "vision__",
    "courseware__",
    "slides__",
    "speakers__",
)
LLM_DIM_COLS = frozenset(
    {
        "llm_dim_teaching_attitude",
        "llm_dim_teaching_content",
        "llm_dim_teaching_method",
        "llm_dim_teaching_effect",
        "llm_dim_teaching_quality",
    }
)

LIVE_VARIANT = "obj_cls5"
LIVE_PROMPT_VERSION = "v7.1-goal-effect-fallback"
LIVE_GB_DIR = ROOT / "models" / "live"
LIVE_GB_PATH = LIVE_GB_DIR / f"gb_{LIVE_VARIANT}.pkl"
LIVE_SCORE_SOURCE = "gb_obj_cls5"


def _is_indicator_score(col: str) -> bool:
    return col.startswith("ind_") and not col.endswith("_assessed")


def feature_columns(
    columns: Iterable[str],
    *,
    mode: str = "all",
) -> list[str]:
    """从训练表列名里挑特征：去掉 id / 标签 / 批次，不把评语当特征。

    all = 客观特征 + 五维一级分；llm = 只要五维一级分；
    objective = 只要 7 组客观特征；indicators = 只要二级指标分。
    """
    cols = [c for c in columns if c not in LEAK_COLS]
    if mode == "llm":
        cols = [c for c in cols if c in LLM_DIM_COLS]
    elif mode == "objective":
        cols = [c for c in cols if c.startswith(OBJECTIVE_PREFIXES)]
    elif mode == "indicators":
        cols = [c for c in cols if _is_indicator_score(c)]
    elif mode == "all":
        cols = [
            c
            for c in cols
            if c.startswith(OBJECTIVE_PREFIXES) or c in LLM_DIM_COLS
        ]
    else:
        raise ValueError(f"未知 features 模式: {mode}")
    return cols


def drop_all_missing(frame: Any, columns: list[str]) -> tuple[list[str], list[str]]:
    """整列都空的特征（说话人分离默认关 → speakers__* 全空）没有方差，丢掉。"""
    kept: list[str] = []
    dropped: list[str] = []
    for col in columns:
        if frame[col].isna().all():
            dropped.append(col)
        else:
            kept.append(col)
    return kept, dropped


def llm_dim_column(dimension_key: str) -> str:
    return f"llm_dim_{dimension_key}"


def features_from_dimensions(dimensions: list[dict[str, Any]]) -> dict[str, float | None]:
    """把 Judge 五维结果收成训练时的 llm_dim_* 列。未评估记为缺失。"""
    out: dict[str, float | None] = {col: None for col in LLM_DIM_COLS}
    for dim in dimensions:
        col = llm_dim_column(str(dim.get("key") or ""))
        if col not in out:
            continue
        if dim.get("assessed") and dim.get("score") is not None:
            out[col] = float(dim["score"])
    return out


def features_from_raw(raw: dict[str, Any] | None) -> dict[str, float | None]:
    """把流水线 raw_features（按组）收成训练时的 group__key 列。"""
    from ai_engine.pedagogy.loader import get_rubric

    spec = get_rubric().get("objective_features") or {}
    out: dict[str, float | None] = {}
    grouped = raw or {}
    for group, keys in spec.items():
        src = grouped.get(group) or {}
        for key in keys:
            val = src.get(key)
            if val is None or val == "":
                out[f"{group}__{key}"] = None
                continue
            try:
                out[f"{group}__{key}"] = float(val)
            except (TypeError, ValueError):
                out[f"{group}__{key}"] = None
    return out


def features_from_evidence(
    dimensions: list[dict[str, Any]],
    raw_features: dict[str, Any] | None = None,
) -> dict[str, float | None]:
    """线上推理用的完整特征：客观特征 + 五维一级分。"""
    out = features_from_raw(raw_features)
    out.update(features_from_dimensions(dimensions))
    return out


def _row_for_bundle(
    scores: dict[str, float | None], feature_names: list[str]
) -> dict[str, float]:
    import math as _math

    row: dict[str, float] = {}
    for name in feature_names:
        if name.endswith("__missing"):
            src = name[: -len("__missing")]
            val = scores.get(src)
            row[name] = 1.0 if val is None or (isinstance(val, float) and _math.isnan(val)) else 0.0
        else:
            val = scores.get(name)
            row[name] = float("nan") if val is None else float(val)
    return row


@lru_cache(maxsize=4)
def load_gb_bundle(path: str) -> dict[str, Any]:
    model_path = Path(path)
    if not model_path.exists():
        raise FileNotFoundError(
            f"找不到线上 GB 模型 {model_path}。请先运行 make train-gb-live"
        )
    with model_path.open("rb") as f:
        bundle = pickle.load(f)
    if not isinstance(bundle, dict) or "pipeline" not in bundle:
        raise ValueError(f"{model_path} 不是有效的 GB bundle")
    return bundle


def predict_overall(
    dimensions: list[dict[str, Any]],
    *,
    raw_features: dict[str, Any] | None = None,
    model_path: Path | str | None = None,
) -> dict[str, Any]:
    """用客观特征+五维 5 分类 GB 合成总分。返回百分制、0–5 与 4 分制。"""
    import pandas as pd

    path = Path(model_path) if model_path is not None else LIVE_GB_PATH
    bundle = load_gb_bundle(str(path.resolve()))
    names = list(bundle.get("feature_names") or [])
    if not names:
        raise ValueError(f"{path} 缺少 feature_names")
    step = float(bundle.get("step") or 0.4)
    row = _row_for_bundle(features_from_evidence(dimensions, raw_features), names)
    pred = bundle["pipeline"].predict(pd.DataFrame([row], columns=names))[0]
    label = int(pred)
    score_5 = label_to_score5(label, step=step)
    score_100 = round(label_to_score_100(label, step=step), 1)
    return {
        "label": label,
        "score_5": round(score_5, 4),
        "score_4": round(score_5 / SCORE5_MAX * THESIS_SCORE_MAX, 4),
        "score": score_100,
        "variant": bundle.get("variant") or LIVE_VARIANT,
        "model_path": str(path),
        "step": step,
        "score_mapping_version": bundle.get("score_mapping_version") or SCORE_MAPPING_VERSION,
    }
