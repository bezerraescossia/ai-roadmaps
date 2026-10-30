---
archetype: traditional-ml
title: Traditional Machine Learning Algorithms
description: A model you train on your own data for a defined prediction task (classification, regression, ranking, forecasting, anomaly detection), then deploy, monitor and maintain, following CRISP-ML(Q).
library_version: 1.0.0
source: https://ml-ops.org/content/crisp-ml
methodology: CRISP-ML(Q)
---

# Archetype: traditional machine learning algorithms

Use when the product is a model trained on your own data with classical algorithms (linear models, tree
ensembles, clustering, classical time-series methods): churn, demand forecasting, fraud or anomaly
detection, ranking, tabular classification.

The roadmap follows CRISP-ML(Q), the quality-assured machine learning lifecycle. There is one epic per
phase and each epic becomes one spec. Tasks, outputs and quality assurance in the epics come from the
methodology; anything marked `(added)` is this library's own addition.

## Phases and epics

All six epics are always in the roadmap. They run in order; `loops_back_to` records where the methodology
sends you back, and never blocks.

| Epic | Phase | Depends on | Loops back to | Weight |
|---|---|---|---|---|
| E1 | Business & Data Understanding | none | none | 2 |
| E2 | Data Engineering | E1 | E1 | 3 |
| E3 | ML Model Engineering | E2 | E2 | 4 |
| E4 | ML Model Evaluation | E3 | E3, E2 | 2 |
| E5 | Deployment | E4 | E4 | 3 |
| E6 | Monitoring & Maintenance | E5 | E2, E3, E4 | 2 |

`weight` is a relative size, proportional between epics and not an estimate. It only draws the bars of the
Gantt chart that `plan.py` generates; the project can override it at intake.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate. Answers never
include or exclude an epic; they tailor the items inside the epics (see Rules).

```yaml
intake:
  - id: use_case
    ask: What is predicted, who uses the prediction, what action does it trigger, and what does a wrong prediction cost?
    feeds: Vision & End States, and the success criteria of E1
  - id: task_type
    ask: What kind of prediction is it (classification, regression, ranking, forecasting, anomaly detection, other)?
    values: [classification, regression, ranking, forecasting, anomaly-detection, other]
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
    feeds: Notes on E6
  - id: constraints
    ask: Fixed technology, hosting, existing ML or data platform, budget or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

## Rules

Epic items tagged with an intake variable, such as `[serving=online]`, appear as ordinary items when the
answer matches. When it does not match, the item stays and is recorded as `not applicable: <reason>`, so the
roadmap shows a deliberate choice. An `unsure` answer keeps the item and adds an Open Question on the spec.

- `task_type` sets the candidate algorithm families and metrics in E3 and the metric of E1's success criteria.
- `labeled_data` `no` or `partial` adds a labeling plan to E2.
- `serving` sets the inference hardware and rollout items in E5; `serving: unsure` adds an Open Question to E5.
- `regulated` `yes` turns on the explainability, fairness and compliance items in E4 and the governance
  item in E5; `no` marks them not applicable; `unsure` keeps them and adds an Open Question to E4.
- `label_delay` sets how E6 measures performance: a long delay means drift proxies instead of live accuracy.
- `constraints` become `C-nn` entries governing every spec they touch.
