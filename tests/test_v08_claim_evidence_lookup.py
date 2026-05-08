import json
import tempfile
import unittest
from pathlib import Path

from cik.evidence_graph.builder import build_evidence_graph
from cik.evidence_graph.queries import query_graph


class TestV08ClaimEvidenceLookup(unittest.TestCase):
    def test_claim_evidence_lookup_finds_non_claim_lock(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "orchestration").mkdir(parents=True)

            (out / "orchestration" / "orch_claim_orchestration_state.json").write_text(json.dumps({
                "orchestration_run_id": "orch_claim",
                "status": "pass",
                "non_claim_locks": {
                    "orchestration_is_not_correctness": True,
                    "composition_is_not_truth": True
                }
            }), encoding="utf-8")

            graph = build_evidence_graph(out)
            result = query_graph(
                graph,
                "claim-evidence",
                claim="orchestration_is_not_correctness",
            )

            self.assertEqual(result["status"], "declared")
            self.assertGreaterEqual(result["count"], 1)
            self.assertTrue(result["non_claim_locks"]["claim_lookup_is_not_claim_truth"])

    def test_missing_claim_returns_missing(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "state").mkdir(parents=True)
            (out / "state" / "run_x_state.json").write_text(json.dumps({
                "run_id": "run_x"
            }), encoding="utf-8")

            graph = build_evidence_graph(out)
            result = query_graph(graph, "claim-evidence", claim="not_declared")

            self.assertEqual(result["status"], "missing")


if __name__ == "__main__":
    unittest.main()