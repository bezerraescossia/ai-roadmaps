---
id: E64
title: Serving Contract & Stub
archetypes: [llm-service, batch-pipeline, classical-ml, agent, fine-tuning, perception, ml-platform]
requires: core
first: true
applies_when: always
depends_on: []
phase: discover
---

## Description

Agree the contract between consumer and provider before anything is built, and publish a stub that returns
constant dummy values, so consumers can integrate while the real service is developed.

## Outcome

Consumers have a signed-off contract and a hosted stub they can call from day one. The stub is replaced by
the real service once it passes the same contract tests.

## Scope (in)

- Contract in the format that matches the serving mode (online API, streaming, batch output, embedded
  interface): payload schemas, error model, versioning and deprecation policy, auth method, and the
  semantics of every field, including what a stub value means. Latency and availability targets and rate
  limits are stated as targets; the stub does not enforce them.
- Worked examples for every operation in the contract; the stub's responses are generated from them, so
  contract and stub cannot drift apart.
- Hosted stub on a stable URL, generated from the contract. It returns one constant canonical example per
  operation and marks every response as a stub (header or `stub: true` field).
- Named fixtures selectable by header or parameter: error, empty result, low confidence, timeout.
- Consumer sign-off: each consumer confirms the contract against their use case before v1 is frozen.
- Revision window: contract changes need the consumer's agreement until the first real-service release;
  after it, the versioning policy applies.
- [cap: contract-tests, tier: production] Contract tests (provider and consumer) that run against the stub from day one and against the
  real service later.

## Scope (out)

- The real implementation, its release and its scaling (Serving & release, Deployment epics).
- Enforcing latency, rate limits or auth in the stub.

## Decisions

- **Select the contract format.** Options: OpenAPI, AsyncAPI, JSON Schema or protobuf, a table or file
  schema with a delivery schedule, or an interface definition. Based on the serving mode and what consumers
  already use.
- **Select the stub stack.** Options: a mock server generated from the spec (for example Prism or
  WireMock), a generated client with fake responses, or the spec and examples only. Based on how fast
  consumers must start and who hosts it.
- **Contract-change risk.** Open Question: what findings from the real model (latency, output shape,
  confidence calibration) could force a change inside the revision window, and who approves it.

## Archetype notes

- **llm-service:** include the streaming protocol (events, termination, mid-stream errors) when streaming is
  used, and what a refusal or guardrail block looks like to the consumer.
- **agent:** include run start, status, result and cancellation, and how tool actions needing approval are
  reported.
- **batch-pipeline:** the contract is the result delivery schema plus schedule; the stub is a sample output
  file or table.
- **classical-ml, fine-tuning, perception:** include the score or label fields, their calibration meaning
  and the "unknown" value; the real model's serving epic implements this contract.
- **ml-platform:** the consumers are internal teams; the contract is the platform API and the pilot team's
  integration points.
