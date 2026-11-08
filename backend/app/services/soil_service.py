"""
KisanSamvaad - Soil Diagnostic & Agronomic Service
Classifies soil test parameters according to ICAR benchmarks.
Generates localized remediation advice and fertilizer cost reduction strategies.
"""

from typing import Dict, Any, List

class SoilDiagnosticService:
    """Evaluates NPK and pH against ICAR standards."""

    @classmethod
    def evaluate_sample(
        cls,
        n: float = 280.0,
        p: float = 14.0,
        k: float = 210.0,
        ph: float = 6.8,
        oc: float = 0.55,
        zinc: float = 0.6,
        boron: float = 0.5
    ) -> Dict[str, Any]:
        """
        Classifies soil parameters and provides bilingual remediation guidance.
        """
        status: Dict[str, str] = {}
        recs_hi: List[str] = []
        recs_kn: List[str] = []
        recs_en: List[str] = []

        # Nitrogen (ICAR: Low < 280, Medium 280-560, High > 560 kg/ha)
        if n < 280.0:
            status["N"] = "Low (कम / ಕಡಿಮೆ)"
            recs_hi.append("नाइट्रोजन की कमी: 5 टन प्रति एकड़ सड़ा हुआ गोबर खाद (FYM) डालें और यूरिया को 3 बार में विभाजित करके दें।")
            recs_kn.append("ಸಾರಜನಕ ಕೊರತೆ: ಎಕರೆಗೆ 5 ಟನ್ ಚೆನ್ನಾಗಿ ಕಳಿತ ಕೊಟ್ಟಿಗೆ ಗೊಬ್ಬರ ಹಾಕಿ ಮತ್ತು ಯೂರಿಯಾವನ್ನು 3 ಕಂತುಗಳಲ್ಲಿ ನೀಡಿ.")
            recs_en.append("Low Nitrogen: Apply 5 tonnes/acre Farm Yard Manure (FYM) and split Urea application into 3 doses.")
        elif n > 560.0:
            status["N"] = "High (अधिक / ಹೆಚ್ಚು)"
            recs_hi.append("नाइट्रोजन अधिक है: यूरिया का प्रयोग 25% कम करें ताकि फसल गिरे नहीं और कीट कम लगें।")
            recs_kn.append("ಸಾರಜನಕ ಹೆಚ್ಚಾಗಿದೆ: ಯೂರಿಯಾ ಬಳಕೆಯನ್ನು 25% ರಷ್ಟು ಕಡಿಮೆ ಮಾಡಿ; ಇದು ಕೀಟ ಬಾಧೆಯನ್ನು ತಪ್ಪಿಸುತ್ತದೆ.")
            recs_en.append("High Nitrogen: Reduce synthetic Urea application by 25% to prevent crop lodging and pest infestation.")
        else:
            status["N"] = "Medium (मध्यम / ಮಧ್ಯಮ)"
            recs_hi.append("नाइट्रोजन संतुलित है। सामान्य अनुशंसित मात्रा बनाए रखें।")
            recs_kn.append("ಸಾರಜನಕ ಮಟ್ಟ ಸಮತೋಲನದಲ್ಲಿದೆ. ಶಿಫಾರಸು ಮಾಡಿದ ಪ್ರಮಾಣವನ್ನು ಮುಂದುವರಿಸಿ.")
            recs_en.append("Nitrogen level is balanced. Maintain standard recommended dose.")

        # Phosphorus (ICAR: Low < 10, Medium 10-25, High > 25 kg/ha)
        if p < 10.0:
            status["P"] = "Low (कम / ಕಡಿಮೆ)"
            recs_hi.append("फास्फोरस की कमी: सिंगल सुपर फास्फेट (SSP) का प्रयोग करें, जो सल्फर भी प्रदान करता है।")
            recs_kn.append("ರಂಜಕದ ಕೊರತೆ: ಸಿಂಗಲ್ ಸೂಪರ್ ಫಾಸ್ಫೇಟ್ (SSP) ಬಳಸಿ; ಇದು ಬೇರುಗಳ ಬೆಳವಣಿಗೆಯನ್ನು ಉತ್ತಮಗೊಳಿಸುತ್ತದೆ.")
            recs_en.append("Low Phosphorus: Use Single Super Phosphate (SSP) which also provides essential sulfur for root vigor.")
        elif p > 25.0:
            status["P"] = "High (अधिक / ಹೆಚ್ಚು)"
            recs_hi.append("फास्फोरस पर्याप्त है: DAP की अतिरिक्त मात्रा न डालें।")
            recs_kn.append("ರಂಜಕ ಸಮೃದ್ಧವಾಗಿದೆ: ಡಿಎಪಿ (DAP) ಹೆಚ್ಚುವರಿ ಬಳಕೆಯನ್ನು ನಿಲ್ಲಿಸಿ, ಹಣ ಉಳಿಸಿ.")
            recs_en.append("High Phosphorus: Avoid additional DAP application to prevent soil fixation and save money.")
        else:
            status["P"] = "Medium (मध्यम / ಮಧ್ಯಮ)"
            recs_hi.append("फास्फोरस स्तर सामान्य है।")
            recs_kn.append("ರಂಜಕದ ಮಟ್ಟ ಸಾಮಾನ್ಯವಾಗಿದೆ.")
            recs_en.append("Phosphorus is in optimal medium range.")

        # Potassium (ICAR: Low < 140, Medium 140-280, High > 280 kg/ha)
        if k < 140.0:
            status["K"] = "Low (कम / ಕಡಿಮೆ)"
            recs_hi.append("पोटाश की कमी: पोटाश (MOP) डालें, यह पौधों को रोग प्रतिरोधक क्षमता और फलों में चमक देता है।")
            recs_kn.append("ಪೊಟ್ಯಾಷ್ ಕೊರತೆ: ಮ್ಯೂರಿಯೇಟ್ ಆಫ್ ಪೊಟ್ಯಾಷ್ (MOP) ಹಾಕಿ; ಇದು ರೋಗ ನಿರೋಧಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ.")
            recs_en.append("Low Potassium: Incorporate MOP to boost plant disease resistance and fruit firmness.")
        else:
            status["K"] = "Adequate (संतोषजनक / ತೃಪ್ತಿಕರ)"
            recs_hi.append("पोटाश संतोषजनक स्तर पर है।")
            recs_kn.append("ಪೊಟ್ಯಾಷ್ ಮಟ್ಟ ತೃಪ್ತಿಕರವಾಗಿದೆ.")
            recs_en.append("Potassium is adequate.")

        # pH (ICAR: Acidic < 6.5, Neutral 6.5-7.8, Alkaline > 8.0)
        if ph < 6.5:
            status["pH"] = "Acidic (अम्लीय / ಆಮ್ಲೀಯ)"
            recs_hi.append("मृदा अम्लीय है (pH < 6.5): बुवाई से पहले 200-300 किग्रा/हेक्टेयर बुझा हुआ चूना (Lime) मिलाएं।")
            recs_kn.append("ಮಣ್ಣು ಆಮ್ಲೀಯವಾಗಿದೆ (pH < 6.5): ಬಿತ್ತನೆಗೆ ಮುಂಚೆ ಹೆಕ್ಟೇರಿಗೆ 200-300 ಕೆಜಿ ಕೃಷಿ ಸುಣ್ಣವನ್ನು (Lime) ಮಣ್ಣಿನಲ್ಲಿ ಬೆರೆಸಿ.")
            recs_en.append("Acidic Soil (pH < 6.5): Apply agricultural lime or dolomite @ 250 kg/ha prior to sowing to correct acidity.")
        elif ph > 8.0:
            status["pH"] = "Alkaline (क्षारीय / ಕ್ಷಾರೀಯ)"
            recs_hi.append("मृदा क्षारीय है (pH > 8.0): 400-500 किग्रा/हेक्टेयर जिप्सम डालें और ढैंचा जैसी हरी खाद उगाएं।")
            recs_kn.append("ಮಣ್ಣು ಕ್ಷಾರೀಯವಾಗಿದೆ (pH > 8.0): ಹೆಕ್ಟೇರಿಗೆ 400-500 ಕೆಜಿ ಜಿಪ್ಸಮ್ ಹಾಕಿ ಮತ್ತು ಹಸಿರೆಲೆ ಗೊಬ್ಬರ ಬಳಸಿ.")
            recs_en.append("Alkaline Soil (pH > 8.0): Apply agricultural gypsum @ 500 kg/ha and cultivate green manure (Dhaincha).")
        else:
            status["pH"] = "Neutral (उदासीन / ತಟಸ್ಥ - ಅತ್ಯುತ್ತಮ)"
            recs_hi.append("मृदा का pH आदर्श है। सभी पोषक तत्वों का अवशोषण सुचारू रहेगा।")
            recs_kn.append("ಮಣ್ಣಿನ pH ಆದರ್ಶ ಮಟ್ಟದಲ್ಲಿದೆ. ಪೋಷಕಾಂಶಗಳ ಹೀರಿಕೊಳ್ಳುವಿಕೆ ಅತ್ಯುತ್ತಮವಾಗಿರುತ್ತದೆ.")
            recs_en.append("Soil pH is ideal. Nutrient uptake efficiency is optimal.")

        return {
            "status": status,
            "recommendations_hi": recs_hi,
            "recommendations_kn": recs_kn,
            "recommendations_en": recs_en
        }

