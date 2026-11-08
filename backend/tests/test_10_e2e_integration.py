"""
Test Suite 10: End-to-End Multilingual Agricultural Advisory Pipeline
Verifies the full pipeline: Audio Input -> Saaras ASR -> RAG Retrieval -> Guardrail Audit -> Bulbul TTS Audio.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.api.routes import APIRouter
from app.services.audio_service import AudioService

class TestEndToEndIntegration(unittest.TestCase):
    def test_complete_voice_advisory_pipeline(self):
        """
        Simulates:
        1. Farmer speaks Kannada query about tomato crop
        2. Saaras ASR converts audio to text
        3. Sarvam-1 LLM reasons with ICAR Kolar Tomato package
        4. AgriGuardrail validates safety and dosage
        5. Bulbul TTS converts advice into spoken Kannada voice
        """
        # Step 1: STT
        stt_res, stt_status = APIRouter.handle_post("/api/stt", {
            "audio_base64": "",
            "language_code": "kn-IN"
        }, {})
        self.assertEqual(stt_status, 200)
        self.assertTrue(stt_res["success"])
        transcript = stt_res["transcript"]
        self.assertGreater(len(transcript), 0)

        # Step 2: Chat Advisory with RAG
        chat_res, chat_status = APIRouter.handle_post("/api/chat", {
            "query": transcript,
            "language": "kn"
        }, {})
        self.assertEqual(chat_status, 200)
        advisory_text = chat_res["response"]
        self.assertGreater(len(advisory_text), 20)
        self.assertTrue(chat_res["guardrails"]["is_safe"])
        
        # Step 3: TTS Audio Output
        tts_res, tts_status = APIRouter.handle_post("/api/tts", {
            "text": advisory_text[:120],
            "target_language_code": "kn-IN"
        }, {})
        self.assertEqual(tts_status, 200)
        self.assertTrue(tts_res["success"])
        self.assertGreater(len(tts_res["audio_base64"]), 100)
        
        # Verify synthesized audio format
        audio_bytes = AudioService.decode_base64_audio(tts_res["audio_base64"])
        channels, rate, duration = AudioService.inspect_wav(audio_bytes)
        self.assertEqual(channels, 1)
        self.assertGreater(duration, 0.5)

    def test_complete_soil_health_pipeline(self):
        """
        Simulates:
        1. Farmer uploads Soil Card image
        2. Document Vision extracts parameters
        3. ICAR Diagnostic classifies NPK deficiency & acidic pH
        4. Farmer modifies pH value to verify instant re-evaluation
        """
        parse_res, p_status = APIRouter.handle_post("/api/soil-parse", {
            "filename": "kolar_farmer_soil.jpg"
        }, {})
        self.assertEqual(p_status, 200)
        card = parse_res["extracted_card"]
        self.assertEqual(card["district"], "Kolar")
        
        # Re-evaluate with farmer modification
        eval_res, e_status = APIRouter.handle_post("/api/soil-evaluate", {
            "nitrogen": 210.0,
            "phosphorus": 14.0,
            "potassium": 190.0,
            "ph": 6.8
        }, {})
        self.assertEqual(e_status, 200)
        self.assertIn("Neutral", eval_res["status"]["pH"])

if __name__ == "__main__":
    unittest.main()

