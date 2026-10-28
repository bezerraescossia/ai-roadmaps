---
id: E27
title: Data Pipeline & Feature Engineering
archetypes: [classical-ml, perception]
requires: core
applies_when: always
depends_on: [E17]
phase: build
---

## Description

Build the reproducible path from raw data to training and serving features.

## Outcome

Training datasets and serving features come from the same versioned definitions, are reproducible for any
past date, and are free of target leakage.

## Scope (in)

- Raw-to-clean data pipeline with data validation checks (schema, ranges, nulls, freshness).
- Feature definitions in code, versioned, with the same logic in training and serving.
- Point-in-time correct joins, so a training row uses only data available at its prediction time.
- Train, validation and test split strategy that matches how the model will be used (time-based for
  forecasting or drifting data, grouped by entity when rows are not independent).
- Dataset versioning: any model can be traced to the exact data and feature versions.
- Leakage review: each feature checked for information unavailable at prediction time.

## Scope (out)

- Model training (next epic).

## Decisions

- **Feature store or plain pipeline?** A feature store helps when many models or online serving share
  features; a plain versioned pipeline is enough for one batch model.
- **Select the data and pipeline stack.** Based on data size and the team's existing platform.

## Archetype notes

- **perception:** features mean preprocessing and transforms (resize, normalisation, audio resampling, spectrograms), identical in training and serving. Large media needs storage and versioning. Splits are grouped by source, so the same person, scene or session never appears in two splits.
