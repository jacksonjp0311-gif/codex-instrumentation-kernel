# src/cik/schemas

## Purpose

JSON schema surface for CIK artifacts.

## S — Formal specification

Schemas define required fields for state, ledger, evidence, instrument manifest, and injection register.

## H — Hooks and integration edges

Future validators may load these schemas.

## A — Artifacts and code units

*.schema.json.

## T — Theory / basis

Artifact contract discipline.

## I — Invariants

Schema changes must preserve generated artifact compatibility or declare migration.

## E — Example usage

cif_state.schema.json declares required state fields.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.