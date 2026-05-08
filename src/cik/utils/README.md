# src/cik/utils

## Purpose

Shared utility functions.

## S — Formal specification

Contains safe JSON helpers, hashing helpers, and UTC timestamp helpers.

## H — Hooks and integration edges

Imported across core, instruments, artifacts, and injection.

## A — Artifacts and code units

safe_json.py, hashing.py, time.py.

## T — Theory / basis

Deterministic artifact and hash discipline.

## I — Invariants

Utility functions should not contain domain-specific claims.

## E — Example usage

stable_hash creates deterministic SHA-256 hashes for JSON-like objects.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.