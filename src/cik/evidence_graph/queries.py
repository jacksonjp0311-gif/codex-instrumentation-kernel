from __future__ import annotations

from typing import Any, Dict, List, Optional


QUERY_NON_CLAIM_LOCKS = {
    "query_result_is_navigation_not_truth": True,
    "queryability_is_not_correctness": True,
    "artifact_lineage_is_not_provenance": True,
}


def _nodes(graph: Dict[str, Any], node_type: Optional[str] = None) -> List[Dict[str, Any]]:
    nodes = graph.get("nodes", [])
    if node_type:
        return [n for n in nodes if n.get("type") == node_type]
    return list(nodes)


def _edges(graph: Dict[str, Any], edge_type: Optional[str] = None) -> List[Dict[str, Any]]:
    edges = graph.get("edges", [])
    if edge_type:
        return [e for e in edges if e.get("type") == edge_type]
    return list(edges)


def _node_by_id(graph: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {n.get("id"): n for n in graph.get("nodes", [])}


def list_runs(graph: Dict[str, Any]) -> Dict[str, Any]:
    runs = sorted(
        [
            {
                "run_id": n.get("run_id"),
                "label": n.get("label"),
                "instrument": n.get("instrument"),
                "id": n.get("id"),
            }
            for n in _nodes(graph, "run")
        ],
        key=lambda x: str(x.get("run_id")),
    )

    return {
        "query": "runs",
        "status": "found" if runs else "missing",
        "count": len(runs),
        "runs": runs,
        "non_claim_locks": dict(QUERY_NON_CLAIM_LOCKS),
    }


def artifacts_for_run(graph: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    by_id = _node_by_id(graph)
    run_nodes = [n for n in _nodes(graph, "run") if n.get("run_id") == run_id]

    artifacts: List[Dict[str, Any]] = []

    for run_node in run_nodes:
        for edge in _edges(graph, "has_artifact"):
            if edge.get("source") == run_node.get("id"):
                target = by_id.get(edge.get("target"))
                if target:
                    artifacts.append(target)

    return {
        "query": "artifacts-for-run",
        "run_id": run_id,
        "status": "found" if artifacts else "missing",
        "count": len(artifacts),
        "artifacts": artifacts,
        "non_claim_locks": dict(QUERY_NON_CLAIM_LOCKS),
    }


def evidence_for_run(graph: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    by_id = _node_by_id(graph)
    run_nodes = [n for n in _nodes(graph, "run") if n.get("run_id") == run_id]

    evidence: List[Dict[str, Any]] = []

    for run_node in run_nodes:
        for edge in _edges(graph, "has_evidence"):
            if edge.get("source") == run_node.get("id"):
                target = by_id.get(edge.get("target"))
                if target:
                    evidence.append(target)

    return {
        "query": "evidence-for-run",
        "run_id": run_id,
        "status": "found" if evidence else "missing",
        "count": len(evidence),
        "evidence": evidence,
        "non_claim_locks": dict(QUERY_NON_CLAIM_LOCKS),
    }


def downgrade_history(graph: Dict[str, Any]) -> Dict[str, Any]:
    by_id = _node_by_id(graph)
    history: Dict[str, Dict[str, Any]] = {}

    for edge in _edges(graph, "has_downgrade"):
        run_node = by_id.get(edge.get("source"))
        downgrade_node = by_id.get(edge.get("target"))

        if not run_node or not downgrade_node:
            continue

        label = downgrade_node.get("label")
        if label not in history:
            history[label] = {
                "downgrade": label,
                "runs": [],
                "status": "active",
            }

        history[label]["runs"].append(run_node.get("run_id"))

    items = list(history.values())

    for item in items:
        item["runs"] = sorted(set([r for r in item["runs"] if r]))
        if len(item["runs"]) > 1:
            item["status"] = "recurring"

    return {
        "query": "downgrade-history",
        "status": "found" if items else "missing",
        "count": len(items),
        "downgrades": sorted(items, key=lambda x: x["downgrade"]),
        "non_claim_locks": {
            **QUERY_NON_CLAIM_LOCKS,
            "downgrade_history_is_not_resolution_proof": True,
        },
    }


def claim_evidence(graph: Dict[str, Any], claim: str) -> Dict[str, Any]:
    by_id = _node_by_id(graph)
    matching_claims = [n for n in _nodes(graph, "claim") if n.get("label") == claim]
    declarations: List[Dict[str, Any]] = []

    target_ids = {n.get("id") for n in matching_claims}

    for edge in _edges(graph, "declares_boundary"):
        if edge.get("target") in target_ids:
            source = by_id.get(edge.get("source"))
            claim_node = by_id.get(edge.get("target"))
            declarations.append({
                "run": source,
                "claim": claim_node,
                "support": edge.get("support"),
                "status": edge.get("status"),
            })

    return {
        "query": "claim-evidence",
        "claim": claim,
        "status": "declared" if declarations else "missing",
        "count": len(declarations),
        "declared_by": declarations,
        "claim_boundary": "non_claim_or_declared_boundary",
        "non_claim_locks": {
            **QUERY_NON_CLAIM_LOCKS,
            "claim_lookup_is_not_claim_truth": True,
        },
    }


def artifact_lineage(graph: Dict[str, Any], artifact: str) -> Dict[str, Any]:
    by_id = _node_by_id(graph)
    candidates = [
        n for n in _nodes(graph, "artifact")
        if n.get("path") == artifact
        or str(n.get("path", "")).endswith(artifact)
        or n.get("label") == artifact
    ]

    if not candidates:
        return {
            "query": "artifact-lineage",
            "artifact": artifact,
            "status": "missing",
            "missing_links": ["artifact_not_found"],
            "non_claim_locks": dict(QUERY_NON_CLAIM_LOCKS),
        }

    artifact_node = candidates[0]
    owners: List[Dict[str, Any]] = []
    verifying: List[Dict[str, Any]] = []

    for edge in graph.get("edges", []):
        if edge.get("target") == artifact_node.get("id"):
            source = by_id.get(edge.get("source"))
            if source:
                owners.append({
                    "edge": edge,
                    "source": source,
                })

        if edge.get("source") == artifact_node.get("id"):
            target = by_id.get(edge.get("target"))
            if target:
                verifying.append({
                    "edge": edge,
                    "target": target,
                })

    return {
        "query": "artifact-lineage",
        "artifact": artifact,
        "status": "found",
        "artifact_node": artifact_node,
        "owners": owners,
        "outgoing": verifying,
        "missing_links": [],
        "non_claim_locks": {
            **QUERY_NON_CLAIM_LOCKS,
            "hash_presence_is_not_correctness": True,
        },
    }


def orphan_artifacts(graph: Dict[str, Any]) -> Dict[str, Any]:
    validation = graph.get("validation", {})
    orphans = validation.get("orphan_artifacts", [])

    return {
        "query": "orphan-artifacts",
        "status": "found" if orphans else "none",
        "count": len(orphans),
        "orphan_artifacts": orphans,
        "non_claim_locks": dict(QUERY_NON_CLAIM_LOCKS),
    }


def query_graph(
    graph: Dict[str, Any],
    kind: str,
    run_id: Optional[str] = None,
    claim: Optional[str] = None,
    artifact: Optional[str] = None,
) -> Dict[str, Any]:
    if kind == "runs":
        return list_runs(graph)

    if kind == "artifacts-for-run":
        return artifacts_for_run(graph, run_id or "")

    if kind == "evidence-for-run":
        return evidence_for_run(graph, run_id or "")

    if kind == "downgrades":
        return downgrade_history(graph)

    if kind == "claim-evidence":
        return claim_evidence(graph, claim or "")

    if kind == "artifact-lineage":
        return artifact_lineage(graph, artifact or "")

    if kind == "orphan-artifacts":
        return orphan_artifacts(graph)

    return {
        "query": kind,
        "status": "unsupported",
        "supported_kinds": [
            "runs",
            "artifacts-for-run",
            "evidence-for-run",
            "downgrades",
            "claim-evidence",
            "artifact-lineage",
            "orphan-artifacts",
        ],
        "non_claim_locks": dict(QUERY_NON_CLAIM_LOCKS),
    }