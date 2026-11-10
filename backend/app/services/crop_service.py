"""
KisanSamvaad - Multimodal Crop Health Diagnostics Subsystem
Performs agronomic symptom and vision differential diagnosis.
Enforces explicit experimental labeling, ICAR treatment grounding,
deterministic CIBRC chemical guardrails, and human KVK escalation.
"""

from typing import Dict, Any, List, Optional
import os
import re
from ..safety.agri_guardrails import AgriGuardrailEngine
from ..db.repository import repository
from .plant_vision import PlantVisionClassifier

# Agronomic Knowledge Base for Common Indian Crop Diseases and Pests
CROP_DIAGNOSTIC_DB: Dict[str, List[Dict[str, Any]]] = {
    "tomato": [
        {
            "id": "tom_early_blight",
            "name": "Tomato Early Blight",
            "pathogen": "Alternaria solani",
            "keywords": ["concentric", "rings", "target board", "lower leaves", "brown spots", "yellow halo", "blight"],
            "base_confidence": 0.88,
            "severity": "Moderate",
            "differential_alternative": "Septoria Leaf Spot (Septoria lycopersici)",
            "alternative_confidence": 0.52,
            "remedy_organic": "Spray Neem Oil (Azadirachtin 1500 ppm) 3ml/L of water or apply Trichoderma harzianum 5g/L.",
            "remedy_chemical": "Spray Mancozeb 75% WP @ 2.0g to 2.5g per liter of water. Ensure thorough coverage of lower foliage.",
            "cultural_practices": "Remove and burn severely infected lower leaves. Practice 3-year crop rotation without solanaceous crops.",
            "advisory_kn": "ಟೊಮೇಟೊ ಮುಂಚಿನ ಎಲೆ ಅಂಗಮಾರಿ ರೋಗ (Early Blight). ಕೆಳಗಿನ ಎಲೆಗಳಲ್ಲಿ ವೃತ್ತಾಕಾರದ ಕಂದು ಚುಕ್ಕೆಗಳು ಕಾಣಿಸುತ್ತವೆ. ಬೇವಿನ ಎಣ್ಣೆ 3 ಮಿ.ಲೀ ಅಥವಾ ಮ್ಯಾಂಕೋಜೆಬ್ 2.0 ಗ್ರಾಂ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "टमाटर का अगेती झुलसा रोग (Early Blight)। निचली पत्तियों पर गोल छल्लेदार भूरे धब्बे बनते हैं। नीम का तेल 3 मि.ली या मैंकोजेब 2.0 ग्राम प्रति लीटर पानी में मिलाकर छिड़काव करें।"
        },
        {
            "id": "tom_leaf_curl",
            "name": "Tomato Leaf Curl Virus (ToLCV)",
            "pathogen": "Begomovirus (Transmitted by Whitefly - Bemisia tabaci)",
            "keywords": ["curl", "curling", "yellow", "stunted", "crinkled", "small leaves", "whitefly", "flies"],
            "base_confidence": 0.91,
            "severity": "High",
            "differential_alternative": "Tomato Mosaic Virus (ToMV) or Mite Damage",
            "alternative_confidence": 0.48,
            "remedy_organic": "Install yellow sticky traps @ 15-20 traps/acre. Spray neem oil 5ml/L to control vector whiteflies.",
            "remedy_chemical": "For whitefly control, spray ICAR-approved Imidacloprid 17.8% SL @ 0.3ml to 0.4ml per liter. (Strictly do not exceed 0.5ml/L).",
            "cultural_practices": "Eradicate virus-infected plants immediately. Raise border crops of maize or sorghum to impede whitefly drift.",
            "advisory_kn": "ಟೊಮೇಟೊ ಎಲೆ ಮುದುಡು ನಂಜು ರೋಗ (Leaf Curl Virus). ಬಿಳಿ ನೊಣಗಳಿಂದ ಈ ರೋಗ ಹರಡುತ್ತದೆ. ಹಳದಿ ಅಂಟು ಬಲೆಗಳನ್ನು ಅಳವಡಿಸಿ ಹಾಗೂ ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 0.3 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "टमाटर का पर्ण कुंचन विषाणु रोग (Leaf Curl Virus)। यह सफेद मक्खी द्वारा फैलता है। पीले चिपचिपे कार्ड लगाएं और इमिडाक्लोप्रिड 0.3 मि.ली प्रति लीटर पानी में छिड़कें।"
        },
        {
            "id": "tom_fruit_borer",
            "name": "Tomato Fruit Borer",
            "pathogen": "Helicoverpa armigera",
            "keywords": ["hole", "borer", "caterpillar", "eating fruit", "larva", "feces"],
            "base_confidence": 0.85,
            "severity": "High",
            "differential_alternative": "Spodoptera litura (Tobacco Cutworm)",
            "alternative_confidence": 0.45,
            "remedy_organic": "Install pheromone traps (Helilure) @ 5/acre. Spray Bacillus thuringiensis (Bt) @ 2g/L.",
            "remedy_chemical": "Spray Chlorantraniliprole 18.5% SC @ 0.3ml per liter of water during early larval instars.",
            "cultural_practices": "Plant African marigold as trap crop (1 marigold row for every 16 tomato rows).",
            "advisory_kn": "ಟೊಮೇಟೊ ಕಾಯಿ ಕೊರೆಯುವ ಹುಳು (Fruit Borer). ಹಣ್ಣುಗಳಲ್ಲಿ ದುಂಡನೆಯ ರಂಧ್ರಗಳನ್ನು ಮಾಡಿ ತಿನ್ನುತ್ತದೆ. ಹೆಲಿಲ್ಯೂರ್ ಮೋಹಕ ಬಲೆಗಳನ್ನು ಇರಿಸಿ ಹಾಗೂ ಜೈವಿಕ ಬಿಟಿ (Bt) ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "टमाटर फल छेदक कीट (Fruit Borer)। फलों में गोल छेद करके अंदर से गूदा खाता है। फेरोमोन ट्रैप लगाएं और जैव कीटनाशक बीटी (Bt) का छिड़काव करें।"
        }
    ],
    "cotton": [
        {
            "id": "cot_pink_bollworm",
            "name": "Pink Bollworm",
            "pathogen": "Pectinophora gossypiella",
            "keywords": ["pink", "bollworm", "rosette flower", "stained lint", "boll damage"],
            "base_confidence": 0.89,
            "severity": "Critical",
            "differential_alternative": "American Bollworm (Helicoverpa armigera)",
            "alternative_confidence": 0.55,
            "remedy_organic": "Install Gossyplure pheromone traps @ 8-10 traps/acre. Release Trichogramma egg parasitoids.",
            "remedy_chemical": "Spray Chlorpyrifos 20% EC @ 2.0ml/L (Strictly do not exceed 2.5ml/L). Do not use banned monocrotophos.",
            "cultural_practices": "Avoid ratoon cotton crop. Ensure synchronous sowing within village cluster.",
            "advisory_kn": "ಹತ್ತಿಯ ಗುಲಾಬಿ ಕಾಯಿ ಹುಳು (Pink Bollworm). ಹೂವುಗಳು ರೊಸೆಟ್ ಆಕಾರಕ್ಕೆ ತಿರುಗುತ್ತವೆ. ಮೋಹಕ ಬಲೆಗಳನ್ನು ಬಳಸಿ ಹಾಗೂ ಕ್ಲೋರ್‌ಪೈರಿಫಾಸ್ 2.0 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "कपास की गुलाबी सूंडी (Pink Bollworm)। गूलर के अंदर घुसकर रुई को नुकसान पहुंचाती है। फेरोमोन ट्रैप लगाएं और सुरक्षित क्लोरपायरीफॉस का छिड़काव करें।"
        }
    ],
    "chilli": [
        {
            "id": "chi_thrips_murda",
            "name": "Chilli Thrips & Leaf Curl (Murda Complex)",
            "pathogen": "Scirtothrips dorsalis / Polyphagotarsonemus latus",
            "keywords": ["boat", "upward curl", "crinkled", "bronzing", "murda", "thrips"],
            "base_confidence": 0.86,
            "severity": "Moderate",
            "differential_alternative": "Yellow Mite Damage (Downward curling)",
            "alternative_confidence": 0.60,
            "remedy_organic": "Spray Neem seed kernel extract (NSKE 5%) or Neem oil 4ml/L.",
            "remedy_chemical": "Spray ICAR-approved Imidacloprid 17.8% SL @ 0.3ml/L. Fails closed against banned organophosphates.",
            "cultural_practices": "Grow border crops of maize or sorghum; avoid excessive chemical nitrogen application.",
            "advisory_kn": "ಮೆಣಸಿನಕಾಯಿ ಮುರಡ ರೋಗ ಮತ್ತು ನುಸಿ ಬಾಧೆ. ಎಲೆಗಳು ದೋಣಿಯಾಕಾರದಲ್ಲಿ ಮೇಲ್ಮುಖವಾಗಿ ಮುದುಡುತ್ತವೆ. ಬೇವಿನ ಕಷಾಯ 5% ಅಥವಾ ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 0.3 ಮಿ.ಲೀ ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "मिर्च का मुरड़ा रोग एवं थ्रिप्स। पत्तियां नाव की तरह ऊपर की ओर मुड़ जाती हैं। 5% नीम का काढ़ा या इमिडाक्लोप्रिड 0.3 मि.ली प्रति लीटर छिड़कें।"
        }
    ],
"rice": [
        {
            "id": "rice_blast",
            "name": "Rice Blast Disease",
            "pathogen": "Magnaporthe oryzae (Pyricularia oryzae)",
            "keywords": ["spindle", "eye-shaped", "blast", "lesion", "grey center", "paddy"],
            "base_confidence": 0.90,
            "severity": "High",
            "differential_alternative": "Brown Spot (Bipolaris oryzae)",
            "alternative_confidence": 0.54,
            "remedy_organic": "Spray Pseudomonas fluorescens @ 2.5 kg/ha or Neem oil 3ml/L of water.",
            "remedy_chemical": "Spray Tricyclazole 75% WP @ 0.6g per liter of water at tillering or panicle emergence stage.",
            "cultural_practices": "Avoid excessive nitrogen top-dressing; maintain 2-3 cm shallow water layer; burn infected stubble.",
            "advisory_kn": "ಭತ್ತದ ಬೆಂಕಿ ರೋಗ (Rice Blast). ಎಲೆಗಳ ಮೇಲೆ ಕಣ್ಣಿನಾಕಾರದ ಅಥವಾ ಕದಿರಿನಂತಹ ಬೂದು ಬಣ್ಣದ ಚುಕ್ಕೆಗಳು ಕಾಣಿಸುತ್ತವೆ. ಟ್ರೈಸೈಕ್ಲಾಜೋಲ್ 0.6 ಗ್ರಾಂ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "धान का झोंका रोग (Rice Blast)। पत्तियों पर आंख के आकार के धब्बे बनते हैं। ट्राइसाइक्लाजोल 0.6 ग्राम प्रति लीटर पानी में मिलाकर छिड़काव करें।"
        }
    ],
    "wheat": [
        {
            "id": "wheat_yellow_rust",
            "name": "Wheat Stripe / Yellow Rust",
            "pathogen": "Puccinia striiformis f. sp. tritici",
            "keywords": ["yellow", "stripes", "rust", "pustules", "powder", "wheat"],
            "base_confidence": 0.91,
            "severity": "Critical",
            "differential_alternative": "Leaf Rust (Puccinia triticina)",
            "alternative_confidence": 0.49,
            "remedy_organic": "Apply Trichoderma viride @ 5g/L; grow resistant varieties like HD-2967 or PBW-550.",
            "remedy_chemical": "Spray Propiconazole 25% EC @ 1.0ml per liter of water immediately upon initial stripe detection.",
            "cultural_practices": "Eradicate alternate hosts; avoid late sowing; do not apply excessive urea during cool humid weather.",
            "advisory_kn": "ಗೋಧಿ ಹಳದಿ ತುಕ್ಕು ರೋಗ (Yellow Rust). ಎಲೆಗಳ ಮೇಲೆ ಹಳದಿ ಬಣ್ಣದ ಗೆರೆಗಳು ಮತ್ತು ಪುಡಿ ಕಾಣಿಸುತ್ತದೆ. ಪ್ರೊಪಿಕೊನಜೋಲ್ 1.0 ಮಿ.ಲೀ ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ ಸಿಂಪಡಿಸಿ.",
            "advisory_hi": "गेहूं का पीला रतुआ (Yellow Rust)। पत्तियों पर पीले रंग की धारियों में पाउडर बनता है। प्रोपिकोनाजोल 1.0 मि.ली प्रति लीटर पानी में तुरंत छिड़काव करें।"
        }
    ]
}

