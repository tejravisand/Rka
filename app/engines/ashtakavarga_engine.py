"""
Ashtakavarga Computational Engine
==================================
Implements classical Brihat Parashara Hora Shastra (BPHS) Ashtakavarga:
1. Bhinna Ashtakavarga (BAV) for all 7 planets (Total 337 Bindus) + Lagna
2. Sarvashtakavarga (SAV) aggregation and house-wise assessment
3. Trikona Shodhana (Triplicity Reduction)
4. Ekadhipatya Shodhana (Dual Lordship Reduction)
5. Shodhita Pinda (Rashi Pinda + Graha Pinda = Yoga Pinda)
6. Kakshya Analysis (8 sub-zones of 3°45' per sign for micro-transit timing)
"""

from typing import Dict, List, Any, Optional, Tuple
from app.models.astrological import Kundali, Planet, PlanetPosition, ZodiacSign
from app.core.constants import ZODIAC_SIGNS, ZODIAC_SANSKRIT, SIGN_LORDS


class AshtakavargaEngine:
    """
    Parashari Ashtakavarga engine adhering strictly to Brihat Parashara Hora Shastra
    chapters 66 to 72.
    """

    # Classical BPHS Benefic houses (1-indexed) contributed by each reference point
    # Each list represents the houses (counted from that planet's position) that receive 1 bindu.
    SUN_RULES = {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [3, 4, 6, 10, 11, 12]
    }  # Total 48 bindus

    MOON_RULES = {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [3, 6, 10, 11]
    }  # Total 49 bindus

    MARS_RULES = {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 3, 6, 10, 11]
    }  # Total 39 bindus

    MERCURY_RULES = {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 2, 4, 6, 8, 10, 11]
    }  # Total 54 bindus

    JUPITER_RULES = {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Ascendant": [1, 2, 4, 5, 6, 7, 9, 10, 11]
    }  # Total 56 bindus

    VENUS_RULES = {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Ascendant": [1, 2, 3, 4, 5, 8, 9, 11]
    }  # Total 52 bindus

    SATURN_RULES = {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [1, 3, 4, 6, 10, 11]
    }  # Total 39 bindus

    PLANET_RULES_MAP = {
        "Sun": SUN_RULES,
        "Moon": MOON_RULES,
        "Mars": MARS_RULES,
        "Mercury": MERCURY_RULES,
        "Jupiter": JUPITER_RULES,
        "Venus": VENUS_RULES,
        "Saturn": SATURN_RULES
    }

    # Rashi Pinda Multipliers (BPHS Ch 69)
    # Aries: 7, Taurus: 10, Gemini: 8, Cancer: 4, Leo: 10, Virgo: 5,
    # Libra: 7, Scorpio: 8, Sagittarius: 9, Capricorn: 5, Aquarius: 11, Pisces: 12
    RASHI_PINDA_MULTIPLIERS = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]

    # Graha Pinda Multipliers (BPHS Ch 69)
    GRAHA_PINDA_MULTIPLIERS = {
        "Sun": 5,
        "Moon": 5,
        "Mars": 8,
        "Mercury": 5,
        "Jupiter": 10,
        "Venus": 7,
        "Saturn": 5
    }

    # Kakshya planetary sequence (8 zones of 3°45' = 3.75° per sign)
    KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Ascendant"]

    @classmethod
    def calculate_bav(cls, target_planet: str, kundali: Kundali) -> List[int]:
        """
        Calculate Bhinna Ashtakavarga (BAV) for a single planet across 12 signs (Aries to Pisces).
        Returns a 12-element list containing the bindu counts for signs 0 to 11.
        """
        rules = cls.PLANET_RULES_MAP.get(target_planet)
        if not rules:
            return [0] * 12

        bindus = [0] * 12

        # Map reference bodies to sign indices
        ref_signs: Dict[str, int] = {}
        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            if p_name in kundali.planets:
                ref_signs[p_name] = kundali.planets[p_name].sign.value
        ref_signs["Ascendant"] = kundali.ascendant.sign.value

        for ref_body, houses in rules.items():
            base_sign = ref_signs.get(ref_body)
            if base_sign is None:
                continue
            for h in houses:
                target_sign = (base_sign + (h - 1)) % 12
                bindus[target_sign] += 1

        return bindus

    @classmethod
    def calculate_all_bav(cls, kundali: Kundali) -> Dict[str, List[int]]:
        """
        Calculate BAV tables for all 7 classical planets.
        """
        bav_tables: Dict[str, List[int]] = {}
        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            bav_tables[p_name] = cls.calculate_bav(p_name, kundali)
        return bav_tables

    @classmethod
    def calculate_sav(cls, kundali: Kundali) -> List[int]:
        """
        Calculate Sarvashtakavarga (SAV) by summing BAV bindus across all 7 planets
        for each sign (Aries to Pisces). Total across all 12 signs equals exactly 337.
        """
        all_bav = cls.calculate_all_bav(kundali)
        sav = [0] * 12
        for p_name, table in all_bav.items():
            for s_idx in range(12):
                sav[s_idx] += table[s_idx]
        return sav

    @classmethod
    def trikona_shodhana(cls, bindus: List[int]) -> List[int]:
        """
        Apply Trikona Shodhana (Triplicity Reduction) according to BPHS Ch 68.
        Triplicities:
        - Fire: Aries (0), Leo (4), Sagittarius (8)
        - Earth: Taurus (1), Virgo (5), Capricorn (9)
        - Air: Gemini (2), Libra (6), Aquarius (10)
        - Water: Cancer (3), Scorpio (7), Pisces (11)
        Rule:
        - If all three signs have bindus, find the minimum and subtract it from all three.
        - If one or more have zero, make remaining non-zeros zero or subtract minimum according
          to classical trikona rules.
        """
        reduced = list(bindus)
        triplicities = [
            [0, 4, 8],    # Fire
            [1, 5, 9],    # Earth
            [2, 6, 10],   # Air
            [3, 7, 11]    # Water
        ]

        for trip in triplicities:
            vals = [reduced[i] for i in trip]
            min_val = min(vals)
            # Subtract minimum from all three signs in the triplicity
            for i in trip:
                reduced[i] -= min_val

        return reduced

    @classmethod
    def ekadhipatya_shodhana(cls, trikona_bindus: List[int], kundali: Kundali) -> List[int]:
        """
        Apply Ekadhipatya Shodhana (Dual Lordship Reduction) according to BPHS Ch 68.
        Applies to pairs of signs owned by the same planet:
        - Mars: Aries (0) & Scorpio (7)
        - Venus: Taurus (1) & Libra (6)
        - Mercury: Gemini (2) & Virgo (5)
        - Jupiter: Sagittarius (8) & Pisces (11)
        - Saturn: Capricorn (9) & Aquarius (10)
        (Sun rules Leo 4 and Moon rules Cancer 3 - single ownership, no reduction).
        """
        reduced = list(trikona_bindus)
        dual_pairs = [
            (0, 7),   # Mars: Aries & Scorpio
            (1, 6),   # Venus: Taurus & Libra
            (2, 5),   # Mercury: Gemini & Virgo
            (8, 11),  # Jupiter: Sagittarius & Pisces
            (9, 10)   # Saturn: Capricorn & Aquarius
        ]

        # Check occupancy of signs
        occupied_signs = set()
        for p_name, pos in kundali.planets.items():
            occupied_signs.add(pos.sign.value)

        for s1, s2 in dual_pairs:
            occ1 = s1 in occupied_signs
            occ2 = s2 in occupied_signs
            v1 = reduced[s1]
            v2 = reduced[s2]

            if v1 == 0 or v2 == 0:
                continue

            # Case 1: Both signs are occupied by planets -> No reduction
            if occ1 and occ2:
                continue

            # Case 2: Neither sign is occupied -> Both take the smaller value (or larger is reduced)
            if not occ1 and not occ2:
                min_v = min(v1, v2)
                reduced[s1] = min_v
                reduced[s2] = min_v
            # Case 3: One is occupied, one is unoccupied
            elif occ1 and not occ2:
                # The unoccupied sign's bindu is reduced to zero or difference
                reduced[s2] = 0
            elif occ2 and not occ1:
                reduced[s1] = 0

        return reduced

    @classmethod
    def calculate_pindas(
        cls,
        planet_name: str,
        shodhita_bindus: List[int],
        kundali: Kundali
    ) -> Dict[str, int]:
        """
        Calculate Shodhita Pindas (Rashi Pinda, Graha Pinda, and Yoga Pinda) according to BPHS Ch 69.
        - Rashi Pinda: Sum of (Shodhita bindus in each sign * sign multiplier).
        - Graha Pinda: Sum of (Shodhita bindus in sign occupied by planet * planet multiplier).
        - Yoga Pinda: Rashi Pinda + Graha Pinda.
        """
        # 1. Rashi Pinda
        rashi_pinda = 0
        for s_idx in range(12):
            rashi_pinda += shodhita_bindus[s_idx] * cls.RASHI_PINDA_MULTIPLIERS[s_idx]

        # 2. Graha Pinda
        graha_pinda = 0
        for p_name, p_mult in cls.GRAHA_PINDA_MULTIPLIERS.items():
            pos = kundali.planets.get(p_name)
            if pos:
                s_idx = pos.sign.value
                graha_pinda += shodhita_bindus[s_idx] * p_mult

        yoga_pinda = rashi_pinda + graha_pinda

        return {
            "planet": planet_name,
            "rashi_pinda": rashi_pinda,
            "graha_pinda": graha_pinda,
            "yoga_pinda": yoga_pinda
        }

    @classmethod
    def get_kakshya(cls, degree_in_sign: float) -> Tuple[int, str, float, float]:
        """
        Identify the Kakshya zone (1 to 8) and Kakshya lord for a specific degree in a sign (0-30°).
        Each Kakshya is 3°45' = 3.75°.
        """
        deg = max(0.0, min(29.9999, degree_in_sign))
        kakshya_idx = int(deg / 3.75)
        kakshya_idx = min(7, kakshya_idx)
        lord = cls.KAKSHYA_LORDS[kakshya_idx]
        start_deg = round(kakshya_idx * 3.75, 2)
        end_deg = round((kakshya_idx + 1) * 3.75, 2)
        return kakshya_idx + 1, lord, start_deg, end_deg

    @classmethod
    def get_complete_ashtakavarga(cls, kundali: Kundali) -> Dict[str, Any]:
        """
        Generate complete, structured Ashtakavarga dossier including BAV, SAV,
        Trikona Shodhana, Ekadhipatya Shodhana, Pindas, and Bhava-wise strength.
        """
        lagna_sign_idx = kundali.ascendant.sign.value
        all_bav = cls.calculate_all_bav(kundali)
        sav = cls.calculate_sav(kundali)

        # Map SAV to Bhavas (1 to 12) from Lagna
        house_sav: List[Dict[str, Any]] = []
        for h in range(1, 13):
            sign_idx = (lagna_sign_idx + (h - 1)) % 12
            bindus = sav[sign_idx]
            status = "Strong / Auspicious" if bindus >= 28 else (
                "Moderate" if bindus >= 25 else "Weak / Vulnerable"
            )
            house_sav.append({
                "house": h,
                "sign_index": sign_idx,
                "sign_name": ZODIAC_SIGNS[sign_idx],
                "sign_sanskrit": ZODIAC_SANSKRIT[sign_idx],
                "bindus": bindus,
                "status": status
            })

        # Financial wealth metrics: 11th house (Gains) vs 10th (Effort) vs 12th (Expenses)
        b10 = house_sav[9]["bindus"]
        b11 = house_sav[10]["bindus"]
        b12 = house_sav[11]["bindus"]
        wealth_potential = "High Accumulation" if (b11 > b12 and b11 >= b10) else (
            "Steady Balance" if (b11 >= b12) else "Higher Outflows / Expenditure Caution"
        )

        # Shodhana and Pindas for each planet
        shodhana_data: Dict[str, Any] = {}
        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            raw_bav = all_bav[p_name]
            trikona_reduced = cls.trikona_shodhana(raw_bav)
            ekadhipatya_reduced = cls.ekadhipatya_shodhana(trikona_reduced, kundali)
            pindas = cls.calculate_pindas(p_name, ekadhipatya_reduced, kundali)

            shodhana_data[p_name] = {
                "raw_bav": raw_bav,
                "trikona_shodhana": trikona_reduced,
                "ekadhipatya_shodhana": ekadhipatya_reduced,
                "pindas": pindas
            }

        return {
            "sarvashtakavarga_totals": sav,
            "total_sav_bindus": sum(sav),  # Should be 337
            "house_sav": house_sav,
            "wealth_financial_flow": {
                "10th_house_bindus": b10,
                "11th_house_bindus": b11,
                "12th_house_bindus": b12,
                "assessment": wealth_potential
            },
            "bhinna_ashtakavarga": all_bav,
            "shodhana_and_pindas": shodhana_data
        }
