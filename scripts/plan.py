# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Select epics from intake answers and order the bundles of one or more archetypes.

Usage:
  uv run scripts/plan.py --archetype llm-service --answers '{"rag": "yes"}' [--drop E14 ...]
  uv run scripts/plan.py --archetype llm-service --answers '{...}' \
      --include '{"classical-ml": {"serving": "online"}}' \
      --profile production --strike canary-release --add mcp

`--profile` (prototype, production or critical) sets which optional capabilities are on by default: an epic's
scope bullets tagged `[cap: <id>, tier: <tier>]` are included when the profile reaches their tier. `--strike`
turns capabilities off and `--add` turns them on.

`--include` adds archetypes the primary one declares under `includes` (a project that also builds, say, a
classical-ML model). Their intake answers are kept apart, so the same variable name can mean different
things in different archetypes. Epics shared by several archetypes appear once: an epic is selected when
any archetype selects it, and its `depends_on` and `after` are the union across archetypes.

Prints JSON: selected epics, numbered specs (bundles) in dependency order, and conflicts.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"```yaml\n(.*?)```", re.S)
STRENGTH = {"planned": 2, "undecided": 1}
PROFILES = ["prototype", "production", "critical"]
CAP = re.compile(r"^- \[cap: ([\w-]+), tier: (production|critical)\] (.*)$")


def frontmatter(path: Path) -> dict:
    text = path.read_text()
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        sys.exit(f"{path}: missing frontmatter")
    return yaml.safe_load(match.group(1))


def load_archetype(name: str) -> dict:
    path = ROOT / "archetypes" / f"{name}.md"
    if not path.is_file():
        sys.exit(f"unknown archetype {name!r}")
    meta = frontmatter(path)
    for block in FENCE.findall(path.read_text()):
        meta.update(yaml.safe_load(block))
    return meta


def load_epics(archetype: str, rules: dict) -> dict:
    """Epics of this archetype, with the archetype's `epic_rules` overrides merged in."""
    epics = {}
    for path in sorted((ROOT / "epics").glob("E*.md")):
        meta = frontmatter(path)
        if archetype in meta.get("archetypes", []):
            meta["file"] = path.name
            meta.update(rules.get(meta["id"], {}))
            epics[meta["id"]] = meta
    unknown = set(rules) - set(epics)
    if unknown:
        sys.exit(f"{archetype}: epic_rules for epics outside the archetype: {sorted(unknown)}")
    return epics


def applies(epic: dict, answers: dict) -> str | None:
    """Return 'planned', 'undecided' or None (not selected)."""
    rule = str(epic.get("applies_when", "always")).strip()
    if rule == "always":
        return "planned"
    match = re.fullmatch(r"(\w+)\s*(==|!=)\s*(\w+)", rule)
    if not match:
        sys.exit(f"{epic['id']}: unsupported applies_when {rule!r}")
    var, op, want = match.groups()
    got = answers.get(var, "no")
    if got == "unsure":
        return "undecided"
    return "planned" if (got == want) == (op == "==") else None


def capabilities_of(epic: dict) -> list[dict]:
    """Optional capabilities tagged in the epic's Scope (in): [{id, tier, text}, ...]."""
    text = (ROOT / "epics" / epic["file"]).read_text()
    scope = re.search(r"## Scope \(in\)\n\n(.*?)(?=\n## )", text, re.S)
    caps, current = [], None
    for line in (scope.group(1) if scope else "").splitlines():
        tagged = CAP.match(line)
        if tagged:
            current = {"id": tagged[1], "tier": tagged[2], "text": tagged[3]}
            caps.append(current)
        elif line.startswith("- "):
            current = None
        elif current and line.strip():
            current["text"] += " " + line.strip()
    return caps


def merge_archetypes(archetype: str, answers: dict, includes: dict) -> tuple[dict, dict, dict]:
    """Combine the primary archetype with its included ones.

    Returns (epics, status, arches): merged epic definitions, the per-epic status ('planned' or
    'undecided', best across archetypes), and the loaded archetype files.
    """
    primary = load_archetype(archetype)
    declared = primary.get("includes", {})
    for name in includes:
        if name not in declared:
            sys.exit(f"{archetype} does not declare {name!r} under `includes` "
                     f"(declared: {sorted(declared) or 'none'})")
    order = [(archetype, answers)] + list(includes.items())
    arches = {name: load_archetype(name) for name, _ in order}
    per = {name: load_epics(name, arches[name].get("epic_rules", {})) for name, _ in order}

    epics, status = {}, {}
    for name, ans in order:
        for eid, epic in per[name].items():
            if eid not in epics:
                epics[eid] = dict(epic, depends_on=list(epic.get("depends_on", [])),
                                  after=list(epic.get("after", [])), origins=[name])
            else:
                merged = epics[eid]
                merged["depends_on"] += [d for d in epic.get("depends_on", []) if d not in merged["depends_on"]]
                merged["after"] += [d for d in epic.get("after", []) if d not in merged["after"]]
                merged["origins"].append(name)
            if epic.get("kind") == "discovery":
                continue
            selected = applies(epic, ans)
            if selected and STRENGTH[selected] > STRENGTH.get(status.get(eid), 0):
                status[eid] = selected

    # An included archetype's serving epic must exist before the epics that consume the model.
    for name in includes:
        exposes = arches[name].get("exposes")
        if exposes not in per[name]:
            sys.exit(f"{name}: `exposes` must name one of its epics, got {exposes!r}")
        for consumer in declared[name].get("consumed_by", []):
            if consumer in epics and exposes not in epics[consumer]["after"]:
                epics[consumer]["after"].append(exposes)
    return epics, status, arches


