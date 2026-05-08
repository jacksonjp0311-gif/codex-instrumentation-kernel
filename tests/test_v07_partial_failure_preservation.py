import unittest

from cik.orchestration.composer import compose_instrument_results


class TestV07PartialFailurePreservation(unittest.TestCase):
    def test_failed_instrument_is_preserved(self):
        results = [
            {"instrument": "ok", "required": True, "status": "pass", "score": 1.0, "downgrades": []},
            {"instrument": "bad", "required": False, "status": "fail", "score": 0.0, "downgrades": ["failed"]},
        ]

        composed = compose_instrument_results("orch_partial", results)

        instruments = [r["instrument"] for r in composed["instrument_records"]]
        self.assertIn("bad", instruments)
        self.assertIn("bad: failed", composed["composed_downgrade_surface"])

    def test_skipped_instrument_is_preserved(self):
        results = [
            {"instrument": "skip", "required": False, "status": "skipped", "score": 0.0, "downgrades": ["disabled"]}
        ]

        composed = compose_instrument_results("orch_skip", results)

        self.assertEqual(composed["instrument_records"][0]["status"], "skipped")
        self.assertTrue(composed["non_claim_locks"]["skipped_instruments_must_be_preserved"])

    def test_blocked_instrument_is_preserved(self):
        results = [
            {"instrument": "block", "required": True, "status": "blocked", "score": 0.0, "downgrades": ["blocked"]}
        ]

        composed = compose_instrument_results("orch_block", results)

        self.assertEqual(composed["status"], "fail")
        self.assertEqual(composed["instrument_records"][0]["status"], "blocked")
        self.assertTrue(composed["non_claim_locks"]["blocked_instruments_must_be_preserved"])


if __name__ == "__main__":
    unittest.main()