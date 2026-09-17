from __future__ import annotations

import asyncio
import contextlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import librosa
import numpy as np
import soundfile as sf

from ai_engine import checkpoints
from ai_engine.evaluation.audio_features import (
    _stream_rms, _stream_pitch, _wave_envelope, extract_audio_features,
    extract_audio_features_isolated,
)
from ai_engine.evaluation.exceptions import EvaluationCancelled
from ai_engine.evaluation.media import extract_audio, cleanup_video_artifacts
from ai_engine.evaluation.transcript_punc import punctuate_asr_result, punctuate_texts
from ai_engine.processes import run_json_worker
from ai_engine.providers.asr import FasterWhisperASR
from ai_engine.providers.base import ASRResult, ASRSegment


class AudioTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "audio.wav"
        t = np.arange(16000 * 4) / 16000
        self.samples = (0.2 * np.sin(2 * np.pi * 220 * t)).astype(np.float32)
        self.samples[8000:56000] = 0
        sf.write(self.path, self.samples, 16000, subtype="FLOAT")

    def test_stream_rms_and_envelope_match_whole_audio(self):
        with sf.SoundFile(self.path) as audio:
            actual = _stream_rms(audio, librosa, block_seconds=0.5)
            envelope = _wave_envelope(audio)
        expected = librosa.feature.rms(y=self.samples, frame_length=2048, hop_length=512)[0]
        np.testing.assert_allclose(actual, expected, atol=1e-7)
        win = self.samples.size // 360
        peaks = np.max(np.abs(self.samples[:360 * win].reshape(360, win)), axis=1)
        self.assertEqual(envelope, [round(float(v / peaks.max()), 4) for v in peaks])

    def test_pitch_bounded_full_coverage_and_cached(self):
        sizes = []
        def pitch(y, **kwargs):
            sizes.append(len(y))
            return np.full(1 + len(y) // 256, 220.), None, None
        with sf.SoundFile(self.path) as audio, patch.object(librosa, "pyin", side_effect=pitch):
            result = _stream_pitch(audio, self.path, librosa, "test", block_seconds=1)
        self.assertEqual(result.size, 1 + self.samples.size // 512)
        self.assertLess(max(sizes), 13000)  # one second plus context, not four seconds
        with sf.SoundFile(self.path) as audio, patch.object(librosa, "pyin", side_effect=AssertionError("cached")):
            restored = _stream_pitch(audio, self.path, librosa, "test", block_seconds=1)
        np.testing.assert_array_equal(result, restored)

    def test_real_pitch_and_isolated_process(self):
        t = np.arange(16000 * 2) / 16000
        sf.write(self.path, 0.2 * np.sin(2 * np.pi * 220 * t), 16000)
        events = []
        result = extract_audio_features_isolated(str(self.path), lambda *args: events.append(args))
        self.assertTrue(result["pitch_available"])
        self.assertAlmostEqual(result["pitch_median"], 220, delta=3)
        self.assertEqual(result["audio_duration_sec"], 2)
        self.assertTrue(any(e[0] == "pitch" for e in events))

    def test_pause_across_block_boundary_and_pitch_failure_not_zero(self):
        with patch.object(librosa, "pyin", side_effect=RuntimeError("pitch unavailable")):
            result = extract_audio_features(str(self.path), block_seconds=0.5)
        self.assertEqual(result["long_pause_count"], 1)
        self.assertFalse(result["pitch_available"])
        self.assertNotIn("pitch_median", result)
        self.assertIn("unavailable", result["pitch_warning"])
        self.assertFalse(self.path.with_suffix(".audio-features.json").exists())

    def test_cancellation_propagates(self):
        def cancel(phase, done, total):
            if phase == "pitch":
                raise EvaluationCancelled()
        with patch.object(librosa, "pyin", return_value=(np.full(300, 220.), None, None)):
            with self.assertRaises(EvaluationCancelled):
                extract_audio_features(str(self.path), progress_callback=cancel, block_seconds=0.5)


class ASRTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "audio.wav"
        sf.write(self.path, np.zeros(16000 * 65, dtype=np.float32), 16000)
        self.provider = FasterWhisperASR({"chunk_seconds": 30})

    def fake_chunk(self, module, request, callback, timeout):
        start = request["read_start"]
        core_start = 0 if start == 0 else start + 2
        offset = core_start - start
        callback({"done_sec": offset + 5})
        return {"language": "zh", "segments": [
            {"start": offset + 1, "end": offset + 3, "text": f"第{core_start}段"},
            # Context owned by the preceding core must not be counted twice.
            *([{ "start": 0, "end": 1, "text": "重复上下文"}] if start else []),
        ]}

    def test_timestamps_ownership_resume_and_final_tail(self):
        events = []
        with patch("ai_engine.providers.asr.run_json_worker", side_effect=self.fake_chunk) as worker:
            result = self.provider.transcribe(str(self.path), progress_callback=lambda *v: events.append(v))
            self.assertEqual(worker.call_count, 3)
            self.assertEqual(worker.call_args_list[-1].args[1]["read_end"], 65)
        self.assertEqual([s.start for s in result.segments], [1, 31, 61])
        self.assertNotIn("重复", result.text)
        self.assertEqual(events[-1], (65, 65))
        with patch("ai_engine.providers.asr.run_json_worker", side_effect=AssertionError("cached")):
            restored = self.provider.transcribe(str(self.path))
        self.assertEqual(result, restored)

    def test_interrupted_run_keeps_completed_chunks(self):
        counter = 0
        def fail_second(*args):
            nonlocal counter
            counter += 1
            if counter == 2:
                raise RuntimeError("child interrupted")
            return self.fake_chunk(*args)
        with patch("ai_engine.providers.asr.run_json_worker", side_effect=fail_second):
            with self.assertRaises(RuntimeError):
                self.provider.transcribe(str(self.path))
        with patch("ai_engine.providers.asr.run_json_worker", side_effect=self.fake_chunk) as worker:
            result = self.provider.transcribe(str(self.path))
        self.assertEqual(worker.call_count, 2)
        self.assertEqual(len(result.segments), 3)

    def test_changed_source_and_model_invalidate_cache(self):
        with patch("ai_engine.providers.asr.run_json_worker", side_effect=self.fake_chunk) as worker:
            self.provider.transcribe(str(self.path))
            FasterWhisperASR({"chunk_seconds": 30, "model": "small"}).transcribe(str(self.path))
            sf.write(self.path, np.zeros(16000 * 35, dtype=np.float32), 16000)
            self.provider.transcribe(str(self.path))
        self.assertEqual(worker.call_count, 8)

    def test_cancel_before_launch(self):
        with patch("ai_engine.providers.asr.run_json_worker") as worker:
            with self.assertRaises(EvaluationCancelled):
                self.provider.transcribe(str(self.path), progress_callback=lambda *v: (_ for _ in ()).throw(EvaluationCancelled()))
        worker.assert_not_called()


class PunctuationTests(unittest.TestCase):
    def test_budget_fallback_and_progress_preserve_wording(self):
        texts = ["因为今天我们学习一个非常重要的知识所以请认真思考"] * 4
        events = []
        with patch("ai_engine.evaluation.transcript_punc.get_llm") as llm:
            result = punctuate_texts(texts, budget_seconds=0, chunk_chars=30, progress_callback=lambda *v: events.append(v))
        llm.assert_not_called()
        self.assertEqual(events[-1][:2], (4, 4))
        self.assertTrue(all(e[2]["budget_exhausted"] for e in events))
        for old, new in zip(texts, result):
            self.assertEqual(old, new.replace("，", "").replace("。", ""))

    def test_cached_batches_and_segment_timestamps(self):
        with tempfile.TemporaryDirectory() as folder:
            source = ASRResult("今天我们学习一个很重要的新知识", [ASRSegment(1, 8, "今天我们学习一个很重要的新知识")], "zh", 10)
            call = lambda prompt: "1. 今天我们学习一个很重要的新知识。"
            result = punctuate_asr_result(source, llm_fn=call, checkpoint_dir=Path(folder))
            restored = punctuate_asr_result(source, llm_fn=lambda p: (_ for _ in ()).throw(AssertionError("cached")), checkpoint_dir=Path(folder))
        self.assertEqual(result, restored)
        self.assertEqual((result.segments[0].start, result.segments[0].end), (1, 8))

    def test_progress_cancel_not_swallowed(self):
        with self.assertRaises(EvaluationCancelled):
            punctuate_texts(["这是一个足够长的没有标点的中文句子"], budget_seconds=0, progress_callback=lambda *v: (_ for _ in ()).throw(EvaluationCancelled()))


class ProcessAndCacheTests(unittest.TestCase):
    def test_complete_evidence_checkpoint_skips_extraction_but_not_scoring(self):
        from ai_engine.evaluation import pipeline
        with tempfile.TemporaryDirectory() as folder:
            video = Path(folder) / "video.mp4"
            video.write_bytes(b"test fixture")
            pack = {"evidence": {}, "available": ["audio"], "raw_features": {"audio": {"pitch_available": True}}}
            with patch.object(pipeline, "collect_video_evidence", return_value=pack) as collect, patch.object(pipeline, "score_from_evidence", return_value={}) as score:
                pipeline.evaluate_session(str(video))
                pipeline.evaluate_session(str(video))
                self.assertEqual(collect.call_count, 1)
                self.assertEqual(score.call_count, 2)
                pipeline.evaluate_session(str(video), reference="new syllabus")
                self.assertEqual(collect.call_count, 2)

    def test_worker_cancel_terminates_child(self):
        original = subprocess.Popen
        children = []
        def launch(*args, **kwargs):
            child = original([sys.executable, "-u", "-c", "import sys,time; sys.stdin.read(); time.sleep(30)"], **kwargs)
            children.append(child)
            return child
        with patch("ai_engine.processes.subprocess.Popen", side_effect=launch):
            with self.assertRaises(EvaluationCancelled):
                run_json_worker("unused", {}, lambda v: (_ for _ in ()).throw(EvaluationCancelled()))
        self.assertIsNotNone(children[0].poll())

    def test_worker_timeout_terminates_child(self):
        original = subprocess.Popen
        children = []
        def launch(*args, **kwargs):
            child = original([sys.executable, "-u", "-c", "import sys,time; sys.stdin.read(); time.sleep(30)"], **kwargs)
            children.append(child)
            return child
        with patch("ai_engine.processes.subprocess.Popen", side_effect=launch):
            with self.assertRaises(TimeoutError):
                run_json_worker("unused", {}, timeout=0.2)
        self.assertIsNotNone(children[0].poll())

    def test_atomic_cache_corrupt_or_wrong_signature_is_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "checkpoint.json"
            checkpoints.write(path, "one", {"segments": []})
            self.assertEqual(checkpoints.read(path, "one"), {"segments": []})
            self.assertIsNone(checkpoints.read(path, "two"))
            path.write_text("{broken", encoding="utf-8")
            self.assertIsNone(checkpoints.read(path, "one"))

    def test_audio_extraction_reuses_unchanged_wav(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.wav"
            sf.write(path, np.zeros(16000), 16000)
            output = Path(folder) / "derived"
            output.mkdir()
            with patch("ai_engine.evaluation.media._run", wraps=__import__("ai_engine.evaluation.media", fromlist=["_run"])._run) as run:
                first = extract_audio(path, output)
                second = extract_audio(path, output)
            self.assertEqual(first, second)
            self.assertEqual(run.call_count, 1)

    def test_retry_limit_and_cancellation_recovery(self):
        from backend.app.core import db
        rows = [SimpleNamespace(status="processing", attempt_count=n, worker_id="w", heartbeat_at=None) for n in (1, 3)]
        rows.append(SimpleNamespace(status="cancel_requested", attempt_count=4, worker_id="w", heartbeat_at=None))
        class Session:
            async def scalars(self, stmt):
                return SimpleNamespace(all=lambda: rows)
        @contextlib.asynccontextmanager
        async def scope():
            yield Session()
        with patch.object(db, "session_scope", scope):
            self.assertEqual(asyncio.run(db.recover_stale_eval_tasks(120)), 3)
        self.assertEqual([row.status for row in rows], ["queued", "failed", "cancelled"])


if __name__ == "__main__":
    unittest.main()
