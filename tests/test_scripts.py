"""Run with: uv run --with pyyaml python -m unittest discover -s tests"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


plan_module = load("plan")
plan = plan_module.plan
export = load("export_jira_csv")
roadmap_md = load("roadmap_md")
import sys as _sys  # noqa: E402
_sys.path.insert(0, str(SCRIPTS))
build_skill = load("build_skill")

ARCHETYPE = "traditional-ml"
ARCHETYPES = (ARCHETYPE,)
ORDER = ["Business & Data Understanding", "Data Engineering", "ML Model Engineering",
         "ML Model Evaluation", "Deployment", "Monitoring & Maintenance"]


def titles(result):
    return [s["title"] for s in result["specs"]]


class PlanTests(unittest.TestCase):
    def test_one_spec_per_epic_in_phase_order(self):
        result = plan(ARCHETYPE, {}, set())
        self.assertEqual(titles(result), ORDER)
        self.assertEqual([s["members"] for s in result["specs"]], [[f"E{i}"] for i in range(1, 7)])
        self.assertEqual([s["number"] for s in result["specs"]], ["001", "002", "003", "004", "005", "006"])
        self.assertEqual(result["conflicts"], [])

    def test_chain_of_dependencies(self):
        specs = plan(ARCHETYPE, {}, set())["specs"]
        self.assertEqual(specs[0]["depends_on"], [])
        for before, spec in zip(specs, specs[1:]):
            self.assertEqual(spec["depends_on"], [before["number"]])

    def test_loop_backs_are_informational(self):
        specs = {s["members"][0]: s for s in plan(ARCHETYPE, {}, set())["specs"]}
        self.assertEqual(specs["E4"]["loops_back_to"], ["003", "002"])
        self.assertEqual(specs["E6"]["loops_back_to"], ["002", "003", "004"])

    def test_answers_never_change_the_epics(self):
        for answers in ({}, {"serving": "online", "regulated": "yes"}, {"serving": "unsure", "regulated": "unsure"},
                        {"labeled_data": "no"}):
            result = plan(ARCHETYPE, answers, set())
            self.assertEqual(titles(result), ORDER)
            self.assertEqual(set(result["epics"].values()), {"planned"})
            self.assertEqual(result["answers"], answers)

    def test_dropping_a_dependency_reports_conflicts(self):
        result = plan(ARCHETYPE, {}, {"E3"})
        self.assertEqual([(c["epic"], c["needs"]) for c in result["conflicts"]], [("E4", "E3")])
        self.assertNotIn("ML Model Engineering", titles(result))
        self.assertEqual(result["epics"]["E3"], "dropped")

    def test_gantt_follows_the_dependency_chain(self):
        gantt = plan(ARCHETYPE, {}, set())["gantt"].splitlines()
        self.assertEqual(gantt[0], "gantt")
        bars = [ln.strip() for ln in gantt if ":e" in ln]
        self.assertEqual(len(bars), 6)
        self.assertIn(":e1, 2000-01-01, 2d", bars[0])
        self.assertIn(":e4, after e3, 2d", bars[3])
        self.assertIn("Day %j", "\n".join(gantt))

    def test_gantt_weights_start_and_drop(self):
        result = plan(ARCHETYPE, {}, {"E6"}, {"E3": 6}, "2026-11-02")
        gantt = result["gantt"]
        self.assertIn(":e1, 2026-11-02, 2d", gantt)
        self.assertIn(":e3, after e2, 6d", gantt)
        self.assertNotIn(":e6", gantt)
        self.assertIn("%b %d", gantt)

    def test_loop_backs_are_listed_not_drawn(self):
        result = plan(ARCHETYPE, {}, set())
        self.assertEqual(result["loop_backs"][-1], {"epic": "E6", "loops_back_to": ["E2", "E3", "E4"]})
        self.assertNotIn("loops", result["gantt"])

    def test_unknown_archetype_or_drop_is_rejected(self):
        with self.assertRaises(SystemExit):
            plan("nonsense", {}, set())
        with self.assertRaises(SystemExit):
            plan(ARCHETYPE, {}, {"E9"})


class LibraryTests(unittest.TestCase):
    def test_list_matches_the_archetype_folders(self):
        listed = [a["archetype"] for a in plan_module.list_archetypes()]
        folders = sorted(p.name for p in (SCRIPTS.parent / "archetypes").iterdir() if p.is_dir())
        self.assertEqual(listed, folders)

    def test_references_resolve_and_ids_are_unique(self):
        for name in ARCHETYPES:
            epics = plan_module.load_epics(name)  # exits on a repeated id or an unknown reference
            files = list((SCRIPTS.parent / "archetypes" / name).glob("E*.md"))
            self.assertEqual(len(epics), len(files), name)

    def test_intake_questions_are_well_formed(self):
        for name in ARCHETYPES:
            intake = plan_module.load_archetype(name)["intake"]
            ids = [q["id"] for q in intake]
            self.assertEqual(len(ids), len(set(ids)), name)
            for question in intake:
                self.assertTrue(question["ask"].endswith("?"), question["id"])

    def test_epic_files_have_the_template_sections(self):
        sections = ["Description", "Outcome", "Tasks", "Outputs", "Quality assurance", "Decisions",
                    "Loop-backs", "Open questions"]
        for path in sorted((SCRIPTS.parent / "archetypes" / ARCHETYPE).glob("E*.md")):
            found = [ln[3:] for ln in path.read_text().splitlines() if ln.startswith("## ")]
            self.assertEqual(found, sections, path.name)

    def test_tagged_variables_are_intake_questions(self):
        import re
        known = {q["id"] for q in plan_module.load_archetype(ARCHETYPE)["intake"]}
        for path in sorted((SCRIPTS.parent / "archetypes" / ARCHETYPE).glob("E*.md")):
            for var in re.findall(r"`\[(\w+)=[\w|-]+\]`", path.read_text()):
                self.assertIn(var, known, f"{path.name}: tag on unknown variable {var}")


class SkillTests(unittest.TestCase):
    def test_standalone_skill_is_up_to_date_and_self_contained(self):
        committed = (SCRIPTS.parent / "skills" / "roadmap-intake" / "SKILL.md").read_text()
        self.assertEqual(committed, build_skill.build(), "run scripts/build_skill.py")
        self.assertNotIn(".specify/extensions/roadmap", committed)
        self.assertNotIn("{SCRIPT}", committed)
        self.assertTrue(committed.startswith("---\nname: roadmap-intake\n"))


class ExportTests(unittest.TestCase):
    ROADMAP = """## Planned Specs

