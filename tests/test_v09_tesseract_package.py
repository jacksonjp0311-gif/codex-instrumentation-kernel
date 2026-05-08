import json
import tempfile
import unittest
from pathlib import Path

from cik.tesseract_full.package import build_tesseract_package
from cik.tesseract_full.writer import write_tesseract_outputs


class TestV09TesseractPackage(unittest.TestCase):
    def _make_graph(self, out: Path):
        graph_dir = out / "evidence_graph"
        graph_dir.mkdir(parents=True)

        graph = {
            "schema": "CIK-v0.8-evidence-graph",
            "version": "0.8",
            "node_count": 4,
            "edge_count": 3,
            "nodes": [
                {
                    "id": "node:run:run_a",
                    "type": "run",
                    "label": "run_a",
                    "run_id": "run_a",
                    "instrument": "rcc-drift",
                    "path": None,
                },
                {
                    "id": "node:instrument:rcc-drift",
                    "type": "instrument",
                    "label": "rcc-drift",
                    "instrument": "rcc-drift",
                    "path": None,
                },
                {
                    "id": "node:evidence:e1",
                    "type": "evidence",
                    "label": "run_a_evidence_package.json",
                    "run_id": "run_a",
                    "instrument": "rcc-drift",
                    "path": str(out / "evidence" / "run_a_evidence_package.json"),
                },
                {
                    "id": "node:claim:composition",
                    "type": "claim",
                    "label": "composition_is_not_truth",
                    "path": None,
                },
            ],
            "edges": [
                {
                    "id": "edge:1",
                    "type": "used_instrument",
                    "source": "node:run:run_a",
                    "target": "node:instrument:rcc-drift",
                    "status": "artifact_backed",
                    "support": "test",
                },
                {
                    "id": "edge:2",
                    "type": "has_evidence",
                    "source": "node:run:run_a",
                    "target": "node:evidence:e1",
                    "status": "artifact_backed",
                    "support": "test",
                },
                {
                    "id": "edge:3",
                    "type": "declares_boundary",
                    "source": "node:run:run_a",
                    "target": "node:claim:composition",
                    "status": "artifact_backed",
                    "support": "test",
                },
            ],
            "indexes": {
                "runs": {"run_a": "node:run:run_a"},
                "artifacts": {},
                "instruments": {"rcc-drift": "node:instrument:rcc-drift"},
                "downgrades": {},
                "claims": {"composition_is_not_truth": "node:claim:composition"},
            },
            "validation": {
                "status": "pass",
                "missing_edges": [],
                "inferred_edges": [],
                "ambiguous_edges": [],
                "orphan_artifacts": [],
            },
            "non_claim_locks": {
                "graph_linkage_is_not_truth": True
            },
        }

        (graph_dir / "evidence_graph.json").write_text(json.dumps(graph), encoding="utf-8")

    def test_tesseract_package_builds_from_evidence_graph(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            self._make_graph(out)

            bundle = build_tesseract_package(out)

            self.assertEqual(bundle["package"]["schema"], "CIK-v0.9-tesseract-full-package")
            self.assertIn("run_families", bundle["package"]["views"])
            self.assertTrue(bundle["package"]["non_claim_locks"]["tesseract_linkage_is_not_provenance"])

    def test_writer_emits_tesseract_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            self._make_graph(out)

            bundle = build_tesseract_package(out)
            paths = write_tesseract_outputs(bundle, out)

            self.assertTrue(Path(paths["tesseract_full_package"]).exists())
            self.assertTrue(Path(paths["tesseract_full_report"]).exists())
            self.assertTrue(Path(paths["dashboard_json"]).exists())
            self.assertTrue(Path(paths["dashboard_report"]).exists())
            self.assertTrue(Path(paths["release_readiness_summary"]).exists())
            self.assertTrue(Path(paths["evidence"]).exists())


if __name__ == "__main__":
    unittest.main()