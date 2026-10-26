import unittest
from datetime import datetime
from app.core.kundali import calculate_kundali
from app.engines.medical_astrology_engine import (
    VedicMedicalAstrologyEngine,
    MedicalAstrologyReport,
    DoshaProfile,
    DhatuAssessment
)


class TestVedicMedicalAstrology(unittest.TestCase):

    def setUp(self):
        # 15-Aug-1995 10:30 AM Bengaluru (Mesha Lagna - Movable)
        self.dt_utc = datetime(1995, 8, 15, 5, 0)
        self.lat = 12.9716
        self.lon = 77.5946
        self.tz = 5.5
        self.kundali = calculate_kundali(self.dt_utc, self.lat, self.lon, self.tz)
        self.report = VedicMedicalAstrologyEngine.evaluate(self.kundali, client_name="Test Native")

    def test_report_structure(self):
        self.assertIsInstance(self.report, MedicalAstrologyReport)
        self.assertEqual(self.report.client_name, "Test Native")
        self.assertEqual(self.report.lagna_sign, "Mesha")
        self.assertEqual(self.report.lagna_lord, "Mars")

    def test_dosha_profile(self):
        dosha = self.report.dosha_profile
        self.assertIsInstance(dosha, DoshaProfile)
        self.assertGreater(dosha.vata_pct, 0.0)
        self.assertGreater(dosha.pitta_pct, 0.0)
        self.assertGreater(dosha.kapha_pct, 0.0)
        total_pct = dosha.vata_pct + dosha.pitta_pct + dosha.kapha_pct
        self.assertAlmostEqual(total_pct, 100.0, delta=1.0)
        self.assertIn("Pitta", dosha.dominant_prakriti)

    def test_sapta_dhatus(self):
        dhatus = self.report.dhatu_assessments
        self.assertEqual(len(dhatus), 7)
        expected_names = ["Rasa", "Rakta", "Mamsa", "Meda", "Asthi", "Majja", "Shukra"]
        actual_names = [d.dhatu_name for d in dhatus]
        self.assertEqual(actual_names, expected_names)

        for d in dhatus:
            self.assertIn(d.status, ["Balanced", "Moderate Strain", "High Vulnerability"])
            self.assertTrue(len(d.governing_planets) > 0)

    def test_trika_houses(self):
        trika = self.report.trika_houses
        self.assertEqual(len(trika), 3)
        house_numbers = [h.house_num for h in trika]
        self.assertEqual(house_numbers, [6, 8, 12])

        for h in trika:
            self.assertIn(h.risk_level, ["Low", "Moderate", "Elevated", "Critical"])

    def test_maraka_and_badhaka(self):
        mb = self.report.maraka_badhaka_analysis
        self.assertIn("maraka_lords", mb)
        # For Aries lagna: 2nd house is Taurus (Venus), 7th house is Libra (Venus)
        self.assertEqual(mb["maraka_lords"], ["Venus", "Venus"])
        # For Aries lagna (Movable): Badhaka is 11th house (Aquarius - Saturn)
        self.assertEqual(mb["badhaka_house"], 11)
        self.assertEqual(mb["badhaka_lord"], "Saturn")

    def test_anatomical_zones(self):
        zones = self.report.anatomical_zones
        self.assertEqual(len(zones), 12)
        self.assertEqual(zones[0].zone_name, "Head & Brain")
        self.assertEqual(zones[11].zone_name, "Feet & Lymphatics")

    def test_d30_trimshamsha_insights(self):
        d30 = self.report.d30_trimshamsha_insights
        self.assertIsInstance(d30, list)
        self.assertGreater(len(d30), 0)

    def test_remedial_chikitsa(self):
        remedies = self.report.remedial_chikitsa
        self.assertGreater(len(remedies.ayurvedic_herbs), 0)
        self.assertGreater(len(remedies.dietary_guidelines_ahara), 0)
        self.assertGreater(len(remedies.healing_mantras), 0)
        self.assertGreater(len(remedies.medical_gemstone_cautions), 0)

        # Check Maha Mrityunjaya mantra presence
        deities = [m["deity"] for m in remedies.healing_mantras]
        self.assertTrue(any("Mrityunjaya" in d for d in deities))


if __name__ == "__main__":
    unittest.main()
