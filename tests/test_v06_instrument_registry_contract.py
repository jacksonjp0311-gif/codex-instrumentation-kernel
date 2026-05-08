import json
import tempfile
import unittest
from pathlib import Path

from cik.instruments.contracts_v06 import InstrumentContract, validate_instrument_contract
from cik.instruments.registry_v06 import (
    builtin_rcc_drift_contract,
    registry_payload,
    write_registry,
    validate_registry,
)


class TestV06InstrumentRegistryContract(unittest.TestCase):
    def test_builtin_rcc_drift_contract_validates(self):
        contract = builtin_rcc_drift_contract()
        failures = validate_instrument_contract(contract)

        self.assertEqual(failures, [])
        self.assertEqual(contract.name, "rcc-drift")
        self.assertIn("state", contract.output_contract["required"])
        self.assertIn("evidence", contract.output_contract["required"])

    def test_contract_rejects_missing_minimum_outputs(self):
        contract = InstrumentContract(
            name="bad-instrument",
            version="0.1",
            description="Bad test instrument.",
            input_contract={"requires_repo_path": True},
            output_contract={"required": ["state"]},
            evidence_contract={"schema": "test"},
            capabilities=["test"],
            downgrade_policy={"missing_evidence": "downgrade"},
            non_claim_locks={"instrument_is_not_correctness": True},
        )

        failures = validate_instrument_contract(contract)

        self.assertIn("minimum_outputs_not_declared", failures)

    def test_registry_payload_contains_non_claim_locks(self):
        payload = registry_payload()

        self.assertEqual(payload["schema"], "CIK-v0.6-instrument-registry")
        self.assertEqual(len(payload["instruments"]), 1)
        self.assertTrue(payload["non_claim_locks"]["registry_presence_is_not_instrument_validation"])

    def test_write_and_validate_registry(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "instrument_registry.json"
            write_registry(path)

            self.assertTrue(path.exists())

            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "CIK-v0.6-instrument-registry")

            result = validate_registry(path)
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["instrument_count"], 1)


if __name__ == "__main__":
    unittest.main()