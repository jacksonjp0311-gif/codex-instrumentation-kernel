import os
import sys
import tempfile
import unittest
from pathlib import Path

from cik.rootmirror_full.integration import run_rootmirror_full_command


class TestRootMirrorFullIntegration(unittest.TestCase):
    def test_run_rootmirror_full_command_with_fake_command(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            out = root / "outputs"
            run_id = "cik_rcc_drift_fake"

            script = root / "fake_run.py"
            script.write_text(
                "\n".join([
                    "from pathlib import Path",
                    "import json",
                    f"run_id = '{run_id}'",
                    "out = Path('outputs')",
                    "for folder in ['state','evidence','reports','semantic','ledger','tesseract']:",
                    "    (out / folder).mkdir(parents=True, exist_ok=True)",
                    "(out / 'state' / f'{run_id}_state.json').write_text(json.dumps({'run_id': run_id}), encoding='utf-8')",
                    "(out / 'evidence' / f'{run_id}_evidence_package.json').write_text('{}', encoding='utf-8')",
                    "(out / 'reports' / f'{run_id}_drift_report.md').write_text('# report', encoding='utf-8')",
                    "(out / 'semantic' / f'{run_id}_summary.md').write_text('# semantic', encoding='utf-8')",
                    "(out / 'tesseract' / 'tesseract_lite_index.json').write_text('{}', encoding='utf-8')",
                    "(out / 'ledger' / 'cik_ledger.jsonl').write_text(json.dumps({'run_id': run_id}) + '\\n', encoding='utf-8')",
                ]),
                encoding="utf-8",
            )

            old = Path.cwd()
            os.chdir(root)
            try:
                payload = run_rootmirror_full_command(
                    repo_root=root,
                    output_root=out,
                    command=[sys.executable, str(script)],
                    instrument="rcc-drift",
                    run_tesseract=False,
                )

                result = payload["result"]
                self.assertEqual(payload["command_returncode"], 0)
                self.assertEqual(result.status, "pass")
                self.assertEqual(result.run_id, run_id)
                self.assertTrue(Path(payload["rootmirror_full"]["rootmirror_full_json"]).exists())
                self.assertTrue(Path(payload["rootmirror_full"]["rootmirror_full_evidence"]).exists())
            finally:
                os.chdir(old)


if __name__ == "__main__":
    unittest.main()