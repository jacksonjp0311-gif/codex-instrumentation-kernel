from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Tuple


VIEW_NON_CLAIM_LOCKS = {
    "dashboard_view_is_navigation_not_truth": True,
    "visual_summary_is_not_validation": True,
    "tesseract_linkage_is_not_provenance": True,
}


def nodes_by_type(graph: Dict[str, Any], node_type: str) -> List[Dict[str, Any]]:
    return [n for n in graph.get("nodes", []) if n.get("type") == node_type]


def edges_by_type(graph: Dict[str, Any], edge_type: str) -> List[Dict[str, Any]]:
    return [e for e in graph.get("edges", []) if e.get("type") == edge_type]


def node_index(graph: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {n.get("id"): n for n in graph.get("nodes", [])}


def build_run_family_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    families: Dict[str, Dict[str, Any]] = {}

    for run in nodes_by_type(graph, "run"):
        instrument = run.get("instrument") or "unknown"
        family_id = f"family:instrument:{instrument}"

        if family_id not in families:
            families[family_id] = {
                "family_id": family_id,
                "family_type": "instrument",
                "instrument": instrument,
                "runs": [],
                "artifacts": [],
                "evidence": [],
                "downgrades": [],
                "status": "graph_derived",
                "support": "graph_derived",
                "non_claim_locks": dict(VIEW_NON_CLAIM_LOCKS),
            }

        families[family_id]["runs"].append(run.get("run_id"))

    by_id = node_index(graph)

    for edge in graph.get("edges", []):
        source = by_id.get(edge.get("source"))
        target = by_id.get(edge.get("target"))

        if not source or not target:
            continue

        if source.get("type") != "run":
            continue

        instrument = source.get("instrument") or "unknown"
        family_id = f"family:instrument:{instrument}"

        if family_id not in families:
            continue

        if target.get("type") == "artifact":
            families[family_id]["artifacts"].append(target.get("path") or target.get("label"))

        if target.get("type") == "evidence":
            families[family_id]["evidence"].append(target.get("path") or target.get("label"))

        if target.get("type") == "downgrade":
            families[family_id]["downgrades"].append(target.get("label"))

    for family in families.values():
        family["runs"] = sorted(set([x for x in family["runs"] if x]))
        family["artifacts"] = sorted(set([x for x in family["artifacts"] if x]))
        family["evidence"] = sorted(set([x for x in family["evidence"] if x]))
        family["downgrades"] = sorted(set([x for x in family["downgrades"] if x]))

    return sorted(families.values(), key=lambda x: x["family_id"])


def build_instrument_health_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    runs = nodes_by_type(graph, "run")
    instruments = nodes_by_type(graph, "instrument")
    by_instrument: Dict[str, Dict[str, Any]] = {}

    for instrument_node in instruments:
        name = instrument_node.get("instrument") or instrument_node.get("label") or "unknown"
        by_instrument[name] = {
            "instrument": name,
            "run_count": 0,
            "pass_count": 0,
            "warning_count": 0,
            "fail_count": 0,
            "blocked_count": 0,
            "skipped_count": 0,
            "latest_run": None,
            "downgrades": [],
            "evidence_coverage": 0,
            "non_claim_locks": {
                **VIEW_NON_CLAIM_LOCKS,
                "instrument_health_is_not_correctness": True,
            },
        }

    for run in runs:
        name = run.get("instrument") or "unknown"

        if name not in by_instrument:
            by_instrument[name] = {
                "instrument": name,
                "run_count": 0,
                "pass_count": 0,
                "warning_count": 0,
                "fail_count": 0,
                "blocked_count": 0,
                "skipped_count": 0,
                "latest_run": None,
                "downgrades": [],
                "evidence_coverage": 0,
                "non_claim_locks": {
                    **VIEW_NON_CLAIM_LOCKS,
                    "instrument_health_is_not_correctness": True,
                },
            }

        by_instrument[name]["run_count"] += 1
        by_instrument[name]["latest_run"] = run.get("run_id")

    by_id = node_index(graph)

    for edge in graph.get("edges", []):
        source = by_id.get(edge.get("source"))
        target = by_id.get(edge.get("target"))

        if not source or not target or source.get("type") != "run":
            continue

        name = source.get("instrument") or "unknown"

        if name not in by_instrument:
            continue

        if target.get("type") == "evidence":
            by_instrument[name]["evidence_coverage"] += 1

        if target.get("type") == "downgrade":
            by_instrument[name]["downgrades"].append(target.get("label"))

    for item in by_instrument.values():
        item["downgrades"] = sorted(set([x for x in item["downgrades"] if x]))

    return sorted(by_instrument.values(), key=lambda x: x["instrument"])


def build_evidence_maturity_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = node_index(graph)
    rows: List[Dict[str, Any]] = []

    for run in nodes_by_type(graph, "run"):
        run_id = run.get("run_id")
        evidence_packages = []
        rootmirror_records = []
        tesseract_records = []
        orchestration_records = []
        downgrades = []

        for edge in graph.get("edges", []):
            if edge.get("source") != run.get("id"):
                continue

            target = by_id.get(edge.get("target"))
            if not target:
                continue

            if target.get("type") == "evidence":
                evidence_packages.append(target.get("path") or target.get("label"))

            if target.get("type") == "rootmirror":
                rootmirror_records.append(target.get("path") or target.get("label"))

            if target.get("type") == "tesseract":
                tesseract_records.append(target.get("path") or target.get("label"))

            if target.get("type") == "orchestration":
                orchestration_records.append(target.get("path") or target.get("label"))

            if target.get("type") == "downgrade":
                downgrades.append(target.get("label"))

        rows.append({
            "run_id": run_id,
            "instrument": run.get("instrument"),
            "classification": "CIF-B",
            "maturity": "dashboard-visible",
            "cif_score": None,
            "evidence_packages": sorted(set([x for x in evidence_packages if x])),
            "rootmirror_records": sorted(set([x for x in rootmirror_records if x])),
            "tesseract_records": sorted(set([x for x in tesseract_records if x])),
            "orchestration_records": sorted(set([x for x in orchestration_records if x])),
            "downgrades": sorted(set([x for x in downgrades if x])),
            "non_claim_locks": {
                **VIEW_NON_CLAIM_LOCKS,
                "dashboard_maturity_does_not_promote_maturity": True,
                "cif_b_display_is_not_truth": True,
            },
        })

    return sorted(rows, key=lambda x: str(x.get("run_id")))


def build_downgrade_timeline_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = node_index(graph)
    timeline: Dict[str, Dict[str, Any]] = {}

    for edge in edges_by_type(graph, "has_downgrade"):
        source = by_id.get(edge.get("source"))
        target = by_id.get(edge.get("target"))

        if not source or not target:
            continue

        label = target.get("label")

        if label not in timeline:
            timeline[label] = {
                "downgrade": label,
                "first_seen": source.get("run_id"),
                "last_seen": source.get("run_id"),
                "runs": [],
                "frequency": 0,
                "status": "active",
                "resolved_by": None,
                "support": "artifact_backed",
                "non_claim_locks": {
                    **VIEW_NON_CLAIM_LOCKS,
                    "downgrade_timeline_is_not_resolution": True,
                },
            }

        timeline[label]["runs"].append(source.get("run_id"))

    for item in timeline.values():
        item["runs"] = sorted(set([x for x in item["runs"] if x]))
        item["frequency"] = len(item["runs"])
        if item["frequency"] > 1:
            item["status"] = "recurring"
        if item["runs"]:
            item["first_seen"] = item["runs"][0]
            item["last_seen"] = item["runs"][-1]

    return sorted(timeline.values(), key=lambda x: str(x.get("downgrade")))


def build_claim_boundary_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = node_index(graph)
    rows: Dict[str, Dict[str, Any]] = {}

    for claim_node in nodes_by_type(graph, "claim"):
        claim = claim_node.get("label")

        if claim not in rows:
            rows[claim] = {
                "claim": claim,
                "status": "declared",
                "declared_by": [],
                "bounded_by": [],
                "support": "artifact_backed",
                "missing_support": [],
                "non_claim_locks": {
                    **VIEW_NON_CLAIM_LOCKS,
                    "claim_panel_is_not_truth": True,
                },
            }

    for edge in edges_by_type(graph, "declares_boundary"):
        source = by_id.get(edge.get("source"))
        target = by_id.get(edge.get("target"))

        if not source or not target:
            continue

        claim = target.get("label")

        if claim not in rows:
            rows[claim] = {
                "claim": claim,
                "status": "declared",
                "declared_by": [],
                "bounded_by": [],
                "support": "artifact_backed",
                "missing_support": [],
                "non_claim_locks": {
                    **VIEW_NON_CLAIM_LOCKS,
                    "claim_panel_is_not_truth": True,
                },
            }

        rows[claim]["declared_by"].append(source.get("run_id") or source.get("label"))
        rows[claim]["bounded_by"].append(edge.get("support"))

    for row in rows.values():
        row["declared_by"] = sorted(set([x for x in row["declared_by"] if x]))
        row["bounded_by"] = sorted(set([x for x in row["bounded_by"] if x]))

    return sorted(rows.values(), key=lambda x: str(x.get("claim")))


def build_rootmirror_linkage_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = node_index(graph)
    rows = []

    for edge in edges_by_type(graph, "verified_by"):
        source = by_id.get(edge.get("source"))
        target = by_id.get(edge.get("target"))

        if not source or not target:
            continue

        rows.append({
            "run_id": source.get("run_id"),
            "rootmirror_record": target.get("path") or target.get("label"),
            "support": edge.get("support"),
            "status": edge.get("status"),
            "non_claim_locks": {
                **VIEW_NON_CLAIM_LOCKS,
                "rootmirror_linkage_is_not_code_correctness": True,
            },
        })

    return rows


def build_orchestration_linkage_view(graph: Dict[str, Any]) -> List[Dict[str, Any]]:
    by_id = node_index(graph)
    rows = []

    for edge in edges_by_type(graph, "composed_from"):
        source = by_id.get(edge.get("source"))
        target = by_id.get(edge.get("target"))

        if not source or not target:
            continue

        rows.append({
            "run_id": source.get("run_id"),
            "orchestration_record": target.get("path") or target.get("label"),
            "support": edge.get("support"),
            "status": edge.get("status"),
            "non_claim_locks": {
                **VIEW_NON_CLAIM_LOCKS,
                "orchestration_linkage_is_not_correctness": True,
            },
        })

    return rows


def build_all_views(graph: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "run_families": build_run_family_view(graph),
        "instrument_health": build_instrument_health_view(graph),
        "evidence_maturity": build_evidence_maturity_view(graph),
        "downgrade_timeline": build_downgrade_timeline_view(graph),
        "claim_boundaries": build_claim_boundary_view(graph),
        "rootmirror_linkage": build_rootmirror_linkage_view(graph),
        "orchestration_linkage": build_orchestration_linkage_view(graph),
    }