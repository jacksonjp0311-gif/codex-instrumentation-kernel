import unittest

from cik.rootmirror.scoring import (
    ROOTMIRROR_LITE_REASON,
    ROOTMIRROR_OLD_REASON,
    integrate_rootmirror_lite_score,
    normalize_downgrade_reasons,
    rootmirror_lite_passed,
)


class TestRootMirrorScoringIntegration(unittest.TestCase):
    def rootmirror_pass(self):
        return {
            "rootmirror_lite": {
                "score": 1.0,
                "status": "pass",
                "checks": {
                    "root_anchor_ok": True,
                    "artifact_manifest_ok": True,
                    "state_hash_ok": True,
                    "ledger_append_once_ok": True,
                    "return_to_root_ok": True,
                },
            }
        }

    def base_result(self):
        return {
            "status": "ok",
            "instrument": "rcc-drift",
            "run_id": "test",
            "dphi_global": 0.0,
            "omega_mean": 1.0,
            "cif_score": 5.0 / 7.0,
            "maturity": "CIF4",
            "classification": "CIF-B",
            "downgrade_reason": [
                "No perturbation sweep yet.",
                ROOTMIRROR_OLD_REASON,
                "Tesseract indexing not enabled.",
            ],
            "artifacts": {},
            "non_claim_locks": {
                "cifscore_is_not_truth": True,
            },
        }

    def test_rootmirror_lite_passed(self):
        self.assertTrue(rootmirror_lite_passed(self.rootmirror_pass()))

    def test_downgrade_reason_rewritten(self):
        reasons = normalize_downgrade_reasons(
            self.base_result()["downgrade_reason"],
            self.rootmirror_pass(),
        )
        self.assertNotIn(ROOTMIRROR_OLD_REASON, reasons)
        self.assertIn(ROOTMIRROR_LITE_REASON, reasons)
        self.assertIn("No perturbation sweep yet.", reasons)
        self.assertIn("Tesseract indexing not enabled.", reasons)

    def test_integrated_score_becomes_six_of_seven(self):
        result = integrate_rootmirror_lite_score(self.base_result(), self.rootmirror_pass())
        self.assertAlmostEqual(result["cif_score"], 6.0 / 7.0)
        self.assertAlmostEqual(result["cif_score_integrated"], 6.0 / 7.0)
        self.assertEqual(result["maturity"], "CIF5")
        self.assertEqual(result["classification"], "CIF-B")
        self.assertEqual(result["rootmirror_lite_status"], "pass")
        self.assertTrue(result["rootmirror_lite_integrated"])
        self.assertIn(ROOTMIRROR_LITE_REASON, result["downgrade_reason"])
        self.assertTrue(result["non_claim_locks"]["cif5_is_not_cif8"])

    def test_failed_rootmirror_does_not_improve_score(self):
        rm = {
            "rootmirror_lite": {
                "score": 0.6,
                "status": "fail",
                "checks": {},
            }
        }
        result = integrate_rootmirror_lite_score(self.base_result(), rm)
        self.assertAlmostEqual(result["cif_score"], 5.0 / 7.0)
        self.assertEqual(result["maturity"], "CIF4")
        self.assertIn("RootMirror-lite continuity verification failed.", result["downgrade_reason"])


if __name__ == "__main__":
    unittest.main()