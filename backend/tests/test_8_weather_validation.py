"""
Test Suite 8: Agricultural Weather & IMD Spray Window Validation
Verifies wind thresholds, precipitation warnings, and actionable spray advisories.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.integrations.weather.connector import WeatherConnector

class TestWeatherValidation(unittest.TestCase):
    def test_forecast_structure(self):
        """Verifies 3-day forecast structure and agro-climatic metadata."""
        weather = WeatherConnector.get_forecast(location="Kolar District, Karnataka")
        self.assertIn("location", weather)
        self.assertIn("agro_climatic_zone", weather)
        self.assertIn("forecast", weather)
        self.assertEqual(len(weather["forecast"]), 3)

    def test_spray_safety_evaluation(self):
        """Verifies clear days are spray-safe while thunderstorm/high-wind days are flagged unsafe."""
        weather = WeatherConnector.get_forecast()
        forecast = weather["forecast"]
        
        # Today should be safe (low wind, low rain)
        today = forecast[0]
        self.assertTrue(today["is_spray_safe"])
        self.assertLess(today["wind_kmh"], 15)
        self.assertIn("Safe to spray", today["spray_advisory"])
        
        # Tomorrow has thunderstorm (rain chance 80%, wind 24 km/h)
        tomorrow = forecast[1]
        self.assertFalse(tomorrow["is_spray_safe"])
        self.assertGreater(tomorrow["wind_kmh"], 15)
        self.assertIn("WARNING", tomorrow["spray_advisory"])

if __name__ == "__main__":
    unittest.main()

