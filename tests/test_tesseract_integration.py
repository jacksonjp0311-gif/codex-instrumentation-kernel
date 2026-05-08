import json
import tempfile
import unittest
from pathlib import Path

from cik.tesseract.index import write_tesseract_index
from cik.tesseract.integration import integrate_tesseract_if_available, load_latest_tesseract_summary


class TestTesseractIntegration(unittest.TestCase):
    def test_integrates_tesseract_and_removes_downgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "outputs"
            (out / "state").mkdir(parents=True)

            run_id = "cik_test_run"
            (out / "state" / f"{run_id}_state.json").write_text(
                json.dumps({
                    "run_id": run_id,
                    "instrument": "rcc-drift",
                    "dphi_global": 0.0,
                    "omega_mean": 1.0,
                    "maturity": "CIF6-ready",
                    "classification": "CIF-B"
                }),
                encoding="utf-8",
            )

            write_tesseract_index(out)
            summary = load_latest_tesseract_summary(out)

            self.assertTrue(summary["available"])
            self.assertEqual(summary["status"], "pass")
            self.assertEqual(summary["score"], 1.0)

            base = {
                "maturity": "CIF6-ready",
                "classification": "CIF-B",
                "downgrade_reason": [
                    "Tesseract indexing not enabled.",
                    "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
                ],
                "non_claim_locks": {}
            }

            updated = integrate_tesseract_if_available(base, output_root=out)

            self.assertTrue(updated["tesseract_lite_available"])
            self.assertTrue(updated["tesseract_lite_integrated"])
            self.assertEqual(updated["tesseract_lite_score"], 1.0)
            self.assertEqual(updated["maturity"], "CIF7-ready")
            self.assertEqual(updated["classification"], "CIF-B")
            self.assertNotIn("Tesseract indexing not enabled.", updated["downgrade_reason"])
            self.assertIn(
                "Full RootMirror verification not enabled; RootMirror-lite local continuity only.",
                updated["downgrade_reason"],
            )
            self.assertTrue(updated["non_claim_locks"]["tesseract_lite_is_not_memory_agency"])
            self.assertTrue(updated["non_claim_locks"]["index_presence_is_not_correctness"])
            self.assertTrue(updated["non_claim_locks"]["cif7_ready_is_not_cif8"])

    def test_missing_index_preserves_downgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "outputs"
            out.mkdir(parents=True)

            base = {
                "maturity": "CIF6-ready",
                "classification": "CIF-B",
                "downgrade_reason": [
                    "Tesseract indexing not enabled.",
                    "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
                ],
                "non_claim_locks": {}
            }

            updated = integrate_tesseract_if_available(base, output_root=out)

            self.assertFalse(updated["tesseract_lite_available"])
            self.assertFalse(updated["tesseract_lite_integrated"])
            self.assertIn("Tesseract indexing not enabled.", updated["downgrade_reason"])


if __name__ == "__main__":
    unittest.main()