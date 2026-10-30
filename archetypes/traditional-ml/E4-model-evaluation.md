---
id: E4
title: ML Model Evaluation
phase: model-evaluation
depends_on: [E3]
weight: 2
loops_back_to: [E3, E2]
---

## Description

Check the model against the success criteria on data it has not seen, test its robustness and explainability,
and decide whether it may be deployed.

## Outcome

The evaluation is documented and a deploy or no-deploy decision is recorded against the agreed criteria.

## Tasks

- Validate performance on the test set.
- Assess robustness with noisy or incorrect inputs.
- Ensure explainability.
- Decide whether to deploy, automatically against the criteria or manually by experts.
- Document the evaluation.
- Check fairness across the relevant groups. `[regulated=yes]` (added)
- Prepare the compliance and audit evidence. `[regulated=yes]` (added)

## Outputs

- Evaluation documentation.
- The deploy or no-deploy decision.

## Quality assurance

- **Risks:** the success criteria are not met; users do not trust the model; regulations are not complied
  with; ML-assisted workflows lead to poor decisions.
- **Metrics:** test-set performance against the success criteria; robustness under noisy inputs;
  explainability.
- **Mitigations:** explainable models; automated or expert-reviewed deployment decisions; documented outcomes.

## Decisions

- **Decide who decides:** an automatic gate on the criteria, expert sign-off, or both.
- **Select the explainability method.** (added)

## Loop-backs

- Back to E3 when the success criteria are not met.
- Back to E2 when the evaluation shows a data problem.

## Open questions

Filled from `unsure` intake answers. If `regulated` is `unsure`: does a regulation require explanations,
fairness checks or audit?
