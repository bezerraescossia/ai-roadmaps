---
id: E53
title: Platform Scope, Users & Build-vs-Buy
archetypes: [ml-platform]
requires: core
kind: discovery
applies_when: always
depends_on: []
phase: discover
---

<!-- kind: discovery — not a ledger entry. The intake interview performs this epic; its answers fill
     Vision & End States, Constraints & Decisions and Open Questions of the roadmap. -->

## Description

Understand who the platform serves, what hurts today, and which capabilities to build, buy or adopt.

## Outcome

Users, workloads, pain points, maturity, success metrics and the build-versus-buy stance are written down.

## Scope (in)

- Users and workloads: teams, number of practitioners, models in production, batch, online and LLM workloads.
- Current pain: where time is lost (environments, deployment, reproducibility, GPU access).
- Maturity assessment: ad hoc, repeatable, automated, governed.
- Success metrics: time to first model, deployment frequency, time to roll back, GPU utilisation, teams adopting.
- Constraints: cloud, security, budget, team size.
- Build versus buy versus managed service, per capability.

## Scope (out)

- Detailed design of any single capability.

## Decisions

- **Build, buy or use a managed service, per capability?** Recorded as constraints; open ones become Open Questions.
