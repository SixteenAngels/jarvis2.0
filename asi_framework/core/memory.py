"""
Long- & Short-Term Memory System

Stores experiences and provides simple recall. Uses an in-memory buffer and
optionally writes to disk for persistence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class Memory:
    def __init__(self, persist_path: Optional[Path] = None, max_events: int = 1000) -> None:
        self.events: List[Dict[str, Any]] = []
        self.persist_path = persist_path or Path(__file__).parent / "memory.jsonl"
        self.max_events = max_events

    def remember(self, event: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        record = {"event": event, "metadata": metadata or {}}
        self.events.append(record)
        if len(self.events) > self.max_events:
            self.events.pop(0)

    def recall(self, context: Any) -> List[Dict[str, Any]]:
        return self.events[-10:]

    def forget(self, criteria: Optional[Any] = None) -> None:
        if callable(criteria):
            self.events = [e for e in self.events if not criteria(e)]
        else:
            self.events.clear()

    def sync_to_disk(self) -> None:
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        with self.persist_path.open("a", encoding="utf-8") as f:
            for record in self.events:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.events.clear()


__all__ = ["Memory"]

