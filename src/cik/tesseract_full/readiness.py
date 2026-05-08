from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


READINESS_NON_CLAIM_LOCKS = {
    "release_readiness_is_not_release_proof": True,
    "readiness_summary_is_not_security_proof": True,
    "ready_status_is_not_public_guarantee": True,
}


def build_release_readiness(output_root: Path, graph: Dict[str, Any], views: Dict[str, Any]) -> Dict[str, Any]:
    output_root = Path(output_root).resolve()

    checks = {
        "stable_cli": True,
        "stable_readme": (output_root.parent / "README.md").exists(),
        "stable_rcc": (output_root.parent / "docs" / "context" / "repository_context_index.json").exists(),
        "stable_rootmirror": (output_root / "rootmirror_full").exists(),
        "stable_orchestration": (output_root / "orchestration").exists(),
        "stable_evidence_graph": (output_root / "evidence_graph" / "evidence_graph.json").exists(),
        "stable_dashboard": True,
        "clean_git": None,
        "release_notes": False,
    }

    blocking_gaps: List[str] = []
    warnings: List[str] = []

    if not checks["stable_readme"]:
        blocking_gaps.append("README.md missing.")

    if not checks["stable_rcc"]:
        warnings.append("Repository context index missing.")

    if not checks["stable_evidence_graph"]:
        blocking_gaps.append("Evidence graph JSON missing.")

    if not checks["release_notes"]:
        warnings.append("Release notes are not yet prepared for v1.0.")

    validation = graph.get("validation", {})
    if validation.get("status") == "fail":
        blocking_gaps.append("Evidence graph validation status is fail.")

    if validation.get("status") == "warning":
        warnings.append("Evidence graph validation status is warning.")

    if not views.get("run_families"):
        warnings.append("No run-family view entries found.")

    if not views.get("claim_boundaries"):
        warnings.append("No claim-boundary view entries found.")

    status = "ready"

    if warnings:
        status = "partial"

    if blocking_gaps:
        status = "not_ready"

    return {
        "schema": "CIK-v0.9-release-readiness-summary",
        "version": "0.9",
        "status": status,
        "blocking_gaps": blocking_gaps,
        "warnings": warnings,
        "passed_checks": [k for k, v in checks.items() if v is True],
        "v1_0_gate": checks,
        "non_claim_locks": dict(READINESS_NON_CLAIM_LOCKS),
    }