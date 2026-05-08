from __future__ import annotations

from typing import Any, Dict, List


ROOTMIRROR_FULL_DOWNGRADE = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
ROOTMIRROR_GENERIC_DOWNGRADE = "RootMirror verification not enabled."


def reconcile_downgrades(downgrades: List[str], rootmirror_full_signal: Dict[str, Any]) -> List[str]:
    """Remove only downgrades directly closed by matching evidence.

    RootMirror Full evidence may remove only RootMirror-related downgrades.
    It may not remove perturbation, Tesseract, benchmark, RCC, or other gaps.
    """
    current = list(downgrades or [])
    score = float(rootmirror_full_signal.get("score", 0.0))

    if abs(score - 1.0) > 1e-9:
        return current

    reconciled = [
        item for item in current
        if item != ROOTMIRROR_FULL_DOWNGRADE
        and item != ROOTMIRROR_GENERIC_DOWNGRADE
    ]

    return reconciled


def downgrade_reconciliation_report(
    before: List[str],
    after: List[str],
    rootmirror_full_signal: Dict[str, Any],
) -> Dict[str, Any]:
    removed = [item for item in before if item not in after]
    preserved = [item for item in before if item in after]

    return {
        "schema": "CIK-v0.6-downgrade-reconciliation",
        "rootmirror_full_score": float(rootmirror_full_signal.get("score", 0.0)),
        "removed": removed,
        "preserved": preserved,
        "after": after,
        "non_claim_locks": {
            "downgrade_reconciliation_is_not_correctness": True,
            "rootmirror_full_evidence_removes_only_matching_gaps": True,
            "unrelated_downgrades_must_be_preserved": True,
        },
    }