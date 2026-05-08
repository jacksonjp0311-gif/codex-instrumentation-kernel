# docs/context

## Purpose

Machine-readable repository context index.

## S — Formal specification

repository_context_index.json declares important paths, commands, claims, evidence paths, staleness, and non-claim locks.

## H — Hooks and integration edges

Used by AI agents and future RCC tooling.

## A — Artifacts and code units

repository_context_index.json.

## T — Theory / basis

RCC v1.3 repository context index and claim/evidence discipline.

## I — Invariants

Context index is orientation evidence, not correctness proof.

## E — Example usage

Update repository_context_index.json when major paths, commands, or claims change.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.