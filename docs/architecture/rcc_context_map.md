# RCC Context Map — CIK v0.1

This file defines the repository-context map for the Codex Instrumentation Kernel.

## Purpose

CIK is a minimal Codex instrumentation runtime. Its primary job is to run declared instruments, compute bounded residuals, emit artifacts, append ledgers, package evidence, and classify maturity conservatively.

## Current context rule

Agents should reconstruct repository context in this order:

1. Root README.
2. This RCC context map.
3. `docs/context/repository_context_index.json`.
4. Target folder mini README.
5. Relevant source/config/test/artifact files.

## Primary runtime chain

    repository
    -> context declaration
    -> rcc-drift instrument
    -> DeltaPhi_repo
    -> Omega_repo
    -> state artifact
    -> ledger
    -> evidence package
    -> report
    -> semantic summary

## Major surfaces

| Surface | Role |
|---|---|
| `src/cik/core` | CIF loop, scoring, maturity, classification, locks |
| `src/cik/instruments` | instrument registry and instrument implementations |
| `src/cik/instruments/rcc_drift` | first runnable instrument |
| `src/cik/artifacts` | state, ledger, report, and text writers |
| `src/cik/evidence` | evidence package construction |
| `src/cik/injection` | AIT/HYDRA injection register |
| `src/cik/schemas` | artifact schemas |
| `tests` | unit tests and fixture repos |
| `outputs` | generated fossils |

## Current residual

    DeltaPhi_repo =
        0.20 * missing_path_drift
      + 0.20 * staleness_drift
      + 0.25 * claim_drift
      + 0.25 * evidence_drift
      + 0.10 * command_drift

## Current stability weight

    Omega_repo = 1 / (1 + abs(DeltaPhi_repo))

## Current maturity interpretation

CIK v0.1 is CIF4 because it is runnable and emits artifacts.

CIK v0.1 is CIF-B because it is useful but incomplete:

- no perturbation sweep,
- no RootMirror verification,
- no Tesseract indexing.

## Non-claim locks

- RCC drift is not code correctness.
- CIFScore is not truth.
- Coherence is not truth.
- Semantic summaries are downstream only.
- Evidence packages prove only their declared claim type.
- RootMirror is not implemented yet.
- Tesseract indexing is not implemented yet.

<!-- CIK-V06-BEGIN -->
## CIK v0.6 — Core Scoring, Maturity, Downgrade, and Instrument Registry Integration Layer

CIK v0.6 integrates RootMirror Full evidence into core scoring and maturity surfaces while adding a contract-aware instrument registry.

### New core modules

- `src/cik/core/rootmirror_full_consumer.py`
- `src/cik/core/scoring_v06.py`
- `src/cik/core/downgrades_v06.py`
- `src/cik/core/maturity_v06.py`

### New instrument registry modules

- `src/cik/instruments/contracts_v06.py`
- `src/cik/instruments/registry_v06.py`
- `configs/instruments/instrument_registry.json`

### New protocol

- `docs/protocols/instrument_plugin_contract.md`

### New validation

- `tests/test_v06_rootmirror_full_scoring_integration.py`
- `tests/test_v06_downgrade_reconciliation.py`
- `tests/test_v06_instrument_registry_contract.py`
- `scripts/run_cik_v06_integrated.ps1`

### Non-claim boundary

CIK v0.6 makes verification evidence operational. It does not make scoring truth, maturity correctness, registry validity instrument validity, or RootMirror Full security proof.
<!-- CIK-V06-END -->

<!-- CIK-V07-BEGIN -->
## CIK v0.7 — Multi-Instrument Execution Orchestration and Cross-Instrument Evidence Composition Layer

CIK v0.7 adds governed orchestration over registry-valid instruments.

### New orchestration modules

- `src/cik/orchestration/run_plan.py`
- `src/cik/orchestration/executor.py`
- `src/cik/orchestration/composer.py`
- `src/cik/orchestration/writer.py`
- `src/cik/orchestration/__main__.py`

### New config

- `configs/orchestration/default_run_plan.json`

### New outputs

- `outputs/orchestration/*_run_plan.json`
- `outputs/orchestration/*_orchestration_state.json`
- `outputs/orchestration/*_composed_evidence_bundle.json`
- `outputs/orchestration/*_instrument_results.json`
- `outputs/orchestration/*_orchestration_report.md`
- `outputs/evidence/*_orchestration_evidence_package.json`

### New validation

- `tests/test_v07_run_plan.py`
- `tests/test_v07_evidence_composition.py`
- `tests/test_v07_partial_failure_preservation.py`
- `tests/test_v07_orchestration_executor.py`
- `scripts/run_cik_v07_orchestration.ps1`

### Non-claim boundary

Orchestration is not correctness. Composition is not truth. Multi-instrument agreement is not external validation. Registry validity is not instrument validity.
<!-- CIK-V07-END -->

<!-- CIK-V08-BEGIN -->
## CIK v0.8 — Evidence Graph and Cross-Run Query Layer

CIK v0.8 adds a read-only evidence graph and cross-run query layer over emitted CIK artifacts.

### New evidence graph modules

- `src/cik/evidence_graph/nodes.py`
- `src/cik/evidence_graph/edges.py`
- `src/cik/evidence_graph/builder.py`
- `src/cik/evidence_graph/queries.py`
- `src/cik/evidence_graph/validator.py`
- `src/cik/evidence_graph/writer.py`
- `src/cik/evidence_graph/__main__.py`

### Payload-shape repair

Graph scanning now accepts both JSON object artifacts and JSON array artifacts. This is required because v0.7 emits array-shaped per-instrument result records.

### New protocol

- `docs/protocols/evidence_graph_contract.md`

### New outputs

- `outputs/evidence_graph/evidence_graph.json`
- `outputs/evidence_graph/evidence_graph_report.md`
- `outputs/evidence/evidence_graph_evidence_package.json`

### New validation

- `tests/test_v08_graph_builder.py`
- `tests/test_v08_graph_queries.py`
- `tests/test_v08_downgrade_history.py`
- `tests/test_v08_claim_evidence_lookup.py`
- `tests/test_v08_graph_validation.py`
- `scripts/run_cik_v08_evidence_graph.ps1`

### Non-claim boundary

Graph linkage is not truth. Queryability is not correctness. Artifact lineage is not provenance. Graph completeness is not evidence completeness. Evidence graph is not autonomous memory.
<!-- CIK-V08-END -->
