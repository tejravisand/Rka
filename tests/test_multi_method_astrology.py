"""
Unit test suite for the Multi-Method Astrological System:
1. Parashara Engine tests
2. KP Astrology Engine (Sub-Lords, Placidus cusps, Ruling Planets)
3. Dr. B. V. Raman Engine (Ayanamsha, 300 Yogas, Prasna Marga)
4. Lal Kitab Engine (Pakka Ghar, Sleeping Houses, Karmic Debts)
5. Numerology Engine (Mulank, Bhagyank, Chaldean, Pythagorean, Personal Year)
6. Education Stream, Education Break Risk & Academic Remedies
7. Profession, Career Direction & Amatyakaraka
8. Marriage Breakup / Separation Risk Assessment & Preventive Upayas
9. Favourable & Unfavourable Mobile and Vehicle Numbers
10. Present Name Diagnostic & General-Purpose Alternate Names (Non-legal adoption)
11. Comprehensive Shastric Planetary Aspects (Drishti Matrix)
12. Real-Time Present Gochara (Transit) at Moment of Enquiry & Diagnostic
13. Remedies Engine (Mantras, Sacred Plants Pradakshinam, Danam)
14. Master Q&A Engine (Integration and output verification)
"""
import unittest
from datetime import datetime, date

from app.core.kundali import calculate_kundali
from app.engines.kp_engine import KPEngine, calculate_lahiri_ayanamsa
from app.engines.raman_engine import BVRamanEngine, calculate_raman_ayanamsa
from app.engines.lalkitab_engine import LalKitabEngine
from app.engines.numerology_engine import NumerologyEngine
from app.engines.remedies_engine import RemediesEngine, SACRED_PLANTS_CATALOG, NAVAGRAHA_MANTRAS
from app.engines.parashara_engine import ParasharaEngine
from app.engines.education_profession_engine import EducationProfessionEngine
from app.engines.marriage_harmony_engine import MarriageHarmonyEngine
from app.engines.number_harmony_engine import NumberHarmonyEngine
from app.engines.name_tuning_engine import NameTuningEngine
from app.engines.aspects_engine import AspectsEngine
from app.engines.transit_prashna_engine import TransitPrashnaEngine
from app.engines.multi_method_qa import (
    MasterAstrologyQAEngine,
    ClientProfile,
    QueryContext
)


