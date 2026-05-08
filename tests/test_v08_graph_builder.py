import json
import tempfile
import unittest
from pathlib import Path

from cik.evidence_graph.builder import build_evidence_graph


class TestV08GraphBuilder(unittest.TestCase):
    def _make_outputs(self, root: Path):
        state = root / "state"
        evidence = root / "evidence"
        rootmirror = root / "rootmirror_full"
        orchestration = root / "orchestration"

        state.mkdir(parents=True)
        evidence.mkdir(parents=True)
        rootmirror.mkdir(parents=True)
        orchestration.mkdir(parents=True)

        (state / "run_a_state.json").write_text(json.dumps({
            "run_id": "run_a",
            "instrument": "rcc-drift",
            "downgrade_reason": ["No perturbation sweep yet."],
            "non_claim_locks": {"cifscore_is_not_truth": True}
        }), encoding="utf-8")

        (evidence / "run_a_evidence_package.json").write_text(json.dumps({
            "schema": "CIK-evidence-package",
            "run_id": "run_a",
            "instrument": "rcc-drift",
            "claim_boundary": "instrumentation_only",
            "non_claim_locks": {"coherence_is_not_truth": True}
        }), encoding="utf-8")

        (rootmirror / "run_a_rootmirror_full.json").write_text(json.dumps({
            "schema": "CIK-rootmirror-full",
            "run_id": "run_a",
            "status": "pass",
            "non_claim_locks": {"rootmirror_full_is_not_code_correctness": True}
        }), encoding="utf-8")

        (orchestration / "orch_1_orchestration_state.json").write_text(json.dumps({
            "schema": "CIK-v0.7-orchestration-state",
            "orchestration_run_id": "orch_1",
            "status": "pass",
            "maturity": "CIF7-orchestration-ready",
            "classification": "CIF-B",
            "composed_downgrade_surface": [],
            "non_claim_locks": {"orchestration_is_not_correctness": True}
        }), encoding="utf-8")

    def test_graph_builds_from_existing_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            self._make_outputs(out)

            graph = build_evidence_graph(out)

            self.assertEqual(graph["schema"], "CIK-v0.8-evidence-graph")
            self.assertGreaterEqual(graph["node_count"], 4)
            self.assertGreaterEqual(graph["edge_count"], 3)
            self.assertTrue(graph["non_claim_locks"]["graph_linkage_is_not_truth"])

    def test_graph_contains_run_artifact_evidence_instrument_nodes(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            self._make_outputs(out)

            graph = build_evidence_graph(out)
            types = {n["type"] for n in graph["nodes"]}

            self.assertIn("run", types)
            self.assertIn("artifact", types)
            self.assertIn("evidence", types)
            self.assertIn("instrument", types)

    def test_graph_links_runs_to_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            self._make_outputs(out)

            graph = build_evidence_graph(out)
            edge_types = {e["type"] for e in graph["edges"]}

            self.assertIn("has_artifact", edge_types)
            self.assertIn("has_evidence", edge_types)
            self.assertIn("verified_by", edge_types)


if __name__ == "__main__":
    unittest.main()