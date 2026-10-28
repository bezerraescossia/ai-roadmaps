---
id: E17
title: Data Availability & Quality Assessment
archetypes: [poc, batch-pipeline, classical-ml, fine-tuning, perception]
requires: core
applies_when: always
depends_on: [E16]
phase: discover
---

## Description

Find out what data exists, whether it can be used, and whether it is good enough, before choosing an
approach.

## Outcome

Data sources are inventoried with owners and access, a representative sample has been profiled, and
ground truth for evaluation is identified or planned.

## Scope (in)

- Data source inventory: systems, formats, owners, access rights, volumes, update frequency.
- Access and legal check: licences, privacy constraints, retention, where the data may be processed.
- Profile a representative sample: completeness, duplicates, noise, label quality, class balance, drift
  over time, language and format variance.
- Ground truth for evaluation: existing examples with correct answers, or a plan to create them. If
  `labeled_data` is `no` or `partial`, add a labeling plan (who labels, guidelines, how many, agreement
  check, cost).
- Data quality risks recorded with a decision for each: fix, filter, or accept.

## Scope (out)

- Building the production data pipeline (separate epic where the archetype has one).

## Decisions

- **Is the data good enough to proceed?** Proceed, collect or clean more first, or stop. Record the answer;
  if open, an Open Question that blocks the next epics.

## Archetype notes

- **fine-tuning:** assess the candidate training data (size, quality, licence, overlap with the evaluation data), not only feasibility.
- **perception:** assess the raw media (resolution, noise, device variety, class balance, label quality) and the gap between the collected data and the deployment conditions.
