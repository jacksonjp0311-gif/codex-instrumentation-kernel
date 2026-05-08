import unittest

from cik.orchestration.composer import composed_status, compose_downgrades, compose_instrument_results


class TestV07EvidenceComposition(unittest.TestCase):
    def test_composed_status_pass(self):
        results = [
            {"instrument": "a", "required": True, "status": "pass", "score": 1.0}
        ]

        self.assertEqual(composed_status(results), "pass")

    def test_required_failure_fails_composition(self):
        results = [
            {"instrument": "a", "required": True, "status": "fail", "score": 0.0}
        ]

        self.assertEqual(composed_status(results), "fail")

    def test_optional_skipped_warns(self):
        results = [
            {"instrument": "a", "required": True, "status": "pass", "score": 1.0},
            {"instrument": "b", "required": False, "status": "skipped", "score": 0.0},
        ]

        self.assertEqual(composed_status(results), "warning")

    def test_compose_preserves_records_and_locks(self):
        results = [
            {
                "instrument": "rcc-drift",
                "required": True,
                "status": "pass",
                "score": 1.0,
                "downgrades": [],
            },
            {
                "instrument": "future",
                "required": False,
                "status": "blocked",
                "score": 0.0,
                "downgrades": ["No executor available for instrument."],
            }
        ]

        composed = compose_instrument_results("orch_test", results)

        self.assertEqual(composed["status"], "warning")
        self.assertEqual(len(composed["instrument_records"]), 2)
        self.assertTrue(composed["non_claim_locks"]["composition_is_not_truth"])
        self.assertIn("future: No executor available for instrument.", composed["composed_downgrade_surface"])

    def test_compose_downgrades_prefixes_instrument(self):
        results = [
            {"instrument": "x", "downgrades": ["d1"]},
            {"instrument": "y", "downgrades": ["d2"]},
        ]

        surface = compose_downgrades(results)

        self.assertEqual(surface, ["x: d1", "y: d2"])


if __name__ == "__main__":
    unittest.main()