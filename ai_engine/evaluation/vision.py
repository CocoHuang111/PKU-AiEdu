"""视觉模态：让 VLM 逐帧输出结构化观测标签，再在本地聚合成比例型客观特征。

设计要点：**VLM 是观测员，不是评委**。它只回答「教师视线在看学生 / 屏幕 / 讲稿」，
由本地统计出「看讲稿帧占比 35%」这类数字，再交给 Judge 打分。
如果让 VLM 输出自由文本描述，视觉指标就只能靠 Judge 读一遍留个印象，
「看稿读屏行为少」这种本该可量化的指标会退化成印象分。
"""

from __future__ import annotations

import json
import re
from typing import Any

from ..pedagogy.loader import render_prompt
from ..providers import ProviderError, get_vlm

JSON_BLOCK = re.compile(r"\{[\s\S]*\}")

UNCLEAR = "unclear"

# 每个字段的合法取值。模型给出表外的值时归为 unclear，
# 否则一个臆造的标签会静默进入分母，把比例算错。
LABEL_SCHEMA: dict[str, tuple[str, ...]] = {
    "gaze": ("students", "screen", "script", "audience_away", UNCLEAR),
    "gesture": ("none", "pointing", "illustrative", "writing", UNCLEAR),
    "posture": ("standing_front", "walking", "behind_podium", "seated", UNCLEAR),
    "board_present": ("blackboard", "slide", "both", "none", UNCLEAR),
    "board_content": ("text_heavy", "diagram", "mixed", "none", UNCLEAR),
    "board_readable": ("high", "medium", "low", "none", UNCLEAR),
    "heads_up": ("high", "medium", "low", UNCLEAR),
    "hands_raised": ("yes", "no", UNCLEAR),
}

LABEL_TEXT: dict[str, dict[str, str]] = {
    "gaze": {
        "students": "看学生",
        "screen": "看屏幕",
        "script": "看讲稿",
        "audience_away": "背对学生",
        UNCLEAR: "视线不明",
    },
    "gesture": {
        "none": "无手势",
        "pointing": "指向板书",
        "illustrative": "讲解性手势",
        "writing": "正在书写",
        UNCLEAR: "手势不明",
    },
    "posture": {
        "standing_front": "讲台前",
        "walking": "走动中",
        "behind_podium": "讲台后",
        "seated": "坐姿",
        UNCLEAR: "站位不明",
    },
    "board_present": {
        "blackboard": "有板书",
        "slide": "有投影",
        "both": "板书+投影",
        "none": "无板书投影",
        UNCLEAR: "板书不明",
    },
    "board_content": {
        "text_heavy": "以文字为主",
        "diagram": "以图表为主",
        "mixed": "图文混排",
        "none": "无内容",
        UNCLEAR: "内容不明",
    },
    "board_readable": {
        "high": "可读性高",
        "medium": "可读性中",
        "low": "可读性低",
        "none": "无板书",
        UNCLEAR: "可读性不明",
    },
    "heads_up": {
        "high": "抬头率高",
        "medium": "抬头率中",
        "low": "抬头率低",
        UNCLEAR: "抬头率不明",
    },
    "hands_raised": {"yes": "有人举手", "no": "无人举手", UNCLEAR: "举手情况不明"},
}


