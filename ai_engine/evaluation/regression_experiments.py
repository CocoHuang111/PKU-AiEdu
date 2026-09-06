"""Small-sample regression experiments for v9 teaching evaluation scores.

This module is deliberately separate from the production GB path. It provides
four estimators that can be compared without changing the online model or the
existing six GB variants.
"""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin, clone
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.impute import SimpleImputer
from sklearn.linear_model import HuberRegressor, Ridge, RidgeCV
from sklearn.model_selection import GridSearchCV, KFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, StandardScaler


LLM_DIM_COLUMNS = (
    "llm_dim_teaching_attitude",
    "llm_dim_teaching_content",
    "llm_dim_teaching_method",
    "llm_dim_teaching_effect",
    "llm_dim_teaching_quality",
)

RESIDUAL_CANDIDATES = (
    "ind_completeness",
    "ind_questioning",
    "ind_blackboard",
    "ind_inspiration",
    "ind_teacher_bearing",
    "ind_demeanor",
    "ind_accurate_expression",
    "ind_time_control",
    "text__speech_rate",
    "text__question_per_10min",
    "text__interaction_count",
    "text__filler_density",
    "audio__silence_ratio",
    "slides__dwell_median_sec",
    "vision__board_readable_high_ratio",
    "courseware__cw_readable_high_ratio",
)

AGGREGATE_FEATURE_NAMES = (
    "dim_mean",
    "dim_median",
    "dim_min",
    "dim_max",
    "dim_std",
    "dim_top4_mean",
    "dim_spread",
    "dim_weakest_gap",
    "dim_count_below_60",
    "dim_count_above_85",
)


def dimension_aggregates(values: np.ndarray) -> np.ndarray:
    """Return explicit small-sample summaries for five already-imputed scores."""
    x = np.asarray(values, dtype=float)
    if x.ndim != 2 or x.shape[1] != len(LLM_DIM_COLUMNS):
        raise ValueError(f"expected n×{len(LLM_DIM_COLUMNS)} dimension matrix, got {x.shape}")
    ordered = np.sort(x, axis=1)
    mean = x.mean(axis=1)
    minimum = x.min(axis=1)
    maximum = x.max(axis=1)
    top4 = ordered[:, 1:].mean(axis=1)
    return np.column_stack(
        [
            mean,
            np.median(x, axis=1),
            minimum,
            maximum,
            x.std(axis=1),
            top4,
            maximum - minimum,
            top4 - minimum,
            (x < 60.0).sum(axis=1),
            (x >= 85.0).sum(axis=1),
        ]
    )


class DimensionAggregateTransformer(BaseEstimator, TransformerMixin):
    """Append explicit aggregate rules to the raw five dimensions."""

    def fit(self, X, y=None):
        x = np.asarray(X, dtype=float)
        if x.ndim != 2 or x.shape[1] != len(LLM_DIM_COLUMNS):
            raise ValueError("DimensionAggregateTransformer requires exactly five dimensions")
        return self

    def transform(self, X):
        x = np.asarray(X, dtype=float)
        return np.column_stack([x, dimension_aggregates(x)])

    def get_feature_names_out(self, input_features=None):
        raw = list(input_features or LLM_DIM_COLUMNS)
        return np.asarray(raw + list(AGGREGATE_FEATURE_NAMES), dtype=object)


def monotone_dimension_features(values: np.ndarray) -> np.ndarray:
    """Build summaries that never decrease when any raw dimension increases."""
    x = np.asarray(values, dtype=float)
    ordered = np.sort(x, axis=1)
    return np.column_stack(
        [
            x,
            x.mean(axis=1),
            np.median(x, axis=1),
            x.min(axis=1),
            x.max(axis=1),
            ordered[:, 1:].mean(axis=1),
            (x >= 60.0).sum(axis=1),
            (x >= 85.0).sum(axis=1),
        ]
    )


class MonotonicStepTransformer(BaseEstimator, TransformerMixin):
    """Quantile step bases for a monotone additive (GAM-like) regressor."""

    def __init__(self, quantiles: Sequence[float] = (0.2, 0.4, 0.6, 0.8)):
        self.quantiles = quantiles

    def fit(self, X, y=None):
        z = monotone_dimension_features(np.asarray(X, dtype=float))
        self.thresholds_ = []
        for j in range(z.shape[1]):
            cuts = np.quantile(z[:, j], tuple(self.quantiles))
            self.thresholds_.append(np.unique(cuts).astype(float))
        return self

    def transform(self, X):
        z = monotone_dimension_features(np.asarray(X, dtype=float))
        blocks = []
        for j, cuts in enumerate(self.thresholds_):
            for cut in cuts:
                blocks.append((z[:, j] >= cut).astype(float))
        if not blocks:
            return np.zeros((len(z), 1), dtype=float)
        return np.column_stack(blocks)


