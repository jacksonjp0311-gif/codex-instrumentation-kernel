from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_tesseract_outputs(bundle: Dict[str, Any], output_root: Path) -> Dict[str, str]:
    output_root = Path(output_root).resolve()

    tesseract_root = output_root / "tesseract_full"
    dashboard_root = output_root / "dashboard"
    evidence_root = output_root / "evidence"

    tesseract_root.mkdir(parents=True, exist_ok=True)
    dashboard_root.mkdir(parents=True, exist_ok=True)
    evidence_root.mkdir(parents=True, exist_ok=True)

    package = bundle["package"]
    dashboard = bundle["dashboard"]
    release_readiness = bundle["release_readiness"]

    package_path = tesseract_root / "tesseract_full_package.json"
    package_report_path = tesseract_root / "tesseract_full_report.md"
    dashboard_json_path = dashboard_root / "dashboard_data.json"
    dashboard_report_path = dashboard_root / "dashboard_report.md"
    release_path = dashboard_root / "release_readiness_summary.md"
    evidence_path = evidence_root / "tesseract_full_evidence_package.json"

    _write_json(package_path, package)
    _write_json(dashboard_json_path, dashboard)

    package_report_lines = [
        "# CIK v0.9 Full Tesseract Package Report",
        "",
        f"Schema: {package.get('schema')}",
        f"Version: {package.get('version')}",
        f"Node count: {package.get('node_count')}",
        f"Edge count: {package.get('edge_count')}",
        f"Graph validation: {package.get('graph_validation', {}).get('status')}",
        f"Release readiness: {release_readiness.get('status')}",
        "",
        "## View counts",
        "",
    ]

    for key, value in package.get("views", {}).items():
        count = len(value) if isinstance(value, list) else 0
        package_report_lines.append(f"- {key}: {count}")

    package_report_lines.extend([
        "",
        "## Non-claim locks",
        "",
        "- Visualization is not validation.",
        "- Tesseract linkage is not provenance.",
        "- Dashboard completeness is not evidence completeness.",
        "- Release-readiness is not release proof.",
        "",
    ])

    package_report_path.write_text("\n".join(package_report_lines), encoding="utf-8")

    dashboard_report_lines = [
        "# CIK v0.9 Dashboard Report",
        "",
        "## Summary",
        "",
    ]

    for key, value in dashboard.get("summary", {}).items():
        dashboard_report_lines.append(f"- {key}: {value}")

    dashboard_report_lines.extend([
        "",
        "## Dashboard Views",
        "",
    ])

    for key, value in dashboard.get("views", {}).items():
        count = len(value) if isinstance(value, list) else 0
        dashboard_report_lines.append(f"- {key}: {count}")

    dashboard_report_lines.extend([
        "",
        "## Non-claim locks",
        "",
        "- Dashboard is navigation, not truth.",
        "- Visualization is not validation.",
        "- Dashboard completeness is not evidence completeness.",
        "",
    ])

    dashboard_report_path.write_text("\n".join(dashboard_report_lines), encoding="utf-8")

    readiness_lines = [
        "# CIK v0.9 Release-Readiness Summary",
        "",
        f"Status: {release_readiness.get('status')}",
        "",
        "## Blocking gaps",
        "",
    ]

    blocking = release_readiness.get("blocking_gaps", [])
    if blocking:
        readiness_lines.extend([f"- {item}" for item in blocking])
    else:
        readiness_lines.append("- None")

    readiness_lines.extend([
        "",
        "## Warnings",
        "",
    ])

    warnings = release_readiness.get("warnings", [])
    if warnings:
        readiness_lines.extend([f"- {item}" for item in warnings])
    else:
        readiness_lines.append("- None")

    readiness_lines.extend([
        "",
        "## v1.0 Gate",
        "",
    ])

    for key, value in release_readiness.get("v1_0_gate", {}).items():
        readiness_lines.append(f"- {key}: {value}")

    readiness_lines.extend([
        "",
        "## Non-claim locks",
        "",
        "- Release-readiness is not release proof.",
        "- Readiness summary is not a security proof.",
        "- Ready status is not a public guarantee.",
        "",
    ])

    release_path.write_text("\n".join(readiness_lines), encoding="utf-8")

    evidence = {
        "schema": "CIK-v0.9-tesseract-full-evidence-package",
        "version": "0.9",
        "status": release_readiness.get("status"),
        "tesseract_full_package": str(package_path),
        "tesseract_full_report": str(package_report_path),
        "dashboard_json": str(dashboard_json_path),
        "dashboard_report": str(dashboard_report_path),
        "release_readiness_summary": str(release_path),
        "claim_boundary": "dashboard_navigation_only",
        "non_claim_locks": package.get("non_claim_locks", {}),
    }

    _write_json(evidence_path, evidence)

    return {
        "tesseract_full_package": str(package_path),
        "tesseract_full_report": str(package_report_path),
        "dashboard_json": str(dashboard_json_path),
        "dashboard_report": str(dashboard_report_path),
        "release_readiness_summary": str(release_path),
        "evidence": str(evidence_path),
    }