---
id: E60
title: Monitoring & Observability Platform
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E58]
phase: harden
---

## Description

Monitoring that every model gets by default: service health, data drift, prediction drift and performance.

## Outcome

Each deployed model has dashboards and alerts for health, drift and quality, with a runbook and an owner.

## Scope (in)

- Service metrics for every endpoint.
- Data and prediction drift monitoring as a reusable service.
- Performance monitoring joining predictions to delayed outcomes.
- Logging standards.
- Alerting and on-call runbooks.
- Dashboards per model and per team; cost metrics per model.

## Scope (out)

- Model-specific business dashboards.

## Decisions

- **Select the monitoring tooling.** Reuse the existing observability stack, add an ML monitoring tool, or build.
