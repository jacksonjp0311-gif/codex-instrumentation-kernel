import json
import tempfile
import unittest
from pathlib import Path

from cik.evidence_graph.builder import build_evidence_graph
from cik.evidence_graph.queries import query_graph


class TestV08DowngradeHistory(unittest.TestCase):
    def test_downgrade_history_detects_declared_downgrades(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "state").mkdir(parents=True)

            for idx in range(2):
                (out / "state" / f"run_d{idx}_state.json").write_text(json.dumps({
                    "run_id": f"run_d{idx}",
                    "instrument": "rcc-drift",
                    "downgrade_reason": ["No perturbation sweep yet."],
                    "non_claim_locks": {"cifscore_is_not_truth": True}
                }), encoding="utf-8")

            graph = build_evidence_graph(out)
            result = query_graph(graph, "downgrades")

            self.assertEqual(result["status"], "found")
            self.assertEqual(result["count"], 1)
            self.assertEqual(result["downgrades"][0]["status"], "recurring")
            self.assertTrue(result["non_claim_locks"]["downgrade_history_is_not_resolution_proof"])


if __name__ == "__main__":
    unittest.main()