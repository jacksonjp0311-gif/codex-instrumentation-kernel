from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .loader import load_or_build_evidence_graph
from .views import build_all_views
from .readiness import build_release_readiness
from .dashboard import build_dashboard_data


PACKAGE_NON_CLAIM_LOCKS = {
    "dashboard_visualization_is_not_truth": True,
    "tesseract_linkage_is_not_provenance": True,
    "dashboard_completeness_is_not_evidence_completeness": True,
    "release_readiness_is_not_release_proof": True,
    "visualization_is_not_validation": True,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_tesseract_package(output_root: Path) -> Dict[str, Any]:
    output_root = Path(output_root).resolve()
    graph = load_or_build_evidence_graph(output_root)
    views = build_all_views(graph)
    release_readiness = build_release_readiness(output_root, graph, views)
    dashboard = build_dashboard_data(graph, views, release_readiness)

    package = {
        "schema": "CIK-v0.9-tesseract-full-package",
        "version": "0.9",
        "generated_at": utc_now(),
        "source_graph": str(output_root / "evidence_graph" / "evidence_graph.json"),
        "node_count": graph.get("node_count", 0),
        "edge_count": graph.get("edge_count", 0),
        "views": views,
        "graph_validation": graph.get("validation", {}),
        "dashboard": {
            "dashboard_json": str(output_root / "dashboard" / "dashboard_data.json"),
            "dashboard_markdown": str(output_root / "dashboard" / "dashboard_report.md"),
        },
        "release_readiness": release_readiness,
        "non_claim_locks": dict(PACKAGE_NON_CLAIM_LOCKS),
    }

    return {
        "graph": graph,
        "views": views,
        "release_readiness": release_readiness,
        "dashboard": dashboard,
        "package": package,
    }