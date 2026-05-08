# scripts

## Purpose

Local helper scripts for tests, local run, and repo dump.

## S — Formal specification

Scripts should call existing runtime commands without hiding behavior.

## H — Hooks and integration edges

Used by humans and AI agents for repeatable local operations.

## A — Artifacts and code units

run_tests.ps1, run_local.ps1, repo_dump_light.ps1.

## T — Theory / basis

RootMirror-style local repeatability discipline.

## I — Invariants

Scripts must return to root and avoid blocking process patterns.

## E — Example usage

powershell -ExecutionPolicy Bypass -File .\scripts\run_local.ps1

## AI maintenance note

When this folder changes, update this mini README and run:

    python -m unittest tests.test_rcc_readmes -v

Do not make stronger claims than the local artifacts support.