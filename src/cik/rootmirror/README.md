# RootMirror-lite Module

## Purpose

This folder implements the CIK v0.2 RootMirror-lite local continuity verifier.

RootMirror-lite verifies that a local CIK run starts from an anchored root, emits expected artifacts, hashes the authoritative state artifact, appends the ledger exactly once, and returns to root.

## S — Formal specification

RootMirror-lite checks:

- root anchor exists,
- required artifacts exist,
- state SHA-256 hash is computed,
- ledger append delta equals one,
- post-run working directory returns to pre-run directory or repository root.

Required artifact classes:

- state
- ledger
- evidence
- report
- semantic

## H — Hooks

This module hooks into:

- `scripts/rootmirror_lite_smoke.py`
- `scripts/run_rootmirror_lite_smoke.ps1`
- `outputs/rootmirror`
- `outputs/state`
- `outputs/evidence`
- tests under `tests/test_rootmirror_lite.py`

## A — Artifacts

RootMirror-lite emits:

- `outputs/rootmirror/*_rootmirror_lite.json`
- `outputs/rootmirror/*_rootmirror_lite_report.md`

It may also inject RootMirror-lite continuity references into:

- state JSON artifacts
- evidence package JSON artifacts

## T — Theory

Basis:

- CIK v0.2 RootMirror-lite Continuity Layer
- CIF v2.1 verify stage
- RootMirror continuity discipline
- State-first artifact authority
- Ledger Echo append-only continuity trace

## I — Invariants

- RootMirror-lite is not full RootMirror.
- RootMirror-lite is not a security proof.
- State hash is not truth.
- Ledger append is not correctness.
- Artifact existence is not validity.
- Continuity is not code correctness.

## E — Example

From repository root:

    $env:PYTHONPATH = ".\src"
    python -m unittest tests.test_rootmirror_lite -v
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_rootmirror_lite_smoke.ps1"