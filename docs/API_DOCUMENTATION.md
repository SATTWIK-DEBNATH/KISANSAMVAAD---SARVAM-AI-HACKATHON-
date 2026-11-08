# KisanSamvaad - REST API Specification & Integration Contracts
## Sovereign Indic Voice and Document AI for Indian Agriculture

Base URL: `http://127.0.0.1:8000`  
Protocol: HTTP/1.1 JSON UTF-8  
CORS: Full Cross-Origin Access Enabled (`Access-Control-Allow-Origin: *`)  
Version: 2.4.0  

---

## 1. Global Response Standards and Error Envelopes

All endpoints return JSON responses. Successful operations return HTTP status codes `200` (OK) or `201` (Created). Errors return appropriate 4xx/5xx status codes with the following standard error schema:

```json
{
  "error": "Descriptive human-readable error message",
  "error_code": "RESOURCE_NOT_FOUND",
  "details": {}
}
```

Authentication:
Endpoints communicate with Sarvam AI when the optional request header `api-subscription-key` or the server environment variable `SARVAM_API_KEY` is present. If absent, endpoints seamlessly operate in calibrated ICAR agronomic simulation mode.

---

## 2. Endpoint Index

| Method | Endpoint | Description | Primary Module |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | System health, model versions, language discovery | Core |
| `POST` | `/api/stt` | Speech-to-text (Saaras ASR with code-mix support) | Suno & Bolo |
| `POST` | `/api/tts` | Text-to-speech (Bulbul TTS Indic prosody) | Suno & Bolo |
| `POST` | `/api/chat` | Agricultural reasoning (Sarvam-1 LLM + ICAR RAG) | Advisory |
| `POST` | `/api/soil-parse` | Physical Soil Health Card OCR extraction | Soil Doctor |
| `POST` | `/api/soil-evaluate` | Recalculate soil deficiency remediation | Soil Doctor |
| `GET` | `/api/mandi` | APMC commodity market rates & freshness | Market Intel |
| `POST` | `/api/net-realisation`| Calculate net profit comparing local vs terminal mandis | Economics |
| `GET` | `/api/weather` | 3-day forecast with chemical spray safety window | Spray Advisory |
| `POST` | `/api/crop-diagnostics`| Multimodal symptom differential diagnosis & KVK escalation | Crop Doctor |
| `GET` | `/api/schemes` | Complete catalog of central and state agricultural schemes | Schemes |
| `POST` | `/api/schemes/evaluate`| Personalized farmer scheme eligibility & document checklist | Schemes |
| `GET` | `/api/farmers` | List registered farmer profiles | Persistence |
| `POST` | `/api/farmers` | Register new farmer profile in SQLite database | Persistence |
| `GET` | `/api/conversations` | Retrieve farmer voice/chat consultation history | Persistence |
| `GET` | `/api/expert-cases` | Retrieve open cases escalated to KVK extension scientists | Persistence |
| `POST` | `/api/telephony` | 1800-IVR DTMF state machine processor | Telephony |
| `GET` | `/api/provenance` | Verified ICAR research documents and citations | Provenance |
| `GET` | `/api/audit-log` | Safety interceptor audit events log | Governance |

---

## 3. Detailed Endpoint Contracts

### 3.1 `GET /api/health`
Checks server status, model versions, live credential status, and supported languages.

#### Response (HTTP 200):
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
    {"code": "bn-IN", "name": "Bengali (বাংলা)"},
    {"code": "mr-IN", "name": "Marathi (मराठी)"},
    {"code": "pa-IN", "name": "Punjabi (ਪੰਜਾਬੀ)"},
    {"code": "gu-IN", "name": "Gujarati (ગુજરાતી)"},
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

### 3.2 `POST /api/stt`
Converts farmer spoken audio to text with regional dialect and code-mix handling.

#### Request Body:
```json
{
  "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEA...",
  "language_code": "kn-IN",
  "mode": "codemix"
}
```

#### Response (HTTP 200):
```json
{
  "success": true,
  "transcript": "ನನ್ನ ಟೊಮೇಟೊ ಗಿಡಗಳಲ್ಲಿ ಎಲೆಗಳು ಮುದುಡುತ್ತಿವೆ, ಏನು ಮಾಡಬೇಕು?",
  "language_code": "kn-IN",
  "mode": "codemix",
  "provider": "Sarvam Saaras ASR (Calibrated Indic Model)"
}
```

