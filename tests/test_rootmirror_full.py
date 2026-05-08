import json
import os
import tempfile
import unittest
from pathlib import Path

from cik.rootmirror_full.anchors import capture_anchor
from cik.rootmirror_full.manifest import discover_expected_artifacts, hash_artifacts, output_root_hash_surface
from cik.rootmirror_full.verifier import verify_rootmirror_full
from cik.rootmirror_full.writer import write_rootmirror_full_outputs


class TestRootMirrorFull(unittest.TestCase):
    def test_manifest_hash_and_output_hash_surface(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "outputs"
            run_id = "cik_rcc_drift_test"

            for folder in ["state", "evidence", "reports", "semantic", "ledger"]:
                (out / folder).mkdir(parents=True, exist_ok=True)

            (out / "state" / f"{run_id}_state.json").write_text("{}", encoding="utf-8")
            (out / "evidence" / f"{run_id}_evidence_package.json").write_text("{}", encoding="utf-8")
            (out / "reports" / f"{run_id}_drift_report.md").write_text("# report", encoding="utf-8")
            (out / "semantic" / f"{run_id}_summary.md").write_text("# semantic", encoding="utf-8")
            (out / "ledger" / "cik_ledger.jsonl").write_text('{"run_id":"x"}\n', encoding="utf-8")

            artifacts = discover_expected_artifacts(out, run_id)
            hashes = hash_artifacts(artifacts)

            self.assertIn("state", artifacts)
            self.assertIn("ledger", artifacts)
            self.assertIn("state", hashes)
            self.assertTrue(output_root_hash_surface(out).startswith("sha256:"))

    def test_verify_full_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            out = root / "outputs"
            run_id = "cik_rcc_drift_test"

            for folder in ["state", "evidence", "reports", "semantic", "ledger", "tesseract"]:
                (out / folder).mkdir(parents=True, exist_ok=True)

            ledger = out / "ledger" / "cik_ledger.jsonl"
            ledger.write_text("", encoding="utf-8")

            old = Path.cwd()
            os.chdir(root)
            try:
                pre = capture_anchor(root, ledger)

                (out / "state" / f"{run_id}_state.json").write_text("{}", encoding="utf-8")
                (out / "evidence" / f"{run_id}_evidence_package.json").write_text("{}", encoding="utf-8")
                (out / "reports" / f"{run_id}_drift_report.md").write_text("# report", encoding="utf-8")
                (out / "semantic" / f"{run_id}_summary.md").write_text("# semantic", encoding="utf-8")
                (out / "tesseract" / "tesseract_lite_index.json").write_text("{}", encoding="utf-8")
                ledger.write_text('{"run_id":"cik_rcc_drift_test"}\n', encoding="utf-8")

                result = verify_rootmirror_full(
                    repo_root=root,
                    output_root=out,
                    run_id=run_id,
                    instrument="rcc-drift",
                    command="test command",
                    pre_anchor=pre,
                )

                self.assertEqual(result.status, "pass")
                self.assertEqual(result.continuity_integrity_score, 1.0)
                self.assertTrue(result.checks["return_to_root"])
                self.assertTrue(result.checks["ledger_append_valid"])
                self.assertTrue(result.checks["artifact_manifest_closure"])
                self.assertTrue(result.downgrade_removed)

                paths = write_rootmirror_full_outputs(result, out)
                self.assertTrue(Path(paths["rootmirror_full_json"]).exists())
                self.assertTrue(Path(paths["rootmirror_full_markdown"]).exists())
                self.assertTrue(Path(paths["rootmirror_full_evidence"]).exists())

                payload = json.loads(Path(paths["rootmirror_full_json"]).read_text(encoding="utf-8"))
                self.assertEqual(payload["schema"], "CIK-v0.5-rootmirror-full")
            finally:
                os.chdir(old)

    def test_verify_full_warns_when_artifact_missing(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            out = root / "outputs"
            run_id = "cik_rcc_drift_test"

            for folder in ["state", "ledger"]:
                (out / folder).mkdir(parents=True, exist_ok=True)

            ledger = out / "ledger" / "cik_ledger.jsonl"
            ledger.write_text("", encoding="utf-8")

            old = Path.cwd()
            os.chdir(root)
            try:
                pre = capture_anchor(root, ledger)
                (out / "state" / f"{run_id}_state.json").write_text("{}", encoding="utf-8")
                ledger.write_text('{"run_id":"cik_rcc_drift_test"}\n', encoding="utf-8")

                result = verify_rootmirror_full(
                    repo_root=root,
                    output_root=out,
                    run_id=run_id,
                    instrument="rcc-drift",
                    command="test command",
                    pre_anchor=pre,
                )

                self.assertEqual(result.status, "warning")
                self.assertLess(result.continuity_integrity_score, 1.0)
                self.assertIn("Full RootMirror verification incomplete.", result.remaining_downgrade_reason)
            finally:
                os.chdir(old)


if __name__ == "__main__":
    unittest.main()