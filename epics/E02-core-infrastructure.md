---
id: E02
title: Core Infrastructure & Configuration
archetypes: [llm-service, batch-pipeline, agent]
requires: core
applies_when: always
depends_on: [E16]
phase: build
---

## Description

Shared foundation: configuration, model registry, pricing and the request log schema.

## Outcome

The service starts from environment-based configuration, refuses unknown models, and defines the
per-request record every later epic writes to.

## Scope (in)

- Model registry and pricing table: supported models with input/output price per 1M tokens; unknown
  model configuration fails at startup with a clear error.
- Environment-based configuration and secrets: API keys only in env vars or a secrets manager, never in
  code. [Checklist #1]
- Structured request log schema: request_id, user_id, timestamp, template, template version, model,
  input/output tokens, latency, cache hit, guardrail results, cost, error.

## Scope (out)

- Writing and querying the records (Observability, Cost Management).

## Decisions

- None; the choices here are conventional.

## Archetype notes

- **batch-pipeline:** the request log becomes a per-item record: item_id, source key, pipeline version,
  model, input/output tokens, latency, status, confidence, cost, error. Pricing is per item or page.
- **agent:** the request log becomes a per-run record plus a per-step trace: run_id, step, tool, model, tokens, latency, cost, status.
