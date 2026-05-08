from __future__ import annotations


def build_evidence_package(state: dict, artifact_paths: dict[str, str]) -> dict:
    return {
        "schema": "CIK-v0.1-evidence-package",
        "instrument": state.get("instrument"),
        "run_id": state.get("run_id"),
        "claim": {
            "claim_id": "CLAIM-001",
            "claim_text": "Repository-context drift was measured against declared context surfaces.",
            "claim_type": "context",
        },
        "metrics": {
            "dphi_global": state.get("geometry", {}).get("dphi_global"),
            "omega_mean": state.get("geometry", {}).get("omega_mean"),
            "cif_score": state.get("cif", {}).get("cif_score"),
        },
        "artifacts": artifact_paths,
        "classification": {
            "maturity": state.get("cif", {}).get("maturity_level"),
            "class": state.get("cif", {}).get("classification"),
            "downgrade_reason": state.get("cif", {}).get("downgrade_reason", []),
        },
        "non_claim_locks": {
            "context_reconstruction_is_not_correctness_proof": True,
            "coherence_is_not_truth": True,
            "cifscore_is_not_truth": True,
        },
    }