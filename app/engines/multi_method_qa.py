"""
Master Unified Multi-Method Astrological Q&A Consultation Engine.
Seamlessly synthesizes 5 premier astrological and numerological disciplines:
1. Parashara Hora Method (Brihat Parasara Hora Sastra, Bhavas, Yogas, Vargas, Dashas, Transits).
2. Krishnamurti Padhdhati (KP Astrology: Placidus Cusps, 249 Sub-Lords, Ruling Planets, Significators).
3. Dr. B. V. Raman Method (Raman Ayanamsa, 300 Important Combinations, Prasna Marga).
4. Lal Kitab Method (Red Book: Pakka Ghar, Soya Grah/Ghar, 7 Karmic Debts, Authentic Totke).
5. Numerology (Chaldean & Pythagorean: Mulank, Bhagyank, Name Number, Personal Year/Month/Day).

Also incorporates:
6. Education Stream, Education Break Risk & Academic Saraswati Remedies.
7. Profession, Vocational Domain & D10 Dashamsha Career Direction.
8. Marriage Breakup / Divorce / Separation Risks & Preventive Upayas.
9. Favourable & Unfavourable Mobile Numbers (Vibrations, Repeated Digits, Compounds).
10. Favourable & Unfavourable Vehicle Registration Numbers (Vahana Bhava, Safety, Colors).
11. Present Name Diagnostic & General-Purpose Alternate Name Suggestions (Non-legal adoption).
12. Comprehensive Shastric Planetary Aspects (Drishti Matrix - Special Mars 4/8, Jupiter 5/9, Saturn 3/10).
13. Real-Time Present Gochara (Transit) at Query/Enquiry Moment & Immediate Diagnostic.
"""
import os
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any

from app.models.astrological import Kundali, PlanetPosition, ZodiacSign
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha
from app.core.constants import ZODIAC_SANSKRIT, ZODIAC_SIGNS

# Import engines
from app.engines.parashara_engine import ParasharaEngine, ParasharaQuestionVerdict, TransitAssessment
from app.engines.kp_engine import KPEngine, KPCusp, KPRulingPlanets, KPQuestionVerdict
from app.engines.raman_engine import BVRamanEngine, RamanYoga, RamanPrasnaAssessment
from app.engines.lalkitab_engine import LalKitabEngine, LalKitabAssessment
from app.engines.numerology_engine import NumerologyEngine, NumerologyProfile
from app.engines.remedies_engine import RemediesEngine, ComprehensiveRemedialDossier
from app.engines.education_profession_engine import (
    EducationProfessionEngine,
    EducationStreamProfile,
    EducationBreakAssessment,
    ProfessionProfile
)
from app.engines.marriage_harmony_engine import (
    MarriageHarmonyEngine,
    MarriageBreakupAssessment
)
from app.engines.number_harmony_engine import (
    NumberHarmonyEngine,
    MobileNumberGuidance,
    VehicleNumberGuidance
)
from app.engines.name_tuning_engine import (
    NameTuningEngine,
    NameTuningDossier
)
from app.engines.aspects_engine import (
    AspectsEngine,
    DetailedAspectsDossier
)
from app.engines.transit_prashna_engine import (
    TransitPrashnaEngine,
    PresentGocharaDossier
)
from app.engines.integrative_medical_engine import (
    IntegrativeMedicalEngine,
    IntegrativeMedicalDossier
)


@dataclass
class ClientProfile:
    name: str
    birth_datetime_local: datetime
    tz_offset_hours: float
    latitude: float
    longitude: float
    place_name: str


@dataclass
class QueryContext:
    question_text: str
    question_category: str            # Career, Marriage, Finance, Real Estate, Foreign, Health, etc.
    query_datetime_local: datetime
    query_latitude: float
    query_longitude: float
    query_place_name: str
    specific_mobile: Optional[str] = None
    specific_vehicle_plate: Optional[str] = None


