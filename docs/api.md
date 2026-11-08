# KisanSamvaad - REST API Specification
## Sovereign Indic Voice & Document AI for Indian Agriculture

Base URL: `http://127.0.0.1:8000`  
Standard: JSON UTF-8 with full CORS headers enabled (`Access-Control-Allow-Origin: *`).

---

## 1. Health & Capability Discovery

### `GET /api/health`
Checks server status, model engine versions, active credentials, and supported Indic languages.

#### Response:
```json
{
  "status": "healthy",
  "service": "KisanSamvaad Sovereign Agricultural AI",
  "version": "2.4.0",
  "sarvam_live_connected": false,
  "supported_languages": [
    {"code": "kn-IN", "name": "Kannada (ಕನ್ನಡ) - Primary Regional Focus"},
    {"code": "hi-IN", "name": "Hindi (हिंदी)"},
    {"code": "ta-IN", "name": "Tamil (தமிழ்)"},
    {"code": "te-IN", "name": "Telugu (తెలుగు)"},
    {"code": "mr-IN", "name": "Marathi (मराठी)"},
    {"code": "en-IN", "name": "Indian English"}
  ],
  "active_models": {
    "asr": "Sarvam Saaras v3 (Indic Speech Recognition)",
    "tts": "Sarvam Bulbul v4 (Indian Prosody Synthesis)",
    "llm": "Sarvam-1 (2B Sovereign Indic Core)",
    "vision": "Sarvam Document Parse (Soil Card OCR)",
    "translation": "Sarvam Mayura Indic Translation"
  },
  "guardrails": "ICAR-Grounded AgriGuardrail Engine (Strict Banned Chemical Interceptor)"
}
```

---

## 2. Speech-to-Text (Saaras ASR)

### `POST /api/stt`
Converts spoken farmer audio to text with regional dialect and code-mix handling.

#### Request Headers:
- `Content-Type: application/json`
- `api-subscription-key: <optional_key>`

#### Request Body:
```json
{
  "audio_base64": "<base64_wav_data>",
  "language_code": "kn-IN",
  "mode": "codemix"
}
```

#### Response:
```json
{
  "success": true,
  "transcript": "ನನ್ನ ಟೊಮೇಟೊ ಗಿಡಗಳ ಎಲೆಗಳು ಹಳದಿಯಾಗಿ ಮುದುಡಿಕೊಳ್ಳುತ್ತಿವೆ, ಇದಕ್ಕೆ ಏನು ಪರಿಹಾರ?",
  "language_code": "kn-IN",
  "mode": "codemix",
  "provider": "Sarvam Saaras ASR (Demo Calibration Mode)"
}
```

---

## 3. Text-to-Speech (Bulbul TTS)

### `POST /api/tts`
Synthesizes spoken audio in Indic languages with realistic regional prosody.

#### Request Body:
```json
{
  "text": "ರೈತ ಬಾಂಧವರೇ, ನಿಮ್ಮ ಬೆಳೆಗೆ ಬೇವಿನ ಎಣ್ಣೆ 3 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ.",
  "target_language_code": "kn-IN",
  "speaker": "bulbul:v1"
}
```

#### Response:
```json
{
  "success": true,
  "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEA...",
  "audio_format": "audio/wav",
  "duration_seconds": 3.2,
  "language": "kn-IN",
  "speaker": "bulbul:v1",
  "provider": "Sarvam Bulbul TTS (Calibrated Synthesizer)"
}
```

---

## 4. Grounded Agricultural Advisory (Sarvam-1 + ICAR RAG)

### `POST /api/chat`
Processes farmer queries using ICAR agronomic packages with strict deterministic safety guardrail validation.

#### Request Body:
```json
{
  "query": "ಟೊಮೇಟೊ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಚುಕ್ಕೆ ಮತ್ತು ಹಳದಿ ರೋಗಕ್ಕೆ ಏನು ಮಾಡಬೇಕು?",
  "language": "kn"
}
```