def _parse_labels(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    parsed: Any = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        if match := JSON_BLOCK.search(text):
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                parsed = None
    if not isinstance(parsed, dict):
        raise ValueError(f"VLM 未返回合法 JSON：{raw[:120]}")

    labels: dict[str, Any] = {}
    for field, allowed in LABEL_SCHEMA.items():
        value = str(parsed.get(field, "")).strip().lower()
        labels[field] = value if value in allowed else UNCLEAR

    try:
        count = int(parsed.get("students_visible", -1))
    except (TypeError, ValueError):
        count = -1
    labels["students_visible"] = count if count >= 0 else None

    labels["note"] = str(parsed.get("note", "")).strip()[:60]
    return labels


def render_label_text(labels: dict[str, Any]) -> str:
    """把标签拼成一句中文，供前端展示和报告引用。"""
    parts = [
        LABEL_TEXT[field].get(labels.get(field, UNCLEAR), "")
        for field in ("gaze", "gesture", "posture", "board_present", "board_readable", "heads_up")
    ]
    if labels.get("students_visible") is not None:
        parts.append(f"可见学生 {labels['students_visible']} 人")
    if labels.get("hands_raised") == "yes":
        parts.append("有人举手")
    summary = " · ".join(p for p in parts if p)
    note = labels.get("note")
    return f"{summary}。{note}" if note else summary


def describe_keyframes(frames: list[dict], progress_callback=None) -> list[dict]:
    """逐帧标注。单帧失败不影响其余帧，失败的帧标记为不可用并排除在统计外。"""
    vlm = get_vlm()
    notes: list[dict] = []

    for i, frame in enumerate(frames):
        prompt = render_prompt("eval_vision.j2", timestamp=frame["timestamp"])
        labels: dict[str, Any] = {}
        try:
            raw = vlm.describe([frame["path"]], prompt)
            labels = _parse_labels(raw)
            description = render_label_text(labels)
            ok = True
        except ProviderError as e:
            description = f"（该帧分析失败：{e}）"
            ok = False
        except ValueError as e:
            description = f"（该帧标注格式错误：{e}）"
            ok = False

        notes.append(
            {
                "index": frame["index"],
                "timestamp": frame["timestamp"],
                "time_sec": frame["time_sec"],
                "path": frame["path"],
                "labels": labels,
                "description": description,
                "ok": ok,
            }
        )
        if progress_callback:
            progress_callback(i + 1, len(frames))

    return notes


def _ratio(values: list[str], wanted: tuple[str, ...]) -> float:
    if not values:
        return 0.0
    return round(100.0 * sum(1 for v in values if v in wanted) / len(values), 1)


def aggregate_vision_features(notes: list[dict]) -> dict[str, float]:
    """把逐帧标签聚合成比例型客观特征。

    unclear 的帧留在分母里，并单独报出 unclear 占比：把看不清的帧悄悄剔除
    会让「看学生占比」虚高，Judge 无从知道这个数字建立在几帧证据上。
    """
    labeled = [n["labels"] for n in notes if n.get("ok") and n.get("labels")]
    if not labeled:
        return {}

    def col(field: str) -> list[str]:
        return [str(lb.get(field, UNCLEAR)) for lb in labeled]

    counts = [
        lb["students_visible"]
        for lb in labeled
        if lb.get("students_visible") is not None
    ]

    features: dict[str, float] = {
        "frames_analyzed": len(labeled),
        "gaze_students_ratio": _ratio(col("gaze"), ("students",)),
        "gaze_script_ratio": _ratio(col("gaze"), ("script",)),
        "gaze_screen_ratio": _ratio(col("gaze"), ("screen", "audience_away")),
        "gaze_unclear_ratio": _ratio(col("gaze"), (UNCLEAR,)),
        "gesture_active_ratio": _ratio(
            col("gesture"), ("pointing", "illustrative", "writing")
        ),
        "walking_ratio": _ratio(col("posture"), ("standing_front", "walking")),
        "board_present_ratio": _ratio(
            col("board_present"), ("blackboard", "slide", "both")
        ),
        "board_diagram_ratio": _ratio(col("board_content"), ("diagram", "mixed")),
        "board_readable_high_ratio": _ratio(col("board_readable"), ("high",)),
        "board_readable_low_ratio": _ratio(col("board_readable"), ("low",)),
        "heads_up_high_ratio": _ratio(col("heads_up"), ("high",)),
        "heads_up_unclear_ratio": _ratio(col("heads_up"), (UNCLEAR,)),
        "hands_raised_frame_ratio": _ratio(col("hands_raised"), ("yes",)),
    }
    if counts:
        features["students_visible_median"] = sorted(counts)[len(counts) // 2]
    return features


COURSEWARE_LABEL_SCHEMA: dict[str, tuple[str, ...]] = {
    "layout": ("clear", "cluttered", "mixed", UNCLEAR),
    "density": ("sparse", "moderate", "text_heavy", UNCLEAR),
    "content": ("text_heavy", "diagram", "mixed", "none", UNCLEAR),
    "readable": ("high", "medium", "low", UNCLEAR),
}

COURSEWARE_LABEL_TEXT: dict[str, dict[str, str]] = {
    "layout": {
        "clear": "版式清楚",
        "cluttered": "版式拥挤",
        "mixed": "版式一般",
        UNCLEAR: "版式不明",
    },
    "density": {
        "sparse": "留白充足",
        "moderate": "密度适中",
        "text_heavy": "文字过密",
        UNCLEAR: "密度不明",
    },
    "content": {
        "text_heavy": "以文字为主",
        "diagram": "以图表为主",
        "mixed": "图文混排",
        "none": "几乎空白",
        UNCLEAR: "内容不明",
    },
    "readable": {
        "high": "可读性高",
        "medium": "可读性中",
        "low": "可读性低",
        UNCLEAR: "可读性不明",
    },
}


def _parse_courseware_labels(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    parsed: Any = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        if match := JSON_BLOCK.search(text):
            try:
                parsed = json.loads(match.group())
            except json.JSONDecodeError:
                parsed = None
    if not isinstance(parsed, dict):
        raise ValueError(f"VLM 未返回合法 JSON：{raw[:120]}")

    labels: dict[str, Any] = {}
    for field, allowed in COURSEWARE_LABEL_SCHEMA.items():
        value = str(parsed.get(field, "")).strip().lower()
        labels[field] = value if value in allowed else UNCLEAR
    labels["note"] = str(parsed.get("note", "")).strip()[:80]
    return labels


def render_courseware_label_text(labels: dict[str, Any]) -> str:
    parts = [
        COURSEWARE_LABEL_TEXT[field].get(labels.get(field, UNCLEAR), "")
        for field in ("layout", "density", "content", "readable")
    ]
    summary = " · ".join(p for p in parts if p)
    note = labels.get("note")
    return f"{summary}。{note}" if note else summary


def describe_courseware_pages(pages: list[dict], progress_callback=None) -> list[dict]:
    """对上传课件的渲染页做结构化标注。单页失败不影响其余页。"""
    vlm = get_vlm()
    notes: list[dict] = []
    total = len(pages)

    for i, page in enumerate(pages):
        prompt = render_prompt(
            "eval_courseware.j2",
            page=page.get("page", i + 1),
            page_count=page.get("page_count", total),
        )
        labels: dict[str, Any] = {}
        try:
            raw = vlm.describe([page["path"]], prompt)
            labels = _parse_courseware_labels(raw)
            description = render_courseware_label_text(labels)
            ok = True
        except ProviderError as e:
            description = f"（该页分析失败：{e}）"
            ok = False
        except ValueError as e:
            description = f"（该页标注格式错误：{e}）"
            ok = False

        notes.append(
            {
                "index": page.get("index", i),
                "page": page.get("page", i + 1),
                "page_count": page.get("page_count", total),
                "path": page["path"],
                "labels": labels,
                "description": description,
                "ok": ok,
            }
        )
        if progress_callback:
            progress_callback(i + 1, total)

    return notes


def aggregate_courseware_features(notes: list[dict]) -> dict[str, float]:
    labeled = [n["labels"] for n in notes if n.get("ok") and n.get("labels")]
    if not labeled:
        return {}

    def col(field: str) -> list[str]:
        return [str(lb.get(field, UNCLEAR)) for lb in labeled]

    return {
        "courseware_pages_analyzed": len(labeled),
        "cw_layout_clear_ratio": _ratio(col("layout"), ("clear",)),
        "cw_layout_cluttered_ratio": _ratio(col("layout"), ("cluttered",)),
        "cw_density_heavy_ratio": _ratio(col("density"), ("text_heavy",)),
        "cw_diagram_ratio": _ratio(col("content"), ("diagram", "mixed")),
        "cw_readable_high_ratio": _ratio(col("readable"), ("high",)),
        "cw_readable_low_ratio": _ratio(col("readable"), ("low",)),
    }