### 001 — Foundation  [status: planned]

- **Description:** Service skeleton.
- **Scope (in):**
  - config and secrets
  - request log schema
- **Depends on:** none

### 002 — Tools  [status: undecided]

- **Description:** Tool loop.
- **Scope (in):** a single prose item

## Open Questions

- Q1 — Which vector store? (spec 002)
"""

    def test_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roadmap.md"
            path.write_text(self.ROADMAP)
            rows = export.rows(path)
        ids = [r[0] for r in rows]
        self.assertEqual(ids, ["E001", "E001-S01", "E001-S02", "E002", "E002-S01", "Q1"])
        self.assertEqual(rows[1][2:5], ["config and secrets", "config and secrets", "E001"])
        self.assertEqual(rows[4][2], "a single prose item")
        self.assertEqual(rows[5][2], "Which vector store?")
        self.assertEqual(rows[5][4:], ["E002", "decision"])


ROADMAP = """<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.1.0
Bump rationale: MINOR — added spec 003
  (continued rationale)

Changes this revision:
  - Added spec 003

Specs affected: 003
Open questions added/resolved: none

Previous (1.0.0): initial creation
-->

# Demo — Spec Roadmap

## Planned Specs

### 001 — Foundation  [status: implemented]

- **Description:** Skeleton.
- **Outcome:** Starts.
- **Scope (in):** skeleton
- **Depends on:** none

