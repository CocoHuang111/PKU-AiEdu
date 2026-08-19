"""AI 能力抽象接口。业务代码只依赖这些接口，不关心背后是云端还是本地。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field


class ProviderError(RuntimeError):
    """provider 不可用或调用失败。"""


@dataclass
class ChatMessage:
    role: str  # system | user | assistant
    content: str


@dataclass
class ASRSegment:
    start: float
    end: float
    text: str
    # Whisper 自带的解码质量指标。混杂了录音质量、口音与术语生僻度，
    # 只能作为「口齿清晰」的弱代理，且不同模型规模之间数值不可比。
    avg_logprob: float | None = None
    no_speech_prob: float | None = None


@dataclass
class ASRResult:
    text: str
    segments: list[ASRSegment] = field(default_factory=list)
    language: str = "zh"
    duration: float = 0.0


@dataclass
class RerankResult:
    index: int
    score: float


class LLMProvider(ABC):
    name: str = "llm"

    @abstractmethod
    def chat(self, messages: list[ChatMessage], **kwargs) -> str: ...

    @abstractmethod
    def stream_chat(self, messages: list[ChatMessage], **kwargs) -> Iterator[str]: ...

    def complete(self, prompt: str, system: str | None = None, **kwargs) -> str:
        messages = []
        if system:
            messages.append(ChatMessage("system", system))
        messages.append(ChatMessage("user", prompt))
        return self.chat(messages, **kwargs)

    def stream_complete(
        self, prompt: str, system: str | None = None, **kwargs
    ) -> Iterator[str]:
        messages = []
        if system:
            messages.append(ChatMessage("system", system))
        messages.append(ChatMessage("user", prompt))
        yield from self.stream_chat(messages, **kwargs)


class VLMProvider(ABC):
    """视觉语言模型：看图 + 文字指令 → 文字输出。"""

    name: str = "vlm"

    @abstractmethod
    def describe(
        self, image_paths: list[str], prompt: str, system: str | None = None, **kwargs
    ) -> str: ...


class EmbeddingProvider(ABC):
    name: str = "embedding"

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]: ...

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]

    @property
    @abstractmethod
    def dim(self) -> int: ...


class RerankProvider(ABC):
    name: str = "rerank"

    @abstractmethod
    def rerank(
        self, query: str, documents: list[str], top_n: int | None = None
    ) -> list[RerankResult]: ...


class ASRProvider(ABC):
    name: str = "asr"

    @abstractmethod
    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
        progress_callback=None,
    ) -> ASRResult:
        """progress_callback(done_seconds, total_seconds) 用于上报转写进度。"""
