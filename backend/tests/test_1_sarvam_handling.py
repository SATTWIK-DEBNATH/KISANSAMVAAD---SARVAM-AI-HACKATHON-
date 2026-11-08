"""
Test Suite 1: Sarvam AI Integration & Credential Handling
Verifies graceful handling of valid, missing, or placeholder credentials.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.integrations.sarvam.client import UnifiedSarvamClient
from app.core.config import settings

class TestSarvamHandling(unittest.TestCase):
    def test_missing_credentials_fallback(self):
        """Verifies client gracefully activates calibrated demo fallback without throwing uncaught errors."""
        client = UnifiedSarvamClient(api_key="")
        self.assertFalse(client.has_live_credentials())
        
        # Test STT fallback
        stt = client.speech_to_text(b"", language_code="kn-IN")
        self.assertTrue(stt["success"])
        self.assertIn("transcript", stt)
        self.assertIn("Demo Calibration", stt.get("provider", ""))

    def test_placeholder_credentials_fallback(self):
        """Verifies placeholder string does not trigger invalid network calls."""
        client = UnifiedSarvamClient(api_key="your_sarvam_api_key_here")
        self.assertFalse(client.has_live_credentials())

    def test_mayura_translation_graceful(self):
        """Verifies Mayura translation adapter operates smoothly."""
        client = UnifiedSarvamClient(api_key="")
        res = client.translate_text("Apply fertilizer", source_language_code="en-IN", target_language_code="kn-IN")
        self.assertTrue(res["success"])
        self.assertIn("translated_text", res)

if __name__ == "__main__":
    unittest.main()

