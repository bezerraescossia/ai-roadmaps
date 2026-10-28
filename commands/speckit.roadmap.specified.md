---
description: Mark the roadmap epic that was just specified as `specced` and record its spec directory (runs automatically after specify).
scripts:
  sh: .specify/extensions/roadmap/scripts/bash/load-config.sh
---

## User Input

```text
$ARGUMENTS
```

## Goal

Keep the roadmap in step with spec-kit: once `/speckit-specify` has created a spec directory for an epic,
the epic moves from `planned` to `specced` and gets a `Spec dir:` pointer. That is what stops `next`
from offering it again.

## Outline

1. Run `{SCRIPT}` and parse `roadmap_path` and `roadmap_exists`. If there is no roadmap, stop silently.

2. Find the feature directory: `feature_directory` in `.specify/feature.json`; otherwise the newest
   directory under `specs/`. If none, stop and say so.

3. Find the epic number:
   - the epic that `speckit.roadmap.next` announced in this session, if specify used it;
   - otherwise, match the new spec's title to a `planned` roadmap entry by title similarity;
   - if no match is clear, ask the user which entry it is, or whether it is not on the roadmap (then
     stop without changing anything). Never guess.

4. Run:

   ```bash
   python3 .specify/extensions/roadmap/scripts/set_status.py <roadmap_path> --number NNN --status specced --spec-dir <feature dir>
   ```

5. Report in one line: `Roadmap: epic NNN → specced (<feature dir>)`. The script is idempotent; "already
   specced" is a normal result.
