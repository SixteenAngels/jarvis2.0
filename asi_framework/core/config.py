"""
System Configuration Manager
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    def __init__(self, base_path: Optional[Path] = None) -> None:
        self.base_path = base_path or Path(__file__).resolve().parent.parent
        self._config: Dict[str, Any] = {}

    def load_config(self) -> None:
        self._config.update({
            "ENV": os.getenv("ENV", "dev"),
            "REMOTE_LLM": os.getenv("REMOTE_LLM", "gpt-5"),
            "LOCAL_LLM": os.getenv("LOCAL_LLM", "local-llm"),
        })

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._config[key] = value


__all__ = ["Config"]