#### Response:
```json
{
  "query": "ಟೊಮೇಟೊ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಚುಕ್ಕೆ ಮತ್ತು ಹಳದಿ ರೋಗಕ್ಕೆ ಏನು ಮಾಡಬೇಕು?",
  "response": "ರೈತ ಬಾಂಧವರೇ, ನಿಮ್ಮ ಬೆಳೆಯ ಸಮಸ್ಯೆಗೆ ICAR ಮತ್ತು ಕೃಷಿ ವಿಶ್ವವಿದ್ಯಾಲಯ ಬೆಂಗಳೂರು (UASB) ಪರಿಹಾರ:\n\n🌿 **ಜೈವಿಕ ಪರಿಹಾರ:** ಬೇವಿನ ಎಣ್ಣೆ (1500 ppm) 3 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ.\n\n🧪 **ರಾಸಾಯನಿಕ ರಕ್ಷಣೆ:** ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP 2.0 ಗ್ರಾಂ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ.\n\n🛡️ **ಸುರಕ್ಷತಾ ಎಚ್ಚರಿಕೆ:** ಸಿಂಪಡಿಸುವಾಗ ಮುಖಗವಸು ಮತ್ತು ಕೈಗವಸು ಧರಿಸಿ.",
  "language": "kn",
  "detected_intent": "crop_advisory_icar",
  "crop": "Tomato",
  "guardrails": {
    "is_safe": true,
    "violations": [],
    "cautions": ["Approved agrochemical detected: Mancozeb 75% WP"],
    "safety_notice_present": true,
    "verified_by": "ICAR-Grounded AgriGuardrail Engine"
  },
  "citations": [
    {
      "document_id": "ICAR-UASB-TOMATO-2025-V2",
      "title": "Integrated Pest and Nutrient Management for Tomato in Kolar & Chikkaballapur Districts",
      "institution": "ICAR - National Institute of Agricultural Engineering and Technology & UAS Bangalore",
      "publication_date": "2025-01-15",
      "document_version": "v2.4",
      "source_url": "https://icar.org.in/crop-production/horticulture/tomato-kolar-package"
    }
  ]
}
```

---

## 5. Soil Health Card Intelligence

### `POST /api/soil-parse`
Parses physical government Soil Health Cards using Document Vision OCR and classifies N-P-K and pH metrics.

#### Request Body:
```json
{
  "filename": "soil_card.jpg"
}
```

#### Response:
```json
{
  "success": true,
  "filename": "soil_card.jpg",
  "provider": "Sarvam Document Vision (Indic OCR Pipeline)",
  "extracted_card": {
    "card_id": "SHC-KA-KOL-2026-8941",
    "farmer_name": "Basavarajappa (ಬಸವರಾಜಪ್ಪ)",
    "village": "Sugatur, Kolar Taluk",
    "district": "Kolar",
    "state": "Karnataka",
    "nitrogen_kg_ha": 198.5,
    "phosphorus_kg_ha": 9.2,
    "potassium_kg_ha": 152.0,
    "ph": 5.8,
    "organic_carbon_pct": 0.42,
    "extraction_confidence": 0.94,
    "confidence_ratings": {
      "nitrogen": 0.96,
      "phosphorus": 0.92,
      "potassium": 0.95,
      "ph": 0.98
    },
    "status": {
      "N": "Low (कम / ಕಡಿಮೆ)",
      "P": "Low (कम / ಕಡಿಮೆ)",
      "K": "Medium (मध्यम / ಮಧ್ಯಮ)",
      "pH": "Acidic (अम्लीय / ಆಮ್ಲೀಯ)"
    },
    "savings_estimate_inr": "₹3,400 - ₹5,200 per acre"
  }
}
```

### `POST /api/soil-evaluate`
Allows farmers to manually correct OCR values and recalculate status and remediation recommendations instantly.

#### Request Body:
```json
{
  "nitrogen": 310.0,
  "phosphorus": 14.5,
  "potassium": 190.0,
  "ph": 6.8
}
```

