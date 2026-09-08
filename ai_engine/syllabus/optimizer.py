"""功能② 教学大纲优化 Agent。

文档解析 → LLM 按 schema 生成优化后的 XML → lxml 校验，不合法就带报错信息让模型自修。
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from lxml import etree

from ..config import settings
from ..pedagogy.loader import read_schema_file, render_prompt
from ..providers import ChatMessage, ProviderError, get_llm
from ..rag import load_document
from .exceptions import SyllabusCancelled

ProgressFn = Callable[[int, str, dict[str, Any] | None], None]
CancelFn = Callable[[], bool]

SYSTEM = "你是课程与教学论专家。你只输出合法的 XML 文档，不输出任何解释文字。"
MARKDOWN_SYSTEM = (
    "你是课程与教学论专家。你只输出完整的 Markdown 大纲文档，不输出任何解释文字。"
    "文档必须含有 Markdown 标题行（# / ## / ###），否则校验失败。"
)
MARKDOWN_TEMPLATES = {
    "syllabus_optimize_markdown.j2",
    "syllabus_optimize_markdown_schema.j2",
}
MAX_REPAIR_ATTEMPTS = 2
MAX_BATCH_REPAIR_ATTEMPTS = 3

ORIGIN_VALUES = {"original", "clarified", "added"}
BLOOM_LEVELS = {"记忆", "理解", "应用", "分析", "评价", "创造"}
ACTIVITY_TYPES = {"讲授", "讨论", "实验", "案例", "习题", "汇报", "实践", "其他"}
ACTIVITY_TYPE_ALIASES = {
    "研讨": "讨论",
    "小组讨论": "讨论",
    "课堂讨论": "讨论",
    "案例教学": "案例",
    "案例分析": "案例",
    "上机": "实验",
    "上机实验": "实验",
    "实验课": "实验",
    "练习": "习题",
    "课堂练习": "习题",
    "讲解": "讲授",
    "授课": "讲授",
    "课堂讲授": "讲授",
    "演示": "讲授",
    "教学": "讲授",
    "展示": "汇报",
    "答辩": "汇报",
    "演讲": "汇报",
    "项目实践": "实践",
    "实训": "实践",
    "实习": "实践",
    "翻转课堂": "讨论",
    "探究": "讨论",
}
ACTIVITY_TYPE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("案例", ("案例",)),
    ("讨论", ("讨论", "研讨")),
    ("实验", ("实验", "上机")),
    ("习题", ("习题", "练习")),
    ("汇报", ("汇报", "答辩", "展示", "演讲")),
    ("实践", ("实践", "实训", "实习")),
    ("讲授", ("讲授", "授课", "讲解", "演示", "教学")),
)
ASSESSMENT_TYPES = {
    "平时表现",
    "作业",
    "实验",
    "期中",
    "期末",
    "大作业",
    "汇报",
    "项目",
    "其他",
}
ASSESSMENT_TYPE_ALIASES = {
    "课程项目": "项目",
    "小组项目": "项目",
    "研究项目": "项目",
    "综合项目": "项目",
    "课堂参与": "平时表现",
    "课堂表现": "平时表现",
    "出勤": "平时表现",
    "考勤": "平时表现",
    "讨论参与": "平时表现",
    "平时成绩": "平时表现",
    "平时分": "平时表现",
    "过程性评价": "平时表现",
    "过程性考核": "平时表现",
    "学习过程": "平时表现",
    "报告": "大作业",
    "实验报告": "大作业",
    "课程论文": "大作业",
    "论文": "大作业",
    "小论文": "大作业",
    "设计": "大作业",
    "课程设计": "大作业",
    "展示": "汇报",
    "答辩": "汇报",
    "演讲": "汇报",
    "演示": "汇报",
    "期末考试": "期末",
    "期末考": "期末",
    "期末考核": "期末",
    "期末测验": "期末",
    "闭卷考试": "期末",
    "开卷考试": "期末",
    "笔试": "期末",
    "期中考试": "期中",
    "期中考": "期中",
    "期中考核": "期中",
    "随堂测验": "作业",
    "小测": "作业",
    "测验": "作业",
    "在线作业": "作业",
    "平时作业": "作业",
    "实验课": "实验",
    "上机实验": "实验",
    "上机": "实验",
    "实践": "其他",
    "综合考核": "其他",
    "总评": "其他",
}
# 按优先级匹配：先匹配更具体的考核类型关键词
ASSESSMENT_TYPE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("期末", ("期末",)),
    ("期中", ("期中",)),
    ("平时表现", ("平时", "过程性", "出勤", "考勤", "参与", "课堂表现")),
    ("实验", ("实验", "上机")),
    ("项目", ("项目", "课程设计")),
    ("大作业", ("大作业", "论文", "报告", "设计")),
    ("汇报", ("汇报", "答辩", "展示", "演讲")),
    ("作业", ("作业", "测验", "小测")),
)
# 下列校验错误不走 LLM 整篇自修；其余校验失败默认尝试自修（黑名单制）
SKIP_LLM_REPAIR_MARKERS: tuple[str, ...] = (
    # 分阶段漏章/乱序应重新生成，整篇 patch 易超时且难补全
    "章节 source_id 覆盖或顺序错误",
)
REFERENCE_TYPES = {"教材", "参考书", "论文", "网络资源", "其他"}
_BARE_AMPERSAND = re.compile(
    r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)"
)
ROOT_SECTIONS = {
    "course",
    "objectives",
    "chapters",
    "assessment",
    "references",
    "additional_sections",
    "needs_confirmation",
    "improvements",
}
OPTIONAL_ROOT_SECTIONS = {"ai_integration"}


def _report_progress(
    progress: ProgressFn | None,
    is_cancelled: CancelFn | None,
    pct: int,
    step: str,
    detail: dict[str, Any] | None = None,
) -> None:
    if is_cancelled and is_cancelled():
        raise SyllabusCancelled()
    if progress:
        progress(pct, step, detail or {})


class StagedGenerationError(RuntimeError):
    """分阶段生成的中间结构不可用，可安全降级为单轮生成。"""


@dataclass(frozen=True)
class SourceChapter:
    source_id: str
    index: str
    title: str
    start_marker: str
    hours: str
    source_content: str


def _sanitize_llm_xml(xml: str) -> str:
    """把正文中未转义的 & 补成 &amp;，避免 xmlParseEntityRef 导致整篇无法解析。"""
    return _BARE_AMPERSAND.sub("&amp;", xml)


def _parse_xml_root(xml: str) -> tuple[etree._Element | None, str]:
    last_error = ""
    for candidate in (xml, _sanitize_llm_xml(xml)):
        try:
            return etree.fromstring(candidate.encode("utf-8")), ""
        except etree.XMLSyntaxError as e:
            last_error = str(e)
    return None, last_error


def _strip_wrapper(raw: str) -> str:
    """去掉模型可能加上的 markdown 代码块和前后废话。"""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    # 截到第一个 XML 声明或根标签
    for marker in ("<?xml", "<course_syllabus", "<syllabus"):
        if (pos := text.find(marker)) > 0:
            text = text[pos:]
            break
    for closing in ("</course_syllabus>", "</syllabus>"):
        if (pos := text.rfind(closing)) != -1:
            text = text[: pos + len(closing)]
            break
    return _sanitize_llm_xml(text.strip())


def _is_markdown_template(template: str) -> bool:
    return template in MARKDOWN_TEMPLATES


def _strip_markdown_wrapper(raw: str) -> str:
    """去掉模型可能加上的 markdown 代码块和标题前的废话。

    已经以标题开头的正文不能再切：后面的 ``## `` 是文档结构，
    从那里切开会把一级标题（课程名）丢掉。
    """
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    if re.match(r"^#{1,6}\s+\S", text):
        return text
    if match := re.search(r"^#{1,6}\s+\S", text, re.MULTILINE):
        text = text[match.start() :]
    return text.strip()


def _has_atx_heading(text: str) -> bool:
    return bool(re.search(r"^#{1,3}\s+\S", text.strip(), re.MULTILINE))


def _ensure_leading_atx(markdown: str) -> str:
    """Word/PDF 抽出来的节名常常没有 #。至少给首行非空短句补一级标题，避免整篇校验失败。"""
    text = markdown.strip()
    if not text or _has_atx_heading(text):
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            return text
        lines[i] = f"# {stripped}"
        return "\n".join(lines)
    return text


