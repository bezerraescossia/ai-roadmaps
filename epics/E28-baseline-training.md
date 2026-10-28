---
id: E28
title: Baseline & Model Training
archetypes: [classical-ml, perception]
requires: core
applies_when: always
depends_on: [E27]
phase: build
---

## Description

Establish a baseline, then train and tune candidate models in a reproducible, tracked way.

## Outcome

A simple baseline and one or more trained candidates exist, every run is tracked and reproducible, and the
best candidate is selected on the agreed metric.

## Scope (in)

- Baseline: a trivial predictor (majority class, last value, popularity, a simple rule) measured on the
  validation data.
- Reproducible training pipeline: pinned dependencies, seeds, configuration, data and feature versions.
- Experiment tracking: parameters, metrics, artefacts and data versions for each run.
- Candidate models of increasing complexity (linear, gradient-boosted trees, then a neural model only if
  justified).
- Hyperparameter search with a budget, and early stopping where it applies.
- Training cost and time recorded, since they set the retraining cadence.

## Scope (out)

- Final evaluation on the test set (next epic).

## Decisions

- **Select the modelling approach.** Choose from the task type: classification, regression, ranking,
  forecasting, anomaly detection, recommendation. Prefer the simplest model that beats the baseline by a
  margin that matters to the business.
- **Select the experiment tracking tool.** Options: MLflow, Weights & Biases, or a cloud-native service.

## Archetype notes

- **perception:** start from a pretrained backbone or speech model and fine-tune it; train from scratch only if justified. The baseline is an off-the-shelf pretrained model used zero-shot or a simple classical method. Track GPU hours.
