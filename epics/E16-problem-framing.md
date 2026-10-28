---
id: E16
title: Problem Framing & Success Criteria
archetypes: [llm-service, poc, batch-pipeline, classical-ml, agent, fine-tuning, perception]
requires: core
kind: discovery
applies_when: always
depends_on: []
phase: discover
---

<!-- kind: discovery — not a ledger entry. The intake interview performs this epic; its answers fill
     Vision & End States, Constraints & Decisions and Open Questions of the roadmap. -->

## Description

Frame the problem before anything is built: who needs what, how success is measured, and what limits
apply.

## Outcome

The use case, users, success metrics and constraints are written down, and the risk posture is recorded.

## Scope (in)

- Define use case, users and the decision or workflow the AI output changes.
- Define success metrics and thresholds (quality, latency or throughput, cost per unit, business KPI),
  and what the current non-AI process achieves, as the bar to beat.
- Risk, compliance and data sensitivity assessment: sensitive data, regulatory limits, impact of a wrong
  output.
- Record fixed constraints: technology, hosting, provider, budget, deadline.

## Scope (out)

- Detailed design of any single component (done when that epic's spec is started).

## Decisions

- **Is AI the right tool?** Compare with rules or a manual process on the stated metrics. Record the
  answer as a constraint or, if open, an Open Question.

## Archetype notes

- **llm-service:** this replaces the course's "Use Case Definition & Solution Design" epic. Which optional epics apply is decided by the intake questions, not
  by a separate story. Add the **model and provider strategy** decision: hosted API models, open-weight models
  on managed hosting, or self-hosted models; a single model or routing (a small model for simple tasks, a
  large one for complex tasks). Record it as a constraint, or as an Open Question when undecided. The
  Guardrails epic consumes the risk assessment.