def make_ridge5() -> Pipeline:
    return Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
            (
                "ridge",
                RidgeCV(
                    alphas=np.logspace(-3, 3, 25),
                    cv=5,
                    scoring="neg_mean_absolute_error",
                ),
            ),
        ]
    )


def make_huber5agg() -> Pipeline:
    return Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("aggregate", DimensionAggregateTransformer()),
            ("scale", RobustScaler()),
            ("huber", HuberRegressor(epsilon=1.35, alpha=0.01, max_iter=3000)),
        ]
    )


def make_monotonic_gam() -> GridSearchCV:
    pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("monotone_basis", MonotonicStepTransformer()),
            ("ridge", Ridge(positive=True, solver="lbfgs", max_iter=3000)),
        ]
    )
    return GridSearchCV(
        pipe,
        {"ridge__alpha": np.logspace(-3, 2, 12)},
        cv=5,
        scoring="neg_mean_absolute_error",
        n_jobs=1,
    )


class ResidualCorrectionRegressor(BaseEstimator, RegressorMixin):
    """Robust aggregate baseline plus a bounded shallow residual GB."""

    def __init__(
        self,
        dimension_columns: Sequence[str] = LLM_DIM_COLUMNS,
        residual_columns: Sequence[str] = RESIDUAL_CANDIDATES,
        correction_limit: float = 0.25,
        selected_features: int = 8,
        random_state: int = 42,
    ):
        self.dimension_columns = dimension_columns
        self.residual_columns = residual_columns
        self.correction_limit = correction_limit
        self.selected_features = selected_features
        self.random_state = random_state

    def fit(self, X, y):
        frame = pd.DataFrame(X).copy()
        dims = list(self.dimension_columns)
        residuals = list(self.residual_columns)
        y_arr = np.asarray(y, dtype=float)
        inner = KFold(n_splits=5, shuffle=True, random_state=self.random_state)
        self.base_model_ = make_huber5agg()
        base_oof = cross_val_predict(clone(self.base_model_), frame[dims], y_arr, cv=inner)
        self.base_model_.fit(frame[dims], y_arr)

        k = min(int(self.selected_features), len(residuals))
        self.residual_model_ = Pipeline(
            [
                ("impute", SimpleImputer(strategy="median", keep_empty_features=True)),
                ("select", SelectKBest(f_regression, k=k)),
                (
                    "gb",
                    GradientBoostingRegressor(
                        loss="huber",
                        n_estimators=100,
                        learning_rate=0.03,
                        max_depth=2,
                        min_samples_split=10,
                        min_samples_leaf=8,
                        subsample=0.8,
                        random_state=self.random_state,
                    ),
                ),
            ]
        )
        self.residual_model_.fit(frame[residuals], y_arr - base_oof)
        return self

    def predict_components(self, X):
        frame = pd.DataFrame(X).copy()
        base = np.asarray(self.base_model_.predict(frame[list(self.dimension_columns)]), dtype=float)
        raw = np.asarray(
            self.residual_model_.predict(frame[list(self.residual_columns)]), dtype=float
        )
        correction = np.clip(raw, -float(self.correction_limit), float(self.correction_limit))
        return base, correction

    def predict(self, X):
        base, correction = self.predict_components(X)
        return np.clip(base + correction, 0.0, 5.0)


def available_residual_columns(columns: Sequence[str]) -> tuple[str, ...]:
    known = set(columns)
    return tuple(col for col in RESIDUAL_CANDIDATES if col in known)


def experiment_estimators(columns: Sequence[str]):
    residual_cols = available_residual_columns(columns)
    if len(residual_cols) < 8:
        raise ValueError(f"only {len(residual_cols)} residual candidate columns are available")
    return {
        "ridge5": {
            "title": "五维 Ridge",
            "columns": LLM_DIM_COLUMNS,
            "estimator": make_ridge5(),
        },
        "huber5agg": {
            "title": "五维+聚合特征 Huber",
            "columns": LLM_DIM_COLUMNS,
            "estimator": make_huber5agg(),
        },
        "monotonic_gam": {
            "title": "五维+单调聚合 GAM",
            "columns": LLM_DIM_COLUMNS,
            "estimator": make_monotonic_gam(),
        },
        "residual_gb": {
            "title": "聚合主干+精选特征残差 GB",
            "columns": tuple(LLM_DIM_COLUMNS) + residual_cols,
            "estimator": ResidualCorrectionRegressor(residual_columns=residual_cols),
        },
    }
