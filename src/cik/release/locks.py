from __future__ import annotations

from typing import Dict


def build_non_claim_locks() -> Dict[str, bool]:
    return {
        "codex_is_not_intelligence": True,
        "codex_is_not_consciousness": True,
        "coherence_is_not_truth": True,
        "cifscore_is_not_truth": True,
        "rcc_drift_is_not_code_correctness": True,
        "rootmirror_lite_is_not_full_verification": True,
        "rootmirror_full_is_not_code_correctness": True,
        "rootmirror_full_is_not_security_proof": True,
        "orchestration_is_not_correctness": True,
        "composition_is_not_truth": True,
        "multi_instrument_agreement_is_not_external_validation": True,
        "graph_linkage_is_not_truth": True,
        "queryability_is_not_correctness": True,
        "artifact_lineage_is_not_provenance": True,
        "visualization_is_not_validation": True,
        "tesseract_linkage_is_not_provenance": True,
        "dashboard_completeness_is_not_evidence_completeness": True,
        "release_readiness_is_not_release_proof": True,
        "stable_release_is_not_truth": True,
        "local_validation_is_not_formal_verification": True,
        "release_bundle_is_not_provenance": True,
        "git_cleanliness_is_not_semantic_validity": True,
        "release_notes_are_not_external_validation": True,
    }