---
id: E44
title: Training Runs & Iteration
archetypes: [fine-tuning]
requires: core
applies_when: always
depends_on: [E42, E43, E45]
phase: build
---

## Description

Run the training, compare variants, and select the checkpoint to release.

## Outcome

A selected checkpoint that meets the targets on the validation set, with every run recorded and the reasons for choosing it written down.

## Scope (in)

- Smoke run on a tiny subset to prove the pipeline end to end.
- First full run with default settings, evaluated by the harness.
- Experiments within a budget: learning rate, adapter rank, epochs, batch size, data mix.
- Monitoring of loss curves and evaluation metrics during training; early stopping.
- Ablations to learn what helps (data subsets, method variants).
- Preference-tuning stage if chosen.
- Checkpoint selection on the validation set; the test set is used once at the end.

## Scope (out)

- Packaging and serving the selected checkpoint.

## Decisions

- **Set the experiment budget and stopping rule.** Maximum runs or GPU hours, and the improvement below which iteration stops.
