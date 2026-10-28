---
id: E30
title: Model Registry & Versioning
archetypes: [classical-ml, perception, fine-tuning]
requires: core
applies_when: always
depends_on: [E29]
phase: build
---

## Description

Keep every released model traceable and promotable through defined stages.

## Outcome

Each model version is stored with its data, features, code, metrics and approval state, and serving
loads only approved versions.

## Scope (in)

- Registry entry per model version: artefact, training data and feature versions, code commit,
  metrics, evaluation report, owner.
- Stages (candidate, staging, production, archived) with an approval step for promotion.
- [cap: model-lineage, tier: critical] Lineage: from any production prediction back to the model and its training data.
- [cap: model-card, tier: production] Model card: purpose, intended use, data, metrics, limitations.
- Rollback to the previous production version in one step.

## Scope (out)

- Serving infrastructure (next epic).

## Decisions

- **Select the registry.** Options: MLflow registry, a cloud model registry, or artefacts in object
  storage with a manifest. Based on the existing platform.

## Archetype notes

- **perception:** the registry stores the preprocessing configuration and label schema with the model; artefacts are large.
- **fine-tuning:** adapters or merged weights, tokenizer and configuration are the artefacts; the registry entry records the training data, hyperparameters and the harness metrics; quantised variants are separate versions that must pass the harness again.
