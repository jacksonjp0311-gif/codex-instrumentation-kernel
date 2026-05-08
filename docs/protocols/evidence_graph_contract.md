# CIK v0.8 Evidence Graph Contract

## Purpose

CIK v0.8 adds a local evidence graph and cross-run query layer.

The graph connects:

1. runs
2. instruments
3. artifacts
4. evidence packages
5. RootMirror records
6. Tesseract-lite records
7. orchestration bundles
8. downgrades
9. claim boundaries

## Required behavior

- Build from outputs read-only.
- Emit `outputs/evidence_graph/evidence_graph.json`.
- Emit `outputs/evidence_graph/evidence_graph_report.md`.
- Emit `outputs/evidence/evidence_graph_evidence_package.json`.
- Mark inferred, missing, ambiguous, and orphan relations.
- Preserve non-claim locks.
- Provide deterministic query functions.

## Non-claim boundary

Graph linkage is not truth.

Queryability is not correctness.

Artifact lineage is not provenance.

Graph completeness is not evidence completeness.

Evidence graph is not autonomous memory.