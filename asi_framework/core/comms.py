"""
System Communication Backbone
"""

from __future__ import annotations

from typing import Any, Dict


class Comms:
    def send_message(self, target: str, payload: Dict[str, Any]) -> bool:
        return True

    def receive_message(self, source: str) -> Dict[str, Any]:
        return {"source": source, "message": "ok"}

    def broadcast_update(self, data: Dict[str, Any]) -> int:
        return 1


__all__ = ["Comms"]

