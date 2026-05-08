import json
import tempfile
import unittest
from pathlib import Path

from cik.evidence_graph.builder import build_evidence_graph
from cik.evidence_graph.queries import query_graph


class TestV08GraphQueries(unittest.TestCase):
    def _graph(self):
        td = tempfile.TemporaryDirectory()
        out = Path(td.name)
        (out / "state").mkdir(parents=True)
        (out / "evidence").mkdir(parents=True)

        (out / "state" / "run_q_state.json").write_text(json.dumps({
            "run_id": "run_q",
            "instrument": "rcc-drift",
            "downgrade_reason": ["Tesseract indexing not enabled."],
            "non_claim_locks": {"cifscore_is_not_truth": True}
        }), encoding="utf-8")

        (out / "evidence" / "run_q_evidence_package.json").write_text(json.dumps({
            "run_id": "run_q",
            "instrument": "rcc-drift",
            "claim_boundary": "instrumentation_only",
            "non_claim_locks": {"orchestration_is_not_correctness": True}
        }), encoding="utf-8")

        return td, build_evidence_graph(out)

    def test_query_runs(self):
        td, graph = self._graph()
        try:
            result = query_graph(graph, "runs")
            self.assertEqual(result["status"], "found")
            self.assertEqual(result["count"], 1)
        finally:
            td.cleanup()

    def test_query_artifacts_for_run(self):
        td, graph = self._graph()
        try:
            result = query_graph(graph, "artifacts-for-run", run_id="run_q")
            self.assertEqual(result["status"], "found")
            self.assertGreaterEqual(result["count"], 1)
        finally:
            td.cleanup()

    def test_query_evidence_for_run(self):
        td, graph = self._graph()
        try:
            result = query_graph(graph, "evidence-for-run", run_id="run_q")
            self.assertEqual(result["status"], "found")
            self.assertGreaterEqual(result["count"], 1)
        finally:
            td.cleanup()

    def test_query_orphan_artifacts(self):
        td, graph = self._graph()
        try:
            result = query_graph(graph, "orphan-artifacts")
            self.assertIn(result["status"], {"found", "none"})
            self.assertTrue(result["non_claim_locks"]["queryability_is_not_correctness"])
        finally:
            td.cleanup()


if __name__ == "__main__":
    unittest.main()