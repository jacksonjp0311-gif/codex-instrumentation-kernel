# Codex Instrumentation Kernel

**Current version:** CIK v0.7 — Multi-Instrument Execution Orchestration and Cross-Instrument Evidence Composition Layer  
**Status:** Runnable local-first Codex instrumentation kernel with RCC drift measurement, RootMirror-lite continuity, perturbation sweep validation, Tesseract-lite artifact indexing, Full RootMirror run-envelope verification, RootMirror Full evidence consumption, downgrade reconciliation, CIFScore v0.6 scoring, maturity v0.6 classification, contract-aware instrument registry governance, and v0.7 multi-instrument orchestration with composed evidence artifacts.  
**Author:** James Paul Jackson / @unifiedenergy11

---

# PART I — HUMAN README

## Human Summary

Codex Instrumentation Kernel, or **CIK**, is a compact software kernel for turning the Codex ΔΦ framework into executable instrumentation.

CIK does not claim intelligence, consciousness, truth, security, formal verification, supply-chain provenance, autonomous memory, or code correctness. It measures repository-context drift, emits evidence artifacts, validates controlled perturbation behavior, indexes outputs into a hash-linked artifact surface, verifies local run envelopes, consumes verification evidence conservatively, reconciles downgrade reasons, validates instrument contracts, and now orchestrates registry-valid instruments through an explicit run plan.

CIK v0.7 adds the **Multi-Instrument Execution Orchestration and Cross-Instrument Evidence Composition Layer**:

- Declares an orchestration run plan before execution.
- Validates the instrument registry before orchestration.
- Executes enabled registry-valid instruments.
- Emits per-instrument result records.
- Preserves skipped, blocked, failed, warning, and passing instruments.
- Composes evidence without merging claim types.
- Emits a composed downgrade surface.
- Emits orchestration state JSON.
- Emits orchestration evidence packages.
- Preserves RootMirror Full compatibility.
- Preserves Tesseract-lite compatibility.
- Preserves CIF-B classification and non-claim locks.
- Treats optional blocked/skipped/failed instruments as warnings, not clean passes.
- Treats required blocked/failed instruments as orchestration failures.

The latest validated v0.7 repair semantics are:

- Required fail/blocked → **fail**
- Optional fail/blocked/warning/skipped → **warning**
- All clean → **pass**

The current local verification surface has passed:

- v0.7 focused orchestration tests
- v0.6 compatibility tests
- README/RCC tests
- Full unit suite: **72 tests OK**
- v0.7 orchestration smoke
- RootMirror Full compatibility smoke
- Tesseract-lite compatibility
- v0.6 integrated compatibility smoke

## What This Is

- A Codex ΔΦ software instrumentation kernel.
- A CIF v2.1-aligned artifact-emitting runtime.
- An RCC v1.3-readable repository context system.
- An AIT/HYDRA-compatible injection target.
- A repository-context drift instrument.
- A RootMirror-lite continuity system.
- A perturbation sweep validation runtime.
- A Tesseract-lite artifact indexing layer.
- A Full RootMirror run-envelope verification layer.
- A RootMirror Full evidence consumption layer.
- A conservative CIFScore / maturity / downgrade reconciliation layer.
- A contract-aware instrument registry.
- A multi-instrument orchestration substrate.
- A cross-instrument evidence composition system.
- A local-first evidence compiler for Codex instrumentation runs.
- A testable Python package with state, ledger, evidence, report, semantic, RootMirror, Tesseract, and orchestration artifacts.

## What This Is Not

- Not autonomous intelligence.
- Not consciousness.
- Not a truth engine.
- Not proof of code correctness.
- Not proof of runtime correctness.
- Not proof of repository quality.
- Not a security audit.
- Not supply-chain provenance.
- Not formal verification.
- Not full Codex Tesseract.
- Not autonomous memory.
- Not external validation.
- Not permission to treat coherence as truth.
- Not permission to treat artifact hashes as semantic validity.
- Not permission to treat RootMirror Full as a security proof.
- Not permission to treat continuity as correctness.
- Not permission to treat orchestration as correctness.
- Not permission to treat evidence composition as truth.
- Not permission to treat multi-instrument agreement as external validation.
- Not permission to hide skipped, blocked, failed, or warning instruments.

