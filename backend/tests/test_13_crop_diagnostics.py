"""
Test Suite 13: Multimodal Crop Diagnostics Validation
Verifies symptom identification, differential diagnosis, confidence boundaries,
experimental disclaimers, CIBRC banned chemical filtering, and KVK escalation triggers.
"""

import unittest
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.services.crop_service import CropDiagnosticsService

class TestCropDiagnosticsService(unittest.TestCase):
    """Verifies crop diagnostics and agricultural safety guardrails."""

    def test_tomato_early_blight_diagnosis(self):
        """Verifies diagnostic match for concentric brown rings on tomato leaves."""
        res = CropDiagnosticsService.diagnose(
            crop_name="Tomato",
            symptoms="Lower leaves have concentric dark rings with yellow halo and brown blight spots",
            language="en"
        )
        self.assertTrue(res["experimental"])
        self.assertIn("Experimental AI Diagnostic Aid", res["disclaimer"])
        self.assertEqual(res["primary_diagnosis"]["disease_name"], "Tomato Early Blight")
        self.assertGreaterEqual(res["primary_diagnosis"]["confidence_score"], 0.70)
        self.assertIn("Septoria Leaf Spot", res["differential_diagnosis"]["secondary_suspect"])
        self.assertIn("Neem Oil", res["recommended_interventions"]["organic_biological"])
        self.assertIn("Mancozeb", res["recommended_interventions"]["approved_chemical"])
        self.assertTrue(res["safety_guardrails"]["is_safe"])

    def test_tomato_leaf_curl_whitefly_vector(self):
        """Verifies identification of leaf curl virus transmitted by whiteflies."""
        res = CropDiagnosticsService.diagnose(
            crop_name="Tomato",
            symptoms="Plants are stunted with upward leaf curling and small white flies flying around",
            language="kn-IN"
        )
        self.assertEqual(res["primary_diagnosis"]["disease_name"], "Tomato Leaf Curl Virus (ToLCV)")
        self.assertIn("Imidacloprid", res["recommended_interventions"]["approved_chemical"])
        # Dosage check: must not exceed 0.5ml/L
        self.assertIn("0.3ml to 0.4ml", res["recommended_interventions"]["approved_chemical"])
        self.assertTrue(res["safety_guardrails"]["is_safe"])

    def test_cotton_pink_bollworm_critical_escalation(self):
        """Verifies critical severity pest triggers KVK extension escalation."""
        res = CropDiagnosticsService.diagnose(
            crop_name="Cotton",
            symptoms="Rosette flowers observed and pink bollworm caterpillars found inside damaged bolls",
            language="en"
        )
        self.assertEqual(res["primary_diagnosis"]["disease_name"], "Pink Bollworm")
        self.assertEqual(res["primary_diagnosis"]["severity_level"], "Critical")
        self.assertTrue(res["escalate_to_kvk"])
        self.assertIsNotNone(res["kvk_escalation_details"])
        self.assertIn("KVK", res["kvk_escalation_details"]["center"])

    def test_unclear_symptoms_low_confidence_escalation(self):
        """Verifies ambiguous symptoms trigger low confidence and human KVK escalation."""
        res = CropDiagnosticsService.diagnose(
            crop_name="Tomato",
            symptoms="Leaves are slightly weird and maybe some strange color",
            language="en"
        )
        self.assertLess(res["primary_diagnosis"]["confidence_score"], 0.65)
        self.assertTrue(res["escalate_to_kvk"])
        self.assertIsNotNone(res["kvk_escalation_details"])

if __name__ == "__main__":
    unittest.main()

