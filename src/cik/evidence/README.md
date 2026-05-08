# src/cik/evidence

## Purpose

Evidence package construction.

## S — Formal specification

Builds structured evidence packages from state and artifact paths.

## H — Hooks and integration edges

Called by rcc-drift fossilize stage.

## A — Artifacts and code units

package.py.

## T — Theory / basis

RCC claim/evidence discipline and CIF artifact packaging.

## I — Invariants

Evidence packages must preserve non-claim locks.

## E — Example usage

build_evidence_package(state, artifact_paths).

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.