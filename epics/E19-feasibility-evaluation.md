---
id: E19
title: Feasibility Evaluation
archetypes: [poc]
requires: core
applies_when: always
depends_on: [E18]
phase: build
---

## Description

Measure the prototype against the success criteria on held-out data, and understand where it fails.

## Outcome

Results versus the baseline and versus the success thresholds are known, with error analysis showing what
kinds of cases fail and why.

## Scope (in)

- Evaluation set built from the ground truth in the data assessment, separate from anything used to
  tune the prototype.
- Metrics from the framing epic, computed for the prototype and the baseline, with the sample size and
  the uncertainty stated.
- Error analysis: group failures by cause (data, prompt or model, missing context, ambiguous labels).
- Measured cost and latency per unit, extrapolated to expected volume.
- Stakeholder review of real outputs, not only metrics.

## Scope (out)

- Continuous or CI evaluation (production epic).

## Decisions

- **Which thresholds make this feasible?** Fixed in the framing; any change is recorded with the reason.
