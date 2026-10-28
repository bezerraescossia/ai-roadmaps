---
id: E55
title: Data & Feature Platform
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E54]
phase: build
---

## Description

Governed access to data for training and serving, with lineage and quality checks.

## Outcome

Practitioners can discover and use governed datasets with lineage, quality checks and point-in-time-correct training data.

## Scope (in)

- Governed dataset access, catalog and lineage.
- Data quality checks and contracts at ingestion.
- Training dataset versioning and point-in-time correctness.
- Feature store (only when `feature_store` is `yes`): offline and online stores, shared definitions, training and serving consistency.
- Handling and anonymisation of personal data.

## Scope (out)

- Business data warehousing unrelated to ML.

## Decisions

- **Feature store: build, buy or skip?** A shared store pays off with many models or online features; skip it for a few batch models.
