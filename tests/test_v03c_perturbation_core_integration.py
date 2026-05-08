import json
import tempfile
import unittest
from pathlib import Path

from cik.core.perturbation_integration import (
    integrate_perturbation_if_available,
    load_latest_perturbation_summary,
)
from cik.perturbation import run_perturbation_sweep


def make_fixture(root: Path) -> Path:
    repo = root / "fixture"
    (repo / "docs" / "architecture").mkdir(parents=True)
    (repo / "src").mkdir(parents=True)
    (repo / "tests").mkdir(parents=True)

    (repo / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (repo / "tests" / "test_app.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    context = {
        "schema": "test-context",
        "declared_paths": [
            "src/app.py",
            "tests/test_app.py",
            "docs/architecture/rcc_context_map.json"
        ],
        "non_claim_locks": {
            "context_is_not_correctness": True
        }
    }

    (repo / "docs" / "architecture" / "rcc_context_map.json").write_text(
        json.dumps(context, indent=2),
        encoding="utf-8",
    )

    return repo


class TestV03CPerturbationCoreIntegration(unittest.TestCase):
    def test_latest_perturbation_summary_loads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make_fixture(root)
            out = root / "outputs"

            run_perturbation_sweep(repo, out)

            summary = load_latest_perturbation_summary(out_root=out, repo_root=repo)

            self.assertTrue(summary["available"])
            self.assertEqual(summary["status"], "pass")
            self.assertEqual(summary["score"], 1.0)

    def test_integrates_clean_pass_and_removes_old_downgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make_fixture(root)
            out = root / "outputs"

            run_perturbation_sweep(repo, out)

            base = {
                "status": "ok",
                "instrument": "rcc-drift",
                "dphi_global": 0.0,
                "omega_mean": 1.0,
                "cif_score": 0.7142857142857143,
                "maturity": "CIF4",
                "classification": "CIF-B",
                "downgrade_reason": [
                    "No perturbation sweep yet.",
                    "RootMirror verification not enabled.",
                    "Tesseract indexing not enabled."
                ],
                "non_claim_locks": {
                    "cifscore_is_not_truth": True
                }
            }

            updated = integrate_perturbation_if_available(base, out_root=out, repo_root=repo)

            self.assertTrue(updated["perturbation_sweep_available"])
            self.assertTrue(updated["perturbation_sweep_integrated"])
            self.assertEqual(updated["perturbation_sweep_score"], 1.0)
            self.assertEqual(updated["maturity"], "CIF6-ready")
            self.assertEqual(updated["classification"], "CIF-B")

            reasons = updated["downgrade_reason"]
            self.assertNotIn("No perturbation sweep yet.", reasons)
            self.assertNotIn("RootMirror verification not enabled.", reasons)
            self.assertIn("Full RootMirror verification not enabled; RootMirror-lite local continuity only.", reasons)
            self.assertIn("Tesseract indexing not enabled.", reasons)

            self.assertTrue(updated["non_claim_locks"]["perturbation_sweep_is_not_code_correctness"])
            self.assertTrue(updated["non_claim_locks"]["fixture_response_is_not_universal_validation"])
            self.assertTrue(updated["non_claim_locks"]["cif6_ready_is_not_cif8"])

    def test_missing_evidence_preserves_downgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make_fixture(root)
            out = root / "outputs"
            out.mkdir(parents=True)

            base = {
                "maturity": "CIF4",
                "classification": "CIF-B",
                "downgrade_reason": [
                    "No perturbation sweep yet.",
                    "RootMirror verification not enabled.",
                    "Tesseract indexing not enabled."
                ],
                "non_claim_locks": {}
            }

            updated = integrate_perturbation_if_available(base, out_root=out, repo_root=repo)

            self.assertFalse(updated["perturbation_sweep_available"])
            self.assertFalse(updated["perturbation_sweep_integrated"])
            self.assertIn("No perturbation sweep yet.", updated["downgrade_reason"])


if __name__ == "__main__":
    unittest.main()