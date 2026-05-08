from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def write_graph_outputs(graph: Dict[str, Any], output_root: Path) -> Dict[str, str]:
    output_root = Path(output_root).resolve()
    graph_root = output_root / "evidence_graph"
    evidence_root = output_root / "evidence"

    graph_root.mkdir(parents=True, exist_ok=True)
    evidence_root.mkdir(parents=True, exist_ok=True)

    graph_path = graph_root / "evidence_graph.json"
    report_path = graph_root / "evidence_graph_report.md"
    evidence_path = evidence_root / "evidence_graph_evidence_package.json"

    graph_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")

    report_lines = [
        "# CIK v0.8 Evidence Graph Report",
        "",
        f"Schema: {graph.get('schema')}",
        f"Version: {graph.get('version')}",
        f"Node count: {graph.get('node_count')}",
        f"Edge count: {graph.get('edge_count')}",
        f"Validation status: {graph.get('validation', {}).get('status')}",
        "",
        "## Index counts",
        "",
    ]

    indexes = graph.get("indexes", {})

    for key, value in indexes.items():
        report_lines.append(f"- {key}: {len(value)}")

    report_lines.extend([
        "",
        "## Validation",
        "",
        f"- failures: {len(graph.get('validation', {}).get('failures', []))}",
        f"- missing_edges: {len(graph.get('validation', {}).get('missing_edges', []))}",
        f"- inferred_edges: {len(graph.get('validation', {}).get('inferred_edges', []))}",
        f"- ambiguous_edges: {len(graph.get('validation', {}).get('ambiguous_edges', []))}",
        f"- orphan_artifacts: {len(graph.get('validation', {}).get('orphan_artifacts', []))}",
        "",
        "## Non-claim locks",
        "",
        "- Graph linkage is not truth.",
        "- Queryability is not correctness.",
        "- Artifact lineage is not provenance.",
        "- Graph completeness is not evidence completeness.",
        "- Evidence graph is not autonomous memory.",
        "",
    ])

    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    evidence = {
        "schema": "CIK-v0.8-evidence-graph-evidence-package",
        "version": "0.8",
        "status": graph.get("validation", {}).get("status", "unknown"),
        "graph": str(graph_path),
        "report": str(report_path),
        "node_count": graph.get("node_count"),
        "edge_count": graph.get("edge_count"),
        "claim_boundary": "evidence_navigation_only",
        "non_claim_locks": graph.get("non_claim_locks", {}),
    }

    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    return {
        "graph": str(graph_path),
        "report": str(report_path),
        "evidence": str(evidence_path),
    }