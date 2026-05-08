from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
import json
import subprocess
import sys

from cik.instruments.registry_v06 import validate_registry
from .composer import compose_instrument_results
from .run_plan import validate_run_plan, normalize_plan_run_id


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _tail(text: str, n: int = 2000) -> str:
    if text is None:
        return ""
    return text[-n:]


def find_latest_state_run_id(output_root: Path) -> str:
    state_dir = Path(output_root) / "state"

    if not state_dir.exists():
        return ""

    files = sorted(
        [p for p in state_dir.glob("*_state.json") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
    )

    if not files:
        return ""

    latest = files[-1]

    try:
        payload = json.loads(latest.read_text(encoding="utf-8"))
        if payload.get("run_id"):
            return str(payload.get("run_id"))
    except Exception:
        pass

    name = latest.name

    if name.endswith("_state.json"):
        return name[:-len("_state.json")]

    return latest.stem


def validate_registry_gate(repo_root: Path) -> Dict[str, Any]:
    registry_path = Path(repo_root) / "configs" / "instruments" / "instrument_registry.json"
    return validate_registry(registry_path)


def registry_contains_instrument(repo_root: Path, instrument_name: str) -> bool:
    registry_path = Path(repo_root) / "configs" / "instruments" / "instrument_registry.json"

    if not registry_path.exists():
        return False

    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
    except Exception:
        return False

    for item in payload.get("instruments", []):
        if item.get("name") == instrument_name:
            return True

    return False


def execute_instrument_step(step: Dict[str, Any], repo_root: Path, output_root: Path, orchestration_run_id: str) -> Dict[str, Any]:
    instrument_name = step.get("name", "unknown")
    required = bool(step.get("required", False))
    enabled = bool(step.get("enabled", False))

    start = utc_now()

    base = {
        "schema": "CIK-v0.7-instrument-result",
        "orchestration_run_id": orchestration_run_id,
        "instrument": instrument_name,
        "required": required,
        "enabled": enabled,
        "start": start,
        "end": None,
        "status": "blocked",
        "returncode": None,
        "artifacts": {},
        "evidence": {},
        "downgrades": [],
        "score": 0.0,
        "stdout_tail": "",
        "stderr_tail": "",
        "non_claim_locks": {
            "instrument_result_is_not_correctness": True,
            "instrument_result_is_not_truth": True,
            "orchestration_preserves_per_instrument_record": True,
        }
    }

    if not enabled:
        base["status"] = "skipped"
        base["end"] = utc_now()
        base["downgrades"] = ["Instrument disabled in run plan."]
        base["non_claim_locks"]["skipped_instrument_is_preserved"] = True
        return base

    if not registry_contains_instrument(repo_root, instrument_name):
        base["status"] = "blocked"
        base["end"] = utc_now()
        base["downgrades"] = ["Instrument not present in registry."]
        base["non_claim_locks"]["blocked_instrument_is_preserved"] = True
        return base

    if instrument_name != "rcc-drift":
        base["status"] = "blocked"
        base["end"] = utc_now()
        base["downgrades"] = ["No executor available for instrument."]
        base["non_claim_locks"]["blocked_instrument_is_preserved"] = True
        return base

    input_block = step.get("input", {})
    repo_rel = input_block.get("repo", "tests/fixtures/tiny_repo_with_context")
    target_repo = Path(repo_rel)

    if not target_repo.is_absolute():
        target_repo = Path(repo_root) / target_repo

    command = [
        sys.executable,
        "-m",
        "cik",
        "run",
        "--instrument",
        "rcc-drift",
        "--repo",
        str(target_repo),
        "--out",
        str(output_root),
    ]

    completed = subprocess.run(
        command,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )

    base["returncode"] = completed.returncode
    base["stdout_tail"] = _tail(completed.stdout)
    base["stderr_tail"] = _tail(completed.stderr)
    base["end"] = utc_now()

    latest_run_id = find_latest_state_run_id(output_root)

    if latest_run_id:
        base["artifacts"]["state"] = str(Path(output_root) / "state" / f"{latest_run_id}_state.json")
        base["artifacts"]["evidence"] = str(Path(output_root) / "evidence" / f"{latest_run_id}_evidence_package.json")
        base["artifacts"]["report"] = str(Path(output_root) / "reports" / f"{latest_run_id}_drift_report.md")
        base["artifacts"]["semantic"] = str(Path(output_root) / "semantic" / f"{latest_run_id}_summary.md")
        base["artifacts"]["ledger"] = str(Path(output_root) / "ledger" / "cik_ledger.jsonl")
        base["evidence"]["instrument_run_id"] = latest_run_id

    if completed.returncode == 0:
        base["status"] = "pass"
        base["score"] = 1.0
        base["downgrades"] = []
        return base

    base["status"] = "fail"
    base["score"] = 0.0
    base["downgrades"] = ["Instrument command failed."]
    return base


def execute_orchestration(plan: Dict[str, Any], repo_root: Path, output_root: Path) -> Dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    output_root = Path(output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    plan = normalize_plan_run_id(plan)
    run_id = plan["run_id"]

    plan_failures = validate_run_plan(plan)

    registry_result = validate_registry_gate(repo_root)
    registry_ok = registry_result.get("status") == "pass"

    results: List[Dict[str, Any]] = []

    if plan_failures:
        for step in plan.get("instruments", []):
            results.append({
                "schema": "CIK-v0.7-instrument-result",
                "orchestration_run_id": run_id,
                "instrument": step.get("name", "unknown"),
                "required": bool(step.get("required", False)),
                "enabled": bool(step.get("enabled", False)),
                "status": "blocked",
                "downgrades": ["Run plan validation failed."],
                "score": 0.0,
                "artifacts": {},
                "evidence": {},
                "non_claim_locks": {
                    "blocked_instrument_is_preserved": True,
                    "run_plan_failure_is_preserved": True,
                }
            })

    if not plan_failures and not registry_ok:
        for step in plan.get("instruments", []):
            results.append({
                "schema": "CIK-v0.7-instrument-result",
                "orchestration_run_id": run_id,
                "instrument": step.get("name", "unknown"),
                "required": bool(step.get("required", False)),
                "enabled": bool(step.get("enabled", False)),
                "status": "blocked",
                "downgrades": ["Instrument registry validation failed."],
                "score": 0.0,
                "artifacts": {},
                "evidence": {},
                "non_claim_locks": {
                    "blocked_instrument_is_preserved": True,
                    "registry_failure_is_preserved": True,
                }
            })

    if not plan_failures and registry_ok:
        for step in plan.get("instruments", []):
            results.append(execute_instrument_step(step, repo_root, output_root, run_id))

    composed = compose_instrument_results(run_id, results)

    state = {
        "schema": "CIK-v0.7-orchestration-state",
        "version": "0.7",
        "orchestration_run_id": run_id,
        "created_at": plan.get("created_at"),
        "status": composed["status"],
        "registry_validation": registry_result,
        "run_plan_validation_failures": plan_failures,
        "instrument_count": len(results),
        "required_count": len([r for r in results if r.get("required")]),
        "passed_count": len([r for r in results if r.get("status") == "pass"]),
        "warning_count": len([r for r in results if r.get("status") == "warning"]),
        "failed_count": len([r for r in results if r.get("status") == "fail"]),
        "skipped_count": len([r for r in results if r.get("status") == "skipped"]),
        "blocked_count": len([r for r in results if r.get("status") == "blocked"]),
        "composed_cif_score": composed["score_summary"]["mean_score"],
        "classification": "CIF-B",
        "maturity": "CIF7-orchestration-ready",
        "instrument_results": results,
        "composed_evidence": composed,
        "composed_downgrade_surface": composed["composed_downgrade_surface"],
        "artifacts": {},
        "non_claim_locks": {
            "orchestration_is_not_correctness": True,
            "composition_is_not_truth": True,
            "multi_instrument_agreement_is_not_external_validation": True,
            "classification_is_not_truth": True,
            "maturity_is_not_correctness": True,
        }
    }

    return {
        "plan": plan,
        "results": results,
        "composed": composed,
        "state": state,
    }