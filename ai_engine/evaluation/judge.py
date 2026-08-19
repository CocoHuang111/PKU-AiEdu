"""LLM-as-Judge：按 rubric 逐维度、逐二级指标打分，再由模型综合出一级分。

每个一级维度单独调一次 LLM，而不是一次性打全部 24 个指标。
分开调的好处是每次的提示词更聚焦、输出更短，JSON 解析失败率显著更低。

一级维度分默认用模型给出的 dimension_score（可按课型在二级分之间灵活折算）。
缺字段、越界或解析失败时回退到二级指标加权平均，保证链路不断。
"""

from __future__ import annotations

import json
import re
from typing import Any

from ..pedagogy.loader import get_rubric, grade_of, render_prompt
from ..providers import ChatMessage, ProviderError, get_llm

JSON_BLOCK = re.compile(r"[\{\[][\s\S]*[\}\]]")

SYSTEM = "你是严谨的高校教学评估专家。你只输出合法 JSON，不输出任何解释文字。"

# 历史评语蒸馏出的短口径，默认空。数据集 extract/rejudge 可注入；线上评估保持空。
_expert_lessons = ""


def set_expert_lessons(text: str | None) -> None:
    global _expert_lessons
    _expert_lessons = (text or "").strip()


def get_expert_lessons() -> str:
    return _expert_lessons


def _parse_json(raw: str) -> Any:
    """LLM 常会在 JSON 外面裹一层代码块或寒暄，这里做容错提取。"""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    if match := JSON_BLOCK.search(text):
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    raise ValueError(f"无法解析为 JSON：{raw[:200]}")


def _as_indicator_list(parsed: Any) -> list[dict]:
    """把模型的各种输出形态归一成指标列表。

    小参数量模型经常不按约定的 {"indicators": [...]} 输出，
    而是直接给一个数组，或者用别的键名包一层。这里都接住。
    """
    if isinstance(parsed, list):
        candidates = parsed
    elif isinstance(parsed, dict):
        if isinstance(parsed.get("indicators"), list):
            candidates = parsed["indicators"]
        else:
            # 退而求其次：取第一个值为列表的键
            candidates = next(
                (v for v in parsed.values() if isinstance(v, list)), []
            )
            # 也可能是 {"preparation": {...}, "proficiency": {...}} 这种扁平映射
            if not candidates:
                candidates = [
                    {"key": k, **v}
                    for k, v in parsed.items()
                    if isinstance(v, dict) and "score" in v
                ]
    else:
        candidates = []
    return [c for c in candidates if isinstance(c, dict)]


def _clamp_score(value: Any) -> int:
    try:
        return max(0, min(100, int(round(float(value)))))
    except (TypeError, ValueError):
        return 60


# 模型给出的一级分允许略超出已评二级分的 min/max，但不能飞出这节课的证据范围。
DIM_SCORE_SLACK = 5


def _weighted_dimension_score(indicators: list[dict]) -> float | None:
    """二级指标加权平均。跳过项不计入。全部跳过时返回 None。"""
    graded = [i for i in indicators if i.get("assessed")]
    if not graded:
        return None
    total_weight = sum(i.get("weight", 1.0) for i in graded) or 1.0
    return round(
        sum(i["score"] * i.get("weight", 1.0) for i in graded) / total_weight, 1
    )


def _accept_llm_dimension_score(raw: Any, graded: list[dict]) -> int | None:
    """一级分必须能解析，且落在已评二级分的 [min-slack, max+slack] 内。"""
    if not graded or raw is None:
        return None
    try:
        score = int(round(float(raw)))
    except (TypeError, ValueError):
        return None
    score = max(0, min(100, score))
    lo = min(i["score"] for i in graded)
    hi = max(i["score"] for i in graded)
    if score < lo - DIM_SCORE_SLACK or score > hi + DIM_SCORE_SLACK:
        return None
    return score


def _dimension_meta(parsed: Any) -> tuple[Any, str]:
    """从整段 JSON 里抽出一级分和折算说明。裸数组则没有这两项。"""
    if not isinstance(parsed, dict):
        return None, ""
    rationale = str(parsed.get("dimension_rationale") or "").strip()
    return parsed.get("dimension_score"), rationale


MODALITY_LABEL = {"audio": "音频", "text": "文本", "vision": "图像"}


def _fallback_indicator(ind: dict, reason: str) -> dict:
    return {
        "key": ind["key"],
        "label": ind["label"],
        "modalities": ind["modalities"],
        "score": 60,
        "assessed": True,
        "confidence": "low",
        "evidence": f"未能获得有效评分（{reason}），按中位分处理。",
        "suggestion": "建议重新运行评估，或检查大模型配置。",
        "weight": ind.get("weight", 1.0),
    }


def _skipped_indicator(ind: dict, reason: str | None = None) -> dict:
    if reason is None:
        missing = "、".join(MODALITY_LABEL.get(m, m) for m in ind["modalities"])
        reason = f"本次评估缺少{missing}模态数据，该指标未参与评分。"
    return {
        "key": ind["key"],
        "label": ind["label"],
        "modalities": ind["modalities"],
        "score": None,
        "assessed": False,
        "confidence": "none",
        "evidence": reason,
        "suggestion": "补齐所需模态后重新评估即可得到该项得分。",
        "weight": ind.get("weight", 1.0),
    }


REFERENCE_MISSING = (
    "本次未提供本节课的知识点清单或教学大纲。缺少参照物时无法判断「应覆盖什么」，"
    "为避免给出没有依据的分数，该指标标记为未评估。"
)


