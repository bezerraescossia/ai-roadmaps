---
id: E07
title: Tools & Integrations
archetypes: [llm-service, agent]
requires: optional
applies_when: tools == yes
depends_on: [E03, E09, E10]
phase: build
---

## Description

Let the model call external systems (APIs, databases, custom models) to fetch data or take actions.

## Outcome

The model can call registered tools within permission and safety limits, and every call is validated and
logged.

## Scope (in)

- Tool registry with schemas: name, description, JSON Schema parameters.
- Tool selection and execution loop: the model selects tools, the service executes them and returns
  results.
- Tool permissions and action safety: which tools each user/role may use; confirmation for actions with
  side effects (writes, payments, emails).
- Tool call validation and self-correction: validate names and arguments; retry with the error included
  when the call is invalid.
- Log tools used: tools_used in responses and request logs.
- [cap: mcp, tier: production] MCP integration: expose or consume tools via the Model Context Protocol instead of bespoke schemas.

## Scope (out)

- State-changing or business-system tools, unless an explicit decision is recorded.

## Decisions

- **Which tools have side effects?** Decide before the registry is built; side-effecting tools need
  confirmation and a recorded decision.

## Archetype notes

- **agent:** always applies. Tools are the agent's reach; each tool's side effects map to the autonomy levels from Agent Design. Tool results are untrusted input.
