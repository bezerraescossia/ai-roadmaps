# Changelog

## 1.0.0 — 2026-10-30

- Library restarted. All earlier archetypes and the shared `epics/` pool are removed; archetypes are rebuilt
  one at a time and each owns its epics in `archetypes/<slug>/`.
- New archetype `traditional-ml` (Traditional Machine Learning Algorithms) following CRISP-ML(Q): six epics,
  one per phase, each one spec, in a linear dependency chain. `loops_back_to` records the methodology's
  iteration edges and never blocks. All epics are always included; the seven intake answers tailor items
  inside them. Items the library adds to the methodology are marked `(added)`.
- Epics carry a relative `weight`. `plan.py` generates a Mermaid Gantt (`--weights` overrides, `--start`
  for real dates) plus `loop_backs`, and the roadmap template has a `## Timeline` section for them.
- Removed: `applies_when`, `epic_rules`, bundles, `includes`, profiles and capabilities, interview 1 and
  `select_archetypes.py` (`plan.py --list` replaces it). The intake is one interview.

## 0.9.0 — 2026-10-29

- New epic `E64` **Serving Contract & Stub**, the first spec of every archetype except `poc`. It agrees the
  consumer/provider contract up front (schemas, errors, versioning, auth, field semantics), publishes a
  hosted stub with constant canonical responses plus named fixtures (error, empty, low confidence,
  timeout), records consumer sign-off, and keeps a revision window until the first real release. Contract
  tests are the capability `contract-tests` (production tier).
- `E31`, `E58` and `E15` depend on `E64`; the real serving epics implement the contract instead of defining it.
- Epic frontmatter `first: true` sorts an epic ahead of the others in its phase when the planner breaks ties.
- Archetype `library_version` is now 0.9.0.

## 0.8.0 — 2026-10-28

- The intake reads the project brief (`./brief.md`, `./docs/brief.md` or `.specify/brief.md`) after the
  constitution and uses it to pre-fill interview answers, Vision & End States, `C-nn` constraints and Open
  Questions. The constitution wins on conflicts, which are reported. The brief's path is stored in the
  provenance JSON and amend mode re-reads it.

## 0.7.0 — 2026-10-28

- `skills/roadmap-intake/SKILL.md`: a standalone global skill, generated from the extension's intake command
  by `scripts/build_skill.py`, that works in any project and reads the library from this repository. A test
  fails when it is out of date.

- The intake is now two confirmed interviews. **Interview 1** asks plain questions about the project's shape
  (`archetypes/_selection.md`) and `scripts/select_archetypes.py` derives the primary archetype and the
  included ones (the operational archetype is primary; model-building ones are included; model-building
  archetypes cannot include each other). **Interview 2** asks each archetype's gating questions, then one
  project **profile** (`prototype`, `production`, `critical`) and shows a proposed list of capabilities to
  strike or add.
- **Capabilities**: 27 optional scope bullets inside epics are tagged `[cap: <id>, tier: <tier>]` (for
  example `canary-release`, `shared-cache`, `mcp`, `tracing`, `model-card`). Untagged bullets are core.
  `plan.py --profile --strike --add` reports each spec's capabilities with `selected`. Unselected ones are
  written under the spec's Scope (out) as "Not needed", and can be brought back by amending.
- The roadmap's provenance line is one JSON object (answers, profile, strikes), so amend mode can re-plan.
- Split three mixed bullets so only the optional half is a capability: E04 (manual rollback vs automatic
  revert), E24 (routing vs sampled audit), E45 (automatic metrics vs judge calibration vs human sample).

## 0.6.0 — 2026-10-28

- A project can now combine archetypes in one roadmap: a primary archetype plus **included** ones. The
  `llm-service`, `agent` and `batch-pipeline` archetypes declare which of `classical-ml`, `perception` and
  `fine-tuning` they can include (`includes`), and each of those names its serving epic (`exposes: E31`).
- `plan.py --include '{"<archetype>": {<answers>}}'`: included archetypes keep their own intake answers; epics
  shared between archetypes appear once (selected if any archetype selects them, dependencies are the union);
  the epics that consume the model (`consumed_by`) are ordered after its serving epic. Each spec reports the
  archetype it came from.
- The `custom_ml` rule in `llm-service` now includes the model's archetype instead of asking for a separate
  roadmap; `agent` gains a `custom_ml` question and `batch-pipeline` includes a model when `approach` is `ml`
  or `hybrid`.
