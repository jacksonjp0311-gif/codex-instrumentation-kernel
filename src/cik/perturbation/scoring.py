from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List
import copy


@dataclass
class SweepTolerances:
    epsilon_rise: float = 1e-9
    epsilon_fall: float = 1e-9
    epsilon_dphi_recovery: float = 1e-9
    epsilon_omega_recovery: float = 1e-9


@dataclass
class SweepMeasurement:
    label: str
    run_id: str
    dphi_global: float
    omega_mean: float
    state_path: str = ""
    evidence_path: str = ""


def clamp01(x: float) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def omega_from_dphi(dphi: float) -> float:
    return 1.0 / (1.0 + abs(float(dphi)))


def evaluate_sweep(
    baseline: SweepMeasurement,
    perturbed: SweepMeasurement,
    restored: SweepMeasurement,
    tolerances: SweepTolerances | None = None,
    evidence_complete: bool = True,
) -> Dict[str, Any]:
    tol = tolerances or SweepTolerances()

    dphi_rise = perturbed.dphi_global > baseline.dphi_global + tol.epsilon_rise
    omega_fall = perturbed.omega_mean < baseline.omega_mean - tol.epsilon_fall

    dphi_recovery = abs(restored.dphi_global - baseline.dphi_global) <= tol.epsilon_dphi_recovery
    omega_recovery = abs(restored.omega_mean - baseline.omega_mean) <= tol.epsilon_omega_recovery

    checks = {
        "dphi_rises_under_perturbation": bool(dphi_rise),
        "omega_falls_under_perturbation": bool(omega_fall),
        "dphi_recovers_after_restore": bool(dphi_recovery),
        "omega_recovers_after_restore": bool(omega_recovery),
        "sweep_evidence_complete": bool(evidence_complete),
    }

    weights = {
        "dphi_rises_under_perturbation": 0.25,
        "omega_falls_under_perturbation": 0.25,
        "dphi_recovers_after_restore": 0.20,
        "omega_recovers_after_restore": 0.20,
        "sweep_evidence_complete": 0.10,
    }

    score = clamp01(sum(weights[k] for k, v in checks.items() if v))

    if score >= 1.0:
        status = "pass"
    elif score >= 0.75:
        status = "warning"
    else:
        status = "fail"

    return {
        "response_checks": checks,
        "perturbation_score": score,
        "status": status,
    }


def build_sweep_result(
    run_id: str,
    instrument: str,
    fixture: str,
    perturbation_operator: str,
    baseline: SweepMeasurement,
    perturbed: SweepMeasurement,
    restored: SweepMeasurement,
    tolerances: SweepTolerances | None = None,
    perturbation_record: Dict[str, Any] | None = None,
    evidence_complete: bool = True,
) -> Dict[str, Any]:
    tol = tolerances or SweepTolerances()
    evaluation = evaluate_sweep(
        baseline=baseline,
        perturbed=perturbed,
        restored=restored,
        tolerances=tol,
        evidence_complete=evidence_complete,
    )

    return {
        "schema": "CIK-v0.3-perturbation-sweep",
        "run_id": run_id,
        "instrument": instrument,
        "fixture": fixture,
        "perturbation_operator": perturbation_operator,
        "tolerances": asdict(tol),
        "perturbation_record": perturbation_record or {},
        "measurements": {
            "baseline": asdict(baseline),
            "perturbed": asdict(perturbed),
            "restored": asdict(restored),
        },
        "response_checks": evaluation["response_checks"],
        "perturbation_score": evaluation["perturbation_score"],
        "status": evaluation["status"],
        "non_claim_locks": {
            "perturbation_sweep_is_not_code_correctness": True,
            "fixture_response_is_not_universal_validation": True,
            "omega_recovery_is_not_truth": True,
            "cifscore_is_not_truth": True,
            "rcc_drift_is_not_runtime_correctness": True,
        },
    }


def integrate_perturbation_score(
    integrated_result: Dict[str, Any],
    sweep_result: Dict[str, Any],
) -> Dict[str, Any]:
    result = copy.deepcopy(integrated_result)
    perturb_score = clamp01(sweep_result.get("perturbation_score", 0.0))

    result["perturbation_sweep_score"] = perturb_score
    result["perturbation_sweep_status"] = sweep_result.get("status", "unknown")
    result["perturbation_sweep_integrated"] = True

    if perturb_score == 1.0:
        result["cif_score_base_before_perturbation"] = result.get("cif_score", 0.0)
        result["cif_score"] = 1.0
        result["cif_score_integrated"] = 1.0
        result["maturity_base_before_perturbation"] = result.get("maturity", "CIF5")
        result["maturity"] = "CIF6-ready"
        result["maturity_note"] = (
            "Perturbation sweep passed; full RootMirror and Tesseract indexing remain deferred."
        )

        reasons = list(result.get("downgrade_reason") or [])
        reasons = [r for r in reasons if r != "No perturbation sweep yet."]

        rootmirror_reason = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
        tesseract_reason = "Tesseract indexing not enabled."

        if rootmirror_reason not in reasons:
            reasons.append(rootmirror_reason)
        if tesseract_reason not in reasons:
            reasons.append(tesseract_reason)

        result["downgrade_reason"] = reasons
    else:
        reasons = list(result.get("downgrade_reason") or [])
        if "Perturbation sweep failed or incomplete." not in reasons:
            reasons.insert(0, "Perturbation sweep failed or incomplete.")
        result["downgrade_reason"] = reasons

    result.setdefault("non_claim_locks", {})
    result["non_claim_locks"]["perturbation_sweep_is_not_code_correctness"] = True
    result["non_claim_locks"]["fixture_response_is_not_universal_validation"] = True
    result["non_claim_locks"]["omega_recovery_is_not_truth"] = True
    result["non_claim_locks"]["cifscore_is_not_truth"] = True
    result["non_claim_locks"]["cif6_ready_is_not_cif8"] = True

    return result