from __future__ import annotations

from typing import Any, Dict, List


def composed_status(results: List[Dict[str, Any]]) -> str:
    required = [r for r in results if r.get("required")]
    required_blocked_or_failed = [
        r for r in required
        if r.get("status") in {"fail", "blocked"}
    ]

    if required_blocked_or_failed:
        return "fail"

    warnings = [
        r for r in results
        if r.get("status") in {"warning", "skipped"}
    ]

    if warnings:
        return "warning"

    return "pass"


def compose_downgrades(results: List[Dict[str, Any]]) -> List[str]:
    downgrades: List[str] = []

    for result in results:
        instrument = result.get("instrument", "unknown")
        for item in result.get("downgrades", []):
            downgrades.append(f"{instrument}: {item}")

    return downgrades


def score_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not results:
        return {
            "count": 0,
            "mean_score": 0.0,
            "min_score": 0.0,
            "max_score": 0.0,
        }

    scores = []

    for result in results:
        score = result.get("score", None)
        if score is None:
            score = 1.0 if result.get("status") == "pass" else 0.0
        scores.append(float(score))

    return {
        "count": len(scores),
        "mean_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
    }


def compose_instrument_results(run_id: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    status = composed_status(results)
    downgrades = compose_downgrades(results)
    scores = score_summary(results)

    status_counts = {
        "pass": 0,
        "warning": 0,
        "fail": 0,
        "skipped": 0,
        "blocked": 0,
    }

    for result in results:
        key = result.get("status", "blocked")
        if key not in status_counts:
            status_counts[key] = 0
        status_counts[key] += 1

    return {
        "schema": "CIK-v0.7-composed-evidence-bundle",
        "version": "0.7",
        "orchestration_run_id": run_id,
        "status": status,
        "instrument_records": results,
        "status_summary": status_counts,
        "score_summary": scores,
        "composed_downgrade_surface": downgrades,
        "claim_boundaries": {
            "composition_is_not_truth": True,
            "multi_instrument_agreement_is_not_external_validation": True,
            "instrument_claim_types_remain_separate": True,
        },
        "non_claim_locks": {
            "orchestration_is_not_correctness": True,
            "composition_is_not_truth": True,
            "multi_instrument_agreement_is_not_external_validation": True,
            "failed_instruments_must_be_preserved": True,
            "skipped_instruments_must_be_preserved": True,
            "blocked_instruments_must_be_preserved": True,
        }
    }