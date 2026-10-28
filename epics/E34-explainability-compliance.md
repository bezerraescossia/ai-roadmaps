---
id: E34
title: Explainability, Fairness & Compliance
archetypes: [classical-ml, perception]
requires: optional
applies_when: regulated == yes
depends_on: [E29]
phase: harden
---

## Description

Meet explainability, fairness and documentation obligations when predictions affect people or are
regulated.

## Outcome

Predictions can be explained to the people affected and to auditors, bias has been measured across the
relevant groups, and the documentation the regulation requires exists.

## Scope (in)

- Applicable obligations identified (for example a right to explanation, anti-discrimination rules, sector
  model-risk rules, the EU AI Act risk class).
- Explanations: global feature importance and a per-prediction explanation in a form the user of the
  prediction can understand.
- Fairness assessment: performance and error rates by protected or sensitive group, with a documented
  tolerance and what to do when it is exceeded.
- Human oversight: which decisions a person reviews or can override, and the appeal path.
- Audit trail: data lineage, evaluation record and decision log. The model card itself belongs to Model
  Registry & Versioning.

## Scope (out)

- Legal advice; the obligations list is confirmed by the compliance owner.

## Decisions

- **Which fairness criterion applies?** For example demographic parity, equalised odds, or none beyond
  monitoring. Decided with the compliance owner.
- **Explainable model or post-hoc explanation?** A simpler interpretable model, or a complex one with
  SHAP-style explanations.

## Archetype notes

- **perception:** explainability may mean saliency or attention maps for vision; add biometric and privacy obligations and fairness across demographic groups.
