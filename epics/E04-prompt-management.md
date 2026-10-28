---
id: E04
title: Prompt Management & Routing
archetypes: [llm-service]
requires: core
applies_when: always
depends_on: [E02, E14]
phase: build
---

## Description

Versioned prompts, routing to the right template, and safe experimentation.

## Outcome

Prompts are versioned in source control, each request is routed to the right template, and a prompt
change can be rolled out gradually and rolled back in one step.

## Scope (in)

- Versioned prompt template registry: name, version, variables, default model and output limit, in
  version control.
- Prompt router: select a template by request type, user context and experiment assignment.
- [cap: ab-experiments, tier: production] Deterministic experiment assignment: hash(user_id + experiment) mod 100, so each user sees a
  consistent variant.
- One-step manual rollback to the previous prompt version.
- [cap: prompt-auto-revert, tier: critical] Automatic revert when a new version regresses (course example: 2x error rate over
  100 requests).

## Scope (out)

- Learned or trained routers.

## Decisions

- **Select prompt rollout strategy.** Options: shadow mode (run on all traffic, log only), percentage
  rollout (e.g. 10/25/50/100%), or both. Define promotion criteria.
