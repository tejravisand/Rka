"""
Unit tests for the Advanced Astrological Engines:
1. Jaimini Engine (Chara Karakas, Arudhas, Rashi Drishti, Karakamsha, Chara Dasha)
2. Ashtakavarga Engine (337 Bindus, BAV, SAV, Trikona & Ekadhipatya Shodhana, Pindas, Kakshya)
3. Shadbala Engine (Sthana, Dig, Kaala, Cheshta, Naisargika, Drik Bala, Virupas, Rupas)
4. Guna Milan Engine (36 Gunas, Kutas, Nadi/Bhakoot cancellations, Manglik / Kuja Dosha)
5. Panchanga & Muhurtha Engine (Tithi, Vara, Nakshatra, Yoga, Karana, Rahu Kaalam, Abhijit)
6. Skyfield Ephemeris Engine (GAST/LAST, Sun times, Lunar illumination)
7. Advanced Astrology Hub (Unified profile & library audit)
"""

import unittest
from datetime import datetime, timedelta
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.engines.jaimini_engine import JaiminiEngine
from app.engines.ashtakavarga_engine import AshtakavargaEngine
from app.engines.shadbala_engine import ShadbalaEngine
from app.engines.guna_milan_engine import GunaMilanEngine
from app.engines.panchanga_engine import PanchangaEngine
from app.engines.skyfield_ephemeris import SkyfieldEphemerisEngine
from app.engines.advanced_astrology_hub import AdvancedAstrologyHub