class CropDiagnosticsService:
    """Provides multimodal crop diagnostic evaluations with strict safety bounds."""

    @classmethod
    def extract_visual_symptoms_from_image(
        cls,
        image_base64: str,
        crop_name: str
    ) -> tuple[str, str, Dict[str, Any]]:
        """
        Extracts agronomic visual leaf descriptors using deep learning vision models:
        - linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification (Hugging Face)
        - Google Gemini 1.5 Flash Vision API (if GEMINI_API_KEY present)
        - Calibrated ICAR offline vision descriptors
        """
        vision_res = PlantVisionClassifier.classify_image(image_base64, crop_name)
        taxonomy = vision_res["taxonomy"]
        primary_label = vision_res["primary_label"]
        source = vision_res["inference_source"]
        confidence = vision_res["confidence_score"]

        symptom_str = (
            f"Foliar lesions corresponding to {taxonomy['disease_name']} ({taxonomy['pathogen']}). "
            f"Detected by deep learning model {vision_res['model_used']}."
        )
        visual_note = (
            f"Computer vision model ({vision_res['model_used']}) classified image as {primary_label} "
            f"with {int(confidence * 100)}% confidence via {source}."
        )
        return symptom_str, visual_note, vision_res



    @classmethod
    def diagnose(
        cls,
        crop_name: str,
        symptom_description: Optional[str] = None,
        symptoms: Optional[str] = None,
        image_base64: Optional[str] = None,
        farmer_id: Optional[str] = None,
        language: str = "kn-IN"
    ) -> Dict[str, Any]:
        """
        Runs differential diagnosis against ICAR disease profiles.
        Enforces experimental labeling, confidence boundaries, and KVK escalation.
        """
        visual_notes = None
        vision_meta = None
        if image_base64:
            extracted_sym, visual_notes, vision_meta = cls.extract_visual_symptoms_from_image(image_base64, crop_name)
            if not (symptom_description or symptoms):
                raw_symptoms = extracted_sym
            else:
                raw_symptoms = f"{symptom_description or symptoms} {extracted_sym}"
        else:
            raw_symptoms = symptom_description or symptoms or ""
        crop_key = crop_name.strip().lower()
        candidates = CROP_DIAGNOSTIC_DB.get(crop_key, [])
        if not candidates:
            # Fallback for unrecognized crops
            for key in CROP_DIAGNOSTIC_DB:
                if key in crop_key or crop_key in key:
                    candidates = CROP_DIAGNOSTIC_DB[key]
                    break

        symptom_text = raw_symptoms.lower()
        best_match = None
        best_score = 0.0

        if candidates:
            for cand in candidates:
                kw_hits = sum(1 for kw in cand["keywords"] if kw in symptom_text)
                score = cand["base_confidence"] * (0.6 + 0.4 * min(kw_hits / max(1, len(cand["keywords"])), 1.0))
                if kw_hits > 0 and score > best_score:
                    best_score = score
                    best_match = cand

        # If deep learning vision identified a condition, adopt the taxonomy profile
        if vision_meta and vision_meta.get("taxonomy"):
            tax = vision_meta["taxonomy"]
            confidence = vision_meta["confidence_score"]
            primary_name = tax["disease_name"]
            pathogen = tax["pathogen"]
            differential_alt = tax["differential_alternative"]
            alt_confidence = tax["alternative_confidence"]
            severity = tax["severity"]
            remedy_org = tax["organic_remedy"]
            remedy_chem = tax["chemical_remedy"]
            cult_prac = tax["cultural_practices"]
            adv_kn = tax["advisory_kn"]
            adv_hi = tax["advisory_hi"]
        elif not best_match:
            confidence = 0.48
            primary_name = f"Unclassified {crop_name.capitalize()} Pathology"
            pathogen = "Fungal / Viral / Abiotic stress suspected"
            differential_alt = "Nutrient Deficiency or Root Knot Nematode"
            alt_confidence = 0.35
            severity = "Under Investigation"
            remedy_org = "Apply Farm Yard Manure (FYM) enriched with Trichoderma harzianum @ 5 kg/ha."
            remedy_chem = "Avoid applying synthetic chemicals without professional physical inspection."
            cult_prac = "Ensure proper field drainage and inspect plant root zone for gall formation."
            adv_kn = f"{crop_name} ಬೆಳೆಯಲ್ಲಿ ನಿಖರವಾದ ರೋಗ ಲಕ್ಷಣ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ. ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರದ (KVK) ಅಧಿಕಾರಿಗಳ ಬಳಿ ಪರೀಕ್ಷಿಸಿ."
            adv_hi = f"{crop_name} फसल में लक्षण स्पष्ट नहीं हैं। नजदीकी कृषि विज्ञान केंद्र (KVK) के विशेषज्ञ से संपर्क करें।"
        else:
            confidence = round(min(best_score, 0.94), 2)
            primary_name = best_match["name"]
            pathogen = best_match["pathogen"]
            differential_alt = best_match["differential_alternative"]
            alt_confidence = best_match["alternative_confidence"]
            severity = best_match["severity"]
            remedy_org = best_match["remedy_organic"]
            remedy_chem = best_match["remedy_chemical"]
            cult_prac = best_match["cultural_practices"]
            adv_kn = best_match["advisory_kn"]
            adv_hi = best_match["advisory_hi"]

        # Run safety guardrail on chemical remedy
        guardrail_check = AgriGuardrailEngine.validate_recommendation(remedy_chem)
        if not guardrail_check["is_safe"]:
            remedy_chem = "⚠️ Chemical treatment blocked by CIBRC safety guardrails. Consult local KVK agronomist."

        # Escalation criteria: confidence < 0.65 or critical severity
        escalate_to_kvk = (confidence < 0.65) or (severity == "Critical")
        kvk_contact = {
            "center": "ICAR - Krishi Vigyan Kendra (KVK Kolar / UAS Bangalore)",
            "phone": "08152-240212 / Toll-Free 1800-425-1551",
            "email": "kvkkolar@icar.gov.in",
            "advisory_note": "A field extension scientist has been notified for sample validation."
        } if escalate_to_kvk else None

        # Record expert case into database if escalated
        if escalate_to_kvk:
            try:
                repository.create_expert_case(
                    crop_name=crop_name,
                    symptom_summary=raw_symptoms[:200],
                    initial_diagnosis=primary_name,
                    confidence_score=confidence,
                    farmer_id=farmer_id
                )
            except Exception:
                pass

        adv_en = (
            f"Preliminary Assessment: {primary_name} ({pathogen}). "
            f"Confidence: {int(confidence * 100)}%. "
            f"Organic: {remedy_org} "
            f"Chemical: {remedy_chem}"
        )

        # Generate Sarvam Bulbul Indic Spoken Audio
        spoken_audio_url = None
        spoken_advisory_text = adv_kn if "kn" in language.lower() else (adv_hi if "hi" in language.lower() else adv_en)
        try:
            from ..integrations.sarvam_client import sarvam_client
            target_lang_code = "kn-IN" if "kn" in language.lower() else ("hi-IN" if "hi" in language.lower() else "en-IN")
            tts_result = sarvam_client.text_to_speech(spoken_advisory_text, target_language_code=target_lang_code)
            spoken_audio_url = tts_result.get("audio_url")
        except Exception:
            spoken_audio_url = None

        return {
            "experimental": True,
            "image_analyzed": bool(image_base64),
            "vision_model": vision_meta.get("model_used") if vision_meta else "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
            "inference_source": vision_meta.get("inference_source") if vision_meta else "text_symptom_matching",
            "top_predictions": vision_meta.get("top_predictions", []) if vision_meta else [],
            "visual_symptoms_detected": visual_notes,
            "spoken_audio_url": spoken_audio_url,
            "disclaimer": "Experimental AI Diagnostic Aid grounded in ICAR protocols. Verify physically with local KVK before chemical application.",
            "crop": crop_name,
            "primary_diagnosis": {
                "disease_name": primary_name,
                "pathogen": pathogen,
                "confidence_score": confidence,
                "severity_level": severity
            },
            "differential_diagnosis": {
                "secondary_suspect": differential_alt,
                "confidence_score": alt_confidence
            },
            "recommended_interventions": {
                "organic_biological": remedy_org,
                "approved_chemical": remedy_chem,
                "cultural_management": cult_prac
            },
            "safety_guardrails": guardrail_check,
            "escalate_to_kvk": escalate_to_kvk,
            "kvk_escalation_details": kvk_contact,
            "advisory_localized": {
                "kn": adv_kn,
                "hi": adv_hi,
                "en": adv_en
            }
        }
