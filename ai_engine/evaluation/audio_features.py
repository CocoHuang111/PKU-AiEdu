"""声学客观特征：用 librosa 从音轨提取响度、基频、停顿、信噪比等。

同样属于"事实层"，供 Judge 判断语气稳定性、语调变化、课堂噪音等指标。
"""

from __future__ import annotations

import numpy as np

from ..pedagogy.loader import load_yaml


class AudioFeatureError(RuntimeError):
    pass


def extract_audio_features(
    audio_path: str, asr_segments: list | None = None
) -> dict[str, float]:
    try:
        import librosa
    except ImportError as e:
        raise AudioFeatureError(
            "未安装 librosa：pip install librosa soundfile"
        ) from e

    thresholds = load_yaml("feature_lexicon.yaml")["audio_thresholds"]

    y, sr = librosa.load(audio_path, sr=16000, mono=True)
    if y.size == 0:
        raise AudioFeatureError("音频为空")

    duration = float(len(y) / sr)
    features: dict[str, float] = {"audio_duration_sec": round(duration, 1)}

    # --- 响度 ---
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    rms_db = 20 * np.log10(np.maximum(rms, 1e-10))
    voiced = rms_db > (rms_db.max() - 40)  # 只统计有声部分，避免静音拉低均值
    features["loudness_db"] = round(float(np.mean(rms_db[voiced])), 1) if voiced.any() else -60.0
    features["loudness_std"] = round(float(np.std(rms_db[voiced])), 2) if voiced.any() else 0.0

    # --- 静音与停顿 ---
    silence_mask = ~voiced
    features["silence_ratio"] = round(100.0 * float(np.mean(silence_mask)), 1)

    hop_sec = 512 / sr
    long_pause_frames = int(thresholds["long_pause_sec"] / hop_sec)
    long_pauses, run = 0, 0
    for is_silent in silence_mask:
        if is_silent:
            run += 1
        else:
            if run >= long_pause_frames:
                long_pauses += 1
            run = 0
    if run >= long_pause_frames:
        long_pauses += 1

    features["long_pause_count"] = long_pauses
    features["long_pause_per_10min"] = round(
        10.0 * long_pauses / max(duration / 60.0, 1.0), 1
    )

    # --- 基频与语调 ---
    # pyin 很慢，长音频先降采样到 8kHz 并限制分析范围
    try:
        y_pitch = librosa.resample(y, orig_sr=sr, target_sr=8000)
        f0, voiced_flag, _ = librosa.pyin(
            y_pitch,
            fmin=float(librosa.note_to_hz("C2")),
            fmax=float(librosa.note_to_hz("C6")),
            sr=8000,
            frame_length=1024,
        )
        f0_valid = f0[~np.isnan(f0)]
        if f0_valid.size > 0:
            median_f0 = float(np.median(f0_valid))
            features["pitch_median"] = round(median_f0, 1)
            features["pitch_std"] = round(float(np.std(f0_valid)), 1)
            features["pitch_variation"] = round(
                float(np.std(f0_valid)) / max(median_f0, 1.0), 3
            )
        else:
            features.update(pitch_median=0.0, pitch_std=0.0, pitch_variation=0.0)
    except Exception:
        features.update(pitch_median=0.0, pitch_std=0.0, pitch_variation=0.0)

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

    return features
