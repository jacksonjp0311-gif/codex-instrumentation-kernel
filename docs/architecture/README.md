# docs/architecture

## Purpose

Architecture maps and implementation context for CIK.

## S — Formal specification

Architecture docs explain how source modules and artifact surfaces fit together.

## H — Hooks and integration edges

Root README and AI agents use this as the second context layer.

## A — Artifacts and code units

rcc_context_map.md.

## T — Theory / basis

CIF loop and RCC context-map discipline.

## I — Invariants

Architecture maps are explanatory. Runtime source and generated state remain authoritative.

## E — Example usage

Use rcc_context_map.md to find the correct folder before patching.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.