#!/usr/bin/env python3
"""Keep one retrieval summary per course and remove page-level summary blocks."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "knowledge" / "corpora" / "course_cases"


def main() -> None:
    changed = 0
    checked = 0
    for path in course_markdown_files():
        checked += 1
        text = path.read_text(encoding="utf-8")
        updated = re.sub(r"\A>[^\n]*\n\n(?=- Source:)", "", text, count=1)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"checked={checked} changed={changed}")


def course_markdown_files():
    for path in COURSES.rglob("*.md"):
        if path.name in {"README.md", "检索摘要.md"}:
            continue
        yield path


if __name__ == "__main__":
    main()