class TestAdvancedAstrology(unittest.TestCase):

    def setUp(self):
        # Benchmark chart: May 15, 1985, 08:30 AM, Bengaluru (12.9716°N, 77.5946°E)
        self.dt = datetime(1985, 5, 15, 8, 30, 0)
        self.lat = 12.9716
        self.lon = 77.5946
        self.tz = 5.5
        dt_utc = self.dt - timedelta(hours=self.tz)
        self.kundali = calculate_kundali(
            birth_dt_utc=dt_utc,
            latitude=self.lat,
            longitude=self.lon,
            tz_offset_hours=self.tz
        )
        self.kundali.vargas = calculate_all_vargas(self.kundali.ascendant, self.kundali.planets)

    # 1. Jaimini Engine Tests
    def test_jaimini_chara_karakas(self):
        karakas = JaiminiEngine.calculate_chara_karakas(self.kundali)
        self.assertIn("karakas", karakas)
        k_dict = karakas["karakas"]
        self.assertEqual(len(k_dict), 7)
        self.assertIn("AK", k_dict)
        self.assertIn("AmK", k_dict)
        self.assertIn("DK", k_dict)

        # AK degrees must be >= AmK degrees
        ak_deg = k_dict["AK"]["degrees_in_sign"]
        amk_deg = k_dict["AmK"]["degrees_in_sign"]
        self.assertGreaterEqual(ak_deg, amk_deg)

    def test_jaimini_arudha_padas(self):
        arudhas = JaiminiEngine.calculate_arudha_padas(self.kundali)
        self.assertEqual(len(arudhas), 12)
        self.assertIn("AL", arudhas)
        self.assertIn("UL", arudhas)
        self.assertIn("A7", arudhas)
        self.assertIn("A10", arudhas)

        # Arudha Lagna house from Lagna must be 1 to 12
        al_house = arudhas["AL"]["house_from_lagna"]
        self.assertTrue(1 <= al_house <= 12)

    def test_jaimini_rashi_drishti(self):
        # Aries (0, Movable) must aspect Leo (4), Scorpio (7), Aquarius (10), but NOT adjacent Taurus (1)
        aspects = JaiminiEngine.get_rashi_drishti_for_sign(0)
        self.assertIn(4, aspects)
        self.assertIn(7, aspects)
        self.assertIn(10, aspects)
        self.assertNotIn(1, aspects)

        # Gemini (2, Dual) must aspect Virgo (5), Sagittarius (8), Pisces (11), but NOT itself
        dual_aspects = JaiminiEngine.get_rashi_drishti_for_sign(2)
        self.assertEqual(sorted(dual_aspects), [5, 8, 11])

    def test_jaimini_karakamsha_and_chara_dasha(self):
        kl = JaiminiEngine.analyze_karakamsha(self.kundali)
        self.assertIn("karakamsha_sign", kl)
        self.assertIn("ishta_devata", kl)

        dasha = JaiminiEngine.calculate_chara_dasha(self.kundali, years=72)
        self.assertGreater(len(dasha), 0)
        self.assertEqual(dasha[0]["sign_index"], self.kundali.ascendant.sign.value)

    # 2. Ashtakavarga Engine Tests
    def test_ashtakavarga_sav_and_bav(self):
        sav = AshtakavargaEngine.calculate_sav(self.kundali)
        self.assertEqual(len(sav), 12)
        # Classical Parashari rule: Total SAV bindus across all 7 planets equals 337
        self.assertEqual(sum(sav), 337)

        # Check BAV counts
        sun_bav = AshtakavargaEngine.calculate_bav("Sun", self.kundali)
        self.assertEqual(sum(sun_bav), 48)

        moon_bav = AshtakavargaEngine.calculate_bav("Moon", self.kundali)
        self.assertEqual(sum(moon_bav), 49)

        mars_bav = AshtakavargaEngine.calculate_bav("Mars", self.kundali)
        self.assertEqual(sum(mars_bav), 39)

        jupiter_bav = AshtakavargaEngine.calculate_bav("Jupiter", self.kundali)
        self.assertEqual(sum(jupiter_bav), 56)

    def test_ashtakavarga_shodhana_and_kakshya(self):
        sun_bav = AshtakavargaEngine.calculate_bav("Sun", self.kundali)
        trikona = AshtakavargaEngine.trikona_shodhana(sun_bav)
        self.assertEqual(len(trikona), 12)
        self.assertLessEqual(sum(trikona), sum(sun_bav))

        ekadhipatya = AshtakavargaEngine.ekadhipatya_shodhana(trikona, self.kundali)
        self.assertEqual(len(ekadhipatya), 12)
        self.assertLessEqual(sum(ekadhipatya), sum(trikona))

        pindas = AshtakavargaEngine.calculate_pindas("Sun", ekadhipatya, self.kundali)
        self.assertEqual(pindas["yoga_pinda"], pindas["rashi_pinda"] + pindas["graha_pinda"])

        # Test Kakshya: 0.0° to 3.75° is ruled by Saturn
        k_num, lord, start, end = AshtakavargaEngine.get_kakshya(2.5)
        self.assertEqual(k_num, 1)
        self.assertEqual(lord, "Saturn")

        # Kakshya for 28.0° is ruled by Lagna (Ascendant)
        k_num, lord, start, end = AshtakavargaEngine.get_kakshya(28.0)
        self.assertEqual(k_num, 8)
        self.assertEqual(lord, "Ascendant")

    # 3. Shadbala Engine Tests
    def test_shadbala_calculations(self):
        shadbala = ShadbalaEngine.calculate_all_shadbala(self.kundali)
        self.assertIn("planets", shadbala)
        self.assertIn("ranking_summary", shadbala)
        self.assertEqual(len(shadbala["planets"]), 7)

        sun_data = shadbala["planets"]["Sun"]
        self.assertGreater(sun_data["total_virupas"], 0.0)
        self.assertGreater(sun_data["rupas"], 0.0)
        self.assertEqual(sun_data["required_rupas"], 6.5)
        self.assertIn("is_empowered", sun_data)

    # 4. Guna Milan Engine Tests
    def test_guna_milan_36_points(self):
        # Groom: May 15, 1985
        groom_k = self.kundali
        # Bride: Aug 20, 1988, 14:15, Bengaluru
        bride_dt = datetime(1988, 8, 20, 14, 15, 0)
        bride_utc = bride_dt - timedelta(hours=self.tz)
        bride_k = calculate_kundali(
            birth_dt_utc=bride_utc,
            latitude=self.lat,
            longitude=self.lon,
            tz_offset_hours=self.tz
        )
        bride_k.vargas = calculate_all_vargas(bride_k.ascendant, bride_k.planets)

        milan = GunaMilanEngine.match_horoscopes(bride_k, groom_k)
        self.assertIn("total_score", milan)
        self.assertIn("verdict", milan)
        self.assertIn("kutas", milan)
        self.assertTrue(0.0 <= milan["total_score"] <= 36.0)

        # Check all 8 Kutas present
        kutas = milan["kutas"]
        for k_name in ["varna", "vashya", "tara", "yoni", "graha_maitri", "gana", "bhakoot", "nadi"]:
            self.assertIn(k_name, kutas)

        # Manglik check
        self.assertIn("manglik_compatibility", milan)

    # 5. Panchanga & Muhurtha Engine Tests
    def test_panchanga_five_limbs(self):
        panch = PanchangaEngine.get_complete_panchanga(self.kundali)
        self.assertIn("panchanga", panch)
        self.assertIn("muhurtha", panch)

        p = panch["panchanga"]
        self.assertTrue(1 <= p["tithi"]["tithi_number"] <= 30)
        self.assertTrue(0 <= p["vara"]["vara_index"] <= 6)
        self.assertTrue(1 <= p["nakshatra"]["number"] <= 27)
        self.assertTrue(1 <= p["yoga"]["yoga_number"] <= 27)
        self.assertTrue(1 <= p["karana"]["karana_number"] <= 60)

        m = panch["muhurtha"]
        self.assertIn("rahu_kaalam", m)
        self.assertIn("abhijit_muhurtha", m)
        self.assertIn("brahma_muhurtha", m)

    # 6. Skyfield Ephemeris Tests
    def test_skyfield_astronomy(self):
        dt_utc = datetime(1985, 5, 15, 3, 0, 0, tzinfo=None)
        sidereal = SkyfieldEphemerisEngine.calculate_sidereal_time(dt_utc, self.lon)
        self.assertTrue(0.0 <= sidereal["gast_hours"] <= 24.0)
        self.assertTrue(0.0 <= sidereal["last_degrees"] <= 360.0)

        sun_times = SkyfieldEphemerisEngine.calculate_sun_times(self.dt, self.lat, self.lon, self.tz)
        self.assertIn("sunrise", sun_times)
        self.assertIn("sunset", sun_times)
        self.assertIn("solar_noon", sun_times)

        lunar = SkyfieldEphemerisEngine.calculate_lunar_phenomena(self.dt, 50.0, 340.0)
        self.assertIn("phase_name", lunar)
        self.assertTrue(0.0 <= lunar["illuminated_percentage"] <= 100.0)

    # 7. Unified Advanced Astrology Hub Tests
    def test_advanced_astrology_hub(self):
        profile = AdvancedAstrologyHub.get_complete_advanced_profile(
            dt_local=self.dt,
            lat=self.lat,
            lon=self.lon,
            tz_offset=self.tz,
            name="Ravi Kumar"
        )
        self.assertIn("native_info", profile)
        self.assertIn("jaimini", profile)
        self.assertIn("ashtakavarga", profile)
        self.assertIn("shadbala", profile)
        self.assertIn("panchanga_and_muhurtha", profile)
        self.assertIn("astronomy_skyfield", profile)
        self.assertIn("software_environment", profile)

        # Audit libraries
        libs = AdvancedAstrologyHub.get_available_python_libraries()
        self.assertIn("skyfield", libs["libraries"])
        self.assertIn("vedastro", libs["libraries"])
        self.assertIn("pure_python_bphs", libs["libraries"])


if __name__ == "__main__":
    unittest.main()
