"""Regression checks for removal of unreliable question wait-time metrics."""

import unittest

from ai_engine.evaluation.audio_charts import CHARTS
from ai_engine.evaluation.timeline_features import extract_timeline_features
from ai_engine.pedagogy.loader import get_rubric
from ai_engine.providers import ASRSegment


class WaitTimeRemovalTests(unittest.TestCase):
    def test_question_gap_does_not_produce_wait_metrics(self):
        segments = [
            ASRSegment(0, 5, "为什么？", avg_logprob=-0.2),
            ASRSegment(15, 20, "现在来看答案。", avg_logprob=-0.8),
        ]
        self.assertEqual(set(extract_timeline_features(segments)), {
            "asr_confidence", "asr_low_confidence_ratio",
        })
        self.assertEqual(extract_timeline_features([]), {})


    def test_wait_chart_and_rubric_are_removed(self):
        self.assertNotIn("wait_samples", CHARTS)
        self.assertNotIn("wait_time_", str(get_rubric()))
        self.assertNotIn("提问后保留有效思考等待时间", str(get_rubric()))
