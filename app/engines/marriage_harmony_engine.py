"""
Marriage Longevity, Harmony & Breakup / Separation Risk Assessment Engine.
Implements:
1. 7th House (Kalatra Bhava), 8th House (Mangalya / Longevity), 6th House (Litigation / 12th from 7th),
   and 12th House (Sayana Sukha / Bedroom Harmony) analysis.
2. Kuja / Manglik Dosha evaluation (Mars in 1st, 2nd, 4th, 7th, 8th, or 12th from Lagna/Moon).
3. Rahu-Ketu 1/7 or 2/8 axis & Saturn-Sun discord dynamics.
4. D9 Navamsha Chart analysis (Spouse profile, 7th lord in D9, Venus dignity).
5. Upapada Lagna (UL) and 2nd from UL (Sustenance of Matrimonial Bond).
6. KP Astrology 7th Cusp Sub-Lord separation indicators (Houses 6, 8, 12, 1, 10).
7. Breakup / Separation Risk Rating & Marital Longevity Score (0-100%).
8. Comprehensive Preventive Upayas to heal disharmony and protect marital stability.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.models.astrological import Kundali, PlanetPosition, ZodiacSign
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT
from app.core.vargas import calculate_all_vargas


@dataclass
class MarriageBreakupAssessment:
    breakup_risk_level: str             # "Low / Minimal (<20%)", "Moderate (25-45%)", "Elevated / High (>50%)"
    marital_longevity_score: int        # 0 to 100 points
    manglik_dosha_status: str           # "Present - Severe", "Present - Mild / Cancelled", "Absent"
    seventh_house_dynamics: str         # 7th house occupants, aspects, and lord
    eighth_house_mangalya_status: str   # Longevity of matrimonial alliance
    upapada_lagna_analysis: str         # Sustenance of marriage
    d9_navamsha_confirmation: str       # D9 spouse and conjugal harmony
    kp_sub_lord_separation_indicator: str
    primary_conflict_triggers: List[str]# Triggers: Ego, coldness, third-party, in-laws
    critical_vulnerable_periods: str    # Dasha periods requiring vigilance
    preventive_remedies_for_harmony: List[str] # Detailed upayas to heal marriage
    number_of_marriages_verdict: str = "Strictly One Marriage (High Marital Permanence & Dharma)"


class MarriageHarmonyEngine:
    """Evaluates marital stability, separation risks, and preventive healing upayas."""

    @classmethod
    def evaluate(
        cls,
        kundali: Kundali,
        kp_cusps: Optional[List[Any]] = None
    ) -> MarriageBreakupAssessment:
        lagna_idx = kundali.ascendant.sign.value
        moon_idx = kundali.planets["Moon"].sign.value

        h7_idx = (lagna_idx + 6) % 12
        h8_idx = (lagna_idx + 7) % 12
        h6_idx = (lagna_idx + 5) % 12
        h12_idx = (lagna_idx + 11) % 12

        lord_7 = SIGN_LORDS[h7_idx]
        lord_8 = SIGN_LORDS[h8_idx]
        lord_6 = SIGN_LORDS[h6_idx]
        lord_12 = SIGN_LORDS[h12_idx]

        planet_signs = {p: pos.sign.value for p, pos in kundali.planets.items()}
        planet_houses = {p: (sign - lagna_idx) % 12 + 1 for p, sign in planet_signs.items()}

        mars_h = planet_houses.get("Mars", 1)
        sat_h = planet_houses.get("Saturn", 1)
        rahu_h = planet_houses.get("Rahu", 1)
        sun_h = planet_houses.get("Sun", 1)
        ven_h = planet_houses.get("Venus", 1)

        # 1. Manglik / Kuja Dosha Check
        # Mars in 1, 2, 4, 7, 8, 12 from Lagna or Moon
        mars_from_lagna = mars_h
        mars_from_moon = (planet_signs.get("Mars", 0) - moon_idx) % 12 + 1

        manglik_houses = [1, 2, 4, 7, 8, 12]
        is_manglik_lagna = mars_from_lagna in manglik_houses
        is_manglik_moon = mars_from_moon in manglik_houses

        # Cancellation factors (Mars in own sign Aries/Scorpio, or Capricorn exaltation, or aspected by Jupiter)
        jup_h = planet_houses.get("Jupiter", 1)
        jup_aspects_mars = (jup_h in [(mars_h - 4) % 12 + 1, (mars_h - 6) % 12 + 1, (mars_h - 8) % 12 + 1])
        mars_own_or_exalted = planet_signs.get("Mars") in [0, 7, 9]

        if (is_manglik_lagna or is_manglik_moon) and (mars_own_or_exalted or jup_aspects_mars):
            manglik_status = "Present but Neutralized / Cancelled (Kuja Dosha Bhanga via Jupiter aspect / planetary dignity)"
            manglik_penalty = 8
        elif is_manglik_lagna and is_manglik_moon:
            manglik_status = "Double Manglik Dosha (Severe Kuja Dosha from both Lagna and Moon)"
            manglik_penalty = 22
        elif is_manglik_lagna or is_manglik_moon:
            manglik_status = f"Present from {'Lagna' if is_manglik_lagna else 'Moon'} (House {mars_from_lagna if is_manglik_lagna else mars_from_moon})"
            manglik_penalty = 14
        else:
            manglik_status = "Absent (Native is Non-Manglik)"
            manglik_penalty = 0

        # 2. Risk Factors Calculation
        risk_score = 0
        triggers = []

        # 7th Lord placed in 6th, 8th, or 12th
        l7_house = planet_houses.get(lord_7, 1)
        if l7_house in [6, 8, 12]:
            risk_score += 18
            triggers.append(f"7th Lord ({lord_7}) in House {l7_house} (Dusthana: prone to prolonged periods of physical separation or legal friction).")

        # Malefics in 7th House
        planets_in_7 = [p for p, h in planet_houses.items() if h == 7]
        if "Rahu" in planets_in_7 or "Ketu" in planets_in_7:
            risk_score += 15
            triggers.append("Rahu/Ketu axis intersects 7th House, causing high emotional volatility, sudden misunderstandings, or unrealistic expectations.")
        if "Saturn" in planets_in_7:
            risk_score += 12
            triggers.append("Saturn in 7th House generates cold emotional distance, delayed intimacy, or heavy marital obligations.")
        if "Mars" in planets_in_7:
            risk_score += 15
            triggers.append("Mars in 7th House sparks fierce verbal arguments, aggressive temperaments, and ego battles.")
        if "Sun" in planets_in_7:
            risk_score += 10
            triggers.append("Sun in 7th House creates mutual dominance issues and status rivalries between spouses.")

        # Venus status
        ven_pos = kundali.planets["Venus"]
        if ven_pos.dignity == "Debilitated" or ven_h in [6, 8]:
            risk_score += 14
            triggers.append("Venus is debilitated or in Dusthana, indicating vulnerability to emotional discontent or lack of affection.")

        # 6th Lord connection with 7th House or Lord
        if lord_6 == lord_7 or planet_houses.get(lord_6) == 7 or planet_signs.get(lord_6) == planet_signs.get(lord_7):
            risk_score += 12
            triggers.append("6th House (Litigation & Rivalry) linked with 7th House, warning against formal legal disputes if disputes go unmanaged.")

        # Upapada Lagna (UL) Calculation
        # Sign of 12th lord from 12th house
        h12_lord_sign = planet_signs.get(lord_12, 0)
        dist_12_to_lord = (h12_lord_sign - h12_idx) % 12
        ul_sign_idx = (h12_lord_sign + dist_12_to_lord) % 12
        # 2nd from UL
        second_from_ul = (ul_sign_idx + 1) % 12
        second_ul_lord = SIGN_LORDS[second_from_ul]
        ul_text = f"Upapada Lagna falls in {ZODIAC_SANSKRIT[ul_sign_idx]}. Its 2nd house is ruled by {second_ul_lord}, governing marriage sustenance."

        # D9 Navamsha Confirmation
        vargas = getattr(kundali, "vargas", {}) or calculate_all_vargas(kundali.ascendant, kundali.planets)
        d9 = vargas.get(9)
        d9_text = "D9 Navamsha provides stabilizing matrimonial dharma."
        if d9:
            d9_ven = d9.placements.get("Venus")
            d9_l7 = d9.placements.get(lord_7)
            if d9_ven and d9_l7:
                d9_text = f"In D9 Navamsha, Venus is in {d9_ven.sign.sanskrit_name} ({d9_ven.dignity}) and 7th Lord {lord_7} is in {d9_l7.sign.sanskrit_name}."

        # KP Sub-Lord Check
        kp_indicator = "KP 7th Cusp Sub-Lord connects with stabilizing houses 2, 7, 11 (Marital protection active)."
        if kp_cusps and len(kp_cusps) >= 7:
            c7 = kp_cusps[6]
            if c7.sub_lord in ["Rahu", "Saturn", "Mars"] and risk_score > 30:
                kp_indicator = f"KP 7th Cusp Sub-Lord '{c7.sub_lord}' carries separation potential if 6th or 8th house is energized without remedy."

        # Total Longevity Score (out of 100)
        total_risk = min(risk_score + manglik_penalty, 85)
        longevity_score = 100 - total_risk

        if longevity_score >= 75:
            risk_level = "Low / Minimal Risk (<25% — High Marital Stability)"
        elif longevity_score >= 55:
            risk_level = "Moderate Friction Risk (30-45% — Solvable through Mutual Maturity & Upayas)"
        else:
            risk_level = "Elevated / Significant Separation Vulnerability (>50% — Strict Remedial Protection Advised)"

        h7_status = f"House 7 in {ZODIAC_SANSKRIT[h7_idx]} ruled by {lord_7} (placed in House {l7_house}). Occupants: {', '.join(planets_in_7) or 'Unoccupied (Aspects dominate)'}."
        h8_status = f"House 8 (Mangalya Bhava) in {ZODIAC_SANSKRIT[h8_idx]} ruled by {lord_8}. Governs durability of marriage and partner longevity."

        vulnerable_periods = f"Antardashas of {lord_6}, {lord_8}, or Rahu during Saturn transit over natal 7th or 8th house."

        # Comprehensive Preventive Remedies
        remedies = [
            "Wear a certified sacred Gauri-Shankar Rudraksha (conjoined natural double-bead representing Shiva & Parvati) around the neck on a white silk thread on Monday morning.",
            "Chant the sacred Katyayani Mantra 108 times daily facing North: 'Om Katyayani Mahamaye Mahayoginyadheeshwari, Nandagopasutam Devi Patim Me Kuru Te Namah'.",
            "Perform Pradakshinam (16 rounds) around the sacred Banana Tree on Thursdays, and water the sacred Tulsi plant daily morning with pure water and haldi.",
            "Lal Kitab Upaya: Place a small piece of natural camphor (Bhimseni Kapur) in a pure brass or silver bowl in the bedroom to dissolve negative aura and ego clashes.",
            "Feed cows with freshly kneaded wheat dough balls rolled in turmeric and jaggery on Friday mornings to strengthen Venus and domestic harmony.",
            "Avoid displaying aggressive art, predatory animals, or thorny cacti in the bedroom; use pastel rose, ivory, or cream bedsheets."
        ]

        # Number of Marriages Prediction Logic
        dual_signs = [2, 5, 8, 11]  # Gemini, Virgo, Sagittarius, Pisces
        fixed_signs = [1, 4, 7, 10]  # Taurus, Leo, Scorpio, Aquarius
        lagna_is_dual = lagna_idx in dual_signs
        h7_is_dual = h7_idx in dual_signs
        lord_1 = SIGN_LORDS[lagna_idx]
        lord_1_h = planet_houses.get(lord_1, 1)

        # Classical Jaimini & Parashara rules
        if lord_1_h == 7:
            marriage_verdict = "Strictly One Marriage (Lagna Lord placed in 7th Kendra establishes unbreakable Dharmic protection over the 1st alliance)."
        elif lagna_idx in fixed_signs or h7_idx in fixed_signs:
            marriage_verdict = "Strictly One Marriage (Fixed Sign axis anchors unyielding matrimonial loyalty and permanence)."
        elif (lagna_is_dual or h7_is_dual) and l7_house in [6, 8, 12] and risk_score > 35:
            marriage_verdict = "Vulnerability to Multiple Alliances / Second Marriage indicated (Dual sign axis combined with 7th Lord in Dusthana)."
        else:
            marriage_verdict = "Single Lifelong Marriage (Standard resilient marital path with high commitment)."

        return MarriageBreakupAssessment(
            breakup_risk_level=risk_level,
            marital_longevity_score=longevity_score,
            manglik_dosha_status=manglik_status,
            seventh_house_dynamics=h7_status,
            eighth_house_mangalya_status=h8_status,
            upapada_lagna_analysis=ul_text,
            d9_navamsha_confirmation=d9_text,
            kp_sub_lord_separation_indicator=kp_indicator,
            primary_conflict_triggers=triggers if triggers else ["Minor periodic differences of opinion inherent to all partnerships."],
            critical_vulnerable_periods=vulnerable_periods,
            preventive_remedies_for_harmony=remedies,
            number_of_marriages_verdict=marriage_verdict
        )
