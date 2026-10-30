---
id: E5
title: Deployment
phase: deployment
depends_on: [E4]
weight: 3
loops_back_to: [E4]
---

## Description

Put the approved model into use with a rollout strategy and a fallback, and verify it in production before
relying on it.

## Outcome

The model is deployed with an agreed architecture, a fallback plan and a rollout strategy, and its production
behavior and user acceptance have been verified.

## Tasks

- Define the inference hardware. `[serving=batch|online|embedded]`
- Evaluate the model in production, for example with online tests such as A/B tests.
- Test user acceptance and usability.
- Set a fallback plan.
- Choose a rollout strategy: canary, blue/green, A/B testing or multi-armed bandits.
- Establish model governance. `[regulated=yes]`
- Schedule predictions, store them and deliver them to consumers. `[serving=batch]` (added)
- Serve predictions behind an API with agreed latency and availability. `[serving=online]` (added)
- Fit the model to the target device's memory and compute limits. `[serving=embedded]` (added)

## Outputs

- The deployment approach and architecture, batch or online.
- The fallback plan.
- The rollout strategy.
- Acceptance and usability results.

## Quality assurance

- **Risks:** model outages; performance differs between test and production.
- **Metrics:** online test results; user acceptance and usability.
- **Mitigations:** a fallback plan; gradual rollout; evaluation in production.

## Decisions

- **Select the serving mode and hosting.** Follows `serving` and `constraints`.
- **Select the rollout strategy.**
- **Select the fallback.** For example the E1 benchmark rule or the previous model. (added)

## Loop-backs

- Back to E4 when production evaluation shows the model does not meet the success criteria.

## Open questions

Filled from `unsure` intake answers. If `serving` is `unsure`: how will predictions be consumed?
