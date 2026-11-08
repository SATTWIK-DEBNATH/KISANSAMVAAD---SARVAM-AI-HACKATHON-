"""
KisanSamvaad - Typed Data Schemas
Zero third-party dependencies; uses Python standard dataclasses for fast instantiation and low RAM footprint.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

@dataclass
class ProvenanceCitation:
    """Document provenance for RAG groundings."""
    document_id: str
    title: str
    institution: str
    publication_date: str
    document_version: str
    source_url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class GuardrailResult:
    """Deterministic ICAR guardrail verification results."""
    is_safe: bool
    violations: List[str] = field(default_factory=list)
    cautions: List[str] = field(default_factory=list)
    safety_notice_present: bool = True
    verified_by: str = "ICAR-Grounded AgriGuardrail Engine"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SoilCardExtraction:
    """Soil Health Card extracted data and agronomic evaluation."""
    card_id: str
    farmer_name: str
    village: str
    district: str
    state: str
    nitrogen_kg_ha: float
    phosphorus_kg_ha: float
    potassium_kg_ha: float
    ph: float
    organic_carbon_pct: float
    zinc_ppm: float
    boron_ppm: float
    extraction_confidence: float
    confidence_ratings: Dict[str, float] = field(default_factory=dict)
    status: Dict[str, str] = field(default_factory=dict)
    recommendations_hi: List[str] = field(default_factory=list)
    recommendations_kn: List[str] = field(default_factory=list)
    recommendations_en: List[str] = field(default_factory=list)
    savings_estimate_inr: str = "₹3,200 - ₹4,800 per acre"
    provenance: Optional[ProvenanceCitation] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

@dataclass
class MandiPriceRecord:
    """APMC Mandi commodity market rate."""
    market: str
    district: str
    state: str
    commodity: str
    variety: str
    unit: str
    min_price: float
    max_price: float
    modal_price: float
    date: str
    timestamp: str
    data_source_mode: str  # "LIVE" or "DEMO"
    source_note: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class WeatherDayAdvisory:
    """Day agricultural weather and spray advisory."""
    day: str
    temp: str
    humidity: str
    condition: str
    rain_chance: str
    wind_kmh: int
    is_spray_safe: bool
    spray_advisory: str
    agricultural_notes: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AdvisoryResponse:
    """Voice & Chat Advisory response structure."""
    query: str
    response: str
    language: str
    detected_intent: str
    crop: Optional[str]
    guardrails: GuardrailResult
    citations: List[ProvenanceCitation] = field(default_factory=list)
    audio_base64: Optional[str] = None
    audio_duration_sec: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

