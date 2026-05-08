from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


ROOTMIRROR_OLD_REASON = "RootMirror verification not enabled."
ROOTMIRROR_LITE_REASON = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."

PERTURB_REASON = "No perturbation sweep yet."
TESSERACT_REASON = "Tesseract indexing not enabled."


def clamp01(x: float) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def rootmirror_lite_score(rootmirror_result: Dict[str, Any]) -> float:
    rm = rootmirror_result.get("rootmirror_lite", {})
    return clamp01(rm.get("score", 0.0))


def rootmirror_lite_passed(rootmirror_result: Dict[str, Any]) -> bool:
    rm = rootmirror_result.get("rootmirror_lite", {})
    return rm.get("status") == "pass" and rootmirror_lite_score(rootmirror_result) == 1.0


def normalize_downgrade_reasons(base_reasons: List[str], rootmirror_result: Dict[str, Any]) -> List[str]:
    reasons = list(base_reasons or [])
    passed = rootmirror_lite_passed(rootmirror_result)

    cleaned: List[str] = []
    for reason in reasons:
        if reason == ROOTMIRROR_OLD_REASON and passed:
            continue
        if reason not in cleaned:
            cleaned.append(reason)

    if passed:
        if ROOTMIRROR_LITE_REASON not in cleaned:
            insertion_index = 1 if cleaned and cleaned[0] == PERTURB_REASON else len(cleaned)
            cleaned.insert(insertion_index, ROOTMIRROR_LITE_REASON)
    else:
        failure_reason = "RootMirror-lite continuity verification failed."
        if failure_reason not in cleaned:
            cleaned.insert(0, failure_reason)

    if PERTURB_REASON not in cleaned:
        cleaned.insert(0, PERTURB_REASON)

    if TESSERACT_REASON not in cleaned:
        cleaned.append(TESSERACT_REASON)

    return cleaned


def integrate_rootmirror_lite_score(
    run_result: Dict[str, Any],
    rootmirror_result: Dict[str, Any],
) -> Dict[str, Any]:
    result = deepcopy(run_result)

    base_score = clamp01(result.get("cif_score", 0.0))
    rm_score = rootmirror_lite_score(rootmirror_result)
    passed = rootmirror_lite_passed(rootmirror_result)

    old_reason_present = ROOTMIRROR_OLD_REASON in (result.get("downgrade_reason") or [])

    if passed and old_reason_present:
        integrated_score = clamp01(base_score + (1.0 / 7.0))
    elif passed and base_score < (6.0 / 7.0):
        integrated_score = clamp01(max(base_score, 6.0 / 7.0))
    else:
        integrated_score = base_score

    result["cif_score_base"] = base_score
    result["cif_score"] = integrated_score
    result["cif_score_integrated"] = integrated_score
    result["rootmirror_lite_score"] = rm_score
    result["rootmirror_lite_status"] = rootmirror_result.get("rootmirror_lite", {}).get("status", "unknown")
    result["rootmirror_lite_integrated"] = True

    if passed:
        result["maturity_base"] = result.get("maturity", "CIF4")
        result["maturity"] = "CIF5"
        result["maturity_note"] = "CIF5 with CIF6-readiness surface; full RootMirror, perturbation sweep, and Tesseract indexing remain deferred."
    else:
        result["maturity_base"] = result.get("maturity", "CIF4")
        result["maturity"] = result.get("maturity", "CIF4")
        result["maturity_note"] = "RootMirror-lite did not pass; maturity remains base classification."

    result["classification"] = result.get("classification", "CIF-B")
    result["downgrade_reason"] = normalize_downgrade_reasons(
        result.get("downgrade_reason") or [],
        rootmirror_result,
    )

    result.setdefault("non_claim_locks", {})
    result["non_claim_locks"]["rootmirror_lite_is_not_full_rootmirror"] = True
    result["non_claim_locks"]["continuity_is_not_correctness"] = True
    result["non_claim_locks"]["cifscore_is_not_truth"] = True
    result["non_claim_locks"]["cif5_is_not_cif8"] = True

    result["v02c_integration"] = {
        "schema": "CIK-v0.2C-cifscore-rootmirror-lite-integration",
        "base_cif_score": base_score,
        "rootmirror_lite_score": rm_score,
        "integrated_cif_score": integrated_score,
        "rootmirror_lite_passed": passed,
        "old_rootmirror_reason_present": old_reason_present,
        "classification_policy": "Remain CIF-B until perturbation sweep and Tesseract indexing are implemented.",
        "non_claim": "RootMirror-lite improves local continuity maturity only; it does not prove correctness, security, truth, or full RootMirror provenance.",
    }

    return result


def inject_integrated_result_into_state(state_path: str, integrated_result: Dict[str, Any]) -> None:
    import json
    from pathlib import Path

    path = Path(state_path)
    if not path.exists():
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return

    data["cif_score_base"] = integrated_result.get("cif_score_base")
    data["cif_score_integrated"] = integrated_result.get("cif_score_integrated")
    data["cif_score"] = integrated_result.get("cif_score")
    data["maturity_base"] = integrated_result.get("maturity_base")
    data["maturity"] = integrated_result.get("maturity")
    data["maturity_note"] = integrated_result.get("maturity_note")
    data["classification"] = integrated_result.get("classification")
    data["downgrade_reason"] = integrated_result.get("downgrade_reason")
    data["rootmirror_lite_score"] = integrated_result.get("rootmirror_lite_score")
    data["rootmirror_lite_status"] = integrated_result.get("rootmirror_lite_status")
    data["rootmirror_lite_integrated"] = True
    data["v02c_integration"] = integrated_result.get("v02c_integration", {})

    data.setdefault("non_claim_locks", {})
    for key, value in integrated_result.get("non_claim_locks", {}).items():
        data["non_claim_locks"][key] = value

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def inject_integrated_result_into_evidence(evidence_path: str, integrated_result: Dict[str, Any]) -> None:
    import json
    from pathlib import Path

    path = Path(evidence_path)
    if not path.exists():
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return

    data["cifscore_integration_evidence"] = {
        "schema": "CIK-v0.2C-cifscore-integration-evidence",
        "base_cif_score": integrated_result.get("cif_score_base"),
        "integrated_cif_score": integrated_result.get("cif_score_integrated"),
        "rootmirror_lite_score": integrated_result.get("rootmirror_lite_score"),
        "rootmirror_lite_status": integrated_result.get("rootmirror_lite_status"),
        "maturity": integrated_result.get("maturity"),
        "classification": integrated_result.get("classification"),
        "downgrade_reason": integrated_result.get("downgrade_reason"),
        "non_claim": "CIFScore integration reflects instrumentation-compliance maturity only, not truth or code correctness.",
    }

    data.setdefault("non_claim_locks", {})
    data["non_claim_locks"]["rootmirror_lite_is_not_full_rootmirror"] = True
    data["non_claim_locks"]["continuity_is_not_correctness"] = True
    data["non_claim_locks"]["cifscore_is_not_truth"] = True

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")