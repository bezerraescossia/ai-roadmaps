---
id: E45
title: Evaluation Harness & Regression Testing
archetypes: [fine-tuning]
requires: core
applies_when: always
depends_on: [E41, E17]
phase: build
---

## Description

Measure every checkpoint the same way, against the baselines and against loss of general ability.

## Outcome

One automated harness scores the base model, the prompted baseline and each checkpoint on the task and on regression suites.

## Scope (in)

- Task evaluation set tied to the success criteria, frozen and decontaminated.
- Metrics: automatic scores against the task's reference answers or checks.
- [cap: judge-calibration, tier: production] An LLM-as-judge for open-ended outputs, calibrated against human labels.
- [cap: human-eval-sample, tier: critical] A human-reviewed sample of outputs scored against the same rubric.
- Same-harness comparison of the base model, the prompted baseline and every checkpoint.
- Regression suite for general capabilities and instruction following, to detect forgetting.
- Format and structured-output validity checks.
- Automatic run for every checkpoint, with sample sizes large enough to tell real differences from noise.

## Scope (out)

- Safety and red-team evaluation (Safety, Licensing & Governance).

## Decisions

- **Select the judge and how it is calibrated.** Judge model, rubric, and the agreement with human labels required.
- **How much loss of general ability is acceptable?** Set the floor per regression suite.
