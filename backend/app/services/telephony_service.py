"""
KisanSamvaad - 1800-KISAN-AI Telephony IVR Service
Simulates voice telephony for farmers on basic 2G/3G feature phones without internet.
Handles DTMF keypress navigation and synthesizes spoken audio responses.
"""

from typing import Dict, Any, List
from ..integrations.mandi.connector import MandiConnector
from ..integrations.weather.connector import WeatherConnector

class TelephonyIVRService:
    """State machine and menu handler for 1800-KISAN-AI toll-free service."""

    IVR_PROMPTS = {
        "welcome": {
            "kn": "ಕಿಸಾನ್ ಸಂವಾದ ಉಚಿತ ಕೃಷಿ ಸಹಾಯವಾಣಿಗೆ ಸ್ವಾಗತ. ಮಣ್ಣು ಪರೀಕ್ಷೆ ಫಲಿತಾಂಶಕ್ಕೆ 1 ಒತ್ತಿರಿ. ಇಂದಿನ ಮಂಡಿ ದರ ತಿಳಿಯಲು 2 ಒತ್ತಿರಿ. ಹವಾಮಾನ ಮತ್ತು ಸಿಂಪಡಣೆ ಮಾಹಿತಿಗೆ 3 ಒತ್ತಿರಿ. ಕೃಷಿ ವೈದ್ಯರೊಂದಿಗೆ ಮಾತನಾಡಲು 4 ಒತ್ತಿರಿ. ಸರ್ಕಾರಿ ಯೋಜನೆಗಳಿಗೆ 5 ಒತ್ತಿರಿ.",
            "hi": "किसान संवाद टोल-फ्री हेल्पलाइन में आपका स्वागत है। मृदा स्वास्थ्य रिपोर्ट के लिए 1 दबाएं। मंडी भाव के लिए 2 दबाएं। मौसम और छिड़काव सलाह के लिए 3 दबाएं। सीधे कृषि विशेषज्ञ से बात करने के लिए 4 दबाएं। सरकारी योजनाओं के लिए 5 दबाएं।",
            "en": "Welcome to KisanSamvaad sovereign agricultural helpline. Press 1 for Soil Card analysis. Press 2 for Mandi rates. Press 3 for Weather and spray advisories. Press 4 for voice consultation. Press 5 for Government schemes."
        }
    }

    @classmethod
    def process_dtmf_input(cls, digit: str, language: str = "kn") -> Dict[str, Any]:
        """
        Routes farmer DTMF digit press to appropriate agricultural subsystem.
        """
        digit = str(digit).strip()
        lang_key = "kn" if language.startswith("kn") else ("hi" if language.startswith("hi") else "en")

        if digit == "1":
            # Soil Health Card Summary
            if lang_key == "kn":
                speech = "ನಿಮ್ಮ ಕೋಲಾರ ಮಣ್ಣು ಪರೀಕ್ಷೆ ಪ್ರಕಾರ: ಸಾರಜನಕ ಮತ್ತು ರಂಜಕ ಕಡಿಮೆ ಇದೆ. ಎಕರೆಗೆ 5 ಟನ್ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಮತ್ತು ಸುಣ್ಣ ಸೇರಿಸಿ."
            elif lang_key == "hi":
                speech = "आपकी मृदा रिपोर्ट के अनुसार: नाइट्रोजन और फास्फोरस कम है। 5 टन गोबर खाद और चूना मिलाकर उपचार करें।"
            else:
                speech = "Your soil test shows low Nitrogen and Phosphorus. Apply 5 tonnes organic compost and lime to buffer acidity."
            
            return {
                "digit": digit,
                "menu": "Soil Health Summary",
                "speech_response": speech,
                "status": "completed"
            }

        elif digit == "2":
            # Mandi Commodity Rate
            rates = MandiConnector.get_rates(commodity="tomato")
            tomato_rate = rates[0]["modal_price"] if rates else 1750
            if lang_key == "kn":
                speech = f"ಇಂದಿನ ಕೋಲಾರ ಎಪಿಎಂಸಿ ಮಂಡಿಯಲ್ಲಿ ಟೊಮೇಟೊ ಸರಾಸರಿ ದರ ಕ್ವಿಂಟಾಲ್‌ಗೆ {int(tomato_rate)} ರೂಪಾಯಿಗಳು."
            elif lang_key == "hi":
                speech = f"आज कोलार एपीएमसी मंडी में टमाटर का औसत भाव ₹{int(tomato_rate)} प्रति क्विंटल है।"
            else:
                speech = f"Today's modal price for Tomato at Kolar APMC is ₹{int(tomato_rate)} per quintal."

            return {
                "digit": digit,
                "menu": "Mandi Rates",
                "speech_response": speech,
                "status": "completed"
            }

        elif digit == "3":
            # Weather & Spray Window
            if lang_key == "kn":
                speech = "ಇಂದು ಬೆಳಿಗ್ಗೆ 10:30 ರವರೆಗೆ ಸಿಂಪಡಣೆಗೆ ಸೂಕ್ತ. ನಾಳೆ ಭಾರೀ ಮಳೆ ಮತ್ತು ಗಾಳಿ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ, ಆದ್ದರಿಂದ ಯಾವುದೇ ಕೀಟನಾಶಕ ಸಿಂಪಡಿಸಬೇಡಿ."
            elif lang_key == "hi":
                speech = "आज सुबह 10:30 तक छिड़काव सुरक्षित है। कल आंधी-तूफान की संभावना है, अतः कीटनाशक छिड़काव टालें।"
            else:
                speech = "Safe to spray until 10:30 AM today. Thunderstorms expected tomorrow; postpone all chemical spraying."

            return {
                "digit": digit,
                "menu": "Weather Spray Advisory",
                "speech_response": speech,
                "status": "completed"
            }

        elif digit == "4":
            # Direct Voice Query Mode
            if lang_key == "kn":
                speech = "ಬೀಪ್ ಶಬ್ದದ ನಂತರ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ಮಾತನಾಡಿ. ಕಿಸಾನ್ ಸಂವಾದ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ರೆಕಾರ್ಡ್ ಮಾಡುತ್ತದೆ."
            elif lang_key == "hi":
                speech = "बीप के बाद अपनी फसल का सवाल बोलें। किसान संवाद समाधान तैयार करेगा।"
            else:
                speech = "Please state your agricultural question after the beep."

            return {
                "digit": digit,
                "menu": "Voice Consultation Recording",
                "speech_response": speech,
                "status": "ready_for_audio"
            }

        elif digit == "5":
            # Government Schemes Information
            if lang_key == "kn":
                speech = "ಪಿಎಂ ಕಿಸಾನ್ ಯೋಜನೆಯಡಿ ವಾರ್ಷಿಕ 6,000 ರೂ ಹಾಗೂ ಕರ್ನಾಟಕ ರೈತ ಸಿರಿ ಯೋಜನೆಯಡಿ ಸಿರಿಧಾನ್ಯ ಬೆಳೆಗಾರರಿಗೆ ಹೆಕ್ಟೇರ್‌ಗೆ 10,000 ರೂ ಪ್ರೋತ್ಸಾಹಧನ ಲಭ್ಯವಿದೆ."
            elif lang_key == "hi":
                speech = "पीएम-किसान योजना के अंतर्गत ₹6,000 वार्षिक और कर्नाटक रायता सिरी में मिलेट उत्पादकों को ₹10,000 प्रति हेक्टेयर प्रोत्साहन उपलब्ध है।"
            else:
                speech = "PM-KISAN provides ₹6,000 per year and Karnataka Raita Siri provides ₹10,000 per hectare for millet growers."

            return {
                "digit": digit,
                "menu": "Government Schemes Information",
                "speech_response": speech,
                "status": "completed"
            }

        else:
            speech = cls.IVR_PROMPTS["welcome"].get(lang_key, cls.IVR_PROMPTS["welcome"]["kn"])
            return {
                "digit": digit,
                "menu": "Main Menu",
                "speech_response": speech,
                "status": "menu_prompt"
            }

