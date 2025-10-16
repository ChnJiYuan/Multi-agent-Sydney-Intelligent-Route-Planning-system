"""Unit tests for the Sydney Intelligent Route Planner."""
from __future__ import annotations

from src.main import build_planner


def load_request(name: str) -> dict:
    if name == "airport":
        return {
            "origin": "CBD",
            "destination": "Sydney Airport",
            "preferences": {"avoid_tolls": True},
        }
    raise ValueError(f"Unknown request fixture: {name}")


def test_route_planner_generates_summary(tmp_path):
    request = load_request("airport")
    planner = build_planner(request)
    result = planner.run()

    assert result["candidate_route"][:2] == ["CBD", "Surry Hills"]
    assert "summary" in result
    assert "Sydney Intelligent Route Planning Report" in result["summary"]
    assert any(
        incident["segment"] == "Alexandria->Mascot" for incident in result["traffic"]["incidents"]
    )
    assert any(item["location"] == "Mascot" for item in result["weather"])
