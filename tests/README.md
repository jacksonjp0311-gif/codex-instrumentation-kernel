# tests

## Purpose

Executable verification surface.

## S — Formal specification

Tests validate metrics, maturity classification, CLI behavior, rcc-drift behavior, and README coverage.

## H — Hooks and integration edges

Run through python -m unittest discover -s tests.

## A — Artifacts and code units

test_*.py and fixture repositories.

## T — Theory / basis

Validation surface requirement.

## I — Invariants

Behavior changes require tests. Passing tests do not prove full correctness.

## E — Example usage

python -m unittest discover -s tests

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.