def _request_markdown(
    llm,
    prompt: str,
    error_prefix: str,
    *,
    timeout: float | None = None,
) -> str:
    try:
        chat_kwargs = {"timeout": timeout} if timeout is not None else {}
        return _strip_markdown_wrapper(
            llm.chat(
                [ChatMessage("system", MARKDOWN_SYSTEM), ChatMessage("user", prompt)],
                **chat_kwargs,
            )
        )
    except ProviderError as e:
        raise RuntimeError(f"{error_prefix}：{e}") from e


def validate_markdown(
    markdown: str, *, max_chars: int | None = None
) -> tuple[bool, str]:
    text = markdown.strip()
    if len(text) < 80:
        return False, "Markdown 内容过短"
    if not _has_atx_heading(text):
        return False, "Markdown 缺少标题结构"
    if max_chars is not None and len(text) > max_chars:
        return (
            True,
            f"提示：输出约 {len(text)} 字，超过建议上限 {max_chars} 字（原文 2 倍），内容可能偏长",
        )
    return True, ""


def detect_output_format(content: str) -> str:
    stripped = content.lstrip()
    if stripped.startswith(("<?xml", "<syllabus", "<course_syllabus")):
        return "xml"
    return "markdown"


def _request_xml(
    llm,
    prompt: str,
    error_prefix: str,
    *,
    timeout: float | None = None,
) -> str:
    try:
        chat_kwargs = {"timeout": timeout} if timeout is not None else {}
        return _strip_wrapper(
            llm.chat(
                [ChatMessage("system", SYSTEM), ChatMessage("user", prompt)],
                **chat_kwargs,
            )
        )
    except ProviderError as e:
        raise RuntimeError(f"{error_prefix}：{e}") from e


def _parse_staged_xml(xml: str, expected_root: str) -> etree._Element:
    root, error = _parse_xml_root(xml)
    if root is None:
        raise StagedGenerationError(f"<{expected_root}> XML 无法解析：{error}") from None
    if root.tag != expected_root:
        raise StagedGenerationError(
            f"中间结果根节点应为 <{expected_root}>，实际为 <{root.tag}>"
        )
    return root


def _normalize_match_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text.strip())


def _find_from_cursor(original_text: str, needle: str, cursor: int) -> int:
    if not needle:
        return -1
    pos = original_text.find(needle, cursor)
    if pos >= 0:
        return pos
    compact_needle = _normalize_match_text(needle)
    if not compact_needle:
        return -1
    chunk = original_text[cursor:]
    compact_chunk = _normalize_match_text(chunk)
    rel = compact_chunk.find(compact_needle)
    if rel < 0:
        return -1
    prefix = compact_needle[: min(24, len(compact_needle))]
    return original_text.find(prefix, cursor)


