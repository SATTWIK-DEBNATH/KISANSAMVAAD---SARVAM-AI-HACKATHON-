"""
Test Suite 9: API Layer Error Handling & Resilience
Verifies that all endpoints handle malformed inputs, bad keys, and nonexistent routes gracefully.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.api.routes import APIRouter

class TestAPIErrorHandling(unittest.TestCase):
    def test_nonexistent_endpoint_404(self):
        """Verifies 404 response for unknown routes."""
        res, status = APIRouter.handle_get("/api/invalid-route", {})
        self.assertEqual(status, 404)
        self.assertIn("error", res)

    def test_empty_chat_body_handled(self):
        """Verifies chat endpoint returns gracefully without crashing on empty payload."""
        res, status = APIRouter.handle_post("/api/chat", {}, {})
        self.assertEqual(status, 200)
        self.assertIn("response", res)

    def test_empty_audio_stt_handled(self):
        """Verifies STT endpoint returns fallback transcript without crashing on empty audio."""
        res, status = APIRouter.handle_post("/api/stt", {"audio_base64": ""}, {})
        self.assertEqual(status, 200)
        self.assertTrue(res["success"])

    def test_invalid_dtmf_telephony_digit(self):
        """Verifies telephony service returns menu prompt for unrecognized DTMF key."""
        res, status = APIRouter.handle_post("/api/telephony", {"digit": "9"}, {})
        self.assertEqual(status, 200)
        self.assertEqual(res["menu"], "Main Menu")

    def test_health_check_endpoint(self):
        """Verifies /api/health returns 200 with service information and language list."""
        res, status = APIRouter.handle_get("/api/health", {})
        self.assertEqual(status, 200)
        self.assertEqual(res["status"], "healthy")
        self.assertGreater(len(res["supported_languages"]), 5)

if __name__ == "__main__":
    unittest.main()

