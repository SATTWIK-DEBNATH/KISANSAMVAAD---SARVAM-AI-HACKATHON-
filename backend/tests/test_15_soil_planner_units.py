"""
Test Suite 15: Soil Planner Unit Conversion & State Configurations
Verifies conversions between acres, hectares, guntas, and regional bighas,
as well as configurable state ratios.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.planner.conversion import UnitConverter, ACRE_TO_HECTARE_FACTOR

class TestSoilPlannerUnits(unittest.TestCase):
    """Verifies land area unit conversions and regional state rules."""

    def test_acre_to_hectare_standard(self):
        """Verifies 1 acre = 0.404686 ha and 2.5 acres conversion."""
        ha_1 = UnitConverter.to_hectares(1.0, "acre")
        self.assertAlmostEqual(ha_1, 0.404686, places=5)

        ha_2_5 = UnitConverter.to_hectares(2.5, "acres")
        self.assertAlmostEqual(ha_2_5, 2.5 * 0.404686, places=4)

    def test_hectare_identity(self):
        """Verifies hectare input passes through unchanged."""
        ha = UnitConverter.to_hectares(3.2, "hectare")
        self.assertEqual(ha, 3.2)
        ha_short = UnitConverter.to_hectares(1.5, "ha")
        self.assertEqual(ha_short, 1.5)

    def test_karnataka_gunta_conversion(self):
        """Verifies 40 guntas = 1 acre in Karnataka (0.404686 ha)."""
        ha_40_guntas = UnitConverter.to_hectares(40.0, "gunta", state="Karnataka")
        self.assertAlmostEqual(ha_40_guntas, 0.404686, places=5)

        ha_20_guntas = UnitConverter.to_hectares(20.0, "guntas", state="Karnataka")
        self.assertAlmostEqual(ha_20_guntas, 0.5 * 0.404686, places=5)

        acres_20 = UnitConverter.to_acres(20.0, "guntas", state="Karnataka")
        self.assertEqual(acres_20, 0.5)

    def test_zero_and_negative_area(self):
        """Verifies zero or negative area returns zero."""
        self.assertEqual(UnitConverter.to_hectares(0.0, "acre"), 0.0)
        self.assertEqual(UnitConverter.to_hectares(-5.0, "acre"), 0.0)

    def test_state_configurable_guntas(self):
        """Verifies guntas ratio can be queried per state."""
        self.assertEqual(UnitConverter.get_guntas_per_acre("Karnataka"), 40.0)
        self.assertEqual(UnitConverter.get_guntas_per_acre("Maharashtra"), 40.0)
        self.assertEqual(UnitConverter.get_guntas_per_acre("UnknownState"), 40.0)

if __name__ == "__main__":
    unittest.main()

