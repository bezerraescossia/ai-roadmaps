---
id: E13
title: Cost Management
archetypes: [llm-service, batch-pipeline, agent]
requires: core
applies_when: always
depends_on: [E02, E12]
phase: build
---

## Description

Token accounting and controls that keep unit economics viable.

## Outcome

Every request path records its cost, spend is visible by user, feature and model, and a pre-launch
monthly projection exists.

## Scope (in)

- Per-request cost accounting: tokens and cost for every request, including zero-cost cache hits.
- Cost aggregation by user, feature and model: totals, average cost per request, top consumers.
  [Checklist #10]
- Monthly cost projection before launch: DAU x requests per user x avg tokens x pricing x
  (1 - cache hit rate).
- Per-user budget enforcement (optional; `budget_control == yes`): route over-budget users to a cheaper
  model or limit usage.
- Emergency cost mode (optional; `budget_control == yes`): when daily spend exceeds a limit, cache-only
  for repeats, cheapest model, stricter input limits.

## Scope (out)

- Billing or chargeback to end customers.

## Decisions

- None; budgets and limits are set from the monthly projection.

## Archetype notes

- **batch-pipeline:** cost per item and per run. Projection = items per day x average tokens or pages x
  price. Per-user budgets do not apply; a per-run spend cap is the equivalent control.
- **agent:** per-run spend caps and step limits are the main controls; cost scales with the number of steps.
