"""
KisanSamvaad - Backend Automated Test Suite
Verifies:
1. ICAR AgriGuardrail safety checks (banned pesticide detection, excessive dosage flagging, safety disclaimers).
2. Soil Health Card diagnostic logic (NPK classification & pH remediation).
3. SarvamClient unified API operations (Saaras STT, Bulbul TTS audio synthesis, Sarvam-1 reasoning, Document Vision).
"""

import sys
import os

# Ensure backend imports work
sys.path.insert(0, os.path.dirname(__file__))

from agri_guardrails import AgriGuardrailEngine, APPROVED_AGROCHEMICALS, BANNED_SUBSTANCES
from knowledge_base import diagnose_soil_sample, CROP_DISEASES, MANDI_PRICES
from sarvam_client import SarvamClient

def test_guardrails_banned_chemicals():
    print("Test 1: Guardrails - Banned Chemical Interception...")
    hazardous_query = "Spray Endosulfan and Monocrotophos to kill bollworms fast."
    result = AgriGuardrailEngine.validate_recommendation(hazardous_query)
    assert not result["is_safe"], "Failed: Banned chemical was not caught!"
    assert any("ENDOSULFAN" in v for v in result["violations"]), "Endosulfan violation missing"
    assert any("MONOCROTOPHOS" in v for v in result["violations"]), "Monocrotophos violation missing"
    print("  -> PASSED: Banned substances successfully intercepted.")

def test_guardrails_dosage_bounds():
    print("Test 2: Guardrails - Agrochemical Dosage Bounds...")
    # Safe dosage
    safe_rec = "Spray Imidacloprid 0.3 ml per liter of water during early morning with gloves."
    safe_result = AgriGuardrailEngine.validate_recommendation(safe_rec)
    assert safe_result["is_safe"], "Failed: Safe recommendation flagged incorrectly"
    
    # Toxic overdose
    lethal_rec = "Mix Imidacloprid 15 ml per liter of water for immediate effect."
    unsafe_result = AgriGuardrailEngine.validate_recommendation(lethal_rec)
    assert not unsafe_result["is_safe"], "Failed: 30x lethal dosage was not intercepted!"
    print("  -> PASSED: Dosage threshold verification confirmed.")

def test_soil_health_diagnostic():
    print("Test 3: Soil Health Card Diagnostic Engine...")
    diagnosis = diagnose_soil_sample(n=195.0, p=8.4, k=145.0, ph=5.8)
    assert diagnosis["status"]["N"] == "Low (कम)", "Nitrogen diagnosis mismatch"
    assert diagnosis["status"]["P"] == "Low (कम)", "Phosphorus diagnosis mismatch"
    assert diagnosis["status"]["pH"] == "Acidic (अम्लीय)", "pH acidity mismatch"
    assert any("चूना" in r for r in diagnosis["recommendations_hi"]), "Lime remediation missing for acidic soil"
    print("  -> PASSED: Soil NPK & pH diagnostics matched ICAR guidelines.")

def test_sarvam_client_services():
    print("Test 4: Sarvam Client Unified Operations...")
    client = SarvamClient()
    
    # STT Test
    stt = client.speech_to_text(b"mock_audio", language_code="hi-IN", mode="codemix")
    assert stt["success"] and len(stt["transcript"]) > 0, "STT transcript empty"
    
    # TTS Test
    tts = client.text_to_speech("किसान भाई, अपनी फसल का ध्यान रखें।", target_language_code="hi-IN")
    assert tts["success"] and len(tts["audio_base64"]) > 50, "TTS audio synthesis failed"
    
    # Chat RAG Test
    chat = client.chat_advisory("कपास में पत्तियां पीली हो रही हैं", language="hi")
    assert "मैग्नीशियम" in chat["response"] or "इमिडाक्लोप्रिड" in chat["response"], "Agronomic advisory missing"
    assert chat["guardrails"]["is_safe"], "Legitimate advisory flagged as unsafe"
    
    # Document Parse Test
    doc = client.parse_soil_health_card()
    assert doc["success"] and doc["extracted_card"]["nitrogen_kg_ha"] > 0, "Document parse failed"
    
    # Mayura Translation Test
    trans = client.translate_text("Apply fertilizer", target_language_code="kn-IN")
    assert trans["success"] and len(trans["translated_text"]) > 0, "Translation failed"
    print("  -> PASSED: All 5 Sarvam AI services (ASR, TTS, LLM, Vision, Mayura) validated.")

if __name__ == "__main__":
    print("\n🧪 Running KisanSamvaad Backend Verification Tests...\n" + "="*50)
    test_guardrails_banned_chemicals()
    test_guardrails_dosage_bounds()
    test_soil_health_diagnostic()
    test_sarvam_client_services()
    print("="*50 + "\n✅ ALL 4 AUTOMATED TEST SUITES PASSED SUCCESSFULLY!\n")

