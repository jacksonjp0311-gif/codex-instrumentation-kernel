# Protocols

## Purpose

This folder stores operating protocols for CIK.

## S — Formal specification

Protocols define execution discipline that spans multiple code folders.

Current protocol surfaces:

- RootMirror-lite local continuity verification
- future perturbation sweep protocol
- future Tesseract-lite indexing protocol

## H — Hooks

Protocol documents are used by:

- root README,
- AI/agent operating contract,
- implementation scripts,
- tests,
- future RCC context index updates.

## A — Artifacts

Protocol documents are Markdown files.

## T — Theory

Protocols translate Codex theory locks into executable repository behavior.

## I — Invariants

- Protocols do not prove correctness.
- Protocols must preserve non-claim locks.
- Protocols must remain additive unless explicitly versioned as breaking.
- Protocols must distinguish local verification from full security/provenance claims.

## E — Example

RootMirror-lite protocol:

    docs/protocols/rootmirror_lite_contract.md