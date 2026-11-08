"""
KisanSamvaad - Deterministic Net Realisation Economic Calculator
Enables farmers to calculate true take-home earnings by deducting transport,
labor, market fees, packaging, and spoilage losses across competing mandis.
"""

from typing import Dict, Any, List, Optional
from ..schemas.models import MandiPriceRecord

class NetRealisationCalculator:
    """Calculates true net farmer realization and compares market options."""

    @staticmethod
    def calculate_single_mandi(
        market_name: str,
        commodity: str,
        quantity_quintals: float,
        modal_price_per_quintal: float,
        distance_km: float,
        transport_rate_per_km: float = 25.0,
        labor_rate_per_quintal: float = 30.0,
        mandi_commission_pct: float = 2.0,
        packaging_rate_per_quintal: float = 40.0,
        spoilage_pct: float = 2.0
    ) -> Dict[str, Any]:
        """Calculates itemized revenue and deductions for a single market."""
        gross_sale = quantity_quintals * modal_price_per_quintal
        transport_cost = distance_km * transport_rate_per_km
        loading_labor_cost = quantity_quintals * labor_rate_per_quintal
        mandi_commission = gross_sale * (mandi_commission_pct / 100.0)
        packaging_cost = quantity_quintals * packaging_rate_per_quintal
        spoilage_loss = gross_sale * (spoilage_pct / 100.0)

        total_deductions = (
            transport_cost +
            loading_labor_cost +
            mandi_commission +
            packaging_cost +
            spoilage_loss
        )
        net_realisation = max(0.0, gross_sale - total_deductions)
        net_rate_per_quintal = net_realisation / quantity_quintals if quantity_quintals > 0 else 0.0

        return {
            "market_name": market_name,
            "commodity": commodity,
            "quantity_quintals": round(quantity_quintals, 2),
            "modal_price_per_quintal": round(modal_price_per_quintal, 2),
            "gross_sale_inr": round(gross_sale, 2),
            "distance_km": round(distance_km, 1),
            "itemized_deductions": {
                "transport_cost_inr": round(transport_cost, 2),
                "loading_labor_inr": round(loading_labor_cost, 2),
                "mandi_fee_commission_inr": round(mandi_commission, 2),
                "packaging_cost_inr": round(packaging_cost, 2),
                "spoilage_loss_inr": round(spoilage_loss, 2),
                "total_deductions_inr": round(total_deductions, 2)
            },
            "net_realisation_inr": round(net_realisation, 2),
            "net_rate_per_quintal_inr": round(net_rate_per_quintal, 2),
            "deduction_share_pct": round((total_deductions / gross_sale * 100.0) if gross_sale > 0 else 0.0, 1)
        }

    @classmethod
    def compare_mandis(
        cls,
        commodity: str,
        quantity_quintals: float,
        local_market: Dict[str, Any],
        terminal_market: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compares a nearby local mandi against a distant terminal market.
        Provides recommendations in Kannada, Hindi, and English.
        """
        res_local = cls.calculate_single_mandi(
            market_name=local_market.get("name", "Local APMC"),
            commodity=commodity,
            quantity_quintals=quantity_quintals,
            modal_price_per_quintal=float(local_market.get("price", 1850.0)),
            distance_km=float(local_market.get("distance_km", 15.0)),
            transport_rate_per_km=float(local_market.get("transport_rate_per_km", 22.0)),
            spoilage_pct=float(local_market.get("spoilage_pct", 1.5))
        )

        res_terminal = cls.calculate_single_mandi(
            market_name=terminal_market.get("name", "Terminal APMC"),
            commodity=commodity,
            quantity_quintals=quantity_quintals,
            modal_price_per_quintal=float(terminal_market.get("price", 2250.0)),
            distance_km=float(terminal_market.get("distance_km", 75.0)),
            transport_rate_per_km=float(terminal_market.get("transport_rate_per_km", 28.0)),
            spoilage_pct=float(terminal_market.get("spoilage_pct", 4.0))
        )

        diff_inr = res_terminal["net_realisation_inr"] - res_local["net_realisation_inr"]
        gain_pct = round((abs(diff_inr) / res_local["net_realisation_inr"] * 100.0) if res_local["net_realisation_inr"] > 0 else 0.0, 1)

        if diff_inr > 0:
            recommended = res_terminal["market_name"]
            advice_en = (
                f"Selling at {res_terminal['market_name']} yields ₹{diff_inr:,.0f} (+{gain_pct}%) more net profit "
                f"after factoring in transit fuel and spoilage."
            )
            advice_kn = (
                f"{res_terminal['market_name']} ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಮಾರಾಟ ಮಾಡುವುದರಿಂದ ಸಾರಿಗೆ ಮತ್ತು ಸಾಗಾಣಿಕೆ ವೆಚ್ಚ ಕಳೆದು "
                f"ನಿಮಗೆ ಹೆಚ್ಚುವರಿಯಾಗಿ ₹{diff_inr:,.0f} (+{gain_pct}%) ನಿವ್ವಳ ಲಾಭ ದೊರೆಯುತ್ತದೆ."
            )
            advice_hi = (
                f"{res_terminal['market_name']} मंडी में बेचने पर परिवहन और छंटाई खर्च काटकर "
                f"आपको ₹{diff_inr:,.0f} (+{gain_pct}%) का अधिक शुद्ध मुनाफा प्राप्त होगा।"
            )
        else:
            recommended = res_local["market_name"]
            advice_en = (
                f"Local market {res_local['market_name']} is more profitable! Long-distance transport to {res_terminal['market_name']} "
                f"erodes the price premium by ₹{abs(diff_inr):,.0f}."
            )
            advice_kn = (
                f"ಹತ್ತಿರದ {res_local['market_name']} ಮಾರುಕಟ್ಟೆಯೇ ಉತ್ತಮ! ದೂರದ ಮಾರುಕಟ್ಟೆಗೆ ಸಾಗಾಣಿಕೆ ವೆಚ್ಚ ಮತ್ತು ಹಾನಿಯಿಂದಾಗಿ "
                f"₹{abs(diff_inr):,.0f} ಲಾಭ ಕಡಿಮೆಯಾಗುತ್ತದೆ."
            )
            advice_hi = (
                f"स्थानीय {res_local['market_name']} मंडी अधिक लाभदायक है! दूर ले जाने पर परिवहन और बर्बादी के कारण "
                f"₹{abs(diff_inr):,.0f} का नुकसान होगा।"
            )

        return {
            "commodity": commodity,
            "quantity_quintals": quantity_quintals,
            "local_market": res_local,
            "terminal_market": res_terminal,
            "net_difference_inr": round(diff_inr, 2),
            "percentage_gain": gain_pct,
            "recommended_market": recommended,
            "recommendation_en": advice_en,
            "recommendation_kn": advice_kn,
            "recommendation_hi": advice_hi
        }
