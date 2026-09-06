"""Focused tests for the isolated small-sample regression experiments."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ai_engine.evaluation.regression_experiments import (
    LLM_DIM_COLUMNS,
    RESIDUAL_CANDIDATES,
    ResidualCorrectionRegressor,
    dimension_aggregates,
    make_monotonic_gam,
)


def main() -> int:
    strong_with_one_weak = np.asarray([[90, 90, 90, 90, 55]], dtype=float)
    several_weak = np.asarray([[90, 90, 55, 55, 55]], dtype=float)
    a = dimension_aggregates(strong_with_one_weak)[0]
    b = dimension_aggregates(several_weak)[0]
    assert a[5] > b[5], "top-four mean must distinguish one weak dimension from several"
    assert a[8] == 1 and b[8] == 3, "low-dimension count is incorrect"

    rng = np.random.default_rng(42)
    X = rng.uniform(45, 95, size=(60, 5))
    y = 2.0 + X.mean(axis=1) / 35.0
    gam = make_monotonic_gam().fit(X, y)
    low = np.full((1, 5), 65.0)
    high = low.copy()
    high[0, 2] = 90.0
    assert float(gam.predict(high)[0]) + 1e-9 >= float(gam.predict(low)[0])

    frame = pd.DataFrame(X, columns=LLM_DIM_COLUMNS)
    for i, col in enumerate(RESIDUAL_CANDIDATES):
        frame[col] = rng.normal(loc=i, scale=1.0, size=len(frame))
    residual = ResidualCorrectionRegressor().fit(frame, y)
    base, correction = residual.predict_components(frame.iloc[:10])
    pred = residual.predict(frame.iloc[:10])
    assert np.max(np.abs(correction)) <= 0.2500001
    assert np.allclose(pred, np.clip(base + correction, 0.0, 5.0))
    print("回归实验测试全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
