import unittest
import sys
import os

# 1. Add the 'src' folder to Python's path so we can import our code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# 2. Import the functions we want to test
from analysis import calculate_spr, get_placement_tiers

class TestSmashAnalysis(unittest.TestCase):

    def setUp(self):
        # Create the tier list once before running tests
        self.tiers = get_placement_tiers()

    def test_spr_neutral(self):
        """Test that meeting expectations results in SPR 0"""
        # Seed 1 (Tier Index 0) -> Placed 1st (Tier Index 0)
        result = calculate_spr(1, 1, self.tiers)
        self.assertEqual(result, 0)

    def test_spr_upset(self):
        """Test that outplacing your seed results in positive SPR"""
        # Seed 17 (Expected 17th) -> Placed 13th (One tier higher)
        # This should be SPR +1
        result = calculate_spr(17, 13, self.tiers)
        self.assertEqual(result, 1)

    def test_spr_underperformance(self):
        """Test that doing worse than seed results in negative SPR"""
        # Seed 1 (Expected 1st) -> Placed 3rd
        result = calculate_spr(1, 3, self.tiers)
        self.assertLess(result, 0)

if __name__ == '__main__':
    unittest.main()