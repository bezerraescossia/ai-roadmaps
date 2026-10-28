---
id: E12
title: Observability
archetypes: [llm-service, batch-pipeline, agent]
requires: core
applies_when: always
depends_on: [E02, E10]
phase: build
---

## Description

Logging, tracing and metrics so production issues can be diagnosed.

## Outcome

Every request leaves a structured record and a trace, and metric thresholds raise alerts.

## Scope (in)

- Structured logging with request IDs: one entry per request using the log schema. [Checklist #9]
- [cap: tracing, tier: production] Distributed tracing: each component (cache, guardrails, retrieval, tools, model call, cost) as a span,
  e.g. with OpenTelemetry.
- Core metrics dashboard with targets (course defaults: P50 < 2s, P99 < 10s, cache > 30%, blocks < 5%,
  cost < $0.01 per request).
- [cap: alerting, tier: production] Threshold alerting when metrics breach targets.

## Scope (out)

- Quality evaluation (Evaluation & Quality).

## Decisions

- None; the metric targets are set from the use case's success metrics.

## Archetype notes

- **batch-pipeline:** "request" means item or job. Metrics: items per hour, success and failure rate,
  review rate, queue depth and oldest-item age, cost per item, pipeline version. Alerts on backlog age and
  failure spikes replace latency percentiles.
- **agent:** trace every run as a tree of steps and keep redacted prompts and tool inputs and outputs, so a failed run can be replayed.
