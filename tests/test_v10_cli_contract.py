import unittest

from cik.release.validator import STABLE_CLI_COMMANDS


class TestV10CliContract(unittest.TestCase):
    def test_cli_contract_preserves_prior_layers(self):
        joined = "\n".join(STABLE_CLI_COMMANDS)
        self.assertIn("python -m cik.evidence_graph build", joined)
        self.assertIn("python -m cik.tesseract_full build", joined)
        self.assertIn("python -m cik.release lock", joined)

    def test_cli_contract_is_non_empty(self):
        self.assertGreaterEqual(len(STABLE_CLI_COMMANDS), 10)


if __name__ == "__main__":
    unittest.main()