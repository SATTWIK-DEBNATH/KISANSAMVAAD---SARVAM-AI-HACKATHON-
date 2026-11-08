"""
KisanSamvaad - Localized Spoken Narration & Number-Grounding Validator
Generates farmer-friendly spoken responses in Kannada, Hindi, Tamil, and English.
Enforces a strict number-grounding check: if an LLM is used for rephrasing and
hallucinates any number not present in the deterministic PlanResult, it fails closed
to the certified localized template.
"""

import re
from typing import Dict, Any, List, Set, Optional, Tuple

class NumberGroundingValidator:
    """Verifies that every numerical token in spoken text is grounded in the deterministic plan."""

    @classmethod
    def extract_numbers(cls, text: str) -> Set[float]:
        """Extracts all numerical values (integers, decimals) from text."""
        # Strip currency symbols and commas before matching
        cleaned = text.replace(",", "").replace("₹", "").replace("Rs.", "").replace("Rs", "")
        tokens = re.findall(r"\b\d+(?:\.\d+)?\b", cleaned)
        return {float(t) for t in tokens}

    @classmethod
    def collect_plan_numbers(cls, plan_dict: Dict[str, Any]) -> Set[float]:
        """Collects all valid numbers present in the deterministic plan."""
        valid_numbers: Set[float] = set()

        def _traverse(val):
            if isinstance(val, (int, float)):
                valid_numbers.add(float(val))
                valid_numbers.add(float(round(val)))
                valid_numbers.add(float(int(val)))
            elif isinstance(val, str):
                for s_num in re.findall(r"\b\d+(?:\.\d+)?\b", val):
                    try:
                        valid_numbers.add(float(s_num))
                    except ValueError:
                        pass
            elif isinstance(val, dict):
                for v in val.values():
                    _traverse(v)
            elif isinstance(val, (list, tuple)):
                for item in val:
                    _traverse(item)

        _traverse(plan_dict)
        return valid_numbers

    @classmethod
    def is_grounded(cls, candidate_text: str, plan_dict: Dict[str, Any]) -> Tuple[bool, List[float]]:
        """
        Returns True if every number in candidate_text exists in plan_dict.
        Returns False and list of ungrounded numbers if hallucination detected.
        """
        spoken_numbers = cls.extract_numbers(candidate_text)
        valid_numbers = cls.collect_plan_numbers(plan_dict)

        ungrounded = []
        for num in spoken_numbers:
            # Allow common day numbers (30, 45, 50) and rounding tolerance of 1.0
            matched = any(abs(num - v) < 0.05 or abs(num - round(v)) < 0.05 for v in valid_numbers)
            if not matched:
                ungrounded.append(num)

        return (len(ungrounded) == 0, ungrounded)

