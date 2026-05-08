import unittest

from cik.release.locks import build_non_claim_locks


class TestV10NonClaimLocks(unittest.TestCase):
    def test_required_v10_locks_exist(self):
        locks = build_non_claim_locks()
        self.assertTrue(locks["stable_release_is_not_truth"])
        self.assertTrue(locks["local_validation_is_not_formal_verification"])
        self.assertTrue(locks["release_bundle_is_not_provenance"])
        self.assertTrue(locks["git_cleanliness_is_not_semantic_validity"])
        self.assertTrue(locks["release_notes_are_not_external_validation"])

    def test_prior_locks_preserved(self):
        locks = build_non_claim_locks()
        self.assertTrue(locks["graph_linkage_is_not_truth"])
        self.assertTrue(locks["visualization_is_not_validation"])
        self.assertTrue(locks["tesseract_linkage_is_not_provenance"])


if __name__ == "__main__":
    unittest.main()