class TestMultiMethodAstrology(unittest.TestCase):

    def setUp(self):
        # Sample Native: Ravi Kumar S, May 15, 1983, 10:30 AM IST, Bengaluru
        self.birth_dt = datetime(1983, 5, 15, 10, 30, 0)
        self.lat = 12.9716
        self.lon = 77.5946
        self.tz = 5.5

        # Query time: Oct 25, 2026, 11:49 AM IST
        self.query_dt = datetime(2026, 10, 25, 11, 49, 49)

        self.client = ClientProfile(
            name="Ravi Kumar S",
            birth_datetime_local=self.birth_dt,
            tz_offset_hours=self.tz,
            latitude=self.lat,
            longitude=self.lon,
            place_name="Bengaluru, Karnataka"
        )

        self.query = QueryContext(
            question_text="Will I get promoted to Executive Director and when will my business succeed?",
            question_category="Career & Promotion",
            query_datetime_local=self.query_dt,
            query_latitude=self.lat,
            query_longitude=self.lon,
            query_place_name="Bengaluru, Karnataka",
            specific_mobile="9845012345",
            specific_vehicle_plate="KA 01 AB 1234"
        )

    def test_kp_sub_lord_calculation(self):
        kp_info = KPEngine.calculate_kp_sub(0.0)
        self.assertEqual(kp_info.sign_name, "Aries")
        self.assertEqual(kp_info.nakshatra_name, "Ashwini")
        self.assertEqual(kp_info.nakshatra_lord, "Ketu")
        self.assertEqual(kp_info.sub_lord, "Ketu")

        kp_info_venus = KPEngine.calculate_kp_sub(1.0)
        self.assertEqual(kp_info_venus.nakshatra_lord, "Ketu")
        self.assertEqual(kp_info_venus.sub_lord, "Venus")

    def test_kp_ruling_planets(self):
        rp = KPEngine.calculate_ruling_planets(
            query_dt_local=self.query_dt,
            tz_offset_hours=self.tz,
            latitude=self.lat,
            longitude=self.lon
        )
        self.assertEqual(rp.vara_lord, "Sun")
        self.assertTrue(len(rp.strong_rulers) >= 3)

    def test_raman_ayanamsa_and_yogas(self):
        ayan_1900 = calculate_raman_ayanamsa(2415020.0)
        self.assertAlmostEqual(ayan_1900, 21.0122, places=3)

        raman_ayan, raman_asc, raman_planets = BVRamanEngine.calculate_raman_positions(
            dt_utc=datetime(1983, 5, 15, 5, 0, 0),
            latitude=self.lat,
            longitude=self.lon
        )
        yogas = BVRamanEngine.detect_300_combinations(raman_asc, raman_planets)
        self.assertTrue(len(yogas) >= 1)

    def test_lalkitab_debts_and_sleeping_houses(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        lk = LalKitabEngine.evaluate_kundali(natal, "Career")
        self.assertTrue(len(lk.sleeping_houses) > 0)
        self.assertTrue(isinstance(lk.active_karmic_debts, list))
        self.assertTrue(len(lk.specific_totke_for_query) >= 3)

    def test_numerology_calculations(self):
        num_profile = NumerologyEngine.evaluate(
            name="Ravi Kumar S",
            birth_date=date(1983, 5, 15),
            query_date=date(2026, 10, 25),
            query_category="Career"
        )
        self.assertEqual(num_profile.mulank, 6)
        self.assertEqual(num_profile.bhagyank, 5)
        self.assertEqual(num_profile.chaldean_name_compound, 28)
        self.assertEqual(num_profile.chaldean_name_single, 1)
        self.assertEqual(num_profile.personal_year, 3)

    def test_education_stream_and_break(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        ed = EducationProfessionEngine.evaluate_education_stream(natal)
        br = EducationProfessionEngine.evaluate_education_break(natal)

        self.assertIn("Engineering", ed.primary_stream)
        self.assertTrue(len(ed.recommended_degrees) >= 2)
        self.assertIsNotNone(br.break_risk_level)
        self.assertTrue(len(br.academic_remedies) >= 3)

    def test_profession_evaluation(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        pf = EducationProfessionEngine.evaluate_profession(natal)

        self.assertIsNotNone(pf.career_path_verdict)
        self.assertIsNotNone(pf.amatyakaraka_planet)
        self.assertTrue(len(pf.top_recommended_domains) >= 3)

    def test_marriage_harmony_and_breakup(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        mb = MarriageHarmonyEngine.evaluate(natal)

        self.assertTrue(0 <= mb.marital_longevity_score <= 100)
        self.assertIsNotNone(mb.breakup_risk_level)
        self.assertIsNotNone(mb.manglik_dosha_status)
        self.assertTrue(len(mb.preventive_remedies_for_harmony) >= 3)

    def test_mobile_and_vehicle_numbers(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)

        # Mobile
        mob = NumberHarmonyEngine.evaluate_mobile_number_guidance(6, 5, "9845012345")
        self.assertTrue(len(mob.favourable_single_totals) >= 1)
        self.assertTrue(len(mob.unfavourable_single_totals) >= 1)
        self.assertIsNotNone(mob.evaluated_custom_number)
        self.assertEqual(mob.evaluated_custom_number.total_digits_sum, 41)
        self.assertEqual(mob.evaluated_custom_number.reduced_single_digit, 5)

        # Vehicle
        veh = NumberHarmonyEngine.evaluate_vehicle_guidance(natal, 6, 5, "KA 01 AB 1234")
        self.assertTrue(len(veh.favourable_plate_single_sums) >= 1)
        self.assertTrue(len(veh.unfavourable_plate_single_sums) >= 1)
        self.assertIsNotNone(veh.evaluated_custom_plate)
        self.assertEqual(veh.evaluated_custom_plate.four_digit_sum, 10)
        self.assertEqual(veh.evaluated_custom_plate.four_digit_reduced, 1)
        self.assertIsNotNone(veh.four_wheeler_feasibility)
        self.assertIsNotNone(veh.vehicle_ownership_diagnosis)

    def test_name_tuning_and_alternate_names(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        nt = NameTuningEngine.evaluate_name("Ravi Kumar S", natal, 6, 5)

        self.assertEqual(nt.present_chaldean_compound, 28)
        self.assertEqual(nt.present_chaldean_single, 1)
        self.assertTrue(len(nt.spelling_calibration_suggestions) >= 1)
        self.assertTrue(len(nt.vedic_nakshatra_name_options) >= 1)
        self.assertTrue(len(nt.non_legal_adoption_guidelines) >= 3)

        # Test Royal Compound evaluation (e.g. compound 23 or 24)
        nt_royal = NameTuningEngine.evaluate_name("Ravi Kumaar S", natal, 6, 5)
        self.assertIn(nt_royal.present_chaldean_compound, [19, 23, 24, 27, 32, 33, 37, 41, 42, 45, 46, 50, 29])
        if nt_royal.present_chaldean_compound in [19, 23, 24, 27, 32, 33, 37, 41, 42, 45, 46, 50]:
            self.assertIn("Royal Compound", nt_royal.present_name_status)

    def test_aspects_matrix(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        asp = AspectsEngine.calculate_detailed_aspects(natal)

        self.assertTrue(len(asp.all_aspects_list) >= 15)
        self.assertTrue(len(asp.key_points_aspects) >= 5)

    def test_realtime_gochara_at_enquiry(self):
        birth_utc = datetime(1983, 5, 15, 5, 0, 0)
        natal = calculate_kundali(birth_utc, self.lat, self.lon, self.tz)
        goc = TransitPrashnaEngine.calculate_realtime_gochara(
            natal, self.query_dt, self.lat, self.lon, self.tz
        )

        self.assertEqual(len(goc.transiting_planets), 9)
        self.assertIsNotNone(goc.saturn_transit_verdict)
        self.assertIsNotNone(goc.jupiter_transit_verdict)
        self.assertIsNotNone(goc.why_this_question_now_diagnostic)

    def test_remedies_catalog(self):
        self.assertIn("Peepal", SACRED_PLANTS_CATALOG)
        self.assertIn("Shami", SACRED_PLANTS_CATALOG)
        peepal = SACRED_PLANTS_CATALOG["Peepal"]
        self.assertEqual(peepal.prescribed_pradakshinam_rounds, 21)

        self.assertIn("Saturn", NAVAGRAHA_MANTRAS)
        sat_m = NAVAGRAHA_MANTRAS["Saturn"]
        self.assertEqual(sat_m.prescribed_japa_count, 23000)

    def test_master_qa_engine_integration(self):
        response = MasterAstrologyQAEngine.evaluate_consultation(self.client, self.query)
        self.assertIsNotNone(response.unified_verdict)
        self.assertTrue(response.consensus_probability_percent >= 50)
        # Verify all new horizons
        self.assertIsNotNone(response.education_stream)
        self.assertIsNotNone(response.education_break)
        self.assertIsNotNone(response.profession)
        self.assertIsNotNone(response.marriage_breakup)
        self.assertIsNotNone(response.mobile_guidance)
        self.assertIsNotNone(response.vehicle_guidance)
        self.assertIsNotNone(response.name_tuning)
        self.assertIsNotNone(response.detailed_aspects)
        self.assertIsNotNone(response.present_gochara)
        self.assertIsNotNone(response.medical_dossier)
        self.assertGreaterEqual(len(response.medical_dossier.consensus_vulnerabilities), 3)


if __name__ == "__main__":
    unittest.main()