#### Response:
```json
{
  "success": true,
  "status": {
    "N": "Medium (मध्यम / ಮಧ್ಯಮ)",
    "P": "Medium (मध्यम / ಮಧ್ಯಮ)",
    "K": "Adequate (संतोषजनक / ತೃಪ್ತಿಕರ)",
    "pH": "Neutral (उदासीन / ತಟಸ್ಥ - ಅತ್ಯುತ್ತಮ)"
  },
  "recommendations_kn": [
    "ಸಾರಜನಕ ಮಟ್ಟ ಸಮತೋಲನದಲ್ಲಿದೆ. ಶಿಫಾರಸು ಮಾಡಿದ ಪ್ರಮಾಣವನ್ನು ಮುಂದುವರಿಸಿ.",
    "ರಂಜಕದ ಮಟ್ಟ ಸಾಮಾನ್ಯವಾಗಿದೆ.",
    "ಪೊಟ್ಯಾಷ್ ಮಟ್ಟ ತೃಪ್ತಿಕರವಾಗಿದೆ.",
    "ಮಣ್ಣಿನ pH ಆದರ್ಶ ಮಟ್ಟದಲ್ಲಿದೆ. ಪೋಷಕಾಂಶಗಳ ಹೀರಿಕೊಳ್ಳುವಿಕೆ ಅತ್ಯುತ್ತಮವಾಗಿರುತ್ತದೆ."
  ]
}
```

---

## 6. APMC Mandi Market Rates

### `GET /api/mandi`
Returns modal, minimum, and maximum commodity rates across Karnataka and National APMC yards.

#### Parameters:
- `commodity`: (Optional) Filter by commodity name (e.g. `tomato`, `onion`, `cotton`).
- `live`: (Optional) `true` or `false`.

#### Response:
```json
{
  "mandis": [
    {
      "market": "Kolar APMC Mandi",
      "district": "Kolar",
      "state": "Karnataka",
      "commodity": "Tomato (ಟೊಮೇಟೊ)",
      "variety": "Hybrid Grade A",
      "unit": "₹ / Quintal",
      "min_price": 1400.0,
      "max_price": 1950.0,
      "modal_price": 1750.0,
      "date": "2026-11-08",
      "timestamp": "2026-11-08 23:25 IST",
      "data_source_mode": "DEMO",
      "source_note": "Karnataka State Agricultural Marketing Board (KSAMB) daily bulletin"
    }
  ],
  "count": 1
}
```

---

## 7. Weather & Spray Advisory

### `GET /api/weather`
Returns 3-day agricultural forecast with IMD wind and precipitation spray advisories.

#### Parameters:
- `location`: (Optional) Location string (defaults to `Kolar District, Karnataka`).

#### Response:
```json
{
  "location": "Kolar District, Karnataka",
  "agro_climatic_zone": "Eastern Dry Zone (Zone-5), Karnataka",
  "source": "IMD District Agro-Met Unit (DAMU) & ICAR Advisory Bulletin",
  "forecast": [
    {
      "day": "Today (ಇಂದು / आज)",
      "temp": "30°C",
      "humidity": "58%",
      "condition": "Partly Sunny (ಭಾಗಶಃ ಬಿಸಿಲು)",
      "rain_chance": "10%",
      "wind_kmh": 9,
      "is_spray_safe": true,
      "spray_advisory": "Safe to spray foliar nutrients and bio-pesticides between 7:00 AM - 10:30 AM."
    }
  ]
}
```

---

## 8. 1800-KISAN-AI Telephony IVR

### `POST /api/telephony`
Routes simulated keypad phone DTMF keypresses to agricultural subsystems and outputs spoken voice prompts.

#### Request Body:
```json
{
  "digit": "2",
  "language": "kn"
}
```

#### Response:
```json
{
  "digit": "2",
  "menu": "Mandi Rates",
  "speech_response": "ಇಂದಿನ ಕೋಲಾರ ಎಪಿಎಂಸಿ ಮಂಡಿಯಲ್ಲಿ ಟೊಮೇಟೊ ಸರಾಸರಿ ದರ ಕ್ವಿಂಟಾಲ್‌ಗೆ 1750 ರೂಪಾಯಿಗಳು.",
  "status": "completed"
}
```

---

## 9. Safety Audit Log & Provenance

### `GET /api/audit-log`
Returns real-time records of all blocked hazardous queries and intercepted banned substances.

### `GET /api/provenance`
Returns verified ICAR agronomic packages, source URLs, and CIBRC statutory reference citations.

