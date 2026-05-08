# configs/rcc

## Purpose

RCC policy configuration surface.

## S — Formal specification

Reserved for RCC profile, TTL, linter-tier, evidence-tier, and README contract policy.

## H — Hooks and integration edges

Future RCC linter and docs/context repository index may consume this.

## A — Artifacts and code units

Policy files may be added in later versions.

## T — Theory / basis

RCC v1.3: context records should be measurable, typed, and stale-aware.

## I — Invariants

RCC policy must not imply code correctness.

## E — Example usage

Future: rcc_policy.json with max_age_days and required README sections.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.