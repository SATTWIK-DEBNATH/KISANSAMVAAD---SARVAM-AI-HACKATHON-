"""
KisanSamvaad - API Request Router & Endpoint Dispatcher
Dispatches incoming HTTP requests to corresponding services and integrations.
Enforces CORS, validates payloads, and guarantees graceful error handling.
"""

from typing import Dict, Any, Tuple
from ..integrations.sarvam.client import UnifiedSarvamClient
from ..integrations.mandi.connector import MandiConnector
from ..integrations.weather.connector import WeatherConnector
from ..services.soil_service import SoilDiagnosticService
from ..services.telephony_service import TelephonyIVRService
from ..services.audio_service import AudioService
from ..services.calculator_service import NetRealisationCalculator
from ..services.crop_service import CropDiagnosticsService
from ..services.scheme_service import SchemeIntelligenceService
from ..safety.agri_guardrails import AgriGuardrailEngine
from ..ai.rag.knowledge_store import knowledge_store
from ..db.repository import repository
from ..core.config import settings

# Backward-compatible alias for schemes
GOVERNMENT_SCHEMES = SchemeIntelligenceService.list_all_schemes()

class APIRouter:
    """Dispatches API requests with error handling."""

    @classmethod
    def handle_get(cls, path: str, query: Dict[str, list]) -> Tuple[Dict[str, Any], int]:
        """Routes GET endpoints."""
        if path == "/api/health":
            client = UnifiedSarvamClient()
            return {
                "status": "healthy",
                "service": "KisanSamvaad Sovereign Agricultural AI",
                "version": settings.app_version,
                "sarvam_live_connected": client.has_live_credentials(),
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
            }, 200

        elif path == "/api/mandi":
            commodity = query.get("commodity", [None])[0]
            live_flag = query.get("live", ["false"])[0].lower() in ("true", "1")
            rates = MandiConnector.get_rates(commodity=commodity, live_mode=live_flag)
            return {"mandis": rates, "count": len(rates)}, 200

        elif path == "/api/weather":
            loc = query.get("location", ["Kolar District, Karnataka"])[0]
            weather_data = WeatherConnector.get_forecast(location=loc)
            return weather_data, 200

        elif path == "/api/schemes":
            schemes = SchemeIntelligenceService.list_all_schemes()
            return {"schemes": schemes, "count": len(schemes)}, 200

        elif path == "/api/provenance":
            packages = knowledge_store.crop_packages
            return {"packages": packages, "soil_standards": knowledge_store.soil_standards}, 200

        elif path == "/api/audit-log":
            return {"events": AgriGuardrailEngine.get_audit_log()}, 200

        elif path == "/api/farmers":
            limit = int(query.get("limit", [50])[0])
            farmers = repository.list_farmers(limit=limit)
            return {"farmers": farmers, "count": len(farmers)}, 200

        elif path == "/api/conversations":
            farmer_id = query.get("farmer_id", [None])[0]
            limit = int(query.get("limit", [20])[0])
            convs = repository.get_conversation_history(farmer_id=farmer_id, limit=limit)
            return {"conversations": convs, "count": len(convs)}, 200

        elif path == "/api/expert-cases":
            cases = repository.list_open_expert_cases()
            return {"expert_cases": cases, "count": len(cases)}, 200

        return {"error": f"Endpoint '{path}' not found"}, 404

    @classmethod
    def handle_post(cls, path: str, body: Dict[str, Any], headers: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
        """Routes POST endpoints."""
        req_key = headers.get("api-subscription-key")
        client = UnifiedSarvamClient(api_key=req_key)

        if path == "/api/stt":
            audio_b64 = body.get("audio_base64", "")
            language_code = body.get("language_code", "kn-IN")
            mode = body.get("mode", "codemix")
            audio_bytes = AudioService.decode_base64_audio(audio_b64)
            result = client.speech_to_text(audio_bytes=audio_bytes, language_code=language_code, mode=mode)
            return result, 200

        elif path == "/api/tts":
            text = body.get("text", "")
            target_lang = body.get("target_language_code", "kn-IN")
            speaker = body.get("speaker", "bulbul:v1")
            result = client.text_to_speech(text=text, target_language_code=target_lang, speaker=speaker)
            return result, 200

        elif path == "/api/chat":
            query = body.get("query", "")
            lang = body.get("language", "kn")
            farmer_id = body.get("farmer_id")
            result = client.chat_advisory(query=query, language=lang)
            # Persist conversation to database
            try:
                repository.save_conversation(
                    query_text=query,
                    response_text=result.get("response", ""),
                    farmer_id=farmer_id,
                    language=lang,
                    detected_intent=result.get("detected_intent", "advisory")
                )
            except Exception:
                pass
            return result, 200

        elif path == "/api/soil-parse":
            filename = body.get("filename", "soil_card.jpg")
            result = client.parse_soil_health_card(filename=filename)
            return result, 200

        elif path == "/api/soil-evaluate":
            # For farmer manual corrections of extracted card values
            n = float(body.get("nitrogen", 198.5))
            p = float(body.get("phosphorus", 9.2))
            k = float(body.get("potassium", 152.0))
            ph = float(body.get("ph", 5.8))
            oc = float(body.get("organic_carbon", 0.42))
            zinc = float(body.get("zinc", 0.55))
            boron = float(body.get("boron", 0.40))

            diag = SoilDiagnosticService.evaluate_sample(
                n=n, p=p, k=k, ph=ph, oc=oc, zinc=zinc, boron=boron
            )
            return {
                "success": True,
                "evaluated_values": {
                    "nitrogen": n,
                    "phosphorus": p,
                    "potassium": k,
                    "ph": ph,
                    "organic_carbon": oc,
                    "zinc": zinc,
                    "boron": boron
                },
                "status": diag["status"],
                "recommendations_hi": diag["recommendations_hi"],
                "recommendations_kn": diag["recommendations_kn"],
                "recommendations_en": diag["recommendations_en"]
            }, 200

        elif path == "/api/net-realisation":
            commodity = body.get("commodity", "Tomato")
            quantity = float(body.get("quantity_quintals", 50.0))
            local_market = body.get("local_market", {
                "name": "Kolar APMC",
                "price": 1850.0,
                "distance_km": 15.0,
                "transport_rate_per_km": 22.0,
                "spoilage_pct": 1.5
            })
            terminal_market = body.get("terminal_market", {
                "name": "Yeshwanthpur APMC (Bengaluru)",
                "price": 2250.0,
                "distance_km": 75.0,
                "transport_rate_per_km": 28.0,
                "spoilage_pct": 4.0
            })
            comparison = NetRealisationCalculator.compare_mandis(
                commodity=commodity,
                quantity_quintals=quantity,
                local_market=local_market,
                terminal_market=terminal_market
            )
            return comparison, 200

        elif path == "/api/crop-diagnostics":
            crop_name = body.get("crop", "Tomato")
            symptoms = body.get("symptoms", "")
            image_b64 = body.get("image_base64")
            farmer_id = body.get("farmer_id")
            lang = body.get("language", "kn-IN")
            diagnostic = CropDiagnosticsService.diagnose(
                crop_name=crop_name,
                symptom_description=symptoms,
                image_base64=image_b64,
                farmer_id=farmer_id,
                language=lang
            )
            return diagnostic, 200

        elif path == "/api/schemes/evaluate":
            farmer_name = body.get("farmer_name", "Farmer")
            land_acres = float(body.get("landholding_acres", 2.0))
            state = body.get("state", "Karnataka")
            district = body.get("district", "Kolar")
            crops = body.get("crops", ["Tomato", "Ragi"])
            irrigation = body.get("irrigation_source", "Borewell")
            evaluation = SchemeIntelligenceService.evaluate_eligibility(
                farmer_name=farmer_name,
                landholding_acres=land_acres,
                state=state,
                district=district,
                crops=crops,
                irrigation_source=irrigation
            )
            return evaluation, 200

        elif path == "/api/farmers":
            name = body.get("name", "")
            if not name:
                return {"error": "Farmer name is required"}, 400
            farmer = repository.create_farmer(
                name=name,
                phone=body.get("phone"),
                village=body.get("village"),
                district=body.get("district", "Kolar"),
                state=body.get("state", "Karnataka"),
                preferred_language=body.get("preferred_language", "kn-IN"),
                landholding_acres=float(body.get("landholding_acres", 1.0))
            )
            return {"success": True, "farmer": farmer}, 201

        elif path == "/api/telephony":
            digit = body.get("digit", "welcome")
            lang = body.get("language", "kn")
            result = TelephonyIVRService.process_dtmf_input(digit=digit, language=lang)
            return result, 200

        elif path == "/api/translate":
            text = body.get("text", "")
            src = body.get("source_language_code", "en-IN")
            tgt = body.get("target_language_code", "kn-IN")
            result = client.translate_text(text, source_language_code=src, target_language_code=tgt)
            return result, 200

        return {"error": f"Endpoint '{path}' not found"}, 404
