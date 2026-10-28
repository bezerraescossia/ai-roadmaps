---
id: E18
title: Prototype & Baseline Spike
archetypes: [poc]
requires: core
applies_when: always
depends_on: [E17]
phase: build
---

## Description

Build the smallest thing that can show whether the approach works, plus a trivial baseline to compare
against.

## Outcome

A throwaway prototype runs end to end on real sample data, and a simple baseline (rules, majority class,
or manual) is measured on the same data.

## Scope (in)

- Baseline: the simplest non-AI or minimal-AI method on the same sample.
- Prototype of the chosen approach, run end to end on real data, not toy data.
- Timebox and stop rule agreed up front; log what was tried and what failed.
- Record assumptions the prototype makes that production would not (cleaned data, no latency limit, one
  user, hand-picked examples).

## Scope (out)

- Production code quality, security hardening, deployment, monitoring.

## Decisions

- **Select the approach(es) to try.** Options: prompted LLM, retrieval + LLM, classical ML, rules, or a
  hybrid. Try at most two or three, chosen from the framing and the data assessment.
- **Select the provider or model for the spike.** A hosted API is usually the fastest; note data
  restrictions that rule it out.
