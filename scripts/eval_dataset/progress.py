"""CLI 进度条：ASR / VLM / Judge 等长步骤在同一行刷新，短步骤各打一行。"""

from __future__ import annotations

import sys
from typing import Any, TextIO

STEP_LABELS = {
    "queued": "排队中",
    "starting": "准备中",
    "extracting_audio": "抽取音频",
    "parse_materials": "解析材料",
    "keyframe_sampling": "抽取关键帧",
    "asr": "语音识别",
    "objective_features": "客观特征",
    "slide_detection": "课件切换",
    "diarization": "说话人分离",
    "vlm_describe": "视觉分析",
    "llm_judge": "五维评分",
    "report": "生成报告",
    "done": "完成",
    "failed": "失败",
    "cancelled": "已停止",
}

# 回调很密，TTY 上用 \r 刷新；非 TTY 按百分比节流。
BUSY_STEPS = frozenset({"asr", "vlm_describe", "llm_judge"})


def step_label(step: str) -> str:
    return STEP_LABELS.get(step, step)


def format_extra(step: str, detail: dict[str, Any] | None) -> str:
    detail = detail or {}
    if step == "asr" and detail.get("phase") == "punctuate":
        return "补标点"
    if step == "asr" and detail.get("total_sec"):
        done = int(detail.get("done_sec") or 0)
        total = int(detail["total_sec"])
        return f"{done // 60}/{max(total // 60, 1)} 分钟"
    if step == "slide_detection" and detail.get("phase") == "roi":
        return "定位投影"
    if step == "vlm_describe" and detail.get("total"):
        suffix = " 课件" if detail.get("kind") == "courseware" else ""
        return f"{int(detail.get('done') or 0)}/{int(detail['total'])}{suffix}"
    if step == "llm_judge" and detail.get("dimension"):
        return str(detail["dimension"])
    if step == "parse_materials" and detail.get("kind"):
        return str(detail["kind"])
    skip = {"warning", "done", "total", "done_sec", "total_sec", "dimension", "kind", "phase"}
    return " ".join(f"{k}={v}" for k, v in detail.items() if k not in skip and v is not None)


def format_progress_line(
    pct: int,
    step: str,
    detail: dict[str, Any] | None = None,
    *,
    width: int = 22,
    indent: str = "  ",
    fill: str = "█",
    empty: str = "░",
) -> str:
    pct = max(0, min(100, int(pct)))
    filled = int(round(width * pct / 100))
    bar = fill * filled + empty * (width - filled)
    extra = format_extra(step, detail)
    extra_s = f"  {extra}" if extra else ""
    return f"{indent}{step_label(step):<8} [{bar}] {pct:3d}%{extra_s}"


def _bar_glyphs(stream: TextIO) -> tuple[str, str]:
    enc = getattr(stream, "encoding", None) or "utf-8"
    try:
        "█░".encode(enc)
        return "█", "░"
    except LookupError:
        return "#", "-"
    except UnicodeEncodeError:
        return "#", "-"


class CliProgress:
    """pipeline 的 progress(pct, step, detail) 回调。"""

    def __init__(self, stream: TextIO | None = None, width: int = 22, indent: str = "  "):
        self.stream = stream or sys.stdout
        self.width = width
        self.indent = indent
        self._fill, self._empty = _bar_glyphs(self.stream)
        self._tty = bool(getattr(self.stream, "isatty", lambda: False)())
        self._step: str | None = None
        self._open = False
        self._last_bucket = -1

    def __call__(self, pct: int, step: str, detail: dict | None = None) -> None:
        detail = detail or {}
        warning = detail.get("warning")
        if warning:
            self.finish()
            self.stream.write(f"{self.indent}⚠ {step_label(step)}: {warning}\n")
            self.stream.flush()
            return

        if step != self._step:
            self.finish()
            self._step = step
            self._last_bucket = -1

        line = format_progress_line(
            pct,
            step,
            detail,
            width=self.width,
            indent=self.indent,
            fill=self._fill,
            empty=self._empty,
        )
        busy = step in BUSY_STEPS
        if busy and self._tty:
            self.stream.write(f"\r{line}\033[K")
            self.stream.flush()
            self._open = True
            if pct >= 100:
                self.finish()
            return

        if busy and not self._tty:
            bucket = int(pct) // 10
            if bucket == self._last_bucket:
                return
            self._last_bucket = bucket

        self.stream.write(line + "\n")
        self.stream.flush()
        self._open = False

    def finish(self) -> None:
        if self._open:
            self.stream.write("\n")
            self.stream.flush()
            self._open = False
        self._step = None
        self._last_bucket = -1
