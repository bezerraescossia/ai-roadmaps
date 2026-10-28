---
id: E22
title: Document Parsing & Preprocessing
archetypes: [batch-pipeline]
requires: optional
applies_when: input_docs == yes
depends_on: [E21]
phase: build
---

## Description

Turn raw files (PDFs, scans, emails, office documents) into clean text and structure the next stage can
use.

## Outcome

Each supported file type becomes normalised text plus structure (pages, tables, layout) with a quality
signal, and unreadable files are flagged.

## Scope (in)

- Supported file types and a rejection path for the others.
- Text extraction per type; table and layout extraction where the answer depends on them.
- OCR for scans (only when `scanned` is `yes`): engine, language support, a confidence threshold for
  re-processing.
- Normalisation: encoding, language detection, deduplication, page and section boundaries kept for
  citations.
- Parse-quality signal stored per item, so downstream stages and reviewers can see low-quality input.
- Parsing regression set: a few hard files per type, re-run on every change.

## Scope (out)

- Extraction or classification of the content (next epic).

## Decisions

- **Select the parsing tooling.** Options: open-source parsers, a managed document-AI service, a
  vision-capable LLM on page images, or a combination. Based on layout complexity, scan share, cost per
  page and data restrictions.
