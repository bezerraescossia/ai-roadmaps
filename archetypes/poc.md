---
archetype: poc
title: AI feasibility study / proof of concept
description: A short, timeboxed spike that answers "does this work well enough to be worth building?" and ends in a go / no-go with a recommended production archetype.
library_version: 0.7.0
source: drafted from general practice; to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: AI feasibility study / proof of concept

Use when the question is whether an AI approach is feasible and worth funding, not how to run it in
production. It is usually 2 to 6 weeks and its main deliverable is a decision. The follow-on production
project gets its own roadmap, from another archetype, using the recommendation in the last epic.

Not for a project that already has a decided approach and needs building.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: use_case
    ask: What problem does this solve, for whom, and what decision or workflow would the output change?
    feeds: Vision & End States
  - id: solution_type
    ask: Which kind of solution do you expect to try?
    values: [llm, classical-ml, batch-extraction, unsure]
    feeds: Notes on the prototype spec; shapes the recommendation in the go/no-go spec
  - id: labeled_data
    ask: Do you already have examples with the correct answers (labels, past decisions, reference outputs)?
    values: [yes, partial, no]
  - id: sensitive_data
    ask: Which sensitive data or regulatory limits apply, and may the data leave your environment?
    feeds: Constraints & Decisions
  - id: timebox
    ask: How long does the spike run, and who decides go / no-go?
    feeds: Constraints & Decisions
  - id: constraints
    ask: Fixed technology, provider, budget or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- All POC epics always apply; there are no optional epics.
- `solution_type: unsure` is fine: the prototype spec gets an Open Question about which approaches to try.
- `labeled_data` `no` or `partial` adds the labeling plan to the data assessment.

## Bundles

`E16` is discovery and never becomes a spec.

```yaml
bundles:
  - title: Data assessment
    members: [E17]
  - title: Prototype & baseline
    members: [E18]
  - title: Feasibility evaluation
    members: [E19]
  - title: Go / no-go & production estimate
    members: [E20]
```

## Ordering

The same rules as the other archetypes: a bundle depends on the bundles of its members' `depends_on`,
specs are sorted topologically (ties broken by phase, then epic id) and numbered 001..N. For this archetype
the order is a straight line.

## Conflicts

Dropping an epic breaks the chain (a prototype cannot be evaluated without data, a decision cannot be made
without results). Warn, name the dependency, and let the user decide; record any dropped epic as
`deferred` or `abandoned` with the reason.
