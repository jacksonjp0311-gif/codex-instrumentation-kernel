import unittest

from cik.perturbation import SweepMeasurement, SweepTolerances, evaluate_sweep
from cik.perturbation.scoring import integrate_perturbation_score


class TestPerturbationFailureModes(unittest.TestCase):
    def test_sweep_fails_when_dphi_does_not_rise(self):
        baseline = SweepMeasurement("baseline", "b", 0.0, 1.0)
        perturbed = SweepMeasurement("perturbed", "p", 0.0, 1.0)
        restored = SweepMeasurement("restored", "r", 0.0, 1.0)

        result = evaluate_sweep(
            baseline,
            perturbed,
            restored,
            SweepTolerances(),
            evidence_complete=True,
        )

        self.assertNotEqual(result["status"], "pass")
        self.assertFalse(result["response_checks"]["dphi_rises_under_perturbation"])
        self.assertFalse(result["response_checks"]["omega_falls_under_perturbation"])

    def test_integrate_perturbation_score_updates_clean_pass(self):
        integrated = {
            "cif_score": 0.8571428571428572,
            "maturity": "CIF5",
            "classification": "CIF-B",
            "downgrade_reason": [
                "No perturbation sweep yet.",
                "Full RootMirror verification not enabled; RootMirror-lite local continuity only.",
                "Tesseract indexing not enabled.",
            ],
            "non_claim_locks": {
                "cifscore_is_not_truth": True
            },
        }

        sweep = {
            "status": "pass",
            "perturbation_score": 1.0,
        }

        result = integrate_perturbation_score(integrated, sweep)

        self.assertEqual(result["cif_score"], 1.0)
        self.assertEqual(result["maturity"], "CIF6-ready")
        self.assertEqual(result["classification"], "CIF-B")
        self.assertNotIn("No perturbation sweep yet.", result["downgrade_reason"])
        self.assertIn("Tesseract indexing not enabled.", result["downgrade_reason"])
        self.assertTrue(result["non_claim_locks"]["perturbation_sweep_is_not_code_correctness"])
        self.assertTrue(result["non_claim_locks"]["cif6_ready_is_not_cif8"])

    def test_integrate_perturbation_score_preserves_failure_downgrade(self):
        integrated = {
            "cif_score": 0.8571428571428572,
            "maturity": "CIF5",
            "classification": "CIF-B",
            "downgrade_reason": [],
            "non_claim_locks": {},
        }

        sweep = {
            "status": "fail",
            "perturbation_score": 0.0,
        }

        result = integrate_perturbation_score(integrated, sweep)

        self.assertEqual(result["cif_score"], 0.8571428571428572)
        self.assertEqual(result["maturity"], "CIF5")
        self.assertIn("Perturbation sweep failed or incomplete.", result["downgrade_reason"])


if __name__ == "__main__":
    unittest.main()