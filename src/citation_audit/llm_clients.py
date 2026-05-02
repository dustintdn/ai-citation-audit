"""
llm_clients.py — Abstract LLM client interface + concrete implementations.

Providers:
  - OpenAI      (openai AsyncOpenAI SDK)
  - Anthropic   (anthropic AsyncAnthropic SDK)
  - Perplexity  (httpx, OpenAI-compatible REST API)

All clients cache raw responses to disk so the tool can be re-run without
re-querying APIs.
"""

from __future__ import annotations

import asyncio
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

import httpx
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from citation_audit.prompts import Prompt

# Max simultaneous in-flight requests per provider. Anthropic enforces a strict
# concurrent-connection limit; 3 is conservative enough to avoid 429s.
_DEFAULT_CONCURRENCY = 3

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

ModelName = str  # "openai" | "anthropic" | "perplexity"


# ---------------------------------------------------------------------------
# Raw response cache helpers
# ---------------------------------------------------------------------------

def _cache_path(raw_dir: Path, model: ModelName, prompt_index: int) -> Path:
    return raw_dir / f"{model}_{prompt_index}.json"


def _load_cached(raw_dir: Path, model: ModelName, prompt_index: int) -> str | None:
    path = _cache_path(raw_dir, model, prompt_index)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("response")
    return None


def _save_cache(
    raw_dir: Path,
    model: ModelName,
    prompt_index: int,
    prompt_text: str,
    response: str,
) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = _cache_path(raw_dir, model, prompt_index)
    payload = {
        "model": model,
        "prompt_index": prompt_index,
        "prompt": prompt_text,
        "response": response,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class LLMClient(ABC):
    """Common interface for all LLM provider clients."""

    name: ModelName  # must be set by subclasses

    def __init__(self, raw_dir: Path, concurrency: int = _DEFAULT_CONCURRENCY) -> None:
        self.raw_dir = raw_dir
        self._semaphore = asyncio.Semaphore(concurrency)

    async def query(self, prompt: Prompt, prompt_index: int) -> str:
        """
        Return the model response for *prompt*, using the on-disk cache if
        a response was already fetched. Concurrent calls are throttled by a
        per-client semaphore to avoid provider rate limits.
        """
        cached = _load_cached(self.raw_dir, self.name, prompt_index)
        if cached is not None:
            return cached

        async with self._semaphore:
            response = await self._complete(prompt.text)
        _save_cache(self.raw_dir, self.name, prompt_index, prompt.text, response)
        return response

    @abstractmethod
    async def _complete(self, prompt_text: str) -> str:
        """Send *prompt_text* to the provider and return the response string."""


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------

class OpenAIClient(LLMClient):
    name: ModelName = "openai"

    def __init__(self, raw_dir: Path, model: str = "gpt-4o") -> None:
        super().__init__(raw_dir)
        self._model = model
        self._client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

    async def _complete(self, prompt_text: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.3,
        )
        return response.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------

class AnthropicClient(LLMClient):
    name: ModelName = "anthropic"

    def __init__(self, raw_dir: Path, model: str = "claude-sonnet-4-6") -> None:
        super().__init__(raw_dir)
        self._model = model
        self._client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    async def _complete(self, prompt_text: str) -> str:
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt_text}],
        )
        block = response.content[0]
        return block.text if hasattr(block, "text") else ""


# ---------------------------------------------------------------------------
# Perplexity
# ---------------------------------------------------------------------------

_PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityClient(LLMClient):
    name: ModelName = "perplexity"

    def __init__(
        self,
        raw_dir: Path,
        model: str = "sonar-pro",
    ) -> None:
        super().__init__(raw_dir)
        self._model = model
        self._api_key = os.environ["PERPLEXITY_API_KEY"]

    async def _complete(self, prompt_text: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = client.post(_PERPLEXITY_API_URL, json=payload, headers=headers)
            resp = await resp
            resp.raise_for_status()
            data = resp.json()
        return data["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_CLIENT_MAP: dict[ModelName, type[LLMClient]] = {
    "openai": OpenAIClient,
    "anthropic": AnthropicClient,
    "perplexity": PerplexityClient,
}

AVAILABLE_MODELS: list[ModelName] = list(_CLIENT_MAP.keys())


def build_clients(models: list[ModelName], raw_dir: Path) -> list[LLMClient]:
    """
    Instantiate and return LLM clients for the requested *models*.

    Args:
        models:  List of model names (e.g. ["openai", "anthropic"]).
        raw_dir: Directory used for raw response caching.

    Raises:
        ValueError: If an unknown model name is requested.
    """
    clients: list[LLMClient] = []
    for name in models:
        cls = _CLIENT_MAP.get(name)
        if cls is None:
            raise ValueError(
                f"Unknown model '{name}'. Available: {AVAILABLE_MODELS}"
            )
        clients.append(cls(raw_dir=raw_dir))
    return clients
