---
id: E09
title: Guardrails & Safety
archetypes: [llm-service, batch-pipeline, agent]
requires: core
applies_when: always
depends_on: [E03, E10]
phase: build
---

## Description

Input and output checks so nothing reaches the model or the user unchecked.

## Outcome

Unsafe input is blocked before any model call, unsafe output is replaced before it reaches the user, and
the block rate is monitored for false positives.

## Scope (in)

- Prompt injection detection before prompt routing. [Checklist #3]
- PII detection and redaction for the PII types relevant to the use case. [Checklist #3]
- Output content safety: block harmful content, destructive commands and policy violations, replace
  with a safe message. [Checklist #4]
- Output format validation against the expected schema. [Checklist #4]
- Blocked request messaging: explain blocks without retrying; log the reason.
- Guardrail block rate monitoring (course target < 5%).

## Scope (out)

- Human review workflow.

## Decisions

- **Select guardrail approach.** Options: rule/regex-based, ML classifiers, LLM-as-judge, managed
  guardrail service, or a layered combination. Balance latency, cost and accuracy.

## Archetype notes

- **batch-pipeline:** applies only when `sensitive_data` is `yes`. Redact PII before items reach a hosted
  model, validate output against the schema, and treat document content as untrusted: a document can
  contain instructions aimed at the model (prompt injection). There is no end user to message; a blocked
  item is marked failed and routed to review.
- **agent:** guard tool inputs and outputs, not only user text; tool results can carry injected instructions. Enforce action allow-lists outside the model.
