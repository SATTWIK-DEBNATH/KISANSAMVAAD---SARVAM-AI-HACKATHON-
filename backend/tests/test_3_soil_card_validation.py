"""
Test Suite 3: Soil Health Card Extraction & Agronomic Diagnostic Validation
Verifies Document Vision parsing, ICAR classification, and manual value re-evaluation.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.integrations.sarvam.client import UnifiedSarvamClient
from app.services.soil_service import SoilDiagnosticService

class TestSoilCardValidation(unittest.TestCase):
    def setUp(self):
        self.client = UnifiedSarvamClient()

    def test_soil_health_card_extraction(self):
        """Verifies extracted parameters, confidence metrics, and provenance citation."""
        doc = self.client.parse_soil_health_card(filename="kolar_soil_sample.jpg")
        self.assertTrue(doc["success"])
        card = doc["extracted_card"]
        self.assertEqual(card["district"], "Kolar")
        self.assertGreater(card["extraction_confidence"], 0.85)
        self.assertIn("nitrogen", card["confidence_ratings"])
        self.assertIn("provenance", card)
        self.assertEqual(card["provenance"]["document_id"], "GOI-DAC-SHC-2024")

    def test_acidic_soil_diagnosis_and_lime_recommendation(self):
        """Verifies pH < 6.5 triggers agricultural lime remediation in Kannada and Hindi."""
        diag = SoilDiagnosticService.evaluate_sample(n=180.0, p=7.5, k=110.0, ph=5.4)
        self.assertIn("Acidic", diag["status"]["pH"])
        self.assertTrue(any("Lime" in r or "चूना" in r or "ಸುಣ್ಣ" in r for r in diag["recommendations_kn"]))

    def test_alkaline_soil_diagnosis_and_gypsum_recommendation(self):
        """Verifies pH > 8.0 triggers gypsum and green manure remediation."""
        diag = SoilDiagnosticService.evaluate_sample(n=350.0, p=18.0, k=250.0, ph=8.4)
        self.assertIn("Alkaline", diag["status"]["pH"])
        self.assertTrue(any("Gypsum" in r or "जिप्सम" in r or "ಜಿಪ್ಸಮ್" in r for r in diag["recommendations_kn"]))

    def test_manual_correction_recalculation(self):
        """Verifies farmer manual input corrections dynamically re-evaluate status."""
        # Farmer modifies extracted nitrogen from low (190) to optimal (320)
        diag = SoilDiagnosticService.evaluate_sample(n=320.0, p=15.0, k=200.0, ph=6.8)
        self.assertIn("Medium", diag["status"]["N"])
        self.assertIn("Neutral", diag["status"]["pH"])

if __name__ == "__main__":
    unittest.main()

