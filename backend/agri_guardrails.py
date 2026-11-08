"""
KisanSamvaad - Deterministic Agricultural Safety Guardrails Engine
Enforces strict scientific safety bounds on agrochemicals, fertilizers, and pest management.
Prevents dangerous hallucinations regarding pesticide dilutions, toxic chemical recommendations,
and inappropriate fertilizer ratios. Grounded in ICAR (Indian Council of Agricultural Research) standards.
"""

from typing import Dict, Any, List, Optional
import re

# Approved ICAR chemical reference bounds (dilution rates per liter of water, safe waiting periods)
APPROVED_AGROCHEMICALS: Dict[str, Dict[str, Any]] = {
    "chlorpyrifos": {
        "common_name": "Chlorpyrifos 20% EC",
        "target_pests": ["termite", "stem borer", "leaf hopper", "cutworm"],
        "max_dose_per_liter_ml": 2.5,
        "min_dose_per_liter_ml": 1.5,
        "waiting_period_days": 15,
        "toxicity_class": "Class II (Moderately Hazardous)",
        "warning": "Do not spray near water bodies or bee-foraging hours.",
    },
    "imidacloprid": {
        "common_name": "Imidacloprid 17.8% SL",
        "target_pests": ["aphid", "jassid", "whitefly", "thrips"],
        "max_dose_per_liter_ml": 0.5,
        "min_dose_per_liter_ml": 0.3,
        "waiting_period_days": 21,
        "toxicity_class": "Class II",
        "warning": "Do not exceed 0.5ml per liter. Highly toxic to honeybees.",
    },
    "neem_oil": {
        "common_name": "Neem Oil (Azadirachtin 1500 ppm)",
        "target_pests": ["aphid", "caterpillar", "whitefly", "mildew"],
        "max_dose_per_liter_ml": 5.0,
        "min_dose_per_liter_ml": 3.0,
        "waiting_period_days": 0,
        "toxicity_class": "Bio-pesticide (Safe)",
        "warning": "Safe organic option. Spray during cool morning or evening.",
    },
    "mancozeb": {
        "common_name": "Mancozeb 75% WP",
        "target_pests": ["blight", "leaf spot", "downy mildew", "rust"],
        "max_dose_per_liter_gm": 2.5,
        "min_dose_per_liter_gm": 2.0,
        "waiting_period_days": 10,
        "toxicity_class": "Class IV (Slightly Hazardous)",
        "warning": "Wear mask and gloves while spraying fungicide.",
    },
    "carbendazim": {
        "common_name": "Carbendazim 50% WP",
        "target_pests": ["powdery mildew", "seed rot", "anthracnose"],
        "max_dose_per_liter_gm": 1.5,
        "min_dose_per_liter_gm": 1.0,
        "waiting_period_days": 14,
        "toxicity_class": "Class III",
        "warning": "Effective systemic fungicide. Do not mix with alkaline substances.",
    },
    "urea": {
        "common_name": "Urea (46% N) foliar spray",
        "target_crops": ["wheat", "paddy", "cotton", "maize"],
        "max_foliar_concentration_pct": 2.0,
        "warning": "Never exceed 2% concentration (20g/L) for foliar spray to avoid leaf burn.",
    }
}

# Strictly banned substances in India (Central Insecticides Board / CIBRC banned list)
BANNED_SUBSTANCES = [
    "endosulfan", "ddt", "aldrin", "dieldrin", "paraquat", "monocrotophos",
    "methyl parathion", "chlordane", "heptachlor", "phosphamidon"
]


class AgriGuardrailEngine:
    """Deterministic validation of agricultural recommendations to prevent harm."""

    @classmethod
    def validate_recommendation(cls, text: str) -> Dict[str, Any]:
        """
        Scans generated recommendation text for:
        1. Mentions of banned or restricted chemicals
        2. Dangerous over-dosage of approved pesticides
        3. Mandatory safety warnings and PPE notices
        """
        lower_text = text.lower()
        violations: List[str] = []
        cautions: List[str] = []
        is_safe = True

        # Check 1: Banned substances
        for banned in BANNED_SUBSTANCES:
            if banned in lower_text:
                is_safe = False
                violations.append(
                    f"CRITICAL SAFETY VIOLATION: '{banned.upper()}' is strictly banned in India under CIBRC regulations. It must never be recommended."
                )

        # Check 2: Chemical dosage sanity bounds
        for chem_key, chem_info in APPROVED_AGROCHEMICALS.items():
            if chem_key in lower_text:
                cautions.append(f"Approved agrochemical detected: {chem_info['common_name']}")
                
                # Check for numerical dosage hallucination (e.g., '10 ml per liter')
                matches = re.findall(rf"{chem_key}.*?(\d+(?:\.\d+)?)\s*(?:ml|gm|g|grams)\s*(?:per|/)\s*liter", lower_text)
                for dose_str in matches:
                    dose = float(dose_str)
                    max_allowed = chem_info.get("max_dose_per_liter_ml") or chem_info.get("max_dose_per_liter_gm", 5.0)
                    if dose > (max_allowed * 1.5):
                        is_safe = False
                        violations.append(
                            f"EXCESSIVE DOSAGE DETECTED: {dose} for {chem_key}. Maximum safe ICAR dose is {max_allowed}. This can destroy crops or cause chemical poisoning!"
                        )

        # Check 3: Safety disclaimer addition
        has_safety_notice = any(w in lower_text for w in ["gloves", "mask", "waiting period", "safety", "सावधानी", "मास्क"])
        
        return {
            "is_safe": is_safe,
            "violations": violations,
            "cautions": cautions,
            "safety_notice_present": has_safety_notice,
            "verified_by": "ICAR-Grounded AgriGuardrail Engine"
        }

    @classmethod
    def sanitize_response(cls, response_text: str, validation: Dict[str, Any], language: str = "hi") -> str:
        """Injects safety overrides or critical disclaimers when violations are found."""
        if not validation["is_safe"]:
            override_msg_hi = (
                "\n\n⚠️ **कृषि सुरक्षा चेतावनी (ICAR दिशानिर्देश):** "
                "अनुशंसा में कुछ रसायनों की मात्रा अधिक पाई गई है। "
                "कृपया किसी भी कीटनाशक के छिड़काव से पहले नजदीकी कृषि विज्ञान केंद्र (KVK) से संपर्क करें।"
            )
            override_msg_en = (
                "\n\n⚠️ **Agricultural Safety Warning (ICAR Guidelines):** "
                "Potential dosage or restricted substance alert detected. "
                "Always verify pesticide dosages with your local Krishi Vigyan Kendra (KVK) officer."
            )
            return response_text + (override_msg_hi if language == "hi" else override_msg_en)
        return response_text

