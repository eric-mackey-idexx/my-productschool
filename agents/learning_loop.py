#!/usr/bin/env python3
"""
Learning Loop — mechanical half

Parses agents/outcome-log.md and splits its logged diagnoses into
"scoreable" (the top-ranked hypothesis has a real, filled-in "what
actually happened" note) and "pending" (still the placeholder text).

This script does NOT score hit/miss/partial itself — that's a semantic
judgment (does hypothesis text X match outcome text Y), which belongs to
whoever/whatever is running the weekly review (see agents/learning-loop.md),
not to a string-matching script pretending to have judgment it doesn't.
This script's only job is the mechanical part: find what's actually
scoreable so the reviewer doesn't have to hand-parse markdown every week.

Usage:
    python3 learning_loop.py [--log agents/outcome-log.md]
"""

import argparse
import os
import re
import sys

PLACEHOLDER = "_placeholder — fill in after investigating_"


def parse_outcome_log(path):
    with open(path) as f:
        content = f.read()

    entries = []
    blocks = content.split("\n## ")[1:]
    for block in blocks:
        lines = block.strip().split("\n")
        header = lines[0].strip()
        m = re.match(r"(\S+) — (.+)", header)
        date, description = (m.group(1), m.group(2)) if m else (None, header)

        stopped_at = None
        rows = []
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("**Loop"):
                stopped_at = line.strip("*").strip()
            elif line.startswith("|") and "Rank" not in line and not line.startswith("|---"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 4 and cells[0].isdigit():
                    rows.append({
                        "rank": int(cells[0]), "hypothesis": cells[1],
                        "confidence": cells[2], "outcome": cells[3],
                    })
        entries.append({"date": date, "description": description, "stopped_at": stopped_at, "rows": rows})
    return entries


def classify(entries):
    scoreable, pending, no_hypothesis = [], [], []
    for e in entries:
        top = next((r for r in e["rows"] if r["rank"] == 1), None)
        if top is None:
            no_hypothesis.append(e)  # e.g. stopped at Step 1, no hypotheses generated at all
        elif top["outcome"] == PLACEHOLDER or not top["outcome"]:
            pending.append(e)
        else:
            scoreable.append(e)
    return scoreable, pending, no_hypothesis


def main():
    parser = argparse.ArgumentParser(description="Mechanical split of outcome-log.md for the weekly learning-loop review.")
    parser.add_argument("--log", default=os.path.join(os.path.dirname(__file__), "outcome-log.md"))
    args = parser.parse_args()

    entries = parse_outcome_log(args.log)
    scoreable, pending, no_hypothesis = classify(entries)

    print(f"Total logged diagnosis checks: {len(entries)}")
    print(f"  Scoreable (outcome filled in):     {len(scoreable)}")
    print(f"  Pending (still placeholder):       {len(pending)}")
    print(f"  No hypothesis generated (Step 1/2 stop): {len(no_hypothesis)}")
    print()

    if scoreable:
        print("=== SCOREABLE ENTRIES (needs semantic hit/miss/partial judgment) ===")
        for e in scoreable:
            top = next(r for r in e["rows"] if r["rank"] == 1)
            print(f"- {e['date']} | {e['description']}")
            print(f"    Top hypothesis: {top['hypothesis']}")
            print(f"    What happened:  {top['outcome']}")
    else:
        print("Nothing scoreable yet — every logged diagnosis still has a placeholder outcome, "
              "or stopped before generating a hypothesis. No heuristic update can be responsibly "
              "proposed from zero confirmed outcomes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
