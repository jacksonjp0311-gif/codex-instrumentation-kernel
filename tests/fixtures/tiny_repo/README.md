# tests/fixtures/tiny_repo

## Purpose

Minimal repo without context declaration.

## S — Formal specification

Used to confirm rcc-drift does not crash when no context map exists.

## H — Hooks and integration edges

Consumed by tests/test_rcc_drift_metrics.py.

## A — Artifacts and code units

placeholder.txt.

## T — Theory / basis

Missing context should be handled safely.

## I — Invariants

Do not make this fixture complex.

## E — Example usage

Expected behavior: compute_drift returns dphi_global.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.