#!/usr/bin/env python3
"""Print the next roadmap action as JSON: specify | resume | blocked | complete.

Usage: next.py <roadmap.md>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roadmap_md  # noqa: E402

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    if not path.is_file():
        sys.exit(f"{path}: roadmap not found")
    print(json.dumps(roadmap_md.next_action(path.read_text()), indent=2))
