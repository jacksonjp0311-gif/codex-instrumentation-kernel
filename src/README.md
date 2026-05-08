# src

## Purpose

Python source root.

## S — Formal specification

Contains importable package code under src/cik.

## H — Hooks and integration edges

PYTHONPATH should include .\src for local execution.

## A — Artifacts and code units

cik package.

## T — Theory / basis

Software implementation surface for CIF loop.

## I — Invariants

Do not place generated artifacts in src.

## E — Example usage

$env:PYTHONPATH = ".\src"

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.