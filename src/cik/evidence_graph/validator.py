from __future__ import annotations

from typing import Any, Dict, List


VALID_EDGE_STATUSES = {"artifact_backed", "inferred", "missing", "ambiguous"}


def validate_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    missing_edges: List[Dict[str, Any]] = []
    inferred_edges: List[Dict[str, Any]] = []
    ambiguous_edges: List[Dict[str, Any]] = []
    orphan_artifacts: List[Dict[str, Any]] = []
    failures: List[str] = []

    node_ids = {node.get("id") for node in graph.get("nodes", [])}

    linked_targets = set()
    linked_sources = set()

    for edge in graph.get("edges", []):
        status = edge.get("status")

        if status not in VALID_EDGE_STATUSES:
            failures.append(f"invalid_edge_status:{edge.get('id')}")

        if edge.get("source") not in node_ids:
            failures.append(f"edge_missing_source:{edge.get('id')}")

        if edge.get("target") not in node_ids:
            failures.append(f"edge_missing_target:{edge.get('id')}")

        if status == "missing":
            missing_edges.append(edge)

        if status == "inferred":
            inferred_edges.append(edge)

        if status == "ambiguous":
            ambiguous_edges.append(edge)

        linked_sources.add(edge.get("source"))
        linked_targets.add(edge.get("target"))

    for node in graph.get("nodes", []):
        if node.get("type") == "artifact":
            node_id = node.get("id")
            has_link = node_id in linked_targets or node_id in linked_sources
            if not has_link:
                orphan_artifacts.append(node)

    status = "pass"

    if orphan_artifacts or inferred_edges or missing_edges or ambiguous_edges:
        status = "warning"

    if failures:
        status = "fail"

    return {
        "schema": "CIK-v0.8-graph-validation",
        "status": status,
        "failures": failures,
        "missing_edges": missing_edges,
        "inferred_edges": inferred_edges,
        "ambiguous_edges": ambiguous_edges,
        "orphan_artifacts": [
            {
                "id": n.get("id"),
                "path": n.get("path"),
                "label": n.get("label"),
            }
            for n in orphan_artifacts
        ],
        "non_claim_locks": {
            "graph_validation_is_not_correctness": True,
            "orphan_detection_is_not_semantic_invalidity": True,
            "missing_edge_disclosure_is_not_failure_by_itself": True,
        },
    }