## Version Lineage

| Version | Layer | Status |
|---|---|---|
| v0.1 | Kernel Genesis + RCC Drift Instrument | Complete |
| v0.2 | RootMirror-lite Continuity Layer | Complete |
| v0.2C | CIFScore + RootMirror-lite Maturity Integration | Complete |
| v0.3 | Perturbation Sweep Validation Layer | Complete |
| v0.3B | Datetime + README Alignment Patch | Complete |
| v0.3C | Core Scoring Integration Patch | Complete |
| v0.4 | Tesseract-lite Artifact Indexing Layer | Complete |
| v0.5 | Full RootMirror Verification Layer | Complete |
| v0.6 | Core Scoring, Maturity, Downgrade, and Instrument Registry Integration Layer | Complete |
| v0.7 | Multi-Instrument Execution Orchestration and Cross-Instrument Evidence Composition Layer | Current |
| v0.8 | Evidence Graph and Cross-Run Query Layer | Next |
| v0.9 | Full Tesseract and Dashboard-Ready Package | Planned |
| v1.0 | Stable Local-First CIK Release | Target |

---

# PART II — AI RECONSTRUCTION README

## AI Reconstruction Summary

This repository is an executable Codex ΔΦ instrumentation kernel.

Use this README as the first reconstruction surface, then inspect:

1. `docs/context/repository_context_index.json`
2. `docs/architecture/rcc_context_map.md`
3. `docs/protocols/rootmirror_full_contract.md`
4. `docs/protocols/instrument_plugin_contract.md`
5. `docs/protocols/orchestration_contract.md`
6. `configs/instruments/instrument_registry.json`
7. `configs/orchestration/default_run_plan.json`
8. `src/cik/`
9. `src/cik/rootmirror_full/`
10. `src/cik/core/`
11. `src/cik/instruments/`
12. `src/cik/orchestration/`
13. `tests/`
14. `outputs/state/`
15. `outputs/ledger/`
16. `outputs/evidence/`
17. `outputs/rootmirror/`
18. `outputs/rootmirror_full/`
19. `outputs/perturbation/`
20. `outputs/tesseract/`
21. `outputs/orchestration/`

Do not infer claims beyond emitted artifacts, source files, tests, and declared non-claim locks.

## AI Operating Contract

When using an AI assistant on this repo:

1. Start with this README.
2. Read the repository context index.
3. Read the RCC context map.
4. Inspect affected modules before patching.
5. Preserve v0.1-v0.7 behavior.
6. Run tests before claiming success.
7. Keep non-claim locks intact.
8. Update README and mini READMEs when architecture changes.
9. Do not treat generated artifacts as truth.
10. Do not promote maturity without evidence.
11. Do not treat RootMirror Full as correctness proof.
12. Do not remove downgrade reasons without a passing validation surface.
13. Do not treat orchestration as correctness.
14. Do not treat composed evidence as truth.
15. Do not hide failed, skipped, blocked, or warning instruments.
16. Do not advance toward v0.8 until v0.7 remains clean from HEAD.

## RCC Documentation Contract

This repository uses RCC-style documentation as a human/AI reconstruction surface.

Required RCC surfaces:

1. Root README with human-facing summary.
2. AI operating contract.
3. RCC documentation contract.
4. Repository context index.
5. RCC context map.
6. Mini READMEs in required subsections.
7. Validation commands.
8. Non-claim locks.
9. Version lineage.
10. Current downgrade surface.
11. RootMirror Full protocol contract.
12. Instrument plugin contract.
13. Orchestration contract.
14. Current local verification surface.

RCC documentation improves orientation and maintenance discipline. It does not prove code correctness, runtime correctness, security, truth, or artifact meaning.

