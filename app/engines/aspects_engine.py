"""
Detailed Shastric Planetary Aspects (Drishti) Engine.
Implements:
1. Full 100% Saptama (7th) Drishti for all 9 Navagrahas.
2. Special Parashari Drishtis:
   - Mars (Mangala): 4th (Chaturtha), 7th (Saptama), 8th (Ashtama) aspects.
   - Jupiter (Guru): 5th (Panchama), 7th (Saptama), 9th (Navama) divine Amrita aspects.
   - Saturn (Shani): 3rd (Tritiya), 7th (Saptama), 10th (Dashama) karmic aspects.
   - Rahu & Ketu: 5th (Panchama), 7th (Saptama), 9th (Navama) aspects.
3. Aspect impacts on critical pivot points:
   - Lagna (Ascendant - Body & Vitality)
   - Moon (Chandra - Mind & Emotional Peace)
   - Sun (Surya - Soul & Executive Authority)
   - 10th House (Karma - Career & Profession)
   - 7th House (Kalatra - Marriage & Partnerships)
   - 4th House (Sukha/Vidya/Vahana - Education & Conveyances)
   - 2nd & 11th Houses (Dhana & Labha - Wealth & Financial Gains).
4. Mutual Planetary Aspects (Samyoga & Drishti Sambandha).
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from app.models.astrological import Kundali
from app.core.constants import SIGN_LORDS, ZODIAC_SANSKRIT


@dataclass
class PlanetAspectDetail:
    aspecting_planet: str
    from_house: int
    aspected_house: int
    aspect_type: str                   # "7th Full", "Special 4th", "Special 8th", "Special 5th", "Special 9th", "Special 3rd", "Special 10th"
    benefic_or_malefic: str            # "Benefic Blessing", "Protective Amrita", "Karmic Discipline / Delay", "Aggressive / Fiery"
    life_influence_summary: str


@dataclass
class KeyPointAspectSummary:
    target_point: str                  # e.g., "Lagna (1st House)", "10th House (Career)", "Moon (Mind)"
    aspecting_planets: List[str]
    net_influence: str                 # "Highly Favorable / Protected", "Mixed Dynamic", "Challenging / Needs Upaya"
    detailed_interpretation: str


@dataclass
class DetailedAspectsDossier:
    all_aspects_list: List[PlanetAspectDetail]
    key_points_aspects: List[KeyPointAspectSummary]
    mutual_planetary_aspects: List[str]
    synthesis_summary: str


class AspectsEngine:
    """Calculates comprehensive Parashari Drishtis (aspects) across all houses and planets."""

    @classmethod
    def calculate_detailed_aspects(cls, kundali: Kundali) -> DetailedAspectsDossier:
        lagna_idx = kundali.ascendant.sign.value
        planet_signs = {p: pos.sign.value for p, pos in kundali.planets.items()}
        planet_houses = {p: (sign - lagna_idx) % 12 + 1 for p, sign in planet_signs.items()}

        all_aspects: List[PlanetAspectDetail] = []

        # Define aspect rules for each planet
        for p_name, from_h in planet_houses.items():
            aspect_offsets = []

            # Universal 7th aspect for all planets
            aspect_offsets.append((7, "7th Full Aspect"))

            # Special aspects
            if p_name == "Mars":
                aspect_offsets.append((4, "Special 4th Aspect (Chaturtha)"))
                aspect_offsets.append((8, "Special 8th Aspect (Ashtama)"))
            elif p_name == "Jupiter":
                aspect_offsets.append((5, "Special 5th Aspect (Panchama - Amrita)"))
                aspect_offsets.append((9, "Special 9th Aspect (Navama - Dharma)"))
            elif p_name == "Saturn":
                aspect_offsets.append((3, "Special 3rd Aspect (Tritiya)"))
                aspect_offsets.append((10, "Special 10th Aspect (Dashama - Karma)"))
            elif p_name in ["Rahu", "Ketu"]:
                aspect_offsets.append((5, "Special 5th Aspect"))
                aspect_offsets.append((9, "Special 9th Aspect"))

            for offset, a_type in aspect_offsets:
                to_h = (from_h + (offset - 1) - 1) % 12 + 1

                # Classify nature
                if p_name == "Jupiter":
                    nature = "Protective Amrita (Divine Grace & Expansion)"
                    inf = f"Jupiter casts divine grace on House {to_h}, expanding wisdom, neutralizing toxicity, and shielding against crises."
                elif p_name == "Venus":
                    nature = "Benefic Blessing (Harmony & Prosperity)"
                    inf = f"Venus infuses House {to_h} with aesthetic refinement, material comfort, and amicable relationships."
                elif p_name == "Mercury":
                    nature = "Intellectual & Commercial (Analytical Acumen)"
                    inf = f"Mercury stimulates analytical clarity, sharp communication, and trade enterprise in House {to_h}."
                elif p_name == "Moon":
                    nature = "Emotional Nourishment & Public Goodwill"
                    inf = f"Moon nurtures House {to_h} with emotional intuition, public popularity, and maternal warmth."
                elif p_name == "Sun":
                    nature = "Royal Radiance & Administrative Vitality"
                    inf = f"Sun illuminates House {to_h} with authority, executive prestige, but also potential ego flare-ups."
                elif p_name == "Saturn":
                    nature = "Karmic Discipline / Delay & Endurance"
                    inf = f"Saturn demands meticulous perseverance, structure, and patience in House {to_h}; delays instant gratification."
                elif p_name == "Mars":
                    nature = "Aggressive / Fiery Drive & Technical Energy"
                    inf = f"Mars injects high executive courage, technical dynamism, and quick reactions into House {to_h}; watch for impatience."
                elif p_name == "Rahu":
                    nature = "Unconventional Expansion & Foreign Aspiration"
                    inf = f"Rahu stimulates ambitious hunger, international curiosity, and sudden breakthrough opportunities in House {to_h}."
                else:  # Ketu
                    nature = "Spiritual Detachment & Analytical Insight"
                    inf = f"Ketu induces deep philosophical detachment and subtle intuitive expertise in House {to_h}."

                all_aspects.append(PlanetAspectDetail(
                    aspecting_planet=p_name,
                    from_house=from_h,
                    aspected_house=to_h,
                    aspect_type=a_type,
                    benefic_or_malefic=nature,
                    life_influence_summary=inf
                ))

        # -------------------------------------------------------------
        # Aspects on Key Pivot Points
        # -------------------------------------------------------------
        # Targets: Lagna (1), Moon House, Sun House, 10th House, 7th House, 4th House, 2nd & 11th Houses
        moon_h = planet_houses["Moon"]
        sun_h = planet_houses["Sun"]

        targets = [
            ("Lagna (1st House - Vitality & Personality)", 1),
            (f"Moon ({planet_houses['Moon']}th House - Mind & Emotions)", moon_h),
            (f"Sun ({planet_houses['Sun']}th House - Soul & Authority)", sun_h),
            ("10th House (Karma - Career & Executive Prestige)", 10),
            ("7th House (Kalatra - Marriage & Partnerships)", 7),
            ("4th House (Sukha - Education, Assets & Vehicles)", 4),
            ("11th House (Labha - Wealth Gains & Desires)", 11)
        ]

        key_summaries: List[KeyPointAspectSummary] = []

        for title, target_h in targets:
            asp_planets = [
                f"{a.aspecting_planet} ({a.aspect_type.split()[0]})"
                for a in all_aspects
                if a.aspected_house == target_h and a.aspecting_planet not in title
            ]
            # Deduplicate
            asp_planets = list(dict.fromkeys(asp_planets))

            # Interpret
            jup_asp = any("Jupiter" in p for p in asp_planets)
            sat_asp = any("Saturn" in p for p in asp_planets)
            mars_asp = any("Mars" in p for p in asp_planets)
            ven_asp = any("Venus" in p for p in asp_planets)

            if jup_asp and not (sat_asp and mars_asp):
                net = "Supremely Protected by Divine Guru Aspect"
                detail = f"Receives the sacred Amrita Drishti of Jupiter, ensuring that challenges are neutralized and converted into lasting wisdom."
            elif jup_asp and (sat_asp or mars_asp):
                net = "Mixed Dynamic — Growth through Rigorous Discipline"
                detail = f"Jupiter's divine protection counterbalances Saturn's or Mars's pressure, demanding steadfast effort before granting massive reward."
            elif sat_asp and mars_asp:
                net = "High Karmic Tension — Structured Remedies Advised"
                detail = f"Under joint influence of Saturn and Mars; requires patient forbearance, anger control, and regular Shanti upayas."
            elif sat_asp:
                net = "Disciplined & Measured Unfolding"
                detail = f"Saturn's karmic gaze promotes solid long-term stability but insists on patience and avoidance of shortcuts."
            elif ven_asp:
                net = "Harmonious & Graceful Auspices"
                detail = f"Venus radiates comfort, social elegance, and smooth interpersonal alignment."
            else:
                net = "Balanced Cosmic Configuration"
                detail = f"Operates with moderate planetary momentum aligned with ruling Dasha."

            key_summaries.append(KeyPointAspectSummary(
                target_point=title,
                aspecting_planets=asp_planets if asp_planets else ["None (Empty / Unaspected)"],
                net_influence=net,
                detailed_interpretation=detail
            ))

        # -------------------------------------------------------------
        # Mutual Planetary Aspects
        # -------------------------------------------------------------
        mutual_aspects: List[str] = []
        planets_list = list(planet_houses.keys())
        for i in range(len(planets_list)):
            for j in range(i + 1, len(planets_list)):
                p1, p2 = planets_list[i], planets_list[j]
                h1, h2 = planet_houses[p1], planet_houses[p2]
                diff = (h2 - h1) % 12
                # Mutual 7th aspect
                if diff == 6:
                    mutual_aspects.append(
                        f"• {p1} in House {h1} and {p2} in House {h2} form a direct 7th Mutual Aspect (Saptama Drishti Sambandha)."
                    )

        if not mutual_aspects:
            mutual_aspects.append("No direct 180° mutual 7th aspects active; planets operate via independent trine/quadrant aspects.")

        synthesis = (
            f"The native's chart demonstrates a highly interconnected aspect network. "
            f"Key focal point: {'Jupiter casts divine protection across critical houses' if any('Jupiter' in a.aspecting_planet for a in all_aspects if a.aspected_house in [1, 7, 10]) else 'Saturn and Mars provide the technical drive and organizational stamina'}."
        )

        return DetailedAspectsDossier(
            all_aspects_list=all_aspects,
            key_points_aspects=key_summaries,
            mutual_planetary_aspects=mutual_aspects,
            synthesis_summary=synthesis
        )
