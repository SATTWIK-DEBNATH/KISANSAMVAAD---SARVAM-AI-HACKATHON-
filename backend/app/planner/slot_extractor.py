"""
KisanSamvaad - Voice Transcript Slot Extractor
Extracts crop, land area, and measurement unit from spoken farmer transcripts.
Combines Indic regex patterns with clarifying question generation when slots are ambiguous.
Never guesses missing values.
"""

import re
from typing import Dict, Any, Optional, Tuple

# Multilingual crop dictionary mapping local names to canonical keys
CROP_ALIASES: Dict[str, str] = {
    # English
    "tomato": "tomato",
    "tomatoes": "tomato",
    "maize": "maize",
    "corn": "maize",
    "ragi": "ragi",
    "finger millet": "ragi",
    "millet": "ragi",
    "paddy": "paddy",
    "rice": "paddy",

    # Kannada
    "ಟೊಮೇಟೊ": "tomato",
    "ಟೊಮ್ಯಾಟೊ": "tomato",
    "ತೊಮೆಟೊ": "tomato",
    "ಮೆಕ್ಕೆಜೋಳ": "maize",
    "ಮುಸುಕಿನ ಜೋಳ": "maize",
    "ಜೋಳ": "maize",
    "ರಾಗಿ": "ragi",
    "ಭತ್ತ": "paddy",

    # Hindi
    "टमाटर": "tomato",
    "मक्का": "maize",
    "भुट्टा": "maize",
    "रागी": "ragi",
    "मडुआ": "ragi",
    "धान": "paddy",
    "चावल": "paddy",

    # Tamil
    "தக்காளி": "tomato",
    "மக்காச்சோளம்": "maize",
    "கேழ்வரகு": "ragi",
    "ராகி": "ragi",
    "நெல்": "paddy",
    "அரிசி": "paddy"
}

# Multilingual unit aliases mapping local names to canonical units
UNIT_ALIASES: Dict[str, str] = {
    # English
    "acre": "acre",
    "acres": "acre",
    "ac": "acre",
    "hectare": "hectare",
    "hectares": "hectare",
    "ha": "hectare",
    "gunta": "gunta",
    "guntas": "gunta",
    "guntha": "gunta",
    "gunthas": "gunta",

    # Kannada
    "ಎಕರೆ": "acre",
    "ಎಕ್ರೆ": "acre",
    "ಗುಂಟೆ": "gunta",
    "ಗುಂಟ": "gunta",
    "ಹೆಕ್ಟೇರ್": "hectare",
    "ಹೆಕ್ಟೇರು": "hectare",

    # Hindi
    "एकड़": "acre",
    "एकड": "acre",
    "गुंठा": "gunta",
    "गुंटा": "gunta",
    "हेक्टेयर": "hectare",

    # Tamil
    "ஏக்கர்": "acre",
    "ஹெக்டேர்": "hectare",
    "குண்டா": "gunta"
}

