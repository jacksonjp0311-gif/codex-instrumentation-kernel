from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def write_sweep_json(result: Dict[str, Any], out_root: str | Path) -> str:
    out = Path(out_root).resolve() / "perturbation"
    out.mkdir(parents=True, exist_ok=True)

    run_id = result.get("run_id", "cik_perturbation_sweep")
    path = out / f"{run_id}_perturbation_sweep.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return str(path)


def write_sweep_report(result: Dict[str, Any], out_root: str | Path) -> str:
    out = Path(out_root).resolve() / "perturbation"
    out.mkdir(parents=True, exist_ok=True)

    run_id = result.get("run_id", "cik_perturbation_sweep")
    path = out / f"{run_id}_perturbation_sweep_report.md"

    m = result.get("measurements", {})
    b = m.get("baseline", {})
    p = m.get("perturbed", {})
    r = m.get("restored", {})
    checks = result.get("response_checks", {})

    lines = [
        f"# CIK v0.3 Perturbation Sweep Report",
        "",
        f"Run ID: `{run_id}`",
        f"Instrument: `{result.get('instrument', '')}`",
        f"Operator: `{result.get('perturbation_operator', '')}`",
        f"Status: `{result.get('status', '')}`",
        f"Perturbation score: `{result.get('perturbation_score', '')}`",
        "",
        "## Measurements",
        "",
        "| State | DeltaPhi | Omega | Run ID |",
        "|---|---:|---:|---|",
        f"| baseline | {b.get('dphi_global')} | {b.get('omega_mean')} | `{b.get('run_id', '')}` |",
        f"| perturbed | {p.get('dphi_global')} | {p.get('omega_mean')} | `{p.get('run_id', '')}` |",
        f"| restored | {r.get('dphi_global')} | {r.get('omega_mean')} | `{r.get('run_id', '')}` |",
        "",
        "## Response checks",
        "",
    ]

    for key, value in checks.items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(
        [
            "",
            "## Non-claim locks",
            "",
            "- Perturbation sweep is not code correctness.",
            "- Fixture response is not universal validation.",
            "- Omega recovery is not truth.",
            "- CIFScore is not truth.",
            "- RCC drift is not runtime correctness.",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")

    return str(path)


def write_sweep_evidence_package(result: Dict[str, Any], out_root: str | Path, sweep_json: str, sweep_report: str) -> str:
    out = Path(out_root).resolve() / "evidence"
    out.mkdir(parents=True, exist_ok=True)

    run_id = result.get("run_id", "cik_perturbation_sweep")
    path = out / f"{run_id}_perturbation_evidence_package.json"

    package = {
        "schema": "CIK-v0.3-perturbation-evidence-package",
        "run_id": run_id,
        "claim_type": "response_validation",
        "claim_boundary": "fixture_and_declared_damage_model_only",
        "sweep_json": sweep_json,
        "sweep_report": sweep_report,
        "operator": result.get("perturbation_operator"),
        "status": result.get("status"),
        "perturbation_score": result.get("perturbation_score"),
        "measurements": result.get("measurements"),
        "response_checks": result.get("response_checks"),
        "non_claim_locks": {
            "perturbation_sweep_is_not_code_correctness": True,
            "fixture_response_is_not_universal_validation": True,
            "omega_recovery_is_not_truth": True,
            "cifscore_is_not_truth": True,
        },
    }

    path.write_text(json.dumps(package, indent=2), encoding="utf-8")

    return str(path)