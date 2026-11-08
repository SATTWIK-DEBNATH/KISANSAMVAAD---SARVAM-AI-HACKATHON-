"""
KisanSamvaad - Land Area Unit Converter
Standardizes land measurements across Indian agricultural units (Acre, Hectare, Gunta, Bigha).
Allows configurable guntas-per-acre ratios across states.
"""

from typing import Dict, Any

# Standard international conversion
ACRE_TO_HECTARE_FACTOR = 0.404686
HECTARE_TO_ACRE_FACTOR = 1.0 / ACRE_TO_HECTARE_FACTOR  # ~2.47105

# State-wise customary units configuration
STATE_GUNTAS_PER_ACRE: Dict[str, float] = {
    "karnataka": 40.0,
    "maharashtra": 40.0,
    "andhra pradesh": 40.0,
    "telangana": 40.0,
    "gujarat": 40.0,
    "default": 40.0
}

# Regional Bigha variations (in acres)
STATE_ACRES_PER_BIGHA: Dict[str, float] = {
    "uttar pradesh": 0.625,  # 1 Pucca Bigha ~ 0.625 acre (approx 5/8 acre)
    "punjab": 0.20,          # 1 Bigha = 0.2 acre (1 acre = 5 bighas)
    "haryana": 0.20,
    "bihar": 0.625,
    "rajasthan": 0.625,
    "default": 0.625
}

class UnitConverter:
    """Converts farmer-entered land measurements into standardized hectares and acres."""

    @classmethod
    def get_guntas_per_acre(cls, state: str = "Karnataka") -> float:
        st_clean = state.strip().lower()
        return STATE_GUNTAS_PER_ACRE.get(st_clean, STATE_GUNTAS_PER_ACRE["default"])

    @classmethod
    def to_hectares(cls, area: float, unit: str, state: str = "Karnataka") -> float:
        """Converts any recognized land measurement to metric hectares."""
        if area <= 0:
            return 0.0

        u = unit.strip().lower()
        if u in ("hectare", "hectares", "ha"):
            return float(area)

        if u in ("acre", "acres", "ac"):
            return float(area) * ACRE_TO_HECTARE_FACTOR

        if u in ("gunta", "guntas", "guntha", "gunthas"):
            guntas_per_acre = cls.get_guntas_per_acre(state)
            acres = float(area) / guntas_per_acre
            return acres * ACRE_TO_HECTARE_FACTOR

        if u in ("bigha", "bighas"):
            st_clean = state.strip().lower()
            acres_per_bigha = STATE_ACRES_PER_BIGHA.get(st_clean, STATE_ACRES_PER_BIGHA["default"])
            acres = float(area) * acres_per_bigha
            return acres * ACRE_TO_HECTARE_FACTOR

        # Default fallback assumes acres
        return float(area) * ACRE_TO_HECTARE_FACTOR

    @classmethod
    def to_acres(cls, area: float, unit: str, state: str = "Karnataka") -> float:
        """Converts any recognized land measurement to standard acres."""
        if area <= 0:
            return 0.0

        u = unit.strip().lower()
        if u in ("acre", "acres", "ac"):
            return float(area)

        if u in ("hectare", "hectares", "ha"):
            return float(area) * HECTARE_TO_ACRE_FACTOR

        if u in ("gunta", "guntas", "guntha", "gunthas"):
            guntas_per_acre = cls.get_guntas_per_acre(state)
            return float(area) / guntas_per_acre

        if u in ("bigha", "bighas"):
            st_clean = state.strip().lower()
            acres_per_bigha = STATE_ACRES_PER_BIGHA.get(st_clean, STATE_ACRES_PER_BIGHA["default"])
            return float(area) * acres_per_bigha

        return float(area)
