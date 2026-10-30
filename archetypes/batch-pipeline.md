---
archetype: batch-pipeline
title: Batch / document-processing pipeline
description: An offline or scheduled pipeline that processes many items (documents, emails, records) with an LLM, rules or a model, stores structured results, and delivers them downstream. No interactive end user.
library_version: 0.9.0
source: drafted from general practice and reuse of the llm-service epics; to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: batch / document-processing pipeline

Use when AI processes items in volume without a user waiting: invoice or contract extraction, ticket
classification, enrichment of records, summarisation of reports. Throughput, cost per item, idempotency
and review of low-confidence results matter more than latency.

Not for an interactive chat or API (use `llm-service`) and not for a model you train (use `classical-ml`).

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: use_case
    ask: What is extracted, classified or generated, for which downstream use, and what does a wrong result cost?
    feeds: Vision & End States
  - id: input_docs
    ask: Are the inputs files that need parsing (PDF, scans, email, office documents) rather than structured records?
    values: [yes, no]
  - id: scanned
    ask: Are many documents scans or photos that need OCR?
    values: [yes, no]
  - id: arrival
    ask: How do items arrive?
    values: [continuous, scheduled, one-off]
  - id: volume
    ask: How many items per day, how large is each, and is there a one-off backlog to process?
    feeds: Constraints & Decisions; sizes the throughput epic
  - id: approach
    ask: Which method do you expect?
    values: [llm, rules, ml, hybrid, unsure]
    feeds: Open Question on the extraction spec when `unsure`
  - id: human_review
    ask: Must a person check low-confidence or high-stakes results?
    values: [yes, no, unsure]
  - id: labeled_data
    ask: Do you have examples with the correct output for a sample of items?
    values: [yes, partial, no]
  - id: sensitive_data
    ask: Do items contain personal or regulated data that must be redacted or kept inside your environment?
    values: [yes, no]
  - id: constraints
    ask: Fixed technology, hosting, provider, deadline or budget constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `scanned` is only asked when `input_docs` is `yes`.
- `arrival: continuous` adds watch or poll logic and a dead-letter queue to the ingestion spec;
  `one-off` removes the schedule and keeps the backfill plan.
- `human_review: unsure` includes the review epic as `undecided` with an Open Question.
- `approach: ml` or `hybrid` with a model you train or adapt yourself: ask which kind and include that
  archetype (see "Included archetypes"). Add an Open Question on the Extraction spec about how the model is
  called from the pipeline.

## Epic overrides

Shared epics behave differently here (see each epic's "Archetype notes"). The overrides below replace the
epic's own `applies_when` and `depends_on` for this archetype.

```yaml
epic_rules:
  E02: {depends_on: [E16]}
  E09: {applies_when: "sensitive_data == yes", depends_on: [E10]}
  E10: {depends_on: [E02]}
  E12: {depends_on: [E02, E10]}
  E13: {depends_on: [E02, E12]}
  E14: {depends_on: [E02, E17]}
  E23: {depends_on: [E21, E10, E14]}
  E24: {depends_on: [E23]}
  E15: {depends_on: [E10, E12, E64]}
```

## Bundles

`E16` is discovery and never becomes a spec. A bundle with no selected members is omitted.

```yaml
bundles:
  - title: Serving contract & stub
    members: [E64]
  - title: Data assessment
    members: [E17]
  - title: Foundation
    members: [E02]
  - title: LLM integration & reliability
    members: [E10]
  - title: Ingestion & orchestration
    members: [E21]
  - title: Document parsing
    members: [E22]
  - title: Evaluation & quality
    members: [E14]
  - title: Extraction & classification
    members: [E23]
  - title: Guardrails
    members: [E09]
  - title: Review loop
    members: [E24]
  - title: Results & delivery
    members: [E25]
  - title: Observability & cost
    members: [E12, E13]
  - title: Throughput & backfill
    members: [E26]
  - title: Deployment & launch readiness
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
    consumed_by: [E23]
  perception:
    consumed_by: [E23]
  fine-tuning:
    consumed_by: [E10]
```

## Ordering

A bundle depends on the bundles of its members' `depends_on`; `after` is a soft ordering that applies only
when both epics are selected. Specs are sorted topologically (ties broken by phase, then epic id) and
numbered 001..N. Evaluation sorts before Extraction because the evaluation set is a prerequisite for
tuning it.

## Conflicts

If a selected epic needs an unselected one (for example extraction without the evaluation epic), warn, name
the dependency and why it exists, and let the user decide. Record the outcome as `deferred` or `abandoned`
with the reason.
