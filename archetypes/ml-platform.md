---
archetype: ml-platform
title: ML platform / MLOps foundation
description: The shared platform that ML teams build on (environments and compute, data and features, tracking and registry, pipelines, serving, CI/CD, monitoring, governance, adoption). The users are internal practitioners.
library_version: 0.7.0
source: drafted from general practice (MLOps maturity models); to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: ML platform / MLOps foundation

Use when the product is the platform itself and its users are your own data scientists and ML engineers:
a standard way to get from a notebook to a monitored model in production. Adoption and developer experience
matter as much as the technology, so the roadmap ends with a pilot team.

Not for a single model or application (use `classical-ml`, `perception`, `llm-service` or the others);
those roadmaps may sit on top of a platform that this archetype builds.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: goal
    ask: Why a platform now, and what hurts today (environments, deployments, reproducibility, GPU access, governance)?
    feeds: Vision & End States
  - id: users
    ask: Which teams and how many practitioners will use it, and how many models are in production or planned?
    feeds: Constraints & Decisions; sizes the adoption spec
  - id: maturity
    ask: Where is the practice today?
    values: [ad-hoc, repeatable, automated]
    feeds: Notes on every spec
  - id: cloud
    ask: Which cloud or on-premises environment, and which platform services are already in use?
    feeds: Constraints & Decisions
  - id: feature_store
    ask: Do several models or online use cases need shared features?
    values: [yes, no, unsure]
  - id: llmops
    ask: Will teams build LLM applications on this platform?
    values: [yes, no, unsure]
  - id: regulated
    ask: Do regulations or internal policy require model documentation, approvals or audit?
    values: [yes, no, unsure]
  - id: existing_tools
    ask: Which tools already exist (tracking, registry, orchestrator, serving) and must be kept or replaced?
    feeds: Constraints & Decisions (build versus buy)
  - id: constraints
    ask: Fixed budget, team size, security or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `feature_store` `no` removes the feature-store bullet; `unsure` leaves it out and adds an Open Question.
- `llmops: yes` includes the LLMOps epic and the LLM-serving bullet; `unsure` includes the epic as
  `undecided`.
- `regulated: yes` adds the compliance mapping bullet to Governance.
- Existing tools become constraints; build versus buy decisions from the scope epic are recorded as `C-nn`.

## Bundles

`E53` is discovery and never becomes a spec. A bundle with no selected members is omitted.

```yaml
bundles:
  - title: Compute & environments
    members: [E54]
  - title: Data & feature platform
    members: [E55]
  - title: Tracking & registry
    members: [E56]
  - title: Pipelines & orchestration
    members: [E57]
  - title: Model serving
    members: [E58]
  - title: CI/CD for ML
    members: [E59]
  - title: Monitoring platform
    members: [E60]
  - title: Governance & security
    members: [E61]
  - title: LLMOps extensions
    members: [E63]
  - title: Developer experience & adoption
    members: [E62]
```

## Ordering

A bundle depends on the bundles of its members' `depends_on`. Specs are sorted topologically (ties broken
by phase, then epic id) and numbered 001..N. Compute and environments come first; developer experience and
the pilot come last, since they need the capabilities in place.

## Conflicts

If a selected epic needs an unselected one, warn, name the dependency and why it exists, and let the user
decide. Record the outcome as `deferred` or `abandoned` with the reason.
