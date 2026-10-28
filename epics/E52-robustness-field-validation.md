---
id: E52
title: Robustness & Field Validation
archetypes: [perception]
requires: core
applies_when: always
depends_on: [E29]
phase: harden
---

## Description

Prove the model works in the real environment, across conditions and groups, before relying on it.

## Outcome

Per-condition and per-group results meet agreed floors, a field trial has run without acting on the output, and the owner has signed off.

## Scope (in)

- Per-condition metrics from the tagged test sets, with a floor for each.
- Failure-mode catalogue: the worst cases reviewed by a person.
- [cap: field-trial, tier: critical] Field trial in the real environment in shadow mode before the output is acted on.
- Fairness across groups (for example skin tone, age, accents, dialects) with measured gaps.
- Out-of-distribution and corrupted inputs, and an abstain or low-confidence behaviour.
- Privacy and biometric-data compliance check.
- Acceptance sign-off by the owner.

## Scope (out)

- Continuous monitoring (Monitoring & Drift).

## Decisions

- **Set the per-condition floors and the abstain policy.** When the model should refuse to answer and what happens then.
