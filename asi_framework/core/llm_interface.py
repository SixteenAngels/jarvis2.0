"""
Language Model Bridge

Provides a standardized interface to query remote and local LLMs. Prefers
remote (e.g., GPT-5) when available, with local model as fallback.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LLMResponse:
    text: str
    raw: Any


class LLMInterface:
    def __init__(
        self,
        remote_enabled: bool = True,
        local_enabled: bool = True,
        default_remote_model: str = "gpt-5",
        default_local_model: str = "local-llm",
    ) -> None:
        self.remote_enabled = remote_enabled
        self.local_enabled = local_enabled
        self.default_remote_model = default_remote_model
        self.default_local_model = default_local_model

    def query_model(self, prompt: str, model: Optional[str] = None) -> LLMResponse:
        selected = model or self.default_remote_model
        if self.remote_enabled and selected == self.default_remote_model:
            try:
                return self._query_remote(prompt, model=selected)
            except Exception:
                if not self.local_enabled:
                    raise
        if self.local_enabled:
            return self._query_local(prompt, model=self.default_local_model)
        return LLMResponse(text="", raw=None)

    def parse_response(self, response: LLMResponse) -> Dict[str, Any]:
        return {"text": response.text}

    def summarize_context(self, context: Any) -> str:
        return str(context)[:1000]

    def _query_remote(self, prompt: str, model: str) -> LLMResponse:
        # Placeholder for remote API call
        return LLMResponse(text=f"[remote:{model}] Plan steps for: {prompt[:200]}", raw=None)

    def _query_local(self, prompt: str, model: str) -> LLMResponse:
        # Placeholder for local inference
        return LLMResponse(text=f"[local:{model}] Steps for: {prompt[:200]}", raw=None)


__all__ = ["LLMInterface", "LLMResponse"]

