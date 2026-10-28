"""
Unit tests for the Interactive Consultation Flow, Question Catalog,
Marital Status conditioning, Targeted Prediction, and PDF Generation.
"""
import unittest
import os
from datetime import datetime

from app.core.cities import lookup_city, get_default_coordinates
from app.engines.question_catalog import QuestionCatalogEngine, PURPOSE_CATALOG
from app.engines.targeted_prediction_engine import TargetedPredictionEngine
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from qa_consultation_app import run_consultation_flow


class TestConsultationWorkflow(unittest.TestCase):

    def test_city_lookup(self):
        bengaluru = lookup_city("Bengaluru")
        self.assertIsNotNone(bengaluru)
        self.assertAlmostEqual(bengaluru[0], 12.9716, places=2)
        self.assertAlmostEqual(bengaluru[1], 77.5946, places=2)

        mumbai = lookup_city("Mumbai")
        self.assertIsNotNone(mumbai)
        self.assertAlmostEqual(mumbai[0], 19.0760, places=2)

        delhi = lookup_city("Delhi")
        self.assertIsNotNone(delhi)
        self.assertAlmostEqual(delhi[0], 28.6139, places=2)

    def test_question_catalog_three_choices(self):
        purposes = QuestionCatalogEngine.list_purposes()
        self.assertEqual(len(purposes), 9)

        for p_key, title, _ in purposes:
            # Test Unmarried
            q_unmarried = QuestionCatalogEngine.get_three_question_choices(p_key, "Unmarried")
            self.assertEqual(len(q_unmarried), 3, f"Purpose {p_key} should have exactly 3 questions for Unmarried")

            # Test Married
            q_married = QuestionCatalogEngine.get_three_question_choices(p_key, "Married")
            self.assertEqual(len(q_married), 3, f"Purpose {p_key} should have exactly 3 questions for Married")

            # Distinct question sets for marriage domain
            if p_key == "marriage":
                self.assertNotEqual(q_unmarried, q_married)

    def test_targeted_prediction_engine(self):
        # Setup Kundali for test
        bdt = datetime(1995, 10, 15, 5, 0, 0)
        kundali = calculate_kundali(bdt, 12.9716, 77.5946, 5.5)
        kundali.vargas = calculate_all_vargas(kundali.ascendant, kundali.planets)
        active_dasha = {"mahadasha": "Saturn", "antardasha": "Mercury"}

        # 1. Unmarried marriage question
        q1 = "When will I get married, and what are my most favorable astrological timing windows?"
        res1 = TargetedPredictionEngine.predict(
            kundali=kundali,
            question=q1,
            purpose_key="marriage",
            marital_status="Unmarried",
            active_dasha=active_dasha,
            query_dt=datetime.now()
        )
        self.assertIn("MARRIAGE", res1.unified_verdict.upper())
        self.assertGreaterEqual(res1.confidence_score, 70)
        self.assertTrue(len(res1.tailored_remedies) >= 3)

        # 2. Married marriage question
        q2 = "How can my spouse and I resolve marital misunderstandings and restore deep affection and harmony?"
        res2 = TargetedPredictionEngine.predict(
            kundali=kundali,
            question=q2,
            purpose_key="marriage",
            marital_status="Married",
            active_dasha=active_dasha,
            query_dt=datetime.now()
        )
        self.assertIn("AFFECTION", res2.unified_verdict.upper())
        self.assertGreaterEqual(res2.confidence_score, 70)

    def test_end_to_end_consultation_pdf_export(self):
        pdf_out = os.path.join("output", "workflow_test_client_consultation.pdf")
        if os.path.exists(pdf_out):
            os.remove(pdf_out)

        response = run_consultation_flow(
            name="Workflow Test Client",
            dob_str="1990-05-10",
            tob_str="14:30:00",
            place="Bengaluru, Karnataka",
            lat=12.9716,
            lon=77.5946,
            tz_offset=5.5,
            question="When will I get my next job promotion, salary increment, or significant career growth?",
            category="Career",
            marital_status="Unmarried",
            output_prefix="consultation"
        )

        self.assertTrue(os.path.exists(pdf_out), f"PDF was not created at {pdf_out}")
        self.assertGreater(os.path.getsize(pdf_out), 5000, "PDF size is unexpectedly small")


if __name__ == "__main__":
    unittest.main()
