---
id: E54
title: Compute & Environments
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E53]
phase: build
---

## Description

The compute, environments and infrastructure-as-code every other capability runs on.

## Outcome

Separate dev, staging and production environments with managed CPU and GPU pools, quotas, reproducible images and cost visibility per team.

## Scope (in)

- Dev, staging and production separation, defined as code.
- Compute pools: CPU, GPU, spot or preemptible capacity.
- Scheduling and quotas per team.
- Reproducible environments: base images and dependency management.
- Secrets and networking.
- Cost visibility (showback) by team and project.
- Autoscaling and idle shutdown.

## Scope (out)

- Workflow tooling (Training & Pipeline Orchestration).

## Decisions

- **Select the compute substrate.** Options: Kubernetes, a managed ML service, a batch scheduler such as Slurm. Based on cloud, skills and workloads.
