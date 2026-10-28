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
sys_path_scripts = str(SCRIPTS)
import sys as _sys  # noqa: E402
_sys.path.insert(0, sys_path_scripts)
build_skill = load("build_skill")
select_module = load("select_archetypes")
select = select_module.select

FULL = {"rag": "yes", "tools": "yes", "streaming": "yes", "caching": "yes"}


def titles(result):
    return [s["title"] for s in result["specs"]]


class PlanTests(unittest.TestCase):
    def test_core_only_has_no_optional_epics(self):
        result = plan("llm-service", {}, set())
        for optional in ("E05", "E06", "E07", "E11", "E24"):
            self.assertNotIn(optional, result["epics"])
        self.assertNotIn("E16", result["epics"])  # discovery is not a spec

    def test_numbers_follow_dependencies(self):
        result = plan("llm-service", FULL, set())
        order = titles(result)
        self.assertEqual(order[0], "Foundation")
        for later in ("Prompt router", "Knowledge base + RAG"):
            self.assertLess(order.index("Evaluation & quality"), order.index(later))
        self.assertLess(order.index("LLM gateway"), order.index("Guardrails"))
        by_title = {s["title"]: s for s in result["specs"]}
        for spec in result["specs"]:
            for dep in spec["depends_on"]:
                self.assertLess(dep, spec["number"])
        self.assertEqual(by_title["Foundation"]["depends_on"], [])

    def test_unsure_optional_epic_is_undecided(self):
        result = plan("llm-service", {"rag": "unsure"}, set())
        self.assertEqual(result["epics"]["E06"], "undecided")
        rag = next(s for s in result["specs"] if s["title"] == "Knowledge base + RAG")
        self.assertEqual(rag["status"], "undecided")

    def test_dropping_a_dependency_reports_conflicts(self):
        result = plan("llm-service", {"rag": "yes"}, {"E14"})
        pairs = {(c["epic"], c["needs"]) for c in result["conflicts"]}
        self.assertEqual(pairs, {("E04", "E14"), ("E06", "E14")})
        self.assertNotIn("Evaluation & quality", titles(result))


ARCHETYPES = ("llm-service", "poc", "batch-pipeline", "classical-ml",
              "agent", "fine-tuning", "perception", "ml-platform")
ANSWERS = {
    "llm-service": FULL,
    "poc": {},
    "batch-pipeline": {"input_docs": "yes", "scanned": "yes", "human_review": "yes", "sensitive_data": "yes"},
    "classical-ml": {"serving": "online", "regulated": "yes"},
    "agent": {"interface": "chat", "human_oversight": "yes", "code_execution": "yes", "memory": "yes",
              "multi_agent": "yes", "rag": "yes", "streaming": "yes"},
    "fine-tuning": {"hosting": "self-hosted", "continuous": "yes"},
    "perception": {"serving": "embedded", "regulated": "yes"},
    "ml-platform": {"llmops": "yes", "feature_store": "yes", "regulated": "yes"},
}


