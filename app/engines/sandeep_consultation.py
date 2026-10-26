"""
Comprehensive Consultation Engine for Sandeep R.
Evaluates:
1. Present Job Status & Confirmation Timeline.
2. Govt Job vs Private Job Comparison, Probability, Features & Remedies.
3. Abroad Job / Foreign Travel Timeline.
4. Marriage Prediction: Timing, Arranged vs Love, Intercaste/Background, Far-off place, Wife's Nature & Marital Life.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Tuple
from app.models.astrological import Kundali
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha


@dataclass
class JobConfirmationConsultation:
    current_status: str
    confirmation_verdict: str
    confirmation_timeline: str
    probation_clearance_factors: str
    immediate_actions: List[str]


@dataclass
class GovtVsPrivateConsultation:
    govt_job_probability: str
    govt_job_sectors: List[str]
    private_job_features: List[str]
    comparative_matrix: List[Tuple[str, str, str]]
    strategic_career_verdict: str
    effective_remedies: List[str]


@dataclass
class AbroadJobConsultation:
    abroad_possibility: str
    astrological_drivers: str
    target_geographies: List[str]
    timeline_first_wave: str
    timeline_longterm_relocation: str
    career_profile_abroad: str


@dataclass
class MarriageConsultation:
    marriage_timing: str
    ideal_age_at_marriage: str
    marriage_type: str                   # Love, Arranged, or Arranged-cum-Love
    caste_and_background: str            # Intercaste, Inter-subcaste, religion
    geographical_origin: str             # Within relatives or far-off place
    wife_personality_and_career: str     # Supportive, working, attributes
    marital_harmony_score: str
    potential_challenges_and_remedies: List[str]


@dataclass
class SandeepQADossier:
    client_name: str
    kundali: Kundali
    active_dasha: Dict[str, str]
    job_confirmation: JobConfirmationConsultation
    govt_vs_private: GovtVsPrivateConsultation
    abroad_job: AbroadJobConsultation
    marriage: MarriageConsultation


class SandeepConsultationEngine:
    """Detailed astrological predictions for Sandeep R (DOB: 05-02-2000, 7:45 AM, Bengaluru)."""

    @classmethod
    def evaluate(cls, kundali: Kundali) -> SandeepQADossier:
        moon_lon = kundali.planets["Moon"].longitude
        dashas = calculate_vimshottari_dashas(kundali.birth_datetime, moon_lon)
        active_dasha = get_active_dasha(dashas, datetime(2026, 10, 25))

        # 1. Job Confirmation
        job_conf = JobConfirmationConsultation(
            current_status=(
                "Sandeep R has entered the crucial Rahu Mahadasha - Sun Antardasha (Rahu-Sun) in September 2026. "
                "Sun is his Lagna Lord placed in the 6th House (Makara - House of Employment & Service). "
                "While the preceding Rahu-Venus period created uncertainty and delays, the entry of the Lagna Lord Sun "
                "triggers strong stability, official recognition, and service formalization."
            ),
            confirmation_verdict=(
                "CONFIRMED WITH HIGH CERTAINTY. The current job will be successfully confirmed. "
                "In D10 (Dasamsa), Sun is EXALTED in Aries (Mesha), which guarantees official employment confirmation "
                "and probation clearance."
            ),
            confirmation_timeline=(
                "• Primary Official Confirmation Window: January 2027 – April 2027 (Under Rahu-Sun-Jupiter and Rahu-Sun-Saturn).\n"
                "• Immediate Interim Clearance: November 2026 – December 2026 (Rahu-Sun-Rahu)."
            ),
            probation_clearance_factors=(
                "Saturn rules the 6th house of employment in D1, while Jupiter casts its benefic 9th aspect. "
                "The probation clearance will be formally signed off once transiting Jupiter enters favorable motion in early 2027."
            ),
            immediate_actions=[
                "Maintain consistent performance documentation and project deliverables through December 2026.",
                "Avoid unnecessary workplace debates or friction with reporting managers during November 2026.",
                "Expect formal appraisal documentation and letter of permanency between January and March 2027."
            ]
        )

        # 2. Govt vs Private Job Comparison
        govt_vs_pvt = GovtVsPrivateConsultation(
            govt_job_probability="65% – 70% (Favorable if attempted before July 2027)",
            govt_job_sectors=[
                "Banking & Financial Institutions (IBPS PO, SBI, RBI Grade B)",
                "Central / State Public Sector Undertakings (PSUs & Administrative Cadres)",
                "Defence Accounts, Auditing & Revenue Regulatory Authorities",
                "State Gazetted Administrative / Technical Services (KPSC / Group A/B)"
            ],
            private_job_features=[
                "High financial scaling and early wealth accumulation (10th Lord Venus in 5th house).",
                "Exposure to cutting-edge technologies, global corporate practices, and meritocratic growth.",
                "Direct springboard for international travel and overseas onsite postings (Rahu in 12th house)."
            ],
            comparative_matrix=[
                ("Job Security", "Extremely High (Tenured stability)", "Moderate (Performance-driven)"),
                ("Compensation & Scaling", "Moderate & Structured (Pay Commission)", "Very High & Exponential"),
                ("International Exposure", "Very Limited (Domestic postings)", "Extremely High (Onsite & Global transfer)"),
                ("Work-Life Balance", "Predictable & Fixed Hours", "Demanding / Dynamic deadlines"),
                ("Astrological Alignment", "Sun in 6th (Exalted in D10) supports Govt", "Rahu in 12th + Venus in 10th supports MNC/Private")
            ],
            strategic_career_verdict=(
                "RECOMMENDED DUAL-TRACK STRATEGY: Maintain the private corporate job as an anchor, while actively writing "
                "competitive exams for Central Govt / Banking / PSUs during the current Rahu-Sun window (up to July 2027). "
                "If a top-tier Govt/Banking post is secured before mid-2027, take it for lifelong security. "
                "Otherwise, transition fully into an MNC private career, which will rapidly take him ABROAD with much higher financial returns."
            ),
            effective_remedies=[
                "Surya Arghya: Offer water with a pinch of red kumkum and jaggery from a copper vessel to the rising Sun daily morning reciting 'Om Ghrinih Suryaya Namah'.",
                "Aditya Hridaya Stotram: Recite every Sunday morning to empower Lagna Lord Sun.",
                "Subramanya / Kartikeya Pooja: Visit a Murugan/Subramanya temple on Tuesdays (Mars is Yogakaraka).",
                "Cow Seva: Feed green fodder or bananas to a cow on Wednesdays."
            ]
        )

        # 3. Abroad Job / Foreign Travel
        abroad_job = AbroadJobConsultation(
            abroad_possibility="100% CONFIRMED (Extremely Strong Astrological Yoga)",
            astrological_drivers=(
                "Rahu is powerfully placed in the 12th House (Cancer - Water Sign) in D1. The 12th house governs foreign lands, "
                "transoceanic travel, and overseas residence. In D10 (Dasamsa), Rahu is placed in the 9th house of long-distance foreign journeys (Gemini). "
                "Furthermore, he is running Rahu Mahadasha until February 2030, which guarantees international relocation."
            ),
            target_geographies=[
                "North America (USA, Canada)",
                "Europe & United Kingdom (Tech/Finance hubs)",
                "Southeast Asia (Singapore / Middle East - UAE)"
            ],
            timeline_first_wave="July 2027 – January 2029 (Under Rahu Mahadasha - Moon Antardasha; Moon is the 12th Lord of Foreign Lands!)",
            timeline_longterm_relocation="2029 – 2032 (During the transition into Jupiter Mahadasha; long-term overseas residency)",
            career_profile_abroad="Technical Systems, Enterprise Solutions, Financial Data Analytics, or Corporate Operations."
        )

        # 4. Marriage Prediction
        marriage = MarriageConsultation(
            marriage_timing="Mid-2028 to Early 2029 (~Age 28.5 to 29 Years)",
            ideal_age_at_marriage="28 to 29.5 Years",
            marriage_type="Arranged-cum-Love / Modern Arranged (Self-Choice with Strong Family Endorsement)",
            caste_and_background=(
                "Same broader religious faith (Hindu), but different sub-caste, community, or distinct cultural background (Inter-subcaste). "
                "Rahu in the 12th house and Saturn debilitated in the 9th house break traditional rigidity; the alliance will not follow "
                "narrow orthodox family norms, but will be mutually respected."
            ),
            geographical_origin="Far-Off Place (Different city, state, or met during professional/educational tenure. NOT within relatives).",
            wife_personality_and_career=(
                "Wife will be an educated, working professional (Finance, Tech, Corporate, or Creative Design). "
                "In D9 (Navamsa), Venus is in its OWN SIGN (Libra) in the 5th house, and Moon is EXALTED in Taurus. "
                "She will be charming, intelligent, aesthetically refined, independent-minded, and highly supportive of his career advancement."
            ),
            marital_harmony_score="8.0 / 10 (Very Favorable & Financially Auspicious)",
            potential_challenges_and_remedies=[
                "Mercury sits in the 7th house and Mars sits in the 8th house (minor Kuja/Manglik influence).",
                "Occasional intellectual arguments or work-related physical distance/travel need conscious balance.",
                "Remedy: Perform Gauri-Shankar Pooja before marriage and ensure horoscope matching (Ashtakoota & Manglik reconciliation)."
            ]
        )

        return SandeepQADossier(
            client_name="Sandeep R",
            kundali=kundali,
            active_dasha=active_dasha,
            job_confirmation=job_conf,
            govt_vs_private=govt_vs_pvt,
            abroad_job=abroad_job,
            marriage=marriage
        )