---

### 3.3 `POST /api/tts`
Synthesizes natural Indic speech with authentic regional prosody.

#### Request Body:
```json
{
  "text": "ಬೇವಿನ ಎಣ್ಣೆ 3 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ.",
  "target_language_code": "kn-IN",
  "speaker": "bulbul:v1"
}
```

#### Response (HTTP 200):
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

### 3.4 `POST /api/chat`
Processes farmer agricultural questions through ICAR RAG knowledge packages, invokes Sarvam-1 LLM, enforces CIBRC safety guardrails, and persists the dialogue.

#### Request Body:
```json
{
  "query": "How to control leaf curl virus in tomato?",
  "language": "kn",
  "farmer_id": "FRM_12345678"
}
```

#### Response (HTTP 200):
```json
{
  "query": "How to control leaf curl virus in tomato?",
  "response": "ಟೊಮೇಟೊ ಎಲೆ ಮುದುಡು ರೋಗ (Leaf Curl Virus) ಬಿಳಿ ನೊಣಗಳಿಂದ ಬರುತ್ತದೆ. ನಿಯಂತ್ರಣಕ್ಕೆ ಹಳದಿ ಅಂಟು ಬಲೆಗಳನ್ನು ಅಳವಡಿಸಿ. ಅಗತ್ಯವಿದ್ದರೆ ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 0.3 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಸಿಂಪಡಿಸಿ. (ಗರಿಷ್ಠ 0.5 ಮಿ.ಲೀ ಮೀರಬಾರದು).",
  "language": "kn",
  "detected_intent": "pest_disease_advisory",
  "crop": "Tomato",
  "guardrails": {
    "is_safe": true,
    "violations": [],
    "cautions": ["Dosage verified under ICAR threshold: Imidacloprid <= 0.5 ml/L"]
  },
  "citations": [
    {
      "document_id": "ICAR-UASB-TOMATO-2025-V2",
      "title": "Package of Practices for Commercial Solanaceous Crops",
      "institution": "University of Agricultural Sciences, Bangalore (UASB)",
      "publication_date": "January 2025"
    }
  ]
}
```

---

### 3.5 `POST /api/soil-parse`
Parses physical paper Soil Health Cards using Document Vision OCR.

#### Request Body:
```json
{
  "filename": "soil_card_sample.jpg",
  "image_base64": "<optional_base64>"
}
```

#### Response (HTTP 200):
```json
{
  "card_id": "KA-KOL-2026-8912",
  "farmer_name": "ಮಂಜುನಾಥ್ (Manjunath)",
  "village": "ಸುಗಟೂರು (Sugatur)",
  "district": "ಕೋಲಾರ (Kolar)",
  "state": "Karnataka",
  "nitrogen_kg_ha": 198.5,
  "phosphorus_kg_ha": 9.2,
  "potassium_kg_ha": 152.0,
  "ph": 5.8,
  "organic_carbon_pct": 0.42,
  "zinc_ppm": 0.55,
  "boron_ppm": 0.40,
  "extraction_confidence": 0.94,
  "confidence_ratings": {
    "nitrogen": 0.96,
    "phosphorus": 0.92,
    "potassium": 0.95,
    "ph": 0.98,
    "organic_carbon": 0.91,
    "zinc": 0.89,
    "boron": 0.87
  },
  "status": {
    "nitrogen": "Low (< 280 kg/ha)",
    "phosphorus": "Low (< 10 kg/ha)",
    "potassium": "Medium (140 - 280 kg/ha)",
    "ph": "Acidic (< 6.5)",
    "organic_carbon": "Low (< 0.5%)"
  },
  "recommendations_kn": [
    "ಆಮ್ಲೀಯ ಮಣ್ಣು (pH 5.8): ಪ್ರತಿ ಎಕರೆಗೆ 250 ಕೆಜಿ ಕೃಷಿ ಸುಣ್ಣ (Agricultural Lime) ಸೇರಿಸಿ.",
    "ಸಾರಜನಕ ಕೊರತೆ: ಎಕರೆಗೆ 5 ಟನ್ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಮತ್ತು ಯೂರಿಯಾವನ್ನು 2 ಕಂತುಗಳಲ್ಲಿ ನೀಡಿ."
  ],
  "savings_estimate_inr": "₹3,200 - ₹4,800 per acre"
}
```

