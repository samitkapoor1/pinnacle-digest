#!/usr/bin/env python3
"""
Create a blank edition skeleton for a given date.

  python3 scripts/new_edition.py 2026-09-03

Writes content/2026-09-03.json with the schema stubbed out, ready to be
filled from that day's Daily Accountancy Briefing. Refuses to overwrite an
existing file.
"""
import json
import os
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 scripts/new_edition.py YYYY-MM-DD")
    date = sys.argv[1]
    datetime.strptime(date, "%Y-%m-%d")  # validate
    path = os.path.join(ROOT, "content", date + ".json")
    if os.path.exists(path):
        raise SystemExit(f"{path} already exists; not overwriting.")
    skeleton = {
        "date": date,
        "masthead": "Daily Accountancy Briefing",
        "title": "The day's own headline goes here",
        "kicker": "the",
        "region": "UK & Ireland",
        "summary": "One-line summary of the day's briefing.",
        "categories": [
            {
                "name": "Category name",
                "badge": None,
                "stories": [
                    {
                        "headline": "Story headline",
                        "tags": ["Key stat", "Key fact"],
                        "body": ["First paragraph.", "Second paragraph."],
                        "meaning": "Optional 'What this means for firms' takeaway.",
                        "source": "Source name",
                        "charts": []
                    }
                ]
            }
        ]
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(skeleton, fh, ensure_ascii=False, indent=2)
    print("Created", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
