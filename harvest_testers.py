#!/usr/bin/env python3
"""
harvest_testers.py
Pulls alpha tester signups from BetterStack and prints a CSV.

Usage:
    export BETTERSTACK_TOKEN=your_source_token
    python harvest_testers.py
    python harvest_testers.py --output testers.csv
"""

import os
import sys
import json
import argparse
import csv
import urllib.request
from datetime import datetime, timezone

QUERY_URL = "https://telemetry.betterstack.com/api/v1/query"

def fetch_signups(token: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "query": 'message="alpha_tester_signup"',
        "limit": 1000,
    })
    req = urllib.request.Request(
        f"{QUERY_URL}?{params}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    rows = []
    for entry in data.get("data", []):
        j = entry.get("json", {})
        rows.append({
            "first_name":   j.get("first_name", ""),
            "last_name":    j.get("last_name", ""),
            "email":        j.get("email", ""),
            "submitted_at": j.get("submitted_at", ""),
        })

    # Sort newest first
    rows.sort(key=lambda r: r["submitted_at"], reverse=True)
    return rows


def main():
    import urllib.parse  # noqa: PLC0415

    parser = argparse.ArgumentParser(description="Harvest alpha tester signups from BetterStack")
    parser.add_argument("--output", "-o", help="CSV output file (default: stdout)")
    args = parser.parse_args()

    token = os.environ.get("BETTERSTACK_TOKEN")
    if not token:
        print("Error: BETTERSTACK_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)

    rows = fetch_signups(token)
    print(f"Found {len(rows)} signup(s).", file=sys.stderr)

    fields = ["first_name", "last_name", "email", "submitted_at"]

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
