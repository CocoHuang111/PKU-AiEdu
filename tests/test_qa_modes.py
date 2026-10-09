from __future__ import annotations

import unittest
from unittest.mock import patch

from pydantic import ValidationError

from ai_engine.providers import ProviderError
from ai_engine.qa.case_loader import hydrate_matched_cases
from ai_engine.qa.modes import MODES, get_mode, public_modes
from ai_engine.qa.pipeline import _build_messages, plan_retrieval
from ai_engine.rag.loaders import source_url_for_document
from backend.app.schemas import QAForm


class _UnavailableLLM:
    def chat(self, _messages):
        raise ProviderError("offline")


class QAModeTests(unittest.TestCase):
    def test_four_public_modes_have_distinct_workflows(self):
        self.assertEqual(len(MODES), 4)
        self.assertEqual(
            {m.name for m in MODES},
            {"ask", "syllabus_design", "teaching_design", "learning_diagnosis"},
        )
        self.assertEqual(len(public_modes()), 4)
        self.assertEqual(get_mode("unknown").name, "ask")
        self.assertEqual(get_mode("syllabus_design").retrieval_strategy, "course_match")

    def test_api_schema_validates_mode(self):
        self.assertEqual(QAForm(question="test").mode, "ask")
        self.assertEqual(
            QAForm(question="test", mode="teaching_design").mode,
            "teaching_design",
        )
        with self.assertRaises(ValidationError):
            QAForm(question="test", mode="not-a-mode")

    def test_mode_controls_fallback_plan_and_prompt(self):
        with patch("ai_engine.qa.pipeline.get_llm", return_value=_UnavailableLLM()):
            plan = plan_retrieval("设计课程", mode="syllabus_design")
        self.assertEqual(plan["mode"], "syllabus_design")
        self.assertEqual(plan["retrieval_strategy"], "course_match")
        self.assertIn("course_cases", plan["corpora"])
        messages = _build_messages("设计课程", [], [], "syllabus_design")
        self.assertIn("大纲设计", messages[0].content)
        self.assertIn("目标-活动-评价", messages[1].content)

    def test_teaching_design_is_adaptive_and_has_no_default_duration(self):
        mode = get_mode("teaching_design")
        self.assertIn("不要把所有回答机械展开成完整教案", mode.answer_instruction)
        self.assertIn("不要默认90分钟", mode.answer_instruction)
        self.assertIn("阶段比例", mode.answer_instruction)
        self.assertIn("不为凑格式罗列弱相关案例", mode.answer_instruction)
        self.assertIn("不超过回答篇幅的四分之一", mode.answer_instruction)
        self.assertIn("主体篇幅必须用于", mode.answer_instruction)
        self.assertIn("北大教学沙龙", mode.answer_instruction)
        expected_order = [
            "1.学习目标",
            "2.学情假设与难点",
            "3.案例匹配",
            "4.解决方案",
            "5.形成性评价设计",
            "6.实施风险",
        ]
        positions = [mode.answer_instruction.index(item) for item in expected_order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("判断学生是否达到学习目标", mode.answer_instruction)
        self.assertIn("最可能影响落地的条件", mode.answer_instruction)
        self.assertFalse(any("90分钟" in question for question in mode.starter_questions))
        messages = _build_messages("怎样讲清抽象概念？", [], [], "teaching_design")
        self.assertIn("不要把所有回答机械展开成完整教案", messages[1].content)

    def test_whole_teaching_case_is_labeled_separately_from_course(self):
        context = {
            "text": "案例全文",
            "corpus": "teaching_cases",
            "corpus_label": "国内外高校教学案例",
            "source": "某教学案例",
            "source_url": "https://example.edu/case",
            "score": 0.88,
            "whole_case": True,
            "documents": ["case.md"],
        }
        messages = _build_messages("怎样组织课堂活动？", [context], [], "teaching_design")
        self.assertIn("完整教学案例", messages[1].content)
        self.assertNotIn("完整课程案例", messages[1].content)

    def test_chunk_context_without_whole_case_still_renders(self):
        contexts = [
            {
                "text": "切片正文",
                "corpus": "edu_theory",
                "corpus_label": "教育理论",
                "source": "某文献",
                "score": 0.82,
            }
        ]
        messages = _build_messages("怎么设计提问", contexts, [], "ask")
        self.assertIn("某文献", messages[1].content)
        self.assertIn("相似度", messages[1].content)
        self.assertNotIn("完整课程案例", messages[1].content)

    def test_mit_match_hydrates_whole_documents_and_source_url(self):
        source = (
            "MIT-OCW/courses/16-a47-the-engineer-of-2020-fall-2009/"
            "检索摘要.md"
        )
        hits = [
            {
                "corpus": "course_cases",
                "score": 0.91,
                "text": "match",
                "metadata": {"source": source},
            }
        ]
        contexts, matches, consumed = hydrate_matched_cases(
            hits, "course_match", max_cases=1
        )
        self.assertEqual(len(contexts), 1)
        self.assertTrue(contexts[0]["whole_case"])
        self.assertIn("syllabus.md", contexts[0]["documents"])
        self.assertIn("Learning Objectives", contexts[0]["text"])
        self.assertTrue(contexts[0]["source_url"].startswith("https://ocw.mit.edu/"))
        self.assertEqual(len(matches), 1)
        self.assertIn("MIT-OCW/courses/16-a47", next(iter(consumed)))

    def test_bare_source_marker_is_recognized(self):
        url = source_url_for_document(
            "fake.md",
            ".",
            "- Source: https://ocw.mit.edu/courses/example/pages/syllabus/\n",
        )
        self.assertEqual(
            url, "https://ocw.mit.edu/courses/example/pages/syllabus/"
        )


if __name__ == "__main__":
    unittest.main()
