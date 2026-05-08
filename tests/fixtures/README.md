# tests/fixtures

## Purpose

Fixture repositories for deterministic local testing.

## S — Formal specification

Fixtures provide small repositories with and without RCC context.

## H — Hooks and integration edges

Consumed by rcc-drift tests and CLI smoke tests.

## A — Artifacts and code units

tiny_repo and tiny_repo_with_context.

## T — Theory / basis

Small fixtures provide bounded test environments.

## I — Invariants

Fixtures should stay minimal and deterministic.

## E — Example usage

tests/fixtures/tiny_repo_with_context is expected to produce DeltaPhi_repo = 0.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.