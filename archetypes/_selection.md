---
title: Archetype selection (interview 1)
description: Plain questions about the shape of the project, turned into a primary archetype plus included ones by scripts/select_archetypes.py. Not an archetype itself.
---

# Interview 1: which archetypes does the project need?

People starting a project rarely know the archetype names, so ask about the project's shape and derive the
archetypes. Ask only what the constitution, the repo or the conversation do not already answer, then run:

```bash
uv run .specify/extensions/roadmap/scripts/select_archetypes.py --answers '<json of the answers>'
```

It returns the `primary` archetype, the `includes` (model-building archetypes added to the same roadmap),
`unsupported` combinations with the reason, `reasons` in plain words, and `needs` (questions still
unanswered). Show the result and let the user confirm or override it.

## Questions

```yaml
questions:
  - id: purpose
    ask: Is this a feasibility study (does it work well enough to be worth building?), a product to run in production, or the ML platform that other teams will build on?
    values: [feasibility-study, product, platform]
  - id: runtime
    ask: "How does the system run? interactive-service: a request/response API or chat. agent: plans and acts through tools over several steps. batch-pipeline: processes many items offline or on a schedule. model-only: the product is a trained model that is scored in batch or online, with no LLM in the loop. (Product only.)"
    values: [interactive-service, agent, batch-pipeline, model-only]
  - id: own_models
    ask: Which models do you train or adapt yourself? Pick all that apply, or none.
    values: [tabular-or-time-series, images-video-audio, llm-adaptation]
    multiple: true
  - id: use_case
    ask: What problem does this solve, for whom, and what measurable outcome counts as success?
    feeds: Vision & End States
  - id: constraints
    ask: Fixed technology, hosting, provider, budget or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
  - id: sensitive_data
    ask: Which sensitive data or regulatory limits apply, and what is the impact of a wrong or unsafe output?
    feeds: Constraints & Decisions
```

`use_case`, `constraints` and `sensitive_data` are the framing answers shared by every archetype; they are
asked here once, and the archetype interviews skip their free-text versions. Archetype questions that have
fixed `values` (for example a yes/no `sensitive_data`) are still asked in interview 2.

## How the answers map

| Answer | Archetype |
|---|---|
| `purpose: feasibility-study` | `poc` (primary; includes nothing) |
| `purpose: platform` | `ml-platform` (primary; models are the platform's users, not part of it) |
| `runtime: interactive-service` | `llm-service` (primary) |
| `runtime: agent` | `agent` (primary) |
| `runtime: batch-pipeline` | `batch-pipeline` (primary) |
| `runtime: model-only` | the first model archetype in `own_models` (primary) |
| `own_models: tabular-or-time-series` | `classical-ml` |
| `own_models: images-video-audio` | `perception` |
| `own_models: llm-adaptation` | `fine-tuning` |

The archetype that describes how the system runs is primary; model-building archetypes are included in it.
Model-building archetypes cannot include each other, so a model-only product with several kinds of model gets
one roadmap per extra model (reported as `unsupported`).
