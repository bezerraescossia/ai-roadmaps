---
id: E50
title: Augmentation & Condition Coverage
archetypes: [perception]
requires: core
applies_when: always
depends_on: [E49]
phase: build
---

## Description

Make the model robust to the variation it will meet, and make that variation measurable.

## Outcome

Training covers the real variation through augmentation and added data, and test sets are tagged by condition so results can be broken down.

## Scope (in)

- Inventory of real-world variation: lighting, motion blur, background noise, accents, device differences.
- Augmentation pipeline matching that variation, applied to training data only.
- Synthetic data or simulation where real data is scarce, checked against real examples.
- Collection of hard negatives and rare cases.
- Test sets tagged by condition.
- Domain-shift check between the training data and the deployment environment.

## Scope (out)

- Edge hardware optimisation (Edge & Device Optimization).

## Decisions

- **Use synthetic data or simulation?** Based on how scarce the real cases are and how well synthetic ones can be validated.
