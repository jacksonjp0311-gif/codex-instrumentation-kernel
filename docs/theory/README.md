# docs/theory

## Purpose

Theory summaries for CIF, RCC, and AIT/HYDRA as used by CIK.

## S — Formal specification

Theory docs summarize imported framework layers in implementation-facing terms.

## H — Hooks and integration edges

Docs inform implementation but do not execute.

## A — Artifacts and code units

cif_v2_1_summary.md, rcc_v1_3_summary.md, ait_hydra_summary.md.

## T — Theory / basis

CIF v2.1, RCC v1.3, AIT/HYDRA v1.0.

## I — Invariants

Theory summaries must preserve non-claim locks and additive evolution.

## E — Example usage

Before adding an instrument, read CIF and AIT/HYDRA summaries.

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.