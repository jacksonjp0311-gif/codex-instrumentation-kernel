# configs

## Purpose

Configuration root for CIK runtime defaults, instrument policies, RCC policy, and injection policy.

## S — Formal specification

Config files declare runtime defaults. They do not override source code behavior unless explicitly loaded by runtime code.

## H — Hooks and integration edges

Read by CLI/runtime layers when configuration loading is enabled. Current v0.1 uses mostly code defaults.

## A — Artifacts and code units

cik_default.json and subfolder configs.

## T — Theory / basis

CIF configuration discipline: declared parameters must remain visible and auditable.

## I — Invariants

Do not hide runtime behavior in undocumented config. Do not treat config declaration as execution evidence.

## E — Example usage

Update configs/instruments/rcc_drift_default.json only when drift weights change.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.