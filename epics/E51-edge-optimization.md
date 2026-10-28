---
id: E51
title: Edge & Device Optimization
archetypes: [perception]
requires: optional
applies_when: serving == embedded
depends_on: [E30]
phase: build
---

## Description

Fit the model to the memory, latency and power limits of the target device.

## Outcome

The model runs on the target hardware within its limits with the accuracy loss measured, and devices can be updated and rolled back.

## Scope (in)

- Target hardware and its limits: memory, latency, power, thermal.
- Compression: quantisation, pruning, distillation.
- Export and runtime (for example ONNX, TensorRT, Core ML, TFLite), with the accuracy re-checked after each step.
- Benchmarks on real devices, not only simulators.
- Update mechanism (over the air), versioning and rollback on devices.
- Offline behaviour and fallbacks.

## Scope (out)

- Cloud serving (Serving & Release).

## Decisions

- **Select the target runtime and format.** Based on the hardware and the available accelerators.