class LibraryTests(unittest.TestCase):
    """Every archetype loads, plans without conflicts, and no selected epic is left out of a bundle."""

    def test_each_archetype_plans_cleanly(self):
        for name in ARCHETYPES:
            with self.subTest(archetype=name):
                result = plan(name, ANSWERS[name], set())
                self.assertEqual(result["conflicts"], [])
                self.assertEqual(result["unbundled"], [])
                self.assertTrue(result["specs"])

    def test_references_resolve(self):
        arch_ids = {}
        for name in ARCHETYPES:
            arch = plan_module.load_archetype(name)
            epics = plan_module.load_epics(name, arch.get("epic_rules", {}))
            arch_ids[name] = set(epics)
            for epic in epics.values():
                for ref in epic.get("depends_on", []) + epic.get("after", []):
                    self.assertIn(ref, epics, f"{name}: {epic['id']} references {ref}")
            for bundle in arch["bundles"]:
                for member in bundle["members"]:
                    self.assertIn(member, epics, f"{name}: bundle {bundle['title']} lists {member}")

    def test_every_epic_belongs_to_an_archetype_and_has_unique_id(self):
        seen = {}
        for path in sorted((SCRIPTS.parent / "epics").glob("E*.md")):
            meta = plan_module.frontmatter(path)
            self.assertNotIn(meta["id"], seen, f"{path.name} repeats {meta['id']}")
            seen[meta["id"]] = path.name
            self.assertTrue(set(meta["archetypes"]) <= set(ARCHETYPES), path.name)

    def test_poc_is_a_straight_line(self):
        result = plan("poc", {}, set())
        self.assertEqual([s["title"] for s in result["specs"]],
                         ["Data assessment", "Prototype & baseline", "Feasibility evaluation",
                          "Go / no-go & production estimate"])

    def test_batch_optional_epics_follow_the_answers(self):
        result = plan("batch-pipeline", {"input_docs": "no", "human_review": "no", "sensitive_data": "no"}, set())
        for absent in ("E09", "E22", "E24"):
            self.assertNotIn(absent, result["epics"])
        order = titles(result)
        self.assertLess(order.index("Evaluation & quality"), order.index("Extraction & classification"))
        undecided = plan("batch-pipeline", {"human_review": "unsure"}, set())
        self.assertEqual(undecided["epics"]["E24"], "undecided")

    def test_ml_regulated_and_serving_rules(self):
        self.assertNotIn("E34", plan("classical-ml", {"regulated": "no"}, set())["epics"])
        self.assertEqual(plan("classical-ml", {"regulated": "unsure"}, set())["epics"]["E34"], "undecided")
        order = titles(plan("classical-ml", {"regulated": "yes"}, set()))
        self.assertLess(order.index("Offline evaluation"), order.index("Model registry"))
        self.assertEqual(order[-1], "Deployment & launch readiness")

    def test_agent_rules(self):
        background = plan("agent", {"interface": "background"}, set())
        self.assertNotIn("E03", background["epics"])
        for optional in ("E37", "E38", "E24", "E40", "E06", "E11"):
            self.assertNotIn(optional, background["epics"])
        self.assertIn("E07", background["epics"])  # tools always apply to an agent
        order = titles(plan("agent", ANSWERS["agent"], set()))
        self.assertLess(order.index("Agent design"), order.index("Orchestration"))
        self.assertLess(order.index("Tools & integrations"), order.index("Orchestration"))
        self.assertLess(order.index("Sandbox & execution"), order.index("Human oversight"))
        self.assertEqual(order[-1], "Deployment & launch readiness")
        self.assertEqual(plan("agent", {"human_oversight": "unsure"}, set())["epics"]["E24"], "undecided")

    def test_fine_tuning_puts_evaluation_before_training(self):
        result = plan("fine-tuning", {"continuous": "no"}, set())
        for monitoring in ("E32", "E33"):
            self.assertNotIn(monitoring, result["epics"])
        order = titles(result)
        self.assertLess(order.index("Adaptation strategy"), order.index("Training data"))
        self.assertLess(order.index("Evaluation harness"), order.index("Training & iteration"))
        self.assertLess(order.index("Safety, licensing & governance"), order.index("Packaging & serving"))
        self.assertLess(order.index("Training & iteration"), order.index("Packaging & serving"))

    def test_perception_edge_and_ordering(self):
        self.assertNotIn("E51", plan("perception", {"serving": "online"}, set())["epics"])
        self.assertEqual(plan("perception", {"serving": "unsure"}, set())["epics"]["E51"], "undecided")
        order = titles(plan("perception", {"serving": "embedded"}, set()))
        self.assertLess(order.index("Capture & labeling"), order.index("Data pipeline"))
        self.assertLess(order.index("Edge optimization"), order.index("Serving & release"))
        self.assertLess(order.index("Robustness & field validation"), order.index("Deployment & launch readiness"))

    def test_ml_platform_order_and_optional(self):
        result = plan("ml-platform", {"llmops": "no"}, set())
        self.assertNotIn("E63", result["epics"])
        order = titles(result)
        self.assertEqual(order[0], "Compute & environments")
        self.assertEqual(order[-1], "Developer experience & adoption")
        self.assertLess(order.index("Tracking & registry"), order.index("Pipelines & orchestration"))

    def test_retired_ids_are_not_referenced(self):
        retired = ("E01", "E08", "E39", "E46", "E48")
        root = SCRIPTS.parent
        for folder in ("epics", "archetypes", "commands"):
            for path in (root / folder).glob("*.md"):
                text = path.read_text()
                for eid in retired:
                    self.assertNotRegex(text, rf"\b{eid}\b", f"{path.name} still mentions retired {eid}")
        for eid in retired:
            self.assertFalse(list((root / "epics").glob(f"{eid}-*.md")), f"{eid} file still exists")

    def test_human_review_is_one_epic_across_archetypes(self):
        self.assertNotIn("E24", plan("llm-service", {"human_review": "no"}, set())["epics"])
        self.assertEqual(plan("llm-service", {"human_review": "unsure"}, set())["epics"]["E24"], "undecided")
        order = titles(plan("llm-service", {"human_review": "yes"}, set()))
        self.assertIn("Human review", order)
        batch = plan("batch-pipeline", {"human_review": "yes"}, set())
        self.assertLess(titles(batch).index("Extraction & classification"), titles(batch).index("Review loop"))
        agent = titles(plan("agent", {"human_oversight": "yes", "code_execution": "yes"}, set()))
        self.assertLess(agent.index("Orchestration"), agent.index("Human oversight"))
        self.assertLess(agent.index("Sandbox & execution"), agent.index("Human oversight"))

    def test_fine_tuning_reuses_registry_serving_monitoring_and_retraining(self):
        result = plan("fine-tuning", {"continuous": "yes"}, set())
        for reused in ("E30", "E31", "E32", "E33"):
            self.assertEqual(result["epics"][reused], "planned")
        by_title = {s["title"]: s for s in result["specs"]}
        self.assertEqual(by_title["Packaging & serving"]["members"], ["E30", "E31"])
        self.assertEqual(by_title["Monitoring & improvement"]["members"], ["E32", "E33"])
        order = titles(result)
        self.assertLess(order.index("Safety, licensing & governance"), order.index("Packaging & serving"))
        self.assertEqual(order[-1], "Deployment & launch readiness")
        self.assertEqual(len(result["specs"]), 10)

    def test_llm_service_has_no_custom_ml_epic(self):
        self.assertEqual(set(plan("llm-service", {"custom_ml": "yes"}, set())["epics"]),
                         set(plan("llm-service", {"custom_ml": "no"}, set())["epics"]))

    def test_includes_are_declared_and_resolvable(self):
        for name in ARCHETYPES:
            arch = plan_module.load_archetype(name)
            epics = plan_module.load_epics(name, arch.get("epic_rules", {}))
            for included, link in arch.get("includes", {}).items():
                other = plan_module.load_archetype(included)
                self.assertIn(other.get("exposes"), plan_module.load_epics(
                    included, other.get("epic_rules", {})), f"{included} must expose one of its epics")
                for consumer in link.get("consumed_by", []):
                    self.assertIn(consumer, epics, f"{name}: consumed_by {consumer}")

    def test_llm_service_with_an_included_classical_model(self):
        answers = {"rag": "yes", "tools": "yes", "custom_ml": "yes"}
        result = plan("llm-service", answers, set(), {"classical-ml": {"serving": "online", "regulated": "no"}})
        self.assertEqual((result["conflicts"], result["unbundled"]), ([], []))
        order = titles(result)
        self.assertEqual(len(order), len(set(order)))
        self.assertEqual(order.count("Ops hardening & launch"), 1)  # shared E15 appears once
        self.assertNotIn("Deployment & launch readiness", order)
        self.assertLess(order.index("Serving & release"), order.index("Tools"))  # the model before its consumer
        self.assertLess(order.index("Monitoring & drift"), order.index("Ops hardening & launch"))
        by_title = {s["title"]: s for s in result["specs"]}
        self.assertEqual(by_title["Tools"]["archetype"], "llm-service")
        self.assertEqual(by_title["Serving & release"]["archetype"], "classical-ml")
        self.assertEqual(result["includes"], {"classical-ml": {"serving": "online", "regulated": "no"}})

    def test_included_archetype_keeps_its_own_answers(self):
        # `serving` means "where inference runs" only inside perception; the primary's value must not leak.
        result = plan("llm-service", {"serving": "embedded"}, set(), {"perception": {"serving": "online"}})
        self.assertNotIn("E51", result["epics"])
        result = plan("llm-service", {"serving": "online"}, set(), {"perception": {"serving": "embedded"}})
        self.assertEqual(result["epics"]["E51"], "planned")

    def test_shared_epics_use_the_union_of_dependencies(self):
        result = plan("agent", {"interface": "api"}, set(), {"fine-tuning": {"hosting": "api", "continuous": "no"}})
        by_title = {s["title"]: s for s in result["specs"]}
        launch = by_title["Deployment & launch readiness"]
        needed = {by_title[t]["number"] for t in ("Packaging & serving", "Evaluation harness",
                                                  "Safety, licensing & governance", "LLM integration & reliability")}
        self.assertTrue(needed <= set(launch["depends_on"]), launch["depends_on"])

    def test_two_included_archetypes_share_epics_once(self):
        result = plan("agent", {"interface": "api"}, set(),
                      {"classical-ml": {"regulated": "no"}, "perception": {"serving": "online", "regulated": "no"}})
        self.assertEqual((result["conflicts"], result["unbundled"]), ([], []))
        members = [m for s in result["specs"] for m in s["members"]]
        self.assertEqual(len(members), len(set(members)))
        self.assertIn("E49", result["epics"])  # perception-only epic
        self.assertIn("E27", result["epics"])  # shared by both models

    def test_undeclared_include_is_rejected(self):
        with self.assertRaises(SystemExit):
            plan("poc", {}, set(), {"classical-ml": {}})
        with self.assertRaises(SystemExit):
            plan("llm-service", {}, set(), {"ml-platform": {}})

    def test_not_equals_rule(self):
        epic = {"id": "X", "applies_when": "labeled_data != yes"}
        self.assertIsNone(plan_module.applies(epic, {"labeled_data": "yes"}))
        self.assertEqual(plan_module.applies(epic, {"labeled_data": "no"}), "planned")
        self.assertEqual(plan_module.applies(epic, {"labeled_data": "unsure"}), "undecided")


