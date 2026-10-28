---
id: E40
title: Multi-Agent Coordination
archetypes: [agent]
requires: optional
applies_when: multi_agent == yes
depends_on: [E36]
phase: harden
---

## Description

Split the work across several cooperating agents only where one agent is demonstrably not enough.

## Outcome

Agent roles, hand-offs and termination rules are defined, and the multi-agent system beats a single agent on the evaluation tasks at an acceptable cost.

## Scope (in)

- Roles and responsibilities of each agent, with the tools each may use.
- Communication: shared state, messages and hand-offs.
- Coordination pattern: supervisor, pipeline, or peer exchange; conflict resolution and termination.
- Cost control, since each added agent multiplies calls.
- Tracing across agents so one task can be followed end to end.
- Evaluation per agent and end to end, compared with a single-agent baseline.

## Scope (out)

- Open-ended agent societies without a task owner.

## Decisions

- **Select the coordination pattern and framework.** Justify against the single-agent baseline.
