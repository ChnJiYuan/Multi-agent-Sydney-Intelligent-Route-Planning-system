"""Command-line entry point for the Sydney Intelligent Route Planning demo."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .agents.base import AgentContext
from .agents.navigator_agent import NavigatorAgent
from .agents.traffic_agent import TrafficAgent
from .agents.weather_agent import WeatherAgent
from .orchestration.route_planner import RoutePlanner
from .tools.map_tool import MapTool

DATA_DIR = Path(__file__).parent / "data"
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def load_json(path: Path) -> Dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_planner(request: Dict[str, object]) -> RoutePlanner:
    graph_data = load_json(DATA_DIR / "inner_sydney_graph.json")
    traffic_data = load_json(KNOWLEDGE_DIR / "traffic_segments.json")
    weather_data = load_json(KNOWLEDGE_DIR / "weather_forecast.json")

    map_tool = MapTool.from_dataset(graph_data)

    context = AgentContext(
        request=request,
        knowledge_base={
            "traffic_segments": traffic_data,
            "weather_forecast": weather_data,
        },
    )

    navigator = NavigatorAgent(context, map_tool)
    traffic = TrafficAgent(context)
    weather = WeatherAgent(context)

    planner = RoutePlanner(agents=[navigator, traffic, weather], context=context)
    return planner


def demo() -> Dict[str, object]:
    """Run the planner with a sample request."""

    request = {
        "origin": "CBD",
        "destination": "Sydney Airport",
        "preferences": {"avoid_tolls": True},
    }
    planner = build_planner(request)
    return planner.run()


if __name__ == "__main__":
    results = demo()
    print(json.dumps(results, indent=2, ensure_ascii=False))