## AI non-claim lock

AI assistants working on this repository must preserve the following boundary:

CIK helps reconstruct, inspect, patch, test, and document repository instrumentation context. It does not prove code correctness, runtime correctness, semantic truth, security, intelligence, consciousness, autonomous memory, external validity, or artifact meaning.

AI assistants must not:

1. Treat README context as source truth.
2. Treat RCC context as code correctness.
3. Treat passing README tests as full repository validation.
4. Treat Tesseract-lite indexing as memory agency.
5. Treat SHA-256 hashes as semantic validity.
6. Treat CIFScore as truth.
7. Treat RootMirror-lite continuity as Full RootMirror verification.
8. Treat RootMirror Full verification as code correctness.
9. Treat orchestration as correctness.
10. Treat composed evidence as truth.
11. Treat multi-instrument agreement as external validation.
12. Promote maturity classification without emitted evidence.
13. Remove downgrade reasons without a passing validation surface.
14. Collapse human-facing explanation into AI-only reconstruction.

## Reconstruction Order

Recommended reconstruction order:

1. Root README.
2. Repository context index.
3. RCC context map.
4. RootMirror Full protocol contract.
5. Instrument plugin contract.
6. Orchestration contract.
7. Mini READMEs.
8. Source modules.
9. Tests.
10. Latest state artifacts.
11. Ledger.
12. Evidence packages.
13. Tesseract-lite index.
14. RootMirror Full verification output.
15. Orchestration state and evidence output.

## Non-Claim Locks for AI Use

- Codex is instrumentation, not intelligence.
- Geometry is upstream; semantics is downstream.
- Coherence is not truth.
- CIFScore is not truth.
- RCC drift is not code correctness.
- Tesseract-lite is not full Tesseract.
- Tesseract-lite is not memory agency.
- Artifact indexing is not truth.
- Index presence is not correctness.
- Hash presence is not correctness.
- Run linkage is not provenance.
- RootMirror Full is not code correctness.
- RootMirror Full is not security proof.
- Continuity is not truth.
- Orchestration is not correctness.
- Composition is not truth.
- Multi-instrument agreement is not external validation.
- Registry validity is not instrument validity.
- Evidence composition is not a security proof.
- CIF7-ready is not CIF8.

---

# PART III — EXECUTION AND ARTIFACT SURFACE

## Current v0.7 Capability

CIK v0.7 can:

1. Run the RCC drift instrument.
2. Compute repository-context ΔΦ.
3. Compute Ω stability.
4. Emit state artifacts.
5. Append ledger records.
6. Emit evidence packages.
7. Emit Markdown reports.
8. Emit semantic summaries.
9. Run RootMirror-lite continuity checks.
10. Run perturbation sweeps.
11. Validate baseline to perturbed to restored behavior.
12. Generate Tesseract-lite artifact indexes.
13. Hash artifacts with SHA-256.
14. Bind artifacts to run records.
15. Emit a queryable artifact lattice.
16. Capture pre-run root anchors.
17. Capture post-run root anchors.
18. Verify return-to-root execution.
19. Verify ledger append delta.
20. Verify artifact manifest closure.
21. Emit RootMirror Full JSON / Markdown / evidence outputs.
22. Remove the Full RootMirror downgrade only when verification passes.
23. Consume RootMirror Full evidence as a core scoring signal.
24. Reconcile downgrade reasons from matching evidence only.
25. Classify maturity through v0.6 evidence-bound signals.
26. Preserve CIF-B classification under internal closure.
27. Validate instrument plugin contracts.
28. Register RCC Drift through a contract-aware instrument registry.
29. Emit a v0.7 run plan.
30. Validate registry before orchestration.
31. Execute enabled registry-valid instruments.
32. Emit per-instrument result records.
33. Preserve skipped instruments.
34. Preserve blocked instruments.
35. Preserve failed instruments.
36. Preserve optional degradation as warning.
37. Compose cross-instrument evidence without merging claim types.
38. Emit composed downgrade surface.
39. Emit orchestration state JSON.
40. Emit orchestration evidence package.
41. Preserve RootMirror Full compatibility.
42. Preserve Tesseract-lite compatibility.

