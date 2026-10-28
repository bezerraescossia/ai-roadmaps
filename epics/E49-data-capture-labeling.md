---
id: E49
title: Data Capture, Annotation & Labeling Operations
archetypes: [perception]
requires: core
applies_when: always
depends_on: [E17]
phase: build
---

## Description

Collect and label the images, video or audio the model learns from, at the quality and coverage it needs.

## Outcome

A labeled, versioned dataset that covers the real deployment conditions, with measured label quality and documented consent.

## Scope (in)

- Capture plan: devices, sensors, locations and conditions (lighting, noise, angles, accents), and how coverage is checked.
- Consent and privacy: faces, voices, plates and other personal data; on-device processing or redaction; retention.
- Annotation guidelines with examples and edge cases.
- Annotation tooling and workforce (in-house or vendor), with throughput and cost.
- Quality control: a gold set, inter-annotator agreement, and sampled review.
- Versioned label schema, and storage and versioning of the raw media.
- Active learning: choose which examples to label next.

## Scope (out)

- Model training (Baseline & Training).

## Decisions

- **Select the annotation tool and workforce.** Based on volume, data sensitivity and the skill the labeling needs.
