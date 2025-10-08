"""
Task Dispatcher & Agent Coordinator
"""

from __future__ import annotations

from typing import Any, Callable, Dict


class Router:
    def __init__(self) -> None:
        self._registry: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def dispatch(self, request: Dict[str, Any]) -> Any:
        agent = request.get("agent")
        if agent not in self._registry:
            raise KeyError(f"Agent not registered: {agent}")
        handler = self._registry[agent]
        return handler(request.get("task", {}))

    def register_agent(self, name: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self._registry[name] = handler

    def get_route_map(self) -> Dict[str, str]:
        return {name: getattr(handler, "__name__", "handler") for name, handler in self._registry.items()}


__all__ = ["Router"]

