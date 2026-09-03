"""GB 评分校准：特征列约定、无效标签剔除、离散化映射。

四个对照脚本共用同一份划分（见 gb_fit.py），线上评估仍走 Judge。
"""
from __future__ import annotations

import math
from typing import Any, Iterable

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
