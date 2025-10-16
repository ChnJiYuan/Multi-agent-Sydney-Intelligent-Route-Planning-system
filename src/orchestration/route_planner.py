"""Simple multi-agent orchestrator for Sydney route planning."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence

from ..agents.base import AgentContext, BaseAgent


@dataclass
class AgentResult:
    name: str
    payload: Dict[str, object]


@dataclass
class RoutePlanner:
    """Coordinates multiple agents to build a travel recommendation."""

    agents: Sequence[BaseAgent]
    context: AgentContext
    history: List[AgentResult] = field(default_factory=list)

    def run(self) -> Dict[str, object]:
        combined: Dict[str, object] = {}
        for agent in self.agents:
            result = agent.run()
            self.history.append(AgentResult(name=agent.name, payload=result))
            combined.update(result)
        combined["summary"] = self._build_summary(combined)
        return combined

    def _build_summary(self, combined: Dict[str, object]) -> str:
        route = combined.get("candidate_route", [])
        traffic = combined.get("traffic", {})
        weather = combined.get("weather", [])

        parts = [
            "Sydney Intelligent Route Planning Report",
            f"Proposed route: {' -> '.join(route) if route else 'N/A'}.",
        ]

        incidents = traffic.get("incidents", []) if isinstance(traffic, dict) else []
        if incidents:
            traffic_text = "; ".join(
                f"{item['segment']} ({item['status']}, +{item['expected_delay_min']} min)"
                for item in incidents
            )
            if not traffic_text.endswith("."):
                traffic_text += "."
            parts.append("Traffic alerts: " + traffic_text)
            parts.append(
                f"Estimated extra delay: {traffic.get('estimated_delay_min', 0)} minutes."
            )
        else:
            parts.append("Traffic conditions are clear on all segments.")

        if weather:
            weather_text = "; ".join(
                f"{item['location']} {item['condition']} - {item['advice'].rstrip('.')}"
                for item in weather
            )
            if not weather_text.endswith("."):
                weather_text += "."
            parts.append("Weather cautions: " + weather_text)
        else:
            parts.append("No severe weather expected along the route.")

        return " ".join(parts)
