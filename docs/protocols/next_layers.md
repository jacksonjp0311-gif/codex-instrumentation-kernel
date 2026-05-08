# CIK Next Layers

## v0.2 candidate: RootMirror-lite

Add:

- root anchor verification,
- artifact emission check,
- ledger append-once check,
- state hash check,
- return-to-root check.

Non-claim:

RootMirror-lite is continuity verification, not security proof.

## v0.3 candidate: perturbation sweep

Add controlled repository-context perturbations:

- remove declared path,
- remove evidence path,
- stale record toggle,
- unsupported claim toggle,
- command undeclared toggle.

Expected behavior:

DeltaPhi_repo rises and Omega_repo falls.

## v0.4 candidate: Tesseract-lite index

Add bounded artifact registry:

    run_id -> state_hash -> artifact_paths

Non-claim:

Tesseract-lite is an index, not an agent.