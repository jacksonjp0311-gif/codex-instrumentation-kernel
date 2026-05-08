import json
import tempfile
import unittest
from pathlib import Path

from cik.orchestration.executor import execute_instrument_step, execute_orchestration
from cik.orchestration.run_plan import default_run_plan
from cik.orchestration.writer import write_orchestration_outputs


class TestV07OrchestrationExecutor(unittest.TestCase):
    def _make_repo_root(self, td):
        root = Path(td)
        registry = root / "configs" / "instruments"
        registry.mkdir(parents=True)
        (registry / "instrument_registry.json").write_text(json.dumps({
            "schema": "CIK-v0.6-instrument-registry",
            "version": "0.6",
            "instruments": [
                {
                    "name": "rcc-drift",
                    "version": "0.6",
                    "description": "Repository-context drift measurement instrument.",
                    "input_contract": {"requires_repo_path": True},
                    "output_contract": {"required": ["state", "ledger", "evidence"]},
                    "evidence_contract": {"schema": "CIK-evidence-package"},
                    "capabilities": ["dphi_repo"],
                    "downgrade_policy": {"missing_evidence": "downgrade"},
                    "non_claim_locks": {"instrument_is_not_code_correctness": True}
                }
            ]
        }), encoding="utf-8")
        return root

    def test_disabled_step_returns_skipped(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._make_repo_root(td)
            out = root / "outputs"
            step = {"name": "rcc-drift", "enabled": False, "required": False}

            result = execute_instrument_step(step, root, out, "orch_test")

            self.assertEqual(result["status"], "skipped")
            self.assertIn("Instrument disabled in run plan.", result["downgrades"])

    def test_unknown_step_returns_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._make_repo_root(td)
            out = root / "outputs"
            step = {"name": "unknown", "enabled": True, "required": True}

            result = execute_instrument_step(step, root, out, "orch_test")

            self.assertEqual(result["status"], "blocked")
            self.assertIn("Instrument not present in registry.", result["downgrades"])

    def test_orchestration_blocks_on_bad_plan_but_preserves_record(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._make_repo_root(td)
            out = root / "outputs"
            plan = {
                "schema": "bad",
                "run_id": "orch_bad",
                "instruments": [
                    {"name": "rcc-drift", "enabled": True, "required": True}
                ],
                "non_claim_locks": {}
            }

            bundle = execute_orchestration(plan, root, out)

            self.assertEqual(bundle["state"]["status"], "fail")
            self.assertEqual(bundle["results"][0]["status"], "blocked")
            self.assertIn("Run plan validation failed.", bundle["results"][0]["downgrades"])

    def test_writer_emits_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = self._make_repo_root(td)
            out = root / "outputs"

            plan = default_run_plan()
            plan["run_id"] = "orch_writer"
            plan["instruments"][0]["enabled"] = False
            plan["instruments"][0]["required"] = False

            bundle = execute_orchestration(plan, root, out)
            paths = write_orchestration_outputs(bundle, out)

            self.assertTrue(Path(paths["run_plan"]).exists())
            self.assertTrue(Path(paths["orchestration_state"]).exists())
            self.assertTrue(Path(paths["composed_evidence_bundle"]).exists())
            self.assertTrue(Path(paths["instrument_results"]).exists())
            self.assertTrue(Path(paths["orchestration_report"]).exists())
            self.assertTrue(Path(paths["orchestration_evidence"]).exists())


if __name__ == "__main__":
    unittest.main()