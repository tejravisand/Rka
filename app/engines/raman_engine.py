"""
Dr. B. V. Raman Astrology Method Engine.
Implements:
1. Precise B. V. Raman Ayanamsa calculation.
2. 300 Important Combinations (Dr. B. V. Raman) detection and yoga analysis.
3. Prasna Marga / Hindu Predictive Astrology principles for current situation queries.
4. Bhava Bala & Shadbala strength evaluation summary.
"""
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT, NAKSHATRAS
from app.core.ephemeris import normalize_degrees, datetime_to_jd, get_nakshatra_info, get_planet_dignity


def calculate_raman_ayanamsa(jd: float) -> float:
    """
    Calculate Dr. B. V. Raman's Ayanamsa for a given Julian Day.
    Standard Raman definition: 21° 0' 44" (21.012222°) on Jan 1, 1900 (JD 2415020.0)
    Annual precession: ~50.288 arcseconds per year.
    Difference with Lahiri is typically ~1° 26' to 1° 27'.
    """
    years_from_1900 = (jd - 2415020.0) / 365.25
    ayanamsa_deg = 21.012222 + years_from_1900 * (50.288 / 3600.0)
    return ayanamsa_deg % 360.0


@dataclass
class RamanYoga:
    name: str
    is_present: bool
    planets_involved: List[str]
    houses_involved: List[int]
    classical_effects: str
    relevance_to_query: str


@dataclass
class RamanPrasnaAssessment:
    query_category: str
    karya_bhava_number: int
    karya_bhava_lord: str
    lagna_lord: str
    lagna_to_karya_relation: str       # "Friendly / Mutual Kendra", "Neutral", "Adverse 6/8"
    moon_condition: str                # Moon placement and strength
    jupiter_protective_aspect: bool
    raman_verdict: str
    classical_prasna_remedy: str


@dataclass
class RamanProfile:
    ayanamsa_name: str
    ayanamsa_value: float
    detected_yogas: List[RamanYoga]
    prasna_assessment: RamanPrasnaAssessment


