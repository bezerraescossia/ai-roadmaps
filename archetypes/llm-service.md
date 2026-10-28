---
archetype: llm-service
title: Production LLM service (optional RAG, tools, custom ML, streaming)
description: A request/response service built on a hosted or self-hosted LLM, possibly with retrieval, tools, a custom model and streaming.
library_version: 0.7.0
source: course template "ai_app_template" (15 epics)
phases: [discover, build, harden, launch]
---

# Archetype: production LLM service

Use when the project is a request/response service built on a hosted or self-hosted LLM, possibly with
retrieval, tools, a custom model and streaming. Not for batch pipelines, training/fine-tuning projects
or classical-ML-only work (other archetypes).

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate. Variables feed
the `applies_when` field of the epics.

```yaml
intake:
  - id: use_case
    ask: What problem does this solve, and for whom? What measurable outcome counts as success?
    feeds: Vision & End States
  - id: rag
    ask: Must answers be grounded in the project's own data (documents, databases)?
    values: [yes, no, unsure]
  - id: tools
    ask: Must the model call external systems (APIs, databases, other models) or take actions?
    values: [yes, no, unsure]
  - id: custom_ml
    ask: Does the product need a model you train or adapt yourself besides calling an LLM (a classical ML model, a vision or speech model, a fine-tuned LLM)?
    values: [yes, no, unsure]
  - id: streaming
    ask: Do users read answers as they are generated (chat UI)?
    values: [yes, no, unsure]
  - id: caching
    ask: Will many requests repeat or be near-duplicates, so caching can cut cost or latency?
    values: [yes, no, unsure]
  - id: human_review
    ask: Must a person review some answers (flagged, high-risk or low-confidence ones) before or after they reach users?
    values: [yes, no, unsure]
  - id: long_tasks
    ask: Are there non-real-time jobs (e.g. summarising large documents) that should run in a queue?
    values: [yes, no]
  - id: budget_control
    ask: Is per-user budget enforcement or an emergency cost mode needed?
    values: [yes, no]
  - id: self_hosted
    ask: Will models run on your own infrastructure?
    values: [yes, no, unsure]
  - id: sensitive_data
    ask: Which sensitive data or regulatory limits apply, and what is the impact of a wrong or unsafe answer?
    feeds: Constraints & Decisions; informs Guardrails
  - id: constraints
    ask: Fixed technology, hosting or provider decisions already made?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `unsure` on an optional epic: include the epic with status `undecided` and add an Open Question.
- Answers that are decisions (a chosen provider, store, protocol) become `C-nn` constraints.
  Decisions the user has not made stay as Open Questions (`Qn`) on the epic that owns them.
- `custom_ml: yes`: ask which kind of model (see "Included archetypes") and include that archetype in this
  roadmap. Add an Open Question on the Tools spec (on the Foundation spec if there is none): how is the model
  integrated (a tool, a fixed pipeline step before the LLM, or precomputed results)? Several models of
  different kinds can be included. `unsure` adds the same Open Question as undecided and includes nothing.

## Bundles

A bundle becomes **one Planned Spec**. A bundle includes only its member epics that were selected; a
bundle with no selected members is omitted. `E16` is discovery and never becomes a spec. Bundle
titles and member lists reproduce the grouping used in `llm-production-app` and may be changed per
project.

```yaml
bundles:
  - title: Foundation
    members: [E02, E03, E11]
  - title: LLM gateway
    members: [E10]
  - title: Cost tracker + eval logger
    members: [E12, E13]
  - title: Knowledge base + RAG
    members: [E06]
  - title: Guardrails
    members: [E09]
  - title: Prompt router
    members: [E04]
  - title: Semantic cache
    members: [E05]
  - title: Tools
    members: [E07]
  - title: Human review
    members: [E24]
  - title: Evaluation & quality
    members: [E14]
  - title: Ops hardening & launch
    members: [E15]
```

## Included archetypes

When the project also builds a model of another kind, include that archetype in the same roadmap instead of
starting a second one. Ask the included archetype's intake (skip `constraints`, already answered; read
`use_case` as the model's purpose) and run the planner with `--include`. The included archetype's serving
epic (its `exposes` epic) is ordered before each epic listed in `consumed_by`.

```yaml
includes:
  classical-ml:
    consumed_by: [E07]
  perception:
    consumed_by: [E07]
  fine-tuning:
    consumed_by: [E10]
```

## Ordering

1. A bundle's `depends_on` is the union of its members' `depends_on`, mapped to bundles, minus itself.
2. Sort bundles topologically; ties are broken by the earliest member `phase`
   (discover, build, harden, launch) and then by epic id.
3. Number the specs 001..N in that order.
4. `E14` is a prerequisite of `E04` and `E06`, so the Evaluation bundle sorts before the prompt router
   and the knowledge base. The first CI eval gate can still be phased in with the first spec that has
   evaluable behavior; the roadmap notes this under Cross-Cutting Notes.

## Conflicts

If the dependency graph shows a selected epic requiring an unselected one (e.g. RAG selected while the
evaluation epic is dropped), warn, name the dependency and why it exists, and let the user decide. Record
the outcome as a `deferred` or `abandoned` entry with the reason, and note it in the Sync Impact Report.
