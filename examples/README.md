# examples

## Purpose

Example usage surfaces and future demonstration repositories.

## S — Formal specification

Examples illustrate usage but are not benchmark proof.

## H — Hooks and integration edges

May be referenced by docs and tests in later versions.

## A — Artifacts and code units

minimal_repo and future example runs.

## T — Theory / basis

Examples support adoption but do not establish generality.

## I — Invariants

Examples must not be treated as validation benchmarks unless declared and tested.

## E — Example usage

Future: add a minimal repo with a stale RCC record to demonstrate drift increase.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.