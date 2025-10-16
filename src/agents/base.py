"""Base classes and utilities for route-planning agents."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AgentContext:
    """Shared state for agent collaboration."""

    request: Dict[str, Any]
    knowledge_base: Dict[str, Any]


class BaseAgent:
    """A simple base class all agents inherit from."""

    name: str = "base-agent"

    def __init__(self, context: AgentContext) -> None:
        self.context = context

    def run(self) -> Dict[str, Any]:
        """Execute the agent and return its contribution."""
        raise NotImplementedError
