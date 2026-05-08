# docs

## Purpose

Human and AI documentation root for architecture, context, protocols, and theory summaries.

## S — Formal specification

Docs provide bounded context surfaces. They do not override generated artifacts.

## H — Hooks and integration edges

Root README links here. Agents should read docs/architecture and docs/context before editing.

## A — Artifacts and code units

architecture, context, protocols, theory.

## T — Theory / basis

RCC: structured context exposure reduces repository noise.

## I — Invariants

Docs must not claim stronger evidence than outputs/state and outputs/evidence support.

## E — Example usage

Read docs/architecture/rcc_context_map.md before modifying src/cik.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.