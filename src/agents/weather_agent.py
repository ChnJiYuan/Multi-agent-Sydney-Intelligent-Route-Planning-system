"""Weather agent for Sydney route planning."""
from __future__ import annotations

from typing import Dict, List

from .base import AgentContext, BaseAgent


class WeatherAgent(BaseAgent):
    """Provides weather cautions for each stop in the route."""

    name = "weather-specialist"

    def run(self) -> Dict[str, List[Dict[str, str]]]:
        route = self.context.request.get("candidate_route", [])
        forecast = self.context.knowledge_base.get("weather_forecast", {})

        advisories = []
        for stop in route:
            stop_weather = forecast.get(stop)
            if not stop_weather:
                continue
            if stop_weather["condition"].lower() in {"rain", "storm"}:
                advisories.append(
                    {
                        "location": stop,
                        "condition": stop_weather["condition"],
                        "advice": stop_weather["advice"],
                    }
                )

        return {"weather": advisories}
