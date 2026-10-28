---
archetype: agent
title: Autonomous agent / multi-step workflow
description: An LLM system that plans and carries out multi-step tasks by calling tools, with bounded autonomy, state, and human oversight where actions matter.
library_version: 0.7.0
source: drafted from general practice and reuse of the llm-service epics; to be corrected from delivered projects
phases: [discover, build, harden, launch]
---

# Archetype: autonomous agent / multi-step workflow

Use when the system decides its own steps and acts through tools: a support agent that looks up and updates
records, a research agent, an operations agent that runs commands, a coding or browsing agent. Control flow,
action safety, run-level evaluation and cost per run matter more than single-response quality.

Not for a single prompt-and-answer service, even with retrieval (use `llm-service`), and not for fixed
pipelines over many items (use `batch-pipeline`). If one fixed sequence of LLM calls covers the tasks, Agent
Design should say so, and the roadmap can shrink to the `llm-service` shape.

## Intake

Ask only what the context does not already answer. Record each answer; never fabricate.

```yaml
intake:
  - id: use_case
    ask: What tasks does the agent carry out, for whom, and what does a wrong or harmful action cost?
    feeds: Vision & End States
  - id: interface
    ask: How is the agent used?
    values: [api, chat, background]
  - id: autonomy
    ask: How much may it do without a person (suggest only, act after approval, act alone within limits)?
    values: [assistive, supervised, autonomous]
    feeds: Constraints & Decisions; the decision in Agent Design
  - id: human_oversight
    ask: Must a person approve, review or be able to interrupt some actions?
    values: [yes, no, unsure]
  - id: code_execution
    ask: Does the agent run code, shell commands or a browser?
    values: [yes, no]
  - id: memory
    ask: Must it remember things across runs or conversations?
    values: [yes, no, unsure]
  - id: custom_ml
    ask: Does the agent need a model you train or adapt yourself (a classical ML model, a vision or speech model, a fine-tuned LLM), for example behind one of its tools?
    values: [yes, no, unsure]
  - id: multi_agent
    ask: Do you expect several cooperating agents rather than one?
    values: [yes, no, unsure]
  - id: rag
    ask: Must it ground answers in your own documents or data?
    values: [yes, no, unsure]
  - id: streaming
    ask: Do users watch progress as the agent works?
    values: [yes, no, unsure]
  - id: sensitive_data
    ask: Which sensitive data or systems can the agent reach, and which actions have side effects?
    feeds: Constraints & Decisions; informs Guardrails, Tools and Oversight
  - id: constraints
    ask: Fixed technology, provider, hosting, budget or deadline constraints?
    feeds: Constraints & Decisions (C-nn)
```

Rules:

- `unsure` on an optional epic includes it as `undecided` with an Open Question.
- If tools have side effects and `human_oversight` is `no`, warn, and add an Open Question to Agent Design
  asking for the justification.
- `multi_agent: yes` needs a single-agent baseline; note it in the Agent Design spec.
- `interface: background` removes the gateway epic; the agent is started by a trigger.
- `custom_ml: yes`: ask which kind of model and include that archetype (see "Included archetypes"). Add an
  Open Question on the Tools spec about how the model is exposed to the agent. `unsure` adds the question
  only.

## Epic overrides

```yaml
epic_rules:
  E03: {applies_when: "interface != background"}
  E07: {applies_when: always, depends_on: [E10, E09, E35], after: [E03]}
  E09: {depends_on: [E10]}
  E11: {depends_on: [E10], after: [E03]}
  E14: {depends_on: [E02, E35]}
  E24: {applies_when: "human_oversight == yes", depends_on: [E36], after: [E38]}
  E15: {depends_on: [E10, E12], after: [E03]}
  E02: {depends_on: [E16]}
```

## Bundles

`E16` is discovery and never becomes a spec. A bundle with no selected members is omitted.

```yaml
bundles:
  - title: Foundation
    members: [E02, E03]
  - title: LLM integration & reliability
    members: [E10]
  - title: Guardrails
    members: [E09]
  - title: Agent design
    members: [E35]
  - title: Evaluation & quality
    members: [E14]
  - title: Tools & integrations
    members: [E07]
  - title: Orchestration
    members: [E36]
  - title: Memory & context
    members: [E37]
  - title: Sandbox & execution
    members: [E38]
  - title: Human oversight
    members: [E24]
  - title: Multi-agent coordination
    members: [E40]
  - title: Knowledge retrieval
    members: [E06]
  - title: Streaming
    members: [E11]
  - title: Observability & cost
    members: [E12, E13]
  - title: Deployment & launch readiness
    members: [E15]
```

## Included archetypes

When the project also builds a model of another kind, include that archetype in the same roadmap instead of
starting a second one. Ask the included archetype's intake (skip `constraints`, already answered; read
`use_case` as the model's purpose) and run the planner with `--include`. The included archetype's serving
epic (its `exposes` epic) is ordered before each epic listed in `consumed_by`.

```yaml
includes:
  classical-ml:
    consumed_by: [E07]
  perception:
    consumed_by: [E07]
  fine-tuning:
    consumed_by: [E10]
```

## Ordering

A bundle depends on the bundles of its members' `depends_on`; `after` is a soft ordering that applies only
when both epics are selected. Specs are sorted topologically (ties broken by phase, then epic id) and
numbered 001..N. Agent Design sorts before Tools and Orchestration, and the evaluation tasks follow
directly from it.

## Conflicts

If a selected epic needs an unselected one, warn, name the dependency and why it exists, and let the user
decide. Record the outcome as `deferred` or `abandoned` with the reason.
