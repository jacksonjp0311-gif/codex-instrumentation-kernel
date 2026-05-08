from __future__ import annotations

from typing import Dict, Any


def clamp01(x: float) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def cif_score_v06(
    dphi_declared: float,
    omega_declared: float,
    perturbation_score: float,
    artifact_score: float,
    rootmirror_full_score: float,
    falsification_score: float,
    tesseract_index_score: float,
) -> float:
    values = [
        clamp01(dphi_declared),
        clamp01(omega_declared),
        clamp01(perturbation_score),
        clamp01(artifact_score),
        clamp01(rootmirror_full_score),
        clamp01(falsification_score),
        clamp01(tesseract_index_score),
    ]
    return clamp01(sum(values) / len(values))


def score_from_evidence_bundle(bundle: Dict[str, Any]) -> Dict[str, Any]:
    score = cif_score_v06(
        dphi_declared=bundle.get("dphi_declared", 1.0),
        omega_declared=bundle.get("omega_declared", 1.0),
        perturbation_score=bundle.get("perturbation_score", 0.0),
        artifact_score=bundle.get("artifact_score", 1.0),
        rootmirror_full_score=bundle.get("rootmirror_full_score", 0.0),
        falsification_score=bundle.get("falsification_score", 1.0),
        tesseract_index_score=bundle.get("tesseract_index_score", 0.0),
    )

    return {
        "schema": "CIK-v0.6-cifscore",
        "cif_score": score,
        "components": {
            "dphi_declared": clamp01(bundle.get("dphi_declared", 1.0)),
            "omega_declared": clamp01(bundle.get("omega_declared", 1.0)),
            "perturbation_score": clamp01(bundle.get("perturbation_score", 0.0)),
            "artifact_score": clamp01(bundle.get("artifact_score", 1.0)),
            "rootmirror_full_score": clamp01(bundle.get("rootmirror_full_score", 0.0)),
            "falsification_score": clamp01(bundle.get("falsification_score", 1.0)),
            "tesseract_index_score": clamp01(bundle.get("tesseract_index_score", 0.0)),
        },
        "non_claim_locks": {
            "cifscore_is_not_truth": True,
            "cifscore_is_not_code_correctness": True,
            "rootmirror_full_score_is_not_security_proof": True,
            "maturity_score_is_not_external_validation": True,
        },
    }