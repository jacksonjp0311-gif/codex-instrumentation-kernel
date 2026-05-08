from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from .contracts_v06 import InstrumentContract, contract_from_dict, validate_instrument_contract


def builtin_rcc_drift_contract() -> InstrumentContract:
    return InstrumentContract(
        name="rcc-drift",
        version="0.6",
        description="Repository-context drift measurement instrument.",
        input_contract={
            "requires_repo_path": True,
            "requires_context_index": True,
            "requires_rcc_map": True,
        },
        output_contract={
            "required": ["state", "ledger", "evidence", "report", "semantic"],
            "optional": ["rootmirror_full", "tesseract", "perturbation"],
        },
        evidence_contract={
            "schema": "CIK-evidence-package",
            "claim_boundary": "instrumentation_only",
        },
        capabilities=[
            "dphi_repo",
            "omega_repo",
            "rcc_context_drift",
            "artifact_emission",
        ],
        downgrade_policy={
            "missing_state": "downgrade",
            "missing_evidence": "downgrade",
            "missing_rootmirror_full": "downgrade_until_verified",
            "missing_tesseract": "downgrade_until_indexed",
        },
        non_claim_locks={
            "instrument_is_not_code_correctness": True,
            "dphi_is_not_truth": True,
            "omega_is_not_truth": True,
            "evidence_package_is_not_external_validation": True,
        },
    )


def registry_payload(contracts: Optional[List[InstrumentContract]] = None) -> Dict[str, Any]:
    instruments = contracts if contracts is not None else [builtin_rcc_drift_contract()]

    serialized = []
    for contract in instruments:
        serialized.append({
            "name": contract.name,
            "version": contract.version,
            "description": contract.description,
            "input_contract": contract.input_contract,
            "output_contract": contract.output_contract,
            "evidence_contract": contract.evidence_contract,
            "capabilities": contract.capabilities,
            "downgrade_policy": contract.downgrade_policy,
            "non_claim_locks": contract.non_claim_locks,
        })

    return {
        "schema": "CIK-v0.6-instrument-registry",
        "version": "0.6",
        "instruments": serialized,
        "non_claim_locks": {
            "registry_presence_is_not_instrument_validation": True,
            "plugin_contract_is_not_code_correctness": True,
            "instrument_capability_is_not_external_validation": True,
        },
    }


def write_registry(path: Path) -> Dict[str, Any]:
    payload = registry_payload()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def load_registry(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return registry_payload()
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(path: Path) -> Dict[str, Any]:
    payload = load_registry(path)
    failures: Dict[str, List[str]] = {}

    for item in payload.get("instruments", []):
        contract = contract_from_dict(item)
        result = validate_instrument_contract(contract)
        if result:
            failures[contract.name or "unknown"] = result

    status = "pass" if not failures else "fail"

    return {
        "schema": "CIK-v0.6-instrument-registry-validation",
        "status": status,
        "failures": failures,
        "instrument_count": len(payload.get("instruments", [])),
        "non_claim_locks": {
            "registry_validation_is_not_code_correctness": True,
            "registry_validation_is_not_security_proof": True,
        },
    }