---
id: E24
title: Human Review & Oversight
archetypes: [batch-pipeline, agent, llm-service]
requires: optional
applies_when: human_review == yes
depends_on: [E10]
phase: build
---

## Description

Keep a person in the loop where the AI output is uncertain or consequential: route work to people by
confidence or risk, make review quick, and learn from what they change.

## Outcome

Work above the agreed risk or below the agreed confidence reaches a person through a defined queue or
approval step, every decision is recorded, and the rate at which people change the AI's output is measured.

## Scope (in)

- Routing rules: auto-accept above a confidence threshold, and send to a person below it or above a risk
  level.
- [cap: sampled-audit, tier: production] Sample the auto-accepted work to measure the real error rate.
- Review interface or queue showing the item or proposed action, the evidence and the expected impact, with
  approve, edit and reject.
- Audit trail: who decided what and when, and what they changed.
- Ownership, SLA and backlog alert for the queue; timeouts and the default when nobody answers.
- Escalation and handover when the system is stuck or uncertain.
- Override and edit rates measured, to tune thresholds and autonomy.
- Corrections flow into the evaluation set, as described in Evaluation & Quality.

## Scope (out)

- A general workflow product for reviewers.
- Fully automated acceptance without sampling.

## Decisions

- **Where does review happen?** A custom interface, an annotation tool (Label Studio and similar), the chat
  itself, or a ticketing or spreadsheet workflow. Based on reviewer count, volume and how much context a
  reviewer needs.
- **Set the thresholds and the timeout default.** Confidence and risk levels from the evaluation set and the
  review capacity; abort or hold when an approval times out.

## Archetype notes

- **batch-pipeline:** adds automatic validation before routing (schema, ranges, cross-field consistency,
  business rules); thresholds come from the precision measured on the evaluation set at each level; reviewer
  corrections are exported for later prompt or model improvement.
- **agent:** the approval gates are the action classes and autonomy levels from Agent Design; add the
  ability to interrupt and kill a run mid-way and to revoke its access.
- **llm-service:** optional review of flagged, high-risk or low-confidence answers before or after they reach
  the user; the feedback loop feeds the golden dataset.
