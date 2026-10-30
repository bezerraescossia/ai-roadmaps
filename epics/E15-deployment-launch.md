---
id: E15
title: Deployment, Scaling & Launch Readiness
archetypes: [llm-service, batch-pipeline, classical-ml, agent, fine-tuning, perception]
requires: core
applies_when: always
depends_on: [E03, E10, E12, E64]
phase: launch
---

## Description

Package, deploy and scale the service; gate launch on the production checklist.

## Outcome

The service is deployed through CI/CD, load-tested at expected peak, and signed off against all 15
checklist items.

## Scope (in)

- Containerization: image with the app server and multiple async workers.
- Health check with dependency status for model providers, cache, retrieval and guardrails.
  [Checklist #11]
- CI/CD pipeline: build, test, eval gate and deploy across dev, staging and production.
- [cap: load-test, tier: production] Load testing at expected peak concurrency (course default: 100 concurrent users). [Checklist #15]
- [cap: scaling-plan, tier: critical] Scaling plan by traffic tier: single server, then async + cache + queue, then horizontal scaling, then
  multi-region.
- Self-hosted inference (optional; `self_hosted == yes`): vLLM, TGI or TensorRT-LLM.
- Production readiness review: architecture gap analysis and sign-off on all 15 deployment checklist
  items.

## Scope (out)

- Multi-region deployment unless the traffic tier requires it.

## Decisions

- **Select deployment target.** Options: VM, containers/Kubernetes, serverless, managed AI platform,
  based on expected traffic and team skills.

## Archetype notes

- **batch-pipeline:** workers and schedulers instead of a request/response service. Health means worker
  heartbeat and queue age. The load test runs at backfill volume. Self-hosted inference only if the
  method chosen needs it.
- **classical-ml:** packages the serving component and the training pipeline. The release gate is the
  thresholds from Offline Evaluation and Retraining; the self-hosted inference story does not apply.
- **agent:** ship tool credentials and sandbox configuration with least privilege, load-test long runs, release new agent versions by canary, and provide a kill switch.
- **fine-tuning:** packages the serving of the tuned model; the launch gate is the release criteria from the evaluation harness plus the safety and licensing approval.
- **perception:** covers cloud serving and the training pipeline; for embedded targets the device release process comes from Edge & Device Optimization.
