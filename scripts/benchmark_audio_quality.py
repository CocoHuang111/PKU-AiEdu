"""Compare ASR and acoustic features before and after speech compression."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import time
from pathlib import Path

from ai_engine.config import settings
from ai_engine.evaluation.audio_features import AUDIO_SERIES_KEYS, extract_audio_features
from ai_engine.providers.asr import build_asr


SCALAR_AUDIO_KEYS = (
    "audio_duration_sec",
    "loudness_db",
    "loudness_std",
    "silence_ratio",
    "long_pause_count",
    "long_pause_per_10min",
    "pitch_median",
    "pitch_std",
    "pitch_variation",
    "snr_estimate",
    "emphasis_per_min",
)


def elapsed(callable_, *args):
    started = time.perf_counter()
    value = callable_(*args)
    return value, time.perf_counter() - started


def to_wav(source: Path, destination: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(destination),
        ],
        check=True,
    )


def normalized(text: str) -> str:
    return "".join(re.findall(r"[\w\u4e00-\u9fff]", text.lower()))


def scalar_features(features: dict) -> dict:
    return {key: features.get(key) for key in SCALAR_AUDIO_KEYS}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("original_audio", type=Path)
    parser.add_argument("compact_audio", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    original_wav = args.output / "original-16k.wav"
    compact_wav = args.output / "compact-16k.wav"
    _, original_decode_sec = elapsed(to_wav, args.original_audio, original_wav)
    _, compact_decode_sec = elapsed(to_wav, args.compact_audio, compact_wav)

    asr = build_asr(settings.flat_config("asr"))
    original_asr, original_asr_sec = elapsed(asr.transcribe, str(original_wav))
    compact_asr, compact_asr_sec = elapsed(asr.transcribe, str(compact_wav))

    original_text = normalized(original_asr.text)
    compact_text = normalized(compact_asr.text)
    similarity = difflib.SequenceMatcher(None, original_text, compact_text).ratio()

    original_features, original_features_sec = elapsed(
        extract_audio_features, str(original_wav), original_asr.segments
    )
    compact_features, compact_features_sec = elapsed(
        extract_audio_features, str(compact_wav), compact_asr.segments
    )
    original_scalars = scalar_features(original_features)
    compact_scalars = scalar_features(compact_features)
    differences = {}
    for key in SCALAR_AUDIO_KEYS:
        left = original_scalars.get(key)
        right = compact_scalars.get(key)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            differences[key] = round(float(right) - float(left), 4)

    report = {
        "inputs": {
            "original_audio": str(args.original_audio),
            "original_bytes": args.original_audio.stat().st_size,
            "compact_audio": str(args.compact_audio),
            "compact_bytes": args.compact_audio.stat().st_size,
        },
        "asr": {
            "normalized_text_similarity": round(similarity, 6),
            "original_chars": len(original_text),
            "compact_chars": len(compact_text),
            "original_segments": len(original_asr.segments),
            "compact_segments": len(compact_asr.segments),
            "original_text": original_asr.text,
            "compact_text": compact_asr.text,
        },
        "audio_features": {
            "original": original_scalars,
            "compact": compact_scalars,
            "compact_minus_original": differences,
            "omitted_series": list(AUDIO_SERIES_KEYS),
        },
        "timings_sec": {
            "original_decode": round(original_decode_sec, 3),
            "compact_decode": round(compact_decode_sec, 3),
            "original_asr": round(original_asr_sec, 3),
            "compact_asr": round(compact_asr_sec, 3),
            "original_audio_features": round(original_features_sec, 3),
            "compact_audio_features": round(compact_features_sec, 3),
        },
    }
    report_path = args.output / "audio-quality.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
