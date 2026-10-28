---
id: E41
title: Adaptation Strategy & Baselines
archetypes: [fine-tuning]
requires: core
applies_when: always
depends_on: [E17]
phase: build
---

## Description

Decide whether and how to adapt a model, after measuring what simpler options achieve.

## Outcome

A recorded decision on method, base model and compute, backed by measured baselines from prompting (and retrieval where relevant).

## Scope (in)

- Prompting baseline: the best prompted or few-shot result from the candidate base models on a small evaluation set.
- Retrieval or tool baseline where missing knowledge could be the problem.
- Gap analysis: whether failures are missing knowledge, style or format, or reasoning; tuning fixes style, format and behaviour more readily than missing knowledge.
- Targets: the quality gain, latency or cost reduction that justifies the effort, with thresholds.
- Method and base model selection: size, licence, context length, tooling.
- Compute and budget plan for training and serving.

## Scope (out)

- Data preparation and training (next epics).

## Decisions

- **Is fine-tuning needed?** Proceed, or improve prompts and retrieval first. Record the evidence.
- **Select the method.** Options: full fine-tune, LoRA/QLoRA (parameter-efficient), supervised tuning then preference tuning (DPO or similar), distillation from a larger model, continued pre-training.
- **Select the base model.** Based on licence, size, quality on the baseline, and serving cost.
- **Hosted tuning API or your own training?** Based on data restrictions, control and cost.
