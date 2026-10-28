---
id: E58
title: Model Serving Infrastructure
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E54, E56]
phase: build
---

## Description

A shared way to serve models in batch and online, safely and at an agreed service level.

## Outcome

Teams deploy a registered model to a versioned endpoint or batch job with autoscaling, safe release and an SLO.

## Scope (in)

- Batch scoring service.
- Online serving with autoscaling and versioned endpoints.
- [cap: platform-release-strategies, tier: critical] Release strategies: shadow, canary, A/B and rollback.
- [cap: gpu-sharing, tier: critical] Multi-model hosting and GPU sharing.
- LLM serving (only when `llmops` is `yes`): inference engine, batching, token-based autoscaling.
- SLOs per endpoint and a request and response logging standard.
- Authentication and network security.

## Scope (out)

- Model-specific optimisation owned by the model team.

## Decisions

- **Select the serving stack.** For example KServe, Seldon, BentoML, a managed endpoint service.
