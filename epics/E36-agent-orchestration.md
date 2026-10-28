---
id: E36
title: Orchestration & Planning Loop
archetypes: [agent]
requires: core
applies_when: always
depends_on: [E35, E10, E07]
phase: build
---

## Description

The control flow that runs the agent: planning, tool calls, state and termination.

## Outcome

Runs follow an explicit, inspectable control flow with bounded steps, saved state, resumption after failure and a clear end state.

## Scope (in)

- Control flow as an explicit graph or state machine, not an unbounded prompt loop.
- Planning approach: plan up front, step by step, or a hybrid; plan revision on failure.
- Run state persisted after each step, so a run can be resumed, inspected or replayed.
- Limits per run: steps, tokens, wall-clock time and spend; detection of loops and repeated calls.
- Error handling inside runs: tool failure, malformed model output, timeouts; retry, replan or escalate.
- Run result contract: status (completed, failed, needs input, aborted), outputs, trace id.
- Idempotent tool calls or compensating actions wherever a step can be retried.

## Scope (out)

- Long-term memory (Memory & Context), human approvals (Human Oversight).

## Decisions

- **Select the orchestration framework.** Options: LangGraph, a vendor agent SDK, a workflow engine (Temporal, Prefect), or custom code. Based on needed durability, team skills and lock-in.
