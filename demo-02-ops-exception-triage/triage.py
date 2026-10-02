#!/usr/bin/env python3
"""Demo 02 - Ops Exception Triage (Pillar 2: Product and ops strategy).

Deterministic starter: classifies an ops incident, gathers runbook context,
proposes an action, and PAUSES before anything consequential. Nothing here
executes a real action; the approval gate is the point.

Run:
  python3 triage.py --list
  python3 triage.py INC-101
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
INCIDENTS = json.loads((HERE / "incidents.json").read_text())

RULES = [
    ({"outage", "failing", "down", "breach", "payment", "checkout"},
     "high", "payments"),
    ({"slow", "latency", "timeout", "degraded", "overload"},
     "medium", "performance"),
]

RUNBOOK = {
    "payments": "Runbook RB-7: confirm the error rate in the payments dashboard, "
                "check the processor status page, then page on-call before any customer notice.",
    "performance": "Runbook RB-3: capture a 5-minute trace, compare against last "
                   "week's baseline, then decide on scaling.",
    "cosmetic": "Runbook RB-1: batch non-urgent content fixes into the next scheduled deploy.",
}

ACTIONS = {
    "payments": "Page the on-call engineer and prepare a customer notice.",
    "performance": "Open a tracking ticket with the trace attached.",
    "cosmetic": "Queue the fix for the next content deploy.",
}


def classify(incident):
    text = (incident["title"] + " " + incident["description"]).lower()
    for keywords, severity, category in RULES:
        if any(k in text for k in keywords):
            return severity, category
    return "low", "cosmetic"


def triage(incident_id):
    incident = next((i for i in INCIDENTS if i["id"] == incident_id), None)
    if incident is None:
        return {"error": f"unknown incident {incident_id}"}
    severity, category = classify(incident)
    consequential = severity == "high"
    return {
        "incident_id": incident_id,
        "severity": severity,
        "category": category,
        "context": RUNBOOK[category],
        "proposed_action": ACTIONS[category],
        "consequential": consequential,
        "status": ("PAUSED - approval required"
                   if consequential else
                   "READY - proposal only, nothing executed"),
    }


def main(argv):
    if len(argv) < 2 or argv[1] == "--list":
        for i in INCIDENTS:
            print(f'{i["id"]}: {i["title"]}')
        return 0
    print(json.dumps(triage(argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
