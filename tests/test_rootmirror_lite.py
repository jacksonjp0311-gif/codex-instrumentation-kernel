import json
import tempfile
import unittest
from pathlib import Path

from cik.rootmirror import (
    line_count,
    sha256_file,
    verify_artifacts,
    rootmirror_lite_verify,
    write_rootmirror_outputs,
    inject_rootmirror_into_state,
    inject_rootmirror_into_evidence,
)


class TestRootMirrorLite(unittest.TestCase):
    def test_hash_and_line_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "state.json"
            p.write_text('{"ok": true}', encoding="utf-8")
            self.assertEqual(len(sha256_file(p)), 64)

            ledger = Path(tmp) / "ledger.jsonl"
            self.assertEqual(line_count(ledger), 0)
            ledger.write_text("a\nb\n", encoding="utf-8")
            self.assertEqual(line_count(ledger), 2)

    def test_verify_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = {}
            for name in ["state", "ledger", "evidence", "report", "semantic"]:
                p = root / f"{name}.txt"
                p.write_text(name, encoding="utf-8")
                artifacts[name] = str(p)

            result = verify_artifacts(artifacts)
            self.assertTrue(result["artifact_manifest_ok"])
            self.assertEqual(result["artifact_emission_score"], 1.0)

    def test_rootmirror_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.json"
            ledger = root / "ledger.jsonl"
            evidence = root / "evidence.json"
            report = root / "report.md"
            semantic = root / "semantic.md"

            state.write_text('{"status":"ok"}', encoding="utf-8")
            ledger.write_text("old\nnew\n", encoding="utf-8")
            evidence.write_text('{"evidence":true}', encoding="utf-8")
            report.write_text("# report", encoding="utf-8")
            semantic.write_text("# semantic", encoding="utf-8")

            run_result = {
                "run_id": "test_run",
                "instrument": "rcc-drift",
                "artifacts": {
                    "state": str(state),
                    "ledger": str(ledger),
                    "evidence": str(evidence),
                    "report": str(report),
                    "semantic": str(semantic),
                },
            }

            result = rootmirror_lite_verify(
                repo_root=str(root),
                run_result=run_result,
                ledger_count_before=1,
                cwd_pre=str(Path.cwd().resolve()),
            )

            self.assertEqual(result["rootmirror_lite"]["status"], "pass")
            self.assertEqual(result["ledger_verification"]["append_delta"], 1)
            self.assertTrue(result["state_hash"]["computed"])

    def test_rootmirror_fails_missing_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.json"
            ledger = root / "ledger.jsonl"
            state.write_text('{"status":"ok"}', encoding="utf-8")
            ledger.write_text("old\nnew\n", encoding="utf-8")

            run_result = {
                "run_id": "bad_run",
                "instrument": "rcc-drift",
                "artifacts": {
                    "state": str(state),
                    "ledger": str(ledger),
                    "evidence": "",
                    "report": "",
                    "semantic": "",
                },
            }

            result = rootmirror_lite_verify(
                repo_root=str(root),
                run_result=run_result,
                ledger_count_before=1,
                cwd_pre=str(Path.cwd().resolve()),
            )

            self.assertNotEqual(result["rootmirror_lite"]["status"], "pass")
            self.assertFalse(result["artifact_manifest"]["artifact_manifest_ok"])

    def test_write_outputs_and_inject(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / "state.json"
            evidence = root / "evidence.json"
            state.write_text('{"status":"ok"}', encoding="utf-8")
            evidence.write_text('{"status":"ok"}', encoding="utf-8")

            result = {
                "run_id": "inject_run",
                "instrument": "rcc-drift",
                "repo_root": str(root),
                "root_anchor": {"return_to_root_ok": True},
                "artifact_manifest": {"required": {}, "artifact_manifest_ok": True},
                "state_hash": {"algorithm": "sha256", "state_path": str(state), "computed": True, "sha256": "abc"},
                "ledger_verification": {"append_once_ok": True},
                "rootmirror_lite": {
                    "score": 1.0,
                    "status": "pass",
                    "checks": {
                        "root_anchor_ok": True,
                        "artifact_manifest_ok": True,
                        "state_hash_ok": True,
                        "ledger_append_once_ok": True,
                        "return_to_root_ok": True,
                    },
                },
            }

            paths = write_rootmirror_outputs(result, str(root), "inject_run")
            self.assertTrue(Path(paths["rootmirror_json"]).exists())
            self.assertTrue(Path(paths["rootmirror_markdown"]).exists())

            inject_rootmirror_into_state(str(state), result, paths)
            inject_rootmirror_into_evidence(str(evidence), result, paths)

            state_data = json.loads(state.read_text(encoding="utf-8"))
            evidence_data = json.loads(evidence.read_text(encoding="utf-8"))

            self.assertIn("rootmirror_lite", state_data)
            self.assertIn("continuity_evidence", evidence_data)


if __name__ == "__main__":
    unittest.main()