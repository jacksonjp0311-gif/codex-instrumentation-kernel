# src/cik/rcc

## Purpose

Reserved RCC utility and future linter surface.

## S — Formal specification

Future location for RCC validators, README contract logic, TTL checks, and drift-linter rules.

## H — Hooks and integration edges

Future tools may use docs/context repository index.

## A — Artifacts and code units

Currently README only.

## T — Theory / basis

RCC v1.3 linter-tier and evidence-tier governance.

## I — Invariants

Do not claim RCC linter exists until runtime code and tests are added.

## E — Example usage

Future: validate repository_context_index.json.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.