"""
Test Suite 14: Government Schemes Intelligence Validation
Verifies scheme catalog retrieval, personalized eligibility evaluation,
landholding constraints, crop requirements, and documentation checklists.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.services.scheme_service import SchemeIntelligenceService

class TestSchemeIntelligenceService(unittest.TestCase):
    """Verifies government schemes intelligence and eligibility checks."""

    def test_catalog_retrieval(self):
        """Verifies deep catalog contains core national and Karnataka schemes."""
        schemes = SchemeIntelligenceService.list_all_schemes()
        self.assertGreaterEqual(len(schemes), 5)
        codes = [s["code"] for s in schemes]
        self.assertIn("PM_KISAN", codes)
        self.assertIn("PMFBY", codes)
        self.assertIn("KCC", codes)
        self.assertIn("RAITA_SIRI", codes)
        self.assertIn("PM_KUSUM", codes)

    def test_karnataka_millet_farmer_eligibility(self):
        """Verifies Karnataka millet farmer qualifies for Karnataka Raita Siri and PM-KISAN."""
        eval_res = SchemeIntelligenceService.evaluate_eligibility(
            farmer_name="Manjunath Gowda",
            landholding_acres=3.0,
            state="Karnataka",
            district="Kolar",
            crops=["Ragi", "Tomato"],
            irrigation_source="Borewell"
        )
        self.assertEqual(eval_res["farmer_name"], "Manjunath Gowda")
        self.assertGreaterEqual(eval_res["eligible_schemes_count"], 4)

        evals_by_id = {e["scheme_id"]: e for e in eval_res["scheme_evaluations"]}
        # Karnataka Raita Siri should be ELIGIBLE because state is Karnataka, crop is Ragi, land is <= 5 acres
        self.assertEqual(evals_by_id["raita_siri"]["eligibility_status"], "Eligible")
        self.assertIn("Pahani / RTC", evals_by_id["raita_siri"]["required_documents"][0])

        # PM-KISAN should be ELIGIBLE
        self.assertEqual(evals_by_id["pm_kisan"]["eligibility_status"], "Eligible")

    def test_raita_siri_ineligible_for_non_karnataka(self):
        """Verifies farmer outside Karnataka cannot claim Karnataka Raita Siri."""
        eval_res = SchemeIntelligenceService.evaluate_eligibility(
            farmer_name="Sukhwinder Singh",
            landholding_acres=4.0,
            state="Punjab",
            district="Ludhiana",
            crops=["Wheat", "Paddy"]
        )
        evals_by_id = {e["scheme_id"]: e for e in eval_res["scheme_evaluations"]}
        self.assertEqual(evals_by_id["raita_siri"]["eligibility_status"], "Ineligible")
        self.assertIn("Karnataka", evals_by_id["raita_siri"]["reasons"][0])

if __name__ == "__main__":
    unittest.main()