class NarrationRenderer:
    """Renders localized spoken text and validates against hallucination."""

    @classmethod
    def render_template(
        cls,
        crop: str,
        area: float,
        unit: str,
        bags: List[Dict[str, Any]],
        total_cost_inr: float,
        delay_recommended: bool,
        language: str = "kn"
    ) -> str:
        """Renders certified deterministic spoken response from localized templates."""
        lang = (language or "kn").lower()
        cost_formatted = f"{int(round(total_cost_inr + 1e-6)):,}"

        crop_clean = crop.lower()
        kn_crops = {"tomato": "ಟೊಮೇಟೊ", "maize": "ಮೆಕ್ಕೆಜೋಳ", "ragi": "ರಾಗಿ", "paddy": "ಭತ್ತ"}
        hi_crops = {"tomato": "टमाटर", "maize": "मक्का", "ragi": "रागी", "paddy": "धान"}
        ta_crops = {"tomato": "தக்காளி", "maize": "மக்காச்சோளம்", "ragi": "கேழ்வரகு", "paddy": "நெல்"}

        crop_kn = kn_crops.get(crop_clean, crop)
        crop_hi = hi_crops.get(crop_clean, crop)
        crop_ta = ta_crops.get(crop_clean, crop)

        kn_units = {"acre": "ಎಕರೆ", "acres": "ಎಕರೆ", "gunta": "ಗುಂಟೆ", "guntas": "ಗುಂಟೆ", "hectare": "ಹೆಕ್ಟೇರ್", "ha": "ಹೆಕ್ಟೇರ್"}
        hi_units = {"acre": "एकड़", "acres": "एकड़", "gunta": "गुंठा", "guntas": "गुंठा", "hectare": "हेक्टेयर", "ha": "हेक्टेयर"}
        ta_units = {"acre": "ஏக்கர்", "acres": "ஏக்கர்", "gunta": "குண்டா", "guntas": "குண்டா", "hectare": "ஹெக்டேர்", "ha": "ஹெக்டேர்"}

        unit_kn = kn_units.get(unit.lower(), unit)
        unit_hi = hi_units.get(unit.lower(), unit)
        unit_ta = ta_units.get(unit.lower(), unit)

        # Build bags summary
        if not bags:
            if lang.startswith("kn"):
                return f"{area} {unit_kn} {crop_kn} ಬೆಳೆಗೆ ಮಣ್ಣಿನಲ್ಲಿ ಪೋಷಕಾಂಶಗಳು ಸಮೃದ್ಧವಾಗಿದ್ದು ಯಾವುದೇ ರಾಸಾಯನಿಕ ಗೊಬ್ಬರದ ಅಗತ್ಯವಿಲ್ಲ."
            elif lang.startswith("hi"):
                return f"{area} {unit_hi} {crop_hi} फसल के लिए मृदा में पोषक तत्व पर्याप्त हैं, किसी रासायनिक खाद की आवश्यकता नहीं है।"
            elif lang.startswith("ta"):
                return f"{area} {unit_ta} {crop_ta} பயிருக்கு மண்ணில் சத்துக்கள் நிறைந்துள்ளன, ரசாயன உரம் தேவையில்லை."
            else:
                return f"For {area} {unit} of {crop}, soil nutrient reserves are high. No chemical fertilizer application is needed."

        # Format items per language
        kn_parts = []
        hi_parts = []
        ta_parts = []
        en_parts = []

        for b in bags:
            name = b.get("name", "")
            cnt = b.get("bags_count", 0)
            fid = b.get("fertilizer_id", "").lower()
            if fid == "urea":
                kn_parts.append(f"{cnt} ಚೀಲ ಯೂರಿಯಾ")
                hi_parts.append(f"{cnt} बोरी यूरिया")
                ta_parts.append(f"{cnt} மூட்டை யூரியா")
                en_parts.append(f"{cnt} bag(s) of Urea")
            elif fid == "dap":
                kn_parts.append(f"{cnt} ಚೀಲ ಡಿಎಪಿ")
                hi_parts.append(f"{cnt} बोरी डीएपी")
                ta_parts.append(f"{cnt} மூட்டை டிஏபி")
                en_parts.append(f"{cnt} bag(s) of DAP")
            elif fid == "ssp":
                kn_parts.append(f"{cnt} ಚೀಲ ಎಸ್ಎಸ್ಪಿ")
                hi_parts.append(f"{cnt} बोरी एसएसपी")
                ta_parts.append(f"{cnt} மூட்டை எஸ்எஸ்பி")
                en_parts.append(f"{cnt} bag(s) of SSP")
            elif fid == "mop":
                kn_parts.append(f"{cnt} ಚೀಲ ಎಂಒಪಿ (ಪೊಟ್ಯಾಷ್)")
                hi_parts.append(f"{cnt} बोरी एमओपी (पोटाश)")
                ta_parts.append(f"{cnt} மூட்டை எம்போபி")
                en_parts.append(f"{cnt} bag(s) of MOP")
            else:
                kn_parts.append(f"{cnt} ಚೀಲ {name}")
                hi_parts.append(f"{cnt} बोरी {name}")
                ta_parts.append(f"{cnt} மூட்டை {name}")
                en_parts.append(f"{cnt} bag(s) of {name}")

        kn_bags = ", ".join(kn_parts)
        hi_bags = ", ".join(hi_parts)
        ta_bags = ", ".join(ta_parts)
        en_bags = ", ".join(en_parts)

        # Weather warning sentence
        kn_rain = " ನಾಳೆ ಭಾರಿ ಮಳೆ ನಿರೀಕ್ಷೆಯಿರುವುದರಿಂದ ಗೊಬ್ಬರ ಹಾಕುವುದನ್ನು 2-3 ದಿನ ಮುಂದೂಡಿ." if delay_recommended else " ಇಂದಿನ ಹವಾಮಾನವು ಗೊಬ್ಬರ ಹಾಕಲು ಅನುಕೂಲಕರವಾಗಿದೆ."
        hi_rain = " कल भारी बारिश की संभावना है, इसलिए खाद डालना 2-3 दिन टालें।" if delay_recommended else " आज का मौसम खाद डालने के लिए अनुकूल है।"
        ta_rain = " கனமழை எதிர்பார்க்கப்படுவதால், உரமிடுவதை 2-3 நாட்கள் தள்ளிப்போடுங்கள்." if delay_recommended else " இன்றைய வானிலை உரமிட ஏற்றதாக உள்ளது."
        en_rain = " Heavy rain is expected, so delay application by 2-3 days." if delay_recommended else " Today's weather is clear and safe for application."

        # Final disclaimer
        disclaimer_kn = " ಗೊಬ್ಬರ ಬಳಸುವ ಮುನ್ನ ಸ್ಥಳೀಯ ಕೃಷಿ ಅಧಿಕಾರಿಯ ಸಲಹೆ ಪಡೆಯಿರಿ."
        disclaimer_hi = " खाद डालने से पहले स्थानीय कृषि अधिकारी या केवीके से पुष्टि करें।"
        disclaimer_ta = " உரமிடுவதற்கு முன் உள்ளூர் வேளாண் அலுவலரிடம் ஆலோசனை பெறவும்."
        disclaimer_en = " Confirm with your local KVK or agricultural officer before applying."

        if lang.startswith("kn"):
            return (
                f"{area} {unit_kn} {crop_kn} ಬೆಳೆಗೆ {kn_bags} ಅಗತ್ಯವಿದೆ, ಒಟ್ಟು ಅಂದಾಜು ರೂ. {cost_formatted}. "
                f"ಬಿತ್ತನೆ ಸಮಯದಲ್ಲಿ ಎಲ್ಲಾ ರಂಜಕ, ಪೊಟ್ಯಾಷ್ ಮತ್ತು ಸ್ವಲ್ಪ ಯೂರಿಯಾ ಹಾಕಿ, ಉಳಿದ ಯೂರಿಯಾವನ್ನು 30 ದಿನಗಳ ನಂತರ ಮೇಲುಗೊಬ್ಬರವಾಗಿ ನೀಡಿ."
                f"{kn_rain}{disclaimer_kn}"
            )
        elif lang.startswith("hi"):
            return (
                f"{area} {unit_hi} {crop_hi} फसल के लिए {hi_bags} की आवश्यकता है, कुल अनुमानित लागत लगभग ₹{cost_formatted} है। "
                f"बुवाई के समय पूरा फास्फोरस, पोटाश और यूरिया की आंशिक मात्रा डालें, शेष यूरिया 30 दिनों बाद टॉप ड्रेसिंग में दें।"
                f"{hi_rain}{disclaimer_hi}"
            )
        elif lang.startswith("ta"):
            return (
                f"{area} {unit_ta} {crop_ta} பயிருக்கு {ta_bags} தேவை, மொத்த உத்தேச செலவு சுமார் ரூ. {cost_formatted}. "
                f"விதைக்கும் போது பாஸ்பரஸ், பொட்டாஷ் இடவும், யூரியாவை 30 நாட்களுக்குப் பிறகு பிரித்து இடவும்."
                f"{ta_rain}{disclaimer_ta}"
            )
        else:
            return (
                f"For {area} {unit} of {crop}, you need {en_bags}, totaling about Rs {cost_formatted}. "
                f"Apply all phosphorus and potash with basal urea at sowing, then top-dress the remaining urea after 30 days."
                f"{en_rain}{disclaimer_en}"
            )

    @classmethod
    def process_narration(
        cls,
        candidate_text: Optional[str],
        plan_dict: Dict[str, Any],
        crop: str,
        area: float,
        unit: str,
        bags: List[Dict[str, Any]],
        total_cost_inr: float,
        delay_recommended: bool,
        language: str = "kn"
    ) -> str:
        """
        Validates candidate LLM text with NumberGroundingValidator.
        Falls back to template if candidate is missing or contains ungrounded numbers.
        """
        if candidate_text and candidate_text.strip():
            is_valid, ungrounded = NumberGroundingValidator.is_grounded(candidate_text, plan_dict)
            if is_valid:
                return candidate_text

        return cls.render_template(
            crop=crop,
            area=area,
            unit=unit,
            bags=bags,
            total_cost_inr=total_cost_inr,
            delay_recommended=delay_recommended,
            language=language
        )
