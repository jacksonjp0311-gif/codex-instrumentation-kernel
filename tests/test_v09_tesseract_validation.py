import unittest

from cik.tesseract_full.package import PACKAGE_NON_CLAIM_LOCKS
from cik.tesseract_full.views import build_downgrade_timeline_view, build_rootmirror_linkage_view, build_orchestration_linkage_view


class TestV09TesseractValidation(unittest.TestCase):
    def test_package_non_claim_locks(self):
        self.assertTrue(PACKAGE_NON_CLAIM_LOCKS["dashboard_visualization_is_not_truth"])
        self.assertTrue(PACKAGE_NON_CLAIM_LOCKS["tesseract_linkage_is_not_provenance"])
        self.assertTrue(PACKAGE_NON_CLAIM_LOCKS["release_readiness_is_not_release_proof"])

    def test_downgrade_timeline_discloses_recurrence(self):
        graph = {
            "nodes": [
                {"id": "run1", "type": "run", "run_id": "run_1"},
                {"id": "run2", "type": "run", "run_id": "run_2"},
                {"id": "d1", "type": "downgrade", "label": "missing graph edge"},
            ],
            "edges": [
                {"id": "e1", "type": "has_downgrade", "source": "run1", "target": "d1"},
                {"id": "e2", "type": "has_downgrade", "source": "run2", "target": "d1"},
            ],
        }

        timeline = build_downgrade_timeline_view(graph)

        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0]["status"], "recurring")
        self.assertTrue(timeline[0]["non_claim_locks"]["downgrade_timeline_is_not_resolution"])

    def test_linkage_views_exist(self):
        graph = {
            "nodes": [
                {"id": "run1", "type": "run", "run_id": "run_1"},
                {"id": "rm1", "type": "rootmirror", "path": "rootmirror.json"},
                {"id": "orch1", "type": "orchestration", "path": "orch.json"},
            ],
            "edges": [
                {"id": "e1", "type": "verified_by", "source": "run1", "target": "rm1", "status": "artifact_backed"},
                {"id": "e2", "type": "composed_from", "source": "run1", "target": "orch1", "status": "artifact_backed"},
            ],
        }

        rootmirror = build_rootmirror_linkage_view(graph)
        orchestration = build_orchestration_linkage_view(graph)

        self.assertEqual(len(rootmirror), 1)
        self.assertEqual(len(orchestration), 1)
        self.assertTrue(rootmirror[0]["non_claim_locks"]["rootmirror_linkage_is_not_code_correctness"])
        self.assertTrue(orchestration[0]["non_claim_locks"]["orchestration_linkage_is_not_correctness"])


if __name__ == "__main__":
    unittest.main()