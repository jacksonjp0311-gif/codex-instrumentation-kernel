# CIK Tesseract-lite

## Purpose

Tesseract-lite indexes emitted CIK artifacts into a bounded, hash-linked, queryable evidence surface.

## S — Formal specification

Artifact -> path -> type -> SHA-256 hash -> run binding -> index record -> non-claim locks.

## H — Hooks

- Reads outputs/state.
- Reads outputs/ledger.
- Reads outputs/evidence.
- Reads outputs/reports.
- Reads outputs/semantic.
- Reads outputs/rootmirror.
- Reads outputs/perturbation.
- Writes outputs/tesseract.

## A — Artifacts

- outputs/tesseract/tesseract_lite_index.json
- outputs/tesseract/tesseract_lite_index.md
- outputs/tesseract/tesseract_lite_evidence_package.json

## T — Theory

Tesseract-lite implements the CIK v0.4 artifact indexing layer.

## I — Invariants

- Artifact indexing is not truth.
- Hash presence is not correctness.
- Run linkage is not provenance.
- Tesseract-lite is not full Codex Tesseract.
- Tesseract-lite is not memory agency.

## E — Example

Run:

    python -m cik.tesseract --out ".\outputs"