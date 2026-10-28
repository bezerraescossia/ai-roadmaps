---
id: E25
title: Results Storage & Delivery
archetypes: [batch-pipeline]
requires: core
applies_when: always
depends_on: [E23]
after: [E24]
phase: build
---

## Description

Store results with their provenance and deliver them to the systems and people that use them.

## Outcome

Accepted results are stored versioned and queryable, delivered to each consumer in its format, and can be
re-processed when the pipeline improves.

## Scope (in)

- Result store: output, source item key, pipeline and model versions, confidence, status, timestamps.
- Delivery to each consumer (database load, API push, file export, notification), with idempotent
  writes and retries.
- Schema evolution: how consumers handle a new output schema version.
- Reprocessing: re-run a set of items with a new pipeline version, keeping the previous results.
- Retention and deletion rules for source and result data.

## Scope (out)

- Building the downstream applications that use the results.

## Decisions

- **Select the result store.** Options: a relational database, a data warehouse, object storage with a
  table format, or a search index. Based on query patterns and what consumers already use.
