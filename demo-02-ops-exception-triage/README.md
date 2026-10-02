# Demo 02 - Ops Exception Triage

**Consulting pillar:** Product and ops strategy
**Learning plan demo:** Demo 02 - Ops Exception Triage (classifies an incident, gathers context, proposes an action, pauses before consequential steps)

## What it is

A deterministic triage loop over the sample incidents in `incidents.json`:
classify by severity and category, pull the matching runbook context, propose
an action, and pause for approval when the action is consequential. High
severity incidents always stop at the gate; nothing executes on its own. This
is the strategy pillar's core story: the value is in the decision structure
and the risk boundary, not in autonomous action.

## Run it

```bash
python3 triage.py --list
python3 triage.py INC-101
python3 triage.py INC-103
python3 test_triage.py
```

INC-101 pauses for approval; INC-103 is a cosmetic proposal.

## Extend it toward a client-ready demo

- Replace keyword rules with a classifier and pull live context from the
  client's incident tool and runbooks.
- Add the approval record: who approved, what was shown, when it expires
  (the plan's Lab 4 interrupt pattern).
- Build the strategy-pillar assets around it: a use-case prioritization note,
  a risk and data map, and a value and cost model for the triage workflow.