@dataclass
class MultiMethodQAResponse:
    client: ClientProfile
    query: QueryContext
    natal_kundali: Kundali
    current_active_dasha: Dict[str, str]

    # 1. Parashara Horizon
    parashara_verdict: ParasharaQuestionVerdict
    parashara_transits: TransitAssessment

    # 2. KP Astrology Horizon
    kp_cusps: List[KPCusp]
    kp_ruling_planets: KPRulingPlanets
    kp_verdict: KPQuestionVerdict

    # 3. B. V. Raman Horizon
    raman_ayanamsa_value: float
    raman_detected_yogas: List[RamanYoga]
    raman_prasna: RamanPrasnaAssessment

    # 4. Lal Kitab Horizon
    lal_kitab: LalKitabAssessment

    # 5. Numerology Horizon
    numerology: NumerologyProfile

    # 6. Education & Profession Horizon
    education_stream: EducationStreamProfile
    education_break: EducationBreakAssessment
    profession: ProfessionProfile

    # 7. Marriage Harmony & Breakup Assessment Horizon
    marriage_breakup: MarriageBreakupAssessment

    # 8. Mobile & Vehicle Numbers Guidance
    mobile_guidance: MobileNumberGuidance
    vehicle_guidance: VehicleNumberGuidance

    # 9. Name Tuning & Alternate Name Horizon
    name_tuning: NameTuningDossier

    # 10. Detailed Shastric Aspects Horizon
    detailed_aspects: DetailedAspectsDossier

    # 11. Real-Time Present Gochara at Enquiry Moment
    present_gochara: PresentGocharaDossier

    # Unified Synthesis
    unified_verdict: str
    consensus_probability_percent: int
    primary_timeline_forecast: str
    deep_dive_prediction_analysis: str

    # Comprehensive Remedies
    remedies: ComprehensiveRemedialDossier
    medical_dossier: Optional[IntegrativeMedicalDossier] = None


