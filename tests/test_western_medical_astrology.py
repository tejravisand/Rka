import unittest
from datetime import datetime
from app.core.kundali import calculate_kundali
from app.engines.western_medical_astrology import (
    WesternMedicalAstrologyEngine,
    WesternMedicalReport,
    HumoralTemperament
)


class TestWesternMedicalAstrology(unittest.TestCase):

    def setUp(self):
        # 15-Aug-1995 10:30 AM Bengaluru
        self.dt_utc = datetime(1995, 8, 15, 5, 0)
        self.lat = 12.9716
        self.lon = 77.5946
        self.tz = 5.5
        self.kundali = calculate_kundali(self.dt_utc, self.lat, self.lon, self.tz)
        self.report = WesternMedicalAstrologyEngine.evaluate(self.kundali, client_name="Western Test")

    def test_report_structure(self):
        self.assertIsInstance(self.report, WesternMedicalReport)
        self.assertEqual(self.report.client_name, "Western Test")
        self.assertEqual(self.report.tropical_ascendant.sign_name, "Aries")

    def test_tropical_positions(self):
        # August 15 Sun must be in Leo in Tropical zodiac
        sun_pos = self.report.tropical_positions.get("Sun")
        self.assertIsNotNone(sun_pos)
        self.assertEqual(sun_pos.sign_name, "Leo")
        self.assertAlmostEqual(sun_pos.tropical_longitude, 141.92, delta=0.5)

    def test_humoral_temperament(self):
        temp = self.report.temperament
        self.assertIsInstance(temp, HumoralTemperament)
        total_pct = temp.choleric_pct + temp.sanguine_pct + temp.melancholic_pct + temp.phlegmatic_pct
        self.assertAlmostEqual(total_pct, 100.0, delta=1.0)
        self.assertIn("Choleric", temp.dominant_temperament)

    def test_homo_signorum_mapping(self):
        zones = self.report.homo_signorum_zones
        self.assertEqual(len(zones), 12)
        sign_names = [z.sign_name for z in zones]
        self.assertIn("Aries", sign_names)
        self.assertIn("Pisces", sign_names)

    def test_culpeper_herbs(self):
        remedies = self.report.culpeper_remedies
        self.assertGreater(len(remedies), 0)
        herb_names = [h.herb_name for h in remedies]
        self.assertTrue(any("Hawthorn" in name for name in herb_names))


if __name__ == "__main__":
    unittest.main()
