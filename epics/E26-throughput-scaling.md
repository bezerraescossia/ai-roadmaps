---
id: E26
title: Throughput, Scaling & Backfill
archetypes: [batch-pipeline]
requires: core
applies_when: always
depends_on: [E23, E12]
phase: harden
---

## Description

Make the pipeline process its real volume within the time and cost limits, including the first large
backfill.

## Outcome

The pipeline meets the stated items-per-hour and deadline at the projected cost, respects provider rate
limits, and a backfill can run without disturbing the live flow.

## Scope (in)

- Throughput target derived from volume and deadline, with a measured baseline.
- Concurrency and batching: parallel workers, provider batch endpoints where cost allows, bounded queues
  and backpressure.
- Provider rate limits and quotas: token and request budgets shared across workers, retry handling that
  does not stampede.
- Cost at scale: compare the measured cost per item at volume with the projection kept in Cost Management.
- Backfill plan: rate-limited, resumable, prioritised below live traffic, with a progress report.
- Load test at peak and at the backfill volume.

## Scope (out)

- Multi-region or real-time serving.

## Decisions

- **Use provider batch APIs?** Cheaper per item but slower and asynchronous. Based on the deadline and
  how soon results are needed.
