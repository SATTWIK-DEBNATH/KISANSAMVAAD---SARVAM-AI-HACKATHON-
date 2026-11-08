"""
Test Suite 12: Net Realisation Economic Calculator Validation
Verifies transport, labor, commission, packaging, and spoilage deductions,
as well as comparative analysis between local and terminal mandis.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.services.calculator_service import NetRealisationCalculator

class TestNetRealisationCalculator(unittest.TestCase):
    """Verifies economic net realization calculations for farmers."""

    def test_single_mandi_cost_deductions(self):
        """Verifies itemized deductions match mathematical expectations."""
        res = NetRealisationCalculator.calculate_single_mandi(
            market_name="Kolar APMC",
            commodity="Tomato",
            quantity_quintals=100.0,
            modal_price_per_quintal=2000.0,
            distance_km=20.0,
            transport_rate_per_km=25.0,  # 20 * 25 = 500
            labor_rate_per_quintal=30.0,  # 100 * 30 = 3000
            mandi_commission_pct=2.0,    # 2% of 200,000 = 4000
            packaging_rate_per_quintal=40.0,  # 100 * 40 = 4000
            spoilage_pct=2.0             # 2% of 200,000 = 4000
        )
        self.assertEqual(res["gross_sale_inr"], 200000.0)
        ded = res["itemized_deductions"]
        self.assertEqual(ded["transport_cost_inr"], 500.0)
        self.assertEqual(ded["loading_labor_inr"], 3000.0)
        self.assertEqual(ded["mandi_fee_commission_inr"], 4000.0)
        self.assertEqual(ded["packaging_cost_inr"], 4000.0)
        self.assertEqual(ded["spoilage_loss_inr"], 4000.0)
        self.assertEqual(ded["total_deductions_inr"], 15500.0)
        self.assertEqual(res["net_realisation_inr"], 184500.0)
        self.assertEqual(res["net_rate_per_quintal_inr"], 1845.0)

    def test_market_comparison_terminal_advantage(self):
        """Verifies terminal market recommendation when price premium outweighs transport."""
        comp = NetRealisationCalculator.compare_mandis(
            commodity="Tomato",
            quantity_quintals=50.0,
            local_market={"name": "Kolar APMC", "price": 1600.0, "distance_km": 15.0, "transport_rate_per_km": 20.0, "spoilage_pct": 1.5},
            terminal_market={"name": "Yeshwanthpur APMC", "price": 2400.0, "distance_km": 70.0, "transport_rate_per_km": 25.0, "spoilage_pct": 3.0}
        )
        self.assertEqual(comp["recommended_market"], "Yeshwanthpur APMC")
        self.assertGreater(comp["net_difference_inr"], 0)
        self.assertIn("Yeshwanthpur APMC", comp["recommendation_en"])
        self.assertIn("Yeshwanthpur APMC", comp["recommendation_kn"])
        self.assertIn("Yeshwanthpur APMC", comp["recommendation_hi"])

    def test_market_comparison_local_advantage_when_spoilage_high(self):
        """Verifies local market recommendation when high transport and spoilage wipe out margin."""
        comp = NetRealisationCalculator.compare_mandis(
            commodity="Ripe Tomato",
            quantity_quintals=40.0,
            local_market={"name": "Kolar APMC", "price": 1900.0, "distance_km": 10.0, "transport_rate_per_km": 20.0, "spoilage_pct": 1.0},
            terminal_market={"name": "Azadpur APMC", "price": 2000.0, "distance_km": 250.0, "transport_rate_per_km": 35.0, "spoilage_pct": 8.0}
        )
        self.assertEqual(comp["recommended_market"], "Kolar APMC")
        self.assertLess(comp["net_difference_inr"], 0)
        self.assertIn("Kolar APMC", comp["recommendation_en"])

if __name__ == "__main__":
    unittest.main()
