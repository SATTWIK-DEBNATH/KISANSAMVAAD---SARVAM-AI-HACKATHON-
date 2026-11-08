"""
KisanSamvaad - Relational Data Repository
Implements CRUD methods for Farmers, Farms, Crops, Soil Reports,
Conversations, Market Observations, Schemes, and Expert Escalations.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from .database import DatabaseManager

class KisanRepository:
    """Repository accessing the SQLite persistence layer."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager.get_instance()

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    # --- Farmer Methods ---
    def create_farmer(
        self,
        name: str,
        phone: Optional[str] = None,
        village: Optional[str] = None,
        district: Optional[str] = None,
        state: str = "Karnataka",
        preferred_language: str = "kn-IN",
        landholding_acres: float = 1.0,
        farmer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        fid = farmer_id or f"FRM_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO farmers (id, name, phone, village, district, state, preferred_language, landholding_acres, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (fid, name, phone, village, district, state, preferred_language, landholding_acres, now)
            )
        return self.get_farmer(fid)

    def get_farmer(self, farmer_id: str) -> Optional[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM farmers WHERE id = ?", (farmer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def list_farmers(self, limit: int = 50) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM farmers ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(r) for r in cursor.fetchall()]

    # --- Farm Methods ---
    def create_farm(
        self,
        farmer_id: str,
        plot_name: str,
        survey_number: Optional[str] = None,
        area_acres: float = 1.0,
        soil_type: str = "Red Sandy Loam",
        irrigation_source: str = "Borewell",
        farm_id: Optional[str] = None
    ) -> Dict[str, Any]:
        fid = farm_id or f"PLT_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO farms (id, farmer_id, plot_name, survey_number, area_acres, soil_type, irrigation_source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (fid, farmer_id, plot_name, survey_number, area_acres, soil_type, irrigation_source, now)
            )
        cursor = conn.execute("SELECT * FROM farms WHERE id = ?", (fid,))
        return dict(cursor.fetchone())

    def get_farms_by_farmer(self, farmer_id: str) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM farms WHERE farmer_id = ? ORDER BY created_at ASC", (farmer_id,))
        return [dict(r) for r in cursor.fetchall()]

    # --- Crop Methods ---
    def create_crop(
        self,
        farm_id: str,
        crop_name: str,
        variety: Optional[str] = None,
        sowing_date: Optional[str] = None,
        stage: str = "Vegetative",
        expected_harvest_date: Optional[str] = None,
        crop_id: Optional[str] = None
    ) -> Dict[str, Any]:
        cid = crop_id or f"CRP_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO crops (id, farm_id, crop_name, variety, sowing_date, stage, expected_harvest_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (cid, farm_id, crop_name, variety, sowing_date, stage, expected_harvest_date, now)
            )
        cursor = conn.execute("SELECT * FROM crops WHERE id = ?", (cid,))
        return dict(cursor.fetchone())

    def get_crops_by_farm(self, farm_id: str) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM crops WHERE farm_id = ? ORDER BY created_at DESC", (farm_id,))
        return [dict(r) for r in cursor.fetchall()]

    # --- Soil Report Methods ---
    def create_soil_report(
        self,
        farm_id: Optional[str],
        card_number: Optional[str],
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        ph: float,
        organic_carbon: float,
        zinc: float,
        boron: float,
        test_date: Optional[str] = None,
        recommendations: Optional[Dict[str, Any]] = None,
        report_id: Optional[str] = None
    ) -> Dict[str, Any]:
        rid = report_id or f"SHC_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        tdate = test_date or now[:10]
        rec_json = json.dumps(recommendations or {}, ensure_ascii=False)
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO soil_reports (id, farm_id, card_number, nitrogen, phosphorus, potassium, ph, organic_carbon, zinc, boron, test_date, recommendations_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (rid, farm_id, card_number, nitrogen, phosphorus, potassium, ph, organic_carbon, zinc, boron, tdate, rec_json, now)
            )
        cursor = conn.execute("SELECT * FROM soil_reports WHERE id = ?", (rid,))
        row = dict(cursor.fetchone())
        row["recommendations"] = json.loads(row.get("recommendations_json") or "{}")
        return row

    def get_soil_reports_by_farm(self, farm_id: str) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM soil_reports WHERE farm_id = ? ORDER BY test_date DESC", (farm_id,))
        results = []
        for r in cursor.fetchall():
            row = dict(r)
            row["recommendations"] = json.loads(row.get("recommendations_json") or "{}")
            results.append(row)
        return results

    # --- Conversation Methods ---
    def save_conversation(
        self,
        query_text: str,
        response_text: str,
        farmer_id: Optional[str] = None,
        language: str = "kn-IN",
        detected_intent: Optional[str] = None,
        audio_duration: float = 0.0,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        cid = conversation_id or f"CNV_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO conversations (id, farmer_id, query_text, response_text, language, detected_intent, audio_duration, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (cid, farmer_id, query_text, response_text, language, detected_intent, audio_duration, now)
            )
        cursor = conn.execute("SELECT * FROM conversations WHERE id = ?", (cid,))
        return dict(cursor.fetchone())

    def get_conversation_history(self, farmer_id: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        if farmer_id:
            cursor = conn.execute(
                "SELECT * FROM conversations WHERE farmer_id = ? ORDER BY created_at DESC LIMIT ?",
                (farmer_id, limit)
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM conversations ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
        return [dict(r) for r in cursor.fetchall()]

    # --- Market Observations ---
    def record_market_observation(
        self,
        market_name: str,
        commodity: str,
        min_price: float,
        max_price: float,
        modal_price: float,
        district: Optional[str] = None,
        variety: Optional[str] = "Standard",
        date: Optional[str] = None,
        data_source_mode: str = "DEMO"
    ) -> Dict[str, Any]:
        oid = f"MKT_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        dt = date or now[:10]
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO market_observations (id, market_name, district, commodity, variety, min_price, max_price, modal_price, date, data_source_mode, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (oid, market_name, district, commodity, variety, min_price, max_price, modal_price, dt, data_source_mode, now)
            )
        cursor = conn.execute("SELECT * FROM market_observations WHERE id = ?", (oid,))
        return dict(cursor.fetchone())

    def get_latest_market_observations(self, commodity: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        if commodity:
            cursor = conn.execute(
                "SELECT * FROM market_observations WHERE LOWER(commodity) = LOWER(?) ORDER BY date DESC, created_at DESC LIMIT ?",
                (commodity, limit)
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM market_observations ORDER BY date DESC, created_at DESC LIMIT ?",
                (limit,)
            )
        return [dict(r) for r in cursor.fetchall()]

    # --- Scheme Methods ---
    def seed_schemes(self, scheme_list: List[Dict[str, Any]]):
        now = self._now_iso()
        conn = self.db_manager.get_connection()
        with conn:
            for s in scheme_list:
                sid = s.get("id") or f"SCH_{uuid.uuid4().hex[:8].upper()}"
                code = s.get("code") or sid
                crit_json = json.dumps(s.get("eligibility_criteria") or {}, ensure_ascii=False)
                conn.execute(
                    """
                    INSERT INTO schemes (id, code, name_en, name_hi, name_kn, category, benefit_summary, eligibility_criteria_json, portal_url, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(code) DO UPDATE SET
                        name_en=excluded.name_en,
                        name_hi=excluded.name_hi,
                        name_kn=excluded.name_kn,
                        category=excluded.category,
                        benefit_summary=excluded.benefit_summary,
                        eligibility_criteria_json=excluded.eligibility_criteria_json,
                        portal_url=excluded.portal_url
                    """,
                    (
                        sid,
                        code,
                        s.get("name_en", ""),
                        s.get("name_hi", ""),
                        s.get("name_kn", ""),
                        s.get("category", "General"),
                        s.get("benefit_summary", ""),
                        crit_json,
                        s.get("portal_url", ""),
                        now
                    )
                )

    def list_schemes(self) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM schemes ORDER BY code ASC")
        results = []
        for r in cursor.fetchall():
            row = dict(r)
            row["eligibility_criteria"] = json.loads(row.get("eligibility_criteria_json") or "{}")
            results.append(row)
        return results

    # --- Expert Cases ---
    def create_expert_case(
        self,
        crop_name: str,
        symptom_summary: str,
        initial_diagnosis: str,
        confidence_score: float,
        farmer_id: Optional[str] = None,
        query_id: Optional[str] = None,
        assigned_kvk: str = "KVK Kolar, ICAR"
    ) -> Dict[str, Any]:
        eid = f"EXP_{uuid.uuid4().hex[:8].upper()}"
        now = self._now_iso()
        conn = self.db_manager.get_connection()
        with conn:
            conn.execute(
                """
                INSERT INTO expert_cases (id, farmer_id, query_id, crop_name, symptom_summary, initial_diagnosis, confidence_score, escalation_status, assigned_kvk, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'OPEN', ?, ?)
                """,
                (eid, farmer_id, query_id, crop_name, symptom_summary, initial_diagnosis, confidence_score, assigned_kvk, now)
            )
        cursor = conn.execute("SELECT * FROM expert_cases WHERE id = ?", (eid,))
        return dict(cursor.fetchone())

    def list_open_expert_cases(self) -> List[Dict[str, Any]]:
        conn = self.db_manager.get_connection()
        cursor = conn.execute("SELECT * FROM expert_cases WHERE escalation_status = 'OPEN' ORDER BY created_at DESC")
        return [dict(r) for r in cursor.fetchall()]

repository = KisanRepository()
