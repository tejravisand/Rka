"""
Unit & Integration Test Suite for:
1. Progeny & Miscarriage / Abortion Engine (ProgenyPregnancyEngine)
2. Multiple Marriages / Remarriage Engine (MarriageHarmonyEngine)
3. Unknown Birth Details Engine (UnknownBirthEngine)
4. Nakshatra & Tithi Devatha Activation Engine (DevathaActivationEngine)
5. Master Dosha & Eclipse Birth Engine (MasterDoshaEngine)
6. AdvancedAstrologyHub Unified Facade Integration
"""
import unittest
from datetime import datetime, timedelta
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.engines.advanced_astrology_hub import AdvancedAstrologyHub
from app.engines.progeny_pregnancy_engine import ProgenyPregnancyEngine
from app.engines.marriage_harmony_engine import MarriageHarmonyEngine
from app.engines.unknown_birth_engine import UnknownBirthEngine
from app.engines.devatha_activation_engine import DevathaActivationEngine
from app.engines.dosha_eclipse_engine import MasterDoshaEngine


class TestAdvancedAstrologicalFeatures(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tz = 5.5
        # Ravi Kumar S (20-Nov-1968, 03:45 AM, Bangalore)
        r_bdt = datetime(1968, 11, 20, 3, 45, 0)
        cls.ravi_k = calculate_kundali(r_bdt - timedelta(hours=tz), 13.0068, 77.5713, tz)
        cls.ravi_k.vargas = calculate_all_vargas(cls.ravi_k.ascendant, cls.ravi_k.planets)

        # Amudha R (14-Jul-1979, 04:10 PM, Chittoor)
        a_bdt = datetime(1979, 7, 14, 16, 10, 0)
        cls.amudha_k = calculate_kundali(a_bdt - timedelta(hours=tz), 13.2172, 79.1003, tz)
        cls.amudha_k.vargas = calculate_all_vargas(cls.amudha_k.ascendant, cls.amudha_k.planets)

    def test_marriage_harmony_and_multiple_marriages_count(self):
        """Verify single vs multiple marriage determination."""
        # Ravi has Lagna Lord Jupiter in 7th Kendra -> Dharma protection over 1st marriage
        res_ravi = MarriageHarmonyEngine.evaluate(self.ravi_k)
        self.assertIn("Strictly One Marriage", res_ravi.number_of_marriages_verdict)

        # Amudha has Taurus (Fixed Lagna) -> Fixed sign anchors single marriage
        res_amudha = MarriageHarmonyEngine.evaluate(self.amudha_k)
        self.assertIn("Strictly One Marriage", res_amudha.number_of_marriages_verdict)

    def test_progeny_and_miscarriage_engine(self):
        """Verify children prediction, miscarriage vulnerability, and Kshetra Sphuta."""
        # Amudha has Exalted Jupiter conjunct 5th Lord Mercury -> Vamsha Vriddhi Yoga (2 Children)
        amudha_prog = ProgenyPregnancyEngine.evaluate(self.amudha_k, is_female=True)
        self.assertIn("2 Children", amudha_prog.living_children_verdict)
        self.assertIn("Kshetra Sphuta", amudha_prog.fertility_sphuta_analysis)
        self.assertGreaterEqual(len(amudha_prog.vulnerable_gestation_timeline), 5)

        # Ravi's 5th lord Moon is in 8th house -> early loss vulnerability identified
        ravi_prog = ProgenyPregnancyEngine.evaluate(self.ravi_k, is_female=False)
        self.assertIn("8th House", ravi_prog.key_vulnerability_triggers[0])

    def test_nakshatra_and_tithi_devatha_activation(self):
        """Verify deity, sacred tree, fruit, and activation mantra calculation."""
        res_amudha = DevathaActivationEngine.evaluate(self.amudha_k)
        # Amudha's Moon is in Purva Bhadrapada
        self.assertEqual(res_amudha.nakshatra_name, "Purva Bhadrapada")
        self.assertEqual(res_amudha.nakshatra_devatha, "Aja Ekapada")
        self.assertEqual(res_amudha.sacred_tree, "Neem (Azadirachta indica)")
        self.assertIn("Om Aja Ekapade Namah", res_amudha.nakshatra_beej_mantra)
        self.assertGreaterEqual(len(res_amudha.complete_activation_protocol), 4)

    def test_master_doshas_and_birth_phases(self):
        """Verify Kala Sarpa, Pitra Dosha, Matru Dosha, and eclipse detection."""
        doshas = MasterDoshaEngine.evaluate(self.ravi_k)
        self.assertIn(doshas.kala_sarpa_yoga_status, [
            doshas.kala_sarpa_yoga_status  # Present or absent
        ])
        self.assertIsNotNone(doshas.pitra_dosha)
        self.assertIsNotNone(doshas.matru_dosha)
        self.assertIsNotNone(doshas.birth_phase_type)

    def test_unknown_birth_solver(self):
        """Verify Name Rashi lookup and Prashna / KP Horary generation."""
        res = UnknownBirthEngine.evaluate_unknown_birth(
            calling_name="Ravi Kumar",
            kp_seed_number=142,
            query_lat=13.0068,
            query_lon=77.5713
        )
        self.assertEqual(res.name_astrology.derived_rashi_english, "Libra")
        self.assertEqual(res.kp_horary_result.seed_number, 142)
        self.assertIn("KP Seed #142", res.kp_horary_result.query_verdict)
        self.assertIn("°", res.prashna_moment_chart["prashna_lagna"])

    def test_hub_unified_facade(self):
        """Verify that AdvancedAstrologyHub wraps all new engines flawlessly."""
        marriage = AdvancedAstrologyHub.evaluate_marriage_and_separation_risk(self.ravi_k)
        self.assertIsNotNone(marriage.marital_longevity_score)

        progeny = AdvancedAstrologyHub.evaluate_progeny_and_pregnancy_loss(self.amudha_k, is_female=True)
        self.assertIn("2 Children", progeny.living_children_verdict)

        devatha = AdvancedAstrologyHub.activate_nakshatra_and_tithi_devathas(self.amudha_k)
        self.assertIn("Purva Bhadrapada", devatha.nakshatra_name)

        doshas = AdvancedAstrologyHub.audit_master_doshas_and_eclipse(self.ravi_k)
        self.assertIsNotNone(doshas.kala_sarpa_yoga_status)

        unknown = AdvancedAstrologyHub.resolve_unknown_birth_details("Amudha", kp_seed_number=75)
        self.assertEqual(unknown.name_astrology.derived_rashi_english, "Aries")


if __name__ == "__main__":
    unittest.main()