def _find_longest_prefix(
    original_text: str,
    needle: str,
    cursor: int,
    *,
    min_len: int = 12,
) -> tuple[int, int]:
    cleaned = needle.strip()
    for length in range(len(cleaned), min_len - 1, -1):
        pos = _find_from_cursor(original_text, cleaned[:length], cursor)
        if pos >= 0:
            return pos, length
    return -1, 0


def _locate_chapter_start(
    original_text: str,
    marker: str,
    title: str,
    cursor: int,
) -> tuple[int, int, str]:
    for label, candidate in (("marker", marker), ("title", title)):
        if not candidate:
            continue
        pos = _find_from_cursor(original_text, candidate, cursor)
        if pos >= 0:
            return pos, len(candidate.strip()), label
        pos, matched_len = _find_longest_prefix(original_text, candidate, cursor)
        if pos >= 0:
            return pos, matched_len, f"{label}_prefix"
    return -1, 0, ""


def _parse_chapter_index(
    index_xml: str,
    original_text: str,
    max_chapters: int,
) -> tuple[etree._Element, list[SourceChapter]]:
    root = _parse_staged_xml(index_xml, "chapter_index")
    nodes = root.findall("chapter")
    if not nodes:
        raise StagedGenerationError("章节索引为空")
    if len(nodes) > max_chapters:
        raise StagedGenerationError(
            f"识别到 {len(nodes)} 个章节，超过分阶段上限 {max_chapters}"
        )

    metadata: list[tuple[str, str, str, str, str, int]] = []
    cursor = 0
    seen_ids: set[str] = set()
    for order, node in enumerate(nodes, 1):
        source_id = (node.get("source_id") or "").strip()
        index = (node.get("index") or str(order)).strip()
        title = _node_text(node.find("title"))
        marker = _node_text(node.find("start_marker"))
        hours = _node_text(node.find("hours")) or "待教师确认"
        if not source_id or source_id in seen_ids:
            raise StagedGenerationError("章节 source_id 缺失或重复")
        if source_id != f"S{order}":
            raise StagedGenerationError(
                f"章节 source_id 应按顺序为 S{order}，实际为 {source_id}"
            )
        if not title or not marker:
            raise StagedGenerationError(f"{source_id} 缺少 title 或 start_marker")
        position, matched_len, _match_mode = _locate_chapter_start(
            original_text, marker, title, cursor
        )
        if position < 0:
            raise StagedGenerationError(
                f"{source_id} 的定位文本未在原文中找到：{marker[:40]}"
            )
        metadata.append((source_id, index, title, marker, hours, position))
        seen_ids.add(source_id)
        cursor = position + max(1, matched_len)

    chapters: list[SourceChapter] = []
    for order, (source_id, index, title, marker, hours, start) in enumerate(metadata):
        end = (
            metadata[order + 1][5]
            if order + 1 < len(metadata)
            else len(original_text)
        )
        source_content = original_text[start:end].strip()
        if not source_content:
            raise StagedGenerationError(f"{source_id} 切分后的原文内容为空")
        chapters.append(
            SourceChapter(
                source_id=source_id,
                index=index,
                title=title,
                start_marker=marker,
                hours=hours,
                source_content=source_content,
            )
        )
    return root, chapters


def _source_chapters_xml(chapters: list[SourceChapter]) -> str:
    root = etree.Element("source_chapters")
    for chapter in chapters:
        node = etree.SubElement(
            root,
            "chapter",
            source_id=chapter.source_id,
            index=chapter.index,
        )
        etree.SubElement(node, "title").text = chapter.title
        etree.SubElement(node, "hours").text = chapter.hours
        etree.SubElement(node, "source_content").text = chapter.source_content
    return etree.tostring(root, encoding="unicode", pretty_print=True)


def _chapter_schema_xml(schema: str) -> str:
    schema_root = _parse_staged_xml(schema, "syllabus")
    chapter = schema_root.find("chapters/chapter")
    if chapter is None:
        raise StagedGenerationError("syllabus_schema.xml 缺少章节模板")
    return etree.tostring(chapter, encoding="unicode", pretty_print=True)


def _course_context_xml(syllabus: etree._Element) -> str:
    context = etree.Element("course_context")
    for name in ("course", "objectives", "assessment"):
        node = syllabus.find(name)
        if node is not None:
            context.append(etree.fromstring(etree.tostring(node)))
    return etree.tostring(context, encoding="unicode", pretty_print=True)


def _parse_global_skeleton(xml: str) -> etree._Element:
    root = _parse_staged_xml(xml, "syllabus")
    chapters = root.find("chapters")
    if chapters is None:
        raise StagedGenerationError("全局骨架缺少 <chapters>")
    for child in list(chapters):
        chapters.remove(child)
    return root


