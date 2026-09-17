"""声学客观特征：用 librosa 从音轨提取响度、基频、停顿、信噪比等。

同样属于"事实层"，供 Judge 判断语气稳定性、语调变化、课堂噪音等指标。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from ..pedagogy.loader import load_yaml
from .. import checkpoints
from ..processes import run_json_worker

# 只给页面画曲线，不进 rubric / Judge / GB
AUDIO_SERIES_KEYS = (
    "audio_duration_sec",
    "wave_envelope",
    "loudness_curve",
    "pitch_curve",
    "long_pause_times",
)


class AudioFeatureError(RuntimeError):
    pass


def _curve(times: np.ndarray, values: np.ndarray, n: int = 160) -> list[list[float]]:
    finite = np.isfinite(values)
    times = times[finite]
    values = values[finite]
    if times.size == 0:
        return []
    t0, t1 = float(times[0]), float(times[-1])
    if t1 <= t0:
        return [[round(t0, 2), round(float(values[0]), 1)]]
    edges = np.linspace(t0, t1, n + 1)
    out: list[list[float]] = []
    for i in range(n):
        lo, hi = edges[i], edges[i + 1]
        mask = (times >= lo) & (times <= hi if i == n - 1 else times < hi)
        chunk = values[mask]
        if chunk.size == 0:
            continue
        out.append([round(float((lo + hi) / 2), 2), round(float(np.median(chunk)), 2)])
    return out


def _window(audio, start: int, count: int) -> np.ndarray:
    """Read only a bounded window, with the same zero padding as librosa."""
    left = max(0, -start)
    audio.seek(max(0, start))
    actual = max(0, min(count - left, audio.frames - max(0, start)))
    values = audio.read(actual, dtype="float32", always_2d=True).mean(axis=1)
    return np.pad(values, (left, max(0, count - left - values.size)))


def _stream_rms(audio, librosa, progress_callback=None, block_seconds=30):
    hop, frame = 512, 2048
    total = 1 + audio.frames // hop
    per_block = max(1, round(block_seconds * audio.samplerate / hop))
    parts = []
    for start in range(0, total, per_block):
        count = min(per_block, total - start)
        samples = _window(audio, start * hop - frame // 2, (count - 1) * hop + frame)
        parts.append(librosa.feature.rms(
            y=samples, frame_length=frame, hop_length=hop, center=False,
        )[0])
        if progress_callback:
            progress_callback("loudness", min((start + count) * hop / audio.samplerate, audio.frames / audio.samplerate), audio.frames / audio.samplerate)
    return np.concatenate(parts)


def _stream_pitch(audio, path, librosa, signature, progress_callback=None, block_seconds=30):
    # 16kHz input -> 8kHz pitch; the input hop is 512 samples = 32ms.
    hop, context_frames = 512, 8
    total = 1 + audio.frames // hop
    per_block = max(1, round(block_seconds * audio.samplerate / hop))
    parts = []
    for index, start in enumerate(range(0, total, per_block)):
        count = min(per_block, total - start)
        checkpoint = Path(path).with_suffix(".audio-checkpoint") / f"pitch-{index:05d}.json"
        saved = checkpoints.read(checkpoint, signature)
        if saved is None:
            samples = _window(audio, (start - context_frames) * hop, (count + 2 * context_frames) * hop)
            pitch_samples = librosa.resample(samples, orig_sr=16000, target_sr=8000)
            f0, _, _ = librosa.pyin(
                pitch_samples, fmin=float(librosa.note_to_hz("C2")),
                fmax=float(librosa.note_to_hz("C6")), sr=8000,
                frame_length=1024, hop_length=256,
            )
            values = f0[context_frames:context_frames + count]
            if values.size != count:
                raise AudioFeatureError("基频分块返回帧数不一致")
            saved = [float(value) if np.isfinite(value) else None for value in values]
            checkpoints.write(checkpoint, signature, saved)
        parts.append(np.array([np.nan if v is None else v for v in saved]))
        if progress_callback:
            progress_callback("pitch", min((start + count) * hop / audio.samplerate, audio.frames / audio.samplerate), audio.frames / audio.samplerate)
    return np.concatenate(parts)


def _wave_envelope(audio):
    n = min(360, max(8, audio.frames // 64))
    win = max(1, audio.frames // n)
    peaks = []
    # A single display bin can itself be large for very long media. Bound reads.
    for index in range(n):
        audio.seek(index * win)
        remaining, peak = min(win, audio.frames - index * win), 0.0
        while remaining > 0:
            count = min(remaining, audio.samplerate * 30)
            values = audio.read(count, dtype="float32", always_2d=True).mean(axis=1)
            peak = max(peak, float(np.max(np.abs(values))))
            remaining -= count
        peaks.append(peak)
    peak = max(peaks) or 1.0
    return [round(value / peak, 4) for value in peaks]


def extract_audio_features(
    audio_path: str, asr_segments: list | None = None, progress_callback=None,
    block_seconds: float = 30,
) -> dict[str, Any]:
    try:
        import librosa
    except ImportError as e:
        raise AudioFeatureError(
            "未安装 librosa：pip install librosa soundfile"
        ) from e

    thresholds = load_yaml("feature_lexicon.yaml")["audio_thresholds"]

    import soundfile as sf

    signature = checkpoints.identity(audio_path, {"audio_features": 2, "block_seconds": block_seconds})
    final_path = Path(audio_path).with_suffix(".audio-features.json")
    cached = checkpoints.read(final_path, signature)
    if cached is not None:
        if progress_callback:
            progress_callback("cached", cached["audio_duration_sec"], cached["audio_duration_sec"])
        return cached
    with sf.SoundFile(audio_path) as audio:
        sr = audio.samplerate
        if sr != 16000 or audio.frames == 0:
            raise AudioFeatureError("声学分析需要非空的16kHz音频")
        duration = float(audio.frames / sr)
        rms = _stream_rms(audio, librosa, progress_callback, block_seconds)
        envelope = _wave_envelope(audio)
        pitch_warning = None
        try:
            f0 = _stream_pitch(audio, audio_path, librosa, signature, progress_callback, block_seconds)
        except Exception as exc:
            # Cancellation raised by a callback must propagate, not become a warning.
            from .exceptions import EvaluationCancelled
            if isinstance(exc, EvaluationCancelled):
                raise
            f0 = np.array([], dtype=float)
            pitch_warning = str(exc)

    features: dict[str, Any] = {"audio_duration_sec": round(duration, 1)}

    # --- 响度 ---
    hop_length = 512
    rms_db = 20 * np.log10(np.maximum(rms, 1e-10))
    voiced = rms_db > (rms_db.max() - 40)  # 只统计有声部分，避免静音拉低均值
    features["loudness_db"] = round(float(np.mean(rms_db[voiced])), 1) if voiced.any() else -60.0
    features["loudness_std"] = round(float(np.std(rms_db[voiced])), 2) if voiced.any() else 0.0
    hop_sec = hop_length / sr
    rms_times = np.arange(rms_db.size) * hop_sec
    features["loudness_curve"] = _curve(rms_times, rms_db)

    # 波形包络：按窗口取峰值，页面画对称波形，不把原始采样塞进结果
    features["wave_envelope"] = envelope

    # --- 静音与停顿 ---
    silence_mask = ~voiced
    features["silence_ratio"] = round(100.0 * float(np.mean(silence_mask)), 1)

    long_pause_frames = int(thresholds["long_pause_sec"] / hop_sec)
    long_pauses, run = 0, 0
    pause_times: list[float] = []
    for i, is_silent in enumerate(silence_mask):
        if is_silent:
            run += 1
        else:
            if run >= long_pause_frames:
                long_pauses += 1
                pause_times.append(round(float((i - run) * hop_sec), 1))
            run = 0
    if run >= long_pause_frames:
        long_pauses += 1
        pause_times.append(round(float((len(silence_mask) - run) * hop_sec), 1))

    features["long_pause_count"] = long_pauses
    features["long_pause_times"] = pause_times
    features["long_pause_per_10min"] = round(
        10.0 * long_pauses / max(duration / 60.0, 1.0), 1
    )

    # --- 基频与语调 ---
    # Full-duration coverage, but only one 30-second pYIN matrix at a time.
    if pitch_warning is None:
        features["pitch_available"] = True
        f0_valid = f0[~np.isnan(f0)]
        hop_pitch = 256 / 8000
        f0_times = np.arange(f0.size) * hop_pitch
        features["pitch_curve"] = _curve(f0_times, f0)
        if f0_valid.size > 0:
            median_f0 = float(np.median(f0_valid))
            features["pitch_median"] = round(median_f0, 1)
            features["pitch_std"] = round(float(np.std(f0_valid)), 1)
            features["pitch_variation"] = round(
                float(np.std(f0_valid)) / max(median_f0, 1.0), 3
            )
        else:
            features.update(pitch_median=0.0, pitch_std=0.0, pitch_variation=0.0)
    else:
        features.update(pitch_available=False, pitch_warning=pitch_warning, pitch_curve=[])

    # --- 信噪比估计：有声帧能量 vs 静音帧能量 ---
    if voiced.any() and silence_mask.any():
        signal_power = float(np.mean(rms[voiced] ** 2))
        noise_power = float(np.mean(rms[silence_mask] ** 2))
        snr = 10 * np.log10(max(signal_power, 1e-12) / max(noise_power, 1e-12))
        features["snr_estimate"] = round(float(snr), 1)
    else:
        features["snr_estimate"] = 0.0

    # --- 重音节奏：响度峰值密度，反映强调是否充分 ---
    peak_threshold = float(np.mean(rms) + np.std(rms))
    peaks = int(np.sum((rms[1:-1] > rms[:-2]) & (rms[1:-1] > rms[2:]) & (rms[1:-1] > peak_threshold)))
    features["emphasis_per_min"] = round(peaks / max(duration / 60.0, 1.0), 1)

    # Do not permanently cache a transient partial result.
    if pitch_warning is None:
        checkpoints.write(final_path, signature, features)
    return features


def extract_audio_features_isolated(audio_path: str, progress_callback=None):
    return run_json_worker("ai_engine.evaluation.audio_features", {
        "audio_path": str(Path(audio_path).resolve()),
    }, lambda value: progress_callback(
        (value or {}).get("phase", "starting"),
        float((value or {}).get("done_sec", 0)),
        float((value or {}).get("total_sec", 1)),
    ) if progress_callback else None, timeout=3600)


if __name__ == "__main__":
    import json
    import sys
    from ..processes import emit

    request = json.load(sys.stdin)
    result = extract_audio_features(request["audio_path"], progress_callback=lambda phase, done, total: emit(
        "progress", {"phase": phase, "done_sec": done, "total_sec": total},
    ))
    emit("result", result)
