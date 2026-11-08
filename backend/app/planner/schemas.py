"""
KisanSamvaad - Soil-to-Rupee Planner Typed Schemas
Defines input validation contracts, nutrient requirements, optimizer bag allocations,
timing schedules, and localized narration payloads.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

class ValidationError(Exception):
    """Custom exception raised when plan inputs fail boundary checks."""
    def __init__(self, message: str, field_name: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.field_name = field_name

@dataclass
class SoilValues:
    """Soil test parameters extracted from Soil Health Card or edited by farmer."""
    nitrogen_kg_ha: float
    phosphorus_kg_ha: float
    potassium_kg_ha: float
    ph: float
    organic_carbon_pct: Optional[float] = 0.50
    zinc_ppm: Optional[float] = 0.60
    boron_ppm: Optional[float] = 0.50

    def validate(self):
        if self.nitrogen_kg_ha < 0 or self.nitrogen_kg_ha > 2000:
            raise ValidationError("Nitrogen must be between 0 and 2000 kg/ha", "nitrogen_kg_ha")
        if self.phosphorus_kg_ha < 0 or self.phosphorus_kg_ha > 500:
            raise ValidationError("Phosphorus must be between 0 and 500 kg/ha", "phosphorus_kg_ha")
        if self.potassium_kg_ha < 0 or self.potassium_kg_ha > 1500:
            raise ValidationError("Potassium must be between 0 and 1500 kg/ha", "potassium_kg_ha")
        if self.ph < 2.0 or self.ph > 12.0:
            raise ValidationError("Soil pH must be between 2.0 and 12.0", "ph")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class LocationInput:
    """Geographic location for agro-climatic zone and weather forecast."""
    lat: Optional[float] = 13.1367
    lon: Optional[float] = 78.1348
    taluk: Optional[str] = "Kolar"
    state: Optional[str] = "Karnataka"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PlanRequest:
    """Incoming request contract for POST /api/v1/soil-plan."""
    crop: str
    area: float
    unit: str = "acre"
    state: str = "Karnataka"
    soil_values: Optional[SoilValues] = None
    card_recommendations: Optional[Dict[str, Any]] = None
    location: Optional[LocationInput] = None
    language: str = "kn"
    include_organic_alternative: bool = True

    def validate(self):
        if not self.crop or not self.crop.strip():
            raise ValidationError("Crop is required", "crop")
        if self.area <= 0:
            raise ValidationError("Land area must be greater than zero", "area")
        if self.area > 500:
            raise ValidationError("Land area exceeds supported individual farm limit (500 units)", "area")
        valid_units = ("acre", "hectare", "ha", "gunta", "guntas")
        if self.unit.lower() not in valid_units:
            raise ValidationError(f"Invalid unit '{self.unit}'. Supported units: acre, hectare, gunta", "unit")
        if self.soil_values:
            self.soil_values.validate()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlanRequest":
        soil_raw = data.get("soil_values")
        soil_obj = None
        if soil_raw and isinstance(soil_raw, dict):
            soil_obj = SoilValues(
                nitrogen_kg_ha=float(soil_raw.get("nitrogen_kg_ha", 280.0)),
                phosphorus_kg_ha=float(soil_raw.get("phosphorus_kg_ha", 15.0)),
                potassium_kg_ha=float(soil_raw.get("potassium_kg_ha", 180.0)),
                ph=float(soil_raw.get("ph", 6.8)),
                organic_carbon_pct=float(soil_raw.get("organic_carbon_pct", 0.50)),
                zinc_ppm=float(soil_raw.get("zinc_ppm", 0.60)),
                boron_ppm=float(soil_raw.get("boron_ppm", 0.50))
            )
        loc_raw = data.get("location")
        loc_obj = None
        if loc_raw and isinstance(loc_raw, dict):
            loc_obj = LocationInput(
                lat=float(loc_raw.get("lat", 13.1367)),
                lon=float(loc_raw.get("lon", 78.1348)),
                taluk=str(loc_raw.get("taluk", "Kolar")),
                state=str(loc_raw.get("state", "Karnataka"))
            )

        req = cls(
            crop=str(data.get("crop", "")).strip().lower(),
            area=float(data.get("area", 1.0)),
            unit=str(data.get("unit", "acre")).strip().lower(),
            state=str(data.get("state", "Karnataka")),
            soil_values=soil_obj,
            card_recommendations=data.get("card_recommendations"),
            location=loc_obj,
            language=str(data.get("language", "kn")),
            include_organic_alternative=bool(data.get("include_organic_alternative", True))
        )
        req.validate()
        return req

@dataclass
class BagItem:
    """Commercial fertilizer bag allocation result."""
    fertilizer_id: str
    name: str
    bag_size_kg: float
    bags_count: int
    total_kg: float
    price_per_bag_inr: float
    total_cost_inr: float
    nutrients_supplied_kg: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class TimingStage:
    """Application split timing stage (e.g. basal vs top dress)."""
    stage: str
    timing_description: str
    action: str
    weather_safe: bool
    weather_advisory: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PlanResult:
    """Complete response payload for POST /api/v1/soil-plan."""
    inputs_echo: Dict[str, Any]
    nutrient_requirements_kg: Dict[str, float]
    fertilizer_plan: Dict[str, Any]
    organic_alternative: Optional[Dict[str, Any]]
    timing_schedule: List[Dict[str, Any]]
    weather_warning: Dict[str, Any]
    citations: List[Dict[str, Any]]
    spoken_narration: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