def selected_caps(result):
    return {c["id"] for spec in result["specs"] for c in spec["capabilities"] if c["selected"]}


def all_caps(result):
    return {c["id"]: c for spec in result["specs"] for c in spec["capabilities"]}


class CapabilityTests(unittest.TestCase):
    def test_tags_are_well_formed_and_unique(self):
        seen = {}
        for path in sorted((SCRIPTS.parent / "epics").glob("E*.md")):
            for line in path.read_text().splitlines():
                if "[cap:" in line:
                    self.assertRegex(line, plan_module.CAP.pattern, f"{path.name}: malformed tag: {line}")
                    cid = plan_module.CAP.match(line)[1]
                    self.assertNotIn(cid, seen, f"{cid} appears in {path.name} and {seen.get(cid)}")
                    seen[cid] = path.name
        self.assertGreaterEqual(len(seen), 25)

    def test_profile_sets_the_default(self):
        answers = ANSWERS["llm-service"]
        prototype = plan("llm-service", answers, set(), profile="prototype")
        production = plan("llm-service", answers, set(), profile="production")
        critical = plan("llm-service", answers, set(), profile="critical")
        self.assertEqual(selected_caps(prototype), set())
        self.assertTrue(selected_caps(production) < selected_caps(critical))
        tiers = {c["id"]: c["tier"] for c in all_caps(critical).values()}
        self.assertEqual({tiers[i] for i in selected_caps(production)}, {"production"})
        self.assertEqual({tiers[i] for i in selected_caps(critical)}, {"production", "critical"})

    def test_strike_and_add_override_the_profile(self):
        result = plan("classical-ml", {}, set(), profile="critical", strike=("canary-release",))
        self.assertFalse(all_caps(result)["canary-release"]["selected"])
        self.assertTrue(all_caps(result)["model-card"]["selected"])
        result = plan("classical-ml", {}, set(), profile="prototype", add=("canary-release",))
        self.assertEqual(selected_caps(result), {"canary-release"})

    def test_capabilities_belong_to_the_spec_of_their_epic(self):
        result = plan("classical-ml", {}, set(), profile="critical")
        by_title = {s["title"]: s for s in result["specs"]}
        self.assertEqual([c["id"] for c in by_title["Serving & release"]["capabilities"]], ["canary-release"])
        self.assertEqual(by_title["Serving & release"]["capabilities"][0]["epic"], "E31")
        self.assertIn("shadow mode", by_title["Serving & release"]["capabilities"][0]["text"])

    def test_unknown_ids_and_profiles_are_rejected(self):
        with self.assertRaises(SystemExit):
            plan("classical-ml", {}, set(), strike=("nonsense",))
        with self.assertRaises(SystemExit):
            plan("classical-ml", {}, set(), profile="enterprise")


