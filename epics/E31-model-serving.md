---
id: E31
title: Model Serving & Release
archetypes: [classical-ml, perception, fine-tuning]
requires: core
applies_when: always
depends_on: [E30]
phase: build
---

## Description

Get predictions to the people and systems that use them, safely.

## Outcome

Predictions are delivered through the chosen mode within latency or schedule targets, and a new model
version is released gradually and can be rolled back.

## Scope (in)

- Serving contract: inputs, outputs, versioning, error handling.
- Batch scoring (when `serving` is `batch`): schedule, output table, idempotent reruns, backfill.
- Online serving (when `serving` is `online`): API with latency and throughput targets, autoscaling, input
  validation, a feature fetch path with the same definitions as training.
- Embedded or edge serving (when `serving` is `embedded`): packaging, size limits, update mechanism.
- [cap: canary-release, tier: critical] Safe release: shadow mode, then canary or A/B, compared on the success metric, with automatic rollback
  rules.
- Prediction logging with the model version, for monitoring and for later joining to outcomes.

## Scope (out)

- Monitoring and retraining (next epics).

## Decisions

- **Select the serving mode.** Options: batch scoring, online API, streaming, or embedded. Based on how
  fresh predictions must be, volume and who consumes them.
- **Select the serving stack.** Options: a model server, a managed endpoint, or a service embedding the
  model. Based on the existing platform and latency needs.

## Archetype notes

- **perception:** cloud serving covers GPU inference, batching and audio or video streaming; embedded serving is handled by Edge & Device Optimization.
- **fine-tuning:** use the `hosting` answer instead of `serving`. Hosted tuning endpoint (`api`): endpoint and version pinning, deprecation handling. Self-hosted (`self-hosted`): inference engine, GPU sizing, batching, autoscaling, adapter loading for several tenants. Compare latency, throughput and cost per request with the baseline, and release by shadow or canary against the previous model. Select the quantisation level from the quality loss measured by the harness.