- `intake` runs the included archetype's intake (skipping `constraints`) and records every archetype's
  answers in the provenance.

## 0.5.0 — 2026-10-28

Deduplicated the epic library (63 → 58 epics). Rule: merge the same concern at the same scope; keep
project-versus-platform pairs (E27-E33 and E54-E60) separate. Epic ids are stable; retired ids are mapped here.

| Retired | Now |
|---|---|
| E01 Use Case Definition & Solution Design | E16 Problem Framing & Success Criteria (llm-service now uses E16; its model and provider decision is an archetype note) |
| E08 Custom ML Model | Removed. With `custom_ml: yes` the llm-service intake asks for a separate `classical-ml` roadmap per model and adds an Open Question on how it is integrated |
| E39 Human Oversight & Approvals | E24, now "Human Review & Oversight", used by `batch-pipeline`, `agent` and (opt-in, `human_review`) `llm-service` |
| E46 Model Packaging, Registry & Serving | E30 Model Registry + E31 Model Serving, with `fine-tuning` notes |
| E48 Monitoring & Continuous Improvement | E32 Monitoring + E33 Retraining, with `fine-tuning` notes, applied when `continuous` is `yes` |

- Each repeated concern now has one home epic: model card in E30 (E56 for the platform), rollout and
  rollback in E31 (E58 for the platform), feedback capture in E14, retraining triggers in E33, cost
  tracking in E13. E24, E26, E34, E47 and E59 reference the home instead of repeating the story.
- New test: no epic, archetype or command may reference a retired id.

## 0.4.0 — 2026-10-28

- New archetypes (drafted from general practice, to be corrected from delivered projects):
  `agent` (E35-E40 plus shared epics), `fine-tuning` (E41-E48), `perception` (E49-E52 plus the classical-ml
  epics) and `ml-platform` (E53-E63).
- Shared epics extended with "Archetype notes": E02, E03, E06, E07, E09, E10, E11, E12, E13, E14, E15 for
  `agent`; E15, E17 for `fine-tuning`; E15, E17, E27-E34 for `perception`. E16 is now shared by seven
  archetypes.
- `agent` overrides E07 to always apply and E03 to apply unless `interface` is `background`.

## 0.3.0 — 2026-10-28

- New archetypes (drafted from general practice, to be corrected from delivered projects):
  `poc` (E16-E20), `batch-pipeline` (E21-E26 plus shared epics), `classical-ml` (E27-E34 plus E15).
- New shared epics: E16 Problem Framing & Success Criteria (discovery), E17 Data Availability & Quality
  Assessment. E02, E09, E10, E12, E13, E14 and E15 now also serve `batch-pipeline` (E15 also
  `classical-ml`), with an "Archetype notes" section for each.
- `plan.py`: per-archetype `epic_rules` overrides, `!=` rules, `after` soft ordering, an `unbundled` check.
- `intake` proposes an archetype from the available ones instead of assuming `llm-service`.

## 0.2.0 — 2026-10-28

- The repo is now a spec-kit extension (`id: roadmap`) that replaces `srobroek/speckit-roadmap`.
- New commands: `intake` (reads the constitution; creates or amends the roadmap), `next` (`before_specify`
  hook), `specified` (`after_specify`), `implemented` (`after_implement`). `brief` and `debrief` carried
  over and adapted; `write` and `sync` removed (re-run `intake` to amend; hooks keep statuses in sync).
- `scripts/set_status.py` changes a status with a PATCH bump and keeps the Sync Impact Report history;
  `scripts/next.py` picks the first unfinished epic (resume / blocked / complete are reported, not
  re-specified).
- The standalone `roadmap-intake` skill and `install.sh` are removed.
- Evaluation and Ops hardening & launch are separate bundles.

## 0.1.0 — 2026-10-28

- First library version: `llm-service` archetype ported from the course template (15 epics, no effort
  estimates).
- Dependencies reordered from the course numbering: `E14` Evaluation precedes `E04` and `E06`; `E09`
  and `E12` depend on `E10`; `E11` depends only on `E03`.
- `scripts/plan.py` selects epics from intake answers and orders bundles topologically.
- `scripts/export_jira_csv.py` exports a speckit-format roadmap to a Jira CSV.
