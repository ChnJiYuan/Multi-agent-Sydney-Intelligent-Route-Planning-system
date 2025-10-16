"""Simplified map utilities for inner Sydney suburbs."""
from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Tuple

Graph = Dict[str, Dict[str, Dict[str, float]]]


class MapTool:
    """Provides routing capability over a static graph."""

    def __init__(self, graph: Graph) -> None:
        self._graph = graph

    @classmethod
    def from_dataset(cls, dataset: Dict[str, Iterable[Tuple[str, Dict[str, float]]]]) -> "MapTool":
        graph: Graph = {
            node: {neighbor: attributes for neighbor, attributes in edges}
            for node, edges in dataset.items()
        }
        return cls(graph)

    def shortest_path(self, origin: str, destination: str, *, avoid_tolls: bool = False) -> List[str]:
        """Return the shortest path using a BFS variant."""

        if origin not in self._graph:
            raise ValueError(f"Unknown origin suburb: {origin}")
        if destination not in self._graph:
            raise ValueError(f"Unknown destination suburb: {destination}")

        def neighbors(node: str) -> Iterable[str]:
            edges = self._graph.get(node, {})
            for neighbor, attributes in edges.items():
                if avoid_tolls and attributes.get("toll", False):
                    continue
                yield neighbor

        queue: deque[Tuple[str, List[str]]] = deque([(origin, [origin])])
        visited = {origin}

        while queue:
            node, path = queue.popleft()
            if node == destination:
                return path
            for neighbor in neighbors(node):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
        raise ValueError(f"No route found from {origin} to {destination}")
