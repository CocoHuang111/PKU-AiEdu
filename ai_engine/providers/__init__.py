"""AI 能力工厂。业务代码统一通过 get_xxx() 获取 provider。"""

from __future__ import annotations

from functools import lru_cache

from ..config import settings
from .asr import build_asr
from .base import (
    ASRProvider,
    ASRResult,
    ASRSegment,
    ChatMessage,
    EmbeddingProvider,
    LLMProvider,
    ProviderError,
    RerankProvider,
    RerankResult,
    VLMProvider,
)
from .embedding import build_embedder, build_reranker
from .llm import build_llm, build_vlm

__all__ = [
    "ASRProvider",
    "ASRResult",
    "ASRSegment",
    "ChatMessage",
    "EmbeddingProvider",
    "LLMProvider",
    "ProviderError",
    "RerankProvider",
    "RerankResult",
    "VLMProvider",
    "get_llm",
    "get_vlm",
    "get_embedder",
    "get_reranker",
    "get_asr",
    "reset_providers",
]


@lru_cache(maxsize=1)
def get_llm() -> LLMProvider:
    return build_llm(settings.provider_config("llm"))


@lru_cache(maxsize=1)
def get_vlm() -> VLMProvider:
    return build_vlm(settings.provider_config("vlm"))


@lru_cache(maxsize=1)
def get_embedder() -> EmbeddingProvider:
    return build_embedder(settings.provider_config("embedding"))


@lru_cache(maxsize=1)
def get_reranker() -> RerankProvider:
    return build_reranker(settings.provider_config("rerank"))


@lru_cache(maxsize=1)
def get_asr() -> ASRProvider:
    # ASR 读顶层配置，不分 cloud/local
    return build_asr(settings.flat_config("asr"))


def reset_providers() -> None:
    for fn in (get_llm, get_vlm, get_embedder, get_reranker, get_asr):
        fn.cache_clear()
