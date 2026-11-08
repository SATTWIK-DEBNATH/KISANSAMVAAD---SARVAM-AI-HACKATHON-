"""
Test Suite 16: Soil Planner Multi-Nutrient Integer Optimizer
Verifies multi-nutrient accounting (DAP supplying N), statutory Urea 45 kg bag sizing,
whole-bag discrete rounding, overshoot limits, and high-nutrient zero plans.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.planner.optimizer import FertilizerOptimizer
from app.planner.data_loader import PlannerDataLoader

class TestSoilPlannerOptimizer(unittest.TestCase):
    """Verifies integer programming fertilizer allocation."""

    def test_urea_statutory_bag_size(self):
        """Verifies Urea is configured as statutory 45 kg bag as mandated by GoI."""
        ferts = PlannerDataLoader.load_fertilizers()
        self.assertEqual(ferts["urea"]["bag_size_kg"], 45.0)
        self.assertEqual(ferts["urea"]["n_content_pct"], 46.0)

    def test_dap_supplies_nitrogen_credit(self):
        """
        Verifies DAP (18-46-0) supplies Nitrogen, directly reducing Urea requirements.
        If P target is 46 kg, 2 bags of 50kg DAP supply 46 kg P2O5 and 18 kg N.
        If N target is 38.7 kg, remaining N needed is 38.7 - 18 = 20.7 kg N (exactly 1 bag of 45kg Urea).
        Without DAP N credit, a naive model would order 2 bags of Urea.
        """
        plan = FertilizerOptimizer.optimize(
            target_n_kg=38.7,     # 18kg from 2 bags DAP + 20.7kg from 1 bag Urea = 38.7kg N
            target_p2o5_kg=46.0,  # Exactly 2 bags of 50kg DAP (2 * 50 * 0.46 = 46.0)
            target_k2o_kg=0.0
        )
        self.assertTrue(plan["is_feasible"])
        bag_counts = {b["fertilizer_id"]: b["bags_count"] for b in plan["bags"]}
        self.assertEqual(bag_counts.get("dap"), 2)
        # 2 bags of DAP supply 18 kg N, leaving 20.7 kg N -> exactly 1 bag of Urea (45kg * 0.46)
        self.assertEqual(bag_counts.get("urea"), 1)
        self.assertAlmostEqual(plan["nutrients_delivered_kg"]["n"], 38.7, places=1)
        self.assertAlmostEqual(plan["nutrients_delivered_kg"]["p2o5"], 46.0, places=1)

    def test_whole_bag_integer_constraint(self):
        """Verifies every allocated fertilizer item is an integer whole bag count."""
        plan = FertilizerOptimizer.optimize(
            target_n_kg=120.0,
            target_p2o5_kg=80.0,
            target_k2o_kg=60.0
        )
        self.assertTrue(plan["is_feasible"])
        for b in plan["bags"]:
            self.assertIsInstance(b["bags_count"], int)
            self.assertGreater(b["bags_count"], 0)
            # Delivered total kg must equal bags_count * bag_size_kg
            self.assertEqual(b["total_kg"], b["bags_count"] * b["bag_size_kg"])

    def test_high_nutrient_soil_zero_application(self):
        """Verifies zero targets return zero bags and zero cost."""
        plan = FertilizerOptimizer.optimize(
            target_n_kg=0.0,
            target_p2o5_kg=0.0,
            target_k2o_kg=0.0
        )
        self.assertTrue(plan["is_feasible"])
        self.assertEqual(len(plan["bags"]), 0)
        self.assertEqual(plan["total_cost_inr"], 0.0)

    def test_potassium_mop_allocation(self):
        """Verifies MOP (60% K2O in 50 kg bags = 30 kg K2O/bag) allocation."""
        # 60 kg K2O target requires exactly 2 bags MOP
        plan = FertilizerOptimizer.optimize(
            target_n_kg=0.0,
            target_p2o5_kg=0.0,
            target_k2o_kg=60.0
        )
        self.assertTrue(plan["is_feasible"])
        bag_counts = {b["fertilizer_id"]: b["bags_count"] for b in plan["bags"]}
        self.assertEqual(bag_counts.get("mop"), 2)
        self.assertEqual(plan["nutrients_delivered_kg"]["k2o"], 60.0)

if __name__ == "__main__":
    unittest.main()
