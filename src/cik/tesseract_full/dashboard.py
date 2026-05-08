from __future__ import annotations

from typing import Any, Dict


DASHBOARD_NON_CLAIM_LOCKS = {
    "dashboard_is_navigation_not_truth": True,
    "visualization_is_not_validation": True,
    "dashboard_completeness_is_not_evidence_completeness": True,
}


def build_dashboard_data(graph: Dict[str, Any], views: Dict[str, Any], release_readiness: Dict[str, Any]) -> Dict[str, Any]:
    indexes = graph.get("indexes", {})

    summary = {
        "run_count": len(indexes.get("runs", {})),
        "artifact_count": len(indexes.get("artifacts", {})),
        "instrument_count": len(indexes.get("instruments", {})),
        "downgrade_count": len(indexes.get("downgrades", {})),
        "claim_count": len(indexes.get("claims", {})),
        "node_count": graph.get("node_count", 0),
        "edge_count": graph.get("edge_count", 0),
        "validation_status": graph.get("validation", {}).get("status", "unknown"),
        "release_readiness_status": release_readiness.get("status", "unknown"),
    }

    return {
        "schema": "CIK-v0.9-dashboard-data",
        "version": "0.9",
        "summary": summary,
        "views": views,
        "graph_validation": graph.get("validation", {}),
        "release_readiness": release_readiness,
        "non_claim_locks": dict(DASHBOARD_NON_CLAIM_LOCKS),
    }