"""Navigator agent that proposes a route across Sydney suburbs."""
from __future__ import annotations

from typing import Dict, List

from .base import AgentContext, BaseAgent
from ..tools.map_tool import MapTool


class NavigatorAgent(BaseAgent):
    """Uses the MapTool to create candidate routes between two suburbs."""

    name = "navigator"

    def __init__(self, context: AgentContext, map_tool: MapTool) -> None:
        super().__init__(context)
        self._map_tool = map_tool

    def run(self) -> Dict[str, List[str]]:
        request = self.context.request
        origin = request["origin"]
        destination = request["destination"]
        preferences = request.get("preferences", {})

        candidate_route = self._map_tool.shortest_path(
            origin, destination, avoid_tolls=preferences.get("avoid_tolls", False)
        )
        self.context.request["candidate_route"] = candidate_route
        return {"candidate_route": candidate_route}
