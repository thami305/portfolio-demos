#!/usr/bin/env python3
"""Demo 01 - Research Brief Agent (Pillar 1: Agentic AI implementation).

Deterministic starter: takes a business question, searches a small curated
packet of documents, and returns a structured brief with claim-to-evidence
mapping. Refuses when the packet does not support an answer.

Run:  python3 brief_agent.py "What is our SLA for critical incidents?"
"""

import json
import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs"
MIN_OVERLAP = 2  # minimum shared content words for a passage to count

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "and", "or", "for", "in", "on", "at", "by", "with",
    "what", "which", "who", "whom", "how", "when", "where", "why",
    "does", "do", "did", "has", "have", "had", "it", "its", "our",
    "we", "you", "your", "i", "my", "this", "that", "these", "those",
    "as", "from", "into", "per", "up", "out", "about",
}


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def load_passages():
    passages = []
    for doc in sorted(DOCS_DIR.glob("*.md")):
        doc_id = doc.stem.upper().replace("-", "_")
        body = doc.read_text()
        paras = [p.strip() for p in body.split("\n\n") if p.strip()]
        for i, para in enumerate(paras, start=1):
            passages.append({
                "id": f"{doc_id}#P{i}",
                "doc_id": doc_id,
                "text": para,
                "words": set(tokens(para)),
            })
    return passages


def search(question, passages, top_k=3):
    qwords = set(tokens(question))
    scored = []
    for p in passages:
        overlap = qwords & p["words"]
        if len(overlap) >= MIN_OVERLAP:
            scored.append((len(overlap), p))
    scored.sort(key=lambda s: s[0], reverse=True)
    return [p for _, p in scored[:top_k]]


def build_brief(question):
    passages = load_passages()
    hits = search(question, passages)
    if not hits:
        return {
            "question": question,
            "refused": True,
            "reason": "The document packet contains no evidence addressing this question.",
            "claims": [],
            "assumptions": [],
            "open_questions": [question],
        }
    claims = [{"text": h["text"][:280], "sources": [h["id"]]} for h in hits]
    return {
        "question": question,
        "refused": False,
        "claims": claims,
        "assumptions": ["The curated packet is complete and current for this question."],
        "open_questions": [],
    }


def main(argv):
    if len(argv) < 2:
        print('Usage: python3 brief_agent.py "your business question"')
        return 2
    print(json.dumps(build_brief(" ".join(argv[1:])), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
