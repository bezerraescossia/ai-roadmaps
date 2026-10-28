---
id: E06
title: Knowledge Retrieval (RAG)
archetypes: [llm-service, agent]
requires: optional
applies_when: rag == yes
depends_on: [E02, E14]
phase: build
---

## Description

Ground responses in your own data.

## Outcome

A question returns an answer grounded in the project's own data, with citations, and retrieval quality
is measured separately from model quality.

## Scope (in)

- Knowledge source inventory and access: documents, databases and APIs to index, with owners, access
  rights and update frequency.
- Ingestion and chunking pipeline: parse, clean, chunk; keep metadata for filtering and citations.
- Retrieval and context injection: top-k retrieval, instructions to answer only from context and cite
  sources.
- [cap: index-refresh, tier: production] Index refresh and versioning: scheduled or event-driven re-indexing.
- Retrieval evaluation: context precision/recall and answer faithfulness, with and without retrieval;
  retrieval latency tracked separately from model latency.
- [cap: retrieval-degradation, tier: production] Graceful degradation without retrieval: if the vector store is down, continue without context and
  flag lower confidence.
- Pattern-specific scope (only the pattern chosen in Decisions; drop the rest):
  - hybrid search and reranking (rag-pattern-hybrid)
  - corrective RAG: retrieval grader and fallback (rag-pattern-corrective)
  - Self-RAG: retrieval decision and self-critique (rag-pattern-self)
  - GraphRAG: knowledge graph construction (rag-pattern-graph)
  - agentic RAG: multi-step retrieval agent (rag-pattern-agentic)

## Scope (out)

- Upload API with async ingestion jobs.

## Decisions

- **Select RAG pattern.** Options: Basic RAG, Hybrid search + reranking, Corrective RAG, Self-RAG,
  GraphRAG, Agentic RAG. Choose on data type, accuracy needs, latency and cost budget.
- **Select embedding model.** Based on language, domain, cost and dimension size.
- **Select and set up vector store.** In-memory for development; managed or self-hosted (e.g. Pinecone,
  Qdrant, pgvector) for production.

## Archetype notes

- **agent:** retrieval is one tool among others; applies only when `rag` is `yes`. Evaluate retrieval separately from the run outcome.
