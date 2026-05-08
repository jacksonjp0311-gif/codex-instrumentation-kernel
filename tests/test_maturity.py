import unittest

from cik.core.maturity import maturity_from_features
from cik.core.classification import classify_cif


class TestMaturity(unittest.TestCase):
    def test_artifact_maturity(self):
        self.assertEqual(maturity_from_features({"artifact_emitting": True}), "CIF4")

    def test_classification(self):
        self.assertEqual(classify_cif(0.70, "CIF4", ["downgrade"]), "CIF-B")


if __name__ == "__main__":
    unittest.main()