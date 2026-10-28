---
description: Find the first unfinished roadmap epic and hand it to /speckit-specify as the feature description (runs automatically before specify).
scripts:
  sh: .specify/extensions/roadmap/scripts/bash/load-config.sh
---

## User Input

```text
$ARGUMENTS
```

## Goal

`/speckit-specify` normally needs a feature description typed by the user. When the project has a
roadmap, the next unfinished epic **is** that description. This command finds it and puts it in front of
specify. It writes nothing.

## Outline

1. Run `{SCRIPT}` from the repo root and parse `roadmap_path` and `roadmap_exists`. If the roadmap does
   not exist, say in one line that there is no roadmap (suggest `/speckit-roadmap-intake`) and let
   specify continue with whatever the user typed. Stop.

2. Run:

   ```bash
   python3 .specify/extensions/roadmap/scripts/next.py <roadmap_path>
   ```

   It prints JSON with `action` = `specify` | `resume` | `blocked` | `complete`.

3. **If the user typed their own feature description for `/speckit-specify`, it wins.** Do not replace it.
   Report the roadmap's next epic in one line for information, and if the typed description clearly
   matches a roadmap entry by title, say which one so `speckit.roadmap.specified` can link it. Stop.

4. Otherwise act on `action`:

   - **`specify`** — print a block headed `## Roadmap epic NNN — <title>` containing its description,
     outcome, scope (in), scope (out), depends on, governed by, notes, and the listed open questions,
     then state plainly:

     > Use this epic as the feature description for `/speckit-specify`. Treat the open questions as
     > items to settle or mark `[NEEDS CLARIFICATION]` in the spec, not as decisions already made.
     > Remember this is roadmap epic **NNN**; `speckit.roadmap.specified` will link it afterwards.

     If `warnings` is non-empty (a dependency was deferred or abandoned), show them first.

   - **`resume`** — the epic is already `specced` or `in-progress` (`spec_dir` says where). Tell the user:
     "Epic NNN is already specced at `<spec_dir>`. Continue with `/speckit-plan`, `/speckit-tasks`, or
     `/speckit-implement` for that spec instead of running specify again." **Do not run specify.**

   - **`blocked`** — explain `reason`. If the status is `undecided` or `needs-info`, list its open
     questions and suggest settling them (for example with `/speckit-grill-me`) or marking the epic
     `deferred`. If it depends on an unfinished epic, name it. **Do not run specify** unless the user
     typed a description.

   - **`complete`** — every epic is implemented, verified, deferred or abandoned. Say so. **Do not run
     specify** unless the user typed a description.
