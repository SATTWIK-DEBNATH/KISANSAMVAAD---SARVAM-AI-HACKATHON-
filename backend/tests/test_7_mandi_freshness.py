"""
Test Suite 7: Mandi Data Freshness, Freshness Timestamps & Source Mode Labeling
Verifies APMC Mandi records contain required prices, modal rates, timestamps, and DEMO/LIVE labels.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.integrations.mandi.connector import MandiConnector

class TestMandiFreshness(unittest.TestCase):
    def test_mandi_catalog_records_complete(self):
        """Verifies MandiConnector returns all core mandis (Kolar, Yeshwanthpur, Raichur, Shimoga)."""
        rates = MandiConnector.get_rates()
        self.assertGreaterEqual(len(rates), 4)
        markets = [r["market"].lower() for r in rates]
        self.assertTrue(any("kolar" in m for m in markets))
        self.assertTrue(any("yeshwanthpur" in m for m in markets))
        self.assertTrue(any("raichur" in m for m in markets))
        self.assertTrue(any("shimoga" in m for m in markets))

    def test_mandi_record_data_fields(self):
        """Verifies each mandi record includes min, max, modal prices, and freshness timestamp."""
        rates = MandiConnector.get_rates(commodity="tomato")
        self.assertGreater(len(rates), 0)
        rec = rates[0]
        self.assertIn("min_price", rec)
        self.assertIn("max_price", rec)
        self.assertIn("modal_price", rec)
        self.assertGreaterEqual(rec["modal_price"], rec["min_price"])
        self.assertLessEqual(rec["modal_price"], rec["max_price"])
        self.assertIn("timestamp", rec)
        self.assertIn("data_source_mode", rec)
        self.assertIn(rec["data_source_mode"], ["LIVE", "DEMO"])

    def test_commodity_filtering(self):
        """Verifies filtering by commodity name works accurately."""
        tomato_rates = MandiConnector.get_rates(commodity="tomato")
        self.assertTrue(all("tomato" in r["commodity"].lower() for r in tomato_rates))
        
        onion_rates = MandiConnector.get_rates(commodity="onion")
        self.assertTrue(all("onion" in r["commodity"].lower() for r in onion_rates))

if __name__ == "__main__":
    unittest.main()

