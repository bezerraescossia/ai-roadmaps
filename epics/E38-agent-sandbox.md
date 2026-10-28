---
id: E38
title: Sandbox & Execution Environment
archetypes: [agent]
requires: optional
applies_when: code_execution == yes
depends_on: [E07]
phase: build
---

## Description

Run code, shell commands or a browser on the agent's behalf without exposing the host or its secrets.

## Outcome

Agent-driven execution runs isolated, with least privilege and hard resource limits, and every action is logged.

## Scope (in)

- Isolation of the execution environment from the host and other tenants.
- Resource limits: CPU, memory, time, disk, and a network egress allow-list.
- No ambient credentials; short-lived, least-privilege credentials injected only where needed.
- File system scoping, cleanup between runs, and dry-run modes for destructive operations.
- Logging of every command and result.
- [cap: sandbox-hostile-tests, tier: critical] Tests with hostile inputs: escape attempts, data exfiltration, resource exhaustion.

## Scope (out)

- The tools' business logic (Tools & Integrations).

## Decisions

- **Select the sandbox technology.** Options: containers, gVisor or Firecracker microVMs, a managed code interpreter, a browser sandbox. Based on the threat model and startup latency.
