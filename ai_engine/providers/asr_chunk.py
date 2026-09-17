"""One bounded audio slice, one model lifetime. Invoked by the ASR provider."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict

import soundfile as sf

from ai_engine.processes import emit
from ai_engine.providers.asr import FasterWhisperASR


def main():
    request = json.load(sys.stdin)
    with sf.SoundFile(request["audio_path"]) as audio:
        rate = audio.samplerate
        start = round(request["read_start"] * rate)
        stop = round(request["read_end"] * rate)
        audio.seek(start)
        samples = audio.read(stop - start, dtype="float32", always_2d=True).mean(axis=1)
    if rate != 16000:
        import librosa
        samples = librosa.resample(samples, orig_sr=rate, target_sr=16000)
    provider = FasterWhisperASR(request["conf"])
    result = provider._transcribe_one(
        samples, request["language"],
        lambda done, total: emit("progress", {"done_sec": done}),
    )
    emit("result", asdict(result))


if __name__ == "__main__":
    main()
