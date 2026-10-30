# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Order the epics of one archetype into numbered specs, one spec per epic.

Usage:
  uv run scripts/plan.py --list
  uv run scripts/plan.py --archetype traditional-ml --answers '{"serving": "online"}' [--drop E5 ...]
      [--weights '{"E3": 6}'] [--start 2026-11-02]

An archetype lives in `archetypes/<slug>/`: `archetype.md` (frontmatter, an `intake` yaml block) and its epic
files `E*.md` (frontmatter: id, title, phase, depends_on, weight, loops_back_to). Every epic is always in the
roadmap. Intake answers tailor the items inside the epics and never include or exclude one, so they are
only echoed back. `loops_back_to` is informational and never orders or blocks anything.

Each epic has a relative `weight` (default 1; proportional, not an estimate) that sizes its bar in the
Mermaid Gantt chart. The chart is drawn from `depends_on`, one bar after another. Without `--start` it uses a
placeholder start and its axis counts relative days; with `--start` it uses real dates.

Prints JSON: the epics, numbered specs in dependency order, conflicts (a dropped epic that another needs),
and `gantt` (Mermaid source) with `loop_backs` (the edges a Gantt cannot draw).
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ARCHETYPES = ROOT / "archetypes"
FENCE = re.compile(r"```yaml\n(.*?)```", re.S)


def frontmatter(path: Path) -> dict:
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        sys.exit(f"{path}: missing frontmatter")
    return yaml.safe_load(match.group(1))


def list_archetypes() -> list[dict]:
    return [{"archetype": meta["archetype"], "title": meta["title"], "description": meta["description"]}
            for meta in (frontmatter(p) for p in sorted(ARCHETYPES.glob("*/archetype.md")))]


def load_archetype(name: str) -> dict:
    path = ARCHETYPES / name / "archetype.md"
    if not path.is_file():
        sys.exit(f"unknown archetype {name!r}")
    meta = frontmatter(path)
    for block in FENCE.findall(path.read_text()):
        meta.update(yaml.safe_load(block))
    return meta


def load_epics(name: str) -> dict:
    """The epics of an archetype by id; `loops_back_to` defaults to none."""
    epics = {}
    for path in sorted((ARCHETYPES / name).glob("E*.md")):
        meta = frontmatter(path)
        if meta["id"] in epics:
            sys.exit(f"{name}: {path.name} repeats {meta['id']}")
        meta.setdefault("depends_on", [])
        meta.setdefault("loops_back_to", [])
        meta.setdefault("weight", 1)
        meta["file"] = path.name
        epics[meta["id"]] = meta
    for epic in epics.values():
        for ref in epic["depends_on"] + epic["loops_back_to"]:
            if ref not in epics:
                sys.exit(f"{name}: {epic['id']} references unknown epic {ref}")
    return epics


def gantt(arch: dict, epics: dict, ordered: list[str], weights: dict, start: str | None) -> str:
    """Mermaid gantt source: each epic starts when the epics it depends on end."""
    lines = ["gantt", f"    title {arch['title']} ({arch['methodology']})", "    dateFormat YYYY-MM-DD"]
    lines.append("    axisFormat %b %d" if start else "    axisFormat Day %j")
    lines.append("    section Phases")
    for eid in ordered:
        deps = [d.lower() for d in epics[eid]["depends_on"] if d in ordered]
        begin = f"after {' '.join(deps)}" if deps else (start or "2000-01-01")
        label = f"{eid} {epics[eid]['title']}".replace(":", " ")
        lines.append(f"    {label} :{eid.lower()}, {begin}, {weights.get(eid, epics[eid]['weight'])}d")
    return "\n".join(lines)


def plan(archetype: str, answers: dict, dropped: set[str], weights: dict | None = None,
         start: str | None = None) -> dict:
    weights = weights or {}
    arch = load_archetype(archetype)
    epics = load_epics(archetype)
    unknown = dropped - set(epics)
    if unknown:
        sys.exit(f"{archetype}: cannot drop unknown epic(s) {sorted(unknown)}")
    status = {eid: "dropped" if eid in dropped else "planned" for eid in epics}

    conflicts = [{"epic": eid, "needs": dep, "dep_state": "dropped"}
                 for eid, epic in epics.items() if status[eid] != "dropped"
                 for dep in epic["depends_on"] if status[dep] == "dropped"]

    ordered, placed = [], set()
    pending = sorted(e for e in epics if status[e] != "dropped")
    while pending:
        ready = [e for e in pending if {d for d in epics[e]["depends_on"] if status[d] != "dropped"} <= placed]
        if not ready:
            sys.exit("dependency cycle among: " + ", ".join(pending))
        ordered.append(ready[0])
        placed.add(ready[0])
        pending.remove(ready[0])

    number = {eid: f"{i:03d}" for i, eid in enumerate(ordered, 1)}
    specs = [{"number": number[eid], "title": epics[eid]["title"], "members": [eid], "archetype": archetype,
              "status": "planned", "phase": epics[eid]["phase"],
              "depends_on": [number[d] for d in epics[eid]["depends_on"] if d in number],
              "loops_back_to": [number[d] for d in epics[eid]["loops_back_to"] if d in number]}
             for eid in ordered]
    loop_backs = [{"epic": eid, "loops_back_to": [d for d in epics[eid]["loops_back_to"] if d in number]}
                  for eid in ordered if epics[eid]["loops_back_to"]]
    return {"archetype": archetype, "library_version": arch["library_version"], "answers": answers,
            "epics": status, "specs": specs, "conflicts": conflicts,
            "gantt": gantt(arch, epics, ordered, weights, start), "loop_backs": loop_backs}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="list the available archetypes")
    parser.add_argument("--archetype", default="traditional-ml")
    parser.add_argument("--answers", default="{}", help="JSON object of intake answers")
    parser.add_argument("--weights", default="{}", help="JSON object of epic id to relative weight overrides")
    parser.add_argument("--start", help="project start date YYYY-MM-DD; omit for a relative axis")
    parser.add_argument("--drop", nargs="*", default=[], help="epic ids the user chose to drop")
    args = parser.parse_args()
    if args.list:
        print(json.dumps(list_archetypes(), indent=2))
    else:
        print(json.dumps(plan(args.archetype, json.loads(args.answers), set(args.drop),
                         json.loads(args.weights), args.start), indent=2))
