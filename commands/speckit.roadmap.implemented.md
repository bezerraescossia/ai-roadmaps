---
description: Mark the roadmap epic that was just implemented as `implemented` (or `in-progress` when tasks remain) and offer a debrief (runs automatically after implement).
scripts:
  sh: .specify/extensions/roadmap/scripts/bash/load-config.sh
---

## User Input

```text
$ARGUMENTS
```

## Goal

Advance the roadmap after `/speckit-implement`. The status is derived from `tasks.md`, not from your
judgment: all tasks checked → `implemented`, otherwise `in-progress`.

## Outline

1. Run `{SCRIPT}` and parse `roadmap_path` and `roadmap_exists`. If there is no roadmap, stop silently.

2. Find the feature directory: `feature_directory` in `.specify/feature.json`; otherwise ask.

3. Run:

   ```bash
   python3 .specify/extensions/roadmap/scripts/set_status.py <roadmap_path> --spec-dir <feature dir> --auto
   ```

   - Exit 0: report the new status in one line.
   - Exit 2 (no entry has this spec dir): match the spec to a roadmap entry by title similarity; if clear,
     run `set_status.py <roadmap_path> --number NNN --status <implemented|in-progress> --spec-dir <feature dir>`
     (use `implemented` only if `tasks.md` has no unchecked tasks). If unclear, ask; never guess.

4. If the status became `implemented`, offer: "Check the implementation against the roadmap now
   (`/speckit-roadmap-debrief`)?" If it became `in-progress`, say how many tasks remain.
