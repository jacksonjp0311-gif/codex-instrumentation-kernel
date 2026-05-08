import unittest

from cik.core.downgrades_v06 import (
    ROOTMIRROR_FULL_DOWNGRADE,
    ROOTMIRROR_GENERIC_DOWNGRADE,
    reconcile_downgrades,
    downgrade_reconciliation_report,
)


class TestV06DowngradeReconciliation(unittest.TestCase):
    def test_removes_rootmirror_downgrade_when_evidence_passes(self):
        before = [
            ROOTMIRROR_FULL_DOWNGRADE,
            "Tesseract indexing not enabled.",
            "No perturbation sweep yet.",
        ]

        after = reconcile_downgrades(before, {"score": 1.0})

        self.assertNotIn(ROOTMIRROR_FULL_DOWNGRADE, after)
        self.assertIn("Tesseract indexing not enabled.", after)
        self.assertIn("No perturbation sweep yet.", after)

    def test_preserves_rootmirror_downgrade_when_evidence_missing(self):
        before = [ROOTMIRROR_FULL_DOWNGRADE]

        after = reconcile_downgrades(before, {"score": 0.0})

        self.assertIn(ROOTMIRROR_FULL_DOWNGRADE, after)

    def test_removes_generic_rootmirror_only_when_passes(self):
        before = [
            ROOTMIRROR_GENERIC_DOWNGRADE,
            "Benchmark evidence missing.",
        ]

        after = reconcile_downgrades(before, {"score": 1.0})

        self.assertNotIn(ROOTMIRROR_GENERIC_DOWNGRADE, after)
        self.assertIn("Benchmark evidence missing.", after)

    def test_report_records_removed_and_preserved(self):
        before = [
            ROOTMIRROR_FULL_DOWNGRADE,
            "Tesseract indexing not enabled.",
        ]
        after = reconcile_downgrades(before, {"score": 1.0})
        report = downgrade_reconciliation_report(before, after, {"score": 1.0})

        self.assertIn(ROOTMIRROR_FULL_DOWNGRADE, report["removed"])
        self.assertIn("Tesseract indexing not enabled.", report["preserved"])
        self.assertTrue(report["non_claim_locks"]["downgrade_reconciliation_is_not_correctness"])


if __name__ == "__main__":
    unittest.main()