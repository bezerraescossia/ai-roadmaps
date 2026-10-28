---
id: E43
title: Training Infrastructure & Pipeline
archetypes: [fine-tuning]
requires: core
applies_when: always
depends_on: [E41]
phase: build
---

## Description

The compute and tooling that make training runs reproducible, trackable and affordable.

## Outcome

Any run can be reproduced from its recorded code, data, configuration and environment, and its cost is known.

## Scope (in)

- Compute access: cloud GPUs, cluster or hosted service; quotas and spot or preemptible handling.
- Training framework and configuration files in version control.
- Pinned, containerised environment and fixed seeds.
- Experiment tracking: parameters, metrics, artefacts, dataset and code versions.
- Checkpointing and resume after interruption.
- Distributed training setup when the model or data needs it.
- Cost tracking per run and artefact storage.

## Scope (out)

- Production serving (Packaging & Serving).

## Decisions

- **Select the training framework.** For example Hugging Face TRL, Axolotl, Unsloth or a vendor tool. Based on the method and team skills.
- **Select the compute provider.** Based on GPU availability, cost and data location.