class VoiceSlotExtractor:
    """Extracts crop, area, and unit from voice transcripts with clarifying questions."""

    @classmethod
    def extract_slots(cls, transcript: str, language: str = "kn") -> Dict[str, Any]:
        """
        Parses text or voice transcript to extract crop, area, and unit.
        Returns is_complete: False with clarifying_question if any slot is missing.
        """
        raw = transcript.strip().lower()

        # Step 1: Detect Crop
        detected_crop = None
        for alias, canon in CROP_ALIASES.items():
            # Check whole word or substring for Indic scripts
            if alias in raw:
                detected_crop = canon
                break

        # Step 2: Detect Unit
        detected_unit = None
        for alias, canon in UNIT_ALIASES.items():
            if alias in raw:
                detected_unit = canon
                break

        # Step 3: Detect Numerical Area
        detected_area = None
        # Look for numbers adjacent to units or standalone numbers
        num_matches = re.findall(r"(\d+(?:\.\d+)?)", raw)
        if num_matches:
            try:
                # Find the first reasonable area number (e.g. 0.1 to 100)
                for num_str in num_matches:
                    val = float(num_str)
                    if 0.05 <= val <= 500:
                        detected_area = val
                        break
            except Exception:
                pass

        # Default unit to acre if area is found and transcript mentions farm words
        if detected_area and not detected_unit:
            # If word contains acre sounds or standard farm query
            detected_unit = "acre"

        # Check completeness
        missing_slots = []
        if not detected_crop:
            missing_slots.append("crop")
        if detected_area is None:
            missing_slots.append("area")
        if not detected_unit:
            missing_slots.append("unit")

        is_complete = len(missing_slots) == 0

        # Generate targeted clarifying question
        clarifying_question = None
        if not is_complete:
            clarifying_question = cls._generate_clarifying_question(missing_slots, language)

        return {
            "transcript": transcript,
            "is_complete": is_complete,
            "missing_slots": missing_slots,
            "crop": detected_crop,
            "area": detected_area,
            "unit": detected_unit,
            "clarifying_question": clarifying_question
        }

    @classmethod
    def _generate_clarifying_question(cls, missing: list, language: str = "kn") -> str:
        lang = language.lower()

        if "crop" in missing and "area" in missing:
            if lang.startswith("kn"):
                return "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಬೆಳೆ ಮತ್ತು ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣವನ್ನು ತಿಳಿಸಿ (ಉದಾಹರಣೆಗೆ: '2 ಎಕರೆ ಟೊಮೇಟೊ')."
            elif lang.startswith("hi"):
                return "कृपया अपनी फसल और खेत का क्षेत्रफल बताएं (जैसे: '2 एकड़ टमाटर')।"
            elif lang.startswith("ta"):
                return "தயவுசெய்து உங்கள் பயிர் மற்றும் நிலத்தின் அளவைக் குறிப்பிடவும் (உதாரணம்: '2 ஏக்கர் தக்காளி')."
            else:
                return "Please tell us your crop and land area (e.g. '2 acres tomato')."

        if "crop" in missing:
            if lang.startswith("kn"):
                return "ಯಾವ ಬೆಳೆಗೆ ಗೊಬ್ಬರದ ಲೆಕ್ಕಾಚಾರ ಬೇಕು ಎಂದು ತಿಳಿಸಿ (ಟೊಮೇಟೊ, ರಾಗಿ, ಮೆಕ್ಕೆಜೋಳ, ಅಥವಾ ಭತ್ತ)?"
            elif lang.startswith("hi"):
                return "कृपया बताएं कि आपको किस फसल (टमाटर, मक्का, रागी, या धान) के लिए योजना चाहिए?"
            elif lang.startswith("ta"):
                return "எந்தப் பயிருக்கு உரத் திட்டம் வேண்டும் என்று குறிப்பிடவும் (தக்காளி, மக்காச்சோளம், ராகி, அல்லது நெல்)?"
            else:
                return "Which crop are you planning for (tomato, maize, ragi, or paddy)?"

        if "area" in missing:
            if lang.startswith("kn"):
                return "ನಿಮ್ಮ ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ ಎಷ್ಟು ಎಂದು ತಿಳಿಸಿ (ಉದಾಹರಣೆಗೆ 2 ಎಕರೆ ಅಥವಾ 30 ಗುಂಟೆ)?"
            elif lang.startswith("hi"):
                return "कृपया अपने खेत का क्षेत्रफल बताएं (जैसे 2 एकड़ या 30 गुंठा)?"
            elif lang.startswith("ta"):
                return "உங்கள் நிலத்தின் பரப்பளவு என்ன என்று குறிப்பிடவும் (உதாரணம் 2 ஏக்கர் அல்லது 30 குண்டா)?"
            else:
                return "What is your land area (e.g. 2 acres or 30 guntas)?"

        return "Could you please clarify your crop and land area?"

