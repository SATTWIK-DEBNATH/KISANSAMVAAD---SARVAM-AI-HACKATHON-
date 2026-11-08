"""
KisanSamvaad - Application Configuration & Settings
Manages environment variables, Sarvam credentials, timeouts, and system defaults.
"""

import os
from dataclasses import dataclass
from typing import List

@dataclass
class AppSettings:
    """Application global settings."""
    app_name: str = "KisanSamvaad"
    app_version: str = "2.4.0"
    app_environment: str = os.getenv("APP_ENV", "production")
    
    # Sarvam AI API Configuration
    sarvam_api_key: str = os.getenv("SARVAM_API_KEY", "")
    sarvam_base_url: str = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai")
    sarvam_timeout_seconds: int = int(os.getenv("SARVAM_TIMEOUT_SECONDS", "10"))
    
    # Supported Indian Indic Languages
    supported_languages: List[str] = (
        "kn-IN",  # Kannada (Primary Karnataka focus)
        "hi-IN",  # Hindi
        "ta-IN",  # Tamil
        "te-IN",  # Telugu
        "mr-IN",  # Marathi
        "pa-IN",  # Punjabi
        "bn-IN",  # Bengali
        "gu-IN",  # Gujarati
        "en-IN"   # Indian English
    )
    
    # Host & Port
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Safety Engine
    strict_icar_safety: bool = os.getenv("STRICT_ICAR_SAFETY", "true").lower() in ("true", "1", "yes")
    
    # Mandi & Weather Data Defaults
    mandi_cache_ttl_minutes: int = 15
    weather_refresh_hours: int = 3
    
    def has_live_sarvam_key(self) -> bool:
        """Returns True if a non-placeholder Sarvam API key is configured."""
        return bool(self.sarvam_api_key and len(self.sarvam_api_key.strip()) > 8 and "placeholder" not in self.sarvam_api_key.lower())

settings = AppSettings()

