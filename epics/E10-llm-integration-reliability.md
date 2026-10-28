---
id: E10
title: LLM Integration & Reliability
archetypes: [llm-service, batch-pipeline, agent]
requires: core
applies_when: always
depends_on: [E02]
phase: build
---

## Description

Provider integration and the three layers of error handling: API, model and application failures.

## Outcome

Any component can request a completion and get a uniform result, and provider failures degrade
gracefully instead of failing the request.

## Scope (in)

- Provider SDK integration with async clients for the selected provider(s).
- Retry with exponential backoff and jitter (course default: start 1s, double, max 3 retries).
  [Checklist #7]
- [cap: fallback-chain, tier: production] Fallback model chain: primary, alternative model(s), cached response, service-unavailable message.
  [Checklist #8]
- Timeouts on all external calls (course default 30s); on timeout retry once with a shorter prompt or
  smaller model. [Checklist #13]
- Malformed output self-correction: retry with the validation error in the prompt; fall back to raw text
  if still invalid.
- Graceful degradation of secondary systems: failures in cache, retrieval, tools or guardrail
  components never crash the main flow.
- Async I/O and connection pooling.
- Queue-based processing for long tasks (optional; applies when `long_tasks == yes`): queue
  non-real-time jobs for workers, return a job ID for polling.

## Scope (out)

- Routing decisions (Prompt Management & Routing) and cost recording (Cost Management).

## Decisions

- None beyond the model strategy recorded in the discovery epic.

## Archetype notes

- **batch-pipeline:** the queue-based processing story always applies (items are jobs); the queue and
  workers come from the ingestion epic. The fallback chain ends with "mark the item failed and route it to
  review", not a user-facing message. Timeouts and retries are per item.
- **agent:** reliability applies per step. A fallback model must still support the tool calling the agent needs. The queue-based processing story applies to long-running runs.
