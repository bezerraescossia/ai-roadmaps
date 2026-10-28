---
id: E33
title: Retraining & Continuous Delivery
archetypes: [classical-ml, perception, fine-tuning]
requires: core
applies_when: always
depends_on: [E29, E30, E32]
phase: harden
---

## Description

Refresh the model on a defined trigger and ship it through an automated, gated path.

## Outcome

The training pipeline reruns on schedule or on a drift trigger, new candidates pass the same evaluation
gate as the first model, and approved ones are released with the usual safeguards.

## Scope (in)

- Retraining triggers: calendar, drift or performance alert, new-data volume.
- Automated pipeline: data validation, features, training, evaluation, registry entry.
- Evaluation gate: the candidate must beat or match the production model on the release thresholds and
  the slice floors, or it is not promoted.
- CI for the pipeline code and tests for the data and feature logic.
- Release through the serving epic's safe-release path; documented rollback.
- Cost and compute budget for retraining.

## Scope (out)

- Online learning or continual training without review.

## Decisions

- **Select the retraining cadence and trigger.** Based on how fast the data drifts and how much a stale
  model costs.

## Archetype notes

- **perception:** retraining uses newly labeled hard cases (active learning); the gate is the same per-condition floors as the release.
- **fine-tuning:** applies when `continuous` is `yes`. Feedback (ratings, corrections, preference signals) flows into data curation; a retrained model must pass the evaluation harness and the safety checks before release.
