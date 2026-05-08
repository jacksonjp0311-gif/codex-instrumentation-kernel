import json
import tempfile
import unittest
from pathlib import Path

from cik.perturbation import (
    SweepMeasurement,
    SweepTolerances,
    apply_missing_path_perturbation,
    evaluate_sweep,
    measure_repository_context,
    run_perturbation_sweep,
)


def make_fixture(root: Path) -> Path:
    repo = root / "fixture"
    (repo / "docs" / "context").mkdir(parents=True)
    (repo / "README.md").write_text("# Fixture\n", encoding="utf-8")
    (repo / "docs" / "context" / "repository_context_index.json").write_text(
        json.dumps(
            {
                "schema": "test-context",
                "repository": {
                    "name": "fixture"
                },
                "declared_paths": [
                    "README.md",
                    "docs/context/repository_context_index.json"
                ],
                "non_claim_locks": {
                    "context_is_not_correctness": True
                }
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return repo


class TestPerturbationSweep(unittest.TestCase):
    def test_measurement_baseline_is_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_fixture(Path(tmp))
            m = measure_repository_context(repo, "baseline")
            self.assertEqual(m["missing_path_count"], 0)
            self.assertEqual(m["dphi_global"], 0.0)
            self.assertEqual(m["omega_mean"], 1.0)

    def test_missing_path_perturbation_raises_dphi(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_fixture(Path(tmp))
            baseline = measure_repository_context(repo, "baseline")
            apply_missing_path_perturbation(repo)
            perturbed = measure_repository_context(repo, "perturbed")

            self.assertGreater(perturbed["dphi_global"], baseline["dphi_global"])
            self.assertLess(perturbed["omega_mean"], baseline["omega_mean"])

    def test_evaluate_sweep_passes_on_rise_fall_recovery(self):
        baseline = SweepMeasurement("baseline", "b", 0.0, 1.0)
        perturbed = SweepMeasurement("perturbed", "p", 0.25, 0.8)
        restored = SweepMeasurement("restored", "r", 0.0, 1.0)

        result = evaluate_sweep(
            baseline,
            perturbed,
            restored,
            SweepTolerances(),
            evidence_complete=True,
        )

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["perturbation_score"], 1.0)
        self.assertTrue(result["response_checks"]["dphi_rises_under_perturbation"])
        self.assertTrue(result["response_checks"]["omega_falls_under_perturbation"])

    def test_run_perturbation_sweep_emits_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = make_fixture(root)
            out = root / "outputs"

            result = run_perturbation_sweep(repo, out, operator="missing_path")

            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["perturbation_score"], 1.0)
            self.assertTrue(Path(result["artifacts"]["sweep_json"]).exists())
            self.assertTrue(Path(result["artifacts"]["sweep_report"]).exists())
            self.assertTrue(Path(result["artifacts"]["evidence"]).exists())

            m = result["measurements"]
            self.assertGreater(m["perturbed"]["dphi_global"], m["baseline"]["dphi_global"])
            self.assertLess(m["perturbed"]["omega_mean"], m["baseline"]["omega_mean"])
            self.assertEqual(m["restored"]["dphi_global"], m["baseline"]["dphi_global"])
            self.assertEqual(m["restored"]["omega_mean"], m["baseline"]["omega_mean"])


if __name__ == "__main__":
    unittest.main()