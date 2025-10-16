# Sydney Intelligent Route Planning (Multi-agent)

This repository contains a lightweight, self-contained multi-agent demo inspired by [ai-agents-for-beginners](https://github.com/ChnJiYuan/ai-agents-for-beginners). The scenario is tailored for Sydney and demonstrates how multiple specialised agents can collaborate to produce an intelligent travel recommendation.

## Project structure

```
.
├── src
│   ├── agents          # Navigator, traffic, and weather specialists
│   ├── data            # Static inner-Sydney transport network
│   ├── knowledge       # Traffic and weather snapshots
│   ├── orchestration   # Route planner that coordinates agents
│   └── main.py         # Command-line entry point
├── tests               # Pytest-based unit tests
└── requirements.txt
```

## Scenario overview

* **Navigator Agent** computes a candidate path between two suburbs using a simplified graph of Sydney.
* **Traffic Agent** inspects each segment for congestion or incidents.
* **Weather Agent** raises cautions for stops with heavy rain or storms.
* **Route Planner** orchestrates the agents and assembles a human-readable summary.

The included dataset focuses on key inner-Sydney suburbs and corridors (CBD, Surry Hills, Alexandria, Mascot, Sydney Airport, etc.).

## Getting started

Create and activate a virtual environment (optional) and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the demonstration script:

```bash
python -m src.main
```

Example output:

```json
{
  "candidate_route": [
    "CBD",
    "Surry Hills",
    "Redfern",
    "Alexandria",
    "Mascot",
    "Sydney Airport"
  ],
  "traffic": {
    "incidents": [
      {
        "segment": "Redfern->Alexandria",
        "status": "busy",
        "expected_delay_min": 3.5
      },
      {
        "segment": "Alexandria->Mascot",
        "status": "incident",
        "expected_delay_min": 7.0
      }
    ],
    "estimated_delay_min": 10.5
  },
  "weather": [
    {
      "location": "Alexandria",
      "condition": "Rain",
      "advice": "Expect wet roads, reduce speed."
    },
    {
      "location": "Mascot",
      "condition": "Storm",
      "advice": "Delay travel if possible."
    },
    {
      "location": "Sydney Airport",
      "condition": "Rain",
      "advice": "Allow extra time for check-in."
    }
  ],
  "summary": "Sydney Intelligent Route Planning Report Proposed route: CBD -> Surry Hills -> Redfern -> Alexandria -> Mascot -> Sydney Airport. Traffic alerts: Redfern->Alexandria (busy, +3.5 min); Alexandria->Mascot (incident, +7.0 min). Estimated extra delay: 10.5 minutes. Weather cautions: Alexandria Rain - Expect wet roads, reduce speed; Mascot Storm - Delay travel if possible; Sydney Airport Rain - Allow extra time for check-in."
}
```

## Testing

Execute the automated tests with:

```bash
pytest
```

## Extending the demo

The orchestration layer is intentionally simple to keep the code approachable. To extend the project you can:

* Enrich the map data with more suburbs and edges.
* Add new agents (e.g., event planner, public transport recommender).
* Replace the static knowledge base with live feeds or API calls.
* Integrate a UI and visualise the routes on a map of Sydney.
