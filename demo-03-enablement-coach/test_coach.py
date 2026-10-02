"""Tests for Demo 03. Run: python3 test_coach.py"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from coach import score_answer, route, load_curriculum, run_session


def test_scoring():
    assert score_answer("Escalate to a human for any refund",
                        ["escalate", "human", "refund"]) == 3
    assert score_answer("escalate it", ["escalate", "human", "refund"]) == 1
    assert score_answer("", ["escalate"]) == 0


def test_routing():
    lessons = load_curriculum()
    assert route(lessons["L1"], True) == "L2"
    assert route(lessons["L1"], False) == "L1R"
    assert route(lessons["L2"], True) is None


def test_progress_stores_no_personal_data():
    answers = iter([
        "escalate to a human for refunds",
        "check the evidence behind each claim",
    ])
    run_session(read_input=lambda prompt: next(answers), write=lambda *a: None)
    stored = json.loads((HERE / "progress.json").read_text())
    blob = json.dumps(stored)
    assert "@" not in blob
    assert all(set(r) == {"lesson", "score", "of", "passed"}
               for r in stored["results"])


if __name__ == "__main__":
    test_scoring()
    test_routing()
    test_progress_stores_no_personal_data()
    print("demo-03 tests passed")
