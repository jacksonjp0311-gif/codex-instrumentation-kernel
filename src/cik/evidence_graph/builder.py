from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json

from .nodes import sha256_file, make_node, infer_artifact_type, infer_run_id
from .edges import make_edge
from .validator import validate_graph


GRAPH_NON_CLAIM_LOCKS = {
    "graph_linkage_is_not_truth": True,
    "queryability_is_not_correctness": True,
    "artifact_lineage_is_not_provenance": True,
    "graph_completeness_is_not_evidence_completeness": True,
    "evidence_graph_is_not_autonomous_memory": True,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json_maybe(path: Path) -> Optional[Dict[str, Any]]:
    if path.suffix.lower() not in {".json"}:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def iter_artifact_files(output_root: Path) -> List[Path]:
    output_root = Path(output_root)

    if not output_root.exists():
        return []

    files: List[Path] = []

    for path in output_root.rglob("*"):
        if not path.is_file():
            continue

        if path.name.startswith("."):
            continue

        files.append(path)

    return sorted(files)


def add_unique_node(nodes_by_id: Dict[str, Dict[str, Any]], node: Dict[str, Any]) -> Dict[str, Any]:
    if node["id"] not in nodes_by_id:
        nodes_by_id[node["id"]] = node
    return nodes_by_id[node["id"]]


def add_unique_edge(edges_by_id: Dict[str, Dict[str, Any]], edge: Dict[str, Any]) -> Dict[str, Any]:
    if edge["id"] not in edges_by_id:
        edges_by_id[edge["id"]] = edge
    return edges_by_id[edge["id"]]


def extract_downgrades(payload: Optional[Dict[str, Any]]) -> List[str]:
    if not payload:
        return []

    values: List[str] = []

    raw = payload.get("downgrade_reason")
    if isinstance(raw, list):
        values.extend([str(x) for x in raw])
    if isinstance(raw, str):
        values.append(raw)

    raw_surface = payload.get("composed_downgrade_surface")
    if isinstance(raw_surface, list):
        values.extend([str(x) for x in raw_surface])

    classification = payload.get("classification")
    if isinstance(classification, dict):
        class_d = classification.get("downgrade_reason")
        if isinstance(class_d, list):
            values.extend([str(x) for x in class_d])

    return sorted(set([v for v in values if v]))


def extract_claims(payload: Optional[Dict[str, Any]]) -> List[str]:
    if not payload:
        return []

    claims: List[str] = []

    locks = payload.get("non_claim_locks")
    if isinstance(locks, dict):
        claims.extend([k for k, v in locks.items() if bool(v)])

    boundaries = payload.get("claim_boundaries")
    if isinstance(boundaries, dict):
        claims.extend([k for k, v in boundaries.items() if bool(v)])

    claim = payload.get("claim_boundary")
    if claim:
        claims.append(str(claim))

    return sorted(set([c for c in claims if c]))


def infer_instrument(payload: Optional[Dict[str, Any]], artifact_type: str) -> Optional[str]:
    if payload:
        if payload.get("instrument"):
            return str(payload.get("instrument"))

        if payload.get("instruments") and isinstance(payload.get("instruments"), list):
            return "orchestration"

        if payload.get("instrument_results"):
            return "orchestration"

    if artifact_type == "orchestration":
        return "orchestration"

    if artifact_type == "perturbation":
        return "rcc-drift-compatible-context-measurement"

    return None


def build_evidence_graph(output_root: Path) -> Dict[str, Any]:
    output_root = Path(output_root).resolve()

    nodes_by_id: Dict[str, Dict[str, Any]] = {}
    edges_by_id: Dict[str, Dict[str, Any]] = {}

    artifact_files = iter_artifact_files(output_root)

    run_nodes: Dict[str, Dict[str, Any]] = {}
    instrument_nodes: Dict[str, Dict[str, Any]] = {}
    downgrade_nodes: Dict[str, Dict[str, Any]] = {}
    claim_nodes: Dict[str, Dict[str, Any]] = {}

    for path in artifact_files:
        rel = str(path.relative_to(output_root)).replace("\\", "/")
        payload = load_json_maybe(path)
        artifact_type = infer_artifact_type(path)
        file_hash = sha256_file(path)
        run_id = infer_run_id(path, payload)
        instrument = infer_instrument(payload, artifact_type)

        artifact_node = make_node(
            node_type="artifact",
            label=path.name,
            source="file",
            path=str(path),
            file_hash=file_hash,
            run_id=run_id,
            instrument=instrument,
            metadata={
                "artifact_type": artifact_type,
                "relative_path": rel,
                "size_bytes": path.stat().st_size,
            },
        )
        add_unique_node(nodes_by_id, artifact_node)

        if run_id:
            run_node = make_node(
                node_type="run",
                label=run_id,
                source="artifact_inference",
                path=None,
                file_hash=None,
                run_id=run_id,
                instrument=instrument,
                metadata={"source_artifact": rel},
            )
            run_node = add_unique_node(nodes_by_id, run_node)
            run_nodes[run_id] = run_node

            add_unique_edge(
                edges_by_id,
                make_edge(
                    "has_artifact",
                    run_node["id"],
                    artifact_node["id"],
                    support=str(path),
                    status="artifact_backed",
                    metadata={"artifact_type": artifact_type},
                ),
            )

        if instrument:
            instrument_node = make_node(
                node_type="instrument",
                label=instrument,
                source="artifact_inference",
                path=None,
                file_hash=None,
                run_id=None,
                instrument=instrument,
                metadata={},
            )
            instrument_node = add_unique_node(nodes_by_id, instrument_node)
            instrument_nodes[instrument] = instrument_node

            if run_id:
                add_unique_edge(
                    edges_by_id,
                    make_edge(
                        "used_instrument",
                        run_nodes[run_id]["id"],
                        instrument_node["id"],
                        support=str(path),
                        status="artifact_backed",
                    ),
                )

        if artifact_type == "evidence":
            evidence_node = make_node(
                node_type="evidence",
                label=path.name,
                source="file",
                path=str(path),
                file_hash=file_hash,
                run_id=run_id,
                instrument=instrument,
                metadata={"relative_path": rel},
            )
            evidence_node = add_unique_node(nodes_by_id, evidence_node)

            if run_id:
                add_unique_edge(
                    edges_by_id,
                    make_edge(
                        "has_evidence",
                        run_nodes[run_id]["id"],
                        evidence_node["id"],
                        support=str(path),
                        status="artifact_backed",
                    ),
                )

        if artifact_type == "rootmirror":
            rootmirror_node = make_node(
                node_type="rootmirror",
                label=path.name,
                source="file",
                path=str(path),
                file_hash=file_hash,
                run_id=run_id,
                instrument=instrument,
                metadata={"relative_path": rel},
            )
            rootmirror_node = add_unique_node(nodes_by_id, rootmirror_node)

            if run_id:
                add_unique_edge(
                    edges_by_id,
                    make_edge(
                        "verified_by",
                        run_nodes[run_id]["id"],
                        rootmirror_node["id"],
                        support=str(path),
                        status="artifact_backed",
                    ),
                )

        if artifact_type == "tesseract":
            tesseract_node = make_node(
                node_type="tesseract",
                label=path.name,
                source="file",
                path=str(path),
                file_hash=file_hash,
                run_id=run_id,
                instrument=instrument,
                metadata={"relative_path": rel},
            )
            add_unique_node(nodes_by_id, tesseract_node)

        if artifact_type == "orchestration":
            orchestration_node = make_node(
                node_type="orchestration",
                label=path.name,
                source="file",
                path=str(path),
                file_hash=file_hash,
                run_id=run_id,
                instrument="orchestration",
                metadata={"relative_path": rel},
            )
            orchestration_node = add_unique_node(nodes_by_id, orchestration_node)

            if run_id:
                add_unique_edge(
                    edges_by_id,
                    make_edge(
                        "composed_from",
                        run_nodes[run_id]["id"],
                        orchestration_node["id"],
                        support=str(path),
                        status="artifact_backed",
                    ),
                )

        for downgrade in extract_downgrades(payload):
            downgrade_node = make_node(
                node_type="downgrade",
                label=downgrade,
                source="artifact_declared",
                path=None,
                file_hash=None,
                run_id=None,
                instrument=instrument,
                metadata={"downgrade": downgrade},
            )
            downgrade_node = add_unique_node(nodes_by_id, downgrade_node)
            downgrade_nodes[downgrade] = downgrade_node

            if run_id:
                add_unique_edge(
                    edges_by_id,
                    make_edge(
                        "has_downgrade",
                        run_nodes[run_id]["id"],
                        downgrade_node["id"],
                        support=str(path),
                        status="artifact_backed",
                    ),
                )

        for claim in extract_claims(payload):
            claim_node = make_node(
                node_type="claim",
                label=claim,
                source="artifact_declared",
                path=None,
                file_hash=None,
                run_id=None,
                instrument=instrument,
                metadata={"claim": claim},
            )
            claim_node = add_unique_node(nodes_by_id, claim_node)
            claim_nodes[claim] = claim_node

            if run_id:
                add_unique_edge(
                    edges_by_id,
                    make_edge(
                        "declares_boundary",
                        run_nodes[run_id]["id"],
                        claim_node["id"],
                        support=str(path),
                        status="artifact_backed",
                    ),
                )

    graph = {
        "schema": "CIK-v0.8-evidence-graph",
        "version": "0.8",
        "generated_at": utc_now(),
        "output_root": str(output_root),
        "node_count": len(nodes_by_id),
        "edge_count": len(edges_by_id),
        "nodes": list(nodes_by_id.values()),
        "edges": list(edges_by_id.values()),
        "indexes": {
            "runs": {k: v["id"] for k, v in sorted(run_nodes.items())},
            "artifacts": {
                n["path"]: n["id"]
                for n in nodes_by_id.values()
                if n["type"] == "artifact" and n.get("path")
            },
            "instruments": {k: v["id"] for k, v in sorted(instrument_nodes.items())},
            "downgrades": {k: v["id"] for k, v in sorted(downgrade_nodes.items())},
            "claims": {k: v["id"] for k, v in sorted(claim_nodes.items())},
        },
        "validation": {},
        "non_claim_locks": dict(GRAPH_NON_CLAIM_LOCKS),
    }

    graph["validation"] = validate_graph(graph)

    return graph