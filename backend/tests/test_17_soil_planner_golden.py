"""
Test Suite 17: Soil Planner Golden-File Regression Tests
Hand-verified reference cases testing end-to-end plan results across tomato,
ragi, maize, and high-fertility soil scenarios.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.planner.planner_service import SoilPlannerService

class TestSoilPlannerGoldenCases(unittest.TestCase):
    """Verifies complete plans against hand-calculated agronomic baselines."""

    def test_golden_case_1_tomato_two_acres_kolar(self):
        """
        Golden Case 1: 2 acres of Tomato in Kolar, Karnataka.
        Soil: Low Nitrogen (198.5 kg/ha), Low Phosphorus (9.2 kg/ha), Medium Potassium (152 kg/ha), pH 5.8 (acidic).
        """
        req_data = {
            "crop": "tomato",
            "area": 2.0,
            "unit": "acre",
            "state": "Karnataka",
            "soil_values": {
                "nitrogen_kg_ha": 198.5,
                "phosphorus_kg_ha": 9.2,
                "potassium_kg_ha": 152.0,
                "ph": 5.8
            },
            "language": "kn"
        }
        res = SoilPlannerService.generate_plan(req_data)

        # 1. Verify inputs echoed
        inputs = res["inputs_echo"]
        self.assertEqual(inputs["crop"], "tomato")
        self.assertEqual(inputs["area_entered"], 2.0)
        self.assertEqual(inputs["unit_entered"], "acre")
        self.assertAlmostEqual(inputs["area_hectares"], 0.8094, places=3)
        self.assertEqual(inputs["soil_ratings"]["nitrogen"], "low")
        self.assertEqual(inputs["soil_ratings"]["phosphorus"], "low")
        self.assertEqual(inputs["soil_ratings"]["potassium"], "medium")
        self.assertEqual(inputs["ph_classification"], "acidic")

        # 2. Verify nutrient target requirements
        reqs = res["nutrient_requirements_kg"]
        self.assertAlmostEqual(reqs["nitrogen_kg"], 151.76, delta=2.0)
        self.assertAlmostEqual(reqs["phosphorus_p2o5_kg"], 101.17, delta=2.0)
        self.assertAlmostEqual(reqs["potassium_k2o_kg"], 80.94, delta=2.0)

        # 3. Verify discrete fertilizer bags
        plan = res["fertilizer_plan"]
        self.assertTrue(plan["is_feasible"])
        bag_counts = {b["fertilizer_id"]: b["bags_count"] for b in plan["bags"]}
        self.assertEqual(bag_counts.get("dap"), 4)
        self.assertEqual(bag_counts.get("ssp"), 2)
        self.assertEqual(bag_counts.get("urea"), 6)
        self.assertEqual(bag_counts.get("mop"), 3)

        # Total cost: 4 * 1350 + 2 * 550 + 6 * 266.5 + 3 * 1700 = 5400 + 1100 + 1599 + 5100 = 13199.0
        self.assertAlmostEqual(plan["total_cost_inr"], 13199.0, places=1)

        # 4. Verify organic alternative
        org = res["organic_alternative"]
        self.assertIsNotNone(org)
        self.assertAlmostEqual(org["recommended_tonnes"], 20.2, delta=0.5)

        # 5. Verify timing schedule has basal and top-dress stages
        stages = res["timing_schedule"]
        self.assertGreaterEqual(len(stages), 2)
        self.assertIn("Basal", stages[0]["stage"])

        # 6. Verify spoken narration
        narration = res["spoken_narration"]
        self.assertIn("ಟೊಮೇಟೊ", narration["text"])
        self.assertIn("13,199", narration["text"])

    def test_golden_case_2_ragi_one_acre_medium_soil(self):
        """
        Golden Case 2: 1 acre of Ragi (Finger Millet) with balanced medium soil.
        1 acre = 0.4047 ha. Dose: 60:30:30 kg/ha. Targets: 24.3 kg N, 12.1 kg P, 12.1 kg K.
        Plan: 1 bag DAP, 1 bag Urea, 1 bag MOP. Total cost: ₹3,316.50.
        """
        req_data = {
            "crop": "ragi",
            "area": 1.0,
            "unit": "acre",
            "state": "Karnataka",
            "soil_values": {
                "nitrogen_kg_ha": 350.0,
                "phosphorus_kg_ha": 18.0,
                "potassium_kg_ha": 200.0,
                "ph": 6.8
            },
            "language": "en"
        }
        res = SoilPlannerService.generate_plan(req_data)
        plan = res["fertilizer_plan"]
        self.assertTrue(plan["is_feasible"])

        bag_counts = {b["fertilizer_id"]: b["bags_count"] for b in plan["bags"]}
        self.assertEqual(bag_counts.get("dap"), 1)
        self.assertEqual(bag_counts.get("urea"), 1)
        self.assertEqual(bag_counts.get("mop"), 1)
        self.assertAlmostEqual(plan["total_cost_inr"], 3316.5, places=1)

        narration = res["spoken_narration"]["text"]
        self.assertTrue("3,316" in narration or "3,317" in narration)
        self.assertIn("Urea", narration)

    def test_golden_case_3_high_fertility_zero_fertilizer(self):
        """
        Golden Case 3: Soil with saturated nutrient reserves (N > 700, P > 50, K > 450).
        Recommends zero chemical fertilizer to protect soil and save farmer money.
        """
        req_data = {
            "crop": "maize",
            "area": 3.0,
            "unit": "acre",
            "state": "Karnataka",
            "soil_values": {
                "nitrogen_kg_ha": 750.0,
                "phosphorus_kg_ha": 60.0,
                "potassium_kg_ha": 500.0,
                "ph": 7.2
            },
            "language": "hi"
        }
        res = SoilPlannerService.generate_plan(req_data)
        plan = res["fertilizer_plan"]
        self.assertTrue(plan["is_feasible"])
        self.assertEqual(len(plan["bags"]), 0)
        self.assertEqual(plan["total_cost_inr"], 0.0)
        self.assertIn("किसी रासायनिक खाद की आवश्यकता नहीं है", res["spoken_narration"]["text"])

if __name__ == "__main__":
    unittest.main()
