---
id: E56
title: Experiment Tracking & Model Registry
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E54]
phase: build
---

## Description

One place to record experiments and to version, approve and promote models.

## Outcome

Every experiment and model version is recorded with its code, data and metrics, and models move through defined stages with approvals.

## Scope (in)

- Tracking: parameters, metrics, artefacts, code and data versions.
- Registry: versions, stages, approval workflow and lineage.
- Model card and metadata standard.
- Search and comparison.
- Retention and cleanup.
- Integration with pipelines and serving.

## Scope (out)

- Pipeline execution (Training & Pipeline Orchestration).

## Decisions

- **Select the tracking and registry tool.** Options: MLflow, Weights & Biases, a cloud-native service.
