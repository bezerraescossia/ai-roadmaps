# ai-roadmaps

A spec-kit extension (`id: roadmap`) that replaces `srobroek/speckit-roadmap`. It assembles a project
roadmap from a reusable archetype library, feeds the first unfinished epic to `/speckit-specify`, and keeps
the roadmap's status in step with specify and implement. Derived in part from `srobroek/speckit-roadmap`
(Apache-2.0); see `LICENSE`.

## Archetypes

The library is being rebuilt one archetype at a time. Each archetype lives in `archetypes/<slug>/` and owns
its epics: one epic per phase of its methodology, one spec per epic.

| Archetype | For | Methodology | Specs |
|---|---|---|---|
| `traditional-ml` | A model you train on your data with classical algorithms, then deploy, monitor and maintain | [CRISP-ML(Q)](https://ml-ops.org/content/crisp-ml) | 6 |

All of an archetype's epics are always in the roadmap. Intake answers tailor the items inside the epics and
never include or exclude one; items the answers rule out stay as "not applicable". `depends_on` orders the
epics; `loops_back_to` records the methodology's iteration edges (for example evaluation back to model
engineering) and never blocks. Items the library adds to the methodology are marked `(added)`.

Each epic has a relative `weight` (proportional, not an estimate). `plan.py` draws a Mermaid Gantt chart
from `depends_on` and the weights, with a relative axis or real dates when given `--start`, and the intake
writes it under `## Timeline` in the roadmap. Loop-backs are listed under the chart, since a Gantt cannot
draw them.

## Workflow

1. `/speckit-constitution`. The extension offers the next step afterwards.
2. `/speckit-roadmap-intake` runs one confirmed interview and writes the roadmap to
   `.specify/memory/roadmap.md`. It reads the constitution and the brief, you confirm the archetype, then
   it asks that archetype's intake questions (skipping what the context already answers). Decisions not yet
   made stay as Open Questions.
3. `/speckit-specify` (no description needed). The mandatory `before_specify` hook runs
   `speckit.roadmap.next`, which loads the first unfinished epic into the session. Text you type still
   overrides it.
4. The usual flow: clarify, plan, tasks, implement. `after_specify` marks the epic `specced` and records
   its spec directory; `after_implement` marks it `implemented` when every task in `tasks.md` is checked
   (otherwise `in-progress`), then offers `/speckit-roadmap-debrief`.
5. `/speckit-specify` again takes the next epic. If the next one is already specced it says so and points
   you to plan/tasks/implement; if it is `undecided` or blocked by a dependency it says that instead.

Re-running `/speckit-roadmap-intake` on an existing roadmap amends it non-destructively; the provenance
recorded in the roadmap lets it apply a changed or newly answered intake question without asking again.

## As a global skill

`skills/roadmap-intake/` is a standalone skill generated from the extension's intake command, for use in
any project without installing the extension (no hooks). It finds the library through its own symlink, or
through `$AI_ROADMAPS_HOME`. After editing `commands/speckit.roadmap.intake.md`, run
`python3 scripts/build_skill.py`.

## Commands

| Command | Role |
|---|---|
| `speckit.roadmap.intake` | create or amend the roadmap (reads the constitution and `brief.md`) |
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
archetypes/    one folder per archetype: `archetype.md` (intake questions, rules) and its epic files
               `E*.md` (frontmatter: id, title, phase, depends_on, loops_back_to); one epic = one spec
scripts/       plan.py (list archetypes, order epics into specs), next.py,
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
