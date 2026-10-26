import unittest
from datetime import datetime
from app.engines.vedastro_engine import VedAstroEngine, VEDASTRO_AVAILABLE


class TestVedAstroBridge(unittest.TestCase):

    def test_availability(self):
        self.assertTrue(VedAstroEngine.is_available())

    def test_build_time_and_geo(self):
        dt = datetime(1995, 8, 15, 10, 30)
        time, geo = VedAstroEngine.build_time_and_geo(dt, tz_offset=5.5, lat=12.9716, lon=77.5946, location_name="Bengaluru")
        self.assertIsNotNone(time)
        self.assertIsNotNone(geo)

    def test_negative_tz_offset(self):
        dt = datetime(2020, 1, 1, 12, 0)
        time, geo = VedAstroEngine.build_time_and_geo(dt, tz_offset=-5.0, lat=40.7128, lon=-74.0060, location_name="New York")
        self.assertIsNotNone(time)
        self.assertIsNotNone(geo)

    def test_cache_mechanism(self):
        dt = datetime(1995, 8, 15, 10, 30)
        cache_key = f"panchanga_{dt.isoformat()}_5.5_12.9716_77.5946"
        dummy_data = {"success": True, "data": {"Tithi": "MockTithi"}, "error": None}
        VedAstroEngine._cache[cache_key] = dummy_data

        result = VedAstroEngine.get_panchanga(dt, tz_offset=5.5, lat=12.9716, lon=77.5946, use_cache=True)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["Tithi"], "MockTithi")

    def test_integrated_summary_structure(self):
        dt = datetime(1995, 8, 15, 10, 30)
        summary = VedAstroEngine.get_integrated_summary(dt, tz_offset=5.5, lat=12.9716, lon=77.5946)
        self.assertIn("is_available", summary)
        self.assertIn("panchanga", summary)
        self.assertIn("ashtakavarga", summary)


if __name__ == "__main__":
    unittest.main()
