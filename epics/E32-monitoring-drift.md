---
id: E32
title: Monitoring & Drift Detection
archetypes: [classical-ml, perception, fine-tuning]
requires: core
applies_when: always
depends_on: [E31]
phase: harden
---

## Description

Know when the model in production stops working, before users do.

## Outcome

Serving health, input data, predictions and (when available) real outcomes are monitored, with alerts
tied to the success metrics.

## Scope (in)

- Serving health: latency, error rate, throughput, freshness of batch outputs.
- Data drift and data quality: input distributions and missing values against the training data.
- Prediction drift: distribution of the model's outputs over time.
- Performance tracking: join predictions to actual outcomes as they arrive, and compute the metrics
  from the framing epic; define how long labels take to arrive and what to watch in the meantime.
- Alert thresholds, an owner and a runbook for each alert.
- Dashboard shared with the business owner.

## Scope (out)

- Automatic retraining (next epic).

## Decisions

- **Select the monitoring tooling.** Options: an ML monitoring tool (Evidently, WhyLabs and similar), the
  existing observability stack, or custom jobs. Based on what the team already runs.

## Archetype notes

- **perception:** monitor input media statistics (brightness, noise, resolution, language or accent mix), the confidence distribution, and human-reviewed samples.
- **fine-tuning:** applies when `continuous` is `yes`. Monitor production quality against the harness metrics, drift of inputs against the training distribution, latency and cost, and a plan for base-model deprecation.
