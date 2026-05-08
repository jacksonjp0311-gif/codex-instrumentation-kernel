import unittest

from cik.tesseract_full.views import (
    build_run_family_view,
    build_instrument_health_view,
    build_evidence_maturity_view,
    build_claim_boundary_view,
)


class TestV09DashboardViews(unittest.TestCase):
    def _graph(self):
        return {
            "nodes": [
                {"id": "run1", "type": "run", "run_id": "run_1", "instrument": "rcc-drift", "label": "run_1"},
                {"id": "inst1", "type": "instrument", "instrument": "rcc-drift", "label": "rcc-drift"},
                {"id": "ev1", "type": "evidence", "path": "evidence.json", "label": "evidence.json"},
                {"id": "claim1", "type": "claim", "label": "orchestration_is_not_correctness"},
            ],
            "edges": [
                {"id": "e1", "type": "used_instrument", "source": "run1", "target": "inst1", "status": "artifact_backed"},
                {"id": "e2", "type": "has_evidence", "source": "run1", "target": "ev1", "status": "artifact_backed"},
                {"id": "e3", "type": "declares_boundary", "source": "run1", "target": "claim1", "status": "artifact_backed", "support": "state.json"},
            ],
        }

    def test_run_family_view_exists(self):
        view = build_run_family_view(self._graph())
        self.assertEqual(len(view), 1)
        self.assertEqual(view[0]["instrument"], "rcc-drift")
        self.assertTrue(view[0]["non_claim_locks"]["visual_summary_is_not_validation"])

    def test_instrument_health_view_exists(self):
        view = build_instrument_health_view(self._graph())
        self.assertEqual(len(view), 1)
        self.assertEqual(view[0]["instrument"], "rcc-drift")
        self.assertTrue(view[0]["non_claim_locks"]["instrument_health_is_not_correctness"])

    def test_evidence_maturity_view_exists(self):
        view = build_evidence_maturity_view(self._graph())
        self.assertEqual(len(view), 1)
        self.assertEqual(view[0]["classification"], "CIF-B")
        self.assertTrue(view[0]["non_claim_locks"]["dashboard_maturity_does_not_promote_maturity"])

    def test_claim_boundary_view_exists(self):
        view = build_claim_boundary_view(self._graph())
        self.assertEqual(len(view), 1)
        self.assertEqual(view[0]["claim"], "orchestration_is_not_correctness")
        self.assertTrue(view[0]["non_claim_locks"]["claim_panel_is_not_truth"])


if __name__ == "__main__":
    unittest.main()