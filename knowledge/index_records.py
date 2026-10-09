"""按语料类型生成可检索记录。

课程和教学案例只把一条中文摘要写进向量库，命中后由 QA 加载器回读原文；
理论、学科知识、沙龙和 AIMES 的非案例材料按 Markdown 标题分段。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

import yaml

from ai_engine.rag.loaders import iter_documents, load_document, source_url_for_document
from ai_engine.rag.splitter import split_text


@dataclass(frozen=True)
class IndexRecord:
    text: str
    source: str
    source_url: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return value if isinstance(value, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


def _flat_text(value: Any) -> str:
    if isinstance(value, list):
        return "、".join(str(item) for item in value if item not in (None, ""))
    return str(value or "").strip()


def _first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = _HEADING_RE.match(line.strip())
        if match:
            return match.group(2).strip(" *`#")
    return fallback


def _summary_or_preamble(path: Path, limit: int = 2200) -> str:
    text = load_document(path)
    parts = re.split(r"\n\s*---\s*\n", text, maxsplit=1)
    if len(parts) == 2:
        preamble = parts[0].strip()
        if preamble:
            return preamble[:limit]
    return text[:limit]


def _semantic_sections(text: str, target_size: int = 1400) -> list[tuple[str, str]]:
    """按 Markdown 标题建立语义段；超长标题段才继续按段落切分。"""
    sections: list[tuple[str, str]] = []
    heading_stack: list[str] = []
    current_heading = "全文"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines
        body = "\n".join(current_lines).strip()
        current_lines = []
        if not body:
            return
        heading = " > ".join(heading_stack) or current_heading
        prefix = f"章节：{heading}\n\n"
        for chunk in split_text(body, chunk_size=target_size, overlap=120):
            sections.append((heading, prefix + chunk))

    for line in text.splitlines():
        match = _HEADING_RE.match(line.strip())
        if not match:
            current_lines.append(line)
            continue
        flush()
        level = len(match.group(1))
        title = match.group(2).strip()
        heading_stack[level - 1 :] = [title]
        current_heading = title
        current_lines.append(line)
    flush()
    return sections or [("全文", text)]


def _course_records(root: Path) -> Iterator[IndexRecord]:
    for meta_path in sorted(root.rglob("course.yaml")):
        course_dir = meta_path.parent
        summary_path = course_dir / "检索摘要.md"
        if not summary_path.exists():
            print(f"  [跳过] 缺少课程级检索摘要: {course_dir.relative_to(root)}")
            continue
        meta = _yaml(meta_path)
        summary = load_document(summary_path)
        title = _flat_text(meta.get("course_title")) or course_dir.name
        codes = _flat_text(meta.get("course_codes"))
        institution = _flat_text(meta.get("institution"))
        subjects = "、".join(
            value
            for value in (
                _flat_text(meta.get("subject_primary")),
                _flat_text(meta.get("subject_secondary")),
                _flat_text(meta.get("department_path")),
            )
            if value
        )
        levels = _flat_text(meta.get("academic_levels"))
        prefix = [f"课程名称：{title}"]
        if codes:
            prefix.append(f"课程代码：{codes}")
        if institution:
            prefix.append(f"学校：{institution}")
        if subjects:
            prefix.append(f"学科主题：{subjects}")
        if levels:
            prefix.append(f"课程层次：{levels}")
        rel = summary_path.relative_to(root).as_posix()
        item_key = course_dir.relative_to(root).as_posix()
        yield IndexRecord(
            text="\n".join(prefix) + "\n\n" + summary,
            source=rel,
            source_url=_flat_text(meta.get("course_url"))
            or source_url_for_document(summary_path, root, summary),
            metadata={
                "record_type": "course",
                "item_key": item_key,
                "title": title,
                "institution": institution,
                "language": _flat_text(meta.get("language")),
                "subject_tags": subjects,
                "academic_level": levels,
                "is_summary": True,
            },
        )


def _case_record(root: Path, content_path: Path, meta_path: Path | None = None) -> IndexRecord:
    meta = _yaml(meta_path) if meta_path else {}
    summary_path = content_path.parent / "检索摘要.md"
    index_path = summary_path if summary_path.exists() else content_path
    summary = (
        load_document(summary_path)
        if summary_path.exists()
        else _summary_or_preamble(content_path)
    )
    title = _flat_text(meta.get("title")) or _first_heading(
        load_document(content_path), content_path.stem
    )
    institution = _flat_text(meta.get("institution"))
    prefix = [f"教学案例：{title}"]
    if institution:
        prefix.append(f"学校：{institution}")
    item_path = content_path.parent if meta_path else content_path
    return IndexRecord(
        text="\n".join(prefix) + "\n\n" + summary,
        source=index_path.relative_to(root).as_posix(),
        source_url=_flat_text(meta.get("source_url"))
        or source_url_for_document(content_path, root, load_document(content_path)),
        metadata={
            "record_type": "teaching_case",
            "item_key": item_path.relative_to(root).as_posix(),
            "content_file": content_path.name,
            "title": title,
            "institution": institution,
            "language": _flat_text(meta.get("language")),
            "is_summary": True,
        },
    )


def _teaching_case_records(root: Path) -> Iterator[IndexRecord]:
    consumed: set[Path] = set()
    for meta_path in sorted(root.rglob("case.yaml")):
        case_dir = meta_path.parent
        content_path = case_dir / "case.md"
        if not content_path.exists():
            print(f"  [跳过] 缺少案例原文: {case_dir.relative_to(root)}")
            continue
        consumed.add(content_path.resolve())
        yield _case_record(root, content_path, meta_path)

    # 北大等单文件案例没有 case.yaml，每个 Markdown 文件就是一个完整案例。
    for path, _text in iter_documents(root):
        if path.resolve() in consumed or path.name == "检索摘要.md":
            continue
        if path.suffix.lower() != ".md":
            continue
        yield _case_record(root, path)


def _generic_records(corpus: str, root: Path) -> Iterator[IndexRecord]:
    for path, text in iter_documents(root):
        rel = path.relative_to(root).as_posix()
        is_aimes_case = corpus == "AIMES" and "AIMES Library" in path.parts
        if is_aimes_case:
            title = _first_heading(text, path.stem)
            yield IndexRecord(
                text=_summary_or_preamble(path),
                source=rel,
                source_url=source_url_for_document(path, root, text),
                metadata={
                    "record_type": "teaching_case",
                    "item_key": rel,
                    "content_file": path.name,
                    "title": title,
                    "institution": "Stanford University",
                    "language": "en",
                    "is_summary": True,
                },
            )
            continue

        sections = (
            _semantic_sections(text)
            if path.suffix.lower() == ".md"
            else [("全文", chunk) for chunk in split_text(text, 1400, 120)]
        )
        title = _first_heading(text, path.stem)
        url = source_url_for_document(path, root, text)
        for index, (section, chunk) in enumerate(sections):
            yield IndexRecord(
                text=f"文档：{title}\n\n{chunk}",
                source=rel,
                source_url=url,
                metadata={
                    "record_type": "section",
                    "item_key": rel,
                    "title": title,
                    "section": section,
                    "chunk_index": index,
                    "total_chunks": len(sections),
                    "is_summary": False,
                },
            )


def iter_index_records(corpus: str, root: Path) -> Iterator[IndexRecord]:
    if corpus == "course_cases":
        yield from _course_records(root)
    elif corpus == "teaching_cases":
        yield from _teaching_case_records(root)
    else:
        yield from _generic_records(corpus, root)