### 002 — Gateway  [status: planned]

- **Description:** LLM calls.
- **Outcome:** Uniform stream.
- **Scope (in):**
  - retries
  - fallback
- **Depends on:** 001
- **Notes:** n.

### 003 — Tools  [status: planned]

- **Description:** Tool loop.
- **Outcome:** Calls tools.
- **Scope (in):** loop
- **Depends on:** 001–002

## Open Questions

- Q1 — Retry budget? Resolved when 002 is specified.
- Q2 — Which tools? (spec 003)

---

**Version**: 1.1.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
"""


class NextTests(unittest.TestCase):
    def test_first_planned_entry_is_offered_with_its_questions(self):
        result = roadmap_md.next_action(ROADMAP)
        self.assertEqual((result["action"], result["number"]), ("specify", "002"))
        self.assertEqual(result["scope_in"].count("-"), 2)
        self.assertEqual([q.split(" ")[0] for q in result["open_questions"]], ["Q1"])

    def test_specced_entry_resumes_instead_of_respecifying(self):
        text = roadmap_md.set_status(ROADMAP, "002", "specced", "specs/002-gateway", today="2026-02-01")
        result = roadmap_md.next_action(text)
        self.assertEqual((result["action"], result["spec_dir"]), ("resume", "specs/002-gateway"))

    def test_unfinished_dependency_blocks_and_undecided_blocks(self):
        text = roadmap_md.set_status(ROADMAP, "002", "undecided", today="2026-02-01")
        self.assertEqual(roadmap_md.next_action(text)["action"], "blocked")

    def test_everything_done_is_complete(self):
        text = ROADMAP
        for n in ("002", "003"):
            text = roadmap_md.set_status(text, n, "implemented", today="2026-02-01")
        self.assertEqual(roadmap_md.next_action(text), {"action": "complete"})

    def test_deferred_dependency_is_a_warning_not_a_block(self):
        text = roadmap_md.set_status(ROADMAP, "002", "deferred", today="2026-02-01")
        result = roadmap_md.next_action(text)
        self.assertEqual((result["action"], result["number"]), ("specify", "003"))
        self.assertTrue(result["warnings"])


class SetStatusTests(unittest.TestCase):
    def test_bumps_patch_updates_footer_and_keeps_history(self):
        text = roadmap_md.set_status(ROADMAP, "002", "specced", "specs/002-gateway", today="2026-02-01")
        self.assertIn("### 002 — Gateway  [status: specced]", text)
        self.assertIn("- **Spec dir:** specs/002-gateway", text)
        self.assertIn("**Version**: 1.1.1 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-02-01", text)
        self.assertIn("Version change: 1.1.0 → 1.1.1", text)
        self.assertIn("Previous (1.1.0): MINOR — added spec 003", text)
        self.assertIn("  (continued rationale)", text)
        self.assertIn("Previous (1.0.0): initial creation", text)

    def test_is_idempotent(self):
        once = roadmap_md.set_status(ROADMAP, "002", "specced", "specs/002-gateway", today="2026-02-01")
        twice = roadmap_md.set_status(once, "002", "specced", "specs/002-gateway", today="2026-03-01")
        self.assertEqual(once, twice)

    def test_rejects_unknown_status_and_entry(self):
        with self.assertRaises(ValueError):
            roadmap_md.set_status(ROADMAP, "002", "finished")
        with self.assertRaises(ValueError):
            roadmap_md.set_status(ROADMAP, "009", "specced")

    def test_find_by_spec_dir(self):
        text = roadmap_md.set_status(ROADMAP, "003", "specced", "specs/003-tools", today="2026-02-01")
        entry = roadmap_md.find_by_spec_dir(text.splitlines(), "specs/003-tools/")
        self.assertEqual(entry.number, "003")


if __name__ == "__main__":
    unittest.main()
