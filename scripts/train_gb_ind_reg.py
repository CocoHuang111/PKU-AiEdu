"""只用二级指标分 → 回归专家等值 0–5 分。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.evaluation.gb_fit import main_for

if __name__ == "__main__":
    raise SystemExit(main_for("ind_reg"))
