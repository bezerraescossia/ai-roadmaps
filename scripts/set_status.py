#!/usr/bin/env python3
"""Change a roadmap entry's status (PATCH bump, Sync Impact Report updated). Idempotent.

Usage:
  set_status.py <roadmap.md> --number NNN --status specced [--spec-dir specs/NNN-x]
  set_status.py <roadmap.md> --spec-dir specs/NNN-x --auto
      --auto finds the entry by its `Spec dir:` pointer and sets `implemented` when <spec-dir>/tasks.md
      has no unchecked tasks, else `in-progress`.
Exit 2 when no entry matches (the caller then matches by title or asks, and retries with --number).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roadmap_md  # noqa: E402


def tasks_done(spec_dir: Path) -> bool:
    tasks = spec_dir / "tasks.md"
    if not tasks.is_file():
        return False
    text = tasks.read_text()
    return bool(re.search(r"^\s*- \[[xX]\]", text, re.M)) and not re.search(r"^\s*- \[ \]", text, re.M)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roadmap", type=Path)
    parser.add_argument("--number")
    parser.add_argument("--status")
    parser.add_argument("--spec-dir")
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()

    text = args.roadmap.read_text()
    number, status = args.number, args.status
    if args.auto:
        if not args.spec_dir:
            sys.exit("--auto needs --spec-dir")
        entry = roadmap_md.find_by_spec_dir(text.splitlines(), args.spec_dir)
        if entry is None:
            print(f"no roadmap entry has Spec dir {args.spec_dir}", file=sys.stderr)
            sys.exit(2)
        number = entry.number
        status = "implemented" if tasks_done(Path(args.spec_dir)) else "in-progress"
    if not (number and status):
        sys.exit("need --number and --status (or --auto with --spec-dir)")
    try:
        updated = roadmap_md.set_status(text, number, status, args.spec_dir)
    except ValueError as error:
        sys.exit(str(error))
    if updated == text:
        print(f"spec {number} already {status}; nothing to do")
    else:
        args.roadmap.write_text(updated)
        print(f"spec {number} → {status}")
