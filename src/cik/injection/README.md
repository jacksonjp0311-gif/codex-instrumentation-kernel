# src/cik/injection

## Purpose

AIT/HYDRA injection register logic.

## S — Formal specification

Ensures default injection register exists and records injected framework layers.

## H — Hooks and integration edges

CLI validate-injection-register and instrument fossilize stage.

## A — Artifacts and code units

register.py.

## T — Theory / basis

AIT/HYDRA injection governance.

## I — Invariants

Injection register must not be treated as proof of correctness.

## E — Example usage

python -m cik validate-injection-register --repo .

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.