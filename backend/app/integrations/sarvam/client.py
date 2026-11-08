"""
KisanSamvaad - Unified Sarvam AI Client SDK
Orchestrates Saaras ASR, Bulbul TTS, Sarvam-1 LLM, Document Vision, and Mayura Translation.
"""

from typing import Dict, Any, Optional
from .asr import SaarasASRAdapter
from .tts import BulbulTTSAdapter
from .llm import SarvamLLMAdapter
from .vision import SarvamVisionAdapter
from .translate import MayuraTranslationAdapter
from ...core.config import settings

class UnifiedSarvamClient:
    """Unified access point for all sovereign Indic AI models."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.sarvam_api_key
        self.base_url = settings.sarvam_base_url
        
        self.asr = SaarasASRAdapter(api_key=self.api_key, base_url=self.base_url)
        self.tts = BulbulTTSAdapter(api_key=self.api_key, base_url=self.base_url)
        self.llm = SarvamLLMAdapter(api_key=self.api_key, base_url=self.base_url)
        self.vision = SarvamVisionAdapter(api_key=self.api_key, base_url=self.base_url)
        self.translate = MayuraTranslationAdapter(api_key=self.api_key, base_url=self.base_url)

    def has_live_credentials(self) -> bool:
        if not self.api_key:
            return False
        k = self.api_key.strip().lower()
        if len(k) <= 8 or "placeholder" in k or "your_" in k or "api_key" in k or "demo" in k or "test" in k:
            return False
        return True

    def speech_to_text(self, audio_bytes: bytes, language_code: str = "kn-IN", mode: str = "codemix") -> Dict[str, Any]:
        return self.asr.transcribe(audio_bytes=audio_bytes, language_code=language_code, mode=mode)

    def text_to_speech(self, text: str, target_language_code: str = "kn-IN", speaker: str = "bulbul:v1") -> Dict[str, Any]:
        return self.tts.synthesize(text=text, target_language_code=target_language_code, speaker=speaker)

    def chat_advisory(self, query: str, language: str = "kn") -> Dict[str, Any]:
        return self.llm.reason_and_advise(query=query, language=language)

    def parse_soil_health_card(self, filename: str = "soil_health_card.jpg", image_bytes: Optional[bytes] = None) -> Dict[str, Any]:
        return self.vision.parse_soil_health_card(image_bytes=image_bytes, filename=filename)

    def translate_text(self, text: str, source_language_code: str = "en-IN", target_language_code: str = "kn-IN") -> Dict[str, Any]:
        return self.translate.translate(text, source_language_code, target_language_code)
