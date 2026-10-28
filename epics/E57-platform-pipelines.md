---
id: E57
title: Training & Pipeline Orchestration
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E54, E55, E56]
phase: build
---

## Description

Run training, evaluation and batch scoring as reproducible, scheduled, observable pipelines.

## Outcome

Teams start from pipeline templates, runs are reproducible and cached, and failures notify the owner.

## Scope (in)

- Workflow engine and its operation.
- Pipeline templates for common tasks.
- Scheduling and triggers.
- [cap: distributed-training, tier: critical] Distributed training support.
- Step caching and lineage between steps.
- Resource requests and limits per step.
- Failure handling and notifications; reproducible re-runs.

## Scope (out)

- CI/CD for releasing pipelines and models (CI/CD for ML).

## Decisions

- **Select the workflow engine.** Options: Airflow, Kubeflow Pipelines, Dagster, Prefect, Metaflow, a cloud-native service.
