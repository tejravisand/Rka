import unittest
from datetime import datetime
from app.core.kundali import calculate_kundali
from app.engines.integrative_medical_engine import (
    IntegrativeMedicalEngine,
    IntegrativeMedicalDossier
)


class TestIntegrativeMedicalAstrology(unittest.TestCase):

    def setUp(self):
        # 15-Aug-1995 10:30 AM Bengaluru
        self.dt_utc = datetime(1995, 8, 15, 5, 0)
        self.lat = 12.9716
        self.lon = 77.5946
        self.tz = 5.5
        self.kundali = calculate_kundali(self.dt_utc, self.lat, self.lon, self.tz)
        self.dossier = IntegrativeMedicalEngine.evaluate(self.kundali, client_name="Integrative Test")

    def test_dossier_structure(self):
        self.assertIsInstance(self.dossier, IntegrativeMedicalDossier)
        self.assertEqual(self.dossier.client_name, "Integrative Test")
        self.assertIsNotNone(self.dossier.vedic_report)
        self.assertIsNotNone(self.dossier.western_report)

    def test_cross_correlations(self):
        corr = self.dossier.cross_correlations
        self.assertGreaterEqual(len(corr), 3)
        for c in corr:
            self.assertGreaterEqual(c.correlation_score, 0.0)
            self.assertLessEqual(c.correlation_score, 1.0)

    def test_consensus_vulnerabilities(self):
        consensus = self.dossier.consensus_vulnerabilities
        self.assertGreaterEqual(len(consensus), 3)
        systems = [cv.body_system for cv in consensus]
        self.assertTrue(any("Cardiovascular" in s for s in systems))

    def test_unified_therapy(self):
        therapy = self.dossier.unified_therapy
        self.assertGreater(len(therapy.ayurvedic_herbs), 0)
        self.assertGreater(len(therapy.western_herbalism), 0)
        self.assertGreater(len(therapy.unified_dietary_guidelines), 0)
        self.assertGreater(len(therapy.healing_mantras_and_frequencies), 0)


if __name__ == "__main__":
    unittest.main()
