---
id: E21
title: Source Ingestion & Job Orchestration
archetypes: [batch-pipeline]
requires: core
applies_when: always
depends_on: [E02, E17]
phase: build
---

## Description

Get items in from their sources and run them through the pipeline reliably, on a schedule or as they
arrive.

## Outcome

New items are picked up exactly once, each is tracked through its states, and a failed run can be resumed
or replayed without duplicates.

## Scope (in)

- Source connectors for each input (storage bucket, mailbox, database, API), with access credentials in a
  secrets manager.
- Job model: one record per item with state (queued, processing, done, failed, needs review), attempt
  count, timestamps and the pipeline version that produced it.
- Idempotency: the same item processed twice yields one result; items are identified by a stable key or
  content hash.
- Trigger and schedule: event-driven, scheduled, or one-off backfill, as chosen. If `arrival` is
  `continuous`, add watch/poll logic and a dead-letter queue.
- Failure handling: retry with backoff, poison-item quarantine, resume after a crash.

## Scope (out)

- The processing logic itself (parsing, extraction), throughput tuning (separate epics).

## Decisions

- **Select the orchestrator.** Options: a workflow engine (Airflow, Prefect, Dagster), cloud-native
  (Step Functions, Cloud Workflows), a queue with workers, or cron plus a script. Based on volume, team
  skills and existing infrastructure.
