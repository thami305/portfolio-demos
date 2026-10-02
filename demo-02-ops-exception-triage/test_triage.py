"""Tests for Demo 02. Run: python3 test_triage.py"""

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from triage import triage


def test_high_severity_pauses_for_approval():
    result = triage("INC-101")
    assert result["severity"] == "high"
    assert result["category"] == "payments"
    assert result["consequential"] is True
    assert result["status"].startswith("PAUSED")


def test_medium_severity_proposes_without_pause():
    result = triage("INC-102")
    assert result["severity"] == "medium"
    assert result["consequential"] is False


def test_low_severity_is_cosmetic():
    result = triage("INC-103")
    assert result["severity"] == "low"
    assert result["category"] == "cosmetic"


def test_unknown_incident_errors():
    assert "error" in triage("INC-999")


if __name__ == "__main__":
    test_high_severity_pauses_for_approval()
    test_medium_severity_proposes_without_pause()
    test_low_severity_is_cosmetic()
    test_unknown_incident_errors()
    print("demo-02 tests passed")
