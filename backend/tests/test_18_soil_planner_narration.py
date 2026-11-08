"""
Test Suite 18: Soil Planner Narration & Number-Grounding Validation
Verifies localized templates across kn, hi, ta, en, number-grounding hallucination interceptors,
and voice slot extraction with clarifying questions.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.planner.narration import NumberGroundingValidator, NarrationRenderer
from app.planner.slot_extractor import VoiceSlotExtractor

class TestSoilPlannerNarration(unittest.TestCase):
    """Verifies spoken narration grounding and slot extraction."""

    def test_number_grounding_valid_text(self):
        """Verifies candidate text containing only plan numbers is approved."""
        plan_dict = {
            "inputs_echo": {"area_entered": 2.0},
            "fertilizer_plan": {
                "total_cost_inr": 13449.0,
                "bags": [
                    {"fertilizer_id": "dap", "bags_count": 5},
                    {"fertilizer_id": "urea", "bags_count": 6},
                    {"fertilizer_id": "mop", "bags_count": 3}
                ]
            },
            "timing_schedule": [
                {"stage": "30 days split"}
            ]
        }
        # Candidate text with exactly the plan's numbers
        candidate = "For 2 acres, purchase 5 bags of DAP, 6 bags of Urea, and 3 bags of MOP, totaling about Rs 13449. Apply split after 30 days."
        is_grounded, ungrounded = NumberGroundingValidator.is_grounded(candidate, plan_dict)
        self.assertTrue(is_grounded)
        self.assertEqual(len(ungrounded), 0)

    def test_number_grounding_hallucinated_number_blocked(self):
        """Verifies candidate text with hallucinated numbers is rejected."""
        plan_dict = {
            "inputs_echo": {"area_entered": 2.0},
            "fertilizer_plan": {
                "total_cost_inr": 13449.0,
                "bags": [{"bags_count": 5}]
            }
        }
        # Hallucinated "99 bags" and "Rs 55000"
        hallucinated = "Buy 99 bags of fertilizer for Rs 55000."
        is_grounded, ungrounded = NumberGroundingValidator.is_grounded(hallucinated, plan_dict)
        self.assertFalse(is_grounded)
        self.assertIn(99.0, ungrounded)
        self.assertIn(55000.0, ungrounded)

    def test_multilingual_template_snapshots(self):
        """Verifies localized templates generate valid non-empty strings for all 4 languages."""
        bags = [
            {"fertilizer_id": "dap", "bags_count": 4, "name": "DAP"},
            {"fertilizer_id": "urea", "bags_count": 3, "name": "Urea"}
        ]
        total_cost = 6200.0

        for lang in ("kn", "hi", "ta", "en"):
            text = NarrationRenderer.render_template(
                crop="Tomato",
                area=2.0,
                unit="acre",
                bags=bags,
                total_cost_inr=total_cost,
                delay_recommended=False,
                language=lang
            )
            self.assertIsNotNone(text)
            self.assertGreater(len(text), 20)
            self.assertIn("6,200", text)

    def test_slot_extraction_english_complete(self):
        """Verifies slot extraction from English voice query."""
        res = VoiceSlotExtractor.extract_slots("2 acres tomato", language="en")
        self.assertTrue(res["is_complete"])
        self.assertEqual(res["crop"], "tomato")
        self.assertEqual(res["area"], 2.0)
        self.assertEqual(res["unit"], "acre")
        self.assertIsNone(res["clarifying_question"])

    def test_slot_extraction_kannada_complete(self):
        """Verifies slot extraction from Kannada voice query."""
        res = VoiceSlotExtractor.extract_slots("ನನ್ನ 3 ಎಕರೆ ಟೊಮೇಟೊ ಬೆಳೆಗೆ ಗೊಬ್ಬರ ಎಷ್ಟು ಬೇಕು", language="kn")
        self.assertTrue(res["is_complete"])
        self.assertEqual(res["crop"], "tomato")
        self.assertEqual(res["area"], 3.0)
        self.assertEqual(res["unit"], "acre")

    def test_slot_extraction_gunta_support(self):
        """Verifies gunta unit extraction."""
        res = VoiceSlotExtractor.extract_slots("15 gunta ragi", language="en")
        self.assertTrue(res["is_complete"])
        self.assertEqual(res["crop"], "ragi")
        self.assertEqual(res["area"], 15.0)
        self.assertEqual(res["unit"], "gunta")

    def test_slot_extraction_missing_crop_clarifying_question(self):
        """Verifies clarifying question is returned when crop is missing."""
        res = VoiceSlotExtractor.extract_slots("2 acres fertilizer plan", language="kn")
        self.assertFalse(res["is_complete"])
        self.assertIn("crop", res["missing_slots"])
        self.assertIsNotNone(res["clarifying_question"])
        self.assertIn("ಯಾವ ಬೆಳೆಗೆ", res["clarifying_question"])

if __name__ == "__main__":
    unittest.main()

