#!/usr/bin/env python3
"""Demo 03 - Enablement Coach (Pillar 3: AI training and enablement).

Deterministic starter: walks through a tiny curriculum, scores practice
answers against a rubric, adapts the path on misses, and reports progress.
Progress records lesson IDs and scores only - no personal data is stored.

Run:  python3 coach.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROGRESS_FILE = HERE / "progress.json"


def load_curriculum():
    data = json.loads((HERE / "curriculum.json").read_text())
    return {lesson["id"]: lesson for lesson in data["lessons"]}


def score_answer(answer, rubric):
    answer = answer.lower()
    return sum(1 for kw in rubric if kw.lower() in answer)


def route(lesson, passed):
    if passed:
        return lesson.get("next")
    return lesson.get("remediation")


def run_session(read_input=input, write=print):
    lessons = load_curriculum()
    current = "L1"
    results = []
    while current:
        lesson = lessons[current]
        write(f"\n== {lesson['title']} ==")
        for point in lesson["points"]:
            write(f"  - {point}")
        practice = lesson["practice"]
        answer = read_input(f"\nPractice: {practice['question']}\n> ")
        score = score_answer(answer, practice["rubric"])
        passed = score >= practice["pass"]
        results.append({
            "lesson": current,
            "score": score,
            "of": len(practice["rubric"]),
            "passed": passed,
        })
        if passed:
            write(f"Nice - {score}/{len(practice['rubric'])} rubric points. Moving on.")
        else:
            missed = [kw for kw in practice["rubric"] if kw.lower() not in answer.lower()]
            write(f"Got {score}/{len(practice['rubric'])}. "
                  f"Missed: {', '.join(missed)}. Let's reinforce that.")
        current = route(lesson, passed)
    write("\n== Progress report ==")
    for r in results:
        mark = "pass" if r["passed"] else "retry"
        write(f"  {r['lesson']}: {r['score']}/{r['of']} ({mark})")
    PROGRESS_FILE.write_text(json.dumps({"results": results}, indent=2))
    write("\nProgress saved to progress.json (lesson IDs and scores only).")
    return results


def main():
    run_session()
    return 0


if __name__ == "__main__":
    sys.exit(main())