## Core Commands

Run full tests:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    $env:PYTHONPATH = ".\src"
    python -m unittest discover -s tests

Run the RCC drift instrument:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    $env:PYTHONPATH = ".\src"
    python -m cik run --instrument rcc-drift --repo ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs"

Run perturbation sweep:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_perturbation_sweep.ps1"

Run Tesseract-lite indexing:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    $env:PYTHONPATH = ".\src"
    python -m cik.tesseract --out ".\outputs"

Run RootMirror Full verification:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    $env:PYTHONPATH = ".\src"
    python -m cik.rootmirror_full --repo-root "." --out ".\outputs" --target-repo ".\tests\fixtures\tiny_repo_with_context"

Run v0.5 RootMirror Full smoke:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_rootmirror_full.ps1"

Run v0.6 integrated smoke:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v06_integrated.ps1"

Run v0.7 orchestration smoke:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v07_orchestration.ps1"

Run v0.7 orchestration directly:

    cd "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"
    $env:PYTHONPATH = ".\src"
    python -m cik.orchestration --repo-root "." --out ".\outputs" --plan ".\configs\orchestration\default_run_plan.json"

## Main Output Folders

| Folder | Purpose |
|---|---|
| outputs/state/ | Authoritative metric snapshots |
| outputs/ledger/ | Append-only temporal trace |
| outputs/evidence/ | Evidence packages |
| outputs/reports/ | Human-readable reports |
| outputs/semantic/ | Downstream semantic summaries |
| outputs/rootmirror/ | RootMirror-lite continuity artifacts |
| outputs/rootmirror_full/ | Full RootMirror run-envelope verification artifacts |
| outputs/perturbation/ | Perturbation sweep artifacts |
| outputs/tesseract/ | Tesseract-lite artifact index |
| outputs/orchestration/ | v0.7 run plans, orchestration states, composed evidence bundles, per-instrument records, and orchestration reports |

## Tesseract-lite Outputs

CIK preserves v0.4 Tesseract-lite outputs:

    outputs/tesseract/tesseract_lite_index.json
    outputs/tesseract/tesseract_lite_index.md
    outputs/tesseract/tesseract_lite_evidence_package.json

The Tesseract-lite index records:

- Artifact type.
- Artifact path.
- File existence.
- File size.
- SHA-256 hash.
- Inferred run ID.
- Run-level artifact grouping.
- Non-claim locks.

## RootMirror Full Outputs

