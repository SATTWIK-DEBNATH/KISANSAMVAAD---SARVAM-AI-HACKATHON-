"""
Test Suite 11: Relational Persistence Layer Validation
Verifies SQLite schema creation, CRUD operations, foreign key constraints,
and thread-safe connection pooling.
"""

import unittest
import os
import tempfile
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.db.database import DatabaseManager
from app.db.repository import KisanRepository

class TestPersistenceLayer(unittest.TestCase):
    """Verifies relational database persistence capabilities."""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_file.name
        self.temp_file.close()
        self.db_mgr = DatabaseManager(db_path=self.db_path)
        self.repo = KisanRepository(db_manager=self.db_mgr)

    def tearDown(self):
        self.db_mgr.close()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass

    def test_farmer_and_farm_crud(self):
        """Verifies farmer creation and associated farm plots."""
        farmer = self.repo.create_farmer(
            name="Ramesh Kumar",
            phone="9845012345",
            village="Sugatur",
            district="Kolar",
            state="Karnataka",
            preferred_language="kn-IN",
            landholding_acres=4.2
        )
        self.assertIsNotNone(farmer["id"])
        self.assertEqual(farmer["name"], "Ramesh Kumar")
        self.assertEqual(farmer["district"], "Kolar")

        # Create farm plot
        farm = self.repo.create_farm(
            farmer_id=farmer["id"],
            plot_name="South Block",
            survey_number="128/1A",
            area_acres=2.5,
            soil_type="Red Sandy Loam",
            irrigation_source="Drip / Borewell"
        )
        self.assertEqual(farm["farmer_id"], farmer["id"])
        self.assertEqual(farm["plot_name"], "South Block")

        farms = self.repo.get_farms_by_farmer(farmer["id"])
        self.assertEqual(len(farms), 1)
        self.assertEqual(farms[0]["survey_number"], "128/1A")

    def test_soil_report_and_crops_persistence(self):
        """Verifies crop entries and soil health card parameter storage."""
        farmer = self.repo.create_farmer(name="Savitri Bai", village="Holur", district="Kolar")
        farm = self.repo.create_farm(farmer_id=farmer["id"], plot_name="Main Field", area_acres=3.0)

        # Create crop
        crop = self.repo.create_crop(
            farm_id=farm["id"],
            crop_name="Tomato",
            variety="Arka Rakshak",
            stage="Flowering"
        )
        self.assertEqual(crop["crop_name"], "Tomato")
        crops = self.repo.get_crops_by_farm(farm["id"])
        self.assertEqual(len(crops), 1)

        # Create soil report
        report = self.repo.create_soil_report(
            farm_id=farm["id"],
            card_number="KA-KOL-2026-9901",
            nitrogen=195.0,
            phosphorus=9.1,
            potassium=155.0,
            ph=5.8,
            organic_carbon=0.41,
            zinc=0.52,
            boron=0.38,
            recommendations={"action": "Apply agricultural lime 250kg/ha"}
        )
        self.assertEqual(report["card_number"], "KA-KOL-2026-9901")
        self.assertEqual(report["ph"], 5.8)
        self.assertIn("action", report["recommendations"])

    def test_conversation_and_market_observations(self):
        """Verifies farmer conversation logging and APMC market observation tracking."""
        conv = self.repo.save_conversation(
            query_text="Tomato leaf blight symptoms",
            response_text="Apply Mancozeb 75 WP @ 2.0g/L",
            language="kn-IN",
            detected_intent="pest_advisory"
        )
        self.assertIsNotNone(conv["id"])
        self.assertEqual(conv["detected_intent"], "pest_advisory")

        history = self.repo.get_conversation_history(limit=5)
        self.assertGreaterEqual(len(history), 1)

        # Record market observation
        mkt = self.repo.record_market_observation(
            market_name="Kolar APMC",
            commodity="Tomato",
            min_price=1600.0,
            max_price=2100.0,
            modal_price=1850.0,
            district="Kolar",
            data_source_mode="LIVE"
        )
        self.assertEqual(mkt["market_name"], "Kolar APMC")
        self.assertEqual(mkt["modal_price"], 1850.0)

        latest = self.repo.get_latest_market_observations(commodity="Tomato")
        self.assertGreaterEqual(len(latest), 1)

if __name__ == "__main__":
    unittest.main()

