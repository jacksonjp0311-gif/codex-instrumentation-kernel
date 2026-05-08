import tempfile
import unittest
from pathlib import Path

from cik.release.checklist import build_release_checklist, REQUIRED_SMOKES


class TestV10ReleaseChecklist(unittest.TestCase):
    def test_checklist_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checklist = build_release_checklist(root)
            self.assertEqual(checklist["status"], "fail")
            self.assertGreater(len(checklist["blocking_gaps"]), 0)
            self.assertTrue(checklist["non_claim_locks"]["checklist_is_not_certification"])

    def test_checklist_declares_prior_smokes(self):
        self.assertIn("powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v09_tesseract_dashboard.ps1", REQUIRED_SMOKES)
        self.assertIn("powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v1_0_release_lock.ps1", REQUIRED_SMOKES)


if __name__ == "__main__":
    unittest.main()