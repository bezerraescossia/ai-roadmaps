---
id: E3
title: ML Model Engineering
phase: model-engineering
depends_on: [E2]
weight: 4
loops_back_to: [E2]
---

## Description

Select algorithms against a baseline, train candidate models in a tracked and reproducible way, and document
the result.

## Outcome

One or more trained models exist, every run's metadata is collected, the model and its experiments are
documented, and the training pipeline is packaged so it can be repeated.

## Tasks

- Define the quality measures.
- Select algorithms and a baseline. Candidate families follow `task_type`. (added)
- Add domain knowledge.
- Train the models.
- Optionally apply transfer learning, model compression or ensemble learning.
- Document the model and the experiments.
- Tune hyperparameters within a fixed budget. (added)
- Record training cost and time, since they set the retraining cadence. (added)

## Outputs

- Trained model(s).
- Collected metadata: algorithm, train, validation and test data, hyperparameters, runtime environment.
- Model documentation, for example a model card.
- A packaged training pipeline.

## Quality assurance

- **Risks:** results cannot be reproduced; overfitting; bias; lack of transparency.
- **Metrics:** performance, robustness, fairness, scalability, interpretability, model complexity and
  resource demand, weighted by the use case; mean performance across random seeds.
- **Mitigations:** metadata collection; validation across random seeds; cross-validation; model
  documentation; repeatable pipelines.

## Decisions

- **Select the algorithm families** to try, starting with the simplest that can beat the baseline. (added)
- **Select the weights of the quality measures** for this use case.
- **Select the experiment tracking tool.** Options: MLflow, Weights & Biases, a cloud-native service. (added)

## Loop-backs

- Back to E2 when the features or data need to change to improve the model.

## Open questions

Filled from `unsure` intake answers; none by default.
