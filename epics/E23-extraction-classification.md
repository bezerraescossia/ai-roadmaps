---
id: E23
title: Extraction & Classification Logic
archetypes: [batch-pipeline]
requires: core
applies_when: always
depends_on: [E21, E10]
after: [E22]
phase: build
---

## Description

The core of the pipeline: turn each item into structured output (extracted fields, labels, summaries).

## Outcome

Each item produces output that matches a versioned schema, with a confidence signal, using the chosen
method and prompt or model versions that are recorded.

## Scope (in)

- Output schema, versioned, with field definitions, types, allowed values and a null rule for missing
  information.
- Prompts or models versioned in source control; the version is stored with every result.
- Structured-output enforcement (schema-constrained decoding or validation plus retry).
- Long input handling: chunking, map-reduce, or page-level processing, with a merge rule.
- Confidence signal per field or item (model-reported, agreement across runs, or rule checks).
- Routing by difficulty or document type when a cheaper path exists for easy items.

## Scope (out)

- Validation and human review (next epic), throughput tuning.

## Decisions

- **Select the method.** Options: LLM only, rules only, a trained classifier or extractor, or a hybrid
  (rules first, LLM for the rest). Based on accuracy on the evaluation set, cost per item and volume.
- **Select the model strategy.** Single model, or tiers (small model first, escalate on low
  confidence).
