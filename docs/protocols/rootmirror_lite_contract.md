# RootMirror-lite Contract

## Purpose

RootMirror-lite is the CIK v0.2 local continuity verification protocol.

It verifies that a run:

1. starts from a declared repository root,
2. records the pre-run working directory,
3. runs the selected instrument,
4. emits required artifacts,
5. hashes the state artifact,
6. appends the ledger exactly once,
7. records the post-run working directory,
8. returns to root,
9. emits RootMirror-lite JSON and Markdown reports.

## Required checks

| Check | Required result |
|---|---|
| Root anchor | repo root exists |
| Artifact manifest | state, ledger, evidence, report, semantic exist |
| State hash | SHA-256 computed |
| Ledger append | append delta equals one |
| Return-to-root | post-run cwd equals pre-run cwd or repo root |

## Required outputs

- `outputs/rootmirror/*_rootmirror_lite.json`
- `outputs/rootmirror/*_rootmirror_lite_report.md`

## Non-claim locks

RootMirror-lite is not:

- full RootMirror,
- security proof,
- code correctness proof,
- semantic truth proof,
- supply-chain attestation,
- tamper-proof provenance.

## Verification commands

    $env:PYTHONPATH = ".\src"
    python -m unittest tests.test_rootmirror_lite -v
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_rootmirror_lite_smoke.ps1"

## Downgrade discipline

If RootMirror-lite passes, downgrade wording may change from:

    RootMirror verification not enabled.

to:

    Full RootMirror verification not enabled; RootMirror-lite local continuity only.

If RootMirror-lite fails, the system must disclose:

    RootMirror-lite continuity verification failed.