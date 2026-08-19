"""Embedding 与 Rerank 实现。"""

from __future__ import annotations

from typing import Any

import httpx

from .base import EmbeddingProvider, ProviderError, RerankProvider, RerankResult


class OpenAICompatEmbedding(EmbeddingProvider):
    def __init__(self, conf: dict[str, Any]) -> None:
        self.base_url = conf.get("base_url", "").rstrip("/")
        self.model = conf.get("model", "text-embedding-v3")
        self.api_key = conf.get("api_key", "")
        self.api_key_env = conf.get("api_key_env", "DASHSCOPE_API_KEY")
        self.timeout = conf.get("timeout", 60)
        self.batch_size = conf.get("batch_size", 10)
        self._dim: int | None = None

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise ProviderError(
                f"缺少 API Key：请在 .env 中设置 {self.api_key_env}。"
            )
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        out: list[list[float]] = []
        # DashScope 的 text-embedding-v3 单次最多 10 条，必须分批
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            try:
                resp = httpx.post(
                    f"{self.base_url}/embeddings",
                    headers=self._headers(),
                    json={"model": self.model, "input": batch},
                    timeout=self.timeout,
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise ProviderError(
                    f"Embedding 调用失败 [{e.response.status_code}]: "
                    f"{e.response.text[:300]}"
                ) from e
            except httpx.HTTPError as e:
                raise ProviderError(f"Embedding 网络错误: {e}") from e
            data = sorted(resp.json()["data"], key=lambda d: d.get("index", 0))
            out.extend(d["embedding"] for d in data)
        if out:
            self._dim = len(out[0])
        return out

    @property
    def dim(self) -> int:
        if self._dim is None:
            self._dim = len(self.embed_one("维度探测"))
        return self._dim


class OllamaEmbedding(EmbeddingProvider):
    def __init__(self, conf: dict[str, Any]) -> None:
        self.base_url = conf.get("base_url", "http://localhost:11434").rstrip("/")
        self.model = conf.get("model", "bge-m3")
        self.timeout = conf.get("timeout", 120)
        self._dim: int | None = None

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        try:
            resp = httpx.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": texts},
                timeout=self.timeout,
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise ProviderError(
                f"Ollama Embedding 失败: {e}。需要 `ollama pull {self.model}`。"
            ) from e
        out = resp.json()["embeddings"]
        if out:
            self._dim = len(out[0])
        return out

    @property
    def dim(self) -> int:
        if self._dim is None:
            self._dim = len(self.embed_one("维度探测"))
        return self._dim


class SentenceTransformerEmbedding(EmbeddingProvider):
    def __init__(self, conf: dict[str, Any]) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ProviderError(
                "未安装 sentence-transformers：pip install -r requirements-local.txt"
            ) from e
        self.model = SentenceTransformer(
            conf.get("model", "BAAI/bge-small-zh-v1.5"),
            device=conf.get("device", "cpu"),
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    @property
    def dim(self) -> int:
        return int(self.model.get_sentence_embedding_dimension())


class IdentityRerank(RerankProvider):
    """不做重排，保持原有顺序（向量分数序）。"""

    def rerank(
        self, query: str, documents: list[str], top_n: int | None = None
    ) -> list[RerankResult]:
        results = [RerankResult(index=i, score=1.0) for i in range(len(documents))]
        return results[:top_n] if top_n else results


class CrossEncoderRerank(RerankProvider):
    def __init__(self, conf: dict[str, Any]) -> None:
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as e:
            raise ProviderError(
                "未安装 sentence-transformers：pip install -r requirements-local.txt"
            ) from e
        self.model = CrossEncoder(
            conf.get("model", "BAAI/bge-reranker-base"),
            device=conf.get("device", "cpu"),
        )

    def rerank(
        self, query: str, documents: list[str], top_n: int | None = None
    ) -> list[RerankResult]:
        if not documents:
            return []
        scores = self.model.predict([(query, d) for d in documents])
        ranked = sorted(
            (RerankResult(index=i, score=float(s)) for i, s in enumerate(scores)),
            key=lambda r: r.score,
            reverse=True,
        )
        return ranked[:top_n] if top_n else ranked


def build_embedder(conf: dict[str, Any]) -> EmbeddingProvider:
    provider = conf.get("provider", "openai_compat")
    if provider in ("openai_compat", "openai", "dashscope"):
        return OpenAICompatEmbedding(conf)
    if provider == "ollama":
        return OllamaEmbedding(conf)
    if provider in ("sentence_transformers", "bge"):
        return SentenceTransformerEmbedding(conf)
    raise ProviderError(f"未知的 Embedding provider: {provider}")


def build_reranker(conf: dict[str, Any]) -> RerankProvider:
    provider = conf.get("provider", "none")
    if provider in ("none", "identity", ""):
        return IdentityRerank()
    if provider in ("sentence_transformers", "cross_encoder", "bge"):
        return CrossEncoderRerank(conf)
    raise ProviderError(f"未知的 Rerank provider: {provider}")
