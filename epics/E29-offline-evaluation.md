---
id: E29
title: Offline Evaluation & Validation
archetypes: [classical-ml, perception]
requires: core
applies_when: always
depends_on: [E28]
phase: build
---

## Description

Decide whether the selected model is good enough to release, and where it is weak.

## Outcome

The model's test performance against the baseline and the success thresholds is known, with results by
segment and a documented set of limitations.

## Scope (in)

- Final evaluation once on the held-out test set with the metrics from the framing epic (for example
  precision/recall, ROC-AUC, NDCG, MAE, calibration), compared with the baseline.
- [cap: confidence-intervals, tier: production] Confidence intervals or repeated runs, to show whether differences are real.
- [cap: slice-analysis, tier: critical] Slice analysis: performance by segment (region, customer type, rare classes) and cold-start cases.
- Error analysis: the largest errors read by a person, with causes grouped.
- Business-metric translation: what the metric gain is worth in the process the model supports.
- Release criteria written down and checked, and a limitations note (where not to use the model).

## Scope (out)

- Production monitoring (separate epic).

## Decisions

- **Set the release thresholds.** Minimum metric values, per-slice floors, and who signs off.

## Archetype notes

- **perception:** task metrics such as accuracy and F1, mAP and IoU for detection and segmentation, WER and CER for speech. Test sets are tagged by condition, and the worst errors are reviewed by a person.
