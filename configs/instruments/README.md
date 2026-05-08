# configs/instruments

## Purpose

Instrument-specific configuration declarations.

## S — Formal specification

Each instrument may expose weights, thresholds, and policy defaults here.

## H — Hooks and integration edges

Connected to src/cik/instruments when config loading is implemented or manually mirrored.

## A — Artifacts and code units

rcc_drift_default.json.

## T — Theory / basis

RCC and CIF require declared measurement policy.

## I — Invariants

Weight changes must preserve sum and must be reflected in docs if runtime behavior changes.

## E — Example usage

RCC Drift weights are declared for missing paths, staleness, claims, evidence, and commands.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.