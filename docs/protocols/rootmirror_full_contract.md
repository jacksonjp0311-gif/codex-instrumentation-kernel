# CIK v0.5 RootMirror Full Contract

## Purpose

RootMirror full verifies local run-envelope continuity for CIK instrumentation runs.

It verifies:

1. Run envelope declaration.
2. Pre-run root anchor.
3. Post-run root anchor.
4. Return-to-root proof.
5. Ledger append delta.
6. Artifact manifest closure.
7. State hash presence.
8. Output-root hash surface.
9. Replay metadata.
10. RootMirror full evidence package.

## Non-claim lock

RootMirror full verifies continuity only.

It does not prove code correctness, runtime correctness, semantic truth, security, supply-chain provenance, artifact meaning, intelligence, consciousness, or autonomous memory.

## Required outputs

- outputs/rootmirror_full/*_rootmirror_full.json
- outputs/rootmirror_full/*_rootmirror_full.md
- outputs/evidence/*_rootmirror_full_evidence_package.json