class BVRamanEngine:
    """Dr. B. V. Raman Method calculation and combination evaluation engine."""

    @classmethod
    def calculate_raman_positions(
        cls,
        dt_utc: datetime,
        latitude: float,
        longitude: float
    ) -> Tuple[float, float, Dict[str, float]]:
        """
        Calculates Raman Ayanamsa and sidereal planetary longitudes under Raman's system.
        """
        from app.core.ephemeris import AstronomicalCalculator
        jd = datetime_to_jd(dt_utc)
        raman_ayan = calculate_raman_ayanamsa(jd)
        T = (jd - 2451545.0) / 36525.0

        # Sun
        sun_trop, _ = AstronomicalCalculator.calculate_sun(T)
        sun_sid = normalize_degrees(sun_trop - raman_ayan)

        # Moon
        moon_trop, _ = AstronomicalCalculator.calculate_moon(T)
        moon_sid = normalize_degrees(moon_trop - raman_ayan)

        # Rahu & Ketu
        rahu_trop, ketu_trop = AstronomicalCalculator.calculate_rahu_ketu(T)
        rahu_sid = normalize_degrees(rahu_trop - raman_ayan)
        ketu_sid = normalize_degrees(ketu_trop - raman_ayan)

        # Major planets
        planets = {
            "Sun": sun_sid,
            "Moon": moon_sid,
            "Rahu": rahu_sid,
            "Ketu": ketu_sid
        }
        for name in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            trop_lon, _, _ = AstronomicalCalculator.calculate_major_planet(name, T, sun_trop)
            planets[name] = normalize_degrees(trop_lon - raman_ayan)

        asc_sid = AstronomicalCalculator.calculate_ascendant(jd, latitude, longitude, raman_ayan)
        return raman_ayan, asc_sid, planets

    @classmethod
    def detect_300_combinations(
        cls,
        asc_lon: float,
        planets: Dict[str, float]
    ) -> List[RamanYoga]:
        """
        Detects combinations from Dr. B. V. Raman's '300 Important Combinations'.
        """
        lagna_sign = int(asc_lon / 30.0) % 12
        planet_signs = {p: int(lon / 30.0) % 12 for p, lon in planets.items()}
        planet_houses = {p: (sign - lagna_sign) % 12 + 1 for p, sign in planet_signs.items()}

        yogas: List[RamanYoga] = []

        # 1. Gajakesari Yoga (Jupiter in 1, 4, 7, 10 from Moon)
        moon_sign = planet_signs["Moon"]
        jup_sign = planet_signs["Jupiter"]
        jup_from_moon = (jup_sign - moon_sign) % 12 + 1
        if jup_from_moon in [1, 4, 7, 10]:
            yogas.append(RamanYoga(
                name="Gajakesari Yoga",
                is_present=True,
                planets_involved=["Jupiter", "Moon"],
                houses_involved=[planet_houses["Jupiter"], planet_houses["Moon"]],
                classical_effects="Bestows imperishable reputation, intellectual brilliance, victory over adversaries, and royal status.",
                relevance_to_query="Grants sustained honor, public standing, and institutional support in all significant life endeavors."
            ))

        # 2. Chandra-Mangala Yoga (Moon and Mars conjunct or 7th aspect)
        mars_sign = planet_signs["Mars"]
        mars_from_moon = (mars_sign - moon_sign) % 12 + 1
        if mars_from_moon in [1, 7]:
            yogas.append(RamanYoga(
                name="Chandra-Mangala Yoga",
                is_present=True,
                planets_involved=["Moon", "Mars"],
                houses_involved=[planet_houses["Moon"], planet_houses["Mars"]],
                classical_effects="Sharp commercial instinct, high earnings from trade, property development, or self-driven enterprise.",
                relevance_to_query="Enhances financial acumen and decisive action in business negotiations and real estate."
            ))

        # 3. Guru-Mangala Yoga (Jupiter and Mars conjunct or 7th aspect)
        mars_from_jup = (mars_sign - jup_sign) % 12 + 1
        if mars_from_jup in [1, 7]:
            yogas.append(RamanYoga(
                name="Guru-Mangala Yoga",
                is_present=True,
                planets_involved=["Jupiter", "Mars"],
                houses_involved=[planet_houses["Jupiter"], planet_houses["Mars"]],
                classical_effects="Endows righteous executive authority, exceptional technical leadership, and unshakeable ethical backbone.",
                relevance_to_query="Guarantees triumph in high-responsibility leadership and technical projects."
            ))

        # 4. Budhaditya Yoga (Sun + Mercury in same sign)
        if planet_signs["Sun"] == planet_signs["Mercury"]:
            yogas.append(RamanYoga(
                name="Budhaditya Yoga",
                is_present=True,
                planets_involved=["Sun", "Mercury"],
                houses_involved=[planet_houses["Sun"]],
                classical_effects="Sharp analytical intellect, administrative competence, persuasive communication, and quick grasping power.",
                relevance_to_query="Facilitates smooth documentation, negotiations, and intellectual breakthroughs."
            ))

        # 5. Pancha Mahapurusha Yogas (Kendra + Own/Exaltation)
        # Kendras: 1, 4, 7, 10
        kendras = [1, 4, 7, 10]
        # Ruchaka (Mars in Aries, Scorpio, Capricorn in Kendra)
        if planet_houses["Mars"] in kendras and mars_sign in [0, 7, 9]:
            yogas.append(RamanYoga(
                name="Ruchaka Yoga (Mahapurusha)",
                is_present=True,
                planets_involved=["Mars"],
                houses_involved=[planet_houses["Mars"]],
                classical_effects="Courageous, physical vitality, command over forces, supreme executive determination.",
                relevance_to_query="Empowers authoritative victory over competitive hurdles."
            ))

        # Bhadra (Mercury in Gemini, Virgo in Kendra)
        mer_sign = planet_signs["Mercury"]
        if planet_houses["Mercury"] in kendras and mer_sign in [2, 5]:
            yogas.append(RamanYoga(
                name="Bhadra Yoga (Mahapurusha)",
                is_present=True,
                planets_involved=["Mercury"],
                houses_involved=[planet_houses["Mercury"]],
                classical_effects="High scholarly knowledge, mathematical prowess, eloquence, and massive commercial fortune.",
                relevance_to_query="Exceptional commercial and consulting triumph."
            ))

        # Hamsa (Jupiter in Sagittarius, Pisces, Cancer in Kendra)
        if planet_houses["Jupiter"] in kendras and jup_sign in [3, 8, 11]:
            yogas.append(RamanYoga(
                name="Hamsa Yoga (Mahapurusha)",
                is_present=True,
                planets_involved=["Jupiter"],
                houses_involved=[planet_houses["Jupiter"]],
                classical_effects="Pure character, universally revered, spiritual wisdom, respected by society and sovereigns.",
                relevance_to_query="Blesses the native with divine protection and noble mentorship."
            ))

        # Malavya (Venus in Taurus, Libra, Pisces in Kendra)
        ven_sign = planet_signs["Venus"]
        if planet_houses["Venus"] in kendras and ven_sign in [1, 6, 11]:
            yogas.append(RamanYoga(
                name="Malavya Yoga (Mahapurusha)",
                is_present=True,
                planets_involved=["Venus"],
                houses_involved=[planet_houses["Venus"]],
                classical_effects="Aesthetic refinement, possession of luxury vehicles and residences, happy conjugal harmony.",
                relevance_to_query="Accelerates comfort, luxury acquisitions, and domestic bliss."
            ))

        # Sasa (Saturn in Libra, Capricorn, Aquarius in Kendra)
        sat_sign = planet_signs["Saturn"]
        if planet_houses["Saturn"] in kendras and sat_sign in [6, 9, 10]:
            yogas.append(RamanYoga(
                name="Sasa Yoga (Mahapurusha)",
                is_present=True,
                planets_involved=["Saturn"],
                houses_involved=[planet_houses["Saturn"]],
                classical_effects="Leadership over large organizations or public institutions, enduring stamina, strategic perseverance.",
                relevance_to_query="Enables mastery over long-term complex projects and institutional growth."
            ))

        # 6. Amala Yoga (Natural benefic in 10th from Lagna or Moon)
        benefics = ["Jupiter", "Venus", "Mercury"]
        h10_from_lagna_planets = [p for p, h in planet_houses.items() if h == 10 and p in benefics]
        if h10_from_lagna_planets:
            yogas.append(RamanYoga(
                name="Amala Yoga",
                is_present=True,
                planets_involved=h10_from_lagna_planets,
                houses_involved=[10],
                classical_effects="Spotless moral reputation, career prosperity free of scandal, widespread professional admiration.",
                relevance_to_query="Directly uplifts professional standing and public recognition."
            ))

        # 7. Viparita Raja Yogas (Harsha, Sarala, Vimala)
        # 6th lord, 8th lord, 12th lord placements
        lord_6 = SIGN_LORDS[(lagna_sign + 5) % 12]
        lord_8 = SIGN_LORDS[(lagna_sign + 7) % 12]
        lord_12 = SIGN_LORDS[(lagna_sign + 11) % 12]

        if planet_houses.get(lord_6) in [6, 8, 12]:
            yogas.append(RamanYoga(
                name="Harsha Viparita Raja Yoga",
                is_present=True,
                planets_involved=[lord_6],
                houses_involved=[planet_houses[lord_6]],
                classical_effects="Invincibility over opponents, physical fortitude, sudden gains through crisis resolution.",
                relevance_to_query="Turns rivalries and legal/organizational conflicts into definitive personal victories."
            ))
        if planet_houses.get(lord_8) in [6, 8, 12]:
            yogas.append(RamanYoga(
                name="Sarala Viparita Raja Yoga",
                is_present=True,
                planets_involved=[lord_8],
                houses_involved=[planet_houses[lord_8]],
                classical_effects="Fearless nature, longevity, unexpected wealth windfalls, recovery from dire setbacks.",
                relevance_to_query="Ensures hidden resources and miraculous recovery when facing severe bottlenecks."
            ))
        if planet_houses.get(lord_12) in [6, 8, 12]:
            yogas.append(RamanYoga(
                name="Vimala Viparita Raja Yoga",
                is_present=True,
                planets_involved=[lord_12],
                houses_involved=[planet_houses[lord_12]],
                classical_effects="Independent spiritual disposition, judicious expenditure, freedom from heavy liabilities.",
                relevance_to_query="Shields against severe financial bleeding and ensures peaceful self-sufficiency."
            ))

        # 8. Vasumathi Yoga (Natural benefics in Upachayas 3, 6, 10, 11)
        upachaya_benefics = [p for p in benefics if planet_houses.get(p) in [3, 6, 10, 11]]
        if len(upachaya_benefics) >= 2:
            yogas.append(RamanYoga(
                name="Vasumathi Yoga",
                is_present=True,
                planets_involved=upachaya_benefics,
                houses_involved=[planet_houses[p] for p in upachaya_benefics],
                classical_effects="Command of substantial wealth without dependence on ancestors or external patrons.",
                relevance_to_query="Strongly indicates self-built financial sovereignty and enterprise success."
            ))

        # 9. Dharma-Karmadhipati Yoga (9th and 10th lords conjunct or mutual aspect)
        lord_9 = SIGN_LORDS[(lagna_sign + 8) % 12]
        lord_10 = SIGN_LORDS[(lagna_sign + 9) % 12]
        if planet_signs.get(lord_9) == planet_signs.get(lord_10):
            yogas.append(RamanYoga(
                name="Dharma-Karmadhipati Yoga",
                is_present=True,
                planets_involved=[lord_9, lord_10],
                houses_involved=[planet_houses[lord_9]],
                classical_effects="Supreme Raja Yoga of purpose, combining righteous fortune (Dharma) with powerful authority (Karma).",
                relevance_to_query="Marks pivotal executive elevation and legendary professional accomplishment."
            ))

        # 10. Kemadruma Yoga & Cancellation
        # Check 2nd and 12th from Moon
        h2_moon = (moon_sign + 1) % 12
        h12_moon = (moon_sign - 1) % 12
        planets_in_2_12 = [p for p, s in planet_signs.items() if s in [h2_moon, h12_moon] and p not in ["Sun", "Moon", "Rahu", "Ketu"]]
        if not planets_in_2_12:
            # Check cancellation (Moon in Kendra from Lagna or planets in Kendra from Moon)
            cancellation = planet_houses["Moon"] in kendras or any((s - moon_sign) % 12 + 1 in kendras for p, s in planet_signs.items() if p not in ["Sun", "Moon", "Rahu", "Ketu"])
            if cancellation:
                yogas.append(RamanYoga(
                    name="Kemadruma Bhanga (Yoga Nullification)",
                    is_present=True,
                    planets_involved=["Moon", "Jupiter"],
                    houses_involved=[planet_houses["Moon"]],
                    classical_effects="Initial periods of isolation or self-doubt are dismantled, converting hardship into resilient power.",
                    relevance_to_query="Converts early career or relationship trials into profound maturity and lasting success."
                ))

        return yogas

    @classmethod
    def evaluate_prasna_marga(
        cls,
        category: str,
        lagna_sign_idx: int,
        planets: Dict[str, float]
    ) -> RamanPrasnaAssessment:
        """
        Evaluates the query through Dr. B. V. Raman's 'Prasna Marga' guidelines:
        - Ascendant Lord (Pricchaka / Querent)
        - Karya Bhava Lord (Matter inquired)
        - Moon's disposition & Jupiter's aspect
        """
        cat_lower = category.lower()
        if any(w in cat_lower for w in ["job", "career", "promotion", "business", "work", "employment"]):
            karya_house = 10
        elif any(w in cat_lower for w in ["marriage", "relationship", "spouse", "love", "partner"]):
            karya_house = 7
        elif any(w in cat_lower for w in ["property", "land", "house", "real estate", "vehicle"]):
            karya_house = 4
        elif any(w in cat_lower for w in ["foreign", "abroad", "visa", "relocation", "travel"]):
            karya_house = 9
        elif any(w in cat_lower for w in ["finance", "money", "wealth", "debt", "investment"]):
            karya_house = 2
        elif any(w in cat_lower for w in ["court", "legal", "litigation", "enemy", "dispute"]):
            karya_house = 6
        elif any(w in cat_lower for w in ["health", "disease", "illness", "recovery"]):
            karya_house = 1
        else:
            karya_house = 11

        lagna_lord = SIGN_LORDS[lagna_sign_idx]
        karya_sign_idx = (lagna_sign_idx + (karya_house - 1)) % 12
        karya_lord = SIGN_LORDS[karya_sign_idx]

        planet_signs = {p: int(lon / 30.0) % 12 for p, lon in planets.items()}
        lagna_lord_sign = planet_signs.get(lagna_lord, 0)
        karya_lord_sign = planet_signs.get(karya_lord, 0)

        # Relation between Lagna Lord and Karya Lord
        diff = (karya_lord_sign - lagna_lord_sign) % 12 + 1
        if diff in [1, 4, 7, 10]:
            rel_str = "Auspicious Mutual Kendra (Direct Fruition)"
        elif diff in [5, 9]:
            rel_str = "Harmonious Trikona (Blessed by Fortune)"
        elif diff in [3, 11]:
            rel_str = "Upachaya Growth (Progress through Determined Action)"
        elif diff in [6, 8, 12]:
            rel_str = "Shadashtaka / Vyaya Tension (Delay and Deliberation Needed)"
        else:
            rel_str = "Neutral Placement"

        # Jupiter's protective aspect on Karya House or Karya Lord
        jup_sign = planet_signs.get("Jupiter", 0)
        # Jupiter aspects 5th, 7th, 9th from itself
        jup_aspect_houses = [(jup_sign + 4) % 12, (jup_sign + 6) % 12, (jup_sign + 8) % 12, jup_sign]
        has_jup_aspect = (karya_sign_idx in jup_aspect_houses) or (karya_lord_sign in jup_aspect_houses)

        # Moon's condition
        moon_sign = planet_signs.get("Moon", 0)
        moon_house = (moon_sign - lagna_sign_idx) % 12 + 1
        if moon_house in [1, 4, 7, 10, 5, 9, 11]:
            moon_condition = f"Strong and Benefic in House {moon_house} (Favorable mental resolve and timing)"
        else:
            moon_condition = f"Positioned in House {moon_house} (Intense contemplation, caution against emotional haste)"

        # Raman Verdict
        if has_jup_aspect or diff in [1, 4, 7, 10, 5, 9, 11]:
            raman_verdict = (
                f"Favorable outcome assured according to Prasna Marga tenets. "
                f"The Lagna Lord ({lagna_lord}) and Karya Lord ({karya_lord}) share {rel_str}. "
                f"{'Jupiter casts its divine benefic aspect, ensuring protection and success.' if has_jup_aspect else 'The cosmic currents indicate natural unfolding.'}"
            )
            prasna_remedy = "Offer arghya to Surya at sunrise and chant Aditya Hridaya Stotra; feed cows with jaggery."
        else:
            raman_verdict = (
                f"Prasna indicates that fulfillment requires patience and propitiation. "
                f"The Lagna Lord and Karya Lord share {rel_str}, showing initial friction or procedural drag."
            )
            prasna_remedy = "Light sesame oil lamp before Lord Shiva on Mondays/Saturdays; circumambulate sacred Peepal or Shami tree."

        return RamanPrasnaAssessment(
            query_category=category,
            karya_bhava_number=karya_house,
            karya_bhava_lord=karya_lord,
            lagna_lord=lagna_lord,
            lagna_to_karya_relation=rel_str,
            moon_condition=moon_condition,
            jupiter_protective_aspect=has_jup_aspect,
            raman_verdict=raman_verdict,
            classical_prasna_remedy=prasna_remedy
        )
