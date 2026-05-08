import unittest

from cik.tesseract_full.dashboard import build_dashboard_data


class TestV09DashboardNonClaimLocks(unittest.TestCase):
    def test_dashboard_non_claim_locks_survive(self):
        graph = {
            "node_count": 1,
            "edge_count": 0,
            "indexes": {
                "runs": {},
                "artifacts": {},
                "instruments": {},
                "downgrades": {},
                "claims": {},
            },
            "validation": {"status": "pass"},
        }

        views = {
            "run_families": [],
            "instrument_health": [],
            "evidence_maturity": [],
            "downgrade_timeline": [],
            "claim_boundaries": [],
        }

        readiness = {
            "status": "partial",
            "blocking_gaps": [],
            "warnings": [],
            "v1_0_gate": {},
            "non_claim_locks": {
                "release_readiness_is_not_release_proof": True
            },
        }

        dashboard = build_dashboard_data(graph, views, readiness)

        self.assertEqual(dashboard["schema"], "CIK-v0.9-dashboard-data")
        self.assertTrue(dashboard["non_claim_locks"]["dashboard_is_navigation_not_truth"])
        self.assertTrue(dashboard["non_claim_locks"]["visualization_is_not_validation"])


if __name__ == "__main__":
    unittest.main()