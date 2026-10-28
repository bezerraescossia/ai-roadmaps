---
id: E63
title: LLMOps Extensions
archetypes: [ml-platform]
requires: optional
applies_when: llmops == yes
depends_on: [E56, E58]
phase: harden
---

## Description

Shared services for teams building LLM applications.

## Outcome

LLM application teams use shared prompt, gateway, evaluation and tracing services instead of building their own.

## Scope (in)

- Prompt registry and versioning.
- LLM gateway: routing, key management, rate limits, cost attribution.
- Evaluation service for LLM applications.
- Tracing for LLM calls.
- Shared guardrail service.
- Vector store as a service.

## Scope (out)

- Individual applications.

## Decisions

- **Build or adopt the LLM gateway?** Based on the providers used and the controls needed.
