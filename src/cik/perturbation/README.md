# Perturbation Module

## Purpose

This folder implements CIK v0.3 perturbation sweep validation.

It verifies that the repository-context drift measurement responds to controlled damage and recovers after restoration.

## S — Formal specification

Required sweep states:

- baseline
- perturbed
- restored

Required checks:

- DeltaPhi rises under perturbation.
- Omega falls under perturbation.
- DeltaPhi recovers after restoration.
- Omega recovers after restoration.
- Sweep evidence is emitted.

## H — Hooks

This module hooks into:

- `scripts/run_perturbation_sweep.py`
- `scripts/run_perturbation_sweep.ps1`
- `outputs/perturbation`
- `outputs/evidence`
- `tests/test_perturbation_sweep.py`
- `tests/test_perturbation_failure_modes.py`

## A — Artifacts

Expected outputs:

- `outputs/perturbation/*_perturbation_sweep.json`
- `outputs/perturbation/*_perturbation_sweep_report.md`
- `outputs/evidence/*_perturbation_evidence_package.json`

## T — Theory

Basis:

- CIK v0.3 Perturbation Sweep Validation Layer
- CIF v2.1 perturbation coverage
- RCC v1.3 repository-context drift
- DeltaPhi response and Omega recovery

## I — Invariants

- Perturbation sweep is not code correctness.
- Fixture response is not universal validation.
- Omega recovery is not truth.
- CIFScore is not truth.
- RCC drift is not runtime correctness.

## E — Example

From repository root:

    $env:PYTHONPATH = ".\src"
    python ".\scripts\run_perturbation_sweep.py" --fixture ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs"