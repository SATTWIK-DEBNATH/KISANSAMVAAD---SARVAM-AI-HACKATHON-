"""
KisanSamvaad - Agronomic Knowledge Base & Grounded Retrieval
Curated ICAR advisories, crop disease solutions, soil health diagnostics,
and live mandi benchmarks across Indian agricultural states.
"""

from typing import Dict, Any, List, Optional

# Verified Agricultural Advisories
CROP_DISEASES: Dict[str, Dict[str, Any]] = {
    "cotton_yellow_leaves": {
        "crop": "Cotton (कपास)",
        "symptoms": ["yellowing of leaves", "stunted growth", "leaf curling"],
        "cause": "Magnesium deficiency or Sucking Pests (Whitefly / Jassids)",
        "solution_hi": (
            "कपास में पत्तियां पीली होने के दो मुख्य कारण हैं: \n"
            "1. मैग्नीशियम की कमी: इसके लिए 1% मैग्नीशियम सल्फेट (10 ग्राम प्रति लीटर पानी) का छिड़काव करें।\n"
            "2. रस चूसक कीट (सफेद मक्खी/एफिड): इसके नियंत्रण के लिए नीम का तेल 5ml प्रति लीटर या इमिडाक्लोप्रिड 17.8% SL (0.5ml प्रति लीटर) का छिड़काव करें। तेज धूप में छिड़काव न करें।"
        ),
        "solution_en": (
            "Yellowing of cotton leaves typically occurs due to: \n"
            "1. Magnesium Deficiency: Spray 1% Magnesium Sulphate (10g per liter of water).\n"
            "2. Sucking Pests (Whitefly/Jassid): Spray Neem oil (5ml/L) or Imidacloprid 17.8% SL (0.5ml/L). Avoid spraying during peak afternoon heat."
        ),
        "safe_chemicals": ["Magnesium Sulphate", "Neem Oil", "Imidacloprid 17.8% SL"]
    },
    "wheat_yellow_rust": {
        "crop": "Wheat (गेहूं)",
        "symptoms": ["yellow powder on leaves", "stripes along veins", "pili gerui"],
        "cause": "Yellow Rust (Puccinia striiformis)",
        "solution_hi": (
            "गेहूं में पीली रतुआ (Yellow Rust) की पहचान होते ही: \n"
            "1. प्रोपिकोनाजोल 25% EC (टिल्ट) का 1ml प्रति लीटर पानी (200ml प्रति एकड़) की दर से तुरंत छिड़काव करें।\n"
            "2. मौसम में नमी और ठंड होने पर यह तेजी से फैलता है, इसलिए खेत की तुरंत निगरानी करें।"
        ),
        "solution_en": (
            "For Yellow Rust in Wheat: \n"
            "1. Immediately spray Propiconazole 25% EC @ 1ml per liter of water (200ml per acre).\n"
            "2. High moisture and cool temperatures accelerate spread; inspect field perimeter promptly."
        ),
        "safe_chemicals": ["Propiconazole 25% EC"]
    },
    "paddy_blast": {
        "crop": "Paddy / Rice (धान)",
        "symptoms": ["spindle-shaped lesions", "gray centers", "neck rot"],
        "cause": "Blast Fungus (Magnaporthe oryzae)",
        "solution_hi": (
            "धान के ब्लास्ट (झुलसा रोग) के लिए: \n"
            "1. ट्राईसाइक्लाजोल 75% WP (0.6 ग्राम प्रति लीटर) या कासुगामाइसिन (2ml प्रति लीटर) का छिड़काव करें।\n"
            "2. नाइट्रोजन खाद (यूरिया) का अत्यधिक उपयोग तुरंत रोकें।"
        ),
        "solution_en": (
            "For Rice Blast Disease: \n"
            "1. Spray Tricyclazole 75% WP (0.6g/L) or Kasugamycin (2ml/L).\n"
            "2. Suspend excessive application of nitrogen (Urea) immediately."
        ),
        "safe_chemicals": ["Tricyclazole 75% WP"]
    },
    "tomato_blight": {
        "crop": "Tomato (ಟೊಮ್ಯಾಟೊ / टमाटर)",
        "symptoms": ["dark water-soaked spots", "fruit rotting", "wilting", "ಹಳದಿ", "ಸುರುಟಿಕೊಳ್ಳುವುದು", "yellowing"],
        "cause": "Early / Late Blight or Leaf Curl",
        "solution_kn": (
            "ಟೊಮ್ಯಾಟೊ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಕಂದು ಅಥವಾ ಹಳದಿಯಾಗುತ್ತಿದ್ದರೆ (Blight / Leaf Curl): \n"
            "1. ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (ಪ್ರತಿ ಲೀಟರ್ ನೀರಿಗೆ 2.5 ಗ್ರಾಂ) ಅಥವಾ ತಾಮ್ರದ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (3 ಗ್ರಾಂ/ಲೀಟರ್) ಸಿಂಪಡಿಸಿ.\n"
            "2. ಹಾನಿಗೊಳಗಾದ ಎಲೆಗಳನ್ನು ತಕ್ಷಣ ಕಿತ್ತು ನಾಶಮಾಡಿ. ಬಿಳಿ ನೊಣ ನಿಯಂತ್ರಣಕ್ಕೆ ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲಿ/ಲೀಟರ್) ಸಿಂಪಡಿಸಿ."
        ),
        "solution_hi": (
            "टमाटर में झुलसा (Blight) रोग के लिए: \n"
            "1. मैंकोजेब 75% WP (2.5 ग्राम प्रति लीटर) या कॉपर ऑक्सीक्लोराइड 50% WP (3 ग्राम प्रति लीटर) का छिड़काव करें।\n"
            "2. रोगग्रस्त पत्तियों को तोड़कर खेत से दूर नष्ट करें।"
        ),
        "solution_en": (
            "For Tomato Blight: \n"
            "1. Spray Mancozeb 75% WP (2.5g/L) or Copper Oxychloride 50% WP (3g/L).\n"
            "2. Prune and destroy infected leaves away from the field."
        ),
        "safe_chemicals": ["Mancozeb 75% WP", "Copper Oxychloride", "Neem Oil"]
    }
}

# Real-time / Benchmarked Mandi Prices (APMC benchmarks across India including Karnataka)
MANDI_PRICES: List[Dict[str, Any]] = [
    {"commodity": "Tomato (ಟೊಮ್ಯಾಟೊ)", "variety": "Hybrid Red", "mandi": "Kolar APMC (Karnataka)", "modal_price": 1780, "min_price": 1400, "max_price": 2100, "unit": "₹/Quintal", "trend": "+3.5%"},
    {"commodity": "Potato (ಆಲೂಗಡ್ಡೆ)", "variety": "Hassan Fresh", "mandi": "Yeshwanthpur APMC, Bengaluru (Karnataka)", "modal_price": 1620, "min_price": 1350, "max_price": 1850, "unit": "₹/Quintal", "trend": "+1.2%"},
    {"commodity": "Cotton (ಹತ್ತಿ)", "variety": "DCH-32 Long Staple", "mandi": "Raichur APMC (Karnataka)", "modal_price": 7450, "min_price": 7000, "max_price": 7800, "unit": "₹/Quintal", "trend": "+2.1%"},
    {"commodity": "Arecanut (ಅಡಿಕೆ)", "variety": "Rashi / Chali", "mandi": "Shimoga APMC (Karnataka)", "modal_price": 46500, "min_price": 43000, "max_price": 49000, "unit": "₹/Quintal", "trend": "+0.8%"},
    {"commodity": "Wheat (गेहूं)", "variety": "Sharbati / Lokwan", "mandi": "Khanna (Punjab)", "modal_price": 2420, "min_price": 2275, "max_price": 2550, "unit": "₹/Quintal", "trend": "+1.8%"},
    {"commodity": "Wheat (गेहूं)", "variety": "Mill Quality", "mandi": "Neemuch (MP)", "modal_price": 2380, "min_price": 2220, "max_price": 2490, "unit": "₹/Quintal", "trend": "+0.5%"},
    {"commodity": "Paddy / Rice (धान)", "variety": "Basmati 1121", "mandi": "Karnal (Haryana)", "modal_price": 4150, "min_price": 3800, "max_price": 4350, "unit": "₹/Quintal", "trend": "-0.7%"},
    {"commodity": "Cotton (कपास)", "variety": "Medium Staple", "mandi": "Rajkot (Gujarat)", "modal_price": 7250, "min_price": 6800, "max_price": 7600, "unit": "₹/Quintal", "trend": "+2.4%"},
    {"commodity": "Mustard (सरसों)", "variety": "Black Mustard", "mandi": "Bharatpur (Rajasthan)", "modal_price": 5650, "min_price": 5300, "max_price": 5850, "unit": "₹/Quintal", "trend": "+1.1%"},
    {"commodity": "Soybean (सोयाबीन)", "variety": "Yellow Soybean", "mandi": "Indore (MP)", "modal_price": 4820, "min_price": 4500, "max_price": 4980, "unit": "₹/Quintal", "trend": "+0.3%"},
    {"commodity": "Onion (प्याज)", "variety": "Red Nashik", "mandi": "Lasalgaon (Maharashtra)", "modal_price": 1850, "min_price": 1400, "max_price": 2200, "unit": "₹/Quintal", "trend": "-3.2%"},
    {"commodity": "Potato (आलू)", "variety": "Jyoti / Kufri", "mandi": "Agra (UP)", "modal_price": 1420, "min_price": 1150, "max_price": 1600, "unit": "₹/Quintal", "trend": "+4.1%"}
]

# Soil Health Diagnostic Framework
def diagnose_soil_sample(n: float, p: float, k: float, ph: float) -> Dict[str, Any]:
    """
    Evaluates soil parameters against ICAR standard fertility benchmarks:
    - Nitrogen (N): Low < 280 kg/ha, Medium 280-560 kg/ha, High > 560 kg/ha
    - Phosphorus (P): Low < 10 kg/ha, Medium 10-25 kg/ha, High > 25 kg/ha
    - Potassium (K): Low < 110 kg/ha, Medium 110-280 kg/ha, High > 280 kg/ha
    - pH: Acidic < 6.5, Neutral 6.5-7.5, Alkaline > 7.5
    """
    status_n = "Low (कम)" if n < 280 else ("Medium (मध्यम)" if n <= 560 else "High (अधिक)")
    status_p = "Low (कम)" if p < 10 else ("Medium (मध्यम)" if p <= 25 else "High (अधिक)")
    status_k = "Low (कम)" if k < 110 else ("Medium (मध्यम)" if k <= 280 else "High (अधिक)")
    
    ph_status = "Acidic (अम्लीय)" if ph < 6.5 else ("Neutral (संतुलित)" if ph <= 7.5 else "Alkaline (क्षारीय)")
    
    recommendations_hi = []
    recommendations_en = []

    # Nitrogen adjustment
    if n < 280:
        recommendations_hi.append("नाइट्रोजन की कमी है: यूरिया या वर्मीकम्पोस्ट (केंचुआ खाद) की मात्रा 20% बढ़ाएं।")
        recommendations_en.append("Nitrogen is deficient: Increase Urea or vermicompost by 20%.")
    elif n > 560:
        recommendations_hi.append("नाइट्रोजन अत्यधिक है: यूरिया का प्रयोग 25% कम करें ताकि कीटों का प्रकोप न बढ़े।")
        recommendations_en.append("Excess Nitrogen: Reduce Urea by 25% to prevent insect susceptibility.")

    # Phosphorus adjustment
    if p < 10:
        recommendations_hi.append("फास्फोरस कम है: बुवाई के समय DAP (डाय अमोनियम फास्फेट) या सिंगल सुपर फास्फेट (SSP) का प्रयोग करें।")
        recommendations_en.append("Phosphorus is low: Apply DAP or Single Super Phosphate (SSP) at basal sowing.")

    # Potassium adjustment
    if k < 110:
        recommendations_hi.append("पोटाश की कमी है: MOP (म्यूरिएट ऑफ पोटाश) 25-30 किग्रा प्रति एकड़ डालें, जिससे दाने चमकदार और रोगरोधी बनें।")
        recommendations_en.append("Potassium deficient: Apply MOP @ 25-30 kg/acre to boost grain luster and disease resistance.")

    # pH adjustment
    if ph < 6.5:
        recommendations_hi.append(f"मिट्टी अम्लीय है (pH {ph}): बुवाई से 3 सप्ताह पहले 200-300 किग्रा चूना (Agricultural Lime) प्रति एकड़ मिलाएं।")
        recommendations_en.append(f"Soil is acidic (pH {ph}): Incorporate Agricultural Lime @ 250 kg/acre 3 weeks before sowing.")
    elif ph > 8.0:
        recommendations_hi.append(f"मिट्टी क्षारीय/ऊसर है (pH {ph}): खेत में जिप्सम (Gypsum) और हरी खाद (ढैंचा) का प्रयोग करें।")
        recommendations_en.append(f"Soil is alkaline/sodic (pH {ph}): Apply Gypsum and green manuring (Dhaincha) to restore soil balance.")

    return {
        "metrics": {"N": n, "P": p, "K": k, "pH": ph},
        "status": {"N": status_n, "P": status_p, "K": status_k, "pH": ph_status},
        "recommendations_hi": recommendations_hi,
        "recommendations_en": recommendations_en
    }

# Government Scheme Guidelines
GOVERNMENT_SCHEMES = [
    {
        "id": "pm_kisan",
        "name_hi": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)",
        "name_en": "PM-KISAN Samman Nidhi",
        "benefit": "₹6,000 annually in 3 equal installments directly into bank account (DBT).",
        "eligibility": "All landholding farmer families with cultivable land in their names.",
        "documents_required": ["Aadhaar Card", "Land Record (Khasra/Khatauni)", "Bank Account linked with Aadhaar"]
    },
    {
        "id": "pmfby",
        "name_hi": "प्रधानमंत्री फसल बीमा योजना (PMFBY)",
        "name_en": "Pradhan Mantri Fasal Bima Yojana",
        "benefit": "Comprehensive crop insurance against natural calamities, pests, and drought at nominal premium (1.5% - 2%).",
        "eligibility": "All farmers growing notified crops in notified areas.",
        "documents_required": ["Sowing Certificate", "Land Patta / ROR", "Bank Passbook"]
    },
    {
        "id": "kcc",
        "name_hi": "किसान क्रेडिट कार्ड (KCC)",
        "name_en": "Kisan Credit Card Scheme",
        "benefit": "Concessional institutional crop loan up to ₹3 Lakh at an effective interest rate of 4% per annum.",
        "eligibility": "Owner cultivators, tenant farmers, oral lessees & SHGs.",
        "documents_required": ["Land ownership proof", "ID & Address proof", "Crop cultivation record"]
    }
]

