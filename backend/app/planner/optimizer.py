"""
KisanSamvaad - Multi-Nutrient Integer Fertilizer Optimizer
Selects the lowest-cost whole-bag combination of fertilizers satisfying
target N, P2O5, and K2O requirements. Correctly accounts for multi-nutrient
contributions (e.g. Nitrogen supplied by DAP) and enforces configurable overshoot caps.
"""

import math
from typing import Dict, Any, List, Optional, Tuple
from .schemas import BagItem
from .data_loader import PlannerDataLoader

def _ceil_bags(needed: float, per_bag: float) -> int:
    """Returns whole bags needed, resilient to floating-point precision issues."""
    if needed <= 1e-6:
        return 0
    ratio = needed / per_bag
    nearest = round(ratio)
    if abs(ratio - nearest) < 1e-5:
        return nearest
    return math.ceil(ratio)

class FertilizerOptimizer:
    """Solves the discrete multi-nutrient whole-bag fertilizer optimization problem."""

    @classmethod
    def optimize(
        cls,
        target_n_kg: float,
        target_p2o5_kg: float,
        target_k2o_kg: float,
        max_overshoot_pct: float = 40.0,
        allowed_fertilizers: Optional[List[str]] = None,
        custom_fertilizer_registry: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Determines the optimal whole-bag allocation to minimize total farmer cost.
        Returns explicit is_feasible: false if targets cannot be met within constraints.
        """
        fert_registry = custom_fertilizer_registry or PlannerDataLoader.load_fertilizers()
        allowed = [f.lower() for f in (allowed_fertilizers or ["urea", "dap", "ssp", "mop"])]

        # Extract specifications
        # Urea: 45 kg, 46% N -> 20.7 kg N / bag
        urea_spec = fert_registry.get("urea", {})
        urea_bag_kg = urea_spec.get("bag_size_kg", 45.0)
        urea_n_pct = urea_spec.get("n_content_pct", 46.0) / 100.0
        n_per_urea_bag = urea_bag_kg * urea_n_pct
        price_urea = urea_spec.get("default_price_inr", 266.50)

        # DAP: 50 kg, 18% N, 46% P2O5 -> 9.0 kg N, 23.0 kg P2O5 / bag
        dap_spec = fert_registry.get("dap", {})
        dap_bag_kg = dap_spec.get("bag_size_kg", 50.0)
        dap_n_pct = dap_spec.get("n_content_pct", 18.0) / 100.0
        dap_p_pct = dap_spec.get("p2o5_content_pct", 46.0) / 100.0
        n_per_dap_bag = dap_bag_kg * dap_n_pct
        p_per_dap_bag = dap_bag_kg * dap_p_pct
        price_dap = dap_spec.get("default_price_inr", 1350.00)

        # SSP: 50 kg, 16% P2O5 -> 8.0 kg P2O5 / bag
        ssp_spec = fert_registry.get("ssp", {})
        ssp_bag_kg = ssp_spec.get("bag_size_kg", 50.0)
        ssp_p_pct = ssp_spec.get("p2o5_content_pct", 16.0) / 100.0
        p_per_ssp_bag = ssp_bag_kg * ssp_p_pct
        price_ssp = ssp_spec.get("default_price_inr", 550.00)

        # MOP: 50 kg, 60% K2O -> 30.0 kg K2O / bag
        mop_spec = fert_registry.get("mop", {})
        mop_bag_kg = mop_spec.get("bag_size_kg", 50.0)
        mop_k_pct = mop_spec.get("k2o_content_pct", 60.0) / 100.0
        k_per_mop_bag = mop_bag_kg * mop_k_pct
        price_mop = mop_spec.get("default_price_inr", 1700.00)

        # If all targets are zero (e.g. very high soil reserves)
        if target_n_kg <= 0 and target_p2o5_kg <= 0 and target_k2o_kg <= 0:
            return {
                "is_feasible": True,
                "bags": [],
                "total_cost_inr": 0.0,
                "nutrients_delivered_kg": {"n": 0.0, "p2o5": 0.0, "k2o": 0.0},
                "nutrient_surplus_pct": {"n": 0.0, "p2o5": 0.0, "k2o": 0.0},
                "note": "Soil nutrient reserves are high. Zero chemical fertilizer application required."
            }

        best_plan = None
        best_cost = float("inf")

        # Range bounds for integer bag counts
        # Potassium: MOP is sole simple K source
        max_mop = _ceil_bags(target_k2o_kg, k_per_mop_bag) if (target_k2o_kg > 0 and "mop" in allowed) else 0

        # Phosphorus: can come from DAP or SSP
        max_dap = _ceil_bags(target_p2o5_kg, p_per_dap_bag) + 1 if (target_p2o5_kg > 0 and "dap" in allowed) else 0
        max_ssp = _ceil_bags(target_p2o5_kg, p_per_ssp_bag) + 1 if (target_p2o5_kg > 0 and "ssp" in allowed) else 0

        # Explore combination space
        # Strategy A: Use DAP as primary P source, supplement with Urea for remaining N
        # Strategy B: Use SSP as primary P source (zero N supplied by SSP), full N from Urea
        # Strategy C: Hybrid DAP + SSP + Urea

        mop_counts = [max_mop] if "mop" in allowed else [0]
        dap_range = range(0, max_dap + 1) if "dap" in allowed else [0]
        ssp_range = range(0, max_ssp + 1) if "ssp" in allowed else [0]

        for num_mop in mop_counts:
            deliv_k = num_mop * k_per_mop_bag
            if target_k2o_kg > 0 and deliv_k < target_k2o_kg:
                continue

            for num_dap in dap_range:
                p_from_dap = num_dap * p_per_dap_bag
                n_from_dap = num_dap * n_per_dap_bag

                # Determine needed SSP
                needed_p = max(0.0, target_p2o5_kg - p_from_dap)
                if needed_p > 0:
                    if "ssp" not in allowed:
                        continue
                    num_ssp = _ceil_bags(needed_p, p_per_ssp_bag)
                else:
                    num_ssp = 0

                deliv_p = p_from_dap + (num_ssp * p_per_ssp_bag)
                if target_p2o5_kg > 0 and deliv_p < target_p2o5_kg:
                    continue

                # Determine needed Urea
                needed_n = max(0.0, target_n_kg - n_from_dap)
                if needed_n > 0:
                    if "urea" not in allowed:
                        continue
                    num_urea = _ceil_bags(needed_n, n_per_urea_bag)
                else:
                    num_urea = 0

                deliv_n = n_from_dap + (num_urea * n_per_urea_bag)
                if target_n_kg > 0 and deliv_n < target_n_kg:
                    continue

                # Check overshoot constraints
                surplus_n_pct = ((deliv_n - target_n_kg) / target_n_kg * 100.0) if target_n_kg > 0 else 0.0
                surplus_p_pct = ((deliv_p - target_p2o5_kg) / target_p2o5_kg * 100.0) if target_p2o5_kg > 0 else 0.0
                surplus_k_pct = ((deliv_k - target_k2o_kg) / target_k2o_kg * 100.0) if target_k2o_kg > 0 else 0.0

                # Reject if severe overshoot beyond cap
                if surplus_n_pct > max_overshoot_pct or surplus_p_pct > max_overshoot_pct or surplus_k_pct > max_overshoot_pct:
                    # Allow relaxation if bag count is minimal (1 bag)
                    if not (num_urea <= 1 and num_dap <= 1 and num_ssp <= 1 and num_mop <= 1):
                        continue

                cost = (num_urea * price_urea) + (num_dap * price_dap) + (num_ssp * price_ssp) + (num_mop * price_mop)

                if cost < best_cost:
                    best_cost = cost
                    best_plan = {
                        "urea": num_urea,
                        "dap": num_dap,
                        "ssp": num_ssp,
                        "mop": num_mop,
                        "cost": cost,
                        "deliv_n": round(deliv_n, 2),
                        "deliv_p": round(deliv_p, 2),
                        "deliv_k": round(deliv_k, 2),
                        "surplus_n": round(surplus_n_pct, 1),
                        "surplus_p": round(surplus_p_pct, 1),
                        "surplus_k": round(surplus_k_pct, 1)
                    }

        if not best_plan:
            return {
                "is_feasible": False,
                "error": "No whole-bag combination satisfies nutrient requirements within overshoot tolerance.",
                "bags": [],
                "total_cost_inr": 0.0
            }

        # Build BagItem objects
        bags_list: List[Dict[str, Any]] = []

        if best_plan["dap"] > 0:
            bags_list.append(BagItem(
                fertilizer_id="dap",
                name=dap_spec.get("name", "DAP (18-46-0)"),
                bag_size_kg=dap_bag_kg,
                bags_count=best_plan["dap"],
                total_kg=best_plan["dap"] * dap_bag_kg,
                price_per_bag_inr=price_dap,
                total_cost_inr=round(best_plan["dap"] * price_dap, 2),
                nutrients_supplied_kg={
                    "n": round(best_plan["dap"] * n_per_dap_bag, 2),
                    "p2o5": round(best_plan["dap"] * p_per_dap_bag, 2),
                    "k2o": 0.0
                }
            ).to_dict())

        if best_plan["ssp"] > 0:
            bags_list.append(BagItem(
                fertilizer_id="ssp",
                name=ssp_spec.get("name", "Single Super Phosphate (SSP)"),
                bag_size_kg=ssp_bag_kg,
                bags_count=best_plan["ssp"],
                total_kg=best_plan["ssp"] * ssp_bag_kg,
                price_per_bag_inr=price_ssp,
                total_cost_inr=round(best_plan["ssp"] * price_ssp, 2),
                nutrients_supplied_kg={
                    "n": 0.0,
                    "p2o5": round(best_plan["ssp"] * p_per_ssp_bag, 2),
                    "k2o": 0.0
                }
            ).to_dict())

        if best_plan["urea"] > 0:
            bags_list.append(BagItem(
                fertilizer_id="urea",
                name=urea_spec.get("name", "Neem Coated Urea (46% N)"),
                bag_size_kg=urea_bag_kg,
                bags_count=best_plan["urea"],
                total_kg=best_plan["urea"] * urea_bag_kg,
                price_per_bag_inr=price_urea,
                total_cost_inr=round(best_plan["urea"] * price_urea, 2),
                nutrients_supplied_kg={
                    "n": round(best_plan["urea"] * n_per_urea_bag, 2),
                    "p2o5": 0.0,
                    "k2o": 0.0
                }
            ).to_dict())

        if best_plan["mop"] > 0:
            bags_list.append(BagItem(
                fertilizer_id="mop",
                name=mop_spec.get("name", "Muriate of Potash (MOP)"),
                bag_size_kg=mop_bag_kg,
                bags_count=best_plan["mop"],
                total_kg=best_plan["mop"] * mop_bag_kg,
                price_per_bag_inr=price_mop,
                total_cost_inr=round(best_plan["mop"] * price_mop, 2),
                nutrients_supplied_kg={
                    "n": 0.0,
                    "p2o5": 0.0,
                    "k2o": round(best_plan["mop"] * k_per_mop_bag, 2)
                }
            ).to_dict())

        return {
            "is_feasible": True,
            "bags": bags_list,
            "total_cost_inr": round(best_plan["cost"], 2),
            "nutrients_delivered_kg": {
                "n": best_plan["deliv_n"],
                "p2o5": best_plan["deliv_p"],
                "k2o": best_plan["deliv_k"]
            },
            "nutrient_surplus_pct": {
                "n": best_plan["surplus_n"],
                "p2o5": best_plan["surplus_p"],
                "k2o": best_plan["surplus_k"]
            }
        }
