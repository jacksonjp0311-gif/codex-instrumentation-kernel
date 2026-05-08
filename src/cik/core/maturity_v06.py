from __future__ import annotations

from typing import Any, Dict, List


def classify_maturity_v06(
    perturbation_score: float,
    rootmirror_full_score: float,
    tesseract_index_score: float,
    downgrades: List[str],
) -> Dict[str, Any]:
    perturbation_pass = abs(float(perturbation_score) - 1.0) <= 1e-9
    rootmirror_pass = abs(float(rootmirror_full_score) - 1.0) <= 1e-9
    tesseract_pass = abs(float(tesseract_index_score) - 1.0) <= 1e-9

    maturity = "CIF4"

    if rootmirror_pass:
        maturity = "CIF6-rootmirror-full"

    if perturbation_pass and rootmirror_pass and tesseract_pass:
        maturity = "CIF7-verified"

    return {
        "schema": "CIK-v0.6-maturity",
        "maturity": maturity,
        "classification": "CIF-B",
        "downgrade_reason": list(downgrades or []),
        "signals": {
            "perturbation_score": float(perturbation_score),
            "rootmirror_full_score": float(rootmirror_full_score),
            "tesseract_index_score": float(tesseract_index_score),
        },
        "non_claim_locks": {
            "maturity_is_not_correctness": True,
            "classification_is_not_truth": True,
            "cif7_verified_is_not_cif8": True,
            "cif_b_preserved_until_stronger_external_evidence": True,
            "internal_closure_does_not_create_cif_a": True,
        },
    }