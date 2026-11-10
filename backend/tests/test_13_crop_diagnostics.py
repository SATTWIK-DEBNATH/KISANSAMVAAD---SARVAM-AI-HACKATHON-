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

    def test_image_based_leaf_diagnosis(self):
        """Verifies photo-based leaf diagnosis without requiring text symptoms."""
        fake_leaf_image_b64 = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD...early_blight_concentric_rings"
        res = CropDiagnosticsService.diagnose(
            crop_name="Tomato",
            image_base64=fake_leaf_image_b64,
            language="kn-IN"
        )
        self.assertTrue(res["image_analyzed"])
        self.assertIsNotNone(res["visual_symptoms_detected"])
        self.assertEqual(res["primary_diagnosis"]["disease_name"], "Tomato Early Blight")
        self.assertIn("Alternaria solani", res["primary_diagnosis"]["pathogen"])
        self.assertIn("kn", res["advisory_localized"])
        self.assertTrue(res["safety_guardrails"]["is_safe"])

    def test_beans_vit_model_routing_and_diagnosis(self):
        """Verifies that Beans/Pulses route to nateraw/vit-base-beans Vision Transformer model."""
        fake_beans_rust_b64 = "data:image/jpeg;base64,/9j/4AAQ...bean_rust_pustules"
        res = CropDiagnosticsService.diagnose(
            crop_name="Beans",
            image_base64=fake_beans_rust_b64,
            language="hi-IN"
        )
        self.assertTrue(res["image_analyzed"])
        self.assertEqual(res["vision_model"], "nateraw/vit-base-beans")
        self.assertIn("Bean Rust", res["primary_diagnosis"]["disease_name"])
        self.assertEqual(res["primary_diagnosis"]["severity_level"], "Critical")
        self.assertTrue(res["escalate_to_kvk"])
        self.assertIn("Hexaconazole", res["recommended_interventions"]["approved_chemical"])
        self.assertTrue(res["safety_guardrails"]["is_safe"])

    def test_mobilenet_v2_model_for_general_crops(self):
        """Verifies that non-pulse crops route to linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification."""
        from app.services.plant_vision import PlantVisionClassifier
        model = PlantVisionClassifier.select_target_model("Tomato")
        self.assertEqual(model, "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification")
        pulse_model = PlantVisionClassifier.select_target_model("Moong Dal / Pulses")
        self.assertEqual(pulse_model, "nateraw/vit-base-beans")

if __name__ == "__main__":
    unittest.main()

