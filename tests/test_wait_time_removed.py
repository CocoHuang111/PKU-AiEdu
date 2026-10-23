"""Regression checks for restored ASR question wait-time metrics."""

import unittest

from ai_engine.evaluation.audio_charts import CHARTS
from ai_engine.evaluation.timeline_features import extract_timeline_features
from ai_engine.pedagogy.loader import get_rubric
from ai_engine.providers import ASRSegment


class WaitTimeRestorationTests(unittest.TestCase):
    def test_question_gap_produces_wait_metrics(self):
        segments = [
            ASRSegment(0, 5, "为什么？", avg_logprob=-0.2),
            ASRSegment(15, 20, "现在来看答案。", avg_logprob=-0.8),
        ]
        features = extract_timeline_features(segments)
        self.assertEqual(features['wait_time_mean'], 10)
        self.assertEqual(features['wait_time_median'], 10)
        self.assertEqual(features['wait_time_sample_count'], 1)
        self.assertEqual(features['wait_time_effective_ratio'], 100)
        self.assertEqual(features['wait_samples'], [10])
        self.assertIn('asr_confidence', features)
        self.assertEqual(extract_timeline_features([]), {})


    def test_wait_chart_and_rubric_are_restored(self):
        self.assertIn("wait_samples", CHARTS)
        self.assertIn("wait_time_", str(get_rubric()))
        self.assertIn("提问后保留有效思考等待时间", str(get_rubric()))

    def test_cap_negative_and_nonquestion_gaps(self):
        segments = [ASRSegment(0, 5, '为什么？'), ASRSegment(100, 105, '答案。')]
        self.assertEqual(extract_timeline_features(segments)['wait_samples'], [30])
        segments[1].start = 4
        self.assertEqual(extract_timeline_features(segments)['wait_time_sample_count'], 0)
        segments[0].text = '现在开始讲解。'
        self.assertEqual(extract_timeline_features(segments)['wait_time_sample_count'], 0)
