---
id: E6
title: Monitoring & Maintenance
phase: monitoring-maintenance
depends_on: [E5]
weight: 2
loops_back_to: [E2, E3, E4]
---

## Description

Keep the deployed model working: watch how it serves and how well it predicts, and retrain and redeploy when
it degrades.

## Outcome

Serving efficiency and prediction quality are monitored against thresholds, and the model is retrained,
re-evaluated and redeployed when a threshold is crossed.

## Tasks

- Monitor the efficiency and efficacy of prediction serving.
- Compare results to the thresholds.
- Retrain when needed.
- Collect and label new data.
- Repeat the engineering and evaluation phases.
- Apply continuous integration, training and deployment.
- Measure live accuracy once outcomes arrive, using the label delay to set the lag. (added)
- Monitor input and prediction drift as a proxy while outcomes are still unknown. `[label_delay=long]` (added)

## Outputs

- Monitoring reports.
- Retrained models.
- Newly labeled data.

## Quality assurance

- **Risks:** the model goes stale as the data drifts; changes in the hardware or software stack affect it.
- **Metrics:** performance against the defined thresholds; serving efficiency.
- **Mitigations:** continued model evaluation; scheduled or triggered retraining; periodic review of the
  business use case.

## Decisions

- **Select the monitoring thresholds** and who is alerted.
- **Select the retraining trigger:** a schedule, a drift or performance threshold, or both.
- **Select the drift detection method.** (added)

## Loop-backs

- Back to E2 to collect and label new data.
- Back to E3 to retrain.
- Back to E4 to re-evaluate before redeploying.

## Open questions

Filled from `unsure` intake answers. If `label_delay` is unknown: how long until the true outcome is known?
