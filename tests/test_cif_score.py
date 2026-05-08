import unittest

from cik.core.scoring import cif_score
from cik.core.metrics import omega_from_dphi


class TestCIFScore(unittest.TestCase):
    def test_omega(self):
        self.assertAlmostEqual(omega_from_dphi(0.0), 1.0)
        self.assertAlmostEqual(omega_from_dphi(1.0), 0.5)

    def test_default_cif_score(self):
        score = cif_score()
        self.assertGreater(score, 0.5)
        self.assertLess(score, 1.0)


if __name__ == "__main__":
    unittest.main()