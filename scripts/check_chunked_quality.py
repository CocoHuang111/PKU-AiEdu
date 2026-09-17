"""Compare old whole-clip inference with bounded inference on real audio.

Agreement is a regression metric, not accuracy against a human transcript.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import time
from dataclasses import asdict
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from ai_engine.config import settings
from ai_engine.evaluation.audio_features import extract_audio_features
from ai_engine.providers.asr import FasterWhisperASR
from ai_engine.evaluation.exceptions import EvaluationCancelled
from ai_engine.processes import run_json_worker
from unittest.mock import patch


def main(source: Path, output: Path, offset: float, seconds: float):
    output.mkdir(parents=True, exist_ok=True)
    with sf.SoundFile(source) as audio:
        audio.seek(round(offset * audio.samplerate))
        samples = audio.read(round(seconds * audio.samplerate), dtype="float32")
        rate = audio.samplerate
    if rate != 16000:
        raise ValueError("Expected 16kHz WAV")
    clip = output / "quality-clip.wav"
    sf.write(clip, samples, rate, subtype="FLOAT")
    conf = settings.flat_config("asr")
    reference = FasterWhisperASR(conf)._transcribe_one(samples)
    bounded = FasterWhisperASR({**conf, "chunk_seconds": 30}).transcribe(str(clip))
    normalized = lambda text: "".join(re.findall(r"[\w\u4e00-\u9fff]", text.lower()))
    # Before and after the ten-minute boundary in the real input, represented
    # by 30-second cores in this small regression fixture.
    started = time.monotonic()
    pitch, _, _ = librosa.pyin(
        librosa.resample(samples, orig_sr=16000, target_sr=8000),
        fmin=float(librosa.note_to_hz("C2")), fmax=float(librosa.note_to_hz("C6")),
        sr=8000, frame_length=1024, hop_length=256,
    )
    reference_pitch_seconds = time.monotonic() - started
    valid = pitch[np.isfinite(pitch)]
    started = time.monotonic()
    features = extract_audio_features(str(clip))
    bounded_pitch_seconds = time.monotonic() - started
    resume_clip = output / "quality-resume.wav"
    sf.write(resume_clip, samples, rate, subtype="FLOAT")
    first_checkpoint = resume_clip.with_suffix(".asr-checkpoint") / "00000.json"
    def interrupt(done, total):
        if done >= 30 and first_checkpoint.exists():
            raise EvaluationCancelled()
    try:
        FasterWhisperASR({**conf, "chunk_seconds": 30}).transcribe(str(resume_clip), progress_callback=interrupt)
    except EvaluationCancelled:
        pass
    if not first_checkpoint.exists():
        raise RuntimeError("Expected the first completed chunk to survive interruption")
    with patch("ai_engine.providers.asr.run_json_worker", wraps=run_json_worker) as calls:
        resumed = FasterWhisperASR({**conf, "chunk_seconds": 30}).transcribe(str(resume_clip))
    if calls.call_count != int(np.ceil(len(samples) / rate / 30)) - 1:
        raise RuntimeError("Resume reprocessed completed chunks")
    summary = {
        "offset_sec": offset, "duration_sec": len(samples) / rate,
        "normalized_transcript_agreement": difflib.SequenceMatcher(
            None, normalized(reference.text), normalized(bounded.text), autojunk=False,
        ).ratio(),
        "whole_asr": asdict(reference), "chunked_asr": asdict(bounded),
        "whole_pitch_median": float(np.median(valid)) if len(valid) else None,
        "whole_pitch_std": float(np.std(valid)) if len(valid) else None,
        "chunked_pitch_median": features.get("pitch_median"),
        "chunked_pitch_std": features.get("pitch_std"),
        "whole_pitch_seconds": reference_pitch_seconds,
        "chunked_audio_features_seconds": bounded_pitch_seconds,
        "resume_remaining_child_calls": calls.call_count,
        "resume_text_matches_uninterrupted_chunks": resumed.text == bounded.text,
    }
    (output / "quality.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k not in ("whole_asr", "chunked_asr")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--offset", type=float, default=570)
    parser.add_argument("--seconds", type=float, default=60)
    args = parser.parse_args()
    main(args.audio, args.output, args.offset, args.seconds)
