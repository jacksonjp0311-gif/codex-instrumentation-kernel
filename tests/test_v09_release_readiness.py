import json
import tempfile
import unittest
from pathlib import Path

from cik.tesseract_full.readiness import build_release_readiness


class TestV09ReleaseReadiness(unittest.TestCase):
    def test_release_readiness_emits_non_claim_locks(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "outputs"
            out.mkdir(parents=True)
            (out / "evidence_graph").mkdir()
            (out / "evidence_graph" / "evidence_graph.json").write_text("{}", encoding="utf-8")

            graph = {
                "validation": {"status": "pass"},
                "indexes": {},
            }

            views = {
                "run_families": [{"family_id": "f"}],
                "claim_boundaries": [{"claim": "c"}],
            }

            readiness = build_release_readiness(out, graph, views)

            self.assertIn(readiness["status"], {"partial", "ready", "not_ready"})
            self.assertTrue(readiness["non_claim_locks"]["release_readiness_is_not_release_proof"])
            self.assertIn("release_notes", readiness["v1_0_gate"])

    def test_graph_warning_produces_warning(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "outputs"
            out.mkdir(parents=True)
            (out / "evidence_graph").mkdir()
            (out / "evidence_graph" / "evidence_graph.json").write_text("{}", encoding="utf-8")

            graph = {
                "validation": {"status": "warning"},
                "indexes": {},
            }

            views = {
                "run_families": [],
                "claim_boundaries": [],
            }

            readiness = build_release_readiness(out, graph, views)

            self.assertIn("Evidence graph validation status is warning.", readiness["warnings"])


if __name__ == "__main__":
    unittest.main()