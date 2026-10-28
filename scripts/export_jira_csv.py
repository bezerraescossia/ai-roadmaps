#!/usr/bin/env python3
"""Export a speckit-format roadmap.md to a Jira import CSV.

Usage: export_jira_csv.py <roadmap.md> [-o out.csv]

Epic  = each "### NNN — Title  [status: x]" entry under Planned Specs.
Story = each nested bullet under that entry's "Scope (in)" (or the whole text when it has none).
Story = each open question "Qn — ..." under Open Questions, labelled `decision`; the question is
        attached to a spec when its text contains "(spec NNN)", otherwise it has no parent.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import roadmap_md  # noqa: E402

COLUMNS = ["Issue ID", "Issue Type", "Summary", "Description", "Parent", "Labels"]


def stories(entry: roadmap_md.Entry) -> list[str]:
    raw = entry.fields.get("Scope (in)", [])
    nested = [re.sub(r"^\s*[-*]\s+", "", ln).strip() for ln in raw if re.match(r"^\s+[-*]\s+", ln)]
    if nested:
        return nested
    text = " ".join(ln.strip() for ln in raw).strip()
    return [text] if text else []


def rows(path: Path) -> list[list[str]]:
    lines = path.read_text().splitlines()
    specs = roadmap_md.parse_entries(lines)
    if not specs:
        sys.exit(f"{path}: no Planned Specs entries found")
    out = []
    for spec in specs:
        eid = f"E{spec.number}"
        out.append([eid, "Epic", spec.title, spec.text("Description"), "", spec.status])
        for n, story in enumerate(stories(spec), 1):
            out.append([f"{eid}-S{n:02d}", "Story", story[:200], story, eid, spec.status])
    for qid, text in roadmap_md.parse_questions(lines):
        owner = re.search(r"\(spec (\d{3})\)", text)
        out.append([f"{qid}", "Story", re.sub(r"\s*\(spec \d{3}\)", "", text)[:200], text,
                    f"E{owner[1]}" if owner else "", "decision"])
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("roadmap", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    target = args.output or args.roadmap.with_name("roadmap-jira.csv")
    with target.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COLUMNS)
        writer.writerows(rows(args.roadmap))
    print(f"wrote {target}")
