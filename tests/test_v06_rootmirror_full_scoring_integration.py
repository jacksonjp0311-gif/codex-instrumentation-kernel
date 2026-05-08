import json
import tempfile
import unittest
from pathlib import Path

from cik.core.rootmirror_full_consumer import consume_rootmirror_full_evidence
from cik.core.scoring_v06 import cif_score_v06, score_from_evidence_bundle
from cik.core.maturity_v06 import classify_maturity_v06


class TestV06RootMirrorFullScoringIntegration(unittest.TestCase):
    def test_consumer_accepts_valid_rootmirror_full_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "outputs"
            evidence = out / "evidence"
            evidence.mkdir(parents=True)

            path = evidence / "run123_rootmirror_full_evidence_package.json"
            path.write_text(json.dumps({
                "schema": "CIK-v0.5-rootmirror-full-evidence",
                "run_id": "run123",
                "status": "pass",
                "continuity_integrity_score": 1.0,
                "claim_boundary": "continuity_verification_only",
                "checks": {},
                "non_claim_locks": {
                    "rootmirror_full_is_not_code_correctness": True
                }
            }), encoding="utf-8")

            signal = consume_rootmirror_full_evidence(out, run_id="run123")

            self.assertTrue(signal["available"])
            self.assertEqual(signal["status"], "pass")
            self.assertEqual(signal["score"], 1.0)

    def test_consumer_rejects_wrong_claim_boundary(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "outputs"
            evidence = out / "evidence"
            evidence.mkdir(parents=True)

            path = evidence / "run123_rootmirror_full_evidence_package.json"
            path.write_text(json.dumps({
                "schema": "CIK-v0.5-rootmirror-full-evidence",
                "run_id": "run123",
                "status": "pass",
                "continuity_integrity_score": 1.0,
                "claim_boundary": "correctness_claim",
                "checks": {},
                "non_claim_locks": {}
            }), encoding="utf-8")

            signal = consume_rootmirror_full_evidence(out, run_id="run123")

            self.assertTrue(signal["available"])
            self.assertEqual(signal["status"], "warning")
            self.assertEqual(signal["score"], 0.0)

    def test_consumer_missing_evidence_returns_zero(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "outputs"
            signal = consume_rootmirror_full_evidence(out)

            self.assertFalse(signal["available"])
            self.assertEqual(signal["score"], 0.0)
            self.assertEqual(signal["status"], "missing")

    def test_cif_score_v06_includes_rootmirror_full_score(self):
        low = cif_score_v06(1, 1, 1, 1, 0, 1, 1)
        high = cif_score_v06(1, 1, 1, 1, 1, 1, 1)

        self.assertLess(low, high)
        self.assertEqual(high, 1.0)

    def test_score_from_evidence_bundle_has_non_claim_locks(self):
        result = score_from_evidence_bundle({
            "dphi_declared": 1,
            "omega_declared": 1,
            "perturbation_score": 1,
            "artifact_score": 1,
            "rootmirror_full_score": 1,
            "falsification_score": 1,
            "tesseract_index_score": 1,
        })

        self.assertEqual(result["cif_score"], 1.0)
        self.assertTrue(result["non_claim_locks"]["cifscore_is_not_truth"])

    def test_maturity_consumes_three_evidence_signals_but_preserves_cif_b(self):
        result = classify_maturity_v06(
            perturbation_score=1.0,
            rootmirror_full_score=1.0,
            tesseract_index_score=1.0,
            downgrades=[],
        )

        self.assertEqual(result["maturity"], "CIF7-verified")
        self.assertEqual(result["classification"], "CIF-B")
        self.assertTrue(result["non_claim_locks"]["internal_closure_does_not_create_cif_a"])


if __name__ == "__main__":
    unittest.main()