def plan(archetype: str, answers: dict, dropped: set[str], includes: dict | None = None,
         profile: str = "production", strike: tuple = (), add: tuple = ()) -> dict:
    includes = includes or {}
    if profile not in PROFILES:
        sys.exit(f"unknown profile {profile!r}; choose from {PROFILES}")
    epics, status, arches = merge_archetypes(archetype, answers, includes)
    phases = arches[archetype]["phases"]
    for eid in dropped & set(epics):
        status[eid] = "dropped"

    conflicts = []
    for eid, state in status.items():
        if state == "dropped":
            continue
        for dep in epics[eid].get("depends_on", []):
            if dep not in epics or epics[dep].get("kind") == "discovery":
                continue
            if status.get(dep, "dropped") == "dropped":
                conflicts.append({"epic": eid, "needs": dep,
                                  "dep_state": "dropped" if dep in dropped else "not selected"})

    live = {e for e, s in status.items() if s != "dropped"}
    bundles, owner, used_titles = [], {}, set()
    for name in [archetype, *includes]:
        for bundle in arches[name]["bundles"]:
            members = [m for m in bundle["members"] if m in live and m not in owner]
            if not members:
                continue
            title = bundle["title"] if bundle["title"] not in used_titles else f"{bundle['title']} ({name})"
            used_titles.add(title)
            owner.update({m: title for m in members})
            bundles.append({"title": title, "members": members, "archetype": name})
    unbundled = sorted(live - set(owner))
    for bundle in bundles:
        # `after` is a soft ordering: it orders epics when both are selected and never conflicts.
        deps = {owner[d] for m in bundle["members"]
                for d in epics[m].get("depends_on", []) + epics[m].get("after", []) if d in owner}
        bundle["depends_on"] = sorted(deps - {bundle["title"]})
        bundle["rank"] = (min(phases.index(epics[m]["phase"]) for m in bundle["members"]),
                          min(bundle["members"]))
        bundle["status"] = "planned" if any(status[m] == "planned" for m in bundle["members"]) else "undecided"

    ordered, placed = [], set()
    pending = sorted(bundles, key=lambda b: b["rank"])
    while pending:
        ready = [b for b in pending if set(b["depends_on"]) <= placed]
        if not ready:
            sys.exit("dependency cycle among: " + ", ".join(b["title"] for b in pending))
        pick = min(ready, key=lambda b: b["rank"])
        ordered.append(pick)
        placed.add(pick["title"])
        pending.remove(pick)

    caps = {eid: capabilities_of(epics[eid]) for eid in epics}
    unknown = (set(strike) | set(add)) - {c["id"] for cs in caps.values() for c in cs}
    if unknown:
        sys.exit(f"unknown capability id(s): {sorted(unknown)}")
    for eid, cs in caps.items():
        for c in cs:
            c["epic"] = eid
            c["selected"] = (c["id"] not in strike) and (c["id"] in add or PROFILES.index(c["tier"]) <= PROFILES.index(profile))

    number = {b["title"]: f"{i:03d}" for i, b in enumerate(ordered, 1)}
    specs = [{"number": number[b["title"]], "title": b["title"], "members": b["members"],
              "archetype": b["archetype"], "status": b["status"], "phase": phases[b["rank"][0]],
              "depends_on": [number[d] for d in b["depends_on"]],
              "capabilities": [c for m in b["members"] for c in caps[m]]} for b in ordered]
    return {"archetype": archetype, "includes": includes, "profile": profile,
            "strike": sorted(strike), "add": sorted(add),
            "library_version": arches[archetype]["library_version"], "answers": answers,
            "epics": {e: status[e] for e in sorted(status)}, "specs": specs, "conflicts": conflicts,
            "unbundled": unbundled}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archetype", default="llm-service")
    parser.add_argument("--answers", default="{}", help="JSON object of intake answers")
    parser.add_argument("--include", default="{}",
                        help='JSON object: {"<included archetype>": {<its intake answers>}}')
    parser.add_argument("--drop", nargs="*", default=[], help="epic ids the user chose to drop")
    parser.add_argument("--profile", default="production", choices=PROFILES)
    parser.add_argument("--strike", nargs="*", default=[], help="capability ids to turn off")
    parser.add_argument("--add", nargs="*", default=[], help="capability ids to turn on")
    args = parser.parse_args()
    print(json.dumps(plan(args.archetype, json.loads(args.answers), set(args.drop), json.loads(args.include),
                          args.profile, tuple(args.strike), tuple(args.add)), indent=2))
