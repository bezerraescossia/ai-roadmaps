---
id: E47
title: Safety, Licensing & Governance
archetypes: [fine-tuning]
requires: core
applies_when: always
depends_on: [E41]
phase: harden
---

## Description

Check that the tuned model may be used as intended, did not lose its safety behaviour, and is documented.

## Outcome

Licence and data rights are confirmed, safety behaviour has been compared before and after tuning, and a named owner approves the release.

## Scope (in)

- Base model licence and use restrictions checked for the intended use, redistribution and derivative-model terms.
- Rights to the training data confirmed.
- Safety evaluation: refusal behaviour and harmful-output rate before versus after tuning.
- Red-team of the tuned model, including jailbreaks and prompt injection.
- Memorisation and extraction tests for sensitive training data.
- Safety and licensing sections of the model card, which belongs to Model Registry & Versioning.
- Release approval by a named owner.

## Scope (out)

- Legal advice; the licence reading is confirmed by the responsible person.

## Decisions

- **Who approves the release, and what is the safety bar?** For example no increase in harmful outputs on the red-team set.