def _parse_chapter_batch(
    xml: str,
    expected: list[SourceChapter],
) -> list[etree._Element]:
    root = _parse_staged_xml(xml, "chapters")
    generated: dict[str, etree._Element] = {}
    for chapter in root.findall("chapter"):
        source_id = (chapter.get("source_id") or "").strip()
        if not source_id or source_id in generated:
            raise StagedGenerationError("分章结果的 source_id 缺失或重复")
        generated[source_id] = chapter

    expected_ids = {chapter.source_id for chapter in expected}
    if set(generated) != expected_ids:
        missing = sorted(expected_ids - set(generated))
        extra = sorted(set(generated) - expected_ids)
        raise StagedGenerationError(
            f"分章覆盖不完整，缺少 {missing or '无'}，多出 {extra or '无'}"
        )

    ordered: list[etree._Element] = []
    for source in expected:
        chapter = generated[source.source_id]
        chapter.set("source_id", source.source_id)
        chapter.set("index", source.index)
        title = chapter.find("title")
        if title is None:
            title = etree.Element("title")
            chapter.insert(0, title)
        title.text = source.title
        if source.hours != "待教师确认":
            hours = chapter.find("hours")
            if hours is None:
                hours = etree.Element("hours")
                chapter.insert(1, hours)
            hours.text = source.hours
        ordered.append(chapter)
    return ordered


def _generate_single_xml(
    llm,
    template: str,
    prompt_kwargs: dict[str, Any],
    *,
    timeout: float | None = None,
) -> str:
    prompt = render_prompt(template, **prompt_kwargs)
    return _request_xml(llm, prompt, "大纲优化失败", timeout=timeout)


def _generate_single_markdown(
    llm,
    template: str,
    prompt_kwargs: dict[str, Any],
    *,
    timeout: float | None = None,
) -> str:
    prompt = render_prompt(template, **prompt_kwargs)
    return _request_markdown(llm, prompt, "大纲优化失败", timeout=timeout)


def _generate_staged_schema_xml(
    llm,
    original_text: str,
    schema: str,
    *,
    batch_size: int,
    max_chapters: int,
) -> tuple[str, list[str]]:
    index_prompt = render_prompt(
        "syllabus_extract_chapters.j2", original_text=original_text
    )
    index_xml = _request_xml(llm, index_prompt, "大纲章节抽取失败")
    index_root, source_chapters = _parse_chapter_index(
        index_xml, original_text, max_chapters
    )
    normalized_index = etree.tostring(
        index_root, encoding="unicode", pretty_print=True
    )

    global_prompt = render_prompt(
        "syllabus_optimize_global.j2",
        schema=schema,
        chapter_index=normalized_index,
        original_text=original_text,
    )
    global_xml = _request_xml(llm, global_prompt, "大纲全局结构生成失败")
    syllabus = _parse_global_skeleton(global_xml)
    chapters_node = syllabus.find("chapters")
    if chapters_node is None:  # pragma: no cover - 已在 _parse_global_skeleton 检查
        raise StagedGenerationError("全局骨架缺少 <chapters>")

    chapter_schema = _chapter_schema_xml(schema)
    course_context = _course_context_xml(syllabus)
    size = max(1, batch_size)
    for start in range(0, len(source_chapters), size):
        batch = source_chapters[start : start + size]
        chapter_prompt = render_prompt(
            "syllabus_optimize_chapters.j2",
            chapter_schema=chapter_schema,
            course_context=course_context,
            source_chapters=_source_chapters_xml(batch),
        )
        batch_xml = _request_xml(llm, chapter_prompt, "大纲分章优化失败")
        batch_attempts = 0
        required_ids = ", ".join(chapter.source_id for chapter in batch)
        while True:
            try:
                parsed = _parse_chapter_batch(batch_xml, batch)
                break
            except StagedGenerationError as e:
                batch_attempts += 1
                err_msg = str(e)
                if batch_attempts > MAX_BATCH_REPAIR_ATTEMPTS:
                    raise
                if any(
                    marker in err_msg.lower()
                    for marker in (
                        "xml 无法解析",
                        "invalid element",
                        "xmlparseentityref",
                        "xmlparse",
                    )
                ):
                    repair = render_prompt(
                        "syllabus_repair.j2",
                        error=err_msg,
                        broken_xml=batch_xml,
                        schema=chapter_schema,
                    )
                    batch_xml = _request_xml(llm, repair, "大纲分章修复失败")
                else:
                    retry_prompt = (
                        f"{chapter_prompt}\n\n"
                        f"## 上次输出错误\n{err_msg}\n\n"
                        f"必须且只能输出 source_id 为 {required_ids} 的 <chapter>，"
                        "每个 source_id 恰好一个，不要遗漏也不要额外增加。"
                    )
                    batch_xml = _request_xml(
                        llm, retry_prompt, "大纲分章优化失败"
                    )
        for chapter in parsed:
            chapters_node.append(chapter)

    assembled_ids = [
        (chapter.get("source_id") or "").strip()
        for chapter in chapters_node.findall("chapter")
    ]
    expected_ids = [chapter.source_id for chapter in source_chapters]
    if assembled_ids != expected_ids:
        raise StagedGenerationError(
            f"章节合并覆盖校验失败：预期 {expected_ids}，实际 {assembled_ids}"
        )

    return etree.tostring(syllabus, encoding="unicode"), expected_ids


def _validate_source_coverage(
    xml: str,
    expected_ids: list[str],
) -> tuple[bool, str]:
    root, error = _parse_xml_root(xml)
    if root is None:
        return False, f"XML 语法错误：{error}"
    actual_ids = [
        (chapter.get("source_id") or "").strip()
        for chapter in root.findall("chapters/chapter")
    ]
    if actual_ids != expected_ids:
        return (
            False,
            f"章节 source_id 覆盖或顺序错误：预期 {expected_ids}，实际 {actual_ids}",
        )
    return True, ""


