---
id: E59
title: CI/CD for ML
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E56, E57]
phase: build
---

## Description

Automated, gated release of pipeline code, models and infrastructure.

## Outcome

Changes are tested, evaluated against gates, and promoted between environments automatically, with automated rollback.

## Scope (in)

- CI for pipeline and model code: unit, data and integration tests, linting.
- Automated evaluation gates before a model is promoted.
- Automated deployment of models and infrastructure, with promotion across environments.
- Automatic rollback trigger, calling the release strategies of Model Serving Infrastructure.
- Pipeline-as-code templates.
- Supply-chain controls: dependency scanning, image signing.

## Scope (out)

- Model monitoring (Monitoring & Observability).

## Decisions

- **Select the CI system and the gating policy.** What must pass for each risk tier.
