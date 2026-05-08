# configs/injection

## Purpose

AIT/HYDRA injection policy declarations.

## S — Formal specification

Reserved for rules controlling admissible new instruments and theory-layer injections.

## H — Hooks and integration edges

Connected to src/cik/injection/register.py.

## A — Artifacts and code units

Future injection policy files.

## T — Theory / basis

AIT/HYDRA: Anchor -> Inject -> Retract -> Seal.

## I — Invariants

Injection must not weaken existing locks or inflate maturity.

## E — Example usage

Future: require every new instrument to declare residual, omega rule, artifacts, and non-claims.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.