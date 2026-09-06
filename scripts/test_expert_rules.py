"""专家规则学习与 Judge 可观察性约定测试（不调用大模型）。"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from ai_engine.evaluation.judge import _apply_effect_process_fallback, judge_dimension
from ai_engine.evaluation.pipeline import build_evidence
from ai_engine.pedagogy.loader import get_rubric, render_prompt
from scripts.build_eval_dataset import _dim_map
from scripts.eval_dataset.expert_rules import (
    build_rule_candidates,
    freeze_approved_rules,
    ingest_expert_reviews,
)

ROOT = Path(__file__).resolve().parent.parent


class ExpertReviewIngestTest(unittest.TestCase):
    def test_real_workbooks_keep_score_comment_pairing(self):
        source = ROOT / "test" / "expert_judge"
        if not source.exists():
            self.skipTest("本机没有专家评分表")
        with tempfile.TemporaryDirectory() as tmp:
            rows = ingest_expert_reviews(source, Path(tmp))

        counts = {}
        for row in rows:
            key = (row["source_batch"], row["review_scope"])
            counts[key] = counts.get(key, 0) + 1
        self.assertEqual(counts[("2018", "aggregate")], 25)
        self.assertEqual(counts[("2019", "aggregate")], 42)
        self.assertEqual(counts[("2022", "individual")], 204)
        self.assertEqual(counts[("2024", "individual")], 370)
        self.assertEqual(counts[("2024", "aggregate")], 74)

        summary = next(
            r
            for r in rows
            if r["source_batch"] == "2024" and r["review_scope"] == "aggregate"
        )
        self.assertEqual(summary["expert_id"], "")
        self.assertEqual(summary["score_raw"], summary["teacher_avg"])

        paired_005 = [
            r
            for r in rows
            if r["source_batch"] == "2024"
            and r["review_scope"] == "individual"
            and r["expert_id"] == "005"
            and r["has_comment"]
        ]
        self.assertEqual(len(paired_005), 22)
        self.assertTrue(all("汇总评语" not in r["review_text"] for r in paired_005))
        self.assertTrue(all("邮箱" not in r and "职工号" not in r for r in rows))

    def test_candidate_severity_uses_unique_teachers(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            records = []
            for i, score in enumerate((3.7, 3.8, 3.6), start=1):
                records.append(
                    {
                        "record": {
                            "record_id": f"r{i}",
                            "teacher_id": f"t{i}",
                            "score_raw": str(score),
                            "evaluator_delta": "0.2",
                        },
                        "mentions": [
                            {
                                "polarity": "issue",
                                "issue_key": "interaction_weak",
                                "dimension_key": "teaching_effect",
                                "executable": True,
                                "evidence_phrase": "建议增加互动",
                                "observable_condition": "存在真实课堂",
                            }
                        ],
                    }
                )
            # 同一教师重复记录不能把独立教师数从 3 放大。
            records.extend([records[0], records[0]])
            with (work / "expert_mentions.jsonl").open("w", encoding="utf-8") as f:
                for item in records:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            result = build_rule_candidates(work)
        self.assertEqual(result[0]["n_teachers"], 3)
        self.assertEqual(result[0]["suggested_severity"], "improvement_only")


class FrozenRuleTest(unittest.TestCase):
    def test_only_approved_rules_can_freeze(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.yaml"
            output = root / "frozen.yaml"
            candidate.write_text(
                yaml.safe_dump(
                    {
                        "rules": [
                            {
                                "rule_id": "approved_rule",
                                "target_dimension": "teaching_content",
                                "phenomenon": "总结缺失",
                                "scoring_action": "仅在知识闭环未完成时作为主问题",
                                "approved": True,
                            },
                            {
                                "rule_id": "draft_rule",
                                "target_dimension": "teaching_effect",
                                "phenomenon": "互动较少",
                                "scoring_action": "只作建议",
                                "approved": False,
                            },
                        ]
                    },
                    allow_unicode=True,
                ),
                encoding="utf-8",
            )
            count = freeze_approved_rules(candidate, output)
            frozen = yaml.safe_load(output.read_text(encoding="utf-8"))
        self.assertEqual(count, 1)
        self.assertEqual([r["rule_id"] for r in frozen["rules"]], ["approved_rule"])

    def test_freeze_removes_legacy_70_point_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.yaml"
            output = root / "frozen.yaml"
            candidate.write_text(
                yaml.safe_dump(
                    {
                        "rules": [
                            {
                                "rule_id": "legacy_floor_rule",
                                "target_dimension": "teaching_content",
                                "phenomenon": "内容不足",
                                "scoring_action": (
                                    "若为 minor_when，仅轻微扣分，不可作为导致该维度低于70分的唯一理由；"
                                    "若为 major_when，显著扣分，允许导致该维度低于70分。"
                                ),
                                "approved": True,
                            }
                        ]
                    },
                    allow_unicode=True,
                ),
                encoding="utf-8",
            )
            freeze_approved_rules(candidate, output)
            action = yaml.safe_load(output.read_text(encoding="utf-8"))["rules"][0][
                "scoring_action"
            ]
        self.assertNotIn("不可作为导致该维度低于70分", action)
        self.assertIn("不存在70分或其他固定下限", action)
        self.assertIn("多个相互独立且证据充分的问题必须累计", action)
        self.assertIn("允许导致该维度低于60分", action)

    def test_freeze_rejects_non_five_dimension(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            candidate = root / "candidate.yaml"
            candidate.write_text(
                yaml.safe_dump(
                    {
                        "rules": [
                            {
                                "rule_id": "bad_recording_rule",
                                "target_dimension": "recording_only",
                                "primary_dimension": "recording_only",
                                "phenomenon": "画面模糊",
                                "scoring_action": "降低拍摄质量分",
                                "approved": True,
                            }
                        ]
                    },
                    allow_unicode=True,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "不是合法五维 key"):
                freeze_approved_rules(candidate, root / "frozen.yaml")


class _StaticLLM:
    def __init__(self, payload: dict):
        self.payload = payload

    def chat(self, _messages):
        return json.dumps(self.payload, ensure_ascii=False)


class JudgeObservabilityTest(unittest.TestCase):
    def setUp(self):
        self.dimension = next(
            d for d in get_rubric()["dimensions"] if d["key"] == "teaching_effect"
        )
        self.evidence = build_evidence(
            "本视频只有教师讲解，没有学生声音或学生画面。",
            60,
            {"text": {"total_chars": 24}},
        )

    def test_prompt_contains_permanent_missing_evidence_rule(self):
        prompt = render_prompt(
            "eval_judge.j2",
            dimension=self.dimension,
            evidence=self.evidence,
            expert_lessons="",
            expert_rules=[],
        )
        self.assertIn("不可观察不等于表现差", prompt)
        self.assertIn('score: null', prompt)
        self.assertIn("PPT 加画外音", prompt)
        self.assertIn("直接结果与预期效果必须分开", prompt)
        self.assertIn('score_basis: "inferred"', prompt)
        self.assertIn("禁止用 60 或其他固定分填补缺失", prompt)

    def test_all_direct_effect_items_missing_keeps_inferred_dimension_score(self):
        payload = {
            "indicators": [
                {
                    "key": ind["key"],
                    "observability": "not_observable",
                    "assessed": False,
                    "score": None,
                    "confidence": "none",
                    "evidence": "没有学生或真实课堂观察通道",
                    "suggestion": "",
                }
                for ind in self.dimension["indicators"]
            ],
            "dimension_score": 76,
            "score_basis": "inferred",
            "dimension_confidence": "high",
            "dimension_rationale": "未观察到学生反馈；根据讲解逻辑与总结巩固，预计能够支持基本理解。",
            "primary_issue": "",
            "severity": "none",
            "applied_rule_ids": [],
        }
        with patch("ai_engine.evaluation.judge.get_llm", return_value=_StaticLLM(payload)):
            result = judge_dimension(self.dimension, self.evidence, {"text", "audio"})
        self.assertTrue(result["assessed"])
        self.assertEqual(result["score"], 76.0)
        self.assertEqual(result["score_source"], "llm_inferred")
        self.assertEqual(result["score_basis"], "inferred")
        self.assertEqual(result["dimension_confidence"], "medium")
        self.assertFalse(result["direct_effect_assessed"])
        self.assertEqual(result["direct_effect_indicator_count"], 0)
        self.assertTrue(all(i["score"] is None for i in result["indicators"]))

    def test_missing_items_do_not_lower_observed_indicator(self):
        payload = {
            "indicators": [
                {
                    "key": ind["key"],
                    "observability": "observed" if ind["key"] == "atmosphere" else "not_observable",
                    "assessed": ind["key"] == "atmosphere",
                    "score": 82 if ind["key"] == "atmosphere" else None,
                    "confidence": "medium" if ind["key"] == "atmosphere" else "none",
                    "evidence": "音频中课堂环境稳定" if ind["key"] == "atmosphere" else "没有学生证据",
                    "suggestion": "保持" if ind["key"] == "atmosphere" else "",
                }
                for ind in self.dimension["indicators"]
            ],
            # 只有一个直接指标时，一级分还要结合教学过程推断，不应被 82±5 锁死。
            "dimension_score": 70,
            "score_basis": "mixed",
            "dimension_confidence": "medium",
            "dimension_rationale": "课堂环境可观察，但学生反馈不足；结合讲解过程推断预期效果。",
            "primary_issue": "",
            "severity": "none",
            "applied_rule_ids": [],
        }
        with patch("ai_engine.evaluation.judge.get_llm", return_value=_StaticLLM(payload)):
            result = judge_dimension(self.dimension, self.evidence, {"text", "audio"})
        self.assertTrue(result["assessed"])
        self.assertEqual(result["score"], 70.0)
        self.assertEqual(result["score_source"], "llm_mixed")
        self.assertEqual(result["score_basis"], "mixed")
        self.assertTrue(result["direct_effect_assessed"])
        self.assertEqual(result["direct_effect_indicator_count"], 1)
        self.assertEqual(result["skipped_count"], 3)

    def test_non_effect_dimension_stays_unassessed_when_every_item_is_missing(self):
        dimension = next(
            d for d in get_rubric()["dimensions"] if d["key"] == "teaching_attitude"
        )
        payload = {
            "indicators": [
                {
                    "key": ind["key"],
                    "observability": "not_observable",
                    "assessed": False,
                    "score": None,
                    "confidence": "none",
                    "evidence": "缺少直接观察对象",
                    "suggestion": "",
                }
                for ind in dimension["indicators"]
            ],
            "dimension_score": 76,
            "score_basis": "inferred",
            "dimension_confidence": "medium",
            "dimension_rationale": "模型尝试推断，但该维度不允许绕过二级证据。",
            "primary_issue": "",
            "severity": "none",
            "applied_rule_ids": [],
        }
        with patch("ai_engine.evaluation.judge.get_llm", return_value=_StaticLLM(payload)):
            result = judge_dimension(dimension, self.evidence, {"text", "audio", "vision"})
        self.assertFalse(result["assessed"])
        self.assertIsNone(result["score"])
        self.assertIsNone(result["score_basis"])

    def test_invalid_zero_effect_uses_other_process_dimensions(self):
        dimensions = [
            {
                "key": key,
                "score": score,
                "weight": 1.0,
                "assessed": True,
                "indicators": [],
            }
            for key, score in (
                ("teaching_attitude", 80),
                ("teaching_content", 90),
                ("teaching_method", 70),
                ("teaching_quality", 80),
            )
        ]
        dimensions.append(
            {
                "key": "teaching_effect",
                "score": 0.0,
                "weight": 1.0,
                "assessed": True,
                "direct_effect_assessed": False,
                "direct_effect_indicator_count": 0,
                "indicators": [],
            }
        )
        _apply_effect_process_fallback(dimensions)
        effect = dimensions[-1]
        self.assertEqual(effect["score"], 80.0)
        self.assertEqual(effect["score_source"], "process_dimensions_fallback")
        self.assertEqual(effect["score_basis"], "inferred")
        self.assertEqual(effect["dimension_confidence"], "low")

    def test_effect_inference_metadata_is_available_for_detail_table(self):
        flat = _dim_map(
            {
                "dimensions": [
                    {
                        "key": "teaching_effect",
                        "score": 76,
                        "assessed": True,
                        "score_source": "llm_inferred",
                        "score_basis": "inferred",
                        "dimension_confidence": "medium",
                        "direct_effect_assessed": False,
                        "direct_effect_indicator_count": 0,
                        "dimension_rationale": "仅根据教学过程推断预期效果。",
                        "indicators": [],
                    }
                ]
            }
        )
        self.assertEqual(flat["llm_dim_teaching_effect"], 76)
        self.assertEqual(flat["llm_dim_teaching_effect_score_basis"], "inferred")
        self.assertEqual(flat["llm_dim_teaching_effect_confidence"], "medium")
        self.assertEqual(flat["llm_dim_teaching_effect_direct_result_assessed"], 0)
        self.assertEqual(flat["llm_dim_teaching_effect_direct_result_indicator_count"], 0)


class V9PromptContractTest(unittest.TestCase):
    def test_judge_prompt_binds_severity_and_removes_score_floor(self):
        dimension = next(
            d for d in get_rubric()["dimensions"] if d["key"] == "teaching_content"
        )
        prompt = render_prompt(
            "eval_judge.j2",
            dimension=dimension,
            evidence=build_evidence("本节课讲解一个核心概念。", 60, {}),
            expert_lessons="",
            expert_rules=[],
        )
        self.assertIn("不存在 70 分或其他固定分数下限", prompt)
        self.assertIn("`ordinary_issue`：60–79", prompt)
        self.assertIn("`major_issue`：0–59", prompt)
        self.assertIn("90 分以上必须有**示范性证据**", prompt)
        self.assertIn("证据充分的问题必须累计", prompt)

    def test_report_prompt_reads_primary_issue_and_requires_five_dimensions(self):
        prompt = render_prompt(
            "eval_report.j2",
            overall={
                "score": 78,
                "grade": "C",
                "grade_label": "合格",
                "duration_minutes": 20,
                "modalities": ["text"],
                "skipped_indicators": 0,
            },
            dimensions=[
                {
                    "key": "teaching_content",
                    "label": "教学内容",
                    "score": 72,
                    "grade": "C",
                    "assessed": True,
                    "dimension_rationale": "内容基本完整，但重点展开不足。",
                    "primary_issue": "核心难点展开不足",
                    "severity": "ordinary_issue",
                    "indicators": [],
                }
            ],
        )
        self.assertIn("核心难点展开不足", prompt)
        self.assertIn("## 〇、诊断摘要", prompt)
        self.assertIn("每类恰好 2 条", prompt)
        self.assertIn("## 三、五维诊断", prompt)
        self.assertIn("当前证据未发现显著问题", prompt)
        self.assertIn("不再只按全局最低分排序", prompt)

    def test_parse_report_digest_reads_two_points(self):
        from ai_engine.evaluation.pipeline import parse_report_digest

        report = """## 〇、诊断摘要

### 突出优点
- 课件图表清楚，案例能把概念说透
- 23 分钟内讲完导入到小结

### 主要问题
- 提问后几乎不留思考时间
- 视线长时间停在屏幕上

### 改进建议
- 提问后默数三秒再叫答
- 每讲完一块就抬头看学生

## 一、总体评价
展开论述。
"""
        digest = parse_report_digest(report)
        self.assertEqual(digest["strengths"][0], "课件图表清楚，案例能把概念说透")
        self.assertEqual(len(digest["issues"]), 2)
        self.assertEqual(digest["suggestions"][1], "每讲完一块就抬头看学生")


if __name__ == "__main__":
    unittest.main()
