"""
KisanSamvaad - Audio Utility Service
Handles audio format conversions, base64 encoding/decoding, and payload sizing.
"""

import base64
import io
import wave
from typing import Tuple

class AudioService:
    """Audio utility helper."""

    @classmethod
    def decode_base64_audio(cls, b64_string: str) -> bytes:
        """Decodes base64 string safely."""
        if not b64_string:
            return b""
        # Strip header if present (e.g. data:audio/wav;base64,...)
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]
        try:
            return base64.b64decode(b64_string)
        except Exception:
            return b""

    @classmethod
    def inspect_wav(cls, audio_bytes: bytes) -> Tuple[int, int, float]:
        """
        Inspects WAV bytes and returns channels, samplerate, duration_seconds.
        """
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                channels = wf.getnchannels()
                rate = wf.getframerate()
                frames = wf.getnframes()
                duration = frames / float(rate) if rate > 0 else 0.0
                return channels, rate, round(duration, 2)
        except Exception:
            return 1, 16000, 0.0

