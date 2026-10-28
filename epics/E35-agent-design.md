---
id: E35
title: Agent Design & Autonomy Scope
archetypes: [agent]
requires: core
applies_when: always
depends_on: [E02]
phase: build
---

## Description

Decide what the agent may do, how much it decides on its own, and where a simpler workflow is enough.

## Outcome

A written agent specification: tasks, autonomy level, tools and data it may touch, stop conditions and failure modes, agreed with the owner.

## Scope (in)

- Task inventory: the jobs the agent does, each with an example run and the expected result.
- Workflow or agent? For each task, whether a fixed sequence of LLM calls is enough or the model must choose its own steps.
- Autonomy level per action class (read, write, spend, contact people) and which classes need approval.
- Boundaries: tools, data and systems the agent may access, and what it must never do.
- Stop conditions: success, step and time limits, cost cap, and when to give up and hand over.
- Failure-mode analysis: wrong tool, loops, invented results, partial completion, injected instructions in tool output.

## Scope (out)

- Implementation of the control loop (Orchestration) and of the tools.

## Decisions

- **Select the agent pattern.** Options: single agent with tools, fixed workflow with LLM steps, planner-executor, multi-agent. Prefer the simplest pattern that covers the task inventory.
- **Select the autonomy level.** Options: assistive (suggests), supervised (acts after approval), autonomous within limits.
