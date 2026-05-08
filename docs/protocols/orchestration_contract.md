# CIK v0.7 Orchestration Contract

## Purpose

CIK v0.7 adds governed multi-instrument orchestration.

It requires:

1. Run plan emission.
2. Registry validation before execution.
3. Per-instrument result records.
4. Per-instrument status preservation.
5. Cross-instrument evidence composition.
6. Composed downgrade surface.
7. Orchestration state object.
8. Orchestration evidence package.
9. Partial-failure preservation.
10. Non-claim lock preservation.

## Non-claim boundary

Orchestration is not correctness.

Composition is not truth.

Multi-instrument agreement is not external validation.

Registry validity is not instrument validity.

Evidence composition is not a security proof.

## First implementation rule

The first v0.7 implementation should orchestrate the existing `rcc-drift` instrument only. New scientific instruments should be added only after the orchestration substrate passes.