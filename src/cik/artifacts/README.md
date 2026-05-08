# src/cik/artifacts

## Purpose

Artifact writer surface.

## S — Formal specification

Writes JSON, JSONL, text, markdown reports, and artifact hashes.

## H — Hooks and integration edges

Called by instrument fossilize stage.

## A — Artifacts and code units

writers.py, report_writer.py.

## T — Theory / basis

CIF fossilization layer.

## I — Invariants

Writers should be deterministic and simple. Do not interpret metrics here.

## E — Example usage

append_jsonl writes ledger records.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.