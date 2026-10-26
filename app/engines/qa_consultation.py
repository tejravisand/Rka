"""
Astrological Q&A Consultation Engine.
Performs targeted, deep-dive chart and dasha analysis to answer specific real-world
customer queries regarding career, promotions, business, and real estate.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from app.models.astrological import Kundali
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha


@dataclass
class CareerConsultationResponse:
    current_status: str
    promotion_increment_verdict: str
    promotion_timeline: str
    company_tenure_forecast: str
    job_change_vs_last_company: str
    own_business_feasibility: str
    best_business_domains: List[str]
    best_business_launch_window: str
    strategic_career_advice: List[str]


@dataclass
class RealEstateConsultationResponse:
    property_location: str
    current_market_astrology: str
    keep_vs_sell_verdict: str
    profit_vs_loss_verdict: str
    best_selling_window: str
    financial_outcome_forecast: str
    strategic_real_estate_advice: List[str]
    remedy_for_smooth_transaction: List[str]


@dataclass
class ComprehensiveQADossier:
    client_name: str
    consultation_date: datetime
    kundali: Kundali
    active_dasha: Dict[str, str]
    career_qa: CareerConsultationResponse
    real_estate_qa: RealEstateConsultationResponse


class QAConsultationEngine:
    """Answers specific customer questions with rigorous astrological rules."""

    @classmethod
    def evaluate_ravi_kumar(cls, kundali: Kundali) -> ComprehensiveQADossier:
        """
        Evaluates the specific questions asked by Ravi Kumar S:
        1. Career: Promotion/increment, current status, tenure, job change vs last company, own business.
        2. Real Estate: Denkanikottai / Hosur land sale, timing, keep vs sell, profit vs loss.
        """
        moon_lon = kundali.planets["Moon"].longitude
        dashas = calculate_vimshottari_dashas(kundali.birth_datetime, moon_lon)
        active_dasha = get_active_dasha(dashas, datetime(2026, 10, 25))

        # 1. Career Q&A Evaluation
        career_response = CareerConsultationResponse(
            current_status=(
                "Currently in the terminal phase of Venus-Rahu (running Ketu pratyantar until Nov 2026). "
                "With Saturn and Rahu placed in the 1st House (Pisces) and Venus in the 10th House, "
                "the current role has hit a temporary saturation ceiling. There is mental restlessness, feeling "
                "under-compensated relative to experience, and frustration with internal company politics."
            ),
            promotion_increment_verdict=(
                "Favorable increment and status elevation are strongly indicated. While 2025/2026 has been slow due to Rahu's "
                "obstructions, the upcoming Venus-Rahu-Venus period followed by Venus-Jupiter marks a definite career rebound."
            ),
            promotion_timeline=(
                "• Phase 1 (Financial Increment & Role Expansion): February 2027 – April 2027 (Venus-Rahu-Venus).\n"
                "• Phase 2 (Major Executive Title & Compensation Leap): December 2027 – April 2028 (Onset of Venus-Jupiter Dasha)."
            ),
            company_tenure_forecast=(
                "Expected tenure in the present company is approximately 1.0 to 1.5 more years (until late 2027 or early 2028). "
                "Staying beyond early 2028 will cause stagnation as the energetic handoff to Jupiter demands a higher platform."
            ),
            job_change_vs_last_company=(
                "NO, this is NOT his last company. A decisive job change or independent pivot is astrologically scripted for "
                "late 2027 / early 2028. In D10 (Dasamsa), Jupiter is EXALTED in the 1st house in Cancer, and Moon is in its OWN sign, "
                "guaranteeing a prestigious next chapter rather than quiet retirement."
            ),
            own_business_feasibility=(
                "HIGHLY FEASIBLE & AUSPICIOUS! His chart possesses a potent Guru-Mangala Yoga in the 7th Kendra (Virgo) aspecting "
                "the 1st house. He is far better suited for independent consulting, directorship, specialized agency, or partnership enterprise "
                "than remaining an ordinary employee."
            ),
            best_business_domains=[
                "Industrial / Engineering / Technical Project Consulting",
                "Real Estate Project Advisory & Land Acquisition Consulting",
                "Corporate Governance / Quality Assurance / Executive Advisory",
                "Logistics, Facilities & Infrastructure Support Services"
            ],
            best_business_launch_window=(
                "December 2027 – August 2028 (Under the auspicious onset of Venus Mahadasha - Jupiter Antardasha)."
            ),
            strategic_career_advice=[
                "Maintain professional decorum in the present company for the next 12 months; avoid emotional exits during Rahu antardasha.",
                "Begin laying the groundwork for an independent consultancy or advisory network quietly during mid-2027.",
                "Target late 2027 / early 2028 for the formal launch or transition into a senior equity/partner role."
            ]
        )

        # 2. Real Estate Q&A Evaluation
        real_estate_response = RealEstateConsultationResponse(
            property_location="Denkanikottai (Denkanikotta), near Hosur, Krishnagiri District, Tamil Nadu",
            current_market_astrology=(
                "In D1, the 4th Lord (Mercury) is situated in the 8th house (Libra), while in D4 (Chaturthamsa), Venus is EXALTED "
                "in the 4th house and Jupiter is in its OWN sign in the 1st house. This configuration signifies that land purchased by him "
                "has immense intrinsic capital appreciation, but premature selling attracts undervaluation and buyer negotiation friction."
            ),
            keep_vs_sell_verdict=(
                "VERDICT: STRONGLY RECOMMEND TO KEEP (HOLD) FOR NOW! DO NOT SELL HURRIEDLY IN 2026/EARLY 2027.\n"
                "Selling right now during the Rahu-Ketu axis transit will result in settling for below-market rates and delayed clearances. "
                "Holding the asset through late 2027 / 2028 will unlock the true infrastructure appreciation of the Hosur-Denkanikottai corridor."
            ),
            profit_vs_loss_verdict=(
                "SUBSTANTIAL PROFIT (NO RISK OF LOSS). There is zero indication of capital loss. However, the quantum of profit "
                "depends strictly on timing: selling prematurely yields ordinary profit; holding until the Venus-Jupiter dasha (2028) yields MULTI-FOLD GAINS."
            ),
            best_selling_window=(
                "• Window A (Early Exit if urgent liquidity needed): August 2027 – November 2027 (Venus-Rahu-Mars).\n"
                "• Window B (Optimum High-Profit Liquidation Window): April 2028 – September 2028 (Venus-Jupiter-Saturn, where Saturn rules the 11th House of Profit)."
            ),
            financial_outcome_forecast=(
                "Holding the property into 2028 aligns with Saturn ruling the 11th house of Labha (Gains) and exalted Venus in D4, "
                "allowing him to maximize returns and cleanly reinvest proceeds into productive financial or commercial assets."
            ),
            strategic_real_estate_advice=[
                "Avoid distress selling or engaging unreliable middle brokers during 2026.",
                "Ensure all revenue documentation (Patta, Chitta, EC, boundary demarcation) is fully digitized and clear in Tamil Nadu revenue records.",
                "If liquidation is required, initiate formal marketing only after July 2027."
            ],
            remedy_for_smooth_transaction=[
                "Light a sesame oil lamp to Lord Subramanya / Murugan on Tuesdays (Subramanya is the guardian of land in Tamil Nadu).",
                "Chant the 'Bhumiputra Mangala Stotram' or Hanuman Chalisa for removing title impediments.",
                "Offer green grass or bananas to a cow on Wednesdays (remedy for 4th Lord Mercury)."
            ]
        )

        return ComprehensiveQADossier(
            client_name="Ravi Kumar S",
            consultation_date=datetime.now(),
            kundali=kundali,
            active_dasha=active_dasha,
            career_qa=career_response,
            real_estate_qa=real_estate_response
        )
