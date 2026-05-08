import unittest

from cik.rootmirror_full.verifier import continuity_score


class TestV05FullRootMirrorCoreIntegration(unittest.TestCase):
    def test_continuity_score_full(self):
        checks = {
            "run_envelope_declared": True,
            "return_to_root": True,
            "ledger_append_valid": True,
            "artifact_manifest_closure": True,
            "state_hash_present": True,
            "replay_metadata_present": True,
            "non_claim_locks_preserved": True,
        }
        self.assertEqual(continuity_score(checks), 1.0)

    def test_continuity_score_partial(self):
        checks = {
            "run_envelope_declared": True,
            "return_to_root": True,
            "ledger_append_valid": False,
            "artifact_manifest_closure": True,
            "state_hash_present": True,
            "replay_metadata_present": True,
            "non_claim_locks_preserved": True,
        }
        self.assertLess(continuity_score(checks), 1.0)


if __name__ == "__main__":
    unittest.main()