def validate_xml(xml: str) -> tuple[bool, str]:
    _, error = _parse_xml_root(xml)
    if error:
        return False, f"XML 语法错误：{error}"
    return True, ""


def _node_text(node: etree._Element | None) -> str:
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def _decimal(value: str) -> Decimal | None:
    try:
        number = Decimal(value.strip().rstrip("%"))
        return number if number.is_finite() and number >= 0 else None
    except (InvalidOperation, AttributeError):
        return None


def _parse_hours_text(value: str) -> Decimal | None:
    """从纯数字或「约1.5 周」「2 学时」等表述中提取可比较的数值。"""
    text = (value or "").strip()
    if not text or text == "待教师确认":
        return None
    cleaned = re.sub(r"[约\s]", "", text)
    cleaned = re.sub(r"(周|次|课时|学时|小时|h)", "", cleaned, flags=re.I)
    number = _decimal(cleaned)
    if number is not None:
        return number
    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if match:
        return _decimal(match.group(1))
    return None


def _resolve_activity_type(type_value: str) -> str:
    cleaned = re.sub(r"\s+", "", (type_value or "").strip())
    if not cleaned:
        return "其他"
    if cleaned in ACTIVITY_TYPES:
        return cleaned
    if cleaned in ACTIVITY_TYPE_ALIASES:
        return ACTIVITY_TYPE_ALIASES[cleaned]
    for canonical, keywords in ACTIVITY_TYPE_KEYWORDS:
        if any(keyword in cleaned for keyword in keywords):
            return canonical
    return "其他"


def _resolve_assessment_type(type_value: str) -> str | None:
    cleaned = re.sub(r"\s+", "", (type_value or "").strip())
    if not cleaned:
        return None
    if cleaned in ASSESSMENT_TYPES:
        return cleaned
    if cleaned in ASSESSMENT_TYPE_ALIASES:
        return ASSESSMENT_TYPE_ALIASES[cleaned]
    for canonical, keywords in ASSESSMENT_TYPE_KEYWORDS:
        if any(keyword in cleaned for keyword in keywords):
            return canonical
    return None


def _normalize_schema_enums(xml: str) -> str:
    """校验前将 activity/assessment 等的 type 规范到允许枚举，避免同义词导致失败。"""
    root, _ = _parse_xml_root(xml)
    if root is None or root.tag != "syllabus":
        return xml
    changed = False
    for activity in root.iter("activity"):
        if not isinstance(activity.tag, str):
            continue
        raw = activity.get("type") or ""
        resolved = _resolve_activity_type(raw)
        if resolved != raw:
            activity.set("type", resolved)
            changed = True
    assessment = root.find("assessment")
    if assessment is not None:
        for item in assessment.findall("item"):
            raw = item.get("type") or ""
            resolved = _resolve_assessment_type(raw) or "其他"
            if resolved != raw:
                item.set("type", resolved)
                changed = True
    if not changed:
        return xml
    try:
        return etree.tostring(
            root, pretty_print=True, encoding="unicode", xml_declaration=False
        )
    except etree.XMLSyntaxError:
        return xml


def _normalize_schema_assessment_types(xml: str) -> str:
    """兼容旧调用；请改用 _normalize_schema_enums。"""
    return _normalize_schema_enums(xml)


def _should_skip_llm_repair(error: str) -> bool:
    """除 SKIP_LLM_REPAIR_MARKERS 外，校验失败默认尝试 LLM 自修。"""
    if not error:
        return True
    return any(marker in error for marker in SKIP_LLM_REPAIR_MARKERS)


def _require_child(
    parent: etree._Element,
    name: str,
    path: str,
    errors: list[str],
) -> etree._Element | None:
    child = parent.find(name)
    if child is None:
        errors.append(f"{path} 缺少 <{name}>")
    return child


def _validate_origin(node: etree._Element, path: str, errors: list[str]) -> None:
    origin = node.get("origin")
    if origin not in ORIGIN_VALUES:
        errors.append(
            f"{path} 的 origin 必须是 original、clarified 或 added，当前为 {origin!r}"
        )


