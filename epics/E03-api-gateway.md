---
id: E03
title: API Gateway & Service Endpoints
archetypes: [llm-service, agent]
requires: core
applies_when: always
depends_on: [E02]
phase: build
---

## Description

Entry point handling authentication, rate limiting, CORS and validation before any AI logic runs.

## Outcome

Every request is authenticated, validated, rate-limited and size-bounded before it reaches guardrails or
the model, and returns a request_id.

## Scope (in)

- Primary application endpoint(s) with a validated request schema and a response that includes
  request_id (e.g. POST /v1/chat).
- Authentication at the gateway, before guardrails or the model.
- Per-user rate limiting: 429 with a clear message; course default 10-50 req/min. [Checklist #2]
- CORS restricted to production domains and required methods. [Checklist #14]
- Input and output token limits per endpoint/template; reject or truncate oversized inputs.
  [Checklist #12]
- Internal ops endpoints for cost and cache statistics.

## Scope (out)

- Authorization to tools and per-role permissions (Tools & Integrations).

## Decisions

- None; the choices here are conventional.

## Archetype notes

- **agent:** applies when `interface` is not `background`; a background agent has a trigger, not an endpoint.
