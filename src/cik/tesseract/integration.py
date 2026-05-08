from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable
import json


FULL_ROOTMIRROR_REASON = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
TESSERACT_MISSING_REASON = "Tesseract indexing not enabled."


def clamp01(x: Any) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def _dedupe(items: Iterable[str]) -> list[str]:
    out = []
    seen = set()
    for item in items:
        text = str(item)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def load_latest_tesseract_summary(output_root: str | Path = "outputs") -> Dict[str, Any]:
    output_root = Path(output_root)
    index_path = output_root / "tesseract" / "tesseract_lite_index.json"

    if not index_path.exists():
        return {
            "available": False,
            "status": "missing",
            "score": 0.0,
            "index_json": str(index_path),
        }

    data = json.loads(index_path.read_text(encoding="utf-8"))
    score = clamp01(data.get("index_integrity_score", 0.0))

    return {
        "available": True,
        "status": "pass" if score >= 1.0 else "warning",
        "score": score,
        "index_json": str(index_path),
        "index_markdown": data.get("index_markdown"),
        "record_count": data.get("record_count", 0),
        "artifact_count": data.get("artifact_count", 0),
        "raw": data,
    }


def integrate_tesseract_if_available(result: Dict[str, Any], output_root: str | Path = "outputs") -> Dict[str, Any]:
    if not isinstance(result, dict):
        return result

    summary = load_latest_tesseract_summary(output_root)
    updated = dict(result)

    updated["tesseract_lite_available"] = bool(summary.get("available"))
    updated["tesseract_lite_status"] = summary.get("status")
    updated["tesseract_lite_score"] = clamp01(summary.get("score", 0.0))
    updated["tesseract_lite_index"] = summary.get("index_json")
    updated["tesseract_lite_integrated"] = False

    locks = dict(updated.get("non_claim_locks") or {})
    locks.update(
        {
            "tesseract_lite_is_not_full_tesseract": True,
            "tesseract_lite_is_not_memory_agency": True,
            "artifact_indexing_is_not_truth": True,
            "index_presence_is_not_correctness": True,
            "hash_presence_is_not_correctness": True,
            "run_linkage_is_not_provenance": True,
            "cif7_ready_is_not_cif8": True,
        }
    )
    updated["non_claim_locks"] = locks

    reasons = updated.get("downgrade_reason") or []
    if isinstance(reasons, str):
        reasons = [reasons]
    reasons = [str(r) for r in reasons]

    passed = bool(summary.get("available")) and summary.get("status") == "pass" and clamp01(summary.get("score", 0.0)) >= 1.0

    if passed:
        updated["tesseract_lite_integrated"] = True
        reasons = [r for r in reasons if r != TESSERACT_MISSING_REASON and r != "Tesseract-lite indexing failed or incomplete."]

        if FULL_ROOTMIRROR_REASON not in reasons:
            reasons.append(FULL_ROOTMIRROR_REASON)

        updated["downgrade_reason"] = _dedupe(reasons)
        updated["maturity_base_before_tesseract"] = updated.get("maturity")
        updated["maturity"] = "CIF7-ready"
        updated["classification"] = "CIF-B"
        updated["maturity_note"] = "Tesseract-lite artifact indexing passed; full RootMirror remains deferred."
    else:
        if TESSERACT_MISSING_REASON not in reasons:
            reasons.append(TESSERACT_MISSING_REASON)
        updated["downgrade_reason"] = _dedupe(reasons)

    return updated