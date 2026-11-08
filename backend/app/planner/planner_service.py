"""
KisanSamvaad - Soil-to-Rupee Planner Service Orchestrator
Coordinates unit conversion, nutrient calculation, whole-bag optimization,
weather verification, localized narration, and deterministic safety checks.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone

from .schemas import PlanRequest, PlanResult, ValidationError
from .conversion import UnitConverter
from .requirements import RequirementsCalculator
from .optimizer import FertilizerOptimizer
from .schedule import TimingScheduleBuilder
from .narration import NarrationRenderer
from ..safety.agri_guardrails import AgriGuardrailEngine
from ..integrations.sarvam.client import UnifiedSarvamClient

class SoilPlannerService:
    """End-to-end service generating the Soil-to-Rupee fertilizer plan."""

    @classmethod
    def generate_plan(cls, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the Soil-to-Rupee pipeline.
        Returns serialized PlanResult dictionary.
        """
        # Step 1: Input Validation
        request = PlanRequest.from_dict(request_data)

        # Step 2: Unit Conversion to Hectares
        area_ha = UnitConverter.to_hectares(
            area=request.area,
            unit=request.unit,
            state=request.state
        )

        # Step 3: Nutrient Requirements & Soil Classification
        req_analysis = RequirementsCalculator.calculate_targets(
            crop=request.crop,
            area_hectares=area_ha,
            soil=request.soil_values,
            card_recommendations=request.card_recommendations
        )

        target_n = req_analysis["target_nutrients_kg"]["nitrogen_kg"]
        target_p = req_analysis["target_nutrients_kg"]["phosphorus_p2o5_kg"]
        target_k = req_analysis["target_nutrients_kg"]["potassium_k2o_kg"]

        # Step 4: Discrete Whole-Bag Optimization
        opt_result = FertilizerOptimizer.optimize(
            target_n_kg=target_n,
            target_p2o5_kg=target_p,
            target_k2o_kg=target_k
        )

        # Step 5: Weather Verification (Open-Meteo with fallback)
        lat = request.location.lat if request.location else 13.1367
        lon = request.location.lon if request.location else 78.1348
        weather_info = TimingScheduleBuilder.check_open_meteo_weather(lat=lat, lon=lon)

        # Step 6: Split Timing Schedule
        schedule = TimingScheduleBuilder.build_schedule(
            crop=request.crop,
            allocated_bags=opt_result.get("bags", []),
            weather_warning=weather_info
        )

        # Step 7: Localized Spoken Narration
        raw_narration = NarrationRenderer.render_template(
            crop=req_analysis["crop_name"],
            area=request.area,
            unit=request.unit,
            bags=opt_result.get("bags", []),
            total_cost_inr=opt_result.get("total_cost_inr", 0.0),
            delay_recommended=weather_info.get("delay_recommended", False),
            language=request.language
        )

        # Step 8: Safety Guardrail Enforcement (Fail-closed check)
        guardrail_result = AgriGuardrailEngine.validate_recommendation(raw_narration)
        if not guardrail_result["is_safe"]:
            raw_narration = "⚠️ Notice: Advisory filtered by safety guardrails. Consult local KVK agronomist."

        # Step 9: Speech Synthesis (Sarvam Bulbul TTS / Calibrated Synth)
        sarvam_client = UnifiedSarvamClient()
        lang_code = f"{request.language}-IN" if "-" not in request.language else request.language
        if lang_code.startswith("en"):
            lang_code = "en-IN"
        elif lang_code.startswith("kn"):
            lang_code = "kn-IN"
        elif lang_code.startswith("hi"):
            lang_code = "hi-IN"
        elif lang_code.startswith("ta"):
            lang_code = "ta-IN"

        tts_result = sarvam_client.text_to_speech(
            text=raw_narration,
            target_language_code=lang_code,
            speaker="bulbul:v1"
        )

        now_iso = datetime.now(timezone.utc).isoformat()

        # Step 10: Assemble Typed PlanResult
        plan_result = PlanResult(
            inputs_echo={
                "crop": request.crop,
                "crop_display_name": req_analysis["crop_name"],
                "area_entered": request.area,
                "unit_entered": request.unit,
                "area_hectares": req_analysis["area_hectares"],
                "state": request.state,
                "soil_ratings": req_analysis["soil_ratings"],
                "ph_classification": req_analysis["ph_classification"],
                "ph_advisory_note": req_analysis["ph_advisory_note"],
                "data_source": req_analysis["source"]
            },
            nutrient_requirements_kg=req_analysis["target_nutrients_kg"],
            fertilizer_plan=opt_result,
            organic_alternative=req_analysis["organic_alternative"] if request.include_organic_alternative else None,
            timing_schedule=schedule,
            weather_warning=weather_info,
            citations=[req_analysis["citation"]] if req_analysis.get("citation") else [],
            spoken_narration={
                "text": raw_narration,
                "audio_base64": tts_result.get("audio_base64", ""),
                "audio_format": tts_result.get("audio_format", "audio/wav"),
                "duration_seconds": tts_result.get("duration_seconds", 3.0),
                "language": request.language,
                "provider": tts_result.get("provider", "Sarvam Bulbul TTS")
            },
            metadata={
                "timestamp": now_iso,
                "price_version_date": "2026-11-01",
                "engine": "KisanSamvaad Soil-to-Rupee Integer Optimizer v2.4",
                "disclaimer": "Confirm with your local KVK or agricultural officer before applying chemical fertilizers."
            }
        )

        return plan_result.to_dict()
