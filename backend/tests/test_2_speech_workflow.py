"""
Test Suite 2: Speech Workflow & Voice Round-Trip
Verifies Saaras ASR transcription and Bulbul TTS audio synthesis across Indian languages.
"""

import unittest
import sys
import os
import base64

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.integrations.sarvam.client import UnifiedSarvamClient
from app.services.audio_service import AudioService

class TestSpeechWorkflow(unittest.TestCase):
    def setUp(self):
        self.client = UnifiedSarvamClient()

    def test_multilingual_speech_recognition(self):
        """Verifies transcription support for Kannada, Hindi, and English."""
        for lang in ["kn-IN", "hi-IN", "en-IN"]:
            res = self.client.speech_to_text(b"mock_audio", language_code=lang)
            self.assertTrue(res["success"])
            self.assertTrue(len(res["transcript"]) > 0)
            self.assertEqual(res["language_code"], lang)

    def test_bulbul_audio_synthesis(self):
        """Verifies Bulbul speech synthesis generates valid playable WAV audio bytes."""
        kannada_text = "ರೈತ ಬಾಂಧವರೇ, ನಿಮ್ಮ ಬೆಳೆಗೆ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ."
        tts_res = self.client.text_to_speech(kannada_text, target_language_code="kn-IN")
        self.assertTrue(tts_res["success"])
        self.assertTrue(len(tts_res["audio_base64"]) > 50)
        
        # Verify audio decodes to valid WAV
        decoded_bytes = AudioService.decode_base64_audio(tts_res["audio_base64"])
        channels, rate, duration = AudioService.inspect_wav(decoded_bytes)
        self.assertEqual(channels, 1)
        self.assertEqual(rate, 16000)
        self.assertGreater(duration, 0.5)

if __name__ == "__main__":
    unittest.main()

