"""
KisanSamvaad - Government Agricultural Schemes Intelligence Service
Provides deep scheme catalog, eligibility assessment rules, and
required documentation checklists for Indian and Karnataka farmers.
"""

from typing import Dict, Any, List, Optional
from ..db.repository import repository

SCHEMES_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "pm_kisan",
        "code": "PM_KISAN",
        "name_en": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "name_hi": "पीएम-किसान (प्रधानमंत्री किसान सम्मान निधि)",
        "name_kn": "ಪಿಎಂ-ಕಿಸಾನ್ (ಪ್ರಧಾನಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ)",
        "category": "Direct Income Support",
        "benefit_summary": "₹6,000 per year transferred directly to bank accounts in 3 equal installments of ₹2,000.",
        "portal_url": "https://pmkisan.gov.in",
        "required_documents": [
            "Aadhaar Card linked with active bank account",
            "Land Record (Pahani / RTC / Khatauni)",
            "Bank Passbook with IFSC code",
            "Active mobile number for OTP e-KYC"
        ],
        "eligibility_rules": {
            "max_land_acres": None,
            "min_land_acres": 0.05,
            "requires_cultivable_land": True,
            "applicable_states": ["ALL"]
        }
    },
    {
        "id": "pmfby",
        "code": "PMFBY",
        "name_en": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
        "name_hi": "पीएमएफबीवाई (प्रधानमंत्री फसल बीमा योजना)",
        "name_kn": "ಪಿಎಂಎಫ್‌ಬಿವೈ (ಪ್ರಧಾನಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ)",
        "category": "Crop Insurance",
        "benefit_summary": "Comprehensive risk coverage from pre-sowing to post-harvest against drought, flood, pests, and unseasonal rainfall. Farmer premium: 1.5% for Rabi, 2.0% for Kharif, 5.0% for commercial/horticulture.",
        "portal_url": "https://pmfby.gov.in",
        "required_documents": [
            "Land Record (Pahani / RTC)",
            "Crop Sowing Certificate issued by Village Administrative Officer (VAO)",
            "Aadhaar Card",
            "Cancelled Cheque / Bank Passbook"
        ],
        "eligibility_rules": {
            "max_land_acres": None,
            "min_land_acres": 0.1,
            "requires_notified_crop": True,
            "applicable_states": ["ALL"]
        }
    },
    {
        "id": "kcc",
        "code": "KCC",
        "name_en": "Kisan Credit Card (KCC) Concessional Loan",
        "name_hi": "किसान क्रेडिट कार्ड (केसीसी) रियायती ऋण",
        "name_kn": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (ಕೆಸಿಸಿ) ರಿಯಾಯಿತಿ ಸಾಲ",
        "category": "Institutional Credit",
        "benefit_summary": "Credit limit up to ₹3,00,000 at an effective interest rate of 4% per annum (with 3% prompt repayment subvention).",
        "portal_url": "https://www.myscheme.gov.in/schemes/kcc",
        "required_documents": [
            "Land Ownership Records (RTC / Pahani / 7/12 extract)",
            "Identity Proof (Aadhaar / Voter ID)",
            "Address Proof",
            "Passport-size photographs",
            "No Dues Certificate from nearby bank branches"
        ],
        "eligibility_rules": {
            "max_land_acres": None,
            "min_land_acres": 0.5,
            "requires_cultivable_land": True,
            "applicable_states": ["ALL"]
        }
    },
    {
        "id": "raita_siri",
        "code": "RAITA_SIRI",
        "name_en": "Karnataka Raita Siri Scheme (Millet Incentive)",
        "name_hi": "कर्नाटक रायता सिरी योजना (श्रीअन्न मिलेट प्रोत्साहन)",
        "name_kn": "ಕರ್ನಾಟಕ ರೈತ ಸಿರಿ ಯೋಜನೆ (ಸಿರಿಧಾನ್ಯ ಪ್ರೋತ್ಸಾಹಧನ)",
        "category": "State Crop Incentive",
        "benefit_summary": "Direct incentive of ₹10,000 per hectare (up to a maximum of 2 hectares / ₹20,000) for cultivating notified millets (Ragi, Jowar, Bajra, Foxtail, Little millet).",
        "portal_url": "https://raitamitra.karnataka.gov.in",
        "required_documents": [
            "Karnataka Pahani / RTC showing millet cultivation",
            "FID (Farmer Identification Number) from FRUITS portal",
            "Aadhaar-linked Bank Account",
            "Caste Certificate (if claiming special category benefits)"
        ],
        "eligibility_rules": {
            "max_land_acres": 5.0,
            "min_land_acres": 0.5,
            "required_crops": ["millet", "ragi", "jowar", "bajra", "foxtail", "siridhanya"],
            "applicable_states": ["karnataka", "ka"]
        }
    },
    {
        "id": "pm_kusum",
        "code": "PM_KUSUM",
        "name_en": "PM-KUSUM (Solar Agricultural Pumpsets)",
        "name_hi": "पीएम-कुसुम (सौर कृषि पंप योजना)",
        "name_kn": "ಪಿಎಂ-ಕುಸುಮ್ (ಸೌರ ಕೃಷಿ ಪಂಪ್‌ಸೆಟ್ ಯೋಜನೆ)",
        "category": "Clean Energy & Irrigation",
        "benefit_summary": "Up to 60% combined subsidy (30% Central + 30% State) for replacing diesel or installing standalone off-grid solar agricultural pumps (3HP to 7.5HP).",
        "portal_url": "https://pmkusum.mnre.gov.in",
        "required_documents": [
            "Land RTC / Pahani",
            "Aadhaar Card",
            "Water Source Certificate / Borewell yield test report",
            "Bank Passbook"
        ],
        "eligibility_rules": {
            "max_land_acres": None,
            "min_land_acres": 1.0,
            "requires_water_source": True,
            "applicable_states": ["ALL"]
        }
    },
    {
        "id": "shc_scheme",
        "code": "SHC_SCHEME",
        "name_en": "Soil Health Card Scheme",
        "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
        "name_kn": "ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ ಯೋಜನೆ",
        "category": "Soil & Nutrient Advisory",
        "benefit_summary": "Free comprehensive 12-parameter soil testing and scientific fertilizer advisory issued every 2 years by State Agriculture Department / KVK.",
        "portal_url": "https://soilhealth.dac.gov.in",
        "required_documents": [
            "Survey Number / Plot details",
            "Aadhaar Card",
            "Mobile number"
        ],
        "eligibility_rules": {
            "max_land_acres": None,
            "min_land_acres": 0.1,
            "applicable_states": ["ALL"]
        }
    }
]

class SchemeIntelligenceService:
    """Manages scheme discovery and personalized eligibility evaluations."""

    @classmethod
    def list_all_schemes(cls) -> List[Dict[str, Any]]:
        return SCHEMES_CATALOG

    @classmethod
    def evaluate_eligibility(
        cls,
        farmer_name: str,
        landholding_acres: float,
        state: str = "Karnataka",
        district: Optional[str] = "Kolar",
        crops: Optional[List[str]] = None,
        irrigation_source: Optional[str] = "Borewell"
    ) -> Dict[str, Any]:
        """
        Evaluates farmer qualification for central and state agricultural schemes.
        """
        crops_clean = [c.strip().lower() for c in (crops or [])]
        state_clean = state.strip().lower()

        evaluations = []
        for s in SCHEMES_CATALOG:
            rules = s["eligibility_rules"]
            eligible = True
            reasons = []

            # Check state applicability
            app_states = [st.lower() for st in rules.get("applicable_states", ["all"])]
            if "all" not in app_states and state_clean not in app_states:
                eligible = False
                state_names = [st.title() for st in rules.get("applicable_states", [])]
                reasons.append(f"Scheme is restricted to {', '.join(state_names)}.")

            # Check minimum landholding
            min_land = rules.get("min_land_acres")
            if min_land and landholding_acres < min_land:
                eligible = False
                reasons.append(f"Requires at least {min_land} acres of cultivable land (you hold {landholding_acres} acres).")

            # Check maximum landholding
            max_land = rules.get("max_land_acres")
            if max_land and landholding_acres > max_land:
                eligible = False
                reasons.append(f"Restricted to small/marginal farmers with up to {max_land} acres.")

            # Check specific crop requirement (e.g. Karnataka Raita Siri millets)
            req_crops = rules.get("required_crops")
            if req_crops:
                has_crop = any(any(rc in c for rc in req_crops) for c in crops_clean) if crops_clean else False
                if not has_crop:
                    eligible = False
                    reasons.append(f"Requires cultivation of notified crops: {', '.join(req_crops)}.")

            status = "Eligible" if eligible else "Ineligible"
            evaluations.append({
                "scheme_id": s["id"],
                "scheme_name": s["name_en"],
                "scheme_name_kn": s["name_kn"],
                "scheme_name_hi": s["name_hi"],
                "category": s["category"],
                "benefit_summary": s["benefit_summary"],
                "eligibility_status": status,
                "reasons": reasons if not eligible else ["Farmer profile fully meets scheme qualification criteria."],
                "portal_url": s["portal_url"],
                "required_documents": s["required_documents"]
            })

        eligible_count = sum(1 for e in evaluations if e["eligibility_status"] == "Eligible")

        return {
            "farmer_name": farmer_name,
            "evaluated_parameters": {
                "landholding_acres": landholding_acres,
                "state": state,
                "district": district,
                "crops": crops or [],
                "irrigation_source": irrigation_source
            },
            "eligible_schemes_count": eligible_count,
            "total_schemes_reviewed": len(evaluations),
            "scheme_evaluations": evaluations
        }
