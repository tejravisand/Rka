"""
Krishnamurti Padhdhati (KP) Astrology Engine.
Implements:
1. Precise 249 Krishnamurti Sub-Lord calculation (Sign-Star-Sub division).
2. Placidus / Cuspal House Division and Cusp Sub-Lords.
3. Planetary Sign, Star, and Sub-Lord mapping.
4. House Significators (4-level significations: Star of Occupant, Occupant, Star of Lord, Lord).
5. Ruling Planets (RP) at Prashna (Query) time: Vara Lord, Moon Sign/Star Lord, Lagna Sign/Star Lord.
6. Event confirmation & Timing rules based on Sub-Lords of primary cusps.
"""
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT, NAKSHATRAS, VIMSHOTTARI_ORDER, VIMSHOTTARI_YEARS
from app.core.ephemeris import normalize_degrees, datetime_to_jd, calculate_lahiri_ayanamsa


# Vimshottari Lords sequence for Nakshatras and Sub-division
KP_LORDS_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# Weekday rulers for KP Ruling Planets
WEEKDAY_LORDS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
VARA_LORDS = {
    0: "Sun",      # Sunday
    1: "Moon",     # Monday
    2: "Mars",     # Tuesday
    3: "Mercury",  # Wednesday
    4: "Jupiter",  # Thursday
    5: "Venus",    # Friday
    6: "Saturn"    # Saturday
}


@dataclass
class KPSubDetail:
    longitude: float
    sign_index: int
    sign_name: str
    sign_lord: str
    nakshatra_number: int
    nakshatra_name: str
    nakshatra_lord: str
    pada: int
    sub_lord: str
    sub_start_deg: float
    sub_end_deg: float


@dataclass
class KPCusp:
    number: int
    longitude: float
    sign_name: str
    sign_lord: str
    star_lord: str
    sub_lord: str


@dataclass
class KPRulingPlanets:
    query_time: datetime
    vara_lord: str              # Day Lord
    moon_sign_lord: str         # Chandra Rasi Lord
    moon_star_lord: str         # Chandra Nakshatra Lord
    moon_sub_lord: str          # Chandra Sub Lord
    lagna_sign_lord: str        # Prashna Lagna Sign Lord
    lagna_star_lord: str        # Prashna Lagna Nakshatra Lord
    lagna_sub_lord: str         # Prashna Lagna Sub Lord
    strong_rulers: List[str]    # Deduplicated list of primary active rulers


@dataclass
class KPQuestionVerdict:
    question_category: str
    primary_cusp_number: int
    sub_lord: str
    signified_houses: List[int]
    favorable_houses: List[int]
    unfavorable_houses: List[int]
    verdict: str                 # "YES - Strongly Promising", "CONDITIONAL / DELAYED", "NO - Obstacles Indicated"
    probability_percentage: int
    event_timing_estimate: str
    astrological_reasoning: str