def validate_schema_xml(xml: str) -> tuple[bool, str]:
    """校验固定框架 XML 的结构、内容深度与可计算业务规则。"""
    root, parse_error = _parse_xml_root(xml)
    if root is None:
        return False, f"XML 语法错误：{parse_error}"

    errors: list[str] = []
    if root.tag != "syllabus":
        errors.append(f"根节点必须为 <syllabus>，当前为 <{root.tag}>")
        return False, "；".join(errors)

    actual_sections = {child.tag for child in root if isinstance(child.tag, str)}
    for section in ROOT_SECTIONS - actual_sections:
        errors.append(f"/syllabus 缺少 <{section}>")
    for section in actual_sections - ROOT_SECTIONS - OPTIONAL_ROOT_SECTIONS:
        errors.append(f"/syllabus 不允许根级节点 <{section}>")
    for section in ROOT_SECTIONS:
        if len(root.findall(section)) > 1:
            errors.append(f"/syllabus 根级节点 <{section}> 只能出现一次")

    course = root.find("course")
    if course is not None:
        for field in (
            "name",
            "code",
            "credits",
            "total_hours",
            "discipline",
            "audience",
            "prerequisites",
            "description",
        ):
            node = _require_child(course, field, "/syllabus/course", errors)
            if node is not None and not _node_text(node):
                errors.append(f"/syllabus/course/{field} 不能为空，可填写“待教师确认”")
        description = course.find("description")
        if description is not None:
            desc_len = len(_node_text(description))
            if desc_len > 200:
                errors.append("/syllabus/course/description 超过200字，大纲级简介应更简短")

    objectives = root.find("objectives")
    if objectives is not None:
        objective_nodes = objectives.findall("objective")
        if not objective_nodes:
            errors.append("/syllabus/objectives 至少需要一个 <objective>")
        for index, objective in enumerate(objective_nodes, 1):
            path = f"/syllabus/objectives/objective[{index}]"
            _validate_origin(objective, path, errors)
            if objective.get("level") not in BLOOM_LEVELS:
                errors.append(f"{path} 的 level 不在布鲁姆层次枚举中")
            statement_node = _require_child(objective, "statement", path, errors)
            if statement_node is not None and not _node_text(statement_node):
                errors.append(f"{path}/statement 不能为空")
            statement = _node_text(objective.find("statement"))
            if statement and not statement.startswith("学生能够"):
                errors.append(f"{path}/statement 必须以“学生能够”开头")

    chapter_hours: list[Decimal] = []
    all_chapter_hours_numeric = True
    any_chapter_uses_week = False
    chapters = root.find("chapters")
    if chapters is not None:
        chapter_nodes = chapters.findall("chapter")
        chapter_source_ids: set[str] = set()
        if not chapter_nodes:
            errors.append("/syllabus/chapters 至少需要一个 <chapter>")
        for chapter_index, chapter in enumerate(chapter_nodes, 1):
            path = f"/syllabus/chapters/chapter[{chapter_index}]"
            _validate_origin(chapter, path, errors)
            source_id = (chapter.get("source_id") or "").strip()
            if not re.fullmatch(r"S[1-9]\d*", source_id):
                errors.append(f"{path} 的 source_id 必须为 S1、S2……")
            elif source_id in chapter_source_ids:
                errors.append(f"{path} 的 source_id {source_id} 重复")
            else:
                chapter_source_ids.add(source_id)
            if not chapter.get("index"):
                errors.append(f"{path} 缺少 index 属性")
            required = {
                field: _require_child(chapter, field, path, errors)
                for field in ("title", "hours", "points")
            }
            for field in ("title", "hours"):
                if required[field] is not None and not _node_text(required[field]):
                    errors.append(f"{path}/{field} 不能为空")
            points = required["points"]
            point_nodes = points.findall("point") if points is not None else []
            if points is not None and not point_nodes:
                errors.append(f"{path}/points 至少需要一个 <point>")
            for point_index, point in enumerate(point_nodes, 1):
                point_path = f"{path}/points/point[{point_index}]"
                _validate_origin(point, point_path, errors)
                point_text = _node_text(point)
                if len(point_text) < 4:
                    errors.append(f"{point_path} 不能为空或过短")
            teaching_format = chapter.find("teaching_format")
            if teaching_format is not None and not _node_text(teaching_format):
                errors.append(f"{path}/teaching_format 若存在则不能为空")

            hours_text = _node_text(required["hours"])
            if "周" in hours_text:
                any_chapter_uses_week = True
            hours_value = _parse_hours_text(hours_text)
            if hours_value is None:
                all_chapter_hours_numeric = False
            else:
                chapter_hours.append(hours_value)

    ai_root = root.find("ai_integration")
    if ai_root is not None:
        _validate_origin(ai_root, "/syllabus/ai_integration", errors)
        summary = _require_child(ai_root, "summary", "/syllabus/ai_integration", errors)
        if summary is not None and not _node_text(summary):
            errors.append("/syllabus/ai_integration/summary 不能为空")

    assessment_weights: list[Decimal] = []
    all_weights_numeric = True
    assessment = root.find("assessment")
    if assessment is not None:
        for item_index, item in enumerate(assessment.findall("item"), 1):
            path = f"/syllabus/assessment/item[{item_index}]"
            _validate_origin(item, path, errors)
            if _resolve_assessment_type(item.get("type") or "") is None:
                errors.append(
                    f"{path} 的 type 不在允许枚举中（当前为 {item.get('type')!r}；"
                    f"允许：{', '.join(sorted(ASSESSMENT_TYPES))}）"
                )
            weight = item.get("weight", "")
            weight_value = _decimal(weight)
            if weight_value is None:
                all_weights_numeric = False
                if weight != "待教师确认":
                    errors.append(f"{path} 的 weight 必须是数字或“待教师确认”")
            else:
                assessment_weights.append(weight_value)
            description = _require_child(item, "description", path, errors)
            if description is not None and not _node_text(description):
                errors.append(f"{path}/description 不能为空")

    references = root.find("references")
    if references is not None:
        for reference_index, reference in enumerate(
            references.findall("reference"), 1
        ):
            path = f"/syllabus/references/reference[{reference_index}]"
            _validate_origin(reference, path, errors)
            if reference.get("type") not in REFERENCE_TYPES:
                errors.append(f"{path} 的 type 不在允许枚举中")
            if not _node_text(reference):
                errors.append(f"{path} 不能为空")

    additional_sections = root.find("additional_sections")
    if additional_sections is not None:
        for section_index, section in enumerate(
            additional_sections.findall("section"), 1
        ):
            path = f"/syllabus/additional_sections/section[{section_index}]"
            _validate_origin(section, path, errors)
            if not section.get("title"):
                errors.append(f"{path} 缺少 title 属性")
            content = _require_child(section, "content", path, errors)
            if content is not None and not _node_text(content):
                errors.append(f"{path}/content 不能为空")

    total_hours_node = root.find("course/total_hours")
    total_hours = _parse_hours_text(_node_text(total_hours_node))
    chapter_hours_sum = sum(chapter_hours) if chapter_hours else Decimal("0")
    likely_mixed_week_and_hour_units = (
        any_chapter_uses_week
        or (
            total_hours is not None
            and chapter_hours_sum > 0
            and chapter_hours_sum < total_hours / Decimal("2")
        )
    )
    if (
        not likely_mixed_week_and_hour_units
        and total_hours is not None
        and all_chapter_hours_numeric
        and chapter_hours
        and chapter_hours_sum != total_hours
    ):
        errors.append(
            f"章节学时合计 {chapter_hours_sum}，与总学时 {total_hours} 不一致"
        )
    if (
        all_weights_numeric
        and assessment_weights
        and sum(assessment_weights) != Decimal("100")
    ):
        errors.append(f"考核权重合计 {sum(assessment_weights)}，应为100")

    return not errors, "；".join(errors)


