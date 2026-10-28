---
id: E14
title: Evaluation & Quality
archetypes: [llm-service, batch-pipeline, agent]
requires: core
applies_when: always
depends_on: [E16, E02]
phase: build
---

<!-- Ordering note: the course lists this epic late, but the golden dataset and eval criteria are
     prerequisites for prompt changes (E04) and retrieval work (E06), so both depend on it. The first CI
     eval gate may still be phased in with the first spec that has evaluable behavior. -->

## Description

Measure output quality before and after release, tied to prompt and model versions.

## Outcome

Quality is measured against a golden dataset in CI, tracked online per prompt/model version, and
failures feed back into the dataset.

## Scope (in)

- Evaluation criteria and golden dataset: representative inputs with expected outputs or grading
  rubrics.
- Offline eval suite in CI: automated evals (metrics and/or LLM-as-judge) that gate prompt, model and
  retrieval changes.
- [cap: online-eval-logging, tier: critical] Online eval logging: per-request quality signals with template version and model.
- [cap: feedback-capture, tier: production] User feedback capture: ratings/corrections linked to request IDs, failures fed back into the golden
  dataset.
- [cap: quality-by-version, tier: critical] Quality metrics per version: latency, ratings and error rate per prompt/model version.

## Scope (out)

- Human annotation program beyond feedback capture.

## Decisions

- **Evaluation method.** Metrics, LLM-as-judge, or both; chosen from the use case's success metrics.

## Archetype notes

- **batch-pipeline:** the golden dataset comes from the ground truth identified in the data assessment.
  Score extraction per field (precision, recall) and classification per class. Gate changes to parser,
  prompt or model on a regression set. Online signals are reviewer corrections and sampled audits of
  auto-accepted items.
- **agent:** evaluate whole-run outcomes on golden tasks (task success rate), tool-call correctness and trajectory quality (efficiency, unnecessary steps). Use simulated environments or recorded tool responses for repeatability, and gate prompt, model and tool changes on the suite.
