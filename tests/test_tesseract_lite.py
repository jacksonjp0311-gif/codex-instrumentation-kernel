import json
import tempfile
import unittest
from pathlib import Path

from cik.tesseract.index import (
    discover_artifacts,
    extract_run_id,
    infer_artifact_type,
    sha256_file,
    write_tesseract_index,
)


class TestTesseractLite(unittest.TestCase):
    def test_infer_artifact_types(self):
        self.assertEqual(infer_artifact_type(Path("outputs/state/run_state.json")), "state")
        self.assertEqual(infer_artifact_type(Path("outputs/ledger/cik_ledger.jsonl")), "ledger")
        self.assertEqual(infer_artifact_type(Path("outputs/evidence/run_evidence_package.json")), "evidence")
        self.assertEqual(infer_artifact_type(Path("outputs/rootmirror/run_rootmirror_lite.json")), "rootmirror")
        self.assertEqual(infer_artifact_type(Path("outputs/perturbation/run_perturbation_sweep.json")), "perturbation")

    def test_extract_run_id(self):
        self.assertEqual(extract_run_id(Path("abc_state.json")), "abc")
        self.assertEqual(extract_run_id(Path("abc_rootmirror_lite.json")), "abc")
        self.assertEqual(extract_run_id(Path("abc_perturbation_sweep.json")), "abc")
        self.assertEqual(extract_run_id(Path("x.json"), {"run_id": "json_run"}), "json_run")

    def test_hash_and_discover(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "outputs"
            (out / "state").mkdir(parents=True)
            state = out / "state" / "run1_state.json"
            state.write_text(json.dumps({"run_id": "run1", "dphi_global": 0.0, "omega_mean": 1.0}), encoding="utf-8")

            h = sha256_file(state)
            self.assertTrue(h.startswith("sha256:"))

            artifacts = discover_artifacts(out)
            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0].artifact_type, "state")
            self.assertEqual(artifacts[0].run_id, "run1")
            self.assertTrue(artifacts[0].sha256.startswith("sha256:"))

    def test_write_tesseract_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "outputs"
            (out / "state").mkdir(parents=True)
            (out / "evidence").mkdir(parents=True)
            (out / "reports").mkdir(parents=True)

            run_id = "cik_test_run"
            (out / "state" / f"{run_id}_state.json").write_text(
                json.dumps({
                    "run_id": run_id,
                    "instrument": "rcc-drift",
                    "dphi_global": 0.0,
                    "omega_mean": 1.0,
                    "cif_score": 0.7142857142857143,
                    "maturity": "CIF6-ready",
                    "classification": "CIF-B",
                    "downgrade_reason": [
                        "Tesseract indexing not enabled.",
                        "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
                    ],
                    "non_claim_locks": {
                        "coherence_is_not_truth": True
                    }
                }),
                encoding="utf-8",
            )
            (out / "evidence" / f"{run_id}_evidence_package.json").write_text(
                json.dumps({"run_id": run_id, "status": "ok"}),
                encoding="utf-8",
            )
            (out / "reports" / f"{run_id}_drift_report.md").write_text("# Report\n", encoding="utf-8")

            index = write_tesseract_index(out)

            self.assertEqual(index["schema"], "CIK-v0.4-tesseract-lite-index")
            self.assertEqual(index["index_integrity_score"], 1.0)
            self.assertEqual(index["maturity"], "CIF7-ready")
            self.assertEqual(index["classification"], "CIF-B")
            self.assertTrue((out / "tesseract" / "tesseract_lite_index.json").exists())
            self.assertTrue((out / "tesseract" / "tesseract_lite_index.md").exists())
            self.assertTrue((out / "tesseract" / "tesseract_lite_evidence_package.json").exists())
            self.assertTrue(index["non_claim_locks"]["tesseract_lite_is_not_memory_agency"])
            self.assertTrue(index["non_claim_locks"]["artifact_indexing_is_not_truth"])


if __name__ == "__main__":
    unittest.main()