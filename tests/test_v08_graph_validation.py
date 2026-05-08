import json
import tempfile
import unittest
from pathlib import Path

from cik.evidence_graph.builder import build_evidence_graph
from cik.evidence_graph.validator import validate_graph
from cik.evidence_graph.writer import write_graph_outputs


class TestV08GraphValidation(unittest.TestCase):
    def test_validation_emits_status_and_non_claim_locks(self):
        graph = {
            "nodes": [
                {"id": "node:run:a", "type": "run"},
                {"id": "node:artifact:b", "type": "artifact", "path": "b"},
            ],
            "edges": [
                {
                    "id": "edge:1",
                    "type": "has_artifact",
                    "source": "node:run:a",
                    "target": "node:artifact:b",
                    "status": "artifact_backed",
                }
            ],
        }

        validation = validate_graph(graph)

        self.assertEqual(validation["status"], "pass")
        self.assertTrue(validation["non_claim_locks"]["graph_validation_is_not_correctness"])

    def test_validation_marks_invalid_edge_status_fail(self):
        graph = {
            "nodes": [
                {"id": "node:run:a", "type": "run"},
                {"id": "node:artifact:b", "type": "artifact", "path": "b"},
            ],
            "edges": [
                {
                    "id": "edge:bad",
                    "type": "has_artifact",
                    "source": "node:run:a",
                    "target": "node:artifact:b",
                    "status": "fabricated",
                }
            ],
        }

        validation = validate_graph(graph)

        self.assertEqual(validation["status"], "fail")

    def test_writer_emits_graph_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "state").mkdir(parents=True)
            (out / "state" / "run_w_state.json").write_text(json.dumps({
                "run_id": "run_w",
                "non_claim_locks": {"cifscore_is_not_truth": True}
            }), encoding="utf-8")

            graph = build_evidence_graph(out)
            paths = write_graph_outputs(graph, out)

            self.assertTrue(Path(paths["graph"]).exists())
            self.assertTrue(Path(paths["report"]).exists())
            self.assertTrue(Path(paths["evidence"]).exists())


if __name__ == "__main__":
    unittest.main()