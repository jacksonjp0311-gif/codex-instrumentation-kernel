import unittest
from pathlib import Path
import tempfile

from cik.cli import main


class TestCLIRun(unittest.TestCase):
    def test_list_instruments(self):
        self.assertEqual(main(["list-instruments"]), 0)

    def test_run_fixture(self):
        repo = Path(__file__).parent / "fixtures" / "tiny_repo_with_context"
        with tempfile.TemporaryDirectory() as tmp:
            code = main(["run", "--instrument", "rcc-drift", "--repo", str(repo), "--out", tmp])
            self.assertEqual(code, 0)
            self.assertTrue((Path(tmp) / "ledger" / "cik_ledger.jsonl").exists())


if __name__ == "__main__":
    unittest.main()