import tempfile
import unittest
from pathlib import Path

from cik.release.bundle import build_release_bundle
from cik.release.writer import write_release_outputs


class TestV10ReleaseBundle(unittest.TestCase):
    def _seed_docs(self, root: Path):
        required = [
            "README.md",
            "docs/context/repository_context_index.json",
            "docs/architecture/rcc_context_map.md",
            "docs/protocols/rootmirror_full_contract.md",
            "docs/protocols/instrument_plugin_contract.md",
            "docs/protocols/orchestration_contract.md",
            "docs/protocols/evidence_graph_contract.md",
            "docs/protocols/tesseract_full_contract.md",
            "docs/protocols/dashboard_contract.md",
            "docs/release/release_notes_v1_0.md",
            "docs/release/release_checklist_v1_0.md",
            "docs/release/local_install_v1_0.md",
            "docs/release/validation_surface_v1_0.md",
            "docs/release/non_claim_locks_v1_0.md",
            "docs/release/output_contract_v1_0.md",
        ]
        for rel in required:
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("ok", encoding="utf-8")

    def test_release_bundle_builds(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "outputs"
            out.mkdir()
            self._seed_docs(root)
            bundle = build_release_bundle(root, out)
            self.assertEqual(bundle["schema"], "CIK-v1.0-release-bundle")
            self.assertEqual(bundle["version"], "1.0")
            self.assertTrue(bundle["non_claim_locks"]["stable_release_is_not_truth"])

    def test_release_outputs_emit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "outputs"
            out.mkdir()
            self._seed_docs(root)
            bundle = build_release_bundle(root, out)
            paths = write_release_outputs(bundle, out)
            self.assertTrue(Path(paths["release_bundle"]).exists())
            self.assertTrue(Path(paths["release_summary"]).exists())
            self.assertTrue(Path(paths["release_checklist"]).exists())
            self.assertTrue(Path(paths["validation_surface"]).exists())
            self.assertTrue(Path(paths["non_claim_locks"]).exists())


if __name__ == "__main__":
    unittest.main()