class SelectTests(unittest.TestCase):
    def test_runtime_archetype_is_primary_and_models_are_included(self):
        result = select({"purpose": "product", "runtime": "interactive-service",
                         "own_models": ["tabular-or-time-series", "llm-adaptation"]})
        self.assertEqual((result["primary"], result["includes"]), ("llm-service", ["classical-ml", "fine-tuning"]))
        self.assertEqual((result["unsupported"], result["needs"]), ([], []))

    def test_purpose_decides_poc_and_platform(self):
        self.assertEqual(select({"purpose": "feasibility-study", "runtime": "agent"})["primary"], "poc")
        self.assertEqual(select({"purpose": "platform"})["primary"], "ml-platform")

    def test_model_only_products(self):
        result = select({"purpose": "product", "runtime": "model-only",
                         "own_models": ["images-video-audio", "tabular-or-time-series"]})
        self.assertEqual((result["primary"], result["includes"]), ("perception", []))
        self.assertEqual([u["archetype"] for u in result["unsupported"]], ["classical-ml"])
        self.assertEqual(select({"purpose": "product", "runtime": "model-only"})["needs"], ["own_models"])

    def test_missing_answers_are_reported(self):
        self.assertEqual(select({})["needs"], ["purpose"])
        self.assertEqual(select({"purpose": "product"})["needs"], ["runtime"])

    def test_every_selectable_archetype_exists(self):
        sel = select_module
        for name in list(sel.RUNTIME.values()) + list(sel.MODELS.values()) + ["poc", "ml-platform"]:
            self.assertTrue((SCRIPTS.parent / "archetypes" / f"{name}.md").is_file(), name)


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
