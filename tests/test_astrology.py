"""
Unit tests for Kundali, Shodashavargas, Vimshottari Dashas, and Milestones.
"""
import unittest
from datetime import datetime, timezone
from app.core.ephemeris import (
    calculate_lahiri_ayanamsa,
    datetime_to_jd,
    get_nakshatra_info,
    normalize_degrees
)
from app.core.vargas import VargaCalculator
from app.core.dasha import calculate_birth_dasha_balance, calculate_vimshottari_dashas
from app.core.kundali import calculate_kundali
from app.core.milestones import LifeMilestoneEngine


class TestAstrologyEngine(unittest.TestCase):

    def test_ayanamsa_calculation(self):
        # Jan 1, 2000 JD 2451545.0
        ayan = calculate_lahiri_ayanamsa(2451545.0)
        self.assertAlmostEqual(ayan, 23.857, places=2)

    def test_nakshatra_mapping(self):
        # 0.0 degrees sidereal should be Ashwini Pada 1, Lord Ketu
        nak_num, name, pada, lord = get_nakshatra_info(0.0)
        self.assertEqual(nak_num, 0)
        self.assertEqual(name, "Ashwini")
        self.assertEqual(pada, 1)
        self.assertEqual(lord, "Ketu")

        # 40.0 degrees sidereal (Taurus 10°) -> Rohini
        nak_num, name, pada, lord = get_nakshatra_info(45.0)
        self.assertEqual(name, "Rohini")
        self.assertEqual(lord, "Moon")

    def test_navamsa_d9_rules(self):
        # Aries (Movable sign, 0): 0° to 3°20' maps to Aries (0)
        sign, rem = VargaCalculator.calculate_d9(0, 1.5)
        self.assertEqual(sign, 0)

        # Taurus (Fixed sign, 1): starts from 9th (Capricorn, 9)
        sign, rem = VargaCalculator.calculate_d9(1, 1.5)
        self.assertEqual(sign, 9)

        # Gemini (Dual sign, 2): starts from 5th (Libra, 6)
        sign, rem = VargaCalculator.calculate_d9(2, 1.5)
        self.assertEqual(sign, 6)

    def test_vimshottari_dasha_balance(self):
        # Moon at 0° (Ashwini start): 100% of Ketu's 7 years remaining
        first_lord, fraction, balance = calculate_birth_dasha_balance(0.0)
        self.assertEqual(first_lord, "Ketu")
        self.assertAlmostEqual(fraction, 1.0, places=3)
        self.assertAlmostEqual(balance, 7.0, places=3)

        # Moon midway through Ashwini (6° 40' = 6.666667°): 50% remaining (3.5 years)
        first_lord, fraction, balance = calculate_birth_dasha_balance(6.6666667)
        self.assertEqual(first_lord, "Ketu")
        self.assertAlmostEqual(fraction, 0.5, places=3)
        self.assertAlmostEqual(balance, 3.5, places=3)

    def test_full_kundali_and_milestones(self):
        dt = datetime(1995, 8, 15, 5, 0, 0, tzinfo=timezone.utc)
        kundali = calculate_kundali(dt, 12.9716, 77.5946)

        self.assertEqual(len(kundali.houses), 12)
        self.assertIn("Sun", kundali.planets)
        self.assertIn("Moon", kundali.planets)

        # Calculate dashas
        moon_lon = kundali.planets["Moon"].longitude
        dashas = calculate_vimshottari_dashas(dt, moon_lon, max_lifespan_years=100.0)
        self.assertTrue(len(dashas) >= 5)

        # Calculate milestones
        milestones = LifeMilestoneEngine.calculate_all_milestones(kundali, dashas, max_age_years=80.0)
        self.assertTrue(len(milestones) > 0)


if __name__ == "__main__":
    unittest.main()
