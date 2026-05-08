import tempfile
import unittest
from pathlib import Path

from cik.release.validator import build_validation_surface, STABLE_CLI_COMMANDS, VALIDATION_COMMANDS


class TestV10ReleaseValidator(unittest.TestCase):
    def test_stable_cli_contract_exists(self):
        self.assertIn('python -m cik.release lock --out ".\\outputs"', STABLE_CLI_COMMANDS)

    def test_validation_surface_contains_required_commands(self):
        self.assertIn("python -m unittest discover -s tests", VALIDATION_COMMANDS)

    def test_validation_surface_emits(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "outputs"
            out.mkdir()
            surface = build_validation_surface(root, out)
            self.assertEqual(surface["schema"], "CIK-v1.0-validation-surface")
            self.assertTrue(surface["non_claim_locks"]["local_validation_is_not_formal_verification"])


if __name__ == "__main__":
    unittest.main()