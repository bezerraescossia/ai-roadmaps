---
id: E42
title: Training Data Curation & Preparation
archetypes: [fine-tuning]
requires: core
applies_when: always
depends_on: [E41]
phase: build
---

## Description

Build the training dataset: sourced with rights, cleaned, formatted, and separated from the evaluation data.

## Outcome

A versioned, documented training set and frozen train, validation and test splits that share no items.

## Scope (in)

- Sources and rights: licences, consent, terms of providers whose model outputs are used, personal data.
- Collection and cleaning: deduplication, quality filtering, language and length checks.
- Formatting: instruction or chat templates, preference pairs, special tokens.
- Synthetic data generation (if used) with verification of the generated examples.
- Decontamination: remove evaluation items and near-duplicates from the training data.
- Splits frozen before any training run.
- Dataset versioning and a datasheet describing sources, filters and known gaps.
- Quality check of labels or demonstrations by sampling.

## Scope (out)

- Large-scale annotation programmes (see the labeling epic of other archetypes).

## Decisions

- **How much synthetic data, if any?** Based on how many real examples exist and how well synthetic ones can be verified.
- **How strict is quality filtering?** Fewer, cleaner examples usually beat more, noisier ones; confirm on the validation set.
