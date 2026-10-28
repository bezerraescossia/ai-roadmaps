---
id: E61
title: Governance, Security & Access
archetypes: [ml-platform]
requires: core
applies_when: always
depends_on: [E56]
phase: harden
---

## Description

Control who can do what with data and models, and make the platform auditable.

## Outcome

Access is role-based, production promotion needs approval, documentation requirements follow a model risk tier, and actions are auditable.

## Scope (in)

- Role-based access to data, models and endpoints.
- Secrets management and audit logs.
- Approval workflow for promotion to production.
- Model risk tiers with the documentation required for each.
- Compliance mapping (for example GDPR, sector rules, EU AI Act) when `regulated` is `yes`.
- Personal-data and retention policies.
- Vulnerability management.

## Scope (out)

- Legal advice; obligations are confirmed by the compliance owner.

## Decisions

- **Define the risk tiers.** Criteria for each tier and the requirements that follow from it.
