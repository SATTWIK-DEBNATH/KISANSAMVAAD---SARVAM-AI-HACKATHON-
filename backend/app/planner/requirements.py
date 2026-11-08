"""
KisanSamvaad - Crop Nutrient Requirements Calculator
Determines target elemental Nitrogen, P2O5, and K2O based on crop dose tables,
soil test rating adjustment factors, and organic FYM alternatives.
"""

from typing import Dict, Any, Tuple, Optional
from .schemas import SoilValues
from .data_loader import PlannerDataLoader

# ICAR Soil fertility classification thresholds (kg/ha available nutrient)
SOIL_THRESHOLDS = {
    "nitrogen": {"low": 280.0, "medium": 560.0, "high": 700.0},
    "phosphorus": {"low": 10.0, "medium": 25.0, "high": 50.0},
    "potassium": {"low": 140.0, "medium": 280.0, "high": 450.0}
}

# Soil test adjustment factors applied to recommended doses
ADJUSTMENT_FACTORS = {
    "low": 1.25,        # +25% application to build soil reserves
    "medium": 1.00,     # Standard recommended dose
    "high": 0.75,       # -25% reduction to save money and avoid toxicity
    "very_high": 0.00   # 0% application; soil reserves are saturated
}

class RequirementsCalculator:
    """Calculates nutrient targets based on crop, area, and soil test results."""

    @classmethod
    def classify_nutrient(cls, nutrient: str, value: float) -> str:
        """Classifies a soil test value into low, medium, high, or very_high."""
        limits = SOIL_THRESHOLDS.get(nutrient.lower())
        if not limits:
            return "medium"

        if value < limits["low"]:
            return "low"
        elif value <= limits["medium"]:
            return "medium"
        elif value <= limits["high"]:
            return "high"
        else:
            return "very_high"

    @classmethod
    def classify_ph(cls, ph: float) -> Tuple[str, str]:
        """Returns pH classification and agronomic amendment note."""
        if ph < 6.5:
            return "acidic", "Soil is acidic (pH < 6.5). Apply Agricultural Lime 250 kg/ha before sowing to optimize fertilizer uptake."
        elif ph > 8.0:
            return "alkaline", "Soil is alkaline (pH > 8.0). Apply Gypsum 500 kg/ha and incorporate green manure (Dhaincha) to lower alkalinity."
        else:
            return "optimal", "Soil pH is in the optimal neutral range (6.5 to 7.8)."

    @classmethod
    def calculate_targets(
        cls,
        crop: str,
        area_hectares: float,
        soil: Optional[SoilValues] = None,
        card_recommendations: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculates required kg of N, P2O5, and K2O for the given area.
        Prefers card recommendations if provided.
        """
        dose_table = PlannerDataLoader.load_dose_table()
        crop_clean = crop.strip().lower()
        crop_spec = dose_table.get(crop_clean)

        if not crop_spec:
            # Check for partial match (e.g. "paddy (rice)" -> "paddy")
            for key in dose_table:
                if key in crop_clean or crop_clean in key:
                    crop_spec = dose_table[key]
                    crop_clean = key
                    break

        if not crop_spec:
            raise ValueError(f"Crop '{crop}' is not supported. Supported crops: {', '.join(dose_table.keys())}")

        rec_dose = crop_spec["recommended_dose_kg_ha"]
        base_n = rec_dose["nitrogen"]
        base_p = rec_dose["phosphorus_p2o5"]
        base_k = rec_dose["potassium_k2o"]

        ratings = {}
        factors = {"nitrogen": 1.0, "phosphorus": 1.0, "potassium": 1.0}
        ph_class, ph_note = ("untested", "")

        # If explicit card recommendations are present, prefer them
        if card_recommendations and isinstance(card_recommendations, dict):
            target_n = float(card_recommendations.get("nitrogen_kg", base_n * area_hectares))
            target_p = float(card_recommendations.get("phosphorus_p2o5_kg", base_p * area_hectares))
            target_k = float(card_recommendations.get("potassium_k2o_kg", base_k * area_hectares))
            source = "card"
        elif soil:
            ratings["nitrogen"] = cls.classify_nutrient("nitrogen", soil.nitrogen_kg_ha)
            ratings["phosphorus"] = cls.classify_nutrient("phosphorus", soil.phosphorus_kg_ha)
            ratings["potassium"] = cls.classify_nutrient("potassium", soil.potassium_kg_ha)
            ph_class, ph_note = cls.classify_ph(soil.ph)

            factors["nitrogen"] = ADJUSTMENT_FACTORS[ratings["nitrogen"]]
            factors["phosphorus"] = ADJUSTMENT_FACTORS[ratings["phosphorus"]]
            factors["potassium"] = ADJUSTMENT_FACTORS[ratings["potassium"]]

            target_n = base_n * factors["nitrogen"] * area_hectares
            target_p = base_p * factors["phosphorus"] * area_hectares
            target_k = base_k * factors["potassium"] * area_hectares
            source = "soil_card_adjusted"
        else:
            ratings = {"nitrogen": "medium", "phosphorus": "medium", "potassium": "medium"}
            target_n = base_n * area_hectares
            target_p = base_p * area_hectares
            target_k = base_k * area_hectares
            source = "standard_package_of_practices"

        # Organic alternative calculation
        org_spec = crop_spec.get("organic_dose", {})
        fym_per_ha = org_spec.get("fym_tonnes_ha", 10.0)
        total_fym_tonnes = round(fym_per_ha * area_hectares, 1)
        fym_credit_n = round(org_spec.get("fym_n_credit_kg", 15.0) * area_hectares, 1)
        fym_credit_p = round(org_spec.get("fym_p2o5_credit_kg", 7.5) * area_hectares, 1)
        fym_credit_k = round(org_spec.get("fym_k2o_credit_kg", 15.0) * area_hectares, 1)

        organic_info = {
            "material": "Farm Yard Manure (FYM)",
            "recommended_tonnes": total_fym_tonnes,
            "nutrient_credit_kg": {
                "n": fym_credit_n,
                "p2o5": fym_credit_p,
                "k2o": fym_credit_k
            },
            "note": "Organic manure improves soil water retention and organic carbon. Use as an alternative soil builder, not a 1:1 chemical substitute."
        }

        return {
            "crop_key": crop_clean,
            "crop_name": crop_spec["crop_name"],
            "area_hectares": round(area_hectares, 4),
            "source": source,
            "soil_ratings": ratings,
            "soil_adjustment_factors": factors,
            "ph_classification": ph_class,
            "ph_advisory_note": ph_note,
            "target_nutrients_kg": {
                "nitrogen_kg": round(target_n, 2),
                "phosphorus_p2o5_kg": round(target_p, 2),
                "potassium_k2o_kg": round(target_k, 2)
            },
            "organic_alternative": organic_info,
            "citation": crop_spec.get("citation", {})
        }

