---
archetype: classical-ml
title: Classical ML / predictive model
description: A model you train on your own data for a defined prediction task (classification, regression, ranking, forecasting, anomaly detection, recommendation), then serve, monitor and retrain.
exposes: E31
library_version: 0.9.0
source: drafted from general practice (CRISP-ML(Q), MLOps maturity models); to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: classical ML / predictive model

Use when the product is a model trained on your data: churn, demand forecasting, fraud or anomaly
detection, ranking, recommendation, tabular classification. Data quality, evaluation rigour, safe release
and drift matter most.

Not for prompting a hosted LLM (use `llm-service`) and not for large-model fine-tuning (a separate
archetype). In an `llm-service`, `agent` or `batch-pipeline` project that needs its own model, include this archetype in
that project's roadmap (see their "Included archetypes"); several models can each be included.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: use_case
    ask: What is predicted, who uses the prediction, what action does it trigger, and what does a wrong prediction cost?
    feeds: Vision & End States
  - id: task_type
    ask: What kind of prediction is it (classification, regression, ranking, forecasting, anomaly detection, other)?
    feeds: Notes and Open Questions on the training spec
  - id: labeled_data
    ask: Do you already have historical examples with the true outcome?
    values: [yes, partial, no]
  - id: serving
    ask: How are predictions consumed?
    values: [batch, online, embedded, unsure]
  - id: regulated
    ask: Do predictions affect people, or does a regulation require explanations, fairness checks or audit?
    values: [yes, no, unsure]
  - id: label_delay
    ask: How long after a prediction is the true outcome known?
    feeds: Notes on the monitoring spec
  - id: ml_platform
    ask: Is there an existing ML or data platform (feature store, registry, orchestrator) to build on?
    feeds: Constraints & Decisions
  - id: constraints
    ask: Fixed technology, hosting, budget or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `serving: unsure` leaves the serving-mode bullets out and adds an Open Question on the serving spec.
- `regulated: unsure` includes the explainability epic as `undecided`.
- `labeled_data` `no` or `partial` adds the labeling plan to the data assessment.

## Epic overrides

```yaml
epic_rules:
  E15: {depends_on: [E31, E32]}
```

## Bundles

`E16` is discovery and never becomes a spec. A bundle with no selected members is omitted.

```yaml
bundles:
  - title: Serving contract & stub
    members: [E64]
  - title: Data assessment
    members: [E17]
  - title: Data & feature pipeline
    members: [E27]
  - title: Baseline & training
    members: [E28]
  - title: Offline evaluation
    members: [E29]
  - title: Model registry
    members: [E30]
  - title: Serving & release
    members: [E31]
  - title: Monitoring & drift
    members: [E32]
  - title: Retraining & delivery
    members: [E33]
  - title: Explainability & compliance
    members: [E34]
  - title: Deployment & launch readiness
    members: [E15]
```

## Ordering

A bundle depends on the bundles of its members' `depends_on`. Specs are sorted topologically (ties broken
by phase, then epic id) and numbered 001..N. The result is close to a straight line from data to launch,
with monitoring, retraining and compliance after the first release.

## Conflicts

If a selected epic needs an unselected one, warn, name the dependency and why it exists, and let the user
decide (for example retraining without monitoring has no trigger). Record the outcome as `deferred` or
`abandoned` with the reason.
