# src/cik/instruments

## Purpose

Instrument registry and instrument base surface.

## S — Formal specification

Every instrument must implement the CIF loop methods and register itself.

## H — Hooks and integration edges

CLI calls registry to load active instruments.

## A — Artifacts and code units

base.py, registry.py, rcc_drift.

## T — Theory / basis

CIF instruments are bounded measurement modules.

## I — Invariants

No instrument without declared residual, omega rule, artifacts, and non-claims.

## E — Example usage

Current instrument: rcc-drift.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.