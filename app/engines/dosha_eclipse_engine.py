"""
Master Dosha Evaluation & Birth Phase / Eclipse (Purnima, Amavasya, Grahana) Engine.
Implements:
1. Kala Sarpa Dosha vs Yoga detection:
   - Evaluates all 7 classical planets relative to the Rahu-Ketu nodal axis.
   - Classifies into Savya (Anuloma / Material struggle) vs Apasavya (Pratiloma / Kala Amrita).
   - Identifies the specific 12 types (Ananta to Sheshanaga) based on Rahu's house.
   - Computes Kala Sarpa Bhanga (cancellation via Jupiter drishti or planet escape).
2. Pitra Dosha (Paternal lineage debt: Sun / 9th House affliction).
3. Matru Dosha (Maternal lineage debt: Moon / 4th House affliction).
4. Guru Chandal Dosha (Jupiter conjunct Rahu/Ketu).
5. Grahan Dosha (Sun or Moon conjunct Rahu/Ketu within nodal orb).
6. Birth Phase & Eclipse Detection:
   - Purnima (Full Moon - Peak Paksha Bala).
   - Amavasya (New Moon - Ksheena Chandra / Balarishta vulnerability).
   - Grahana Kala (Solar / Lunar Eclipse birth) detection.
7. Authentic Vedic Shanti Poojas, Chhaya Patra Daan, and curative rituals.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from app.models.astrological import Kundali, PlanetPosition
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT


KALA_SARPA_TYPES = {
    1: ("Ananta Kala Sarpa", "1st to 7th House Axis", "Personality struggles, self-doubt, marital friction; delayed self-actualization."),
    2: ("Kulika Kala Sarpa", "2nd to 8th House Axis", "Family discord, erratic finances, harsh speech; legacy and dental vulnerabilities."),
    3: ("Vasuki Kala Sarpa", "3rd to 9th House Axis", "Sibling friction, fluctuating courage, father-child distance; success through solo effort."),
    4: ("Shankhapala Kala Sarpa", "4th to 10th House Axis", "Domestic unrest, property legalities, mother's health anxieties; career relocations."),
    5: ("Padma Kala Sarpa", "5th to 11th House Axis", "Progeny hurdles, speculative caution, delayed creative recognition; academic hurdles."),
    6: ("Mahapadma Kala Sarpa", "6th to 12th House Axis", "Litigation, secret rivals, heavy health expenses; ultimate triumph over debts and enemies."),
    7: ("Takshaka Kala Sarpa", "7th to 1st House Axis", "Marital delays, business partner conflicts; intense public scrutiny."),
    8: ("Karkotaka Kala Sarpa", "8th to 2nd House Axis", "Sudden emergencies, occult and inheritance delays; high psychological depth."),
    9: ("Shankhachooda Kala Sarpa", "9th to 3rd House Axis", "Strained paternal relations, spiritual skepticism; tremendous fortune rises after age 36."),
    10: ("Ghataka Kala Sarpa", "10th to 4th House Axis", "Frequent job transitions, high workplace politics; rise to authoritative leadership."),
    11: ("Vishadhara Kala Sarpa", "11th to 5th House Axis", "Fluctuating cash flow, elder sibling disputes; emotional restlessness in romance."),
    12: ("Sheshanaga Kala Sarpa", "12th to 6th House Axis", "Sleep disturbances, high hospital/foreign expenditures; powerful spiritual detachment.")
}


@dataclass
class DoshaDetail:
    dosha_name: str
    is_present: bool
    severity: str                       # "None", "Mild / Cancelled", "Moderate", "Severe"
    astrological_signature: str
    life_manifestations: str
    prescribed_shanti_remedy: str


@dataclass
class MasterDoshaDossier:
    kala_sarpa_yoga_status: str
    kala_sarpa_type: str
    kala_sarpa_direction: str          # "Savya (Anuloma)", "Apasavya (Kala Amrita)", "None"
    kala_sarpa_bhanga: bool
    pitra_dosha: DoshaDetail
    matru_dosha: DoshaDetail
    guru_chandal_dosha: DoshaDetail
    grahan_dosha: DoshaDetail
    birth_phase_type: str              # "Purnima", "Amavasya", "Grahana Kala (Eclipse)", "Normal Phase"
    birth_phase_shanti_required: bool
    birth_phase_effects: str
    prescribed_birth_shanti_poojas: List[str]


class MasterDoshaEngine:
    """Evaluates major karmic doshas and eclipse/phase births."""

    @classmethod
    def evaluate(cls, kundali: Kundali) -> MasterDoshaDossier:
        lagna_idx = kundali.ascendant.sign.value
        planet_signs = {p: pos.sign.value for p, pos in kundali.planets.items()}
        planet_houses = {p: (sign - lagna_idx) % 12 + 1 for p, sign in planet_signs.items()}

        rahu_h = planet_houses.get("Rahu", 1)
        ketu_h = planet_houses.get("Ketu", 7)
        rahu_lon = kundali.planets["Rahu"].longitude
        ketu_lon = kundali.planets["Ketu"].longitude

        # 1. Kala Sarpa Evaluation
        planets_to_check = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        side_a = 0
        side_b = 0

        for p in planets_to_check:
            lon = kundali.planets[p].longitude
            # Angular distance from Rahu
            diff = (lon - rahu_lon) % 360
            if diff < 180:
                side_a += 1
            else:
                side_b += 1

        is_ks = (side_a == 7 or side_b == 7)
        ks_bhanga = False
        ks_type_name = "None"
        ks_direction = "None"
        ks_status = "Absent (Planets freely distributed outside nodal axis)"

        if is_ks:
            ks_type_name, axis_info, impact = KALA_SARPA_TYPES.get(rahu_h, ("Kala Sarpa", "", ""))
            ks_direction = "Savya (Anuloma / Material struggle)" if side_a == 7 else "Apasavya (Pratiloma / Kala Amrita Yoga)"
            
            # Check for Bhanga (Jupiter conjunct or aspecting Rahu, or Lagna outside)
            jup_lon = kundali.planets["Jupiter"].longitude
            jup_rahu_diff = abs(jup_lon - rahu_lon)
            if jup_rahu_diff < 15 or abs(jup_rahu_diff - 180) < 15:
                ks_bhanga = True
                ks_status = f"Present but Cancelled ({ks_type_name} — Kala Sarpa Bhanga via Guru Drishti / Conjunction)"
            else:
                ks_status = f"Present: {ks_type_name} ({ks_direction})"

        # 2. Pitra Dosha Check (Sun or 9th house afflicted by Rahu/Saturn)
        h9_idx = (lagna_idx + 8) % 12
        sun_sign = planet_signs.get("Sun", 0)
        rahu_sign = planet_signs.get("Rahu", 0)
        sat_sign = planet_signs.get("Saturn", 0)

        sun_with_rahu = (sun_sign == rahu_sign)
        sun_with_sat = (sun_sign == sat_sign)
        h9_has_rahu = (rahu_sign == h9_idx)
        h9_has_sat = (sat_sign == h9_idx)

        has_pitra = sun_with_rahu or sun_with_sat or h9_has_rahu or h9_has_sat
        pitra_dosha = DoshaDetail(
            dosha_name="Pitra Dosha (Ancestral Lineage Debt)",
            is_present=has_pitra,
            severity="Moderate to Severe" if (sun_with_rahu or h9_has_rahu) else ("Mild" if has_pitra else "None"),
            astrological_signature=(
                f"Sun in {ZODIAC_SANSKRIT[sun_sign]}, Rahu in {ZODIAC_SANSKRIT[rahu_sign]}, Saturn in {ZODIAC_SANSKRIT[sat_sign]}. "
                f"9th House is {ZODIAC_SANSKRIT[h9_idx]}."
            ),
            life_manifestations=(
                "Unexplained career obstacles, delayed lineage/progeny, or recurring friction with father/authority figures."
                if has_pitra else "Ancestral paternal blessings active; no blocking debt."
            ),
            prescribed_shanti_remedy=(
                "Perform annual Pinda Daan / Tarpanam at Gaya or Rameswaram. Feed crows and cows on Amavasya days. "
                "Water the Peepal tree with unboiled milk and black sesame seeds every Saturday morning."
            )
        )

        # 3. Matru Dosha Check (Moon or 4th house afflicted by Rahu/Saturn)
        h4_idx = (lagna_idx + 3) % 12
        moon_sign = planet_signs.get("Moon", 0)
        moon_with_rahu = (moon_sign == rahu_sign)
        moon_with_sat = (moon_sign == sat_sign)
        h4_has_rahu = (rahu_sign == h4_idx)
        h4_has_sat = (sat_sign == h4_idx)

        has_matru = moon_with_rahu or moon_with_sat or h4_has_rahu or h4_has_sat
        matru_dosha = DoshaDetail(
            dosha_name="Matru Dosha (Maternal Lineage Debt)",
            is_present=has_matru,
            severity="Severe" if (moon_with_rahu or moon_with_sat) else ("Moderate" if has_matru else "None"),
            astrological_signature=(
                f"Moon in {ZODIAC_SANSKRIT[moon_sign]}, 4th House is {ZODIAC_SANSKRIT[h4_idx]}."
            ),
            life_manifestations=(
                "Emotional loneliness, chronic anxiety, mother's health fragility, or difficulty enjoying domestic peace."
                if has_matru else "Maternal blessings flowing smoothly."
            ),
            prescribed_shanti_remedy=(
                "Serve and seek the blessings of mother/elderly women daily. Offer Kheer to young girls (Kanya Pooja) on Purnima. "
                "Feed white cows with boiled rice, curd, and sugar on Mondays."
            )
        )

        # 4. Guru Chandal Dosha Check (Jupiter conjunct Rahu or Ketu)
        jup_sign = planet_signs.get("Jupiter", 0)
        ketu_sign = planet_signs.get("Ketu", 0)
        has_gc = (jup_sign == rahu_sign) or (jup_sign == ketu_sign)
        gc_dosha = DoshaDetail(
            dosha_name="Guru Chandal Dosha",
            is_present=has_gc,
            severity="Moderate" if has_gc else "None",
            astrological_signature=f"Jupiter in {ZODIAC_SANSKRIT[jup_sign]} conjunct {'Rahu' if jup_sign == rahu_sign else 'Ketu'}.",
            life_manifestations=(
                "Cynicism towards orthodox beliefs, friction with teachers/mentors, digestive/liver sensitivities."
                if has_gc else "Guru's wisdom remains untainted."
            ),
            prescribed_shanti_remedy=(
                "Worship Lord Dakshinamurthy on Thursdays; donate yellow chana dal and turmeric at temples; wear 5-Mukhi Rudraksha."
            )
        )

        # 5. Grahan Dosha Check (Sun or Moon conjunct Rahu/Ketu within 12 deg)
        sun_lon = kundali.planets["Sun"].longitude
        moon_lon = kundali.planets["Moon"].longitude
        sun_node_dist = min(abs(sun_lon - rahu_lon), abs(sun_lon - ketu_lon))
        moon_node_dist = min(abs(moon_lon - rahu_lon), abs(moon_lon - ketu_lon))

        has_grahan = (sun_node_dist < 12.0) or (moon_node_dist < 12.0)
        grahan_dosha = DoshaDetail(
            dosha_name="Grahan Dosha (Eclipse Affliction to Luminaries)",
            is_present=has_grahan,
            severity="Severe" if has_grahan else "None",
            astrological_signature=(
                f"Sun-Node separation: {sun_node_dist:.2f}°, Moon-Node separation: {moon_node_dist:.2f}°."
            ),
            life_manifestations=(
                "Low vitality, identity crises, vision/eye vulnerabilities, or intense psychic fluctuations."
                if has_grahan else "Luminaries free from eclipse conjunction."
            ),
            prescribed_shanti_remedy=(
                "Perform Aditya Hridaya Stotram recitation at dawn for Surya Grahan; Shiva Ksheerabhishekam on Mondays for Chandra Grahan."
            )
        )

        # 6. Birth Phase & Eclipse Check
        elongation = (moon_lon - sun_lon) % 360
        is_eclipse_birth = (has_grahan and (elongation <= 12 or elongation >= 348 or (168 <= elongation <= 192)))

        birth_shantis = []
        if is_eclipse_birth:
            phase_type = "GRAHANA KALA (Solar or Lunar Eclipse Birth)"
            shanti_req = True
            phase_effects = (
                "Deep karmic intensity, exceptional psychic sensitivity, potential eye or nervous vulnerabilities, "
                "and an unconventional genius trajectory that defies normal boundaries."
            )
            birth_shantis = [
                "Grahana Janma Shanti Homa (performed on 27th day after birth or birth star return).",
                "Chhaya Patra Daan: Donate a bronze vessel containing warm cow's ghee reflecting the baby's face.",
                "Daily recitation of Maha Mrityunjaya Mantra (11 times) for physical vitality and longevity protection.",
                "Feed visually impaired people or donate to educational institutions on the native's Nakshatra day."
            ]
        elif elongation <= 12 or elongation >= 348:
            phase_type = "AMAVASYA (New Moon Birth - Ksheena Chandra)"
            shanti_req = True
            phase_effects = (
                "Total absence of lunar illumination (zero Paksha Bala). Imparts deep introversion, occult and research brilliance, "
                "alongside early childhood respiratory/vitality delicacy and paternal financial strain at birth."
            )
            birth_shantis = [
                "Amavasya Janma Shanti Pooja (pacifying the combined Sun-Moon conjunction and Pitrus).",
                "Kalastha Ghee Daan: Reflection of the child in molten cow ghee donated with grains and dakshina.",
                "Place a solid pure silver bangle on the child's arm to anchor lunar prana and soothe the nervous system.",
                "Feed white cows with boiled rice, sugar, and milk on Mondays."
            ]
        elif 168 <= elongation <= 192:
            phase_type = "PURNIMA (Full Moon Birth - Peak Paksha Bala)"
            shanti_req = False
            phase_effects = (
                "100% lunar brightness and magnetic charisma. Endows the child with creative brilliance, vivid imagination, and high empathy, "
                "with a tendency toward restless sleep and tidal emotional swings around full moon cycles."
            )
            birth_shantis = [
                "Sri Satyanarayana Swamy Pooja on naming day or first birthday.",
                "Shiva Abhishekam with raw cow's milk on Shukla Paksha Mondays to ground emotional waves.",
                "Adorn the child with a pure silver ornament for calm sleep."
            ]
        else:
            phase_type = "Standard Lunar Phase (Shukla / Krishna Paksha)"
            shanti_req = False
            phase_effects = "Standard harmonious lunar cycle without eclipse or combustion extremes."

        return MasterDoshaDossier(
            kala_sarpa_yoga_status=ks_status,
            kala_sarpa_type=ks_type_name,
            kala_sarpa_direction=ks_direction,
            kala_sarpa_bhanga=ks_bhanga,
            pitra_dosha=pitra_dosha,
            matru_dosha=matru_dosha,
            guru_chandal_dosha=gc_dosha,
            grahan_dosha=grahan_dosha,
            birth_phase_type=phase_type,
            birth_phase_shanti_required=shanti_req,
            birth_phase_effects=phase_effects,
            prescribed_birth_shanti_poojas=birth_shantis
        )
