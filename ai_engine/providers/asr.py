"""ASR：只有本地 faster-whisper 一种实现，不随 config.yaml 的 mode 切换。

将来若要接云端，只需在本文件新增一个 ASRProvider 子类并在 build_asr 里加一个分支，
业务代码（evaluation pipeline）无需改动。
"""

from __future__ import annotations

import math
import os
import time
from pathlib import Path
from typing import Any

from .. import checkpoints
from ..processes import run_json_worker

from .base import ASRProvider, ASRResult, ASRSegment, ProviderError


def _to_simplified(text: str) -> str:
    """Whisper 转写中文时经常输出繁体，这里统一转成简体。

    不转的话下游的关键词表（"为什么""想一想"等）会全部匹配不上，
    提问次数、启发次数这类客观特征会假性归零。
    """
    try:
        from zhconv import convert

        return convert(text, "zh-cn")
    except ImportError:
        return text


class FasterWhisperASR(ASRProvider):
    def __init__(self, conf: dict[str, Any]) -> None:
        self.model_name = conf.get("model", "base")
        self.language = conf.get("language", "zh")
        self.device = conf.get("device", "cpu")
        self.compute_type = conf.get("compute_type", "int8")
        self.vad_filter = conf.get("vad_filter", True)
        self.chunk_seconds = max(30, float(conf.get("chunk_seconds", 600)))
        self.overlap_seconds = max(0, min(5, float(conf.get("overlap_seconds", 2))))
        self.cpu_threads = max(1, int(conf.get("cpu_threads", min(os.cpu_count() or 1, 4))))
        self.chunk_timeout = max(60, float(conf.get("chunk_timeout", 1800)))
        self._model = None

    def _load(self):
        if self._model is not None:
            return self._model
        try:
            from faster_whisper import WhisperModel
        except ImportError as e:
            raise ProviderError(
                "ASR 未就绪：未安装 faster-whisper。\n"
                "  pip install faster-whisper\n"
                "注意需要 Python 3.11（3.13+ 缺少 ctranslate2 的 arm64 wheel）。"
            ) from e
        # 首次加载会从 HuggingFace 下载权重，可用 .env 的 HF_HOME 指定缓存目录
        from huggingface_hub.utils import LocalEntryNotFoundError
        options = {"device": self.device, "compute_type": self.compute_type,
                   "cpu_threads": self.cpu_threads}
        try:
            # Cached models must not repeat slow HuggingFace HEAD requests per core.
            self._model = WhisperModel(self.model_name, local_files_only=True, **options)
        except LocalEntryNotFoundError:
            self._model = WhisperModel(self.model_name, local_files_only=False, **options)
        return self._model

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
        progress_callback=None,
    ) -> ASRResult:
        import soundfile as sf

        info = sf.info(audio_path)
        total = info.frames / info.samplerate
        if total <= 0:
            raise ProviderError("音频为空")
        lang = language or self.language
        conf = {
            "model": self.model_name, "device": self.device,
            "compute_type": self.compute_type, "vad_filter": self.vad_filter,
            "cpu_threads": self.cpu_threads,
        }
        signature = checkpoints.identity(audio_path, {
            "version": 1, **conf, "language": lang,
            "chunk_seconds": self.chunk_seconds, "overlap_seconds": self.overlap_seconds,
        })
        folder = Path(audio_path).with_suffix(".asr-checkpoint")
        segments: list[ASRSegment] = []
        detected = lang
        for index in range(math.ceil(total / self.chunk_seconds)):
            start = index * self.chunk_seconds
            end = min(total, start + self.chunk_seconds)
            path = folder / f"{index:05d}.json"
            chunk = checkpoints.read(path, signature)
            if progress_callback:
                progress_callback(start, total)
            if chunk is None:
                chunk_started = time.monotonic()
                read_start = max(0, start - self.overlap_seconds)
                read_end = min(total, end + self.overlap_seconds)

                def on_progress(value):
                    if progress_callback:
                        done = read_start + float((value or {}).get("done_sec", 0))
                        progress_callback(max(start, min(done, end)), total)

                raw = run_json_worker("ai_engine.providers.asr_chunk", {
                    "audio_path": str(Path(audio_path).resolve()), "conf": conf,
                    "language": lang, "read_start": read_start, "read_end": read_end,
                }, on_progress, self.chunk_timeout)
                kept = []
                for item in raw["segments"]:
                    left, right = read_start + item["start"], read_start + item["end"]
                    # Each overlapping segment belongs to exactly one core by its midpoint.
                    if start <= (left + right) / 2 < end:
                        kept.append({**item, "start": max(start, left), "end": min(end, right)})
                chunk = {"segments": kept, "language": raw["language"],
                         "child_peak_rss_mb": raw.get("child_peak_rss_mb")}
                checkpoints.write(path, signature, chunk)
                print(f"[asr] core={index+1} seconds={start:g}-{end:g} elapsed={time.monotonic()-chunk_started:.1f}s child_peak_rss_mb={raw.get('child_peak_rss_mb')}", flush=True)
            detected = chunk["language"]
            segments.extend(ASRSegment(**item) for item in chunk["segments"])
            if progress_callback:
                progress_callback(end, total)
        return ASRResult(
            text="".join(s.text for s in segments), segments=segments,
            language=detected, duration=total,
        )

    def _transcribe_one(self, audio, language=None, progress_callback=None) -> ASRResult:
        """Child-only model inference; input is a bounded 16kHz array."""
        model = self._load()
        segments_iter, info = model.transcribe(
            audio,
            language=language or self.language,
            vad_filter=self.vad_filter,
            beam_size=5,
        )

        total = float(getattr(info, "duration", 0.0) or 0.0)
        detected = getattr(info, "language", self.language)
        simplify = str(detected).startswith("zh")

        segments: list[ASRSegment] = []
        # faster-whisper 返回的是惰性生成器，边消费边上报进度，
        # 前端进度条才不会在这一步长时间卡死
        for seg in segments_iter:
            text = (seg.text or "").strip()
            if text:
                if simplify:
                    text = _to_simplified(text)
                segments.append(
                    ASRSegment(
                        start=seg.start,
                        end=seg.end,
                        text=text,
                        avg_logprob=getattr(seg, "avg_logprob", None),
                        no_speech_prob=getattr(seg, "no_speech_prob", None),
                    )
                )
            if progress_callback and total > 0:
                progress_callback(min(seg.end, total), total)

        return ASRResult(
            text="".join(s.text for s in segments),
            segments=segments,
            language=detected,
            duration=total or (segments[-1].end if segments else 0.0),
        )


def build_asr(conf: dict[str, Any]) -> ASRProvider:
    provider = conf.get("provider", "faster_whisper")
    if provider == "faster_whisper":
        return FasterWhisperASR(conf)
    raise ProviderError(
        f"未知的 ASR provider: {provider}（当前只实现了 faster_whisper）"
    )
