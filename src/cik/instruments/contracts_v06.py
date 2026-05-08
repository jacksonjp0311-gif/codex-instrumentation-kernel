from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


MINIMUM_OUTPUTS = {"state", "ledger", "evidence"}


@dataclass
class InstrumentContract:
    name: str
    version: str
    description: str
    input_contract: Dict[str, Any]
    output_contract: Dict[str, Any]
    evidence_contract: Dict[str, Any]
    capabilities: List[str] = field(default_factory=list)
    downgrade_policy: Dict[str, str] = field(default_factory=dict)
    non_claim_locks: Dict[str, bool] = field(default_factory=dict)


def validate_instrument_contract(contract: InstrumentContract) -> List[str]:
    failures: List[str] = []

    if not contract.name:
        failures.append("missing_name")

    if not contract.version:
        failures.append("missing_version")

    if not contract.description:
        failures.append("missing_description")

    if not contract.input_contract:
        failures.append("missing_input_contract")

    if not contract.output_contract:
        failures.append("missing_output_contract")

    if not contract.evidence_contract:
        failures.append("missing_evidence_contract")

    if not contract.capabilities:
        failures.append("missing_capabilities")

    if not contract.downgrade_policy:
        failures.append("missing_downgrade_policy")

    if not contract.non_claim_locks:
        failures.append("missing_non_claim_locks")

    required_outputs = set(contract.output_contract.get("required", []))

    if not MINIMUM_OUTPUTS.issubset(required_outputs):
        failures.append("minimum_outputs_not_declared")

    return failures


def contract_from_dict(data: Dict[str, Any]) -> InstrumentContract:
    return InstrumentContract(
        name=str(data.get("name", "")),
        version=str(data.get("version", "")),
        description=str(data.get("description", "")),
        input_contract=dict(data.get("input_contract", {})),
        output_contract=dict(data.get("output_contract", {})),
        evidence_contract=dict(data.get("evidence_contract", {})),
        capabilities=list(data.get("capabilities", [])),
        downgrade_policy=dict(data.get("downgrade_policy", {})),
        non_claim_locks=dict(data.get("non_claim_locks", {})),
    )