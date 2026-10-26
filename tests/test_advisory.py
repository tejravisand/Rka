"""
Unit tests for the Lifestyle Advisory Engine (Vehicles, Real Estate, Daily Wardrobe).
"""
import unittest
from datetime import datetime, timezone
from app.core.kundali import calculate_kundali
from app.engines.lifestyle_advisor import LifestyleAdvisor


class TestLifestyleAdvisor(unittest.TestCase):

    def setUp(self):
        # Sample Birth: Aug 15, 1995 10:30 AM in Bengaluru (Mesha / Aries Lagna)
        dt_utc = datetime(1995, 8, 15, 5, 0, 0, tzinfo=timezone.utc)
        self.kundali = calculate_kundali(dt_utc, 12.9716, 77.5946)

    def test_vehicle_colors(self):
        rec = LifestyleAdvisor.analyze_vehicle_colors(self.kundali)
        self.assertIsNotNone(rec.fourth_house_lord)
        self.assertTrue(len(rec.primary_lucky_colors) > 0)
        self.assertTrue(len(rec.colors_to_avoid) > 0)
        # Mesha Lagna -> 4th house Cancer (Moon). Primary should feature Moon/Mars colors
        self.assertTrue(any("White" in c or "Silver" in c or "Red" in c or "Copper" in c for c in rec.primary_lucky_colors))

    def test_property_directions(self):
        res, comm = LifestyleAdvisor.analyze_property_direction(self.kundali)
        # Residential: 4th house Cancer (Water element) -> North / North-East
        self.assertIn("North-East", res.primary_best_directions)
        self.assertTrue(len(res.vastu_key_principles) >= 3)

        # Commercial Office: 10th house Capricorn (Saturn) -> North / East
        self.assertTrue("North" in comm.primary_best_directions or "East" in comm.primary_best_directions)
        self.assertTrue(len(comm.vastu_key_principles) >= 3)

    def test_weekly_dress_guide(self):
        weekly = LifestyleAdvisor.analyze_daily_dress_colors(self.kundali)
        self.assertEqual(len(weekly), 7)
        self.assertIn("Monday", weekly)
        self.assertIn("Sunday", weekly)

        # Monday is ruled by Moon
        mon = weekly["Monday"]
        self.assertEqual(mon.ruling_planet, "Moon")
        self.assertTrue(any("White" in c for c in mon.primary_favorable_colors))

        # Wednesday is ruled by Mercury
        wed = weekly["Wednesday"]
        self.assertEqual(wed.ruling_planet, "Mercury")
        self.assertTrue(any("Green" in c for c in wed.primary_favorable_colors))

        # Thursday is ruled by Jupiter
        thu = weekly["Thursday"]
        self.assertEqual(thu.ruling_planet, "Jupiter")
        self.assertTrue(any("Yellow" in c for c in thu.primary_favorable_colors))

    def test_full_lifestyle_dossier(self):
        dossier = LifestyleAdvisor.get_full_lifestyle_dossier(self.kundali)
        self.assertEqual(dossier.lagna_sign, "Mesha")
        self.assertTrue(len(dossier.eternal_power_colors) > 0)
        self.assertTrue(len(dossier.eternal_caution_colors) > 0)


if __name__ == "__main__":
    unittest.main()
