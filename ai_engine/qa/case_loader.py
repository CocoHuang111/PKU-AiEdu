"""二阶段内容加载：摘要索引命中后，按课程/案例边界读取原文。"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from ..config import settings
from ..rag.loaders import load_document, source_url_for_document

SYLLABUS_DOCUMENTS = (
    "检索摘要.md",
    "course-description.md",
    "syllabus.md",
    "calendar.md",
    "assignments.md",
    "instructor-insights.md",
)
TEACHING_DOCUMENTS = (
    "检索摘要.md",
    "course-description.md",
    "syllabus.md",
    "assignments.md",
    "projects.md",
    "instructor-insights.md",
)


def _legacy_course_key(source: str) -> str | None:
    parts = PurePosixPath(source).parts
    if (
        len(parts) >= 4
        and parts[0] in {"MIT-OCW", "Yale-OYC"}
        and parts[1] == "courses"
        and parts[2] not in {"", ".", ".."}
    ):
        return PurePosixPath(*parts[:3]).as_posix()
    return None


def _item_key(hit: dict[str, Any]) -> str | None:
    meta = hit.get("metadata") or {}
    key = str(meta.get("item_key") or "").strip()
    if key:
        return PurePosixPath(key).as_posix()
    if hit.get("corpus") == "course_cases":
        return _legacy_course_key(str(meta.get("source") or ""))
    return None


def _safe_item_path(corpus: str, key: str) -> Path | None:
    root = settings.corpus_dir(corpus).resolve()
    path = (root / Path(*PurePosixPath(key).parts)).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def _course_meta(course_dir: Path) -> dict[str, Any]:
    path = course_dir / "course.yaml"
    if not path.exists():
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return value if isinstance(value, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


def _whole_documents(
    course_dir: Path,
    filenames: tuple[str, ...],
    max_chars: int,
) -> tuple[str, list[str]]:
    """按文档边界装载，不在一个文档内部截断。"""
    parts: list[str] = []
    loaded: list[str] = []
    used = 0
    for filename in filenames:
        path = course_dir / filename
        if not path.exists():
            continue
        try:
            text = load_document(path)
        except Exception:
            continue
        block = f"## {filename}\n\n{text}"
        if parts and used + len(block) > max_chars:
            continue
        # 首个可用文档至少保留一份；仍不截断文档。
        parts.append(block)
        loaded.append(filename)
        used += len(block)
    return "\n\n".join(parts), loaded


def _course_documents(course_dir: Path, strategy: str, max_chars: int) -> tuple[str, list[str]]:
    preferred = SYLLABUS_DOCUMENTS if strategy == "course_match" else TEACHING_DOCUMENTS
    names = list(preferred)
    # Yale OYC 通常没有独立 syllabus，但有课程说明和考试页；不把全部讲课转写
    # 无条件塞进上下文，避免一门课占用数十万字。
    for pattern in ("exam-*.md", "exams*.md"):
        names.extend(path.name for path in sorted(course_dir.glob(pattern)))
    return _whole_documents(course_dir, tuple(dict.fromkeys(names)), max_chars)


def _teaching_case_document(
    corpus: str, item_path: Path, content_file: str = ""
) -> tuple[str, list[str]]:
    if item_path.is_file():
        candidates = [item_path]
    else:
        preferred = item_path / (content_file or "case.md")
        candidates = [preferred] if preferred.exists() else []
        if not candidates:
            candidates = [
                path
                for path in sorted(item_path.glob("*.md"))
                if path.name.lower() != "readme.md" and path.name != "检索摘要.md"
            ]
    if not candidates:
        return "", []

    parts: list[str] = []
    loaded: list[str] = []
    summary_path = item_path / "检索摘要.md" if item_path.is_dir() else None
    if summary_path and summary_path.exists():
        try:
            parts.append(f"## 检索摘要.md\n\n{load_document(summary_path)}")
            loaded.append("检索摘要.md")
        except Exception:
            pass
    for path in candidates:
        try:
            text = load_document(path)
        except Exception:
            continue
        parts.append(f"## {path.name}\n\n{text}")
        loaded.append(path.name)
    return "\n\n".join(parts), loaded


def hydrate_matched_cases(
    hits: list[dict[str, Any]],
    strategy: str,
    *,
    max_cases: int = 3,
    max_chars_per_case: int = 24000,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[str]]:
    """
    返回（完整案例上下文、前端可展示的匹配摘要、已消费课程 key）。

    course_match 加载 MIT/Yale 的课程级材料；case_match 加载教学案例全文。
    向量库只保存摘要，正文仍以磁盘上的来源文件为准。
    """
    if strategy not in {"course_match", "case_match"}:
        return [], [], set()

    ranked: dict[tuple[str, str], dict[str, Any]] = {}
    for hit in hits:
        corpus = str(hit.get("corpus") or "")
        meta = hit.get("metadata") or {}
        record_type = str(meta.get("record_type") or "")
        if strategy == "course_match" and corpus != "course_cases":
            continue
        if strategy == "case_match" and record_type not in {
            "teaching_case",
            "course",
        }:
            continue
        key = _item_key(hit)
        if not key:
            continue
        rank_key = (corpus, key)
        previous = ranked.get(rank_key)
        if previous is None or hit.get("score", 0) > previous.get("score", 0):
            ranked[rank_key] = hit

    ordered = sorted(ranked.items(), key=lambda item: item[1].get("score", 0), reverse=True)
    contexts: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    consumed: set[str] = set()

    for (corpus, key), hit in ordered[:max_cases]:
        item_path = _safe_item_path(corpus, key)
        if item_path is None or not item_path.exists():
            continue
        meta = hit.get("metadata") or {}
        record_type = str(meta.get("record_type") or "")
        if corpus == "course_cases" or record_type == "course":
            if not item_path.is_dir():
                continue
            text, loaded = _course_documents(item_path, strategy, max_chars_per_case)
            item_meta = _course_meta(item_path)
            title = str(item_meta.get("course_title") or meta.get("title") or item_path.name)
            code = ", ".join(str(v) for v in (item_meta.get("course_codes") or []) if v)
            display = f"{code} {title}".strip()
            url = str(item_meta.get("course_url") or meta.get("source_url") or "")
        else:
            text, loaded = _teaching_case_document(
                corpus, item_path, str(meta.get("content_file") or "")
            )
            title = str(meta.get("title") or item_path.stem)
            display = title
            url = str(meta.get("source_url") or "")
        if not text:
            continue
        if not url:
            first_path = item_path / loaded[-1] if item_path.is_dir() else item_path
            url = source_url_for_document(first_path, settings.corpus_dir(corpus), text)
        score = hit.get("score", 0)
        contexts.append(
            {
                "text": text,
                "corpus": corpus,
                "corpus_label": settings.corpus_meta(corpus).get("label", corpus),
                "source": display,
                "source_url": url,
                "score": score,
                "whole_case": True,
                "documents": loaded,
                "case_key": key,
            }
        )
        matches.append(
            {
                "source": display,
                "source_url": url,
                "score": score,
                "documents": loaded,
            }
        )
        consumed.add(f"{corpus}::{key}")

    return contexts, matches, consumed


def hit_belongs_to_cases(hit: dict[str, Any], case_keys: set[str]) -> bool:
    key = _item_key(hit)
    corpus = str(hit.get("corpus") or "")
    return bool(key and f"{corpus}::{key}" in case_keys)
