---
id: E37
title: Memory & Context Management
archetypes: [agent]
requires: optional
applies_when: memory == yes
depends_on: [E36]
phase: build
---

## Description

Decide what the agent remembers within a run and across runs, and how each model call's context is assembled.

## Outcome

Each model call receives a bounded, relevant context, and long-term memory is stored, retrieved, corrected and deleted by explicit rules.

## Scope (in)

- Context assembly: what goes into each call and the token budget for each section.
- Summarisation and truncation of long runs and conversations.
- Short-term working memory per run.
- Long-term memory: what is stored (facts, preferences, past runs), write, read and forget rules, scoped per user or tenant.
- Memory quality: staleness, conflicting entries, and poisoning from untrusted content.
- Deletion on request and retention limits.

## Scope (out)

- Knowledge retrieval from documents (Knowledge Retrieval epic).

## Decisions

- **Select the memory store.** Options: vector database, relational table, key-value store, or files. Based on query patterns and scale.
- **When does the agent write memory?** Explicitly on user request, or automatically with review.
