import threading
import unittest
from unittest.mock import patch

from ai_engine.evaluation.vision import _parallel_describe, describe_courseware_pages


class VisionParallelTests(unittest.TestCase):
    def test_parallel_order_and_callback_thread(self):
        barrier = threading.Barrier(2)
        caller = threading.get_ident()
        callbacks = []

        def describe(item):
            barrier.wait(timeout=5)
            return item * 2

        result = _parallel_describe([1, 2], describe, lambda done, total: callbacks.append((done, total, threading.get_ident())), 2)
        self.assertEqual(result, [2, 4])
        self.assertEqual(callbacks, [(1, 2, caller), (2, 2, caller)])

    def test_empty_and_error(self):
        self.assertEqual(_parallel_describe([], lambda x: x, None, 2), [])
        with self.assertRaises(ValueError):
            _parallel_describe([1], lambda x: int('bad'), None, 2)

    def test_courseware_keeps_original_page_numbers(self):
        fake_vlm = unittest.mock.Mock()
        fake_vlm.describe.return_value = '{}'
        with patch('ai_engine.evaluation.vision._vision_workers', return_value=2), patch('ai_engine.evaluation.vision.get_vlm', return_value=fake_vlm):
            notes = describe_courseware_pages([{'path': 'a'}, {'path': 'b'}])
        self.assertEqual([n['page'] for n in notes], [1, 2])
        self.assertEqual([n['page_count'] for n in notes], [2, 2])
        self.assertEqual([n['index'] for n in notes], [0, 1])
