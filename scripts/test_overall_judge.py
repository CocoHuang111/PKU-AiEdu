"""LLM 综合总分 Prompt 的标签隔离与解析测试（不调用模型）。"""

from __future__ import annotations

import unittest

from scripts.judge_overall import _normalize_result, build_blind_prompt


class OverallJudgeTest(unittest.TestCase):
    def test_prompt_excludes_expert_labels_comments_and_gb_predictions(self):
        evidence = {
            "raw_features": {"text": {"speech_rate": 180}},
            "expert_score_5": 0.25,
            "comment": "绝不能泄漏的专家评语",
            "pred_obj_reg": 4.75,
        }
        scores = {
            "dimensions": [
                {
                    "key": "teaching_content",
                    "label": "教学内容",
                    "score": 82,
                    "assessed": True,
                    "score_basis": "observed",
                    "dimension_confidence": "medium",
                    "dimension_rationale": "内容完整且逻辑清楚。",
                    "primary_issue": "",
                    "severity": "none",
                }
            ],
            "report": "也不应把完整报告带入综合分",
        }
        prompt = build_blind_prompt(evidence, scores)
        self.assertIn("教学内容（82/100）", prompt)
        self.assertIn("语速", prompt)
        self.assertNotIn("0.25", prompt)
        self.assertNotIn("4.75", prompt)
        self.assertNotIn("绝不能泄漏的专家评语", prompt)
        self.assertNotIn("完整报告带入综合分", prompt)

    def test_normalize_result_accepts_score5_and_clamps_list_lengths(self):
        result = _normalize_result(
            {
                "overall_score_5": 3.4,
                "confidence": "high",
                "main_strengths": ["a", "b", "c", "d"],
                "main_issues": [],
                "decisive_evidence": ["1", "2", "3", "4", "5", "6"],
                "rationale": "综合判断。",
            }
        )
        self.assertEqual(result["overall_score_5"], 3.4)
        self.assertEqual(result["overall_score_100"], 68.0)
        self.assertEqual(len(result["main_strengths"]), 3)
        self.assertEqual(len(result["decisive_evidence"]), 5)

    def test_normalize_result_rejects_out_of_range_score(self):
        with self.assertRaisesRegex(ValueError, "越界"):
            _normalize_result({"overall_score_5": 5.1})


if __name__ == "__main__":
    unittest.main()
