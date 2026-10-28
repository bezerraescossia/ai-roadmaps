---
id: E05
title: Caching
archetypes: [llm-service]
requires: optional
applies_when: caching == yes
depends_on: [E03]
phase: harden
---

## Description

Avoid redundant model calls to reduce cost and latency.

## Outcome

Repeated or similar requests are served from cache, the hit rate is measured, and a cache outage never
fails a request.

## Scope (in)

- Cache lookup before the model call; store responses after output guardrails pass. [Checklist #5]
- TTL, max size, eviction policy, and invalidation (source data or prompt version change).
- Cache metrics: hits, misses, hit rate (course target > 30%).
- Cache bypass on failure: if the cache is unavailable, call the model directly.
- [cap: shared-cache, tier: production] Shared cache backend (e.g. Redis) when running multiple instances.

## Scope (out)

- Cache warming.

## Decisions

- **Select caching strategy.** Options: exact-match cache, semantic (embedding) cache, provider prompt
  caching for stable prefixes, or a combination. Define the similarity threshold if semantic.
