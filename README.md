# ai-roadmaps

A spec-kit extension (`id: roadmap`) that replaces `srobroek/speckit-roadmap`. It assembles a project
roadmap from a reusable epic library, feeds the first unfinished epic to `/speckit-specify`, and keeps
the roadmap's status in step with specify and implement. Derived in part from `srobroek/speckit-roadmap`
(Apache-2.0); see `LICENSE`.

## Archetypes

| Archetype | For | Specs (typical) |
|---|---|---|
| `llm-service` | A request/response service on an LLM, optional RAG, tools, streaming (from a course template) | 8-11 |
| `poc` | A timeboxed feasibility study that ends in a go / no-go and a recommended production archetype | 4 |
| `batch-pipeline` | Offline or scheduled processing of many items (documents, records) with human review of low-confidence results | 10-13 |
| `classical-ml` | A model you train on your data, then serve, monitor and retrain | 9-10 |
| `agent` | An LLM system that plans and acts through tools, with bounded autonomy, state and human oversight | 9-15 |
| `fine-tuning` | Adapting a pre-trained model with your data: strategy, data, evaluation harness, training, safety, serving | 8-10 |
| `perception` | Vision, speech and audio models: capture and labeling, condition coverage, optional edge deployment, field validation | 12-14 |
| `ml-platform` | The shared MLOps platform for internal ML teams, ending in a pilot team | 9-10 |

`llm-service` comes from the course; the other seven are drafted from general practice and should be corrected from projects you have delivered. Epics are shared across archetypes where
they fit (observability, cost, evaluation, deployment); an archetype's `epic_rules` can override an epic's
`applies_when` and `depends_on`.

## Projects with more than one archetype

Pick the archetype that describes the project as a whole (the primary one). If it also builds a model of
another kind, include that archetype in the same roadmap: for example an `llm-service` whose tool is backed
by a classical-ML model. `llm-service`, `agent` and `batch-pipeline` can include `classical-ml`,
`perception` and `fine-tuning`. The intake asks the included archetype's questions, `plan.py --include`
merges its specs into one ordered list, and the spec that consumes the model waits for the model's
"Serving & release" spec. `next` and the hooks keep working on the single roadmap. A model that is its
own independently deployed project can still get its own roadmap instead.

## Workflow

1. `/speckit-constitution`. The extension offers the next step afterwards.
2. `/speckit-roadmap-intake` runs two confirmed interviews and writes the roadmap to
   `.specify/memory/roadmap.md`:
   - **Interview 1, which archetypes?** Plain questions about the shape of the project (feasibility study,
     product or platform; interactive service, agent, batch pipeline or model only; which models you train
     or adapt). It reads the constitution, derives a primary archetype plus included ones, and you confirm.
   - **Interview 2, which epics and capabilities?** Each archetype's gating questions (RAG? tools?
     streaming?), then one profile question: `prototype` (core scope only), `production` (core plus what a
     production system normally needs) or `critical` (everything: regulated, high stakes, large scale). You
     see the proposed optional capabilities (for example canary release, semantic cache, MCP) and strike
     or add; what you drop is listed under Scope (out) as "not needed".
   Decisions not yet made stay as Open Questions.
3. `/speckit-specify` (no description needed). The mandatory `before_specify` hook runs
   `speckit.roadmap.next`, which loads the first unfinished epic into the session. Text you type still
   overrides it.
4. The usual flow: clarify, plan, tasks, implement. `after_specify` marks the epic `specced` and records
   its spec directory; `after_implement` marks it `implemented` when every task in `tasks.md` is checked
   (otherwise `in-progress`), then offers `/speckit-roadmap-debrief`.
5. `/speckit-specify` again takes the next epic. If the next one is already specced it says so and points
   you to plan/tasks/implement; if it is `undecided` or blocked by a dependency it says that instead.

Re-running `/speckit-roadmap-intake` on an existing roadmap amends it non-destructively; the provenance
recorded in the roadmap lets it change the profile, bring a capability back, or add an archetype without
asking again.

## As a global skill

`skills/roadmap-intake/` is a standalone skill generated from the extension's intake command, for use in
any project without installing the extension (no hooks). It finds the library through its own symlink, or
through `$AI_ROADMAPS_HOME`. After editing `commands/speckit.roadmap.intake.md`, run
`python3 scripts/build_skill.py`.

## Commands

| Command | Role |
|---|---|
| `speckit.roadmap.intake` | create or amend the roadmap (reads the constitution) |
| `speckit.roadmap.next` | `before_specify` hook: load the first unfinished epic |
| `speckit.roadmap.specified` | `after_specify` hook: status `specced` + `Spec dir` |
| `speckit.roadmap.implemented` | `after_implement` hook: `implemented` or `in-progress` |
| `speckit.roadmap.brief` | optional `before_implement` hook: what the roadmap expects |
| `speckit.roadmap.debrief` | review the implementation against the roadmap entry |

`/speckit-specify` itself is not modified. Reading the epic relies on the model following the hook's
output, because spec-kit's specify takes the text you typed as the feature description.

## Layout

```
extension.yml  config-template.yml  commands/  templates/
epics/         one markdown file per epic (frontmatter: id, applies_when, depends_on, phase); optional scope
               bullets are tagged `[cap: <id>, tier: production|critical]`
archetypes/    one file per archetype: intake questions, epic overrides, bundles (epics grouped into specs);
               `_selection.md` holds the questions of interview 1
scripts/       select_archetypes.py (interview 1), plan.py (select + order + capabilities), next.py,
               set_status.py, export_jira_csv.py, build_skill.py,
               roadmap_md.py (shared parser), bash/load-config.sh
skills/        the generated standalone global skill
tests/
```

## Install

In a project that already ran `specify init`:

```bash
specify extension remove roadmap     # only if the old srobroek extension is installed
specify extension add --dev /home/rafaelescossia/bezerraescossia/ai-roadmaps
```

`--dev` copies the repo into `.specify/extensions/roadmap/`. After changing the library, run
`specify extension add --dev <repo> --force` again in each project. Needs `python3` and `uv`.

## Jira export

```bash
python3 .specify/extensions/roadmap/scripts/export_jira_csv.py .specify/memory/roadmap.md
```

Epic per spec, Story per Scope (in) bullet, decision Story per Open Question.

## Tests

```bash
uv run --with pyyaml python -m unittest discover -s tests
```

## Changing the library

Edit the epic or archetype files and add a line to `CHANGELOG.md`; bump `library_version` in the
archetype. Each generated roadmap records the library version it came from.
