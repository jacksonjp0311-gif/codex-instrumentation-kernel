# tests/fixtures/tiny_repo_with_context

## Purpose

Tiny repository with valid RCC context declaration.

## S — Formal specification

Used to prove rcc-drift can produce zero drift against matching declared paths and evidence.

## H — Hooks and integration edges

Consumed by CLI smoke tests and rcc-drift tests.

## A — Artifacts and code units

src/app.py, tests/test_app.py, docs/architecture/rcc_context_map.json.

## T — Theory / basis

Fixture-level context alignment.

## I — Invariants

This fixture should keep DeltaPhi_repo = 0 unless a test is intentionally changed.

## E — Example usage

python -m cik run --instrument rcc-drift --repo .\tests\fixtures\tiny_repo_with_context --out .\outputs

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.