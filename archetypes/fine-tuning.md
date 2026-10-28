---
archetype: fine-tuning
title: Fine-tuning / model adaptation
description: Adapting a pre-trained model (LLM, embedding, vision, speech) to your task with your own data (supervised tuning, parameter-efficient tuning, preference tuning, distillation) and then evaluating, packaging and serving it.
exposes: E31
library_version: 0.7.0
source: drafted from general practice; to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: fine-tuning / model adaptation

Use when the plan is to change a model's weights: to fit a format or style, to lower cost or latency with a
smaller model, to add a narrow skill, or to specialise an embedding or vision model. The roadmap puts the
baselines and the evaluation harness before training, because most fine-tuning projects fail on evaluation,
not on training.

Not for prompting or retrieval alone (use `llm-service`) and not for classical models trained from scratch
(use `classical-ml`). Adaptation Strategy exists to confirm that tuning is needed; if prompts and retrieval
are enough, the roadmap should stop there.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: use_case
    ask: What should the adapted model do better, and how will you know (quality, latency, cost, format)?
    feeds: Vision & End States
  - id: model_kind
    ask: What kind of model is being adapted?
    values: [llm, embedding, vision, speech, other]
    feeds: Notes on the strategy spec
  - id: method
    ask: Which method do you expect?
    values: [full, lora, preference, distill, unsure]
  - id: labeled_data
    ask: Do you already have training examples (inputs with the desired outputs or preferences)?
    values: [yes, partial, no]
  - id: hosting
    ask: How will the tuned model be served?
    values: [api, self-hosted, unsure]
  - id: continuous
    ask: Will the model be retrained on production feedback over time?
    values: [yes, no]
  - id: licence_limits
    ask: Which base models are allowed by licence, data policy or procurement?
    feeds: Constraints & Decisions
  - id: compute
    ask: What GPU access and training budget exist?
    feeds: Constraints & Decisions
  - id: sensitive_data
    ask: Does the training data contain personal, confidential or regulated content, and may it leave your environment?
    feeds: Constraints & Decisions
  - id: constraints
    ask: Other fixed technology, hosting or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `hosting: unsure` leaves the serving-mode bullets out of Packaging & Serving and adds an Open Question.
- `labeled_data` `no` or `partial`: warn that tuning without examples needs a data plan; the labeling plan
  in Data Assessment and the synthetic-data decision in Training Data apply.
- `continuous: yes` includes monitoring and retraining (E32, E33); `no` omits them.
- Packaging and serving reuse the Model Registry and Model Serving epics; their "Archetype notes" for
  `fine-tuning` apply, and the serving bullets are chosen by `hosting`, not `serving`.

## Epic overrides

```yaml
epic_rules:
  E15: {depends_on: [E31, E45, E47]}
  E30: {depends_on: [E44, E47]}
  E31: {depends_on: [E30]}
  E32: {applies_when: "continuous == yes", depends_on: [E31]}
  E33: {applies_when: "continuous == yes", depends_on: [E45, E47, E30, E32]}
```

## Bundles

`E16` is discovery and never becomes a spec. A bundle with no selected members is omitted.

```yaml
bundles:
  - title: Data assessment
    members: [E17]
  - title: Adaptation strategy
    members: [E41]
  - title: Training data
    members: [E42]
  - title: Training pipeline
    members: [E43]
  - title: Evaluation harness
    members: [E45]
  - title: Training & iteration
    members: [E44]
  - title: Safety, licensing & governance
    members: [E47]
  - title: Packaging & serving
    members: [E30, E31]
  - title: Monitoring & improvement
    members: [E32, E33]
  - title: Deployment & launch readiness
    members: [E15]
```

## Ordering

A bundle depends on the bundles of its members' `depends_on`. Specs are sorted topologically (ties broken
by phase, then epic id) and numbered 001..N. The evaluation harness is ready before the first training run,
and safety and licensing review sits between training and packaging.

## Conflicts

If a selected epic needs an unselected one (for example training runs without an evaluation harness), warn,
name the dependency and why it exists, and let the user decide. Record the outcome as `deferred` or
`abandoned` with the reason.