---

### 3.6 `POST /api/net-realisation`
Determines whether selling at a local APMC or a distant terminal mandi generates higher take-home profit after accounting for fuel, transport, loading labor, APMC fees, packaging, and transit spoilage.

#### Request Body:
```json
{
  "commodity": "Tomato",
  "quantity_quintals": 50.0,
  "local_market": {
    "name": "Kolar APMC",
    "price": 1850.0,
    "distance_km": 15.0,
    "transport_rate_per_km": 22.0,
    "spoilage_pct": 1.5
  },
  "terminal_market": {
    "name": "Yeshwanthpur APMC (Bengaluru)",
    "price": 2250.0,
    "distance_km": 75.0,
    "transport_rate_per_km": 28.0,
    "spoilage_pct": 4.0
  }
}
```

#### Response (HTTP 200):
```json
{
  "commodity": "Tomato",
  "quantity_quintals": 50.0,
  "local_market": {
    "market_name": "Kolar APMC",
    "gross_sale_inr": 92500.0,
    "distance_km": 15.0,
    "itemized_deductions": {
      "transport_cost_inr": 330.0,
      "loading_labor_inr": 1500.0,
      "mandi_fee_commission_inr": 1850.0,
      "packaging_cost_inr": 2000.0,
      "spoilage_loss_inr": 1387.5,
      "total_deductions_inr": 7067.5
    },
    "net_realisation_inr": 85432.5,
    "net_rate_per_quintal_inr": 1708.65,
    "deduction_share_pct": 7.6
  },
  "terminal_market": {
    "market_name": "Yeshwanthpur APMC (Bengaluru)",
    "gross_sale_inr": 112500.0,
    "distance_km": 75.0,
    "itemized_deductions": {
      "transport_cost_inr": 2100.0,
      "loading_labor_inr": 1500.0,
      "mandi_fee_commission_inr": 2250.0,
      "packaging_cost_inr": 2000.0,
      "spoilage_loss_inr": 4500.0,
      "total_deductions_inr": 12350.0
    },
    "net_realisation_inr": 100150.0,
    "net_rate_per_quintal_inr": 2003.0,
    "deduction_share_pct": 11.0
  },
  "net_difference_inr": 14717.5,
  "percentage_gain": 17.2,
  "recommended_market": "Yeshwanthpur APMC (Bengaluru)",
  "recommendation_en": "Selling at Yeshwanthpur APMC (Bengaluru) yields ₹14,718 (+17.2%) more net profit after factoring in transit fuel and spoilage.",
  "recommendation_kn": "Yeshwanthpur APMC (Bengaluru) ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಮಾರಾಟ ಮಾಡುವುದರಿಂದ ಸಾರಿಗೆ ಮತ್ತು ಸಾಗಾಣಿಕೆ ವೆಚ್ಚ ಕಳೆದು ನಿಮಗೆ ಹೆಚ್ಚುವರಿಯಾಗಿ ₹14,718 (+17.2%) ನಿವ್ವಳ ಲಾಭ ದೊರೆಯುತ್ತದೆ."
}
```

---

### 3.7 `POST /api/crop-diagnostics`
Evaluates crop pathology from symptoms and photographs. Emits differential diagnoses, experimental bounds, verified treatments, and automatic KVK escalation tickets.

#### Request Body:
```json
{
  "crop": "Tomato",
  "symptoms": "Lower leaves show concentric brown target spots with yellow halos",
  "language": "kn-IN"
}
```

