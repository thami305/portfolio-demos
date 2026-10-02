"""Tests for Demo 01. Run: python3 test_brief_agent.py"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from brief_agent import build_brief


def test_supported_question_returns_cited_claims():
    brief = build_brief("What is the response time for critical incidents?")
    assert brief["refused"] is False
    assert brief["claims"], "expected at least one claim"
    for claim in brief["claims"]:
        assert claim["sources"], "every claim must carry provenance"


def test_unsupported_question_is_refused():
    brief = build_brief("What is the refund policy for llamas?")
    assert brief["refused"] is True
    assert brief["claims"] == []


if __name__ == "__main__":
    test_supported_question_returns_cited_claims()
    test_unsupported_question_is_refused()
    print("demo-01 tests passed")
