"""读取 config.yaml，按 mode 解析出各能力的 provider 配置。"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent

load_dotenv(ROOT / ".env")


class Settings:
    def __init__(self, config_path: Path | None = None) -> None:
        self.root = ROOT
        self.config_path = config_path or (ROOT / "config.yaml")
        with open(self.config_path, encoding="utf-8") as f:
            self.raw: dict[str, Any] = yaml.safe_load(f) or {}

    @property
    def mode(self) -> str:
        """LLM/VLM/Embedding 的运行模式。默认 cloud，仅 PKU_MODE=local 时走 Ollama。"""
        raw = (os.getenv("PKU_MODE") or self.raw.get("mode") or "cloud").strip().lower()
        return raw if raw in ("cloud", "local") else "cloud"

    def section(self, name: str) -> dict[str, Any]:
        return self.raw.get(name, {}) or {}

    def provider_config(self, capability: str) -> dict[str, Any]:
        """取某能力在当前 mode 下的配置，并把 api_key_env 解析成真实 key。"""
        cap = self.section(capability)
        conf = dict(cap.get(self.mode, {}) or {})
        key_env = conf.pop("api_key_env", None)
        if key_env:
            conf["api_key"] = os.getenv(key_env, "")
            conf["api_key_env"] = key_env
        conf.setdefault("_mode", self.mode)
        conf.setdefault("_capability", capability)
        return conf

    def flat_config(self, capability: str) -> dict[str, Any]:
        """取不分 mode 的顶层配置（ASR 用这个）。"""
        conf = dict(self.section(capability))
        key_env = conf.pop("api_key_env", None)
        if key_env:
            conf["api_key"] = os.getenv(key_env, "")
        conf.setdefault("_capability", capability)
        return conf

    def abs_path(self, value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else (self.root / p).resolve()

    @property
    def chroma_dir(self) -> Path:
        return self.abs_path(self.section("vector_store").get("persist_dir", "./data/chroma"))

    @property
    def upload_dir(self) -> Path:
        d = self.root / "data" / "uploads"
        d.mkdir(parents=True, exist_ok=True)
        return d

    @property
    def frame_dir(self) -> Path:
        d = self.root / "data" / "frames"
        d.mkdir(parents=True, exist_ok=True)
        return d

    @property
    def corpora(self) -> list[dict[str, Any]]:
        return self.raw.get("corpora", []) or []

    def corpus_names(self, include_auto: bool = True) -> list[str]:
        return [
            c["name"] for c in self.corpora if include_auto or not c.get("auto", False)
        ]

    def corpus_meta(self, name: str) -> dict[str, Any]:
        for c in self.corpora:
            if c["name"] == name:
                return c
        return {"name": name, "label": name, "description": ""}

    def corpus_dir(self, name: str) -> Path:
        return self.root / "knowledge" / "corpora" / name


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
