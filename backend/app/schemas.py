from __future__ import annotations

from pydantic import BaseModel, Field


class TranscriptForm(BaseModel):
    text: str = Field(..., min_length=10, description="课堂转写文本")
    duration_sec: float = Field(2700, gt=0, description="课堂时长（秒），默认 45 分钟")
    reference: str | None = Field(
        None,
        description="课程大纲（选填）。有则对照大纲安排评本节课完整性，没有则根据转写评闭环",
    )


class QAForm(BaseModel):
    question: str = Field(..., min_length=1)
    session_id: str | None = None
    corpora: list[str] | None = Field(
        None, description="限定检索的语料库；为空则由模型自动路由"
    )


class SyllabusTextForm(BaseModel):
    text: str = Field(..., min_length=10)
    prompt_mode: str | None = Field(
        None,
        description=(
            "adaptive（灵活 XML）| schema（固定 XML 框架）| "
            "markdown（灵活 Markdown）| markdown_schema（固定 Markdown 框架）；"
            "默认读 config.yaml"
        ),
    )
