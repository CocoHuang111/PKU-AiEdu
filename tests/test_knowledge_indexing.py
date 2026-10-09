from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ai_engine.config import settings
from ai_engine.qa.case_loader import hydrate_matched_cases
from knowledge.index_records import iter_index_records


class KnowledgeIndexingTests(unittest.TestCase):
    def test_course_uses_one_summary_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            course = root / "MIT-OCW" / "courses" / "demo"
            course.mkdir(parents=True)
            (course / "course.yaml").write_text(
                "course_id: demo\ncourse_title: Demo Course\n"
                "institution: MIT\ncourse_url: https://example.edu/demo\n"
                "language: en\n",
                encoding="utf-8",
            )
            (course / "检索摘要.md").write_text("中文课程摘要", encoding="utf-8")
            (course / "syllabus.md").write_text("Syllabus body", encoding="utf-8")

            records = list(iter_index_records("course_cases", root))

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].metadata["record_type"], "course")
            self.assertEqual(records[0].metadata["item_key"], "MIT-OCW/courses/demo")
            self.assertIn("中文课程摘要", records[0].text)
            self.assertNotIn("Syllabus body", records[0].text)

    def test_teaching_case_uses_one_index_record_per_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case = root / "Cornell" / "cases" / "demo"
            case.mkdir(parents=True)
            (case / "case.yaml").write_text(
                "case_id: demo\ntitle: Demo Case\ninstitution: Cornell\n"
                "source_url: https://example.edu/case\nlanguage: en\n",
                encoding="utf-8",
            )
            (case / "case.md").write_text(
                "> 检索摘要：掌握式学习。\n\n---\n\nFull English case.",
                encoding="utf-8",
            )
            pku = root / "PKU" / "single.md"
            pku.parent.mkdir()
            pku.write_text("# 单文件案例\n\n教学改革做法。", encoding="utf-8")

            records = list(iter_index_records("teaching_cases", root))

            self.assertEqual(len(records), 2)
            self.assertTrue(all(r.metadata["record_type"] == "teaching_case" for r in records))
            self.assertFalse(any("Full English case" in r.text for r in records))

    def test_generic_markdown_is_split_by_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "theory.md").write_text(
                "# 总题\n\n导言。\n\n## 方法一\n\n内容一。\n\n## 方法二\n\n内容二。",
                encoding="utf-8",
            )
            records = list(iter_index_records("edu_theory", root))
            sections = {r.metadata["section"] for r in records}
            self.assertIn("总题", sections)
            self.assertIn("总题 > 方法一", sections)
            self.assertIn("总题 > 方法二", sections)

    def test_yale_course_and_teaching_case_are_hydrated_from_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            course = base / "course_cases" / "Yale-OYC" / "courses" / "demo"
            course.mkdir(parents=True)
            (course / "course.yaml").write_text(
                "course_title: Yale Demo\ncourse_codes: [DEMO 1]\n"
                "course_url: https://example.edu/yale\n",
                encoding="utf-8",
            )
            (course / "检索摘要.md").write_text("课程摘要", encoding="utf-8")
            (course / "course-description.md").write_text("Course description", encoding="utf-8")
            (course / "exam-1.md").write_text("Exam material", encoding="utf-8")
            (course / "lecture-1.md").write_text("Long transcript", encoding="utf-8")

            case = base / "teaching_cases" / "Cornell" / "cases" / "demo"
            case.mkdir(parents=True)
            (case / "case.md").write_text("Complete teaching case", encoding="utf-8")

            def corpus_dir(name: str) -> Path:
                return base / name

            with patch.object(settings, "corpus_dir", side_effect=corpus_dir):
                courses, _, _ = hydrate_matched_cases(
                    [{
                        "corpus": "course_cases",
                        "score": 0.9,
                        "metadata": {
                            "record_type": "course",
                            "item_key": "Yale-OYC/courses/demo",
                        },
                    }],
                    "course_match",
                )
                cases, _, _ = hydrate_matched_cases(
                    [{
                        "corpus": "teaching_cases",
                        "score": 0.9,
                        "metadata": {
                            "record_type": "teaching_case",
                            "item_key": "Cornell/cases/demo",
                            "content_file": "case.md",
                            "title": "Demo Case",
                        },
                    }],
                    "case_match",
                )

            self.assertIn("Course description", courses[0]["text"])
            self.assertIn("Exam material", courses[0]["text"])
            self.assertNotIn("Long transcript", courses[0]["text"])
            self.assertEqual(cases[0]["text"].count("Complete teaching case"), 1)
            self.assertTrue(cases[0]["whole_case"])


if __name__ == "__main__":
    unittest.main()
