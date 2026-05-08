# src/cik/core

## Purpose

Core CIF runtime logic.

## S — Formal specification

Defines instrumentation loop, metrics, CIFScore, maturity classification, and non-claim locks.

## H — Hooks and integration edges

Imported by instruments and CLI runtime.

## A — Artifacts and code units

loop.py, metrics.py, scoring.py, maturity.py, classification.py, locks.py.

## T — Theory / basis

CIF v2.1 runtime spine.

## I — Invariants

Core scoring and locks must remain conservative. Do not inflate maturity without evidence.

## E — Example usage

Use omega_from_dphi to derive stability from residual.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.