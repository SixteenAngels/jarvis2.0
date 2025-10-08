"""
Central Cognitive Engine (brain)

Responsibilities:
- Process incoming tasks/goals
- Route to appropriate agents via the router
- Coordinate multi-agent workflows
- Adapt based on feedback and memory context
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .memory import Memory
from .llm_interface import LLMInterface, LLMResponse
from .router import Router
from .logger import Logger


class Brain:
    def __init__(
        self,
        memory: Memory,
        router: Router,
        llm: LLMInterface,
        logger: Optional[Logger] = None,
    ) -> None:
        self.memory = memory
        self.router = router
        self.llm = llm
        self.logger = logger or Logger()

    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        context = self.memory.recall(task)
        prompt = self._build_prompt(task, context)
        self.logger.log({"event": "brain.process_task.start", "task": task})
        reasoning: LLMResponse = self.llm.query_model(prompt)
        plan = self._parse_plan(reasoning)
        result = self._execute_plan(plan, task)
        evaluation = self.evaluate_outcome(result)
        self.feedback_loop({
            "task": task,
            "plan": plan,
            "result": result,
            "evaluation": evaluation,
        })
        self.logger.log({"event": "brain.process_task.end", "evaluation": evaluation})
        return {"result": result, "evaluation": evaluation}

    def route_to_agent(self, agent_type: str, task: Dict[str, Any]) -> Any:
        return self.router.dispatch({"agent": agent_type, "task": task})

    def evaluate_outcome(self, result: Any) -> Dict[str, Any]:
        score = 1.0 if result is not None else 0.0
        return {"success": score > 0.5, "score": score}

    def feedback_loop(self, memory_entry: Dict[str, Any]) -> None:
        self.memory.remember(memory_entry, metadata={"type": "brain_feedback"})
        self.memory.sync_to_disk()

    def _build_prompt(self, task: Dict[str, Any], context: Any) -> str:
        return f"Task: {task}\nContext: {context}\nProvide a step plan."

    def _parse_plan(self, response: LLMResponse) -> Dict[str, Any]:
        return {"steps": ["route", "execute", "summarize"], "raw": response.text}

    def _execute_plan(self, plan: Dict[str, Any], task: Dict[str, Any]) -> Any:
        agent = task.get("agent") or "general"
        return self.route_to_agent(agent, task)


__all__ = ["Brain"]

