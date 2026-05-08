# CIK v0.6 Instrument Plugin Contract

## Purpose

CIK v0.6 introduces a contract-aware instrument registry.

Every CIK instrument must declare:

1. name
2. version
3. description
4. input contract
5. output contract
6. evidence contract
7. capabilities
8. downgrade policy
9. non-claim locks

## Minimum output contract

Every instrument must emit, or explicitly justify not emitting:

- state
- ledger
- evidence

Recommended full output surface:

- state
- ledger
- evidence
- report
- semantic

## Non-claim locks

Instrument registry presence is not instrument validation.

Plugin contract conformance is not code correctness.

Instrument capability declaration is not external validation.

CIFScore is not truth.

Maturity is not correctness.

RootMirror Full is not a security proof.

## v0.6 integration surface

CIK v0.6 consumes RootMirror Full evidence in core scoring and downgrade reconciliation, then applies the same evidence-contract discipline to instruments through the registry.

This does not make CIK an autonomous system, a truth engine, a security framework, or a proof of correctness.