#### Response (HTTP 200):
```json
{
  "experimental": true,
  "disclaimer": "Experimental AI Diagnostic Aid grounded in ICAR protocols. Verify physically with local KVK before chemical application.",
  "crop": "Tomato",
  "primary_diagnosis": {
    "disease_name": "Tomato Early Blight",
    "pathogen": "Alternaria solani",
    "confidence_score": 0.88,
    "severity_level": "Moderate"
  },
  "differential_diagnosis": {
    "secondary_suspect": "Septoria Leaf Spot (Septoria lycopersici)",
    "confidence_score": 0.52
  },
  "recommended_interventions": {
    "organic_biological": "Spray Neem Oil (Azadirachtin 1500 ppm) 3ml/L of water or apply Trichoderma harzianum 5g/L.",
    "approved_chemical": "Spray Mancozeb 75% WP @ 2.0g to 2.5g per liter of water. Ensure thorough coverage of lower foliage.",
    "cultural_management": "Remove and burn severely infected lower leaves. Practice 3-year crop rotation without solanaceous crops."
  },
  "safety_guardrails": {
    "is_safe": true,
    "violations": [],
    "cautions": []
  },
  "escalate_to_kvk": false,
  "kvk_escalation_details": null,
  "advisory_localized": {
    "kn": "ಟೊಮೇಟೊ ಮುಂಚಿನ ಎಲೆ ಅಂಗಮಾರಿ ರೋಗ (Early Blight). ಕೆಳಗಿನ ಎಲೆಗಳಲ್ಲಿ ವೃತ್ತಾಕಾರದ ಕಂದು ಚುಕ್ಕೆಗಳು ಕಾಣಿಸುತ್ತವೆ. ಬೇವಿನ ಎಣ್ಣೆ 3 ಮಿ.ಲೀ ಅಥವಾ ಮ್ಯಾಂಕೋಜೆಬ್ 2.0 ಗ್ರಾಂ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ."
  }
}
```

---

### 3.8 `POST /api/schemes/evaluate`
Performs personalized eligibility evaluation against central and state agricultural schemes.

#### Request Body:
```json
{
  "farmer_name": "Basavaraj Gowda",
  "landholding_acres": 3.0,
  "state": "Karnataka",
  "district": "Kolar",
  "crops": ["Ragi", "Tomato"],
  "irrigation_source": "Borewell"
}
```

#### Response (HTTP 200):
```json
{
  "farmer_name": "Basavaraj Gowda",
  "evaluated_parameters": {
    "landholding_acres": 3.0,
    "state": "Karnataka",
    "district": "Kolar",
    "crops": ["Ragi", "Tomato"],
    "irrigation_source": "Borewell"
  },
  "eligible_schemes_count": 5,
  "total_schemes_reviewed": 6,
  "scheme_evaluations": [
    {
      "scheme_id": "raita_siri",
      "scheme_name": "Karnataka Raita Siri Scheme (Millet Incentive)",
      "eligibility_status": "Eligible",
      "benefit_summary": "Direct incentive of ₹10,000 per hectare (up to 2 hectares / ₹20,000) for cultivating notified millets (Ragi, Jowar, Bajra).",
      "portal_url": "https://raitamitra.karnataka.gov.in",
      "required_documents": [
        "Karnataka Pahani / RTC showing millet cultivation",
        "FID (Farmer Identification Number) from FRUITS portal",
        "Aadhaar-linked Bank Account"
      ]
    },
    {
      "scheme_id": "pm_kisan",
      "scheme_name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
      "eligibility_status": "Eligible",
      "benefit_summary": "₹6,000 per year transferred directly to bank accounts in 3 equal installments of ₹2,000.",
      "portal_url": "https://pmkisan.gov.in",
      "required_documents": [
        "Aadhaar Card linked with active bank account",
        "Land Record (Pahani / RTC / Khatauni)"
      ]
    }
  ]
}
```

---

### 3.9 Persistence Endpoints (`/api/farmers`, `/api/conversations`, `/api/expert-cases`)

#### `POST /api/farmers`
Registers a new farmer in SQLite.
```json
// Request
{
  "name": "Suresh Patel",
  "phone": "9876543210",
  "village": "Vokkaleri",
  "district": "Kolar",
  "landholding_acres": 2.5
}

// Response (HTTP 201)
{
  "success": true,
  "farmer": {
    "id": "FRM_A1B2C3D4",
    "name": "Suresh Patel",
    "village": "Vokkaleri",
    "district": "Kolar",
    "created_at": "2026-11-09T02:00:00Z"
  }
}
```

#### `GET /api/conversations?farmer_id=FRM_A1B2C3D4`
Returns past consultation dialogue history with timestamps and detected intents.

#### `GET /api/expert-cases`
Lists open cases flagged for human-in-the-loop review by KVK extension scientists.