def _skip_reason(ind: dict, evidence: dict, available: set[str]) -> str | None:
    """返回跳过该指标的原因，None 表示可以评。"""
    if not set(ind["modalities"]) & available:
        return ""  # 空串表示走模态缺失的默认文案
    if ind.get("requires_reference") and not evidence.get("reference"):
        return REFERENCE_MISSING
    return None


def judge_dimension(
    dimension: dict, evidence: dict, available: set[str] | None = None
) -> dict[str, Any]:
    """对单个一级维度打分，返回带二级指标明细的结果。

    available 是本次可用的模态集合。完全依赖缺失模态的二级指标会被跳过，
    而不是硬塞给模型瞎猜——否则关掉视觉分析会让"板书设计"这类指标拿到
    莫名其妙的低分，进而拖垮整个维度。
    """
    available = available or {"text", "audio", "vision"}

    assessable: list[dict] = []
    skipped: list[tuple[dict, str]] = []
    for ind in dimension["indicators"]:
        reason = _skip_reason(ind, evidence, available)
        if reason is None:
            assessable.append(ind)
        else:
            skipped.append((ind, reason))

    # 整个维度都没法评时，直接返回未评估状态，不去调模型
    if not assessable:
        return {
            "key": dimension["key"],
            "label": dimension["label"],
            "description": dimension["description"],
            "weight": dimension.get("weight", 1.0),
            "score": None,
            "weighted_score": None,
            "score_source": None,
            "dimension_rationale": "",
            "assessed": False,
            "skipped_count": len(skipped),
            "grade": "-",
            "grade_label": "未评估",
            "indicators": [_skipped_indicator(i, r or None) for i, r in skipped],
        }

    prompt = render_prompt(
        "eval_judge.j2",
        dimension={**dimension, "indicators": assessable},
        evidence=evidence,
        expert_lessons=_expert_lessons,
    )
    llm = get_llm()

    items: list[dict] = []
    parsed: Any = None
    error_reason = ""

    for attempt in range(2):
        try:
            raw = llm.chat(
                [ChatMessage("system", SYSTEM), ChatMessage("user", prompt)]
            )
            parsed = _parse_json(raw)
            items = _as_indicator_list(parsed)
            if items:
                break
            error_reason = "模型未返回任何指标"
        except ValueError:
            error_reason = "输出格式错误"
        except ProviderError as e:
            error_reason = str(e)
            break
        if attempt == 0:
            prompt += (
                "\n\n注意：上次输出不符合要求。请严格输出形如 "
                '{"indicators": [{"key": "...", "score": 85, "confidence": "high", '
                '"evidence": "...", "suggestion": "..."}], '
                '"dimension_score": 78, "dimension_rationale": "..."} 的 JSON。'
            )

    scored = {item["key"]: item for item in items if item.get("key")}
    raw_dim_score, rationale = _dimension_meta(parsed)

    indicators = []
    for ind in assessable:
        item = scored.get(ind["key"])
        if not item:
            indicators.append(
                _fallback_indicator(ind, error_reason or "模型未返回该指标")
            )
            continue
        indicators.append(
            {
                "key": ind["key"],
                "label": ind["label"],
                "modalities": ind["modalities"],
                "score": _clamp_score(item.get("score")),
                "assessed": True,
                "confidence": item.get("confidence", "medium"),
                "evidence": str(item.get("evidence", "")).strip(),
                "suggestion": str(item.get("suggestion", "")).strip(),
                "weight": ind.get("weight", 1.0),
            }
        )
    indicators.extend(_skipped_indicator(i, r or None) for i, r in skipped)

    graded = [i for i in indicators if i["assessed"]]
    weighted = _weighted_dimension_score(indicators)
    llm_dim = _accept_llm_dimension_score(raw_dim_score, graded)
    if llm_dim is not None:
        dim_score = float(llm_dim)
        score_source = "llm"
    else:
        dim_score = weighted if weighted is not None else 60.0
        score_source = "weighted_fallback"
        if not rationale:
            rationale = (
                "模型未给出有效的一级维度分（缺字段或超出已评二级分范围），"
                "改用二级指标加权平均。"
            )

    return {
        "key": dimension["key"],
        "label": dimension["label"],
        "description": dimension["description"],
        "weight": dimension.get("weight", 1.0),
        "score": dim_score,
        "weighted_score": weighted,
        "score_source": score_source,
        "dimension_rationale": rationale,
        "assessed": True,
        "skipped_count": len(skipped),
        **grade_of(dim_score),
        "indicators": indicators,
    }


def judge_all(
    evidence: dict, available: set[str] | None = None, progress_callback=None
) -> dict[str, Any]:
    """遍历五个一级维度，汇总成总分。未评估的维度不计入总分。"""
    rubric = get_rubric()
    dimensions = []

    for i, dim in enumerate(rubric["dimensions"]):
        dimensions.append(judge_dimension(dim, evidence, available))
        if progress_callback:
            progress_callback(i + 1, len(rubric["dimensions"]), dim["label"])

    graded = [d for d in dimensions if d["assessed"]]
    total_weight = sum(d["weight"] for d in graded) or 1.0
    overall_score = round(
        sum(d["score"] * d["weight"] for d in graded) / total_weight, 1
    )

    return {
        "overall": {
            "score": overall_score,
            **grade_of(overall_score),
            "duration_minutes": evidence.get("duration_minutes", 0),
            "modalities": sorted(available or {"text", "audio", "vision"}),
            "skipped_indicators": sum(
                1 for d in dimensions for i in d["indicators"] if not i["assessed"]
            ),
        },
        "dimensions": dimensions,
    }