CIK preserves v0.5 RootMirror Full outputs:

    outputs/rootmirror_full/*_rootmirror_full.json
    outputs/rootmirror_full/*_rootmirror_full.md
    outputs/evidence/*_rootmirror_full_evidence_package.json

The RootMirror Full layer records:

- Run envelope.
- Pre-run anchor.
- Post-run anchor.
- Return-to-root proof.
- Ledger append delta.
- Artifact manifest closure.
- Artifact hashes.
- Output-root hash surface.
- Replay metadata.
- Downgrade removal status.
- Non-claim locks.

## Orchestration Outputs

CIK v0.7 emits:

    outputs/orchestration/*_run_plan.json
    outputs/orchestration/*_orchestration_state.json
    outputs/orchestration/*_composed_evidence_bundle.json
    outputs/orchestration/*_instrument_results.json
    outputs/orchestration/*_orchestration_report.md
    outputs/evidence/*_orchestration_evidence_package.json

The orchestration layer records:

- Run plan.
- Registry validation status.
- Instrument execution status.
- Per-instrument result records.
- Per-instrument artifacts.
- Per-instrument downgrades.
- Composed evidence bundle.
- Composed downgrade surface.
- Orchestration state.
- Orchestration evidence package.
- Non-claim locks.

## Instrumentation Loop

    Repository context
    -> RCC drift instrument
    -> DeltaPhi measurement
    -> Omega weighting
    -> state artifact
    -> ledger append
    -> evidence package
    -> report
    -> semantic summary
    -> RootMirror-lite verification
    -> perturbation validation
    -> Tesseract-lite indexing
    -> RootMirror Full run-envelope verification
    -> RootMirror Full evidence package
    -> RootMirror Full evidence consumption
    -> downgrade reconciliation
    -> instrument registry validation
    -> orchestration run plan
    -> registry-gated instrument execution
    -> per-instrument result records
    -> composed evidence bundle
    -> composed downgrade surface
    -> orchestration state
    -> orchestration evidence package

## Current Downgrade Surface

v0.7 closes the prior orchestration gap:

    multiple instruments do not yet run together as a composed execution plan

The current remaining next-stage gap is graph/query-level:

    Artifacts are emitted and indexed, but they are not yet promoted into a first-class evidence graph with cross-run queries, artifact lineage queries, downgrade history, run-family grouping, and claim/evidence lookup.

This is why the next version is:

    CIK v0.8 — Evidence Graph and Cross-Run Query Layer

## Required Local Verification

This section preserves the executable README/RCC contract anchor required by `tests/test_rcc_readmes.py`.

Before treating the repository as locally aligned, run:

    $env:PYTHONPATH = ".\src"
    python -m unittest tests.test_rcc_readmes -v
    python -m unittest tests.test_tesseract_lite -v
    python -m unittest tests.test_tesseract_integration -v
    python -m unittest tests.test_rootmirror_full -v
    python -m unittest tests.test_rootmirror_full_integration -v
    python -m unittest tests.test_v05_full_rootmirror_core_integration -v
    python -m unittest tests.test_v06_rootmirror_full_scoring_integration -v
    python -m unittest tests.test_v06_downgrade_reconciliation -v
    python -m unittest tests.test_v06_instrument_registry_contract -v
    python -m unittest tests.test_v07_run_plan -v
    python -m unittest tests.test_v07_evidence_composition -v
    python -m unittest tests.test_v07_partial_failure_preservation -v
    python -m unittest tests.test_v07_orchestration_executor -v

For full local verification, run:

    $env:PYTHONPATH = ".\src"
    python -m unittest discover -s tests
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v07_orchestration.ps1"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v06_integrated.ps1"

This verification surface does not prove code correctness, semantic truth, security, intelligence, consciousness, autonomous memory, external validity, or artifact meaning. It only confirms that the declared local README/RCC, Tesseract-lite, RootMirror Full, v0.6 integration, and v0.7 orchestration contract checks pass.

## Minimal Verification Checklist

Before locking a version:

    [ ] Full unit tests pass
    [ ] RCC README tests pass
    [ ] Instrument smoke passes
    [ ] Perturbation sweep passes
    [ ] Tesseract-lite index emits
    [ ] RootMirror Full JSON emits
    [ ] RootMirror Full evidence package emits
    [ ] Orchestration run plan emits
    [ ] Orchestration state emits
    [ ] Orchestration evidence package emits
        [ ] Optional degradation is preserved as warning
    [ ] Required failure is preserved as failure
    [ ] Non-claim locks preserved
    [ ] README updated
    [ ] RCC context index updated
    [ ] RCC context map updated
    [ ] Mini READMEs updated if new modules were added

## Current Next Step

Proceed to:

    CIK v0.8 — Evidence Graph and Cross-Run Query Layer

CIK v0.7 is the current committed local layer. CIK v0.8 is the next target.

<!-- CIK-V06-BEGIN -->
## CIK v0.6 — Core Scoring and Instrument Registry Integration Layer

CIK v0.6 promotes RootMirror Full from a sidecar verification layer into a core-consumed evidence signal.

### v0.6 adds

- RootMirror Full evidence consumer.
- CIFScore v0.6 component integration.
- Downgrade reconciliation.
- Maturity classification v0.6.
- Contract-aware instrument plugin validation.
- Instrument registry schema.
- RCC Drift Instrument v0.6 registry contract.
- Integrated v0.6 smoke script.

### v0.6 commands

    python -m unittest tests.test_v06_rootmirror_full_scoring_integration -v
    python -m unittest tests.test_v06_downgrade_reconciliation -v
    python -m unittest tests.test_v06_instrument_registry_contract -v
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v06_integrated.ps1"

### v0.6 non-claim lock

Integrated scoring is not truth. Maturity is not correctness. Instrument registry validity is not instrument validity. RootMirror Full remains continuity verification only.
<!-- CIK-V06-END -->

<!-- CIK-V07-BEGIN -->
## CIK v0.7 — Multi-Instrument Execution Orchestration and Cross-Instrument Evidence Composition Layer

CIK v0.7 turns the contract-aware v0.6 kernel into a governed orchestration runtime.

### v0.7 adds

- Run plan schema.
- Default orchestration run plan.
- Registry-gated execution.
- Per-instrument result records.
- Cross-instrument composed evidence bundle.
- Composed downgrade surface.
- Orchestration state object.
- Orchestration evidence package.
- Partial-failure preservation.
- RootMirror Full compatibility.
- Tesseract-lite compatibility.
- Composition-status repair: required fail/blocked => fail; optional fail/blocked/warning/skipped => warning; all clean => pass.

### v0.7 commands

    python -m unittest tests.test_v07_run_plan -v
    python -m unittest tests.test_v07_evidence_composition -v
    python -m unittest tests.test_v07_partial_failure_preservation -v
    python -m unittest tests.test_v07_orchestration_executor -v
    python -m cik.orchestration --repo-root "." --out ".\outputs" --plan ".\configs\orchestration\default_run_plan.json"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v07_orchestration.ps1"

### v0.7 output surface

- `outputs/orchestration/*_run_plan.json`
- `outputs/orchestration/*_orchestration_state.json`
- `outputs/orchestration/*_composed_evidence_bundle.json`
- `outputs/orchestration/*_instrument_results.json`
- `outputs/orchestration/*_orchestration_report.md`
- `outputs/evidence/*_orchestration_evidence_package.json`

### v0.7 non-claim lock

Orchestration is not correctness. Composition is not truth. Multi-instrument agreement is not external validation. Registry validity is not instrument validity. Evidence composition is not a security proof.
<!-- CIK-V07-END -->

<!-- CIK-ROADMAP-BEGIN -->
## Roadmap to CIK v1.0

### v0.8 — Evidence Graph and Query Layer

Goal: transform state, ledger, RootMirror, Tesseract-lite, perturbation, registry, and orchestration outputs into a queryable evidence graph.

Adds:

- evidence graph JSON
- cross-run search
- artifact lineage queries
- run-family grouping
- downgrade history query
- claim/evidence lookup
- graph validation tests
- graph query smoke script

### v0.9 — Full Tesseract and Dashboard-Ready Package

Goal: evolve Tesseract-lite into a fuller bounded artifact lattice with dashboard-ready summaries.

Adds:

- full Tesseract index contract
- dashboard JSON
- artifact lineage visualization surface
- evidence maturity views
- RCC/CIF/AIT summary surfaces

### v1.0 — Stable Local-First CIK Release

Goal: lock CIK as a stable local-first Codex instrumentation kernel.

v1.0 must include:

- stable CLI
- stable instrument plugin contract
- stable evidence package schema
- stable RootMirror Full verification
- stable orchestration contract
- stable Tesseract artifact index
- stable evidence graph/query surface
- stable README/RCC reconstruction surface
- full local validation command
- clean local Git state
- optional GitHub release readiness

### End-goal lock

CIK v1.0 is a local-first evidence compiler for Codex instrumentation runs.

It does not prove truth, correctness, security, intelligence, consciousness, autonomous memory, external validity, or artifact meaning.
<!-- CIK-ROADMAP-END -->