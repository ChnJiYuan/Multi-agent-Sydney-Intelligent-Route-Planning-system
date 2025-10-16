"""Traffic analysis agent for Sydney route planning."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import AgentContext, BaseAgent


class TrafficAgent(BaseAgent):
    """Summarises congestion along the proposed route."""

    name = "traffic-analyst"

    def run(self) -> Dict[str, Any]:
        request = self.context.request
        route: List[str] = request.get("candidate_route", [])
        segments = self.context.knowledge_base.get("traffic_segments", {})
        incidents = []
        total_delay = 0.0

        for start, end in zip(route, route[1:]):
            key = f"{start}->{end}"
            segment = segments.get(key)
            if not segment:
                continue
            if segment["status"] != "clear":
                incidents.append(
                    {
                        "segment": key,
                        "status": segment["status"],
                        "expected_delay_min": segment["expected_delay_min"],
                    }
                )
                total_delay += segment["expected_delay_min"]

        summary = {
            "incidents": incidents,
            "estimated_delay_min": round(total_delay, 1),
        }
        return {"traffic": summary}
