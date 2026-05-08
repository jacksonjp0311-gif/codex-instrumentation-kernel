import unittest
from pathlib import Path

from cik.instruments.rcc_drift.reference_loader import load_reference
from cik.instruments.rcc_drift.drift_metrics import compute_drift


class TestRCCDriftMetrics(unittest.TestCase):
    def test_fixture_low_drift(self):
        repo = Path(__file__).parent / "fixtures" / "tiny_repo_with_context"
        ref = load_reference(repo)
        drift = compute_drift(repo, ref)
        self.assertEqual(drift["dphi_global"], 0.0)

    def test_missing_context_no_crash(self):
        repo = Path(__file__).parent / "fixtures" / "tiny_repo"
        ref = load_reference(repo)
        drift = compute_drift(repo, ref)
        self.assertIn("dphi_global", drift)


if __name__ == "__main__":
    unittest.main()