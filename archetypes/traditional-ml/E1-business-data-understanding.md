---
id: E1
title: Business & Data Understanding
phase: business-data-understanding
depends_on: []
weight: 2
loops_back_to: []
---

## Description

Define what the model is for and prove, before building, that the project is feasible: measurable success
criteria, a non-ML benchmark, and data that is available and good enough.

## Outcome

Business, ML and economic success criteria are written down and measurable, a heuristic benchmark exists, the
project is judged feasible, and the data's statistics, origin and requirements are documented.

## Tasks

- Define the scope and the success criteria.
- Define KPIs, for example time saved per user and session.
- Set a non-ML heuristic benchmark the model has to beat.
- Assess feasibility, for example with the ML Canvas.
- Collect the data and verify it.
- Build a proof of concept.
- Plan how to obtain labels. `[labeled_data=no|partial]` (added)
- Record the cost of a wrong prediction and use it to set the success thresholds. (added)

## Outputs

- Measurable business, ML and economic success criteria.
- The heuristic benchmark and its result.
- A feasibility assessment.
- Documented data statistics, data-generating process and data requirements.

## Quality assurance

- **Risks:** the project is infeasible; goals cannot be measured; data quality is poor.
- **Metrics:** measurable KPIs and success criteria.
- **Mitigations:** a feasibility check before the project is set up; documented data properties; data
  quality verification.

## Decisions

- **Select the primary ML success metric and its threshold.** Derive it from `task_type` and `use_case`. (added)
- **Select the benchmark.** A rule, a last-value or majority baseline, or the current manual process. (added)
- **Go or stop.** Proceed only if the feasibility assessment supports the success criteria.

## Loop-backs

None. This is where the project starts, and a failed feasibility check ends it here.

## Open questions

Filled from `unsure` intake answers; none by default.
