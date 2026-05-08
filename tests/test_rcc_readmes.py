import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ROOT_SECTIONS = [
    "# Codex",
    "PART I",
    "PART II",
    "AI operating contract",
    "RCC documentation contract",
    "AI non-claim lock",
    "Required local verification",
]

MINI_README_SECTIONS = [
    "## Purpose",
    "## S",
    "## H",
    "## A",
    "## T",
    "## I",
    "## E",
]

REQUIRED_MINI_README_DIRS = [
    "configs",
    "configs/instruments",
    "configs/rcc",
    "configs/injection",
    "docs",
    "docs/architecture",
    "docs/context",
    "docs/protocols",
    "docs/theory",
    "examples",
    "outputs",
    "outputs/state",
    "outputs/ledger",
    "outputs/evidence",
    "outputs/reports",
    "outputs/semantic",
    "outputs/visuals",
    "outputs/injection",
    "scripts",
    "src",
    "src/cik",
    "src/cik/core",
    "src/cik/instruments",
    "src/cik/instruments/rcc_drift",
    "src/cik/artifacts",
    "src/cik/evidence",
    "src/cik/injection",
    "src/cik/rcc",
    "src/cik/schemas",
    "src/cik/utils",
    "tests",
    "tests/fixtures",
    "tests/fixtures/tiny_repo",
    "tests/fixtures/tiny_repo_with_context",
]


class TestRCCReadmes(unittest.TestCase):
    def test_root_readme_exists_and_has_human_ai_structure(self):
        path = ROOT / "README.md"
        self.assertTrue(path.exists(), "Missing root README.md")
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_ROOT_SECTIONS:
            self.assertIn(section, text)

    def test_rcc_context_index_exists(self):
        path = ROOT / "docs" / "context" / "repository_context_index.json"
        self.assertTrue(path.exists(), "Missing docs/context/repository_context_index.json")

    def test_rcc_context_map_exists(self):
        path = ROOT / "docs" / "architecture" / "rcc_context_map.md"
        self.assertTrue(path.exists(), "Missing docs/architecture/rcc_context_map.md")

    def test_required_mini_readmes_exist_and_have_sections(self):
        missing = []
        bad = []
        for rel in REQUIRED_MINI_README_DIRS:
            path = ROOT / rel / "README.md"
            if not path.exists():
                missing.append(rel)
                continue
            text = path.read_text(encoding="utf-8")
            for section in MINI_README_SECTIONS:
                if section not in text:
                    bad.append((rel, section))
        self.assertEqual(missing, [], f"Missing mini READMEs: {missing}")
        self.assertEqual(bad, [], f"Mini README missing sections: {bad}")


if __name__ == "__main__":
    unittest.main()