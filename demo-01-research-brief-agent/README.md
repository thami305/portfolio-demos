# Demo 01 - Research Brief Agent

**Consulting pillar:** Agentic AI implementation
**Learning plan demo:** Demo 01 - Research Brief Agent (finds evidence, records provenance, produces a structured brief, refuses unsupported claims)

## What it is

A small deterministic agent loop: it takes a business question, searches a
curated packet of documents in `docs/`, and returns a structured brief where
every claim points back to the passage it came from. If the packet has no
supporting evidence, it refuses instead of guessing. No model calls, no
credentials, no network - the retrieval and refusal logic is plain code so the
control structure is visible.

## Run it

```bash
python3 brief_agent.py "What is our SLA for critical incidents?"
python3 brief_agent.py "What is the refund policy for llamas?"
python3 test_brief_agent.py
```

The first question returns cited claims; the second is refused.

## Extend it toward a client-ready demo

- Swap the keyword search for real retrieval (chunking, embeddings, reranking)
  and put a model behind claim extraction, keeping the claim-to-evidence map.
- Add the plan's Lab 2 comparison: prompt-only answer versus tool-using answer
  on the same question set, scored for groundedness.
- Grow `docs/` into a versioned corpus and add the refusal cases to a golden
  eval set (Lab 9).