def prettify(xml: str) -> str:
    """格式化，并清掉 schema 里用于说明的脚手架属性。

    模板里的 repeatable="true" 是给模型看的"这个元素可重复"的标注，
    模型常会照抄到输出里。靠提示词约束不可靠，这里直接删掉。
    """
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(xml.encode("utf-8"), parser)
        for node in tree.iter():
            node.attrib.pop("repeatable", None)
        return etree.tostring(
            tree, pretty_print=True, encoding="unicode", xml_declaration=False
        )
    except etree.XMLSyntaxError:
        return xml


def extract_course_name(xml: str) -> str:
    try:
        tree = etree.fromstring(xml.encode("utf-8"))
        for xpath in (
            ".//course/name",
            ".//course_info/name",
            ".//course_name",
            ".//name",
        ):
            node = tree.find(xpath)
            if node is not None and node.text and node.text.strip():
                return node.text.strip()
    except etree.XMLSyntaxError:
        pass
    return "未命名课程"


def extract_course_name_from_markdown(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        title = re.sub(r"^#+\s*", "", stripped).strip()
        title = re.sub(r"^课程大纲\s*[·•\-—]\s*", "", title).strip()
        if title:
            return title
    match = re.search(r"\*\*课程名称\*\*[：:]\s*(.+)", markdown)
    if match:
        return match.group(1).strip()
    return "未命名课程"


def optimize_text(
    original_text: str,
    *,
    prompt_mode: str | None = None,
    progress: ProgressFn | None = None,
    is_cancelled: CancelFn | None = None,
) -> dict[str, Any]:
    conf = settings.section("syllabus")
    max_chars = conf.get("max_input_chars", 80000)
    text = original_text.strip()
    if not text:
        raise ValueError("大纲内容为空")
    truncated = len(text) > max_chars
    if truncated:
        text = text[:max_chars]

    _report_progress(progress, is_cancelled, 10, "generating")

    mode = (prompt_mode or conf.get("prompt_template", "syllabus_optimize.j2")).strip()
    if mode in ("adaptive", "flexible"):
        template = "syllabus_optimize.j2"
    elif mode in ("schema", "fixed"):
        template = "syllabus_optimize_schema.j2"
    elif mode in ("markdown", "markdown_adaptive", "md", "md_adaptive"):
        template = "syllabus_optimize_markdown.j2"
    elif mode in ("markdown_schema", "md_schema", "markdown_fixed"):
        template = "syllabus_optimize_markdown_schema.j2"
    elif mode.endswith(".j2"):
        template = mode
    else:
        template = conf.get("prompt_template", "syllabus_optimize.j2")

    markdown_mode = _is_markdown_template(template)
    original_char_count = len(text)
    length_ratio = float(conf.get("markdown_max_length_ratio", 2.0))
    max_output_chars = max(int(original_char_count * length_ratio), 800)
    prompt_kwargs: dict[str, Any] = {
        "original_text": text,
        "original_char_count": original_char_count,
        "max_output_chars": max_output_chars,
    }
    if template == "syllabus_optimize_schema.j2":
        prompt_kwargs["schema"] = read_schema_file(
            conf.get("schema_file", "syllabus_schema.xml")
        )
    elif template == "syllabus_optimize_markdown_schema.j2":
        prompt_kwargs["schema"] = read_schema_file(
            conf.get("markdown_schema_file", "syllabus_markdown_schema.md")
        )

    llm = get_llm()
    raw_llm_timeout = conf.get("llm_timeout")
    llm_timeout = float(raw_llm_timeout) if raw_llm_timeout is not None else None
    generation_strategy = "single"
    staged_fallback_reason = ""
    expected_source_ids: list[str] = []

    if markdown_mode:
        markdown = _generate_single_markdown(
            llm, template, prompt_kwargs, timeout=llm_timeout
        )
        markdown = _ensure_leading_atx(markdown)
        _report_progress(progress, is_cancelled, 82, "validating")
        valid, error = validate_markdown(markdown, max_chars=max_output_chars)
        attempts = 0
        while not valid and attempts < MAX_REPAIR_ATTEMPTS:
            if "过短" in error:
                break
            attempts += 1
            _report_progress(
                progress,
                is_cancelled,
                min(88 + attempts * 4, 94),
                "repairing",
                {"attempt": attempts},
            )
            repair = (
                f"下面这份 Markdown 大纲校验失败：{error}\n\n"
                "请只做最小修改后重新输出**全文**：\n"
                "- 给课程名和各原有栏目补上 Markdown 标题（# / ## / ###），标题用词与原文一致；\n"
                "- 不要把段落改成列表，不要改写题记、引语和正文事实；\n"
                "- 不要用代码块包裹，不要在前后加说明。\n\n"
                f"{markdown}"
            )
            try:
                markdown = _ensure_leading_atx(
                    _request_markdown(
                        llm, repair, "大纲自动修复失败", timeout=llm_timeout
                    )
                )
            except RuntimeError:
                break
            valid, error = validate_markdown(markdown, max_chars=max_output_chars)
        xml = markdown
        repair_attempts = attempts
    else:
        use_staged = (
            template == "syllabus_optimize_schema.j2"
            and str(conf.get("generation_strategy", "single")).lower() == "staged"
        )
        if use_staged:
            try:
                xml, expected_source_ids = _generate_staged_schema_xml(
                    llm,
                    text,
                    prompt_kwargs["schema"],
                    batch_size=int(conf.get("chapter_batch_size", 3)),
                    max_chapters=int(conf.get("max_staged_chapters", 30)),
                )
                generation_strategy = "staged"
            except StagedGenerationError as e:
                allow_single_fallback = conf.get("staged_fallback_to_single", True) and (
                    "定位文本未在原文中找到" in str(e)
                    or "章节索引为空" in str(e)
                    or ("识别到" in str(e) and "超过分阶段上限" in str(e))
                    or "chapter_index" in str(e)
                )
                if not allow_single_fallback:
                    raise RuntimeError(f"大纲分阶段生成失败：{e}") from e
                staged_fallback_reason = str(e)
                generation_strategy = "single_fallback"
                xml = _generate_single_xml(
                    llm, template, prompt_kwargs, timeout=llm_timeout
                )
        else:
            xml = _generate_single_xml(
                llm, template, prompt_kwargs, timeout=llm_timeout
            )

        _report_progress(progress, is_cancelled, 78, "generating")
        xml = _sanitize_llm_xml(xml)
        if template == "syllabus_optimize_schema.j2":
            xml = _normalize_schema_enums(xml)
        _report_progress(progress, is_cancelled, 82, "validating")

        def validator(candidate: str) -> tuple[bool, str]:
            if template != "syllabus_optimize_schema.j2":
                return validate_xml(candidate)
            valid, validation_error = validate_schema_xml(candidate)
            if not valid:
                return valid, validation_error
            if expected_source_ids:
                return _validate_source_coverage(candidate, expected_source_ids)
            return True, ""

        valid, error = validator(xml)
        attempts = 0
        repair_aborted = ""
        while not valid and attempts < MAX_REPAIR_ATTEMPTS:
            if _should_skip_llm_repair(error):
                break
            attempts += 1
            _report_progress(
                progress,
                is_cancelled,
                min(88 + attempts * 4, 94),
                "repairing",
                {"attempt": attempts},
            )
            repair = render_prompt(
                "syllabus_repair.j2",
                error=error,
                broken_xml=xml,
                schema=prompt_kwargs.get("schema"),
            )
            try:
                chat_kwargs = {"timeout": llm_timeout} if llm_timeout is not None else {}
                xml = _strip_wrapper(
                    llm.chat(
                        [ChatMessage("system", SYSTEM), ChatMessage("user", repair)],
                        **chat_kwargs,
                    )
                )
                xml = _sanitize_llm_xml(xml)
                if template == "syllabus_optimize_schema.j2":
                    xml = _normalize_schema_enums(xml)
            except ProviderError as e:
                repair_aborted = f"自动修复未完成：{e}"
                if not error:
                    error = repair_aborted
                break
            valid, error = validator(xml)
        if repair_aborted and not valid:
            error = f"{error}；{repair_aborted}" if error else repair_aborted

        if not valid:
            xml = _sanitize_llm_xml(xml)
            if template == "syllabus_optimize_schema.j2":
                xml = _normalize_schema_enums(xml)

        repair_attempts = attempts

    _report_progress(progress, is_cancelled, 96, "validating")

    if markdown_mode:
        course_name = extract_course_name_from_markdown(xml) if valid else "解析失败"
        output = xml.strip() + "\n"
    else:
        course_name = extract_course_name(xml) if valid else "解析失败"
        output = prettify(xml) if valid else xml

    return {
        "xml": output,
        "valid": valid,
        "validation_error": error if not valid else "",
        "repair_attempts": repair_attempts,
        "course_name": course_name,
        "original_text": original_text,
        "truncated": truncated,
        "prompt_mode": template,
        "output_format": "markdown" if markdown_mode else "xml",
        "original_char_count": original_char_count,
        "output_char_count": len(output),
        "max_output_chars": max_output_chars if markdown_mode else None,
        "length_within_limit": (
            len(output) <= max_output_chars if markdown_mode else None
        ),
        "generation_strategy": generation_strategy,
        "chapter_count": len(expected_source_ids),
        "staged_fallback_reason": staged_fallback_reason,
    }


def optimize_file(
    file_path: str,
    *,
    prompt_mode: str | None = None,
    progress: ProgressFn | None = None,
    is_cancelled: CancelFn | None = None,
) -> dict[str, Any]:
    _report_progress(
        progress,
        is_cancelled,
        5,
        "parsing",
        {"filename": Path(file_path).name},
    )
    text = load_document(file_path)
    return optimize_text(
        text,
        prompt_mode=prompt_mode,
        progress=progress,
        is_cancelled=is_cancelled,
    )
