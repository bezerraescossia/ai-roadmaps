---
archetype: perception
title: Perception model (vision, speech, audio)
description: A model that understands images, video or audio (classification, detection, segmentation, OCR, speech recognition), including data capture and labeling, condition coverage, optional edge deployment, and field validation.
exposes: E31
library_version: 0.9.0
source: drafted from general practice; reuses the classical-ml epics with perception notes; to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: perception model (vision, speech, audio)

Use when the input is media: defect detection, document or ID reading, people or object counting, speech
transcription, audio events. It follows the classical-ML path (data, training, evaluation, registry,
serving, monitoring, retraining) and adds capture and labeling operations, coverage of real-world
conditions, optional edge optimisation, and field validation.

Not for tabular prediction (use `classical-ml`) and not for adapting a large language model (use
`fine-tuning`). A project that only calls a hosted vision or speech API and post-processes the result may
fit `llm-service` or `batch-pipeline` better.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: use_case
    ask: What must the system see or hear, who acts on the result, and what does a miss or a false alarm cost?
    feeds: Vision & End States
  - id: modality
    ask: Which media and task (for example image classification, object detection, OCR, speech recognition)?
    feeds: Notes on the training and evaluation specs
  - id: labeled_data
    ask: Do you already have labeled media?
    values: [yes, partial, no]
  - id: serving
    ask: Where does inference run?
    values: [batch, online, embedded, unsure]
    feeds: Serving spec; `embedded` includes Edge & Device Optimization
  - id: conditions
    ask: In what conditions will it run (lighting, noise, camera or microphone types, accents, environments)?
    feeds: Notes on Augmentation & Coverage and on Robustness & Field Validation
  - id: regulated
    ask: Do the media contain faces, voices or other biometric or personal data, or does a regulation require explanations?
    values: [yes, no, unsure]
  - id: ml_platform
    ask: Is there an existing ML or data platform (tracking, registry, GPUs) to build on?
    feeds: Constraints & Decisions
  - id: constraints
    ask: Fixed hardware, hosting, budget or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `serving: embedded` includes Edge & Device Optimization; `unsure` includes it as `undecided` with an Open
  Question.
- `regulated: unsure` includes the explainability epic as `undecided`.
- `labeled_data` `no` or `partial` adds the labeling plan to Data Assessment and sizes Capture & Labeling.
- When the answers span cloud and device, choose the harder target and note the other.

## Epic overrides

```yaml
epic_rules:
  E27: {depends_on: [E17, E49]}
  E28: {depends_on: [E27, E50]}
  E31: {depends_on: [E30, E64], after: [E51]}
  E15: {depends_on: [E31, E32, E52]}
```

## Bundles

`E16` is discovery and never becomes a spec. A bundle with no selected members is omitted.

```yaml
bundles:
  - title: Serving contract & stub
    members: [E64]
  - title: Data assessment
    members: [E17]
  - title: Capture & labeling
    members: [E49]
  - title: Data pipeline
    members: [E27]
  - title: Augmentation & coverage
    members: [E50]
  - title: Baseline & training
    members: [E28]
  - title: Offline evaluation
    members: [E29]
  - title: Model registry
    members: [E30]
  - title: Edge optimization
    members: [E51]
  - title: Serving & release
    members: [E31]
  - title: Robustness & field validation
    members: [E52]
  - title: Monitoring & drift
    members: [E32]
  - title: Retraining & delivery
    members: [E33]
  - title: Explainability & compliance
    members: [E34]
  - title: Deployment & launch readiness
    members: [E15]
```

## Ordering

A bundle depends on the bundles of its members' `depends_on`; `after` is a soft ordering that applies only
when both epics are selected. Specs are sorted topologically (ties broken by phase, then epic id) and
numbered 001..N.

## Conflicts

If a selected epic needs an unselected one, warn, name the dependency and why it exists, and let the user
decide. Record the outcome as `deferred` or `abandoned` with the reason.
