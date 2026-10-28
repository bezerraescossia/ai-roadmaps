---
id: E11
title: Streaming & Response Delivery
archetypes: [llm-service, agent]
requires: optional
applies_when: streaming == yes
depends_on: [E03]
phase: build
---

## Description

Deliver output incrementally to reduce perceived latency.

## Outcome

Chat endpoints stream tokens with a clear end-of-stream event, and the client handles loading, error and
cancel states.

## Scope (in)

- Streaming endpoint: stream tokens with an end-of-stream event for all chat endpoints. [Checklist #6]
- Provider-to-client passthrough: forward provider chunks directly (course target: first token in
  200-500ms).
- Client stream handling: loading, error and cancel states.

## Scope (out)

- Bidirectional transports unless selected in Decisions.

## Decisions

- **Select streaming protocol.** Options: Server-Sent Events (default for most apps), WebSockets
  (bidirectional, e.g. voice), long polling (legacy clients).

## Archetype notes

- **agent:** applies when `streaming` is `yes`; stream intermediate steps (tool calls, status) as well as tokens.