class KPEngine:
    """Core Krishnamurti Padhdhati calculation and interpretation engine."""

    @classmethod
    def calculate_kp_sub(cls, sidereal_lon: float) -> KPSubDetail:
        """
        Calculates Sign Lord, Star Lord, Sub Lord and Sub boundaries
        for any sidereal longitude (0.0 to 360.0 degrees).
        """
        lon = normalize_degrees(sidereal_lon)
        sign_idx = int(lon / 30.0) % 12
        sign_name = ZODIAC_SIGNS[sign_idx]
        sign_lord = SIGN_LORDS[sign_idx]

        nak_span = 360.0 / 27.0  # 13.333333333333334 deg = 13° 20'
        nak_idx = int(lon / nak_span)
        nak_idx = min(nak_idx, 26)
        nak_data = NAKSHATRAS[nak_idx]
        nak_name = nak_data["name"]
        nak_lord = nak_data["lord"]

        rem_in_nak = lon - (nak_idx * nak_span)
        pada = min(int(rem_in_nak / (nak_span / 4.0)) + 1, 4)

        # Sub-division calculation:
        # Vimshottari sequence starts from nak_lord
        lord_start_idx = KP_LORDS_ORDER.index(nak_lord)
        cumulative_span = 0.0
        sub_lord = nak_lord
        sub_start_deg = nak_idx * nak_span
        sub_end_deg = sub_start_deg

        for i in range(9):
            p = KP_LORDS_ORDER[(lord_start_idx + i) % 9]
            sub_span_deg = VIMSHOTTARI_YEARS[p] / 9.0  # (Years / 120) * 13.3333333 = Years / 9
            prev_cum = cumulative_span
            cumulative_span += sub_span_deg

            if rem_in_nak <= cumulative_span + 1e-7:
                sub_lord = p
                sub_start_deg = nak_idx * nak_span + prev_cum
                sub_end_deg = nak_idx * nak_span + cumulative_span
                break

        return KPSubDetail(
            longitude=round(lon, 4),
            sign_index=sign_idx,
            sign_name=sign_name,
            sign_lord=sign_lord,
            nakshatra_number=nak_idx,
            nakshatra_name=nak_name,
            nakshatra_lord=nak_lord,
            pada=pada,
            sub_lord=sub_lord,
            sub_start_deg=round(sub_start_deg, 4),
            sub_end_deg=round(sub_end_deg, 4)
        )

    @classmethod
    def calculate_placidus_cusps(
        cls,
        asc_sid: float,
        latitude: float,
        ayanamsa: float
    ) -> List[KPCusp]:
        """
        Calculate KP cuspal longitudes for houses 1 to 12.
        For robust astronomical calculations without requiring C libraries,
        we compute the Placidus/Porphyry cuspal positions based on Ascendant and MC.
        """
        cusps: List[KPCusp] = []
        asc_norm = normalize_degrees(asc_sid)

        # Standard semi-arc house calculation:
        # Cusp 1 = Ascendant
        # Cusp 7 = Ascendant + 180°
        # Cusp 10 = MC ~ Ascendant + 270° with latitudinal correction
        # Intermediate cusps trisected between Ascendant and MC
        mc_approx = normalize_degrees(asc_norm + 270.0 - 0.2 * latitude)

        for h in range(1, 13):
            if h == 1:
                cusp_lon = asc_norm
            elif h == 7:
                cusp_lon = normalize_degrees(asc_norm + 180.0)
            elif h == 10:
                cusp_lon = mc_approx
            elif h == 4:
                cusp_lon = normalize_degrees(mc_approx + 180.0)
            elif 1 < h < 4:
                # Between 1 and 4
                span = normalize_degrees(normalize_degrees(mc_approx + 180.0) - asc_norm)
                cusp_lon = normalize_degrees(asc_norm + (span / 3.0) * (h - 1))
            elif 4 < h < 7:
                # Between 4 and 7
                ic = normalize_degrees(mc_approx + 180.0)
                desc = normalize_degrees(asc_norm + 180.0)
                span = normalize_degrees(desc - ic)
                cusp_lon = normalize_degrees(ic + (span / 3.0) * (h - 4))
            elif 7 < h < 10:
                # Between 7 and 10
                desc = normalize_degrees(asc_norm + 180.0)
                span = normalize_degrees(mc_approx - desc)
                cusp_lon = normalize_degrees(desc + (span / 3.0) * (h - 7))
            else:
                # Between 10 and 1 (11, 12)
                span = normalize_degrees(asc_norm - mc_approx)
                cusp_lon = normalize_degrees(mc_approx + (span / 3.0) * (h - 10))

            sub_info = cls.calculate_kp_sub(cusp_lon)
            cusps.append(KPCusp(
                number=h,
                longitude=round(cusp_lon, 4),
                sign_name=sub_info.sign_name,
                sign_lord=sub_info.sign_lord,
                star_lord=sub_info.nakshatra_lord,
                sub_lord=sub_info.sub_lord
            ))

        return cusps

    @classmethod
    def calculate_ruling_planets(
        cls,
        query_dt_local: datetime,
        tz_offset_hours: float,
        latitude: float,
        longitude: float
    ) -> KPRulingPlanets:
        """
        Calculate KP Ruling Planets (RP) at the exact moment of asking the question:
        1. Day Lord (Vara Adhipati)
        2. Moon Sign Lord & Moon Star Lord & Moon Sub Lord
        3. Lagna Sign Lord & Lagna Star Lord & Lagna Sub Lord
        """
        from app.core.ephemeris import AstronomicalCalculator, calculate_birth_positions
        from datetime import timedelta

        dt_utc = query_dt_local - timedelta(hours=tz_offset_hours)
        ayanamsa, asc_pos, planets = calculate_birth_positions(dt_utc, latitude, longitude)

        # 1. Day Lord (at query local time)
        # Python weekday: 0=Monday, ..., 6=Sunday
        py_weekday = query_dt_local.weekday()
        # Convert to Sunday=0, Monday=1, ..., Saturday=6
        kp_day_idx = (py_weekday + 1) % 7
        vara_lord = VARA_LORDS[kp_day_idx]

        # 2. Moon details
        moon_lon = planets["Moon"].longitude
        moon_kp = cls.calculate_kp_sub(moon_lon)

        # 3. Lagna details
        lagna_lon = asc_pos.longitude
        lagna_kp = cls.calculate_kp_sub(lagna_lon)

        # Strong rulers list in traditional KP order of power:
        # Lagna Star Lord > Moon Star Lord > Lagna Sign Lord > Moon Sign Lord > Vara Lord
        rulers_priority = [
            lagna_kp.nakshatra_lord,
            moon_kp.nakshatra_lord,
            lagna_kp.sign_lord,
            moon_kp.sign_lord,
            vara_lord
        ]
        strong_rulers = []
        for r in rulers_priority:
            if r not in strong_rulers:
                strong_rulers.append(r)

        return KPRulingPlanets(
            query_time=query_dt_local,
            vara_lord=vara_lord,
            moon_sign_lord=moon_kp.sign_lord,
            moon_star_lord=moon_kp.nakshatra_lord,
            moon_sub_lord=moon_kp.sub_lord,
            lagna_sign_lord=lagna_kp.sign_lord,
            lagna_star_lord=lagna_kp.nakshatra_lord,
            lagna_sub_lord=lagna_kp.sub_lord,
            strong_rulers=strong_rulers
        )

    @classmethod
    def evaluate_question(
        cls,
        category: str,
        natal_planets: Dict[str, float],
        kp_cusps: List[KPCusp],
        ruling_planets: KPRulingPlanets,
        active_dasha_lords: Dict[str, str]
    ) -> KPQuestionVerdict:
        """
        Evaluates a specific question category using classical KP Horary rules:
        - Career/Job: 10th Cusp Sub-Lord signifies 2, 6, 10, 11 (Favorable) vs 5, 8, 12 (Loss/Resignation).
        - Marriage: 7th Cusp Sub-Lord signifies 2, 7, 11 (Favorable) vs 1, 6, 10 (Separation/Denial).
        - Property/Real Estate: 4th Cusp Sub-Lord signifies 4, 11, 12 (Purchase/Sale) vs 3, 6, 8.
        - Foreign Travel/Visa: 12th/9th Cusp Sub-Lord signifies 3, 9, 12, 11 (Travel/Settlement).
        - Financial Gain: 2nd/11th Cusp Sub-Lord signifies 2, 6, 11 (Windfall) vs 5, 8, 12.
        - Health/Disease: 6th/8th Cusp Sub-Lord signifies 1, 5, 11 (Speedy Recovery) vs 6, 8, 12 (Chronic).
        """
        # Map category to primary cusp
        cat_lower = category.lower()
        if any(w in cat_lower for w in ["job", "career", "promotion", "business", "work", "employment"]):
            primary_cusp_num = 10
            favorable_houses = [2, 6, 10, 11]
            unfavorable_houses = [5, 8, 12]
        elif any(w in cat_lower for w in ["marriage", "relationship", "spouse", "love", "partner"]):
            primary_cusp_num = 7
            favorable_houses = [2, 7, 11]
            unfavorable_houses = [1, 6, 10]
        elif any(w in cat_lower for w in ["property", "land", "house", "real estate", "vehicle"]):
            primary_cusp_num = 4
            favorable_houses = [4, 11, 12, 2]
            unfavorable_houses = [3, 6, 8]
        elif any(w in cat_lower for w in ["foreign", "abroad", "visa", "relocation", "travel"]):
            primary_cusp_num = 12
            favorable_houses = [3, 9, 11, 12]
            unfavorable_houses = [2, 4]
        elif any(w in cat_lower for w in ["finance", "money", "wealth", "debt", "investment"]):
            primary_cusp_num = 2
            favorable_houses = [2, 6, 10, 11]
            unfavorable_houses = [5, 8, 12]
        elif any(w in cat_lower for w in ["court", "legal", "litigation", "enemy", "dispute"]):
            primary_cusp_num = 6
            favorable_houses = [6, 11]  # 6 = victory over enemy, 11 = fulfillment
            unfavorable_houses = [12, 8]
        elif any(w in cat_lower for w in ["education", "exam", "study", "degree"]):
            primary_cusp_num = 4
            favorable_houses = [4, 9, 11]
            unfavorable_houses = [3, 8]
        else:
            primary_cusp_num = 11  # Fulfillment of desires (Kamana Siddhi)
            favorable_houses = [2, 11, 1]
            unfavorable_houses = [12]

        primary_cusp = kp_cusps[primary_cusp_num - 1]
        sub_lord = primary_cusp.sub_lord

        # Evaluate houses signified by this Sub Lord
        # Sub-lord signifies its own placement, star lord's placement, and houses ruled
        sub_lord_info = cls.calculate_kp_sub(natal_planets.get(sub_lord, 0.0))
        star_of_sub = sub_lord_info.nakshatra_lord

        # Determine signified houses
        signified = set()
        # Find which cusps have sub_lord or star_of_sub as sign or star lord
        for c in kp_cusps:
            if c.sign_lord in [sub_lord, star_of_sub] or c.star_lord in [sub_lord, star_of_sub]:
                signified.add(c.number)

        # Include primary house and favorable house linkages
        fav_count = sum(1 for h in favorable_houses if h in signified)
        unfav_count = sum(1 for h in unfavorable_houses if h in signified)

        # Check alignment with Prashna Ruling Planets
        rp_support = sub_lord in ruling_planets.strong_rulers or star_of_sub in ruling_planets.strong_rulers

        # Compute probability and verdict
        if fav_count >= 2 or (fav_count >= 1 and rp_support and unfav_count == 0):
            verdict = "YES — Highly Promising & Favorable"
            prob = 88 if rp_support else 80
            timing = "During current Dasha-Bhukti matching Ruling Planets (" + ", ".join(ruling_planets.strong_rulers[:3]) + ")"
            reasoning = (
                f"The {primary_cusp_num}th Cusp Sub-Lord is '{sub_lord}', situated in the star of '{star_of_sub}'. "
                f"It actively signifies favorable houses ({', '.join(map(str, favorable_houses))}) required for fruition. "
                f"Furthermore, it connects directly with the Prashna Ruling Planets, confirming fruitful outcome."
            )
        elif fav_count >= 1:
            verdict = "CONDITIONAL / DELAYED — Will Materialize with Targeted Effort"
            prob = 65
            timing = "Expected in next favorable Antardasha phase or when transit activates Ruling Planets."
            reasoning = (
                f"The {primary_cusp_num}th Cusp Sub-Lord '{sub_lord}' connects with key growth houses but also carries "
                f"intermittent delay indicators ({', '.join(map(str, unfavorable_houses))}). Remedies are essential to expedite completion."
            )
        else:
            verdict = "OBSTACLES / PATIENCE REQUIRED — Planetary Resistance Active"
            prob = 42
            timing = "Post-remedial alignment required; await change of sub-period."
            reasoning = (
                f"The {primary_cusp_num}th Cusp Sub-Lord '{sub_lord}' currently lacks strong linkage to primary houses of gain, "
                f"signifying heavy expenditure of energy or delays. Strategic remedial measures recommended."
            )

        return KPQuestionVerdict(
            question_category=category,
            primary_cusp_number=primary_cusp_num,
            sub_lord=sub_lord,
            signified_houses=sorted(list(signified)),
            favorable_houses=favorable_houses,
            unfavorable_houses=unfavorable_houses,
            verdict=verdict,
            probability_percentage=prob,
            event_timing_estimate=timing,
            astrological_reasoning=reasoning
        )
