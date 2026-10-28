---
id: E20
title: Production Estimate & Go/No-Go
archetypes: [poc]
requires: core
applies_when: always
depends_on: [E19]
phase: launch
---

## Description

Turn the results into a decision and, if it is a go, a starting point for the production project.

## Outcome

A written go / no-go / more-work recommendation with evidence, the gaps between prototype and
production, and the archetype for the follow-on roadmap.

## Scope (in)

- Decision memo: results versus thresholds, cost and risk, what would change the answer.
- Gaps to production: data pipeline, reliability, security and compliance, monitoring, evaluation,
  operations, team and run costs.
- Rough effort and run-cost range for production, with its main uncertainties named.
- Recommended archetype and epics for the production roadmap, and which spike code, if any, is
  reused.
- Handover: the evaluation set, the prototype, and the log of what was tried.

## Scope (out)

- Building the production system.

## Decisions

- **Go, no-go, or more work?** Decided by the sponsor with the memo.
- **Which archetype does production use?** Options: LLM service, agent, batch pipeline, classical ML, fine-tuning, perception, or a
  combination (and an ML platform if several projects will need the same foundations). The next roadmap is created with `/speckit-roadmap-intake`.
