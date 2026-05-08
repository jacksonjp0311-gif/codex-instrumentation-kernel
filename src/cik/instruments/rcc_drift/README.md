# src/cik/instruments/rcc_drift

## Purpose

RCC Drift Instrument implementation.

## S — Formal specification

Measures drift between declared repository context and observed repository surfaces.

## H — Hooks and integration edges

Loaded by src/cik/instruments/registry.py.

## A — Artifacts and code units

instrument.py, drift_metrics.py, reference_loader.py, scanner.py, defaults.py, manifest.json.

## T — Theory / basis

RCC v1.3 context drift and CIF residual measurement.

## I — Invariants

RCC drift is not code correctness. Missing context should not crash the instrument.

## E — Example usage

python -m cik run --instrument rcc-drift --repo .\tests\fixtures\tiny_repo_with_context --out .\outputs

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.