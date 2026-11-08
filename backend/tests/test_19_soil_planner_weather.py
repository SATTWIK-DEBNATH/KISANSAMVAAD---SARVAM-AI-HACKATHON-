"""
Test Suite 19: Soil Planner Weather Thresholds & Offline Degradation
Verifies 72-hour precipitation evaluation against fertilizer leaching thresholds
and graceful local fallback when Open-Meteo is unreachable.
"""

import unittest
import os
import sys
from unittest.mock import patch

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.planner.schedule import TimingScheduleBuilder

class TestSoilPlannerWeather(unittest.TestCase):
    """Verifies weather checks and offline fallback behavior."""

    @patch("urllib.request.urlopen")
    def test_heavy_rain_triggers_delay(self, mock_urlopen):
        """Verifies precipitation > 10mm recommends application delay."""
        mock_resp = unittest.mock.MagicMock()
        mock_resp.read.return_value = b'{"daily": {"precipitation_sum": [8.5, 12.0, 0.0], "precipitation_probability_max": [75, 80, 20]}}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        weather = TimingScheduleBuilder.check_open_meteo_weather(lat=13.1367, lon=78.1348)
        self.assertTrue(weather["delay_recommended"])
        self.assertGreaterEqual(weather["precipitation_next_72h_mm"], 10.0)
        self.assertIn("Delay chemical fertilizer", weather["reason"])
        self.assertIn("Open-Meteo", weather["source"])

    @patch("urllib.request.urlopen")
    def test_clear_weather_permits_application(self, mock_urlopen):
        """Verifies clear weather (<10mm rain, <60% prob) does not delay application."""
        mock_resp = unittest.mock.MagicMock()
        mock_resp.read.return_value = b'{"daily": {"precipitation_sum": [0.0, 1.2, 0.5], "precipitation_probability_max": [10, 25, 15]}}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        weather = TimingScheduleBuilder.check_open_meteo_weather(lat=13.1367, lon=78.1348)
        self.assertFalse(weather["delay_recommended"])
        self.assertIsNone(weather["reason"])

    @patch("urllib.request.urlopen", side_effect=Exception("Network Unreachable"))
    def test_offline_fallback_degrades_gracefully(self, mock_urlopen):
        """Verifies network outage falls back to local IMD model without raising exception."""
        weather = TimingScheduleBuilder.check_open_meteo_weather(lat=13.1367, lon=78.1348)
        self.assertIsNotNone(weather)
        self.assertIn("Local Offline Fallback", weather["source"])
        self.assertIn("delay_recommended", weather)

if __name__ == "__main__":
    unittest.main()
