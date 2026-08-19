"""LLM 与 VLM 实现：OpenAI 兼容接口（DashScope）+ Ollama。"""

from __future__ import annotations

import base64
import json
import mimetypes
from collections.abc import Iterator
from typing import Any

import httpx

from .base import ChatMessage, LLMProvider, ProviderError, VLMProvider


def _image_data_url(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{b64}"


class OpenAICompatLLM(LLMProvider):
    """走 /chat/completions 的通用实现，DashScope 兼容模式即用这个。"""

    def __init__(self, conf: dict[str, Any]) -> None:
        self.base_url = conf.get("base_url", "").rstrip("/")
        self.model = conf.get("model", "qwen3.7-plus")
        self.api_key = conf.get("api_key", "")
        self.api_key_env = conf.get("api_key_env", "DASHSCOPE_API_KEY")
        self.temperature = conf.get("temperature", 0.3)
        self.timeout = conf.get("timeout", 120)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise ProviderError(
                f"缺少 API Key：请在 .env 中设置 {self.api_key_env}（可在 "
                "https://bailian.console.aliyun.com/ 获取）。"
            )
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _payload(self, messages: list[dict], stream: bool, **kwargs) -> dict:
        return {
            "model": kwargs.pop("model", self.model),
            "messages": messages,
            "temperature": kwargs.pop("temperature", self.temperature),
            "stream": stream,
            **kwargs,
        }

    def chat(self, messages: list[ChatMessage], **kwargs) -> str:
        timeout = kwargs.pop("timeout", self.timeout)
        if isinstance(timeout, (int, float)):
            timeout = httpx.Timeout(float(timeout), connect=30.0)
        payload = self._payload(
            [{"role": m.role, "content": m.content} for m in messages], False, **kwargs
        )
        try:
            resp = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=self._headers(),
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ProviderError(
                f"LLM 调用失败 [{e.response.status_code}]: {e.response.text[:300]}"
            ) from e
        except httpx.HTTPError as e:
            raise ProviderError(f"LLM 网络错误: {e}") from e
        return resp.json()["choices"][0]["message"]["content"]

    def stream_chat(self, messages: list[ChatMessage], **kwargs) -> Iterator[str]:
        timeout = kwargs.pop("timeout", self.timeout)
        if isinstance(timeout, (int, float)):
            timeout = httpx.Timeout(float(timeout), connect=30.0)
        payload = self._payload(
            [{"role": m.role, "content": m.content} for m in messages], True, **kwargs
        )
        try:
            with httpx.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=self._headers(),
                json=payload,
                timeout=timeout,
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        delta = json.loads(data)["choices"][0].get("delta", {})
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
                    if content := delta.get("content"):
                        yield content
        except httpx.HTTPStatusError as e:
            raise ProviderError(f"LLM 流式调用失败 [{e.response.status_code}]") from e
        except httpx.HTTPError as e:
            raise ProviderError(f"LLM 网络错误: {e}") from e


class OpenAICompatVLM(OpenAICompatLLM, VLMProvider):
    """多模态：把图片作为 data URL 塞进 content 数组。"""

    def describe(
        self, image_paths: list[str], prompt: str, system: str | None = None, **kwargs
    ) -> str:
        content: list[dict] = [
            {"type": "image_url", "image_url": {"url": _image_data_url(p)}}
            for p in image_paths
        ]
        content.append({"type": "text", "text": prompt})

        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": content})

        payload = self._payload(messages, False, **kwargs)
        try:
            resp = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=self._headers(),
                json=payload,
                timeout=self.timeout,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ProviderError(
                f"VLM 调用失败 [{e.response.status_code}]: {e.response.text[:300]}"
            ) from e
        except httpx.HTTPError as e:
            raise ProviderError(f"VLM 网络错误: {e}") from e
        return resp.json()["choices"][0]["message"]["content"]


class OllamaLLM(LLMProvider):
    def __init__(self, conf: dict[str, Any]) -> None:
        self.base_url = conf.get("base_url", "http://localhost:11434").rstrip("/")
        self.model = conf.get("model", "qwen2.5:3b")
        self.temperature = conf.get("temperature", 0.3)
        self.timeout = conf.get("timeout", 300)

    def _payload(self, messages: list[dict], stream: bool, **kwargs) -> dict:
        return {
            "model": kwargs.pop("model", self.model),
            "messages": messages,
            "stream": stream,
            "options": {"temperature": kwargs.pop("temperature", self.temperature)},
        }

    def chat(self, messages: list[ChatMessage], **kwargs) -> str:
        timeout = kwargs.pop("timeout", self.timeout)
        if isinstance(timeout, (int, float)):
            timeout = httpx.Timeout(float(timeout), connect=30.0)
        payload = self._payload(
            [{"role": m.role, "content": m.content} for m in messages], False, **kwargs
        )
        try:
            resp = httpx.post(
                f"{self.base_url}/api/chat", json=payload, timeout=timeout
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise ProviderError(
                f"Ollama 调用失败: {e}。请确认 `ollama serve` 已启动且已 "
                f"`ollama pull {self.model}`。"
            ) from e
        return resp.json()["message"]["content"]

    def stream_chat(self, messages: list[ChatMessage], **kwargs) -> Iterator[str]:
        timeout = kwargs.pop("timeout", self.timeout)
        if isinstance(timeout, (int, float)):
            timeout = httpx.Timeout(float(timeout), connect=30.0)
        payload = self._payload(
            [{"role": m.role, "content": m.content} for m in messages], True, **kwargs
        )
        try:
            with httpx.stream(
                "POST", f"{self.base_url}/api/chat", json=payload, timeout=timeout
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if content := chunk.get("message", {}).get("content"):
                        yield content
                    if chunk.get("done"):
                        break
        except httpx.HTTPError as e:
            raise ProviderError(f"Ollama 流式调用失败: {e}") from e


class OllamaVLM(OllamaLLM, VLMProvider):
    def describe(
        self, image_paths: list[str], prompt: str, system: str | None = None, **kwargs
    ) -> str:
        images = []
        for p in image_paths:
            with open(p, "rb") as f:
                images.append(base64.b64encode(f.read()).decode())

        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt, "images": images})

        payload = self._payload(messages, False, **kwargs)
        try:
            resp = httpx.post(
                f"{self.base_url}/api/chat", json=payload, timeout=self.timeout
            )
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise ProviderError(
                f"Ollama VLM 调用失败: {e}。需要 `ollama pull {self.model}`。"
            ) from e
        return resp.json()["message"]["content"]


def build_llm(conf: dict[str, Any]) -> LLMProvider:
    provider = conf.get("provider", "openai_compat")
    if provider in ("openai_compat", "openai", "dashscope"):
        return OpenAICompatLLM(conf)
    if provider == "ollama":
        return OllamaLLM(conf)
    raise ProviderError(f"未知的 LLM provider: {provider}")


def build_vlm(conf: dict[str, Any]) -> VLMProvider:
    provider = conf.get("provider", "openai_compat")
    if provider in ("openai_compat", "openai", "dashscope"):
        return OpenAICompatVLM(conf)
    if provider == "ollama":
        return OllamaVLM(conf)
    raise ProviderError(f"未知的 VLM provider: {provider}")