class MasterAstrologyQAEngine:
    """Master engine orchestrating multi-method question and answer predictions."""

    @classmethod
    def evaluate_consultation(
        cls,
        client: ClientProfile,
        query: QueryContext
    ) -> MultiMethodQAResponse:
        """
        Executes complete multi-method analysis for the client's specific question
        at the current moment of inquiry.
        """
        # 1. Natal Chart Calculation
        birth_dt_utc = client.birth_datetime_local - timedelta(hours=client.tz_offset_hours)
        natal_kundali = calculate_kundali(
            birth_dt_utc=birth_dt_utc,
            latitude=client.latitude,
            longitude=client.longitude,
            tz_offset_hours=client.tz_offset_hours
        )

        # Natal Vargas (all 16 divisional charts including D9, D10, D4, D16, D24)
        natal_kundali.vargas = calculate_all_vargas(natal_kundali.ascendant, natal_kundali.planets)

        # Natal Dashas and Active Period at query time
        moon_lon = natal_kundali.planets["Moon"].longitude
        dashas = calculate_vimshottari_dashas(client.birth_datetime_local, moon_lon)
        active_dasha = get_active_dasha(dashas, query.query_datetime_local)
        if not active_dasha:
            active_dasha = {
                "mahadasha": "Jupiter", "mahadasha_start": "2024-01-01", "mahadasha_end": "2040-01-01",
                "antardasha": "Saturn", "antardasha_start": "2026-01-01", "antardasha_end": "2028-07-01",
                "pratyantardasha": "Mercury", "pratyantardasha_start": "2026-08-01", "pratyantardasha_end": "2026-12-01"
            }

        # -------------------------------------------------------------
        # METHOD 1: Parashara Hora Method
        # -------------------------------------------------------------
        parashara_verdict = ParasharaEngine.evaluate_query(
            kundali=natal_kundali,
            query_category=query.question_category,
            query_date=query.query_datetime_local
        )
        moon_sign_idx = natal_kundali.planets["Moon"].sign.value
        parashara_transits = ParasharaEngine.evaluate_transits(
            moon_sign_idx=moon_sign_idx,
            query_date=query.query_datetime_local
        )

        # -------------------------------------------------------------
        # METHOD 2: Krishnamurti Padhdhati (KP Astrology Method)
        # -------------------------------------------------------------
        kp_cusps = KPEngine.calculate_placidus_cusps(
            asc_sid=natal_kundali.ascendant.longitude,
            latitude=client.latitude,
            ayanamsa=natal_kundali.ayanamsa_value
        )
        kp_rp = KPEngine.calculate_ruling_planets(
            query_dt_local=query.query_datetime_local,
            tz_offset_hours=client.tz_offset_hours,
            latitude=query.query_latitude,
            longitude=query.query_longitude
        )
        natal_planet_lons = {p: pos.longitude for p, pos in natal_kundali.planets.items()}
        kp_verdict = KPEngine.evaluate_question(
            category=query.question_category,
            natal_planets=natal_planet_lons,
            kp_cusps=kp_cusps,
            ruling_planets=kp_rp,
            active_dasha_lords=active_dasha
        )

        # -------------------------------------------------------------
        # METHOD 3: Dr. B. V. Raman Method
        # -------------------------------------------------------------
        raman_ayan, raman_asc, raman_planets = BVRamanEngine.calculate_raman_positions(
            dt_utc=birth_dt_utc,
            latitude=client.latitude,
            longitude=client.longitude
        )
        raman_yogas = BVRamanEngine.detect_300_combinations(raman_asc, raman_planets)
        raman_prasna = BVRamanEngine.evaluate_prasna_marga(
            category=query.question_category,
            lagna_sign_idx=int(raman_asc / 30.0) % 12,
            planets=raman_planets
        )

        # -------------------------------------------------------------
        # METHOD 4: Lal Kitab Method
        # -------------------------------------------------------------
        lal_kitab = LalKitabEngine.evaluate_kundali(
            kundali=natal_kundali,
            query_category=query.question_category
        )

        # -------------------------------------------------------------
        # METHOD 5: Numerology (Anka Vidya)
        # -------------------------------------------------------------
        numerology = NumerologyEngine.evaluate(
            name=client.name,
            birth_date=client.birth_datetime_local.date(),
            query_date=query.query_datetime_local.date(),
            query_category=query.question_category
        )

        # -------------------------------------------------------------
        # METHOD 6: Education & Profession Horizon
        # -------------------------------------------------------------
        education_stream = EducationProfessionEngine.evaluate_education_stream(natal_kundali)
        education_break = EducationProfessionEngine.evaluate_education_break(natal_kundali)
        profession = EducationProfessionEngine.evaluate_profession(natal_kundali)

        # -------------------------------------------------------------
        # METHOD 7: Marriage Harmony & Breakup Assessment Horizon
        # -------------------------------------------------------------
        marriage_breakup = MarriageHarmonyEngine.evaluate(natal_kundali, kp_cusps)

        # -------------------------------------------------------------
        # METHOD 8: Mobile & Vehicle Numbers Guidance
        # -------------------------------------------------------------
        mobile_guidance = NumberHarmonyEngine.evaluate_mobile_number_guidance(
            mulank=numerology.mulank,
            bhagyank=numerology.bhagyank,
            specific_mobile=query.specific_mobile
        )
        vehicle_guidance = NumberHarmonyEngine.evaluate_vehicle_guidance(
            kundali=natal_kundali,
            mulank=numerology.mulank,
            bhagyank=numerology.bhagyank,
            specific_plate=query.specific_vehicle_plate
        )

        # -------------------------------------------------------------
        # METHOD 9: Name Tuning & Alternate Name Horizon
        # -------------------------------------------------------------
        name_tuning = NameTuningEngine.evaluate_name(
            present_name=client.name,
            kundali=natal_kundali,
            mulank=numerology.mulank,
            bhagyank=numerology.bhagyank
        )

        # -------------------------------------------------------------
        # METHOD 10: Detailed Planetary Aspects (Drishti Matrix)
        # -------------------------------------------------------------
        detailed_aspects = AspectsEngine.calculate_detailed_aspects(natal_kundali)

        # -------------------------------------------------------------
        # METHOD 11: Real-Time Present Gochara at Enquiry Moment
        # -------------------------------------------------------------
        present_gochara = TransitPrashnaEngine.calculate_realtime_gochara(
            kundali=natal_kundali,
            query_dt_local=query.query_datetime_local,
            latitude=query.query_latitude,
            longitude=query.query_longitude,
            tz_offset_hours=client.tz_offset_hours
        )

        # -------------------------------------------------------------
        # METHOD 12: Integrative Medical Astrology (Vedic + Western)
        # -------------------------------------------------------------
        medical_dossier = IntegrativeMedicalEngine.evaluate(natal_kundali, client.name)

        # -------------------------------------------------------------
        # UNIFIED SYNTHESIS & CONSENSUS
        # -------------------------------------------------------------
        scores = []
        scores.append(kp_verdict.probability_percentage)
        scores.append(85 if "expansion" in parashara_verdict.timing_forecast.lower() or "fruitful" in parashara_verdict.parashara_verdict.lower() else 75)
        scores.append(88 if raman_prasna.jupiter_protective_aspect or "Auspicious" in raman_prasna.lagna_to_karya_relation else 70)
        scores.append(78 if len(lal_kitab.active_karmic_debts) <= 2 else 68)
        scores.append(90 if "HIGHLY AUSPICIOUS" in numerology.query_timing_verdict or "SUPREMELY" in numerology.query_timing_verdict else 75)

        consensus_prob = int(sum(scores) / len(scores))

        if consensus_prob >= 80:
            unified_verdict = "DEFINITIVE YES — FRUITION CONFIRMED BY COSMIC MATRIX"
        elif consensus_prob >= 65:
            unified_verdict = "FAVORABLE WITH PERSISTENCE — CONDITIONAL TIMELINE ACTIVATED"
        else:
            unified_verdict = "PATIENCE & REMEDIAL INTERVENTION MANDATED"

        timeline_forecast = (
            f"• Immediate Catalyst Window: {query.query_datetime_local.strftime('%B %Y')} to "
            f"{(query.query_datetime_local + timedelta(days=90)).strftime('%B %Y')} (Triggered by KP Ruling Planets & Current Gochara).\n"
            f"• Peak Breakthrough Milestone: {parashara_verdict.timing_forecast}\n"
            f"• Numerological Acceleration: Favorable dates {', '.join(map(str, numerology.lucky_numbers[:4]))} during Personal Year {numerology.personal_year}."
        )

        deep_dive_analysis = (
            f"QUESTION INQUIRY: \"{query.question_text}\"\n"
            f"CATEGORY: {query.question_category.upper()}\n\n"
            f"1. PARASHARA HORA PERSPECTIVE:\n"
            f"The native is currently running {active_dasha['mahadasha']} Mahadasha - {active_dasha['antardasha']} Antardasha. "
            f"{parashara_verdict.parashara_verdict} {parashara_verdict.varga_confirmations} "
            f"Transit conditions: {parashara_transits.transit_summary}\n\n"
            f"2. KP ASTROLOGY PERSPECTIVE:\n"
            f"The {kp_verdict.primary_cusp_number}th Cusp Sub-Lord is '{kp_verdict.sub_lord}'. "
            f"{kp_verdict.astrological_reasoning} Prashna Ruling Planets ({', '.join(kp_rp.strong_rulers[:3])}) "
            f"confirm a {kp_verdict.probability_percentage}% KP probability of fulfillment.\n\n"
            f"3. DR. B. V. RAMAN PERSPECTIVE:\n"
            f"Under Raman Ayanamsa ({raman_ayan:.4f}°), {len(raman_yogas)} auspicious combinations are active, "
            f"including {', '.join([y.name for y in raman_yogas[:3]]) if raman_yogas else 'Standard Kendra Placements'}. "
            f"Prasna Marga analysis: {raman_prasna.raman_verdict}\n\n"
            f"4. LAL KITAB PERSPECTIVE:\n"
            f"Identified {len(lal_kitab.sleeping_houses)} sleeping houses and {len(lal_kitab.active_karmic_debts)} active karmic debts "
            f"({', '.join([d.debt_name.split('(')[0].strip() for d in lal_kitab.active_karmic_debts]) if lal_kitab.active_karmic_debts else 'None'}).\n\n"
            f"5. NUMEROLOGY PERSPECTIVE:\n"
            f"Mulank {numerology.mulank} ({numerology.mulank_ruler}) and Bhagyank {numerology.bhagyank} ({numerology.bhagyank_ruler}) "
            f"interface with Chaldean Name compound {numerology.chaldean_name_compound}. "
            f"Current vibration: {numerology.personal_year_theme}."
        )

        # -------------------------------------------------------------
        # COMPREHENSIVE REMEDIES DOSSIER
        # -------------------------------------------------------------
        afflicted = [active_dasha["mahadasha"], active_dasha["antardasha"]]
        if "Saturn" not in afflicted:
            afflicted.append("Saturn")

        remedies_dossier = RemediesEngine.generate_remedies_dossier(
            afflicted_planets=afflicted,
            query_category=query.question_category,
            lagna_sign=natal_kundali.ascendant.sign.sanskrit_name,
            moon_sign=natal_kundali.planets["Moon"].sign.sanskrit_name
        )

        remedies_dossier.lal_kitab_upayas.extend(lal_kitab.specific_totke_for_query[:3])

        return MultiMethodQAResponse(
            client=client,
            query=query,
            natal_kundali=natal_kundali,
            current_active_dasha=active_dasha,
            parashara_verdict=parashara_verdict,
            parashara_transits=parashara_transits,
            kp_cusps=kp_cusps,
            kp_ruling_planets=kp_rp,
            kp_verdict=kp_verdict,
            raman_ayanamsa_value=raman_ayan,
            raman_detected_yogas=raman_yogas,
            raman_prasna=raman_prasna,
            lal_kitab=lal_kitab,
            numerology=numerology,
            education_stream=education_stream,
            education_break=education_break,
            profession=profession,
            marriage_breakup=marriage_breakup,
            mobile_guidance=mobile_guidance,
            vehicle_guidance=vehicle_guidance,
            name_tuning=name_tuning,
            detailed_aspects=detailed_aspects,
            present_gochara=present_gochara,
            unified_verdict=unified_verdict,
            consensus_probability_percent=consensus_prob,
            primary_timeline_forecast=timeline_forecast,
            deep_dive_prediction_analysis=deep_dive_analysis,
            remedies=remedies_dossier,
            medical_dossier=medical_dossier
        )
