---
id: E2
title: Data Engineering
phase: data-engineering
depends_on: [E1]
weight: 3
loops_back_to: [E1]
---

## Description

Turn raw data into a clean, balanced, reproducible training set, and package the preparation as a pipeline
so it can be re-run for retraining.

## Outcome

Selected features, cleaned and balanced datasets, a reproducible transformation pipeline and data unit tests
are in place, and data that fails the quality requirements is discarded.

## Tasks

- Feature selection (filter, wrapper or embedded methods).
- Data selection.
- Class balancing (over- or under-sampling).
- Data cleaning: error detection and correction, imputation.
- Feature engineering, for example one-hot encoding, clustering, discretization.
- Data augmentation.
- Standardization and normalization.
- Execute the labeling plan from E1. `[labeled_data=no|partial]` (added)
- Split train, validation and test data in a way that prevents leakage, and version each split. (added)

## Outputs

- Selected features.
- Cleaned and balanced datasets.
- Data transformation pipelines.
- Data unit tests.

## Quality assurance

- **Risks:** errors propagate to later phases; classes are unbalanced; inputs are erroneous; features on a
  large scale bias the model.
- **Metrics:** data quality requirements, used to discard samples that do not meet them.
- **Mitigations:** unit tests for data; standardized inputs; normalization; reproducible preprocessing
  pipelines.

## Decisions

- **Select the data quality requirements** that a sample must meet.
- **Select the balancing and imputation strategy.**
- **Select the data and pipeline versioning approach.** (added)

## Loop-backs

- Back to E1 when the data turns out to be insufficient or unusable for the success criteria.

## Open questions

Filled from `unsure` intake answers; none by default.
