from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def write_orchestration_outputs(bundle: Dict[str, Any], output_root: Path) -> Dict[str, str]:
    output_root = Path(output_root).resolve()
    root = output_root / "orchestration"
    evidence_root = output_root / "evidence"

    root.mkdir(parents=True, exist_ok=True)
    evidence_root.mkdir(parents=True, exist_ok=True)

    run_id = bundle["state"]["orchestration_run_id"]

    run_plan_path = root / f"{run_id}_run_plan.json"
    state_path = root / f"{run_id}_orchestration_state.json"
    composed_path = root / f"{run_id}_composed_evidence_bundle.json"
    results_path = root / f"{run_id}_instrument_results.json"
    report_path = root / f"{run_id}_orchestration_report.md"
    evidence_path = evidence_root / f"{run_id}_orchestration_evidence_package.json"

    run_plan_path.write_text(json.dumps(bundle["plan"], indent=2), encoding="utf-8")
    state_path.write_text(json.dumps(bundle["state"], indent=2), encoding="utf-8")
    composed_path.write_text(json.dumps(bundle["composed"], indent=2), encoding="utf-8")
    results_path.write_text(json.dumps(bundle["results"], indent=2), encoding="utf-8")

    evidence = {
        "schema": "CIK-v0.7-orchestration-evidence-package",
        "version": "0.7",
        "orchestration_run_id": run_id,
        "status": bundle["state"]["status"],
        "run_plan": str(run_plan_path),
        "orchestration_state": str(state_path),
        "composed_evidence_bundle": str(composed_path),
        "instrument_results": str(results_path),
        "claim_boundary": "orchestration_evidence_only",
        "non_claim_locks": bundle["state"]["non_claim_locks"],
    }

    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    lines = [
        "# CIK v0.7 Orchestration Report",
        "",
        f"Run ID: {run_id}",
        f"Status: {bundle['state']['status']}",
        f"Instrument count: {bundle['state']['instrument_count']}",
        f"Passed: {bundle['state']['passed_count']}",
        f"Failed: {bundle['state']['failed_count']}",
        f"Skipped: {bundle['state']['skipped_count']}",
        f"Blocked: {bundle['state']['blocked_count']}",
        "",
        "## Instruments",
        "",
    ]

    for result in bundle["results"]:
        lines.append(f"- {result.get('instrument')}: {result.get('status')}")

    lines.extend([
        "",
        "## Composed Downgrade Surface",
        "",
    ])

    if bundle["state"]["composed_downgrade_surface"]:
        for item in bundle["state"]["composed_downgrade_surface"]:
            lines.append(f"- {item}")

    if not bundle["state"]["composed_downgrade_surface"]:
        lines.append("- None")

    lines.extend([
        "",
        "## Non-claim locks",
        "",
        "- Orchestration is not correctness.",
        "- Composition is not truth.",
        "- Multi-instrument agreement is not external validation.",
        "- Registry validity is not instrument validity.",
        "- Evidence composition is not security proof.",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")

    bundle["state"]["artifacts"] = {
        "run_plan": str(run_plan_path),
        "orchestration_state": str(state_path),
        "composed_evidence_bundle": str(composed_path),
        "instrument_results": str(results_path),
        "orchestration_report": str(report_path),
        "orchestration_evidence": str(evidence_path),
    }

    state_path.write_text(json.dumps(bundle["state"], indent=2), encoding="utf-8")

    return bundle["state"]["artifacts"]