# Demo 03 - Enablement Coach

**Consulting pillar:** AI training and enablement
**Learning plan demo:** Demo 03 - Enablement Coach (uses a curriculum and rubric to teach a team, adapt practice, and report progress without storing unnecessary personal data)

## What it is

An interactive coaching session over the small curriculum in
`curriculum.json`. Each lesson teaches a few points, asks a practice question,
scores the answer against a rubric, and routes to remediation when the score
misses. At the end it writes `progress.json` containing only lesson IDs and
scores - no names, emails, or answer text. That data boundary is deliberate:
it is the enablement pillar's proof point on privacy.

## Run it

```bash
python3 coach.py
python3 test_coach.py
```

Answer the practice prompts in your own words; try missing a rubric point to
see the remediation path.

## Extend it toward a client-ready demo

- Put a model behind feedback generation while keeping the deterministic
  rubric as the scoring authority.
- Add before/after assessments and a team progress rollup (still no personal
  data beyond what the client consents to).
- Package the enablement-pillar assets: a lab guide, the rubric, and a safe
  adoption playbook for the client's team.
