"""
Central Logging System
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


class Logger:
    def __init__(self, persist_path: Optional[Path] = None) -> None:
        self._buffer: List[Dict[str, Any]] = []
        self.persist_path = persist_path or Path(__file__).parent / "system.log"

    def log(self, event: Dict[str, Any], level: str = "info") -> None:
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            **event,
        }
        self._buffer.append(record)

    def get_logs(self, filter_by: Optional[Dict[str, Any]] = None) -> Iterable[Dict[str, Any]]:
        if not filter_by:
            return list(self._buffer)
        def match(rec: Dict[str, Any]) -> bool:
            return all(rec.get(k) == v for k, v in filter_by.items())
        return [r for r in self._buffer if match(r)]

    def export_logs(self, path: Optional[Path] = None) -> Path:
        target = path or self.persist_path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            for record in self._buffer:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._buffer.clear()
        return target


__all__ = ["Logger"]

