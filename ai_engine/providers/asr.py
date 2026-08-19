"""ASR：只有本地 faster-whisper 一种实现，不随 config.yaml 的 mode 切换。

将来若要接云端，只需在本文件新增一个 ASRProvider 子类并在 build_asr 里加一个分支，
业务代码（evaluation pipeline）无需改动。
"""

from __future__ import annotations

from typing import Any

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
        self._model = WhisperModel(
            self.model_name, device=self.device, compute_type=self.compute_type
        )
        return self._model

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
        progress_callback=None,
    ) -> ASRResult:
        model = self._load()
        segments_iter, info = model.transcribe(
            audio_path,
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
