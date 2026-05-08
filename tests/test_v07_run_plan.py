import tempfile
import unittest
from pathlib import Path

from cik.orchestration.run_plan import default_run_plan, validate_run_plan, write_default_run_plan, load_run_plan


class TestV07RunPlan(unittest.TestCase):
    def test_default_run_plan_validates(self):
        plan = default_run_plan()
        failures = validate_run_plan(plan)

        self.assertEqual(failures, [])
        self.assertEqual(plan["schema"], "CIK-v0.7-run-plan")
        self.assertTrue(plan["registry_validation_required"])

    def test_invalid_plan_fails(self):
        failures = validate_run_plan({"schema": "bad"})
        self.assertIn("invalid_schema", failures)
        self.assertIn("missing_run_id", failures)

    def test_write_and_load_default_plan(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "default_run_plan.json"
            write_default_run_plan(path)

            self.assertTrue(path.exists())

            plan = load_run_plan(path)
            self.assertEqual(plan["schema"], "CIK-v0.7-run-plan")


if __name__ == "__main__":
    unittest.main()