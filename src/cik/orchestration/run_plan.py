from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_orchestration_run_id() -> str:
    return "cik_orchestration_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def default_run_plan() -> Dict[str, Any]:
    return {
        "schema": "CIK-v0.7-run-plan",
        "run_id": make_orchestration_run_id(),
        "created_at": utc_now(),
        "mode": "sequential",
        "registry_validation_required": True,
        "instruments": [
            {
                "name": "rcc-drift",
                "enabled": True,
                "required": True,
                "input": {
                    "repo": "tests/fixtures/tiny_repo_with_context"
                },
                "expected_outputs": [
                    "state",
                    "ledger",
                    "evidence",
                    "report",
                    "semantic"
                ]
            }
        ],
        "failure_policy": {
            "preserve_failed_records": True,
            "continue_on_optional_failure": True,
            "stop_on_required_failure": False
        },
        "non_claim_locks": {
            "run_plan_is_not_execution": True,
            "orchestration_is_not_correctness": True,
            "multi_instrument_agreement_is_not_truth": True
        }
    }


def load_run_plan(path: Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_default_run_plan(path: Path) -> Dict[str, Any]:
    plan = default_run_plan()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    return plan


def validate_run_plan(plan: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if plan.get("schema") != "CIK-v0.7-run-plan":
        failures.append("invalid_schema")

    if not plan.get("run_id"):
        failures.append("missing_run_id")

    if not plan.get("created_at"):
        failures.append("missing_created_at")

    if plan.get("mode") not in {"sequential"}:
        failures.append("unsupported_mode")

    if plan.get("registry_validation_required") is not True:
        failures.append("registry_validation_not_required")

    instruments = plan.get("instruments", [])

    if not isinstance(instruments, list):
        failures.append("instruments_not_list")

    if isinstance(instruments, list) and len(instruments) == 0:
        failures.append("no_instruments")

    if isinstance(instruments, list):
        for idx, instrument in enumerate(instruments):
            prefix = f"instrument_{idx}"
            if not instrument.get("name"):
                failures.append(prefix + "_missing_name")
            if "enabled" not in instrument:
                failures.append(prefix + "_missing_enabled")
            if "required" not in instrument:
                failures.append(prefix + "_missing_required")
            if "expected_outputs" not in instrument:
                failures.append(prefix + "_missing_expected_outputs")

    locks = plan.get("non_claim_locks", {})

    if not locks.get("orchestration_is_not_correctness"):
        failures.append("missing_orchestration_non_claim_lock")

    if not locks.get("multi_instrument_agreement_is_not_truth"):
        failures.append("missing_agreement_non_claim_lock")

    return failures


def normalize_plan_run_id(plan: Dict[str, Any]) -> Dict[str, Any]:
    copy = dict(plan)
    if not copy.get("run_id"):
        copy["run_id"] = make_orchestration_run_id()
    if not copy.get("created_at"):
        copy["created_at"] = utc_now()
    return copy