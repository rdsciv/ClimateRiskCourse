#!/usr/bin/env python3
"""Print the course exercise map."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_manifest import SECTIONS


def main() -> None:
    for section in SECTIONS:
        week = section["week"]
        label = "Orientation" if week == 0 else f"Week {week}"
        print(f"\n## {section['id']} — {section['title']} ({label})")
        print(f"Q: {section['question']}")
        print(f"Deliverable: {section['deliverable']}")
        for ex in section["exercises"]:
            variants = ", ".join(ex["variants"])
            print(f"  {ex['id']}  [{variants}]  {ex['title']}")


if __name__ == "__main__":
    main()
