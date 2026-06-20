#!/usr/bin/env python3
"""Append a local meditation practice check-in as JSONL."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_LOG_PATH = Path("data/practice-log.jsonl")


def append_entry(log_path, duration_min, practice_family, note, source_refs=None):
    log_path = Path(log_path)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "duration_min": int(duration_min),
        "practice_family": practice_family,
        "note": note,
        "source_refs": list(source_refs or []),
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", default=str(DEFAULT_LOG_PATH), help="Practice log JSONL path.")
    parser.add_argument("--duration-min", required=True, type=int, help="Practice duration in minutes.")
    parser.add_argument("--practice-family", required=True, help="Practice family, such as metta or energy-body.")
    parser.add_argument("--note", required=True, help="Short user or coach note.")
    parser.add_argument("--source-ref", action="append", default=[], help="Source path used for the practice.")
    args = parser.parse_args()

    entry = append_entry(
        log_path=Path(args.log),
        duration_min=args.duration_min,
        practice_family=args.practice_family,
        note=args.note,
        source_refs=args.source_ref,
    )
    print(json.dumps(entry, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
