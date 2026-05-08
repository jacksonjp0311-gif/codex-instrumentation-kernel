# src/cik

## Purpose

CIK Python package root.

## S — Formal specification

Exposes package version, CLI entrypoint, and module tree.

## H — Hooks and integration edges

python -m cik routes into cli.py.

## A — Artifacts and code units

__init__.py, __main__.py, cli.py, subpackages.

## T — Theory / basis

Executable kernel shell for CIF instrumentation.

## I — Invariants

CLI should remain thin and delegate behavior to core/instruments.

## E — Example usage

python -m cik list-instruments

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.