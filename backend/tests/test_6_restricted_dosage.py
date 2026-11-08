"""
Test Suite 6: Restricted Chemical Dosage & Overdose Clamping
Verifies mathematical bounds enforcement on approved agrochemicals (Imidacloprid, Chlorpyrifos, Urea).
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.safety.agri_guardrails import AgriGuardrailEngine

class TestRestrictedDosage(unittest.TestCase):
    def test_safe_dosage_accepted(self):
        """Verifies safe ICAR approved dilutions pass validation."""
        safe_inputs = [
            "Spray Imidacloprid 0.3 ml per liter of water for aphids with protective mask.",
            "Apply Chlorpyrifos 2.0 ml per liter around root zone wearing rubber gloves.",
            "Use Mancozeb 2.0 gm per liter of water for leaf spot."
        ]
        for text in safe_inputs:
            res = AgriGuardrailEngine.validate_recommendation(text)
            self.assertTrue(res["is_safe"], f"Safe recommendation falsely flagged: {text}")

    def test_dangerous_overdose_intercepted(self):
        """Verifies lethal overdoses (e.g. 10x-30x safe rate) are blocked."""
        dangerous_inputs = [
            ("Mix Imidacloprid 10 ml per liter of water for instant kill.", "Imidacloprid"),
            ("Apply Chlorpyrifos 15 ml per liter of water directly to leaves.", "Chlorpyrifos"),
            ("Use Mancozeb 25 gm per liter of water on tender plants.", "Mancozeb")
        ]
        for text, chem in dangerous_inputs:
            res = AgriGuardrailEngine.validate_recommendation(text)
            self.assertFalse(res["is_safe"], f"Overdose not caught for: {chem}")
            self.assertTrue(any("EXCESSIVE DOSAGE DETECTED" in v for v in res["violations"]))

    def test_sanitization_injects_kvk_warning(self):
        """Verifies sanitization appends KVK warning in farmer language upon violation."""
        raw_text = "Mix Imidacloprid 12 ml per liter."
        val = AgriGuardrailEngine.validate_recommendation(raw_text)
        sanitized_hi = AgriGuardrailEngine.sanitize_response(raw_text, val, language="hi")
        self.assertIn("कृषि सुरक्षा चेतावनी", sanitized_hi)
        
        sanitized_kn = AgriGuardrailEngine.sanitize_response(raw_text, val, language="kn")
        self.assertIn("ಕೃಷಿ ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆ", sanitized_kn)

if __name__ == "__main__":
    unittest.main()

