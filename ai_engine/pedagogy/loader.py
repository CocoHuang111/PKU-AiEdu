"""教育学理论底座的加载：YAML 指标体系 + Jinja2 提示词模板。"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

PEDAGOGY_DIR = Path(__file__).resolve().parent
PROMPT_DIR = PEDAGOGY_DIR / "prompts"


@lru_cache(maxsize=8)
def load_yaml(name: str) -> dict[str, Any]:
    path = PEDAGOGY_DIR / name
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=1)
def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(PROMPT_DIR),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_prompt(template: str, **kwargs) -> str:
    return _env().get_template(template).render(**kwargs)


@lru_cache(maxsize=1)
def get_rubric() -> dict[str, Any]:
    return load_yaml("evaluation_rubric.yaml")


def grade_of(score: float) -> dict[str, str]:
    """按分数查等级。thresholds 已按 min 降序排列。

    键名用 grade_label 而不是 label，避免展开到维度字典里时覆盖维度自己的 label。
    """
    for t in get_rubric()["meta"]["grade_thresholds"]:
        if score >= t["min"]:
            return {"grade": t["grade"], "grade_label": t["label"]}
    return {"grade": "D", "grade_label": "待提升"}


def iter_indicators():
    """展平遍历所有二级指标，产出 (dimension, indicator)。"""
    for dim in get_rubric()["dimensions"]:
        for ind in dim["indicators"]:
            yield dim, ind


def indicator_index() -> dict[str, tuple[dict, dict]]:
    """indicator_key -> (dimension, indicator)，Judge 结果回填时用。"""
    return {ind["key"]: (dim, ind) for dim, ind in iter_indicators()}


def read_schema_file(name: str) -> str:
    return (PEDAGOGY_DIR / name).read_text(encoding="utf-8")
