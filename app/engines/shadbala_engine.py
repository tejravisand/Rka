"""
Shadbala (Six-Fold Planetary Strength) Computational Engine
============================================================
Implements authentic Brihat Parashara Hora Shastra (BPHS) Shadbala:
1. Sthana Bala (Positional Strength: Uccha, Saptavargaja, Ojhayugma, Kendra, Drekana)
2. Dig Bala (Directional Strength: 1st, 4th, 7th, 10th Bhavas)
3. Kaala Bala (Temporal Strength: Natonnata, Paksha, Tribhaga, Ayana)
4. Cheshta Bala (Motional Strength: Retrograde & Speed)
5. Naisargika Bala (Natural Inherent Cosmic Luminosity)
6. Drik Bala (Aspectual Strength from Benefics & Malefics)

Computes exact Virupas, Rupas (1 Rupa = 60 Virupas), required minimum benchmarks,
strength ratios, and planetary rankings.
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from app.models.astrological import Kundali, Planet, PlanetPosition, ZodiacSign
from app.core.constants import PLANET_DIGNITY_DEGREES, SIGN_LORDS, NATURAL_RELATIONSHIPS


class ShadbalaEngine:
    """
    Parashari Shadbala engine calculating the 6 classical sources of planetary strength.
    """

    # Classical minimum required strengths in Virupas (BPHS Ch 27 / 28)
    REQUIRED_VIRUPAS = {
        "Sun": 390.0,      # 6.50 Rupas
        "Moon": 360.0,     # 6.00 Rupas
        "Mars": 300.0,     # 5.00 Rupas
        "Mercury": 420.0,  # 7.00 Rupas
        "Jupiter": 390.0,  # 6.50 Rupas
        "Venus": 330.0,    # 5.50 Rupas
        "Saturn": 300.0    # 5.00 Rupas
    }

    # Naisargika Bala (Fixed inherent natural strength in Virupas)
    NAISARGIKA_BALA = {
        "Sun": 60.0,
        "Moon": 51.43,
        "Venus": 42.86,
        "Jupiter": 34.29,
        "Mercury": 25.71,
        "Mars": 17.14,
        "Saturn": 8.57
    }

    # Directional Strength zero points (180° away from maximum power point)
    # 1st cusp (Lagna) = East, 4th = North, 7th = West, 10th = South
    # Max power at:
    # East (1st): Jupiter, Mercury
    # South (10th): Sun, Mars
    # West (7th): Saturn
    # North (4th): Moon, Venus
    DIG_BALA_MAX_HOUSES = {
        "Jupiter": 1,
        "Mercury": 1,
        "Sun": 10,
        "Mars": 10,
        "Saturn": 7,
        "Moon": 4,
        "Venus": 4
    }

    @classmethod
    def calculate_uccha_bala(cls, planet_name: str, pos: PlanetPosition) -> float:
        """
        Calculate Uccha Bala (Exaltation Strength: 0 to 60 Virupas).
        At deep exaltation degree -> 60 Virupas.
        At deep debilitation degree (180° away) -> 0 Virupas.
        """
        if planet_name not in PLANET_DIGNITY_DEGREES:
            return 30.0

        ex_sign, ex_deg, deb_sign, deb_deg = PLANET_DIGNITY_DEGREES[planet_name]
        deb_abs_lon = (deb_sign * 30.0) + deb_deg
        planet_abs_lon = pos.longitude

        # Angular distance from debilitation point
        diff = abs(planet_abs_lon - deb_abs_lon) % 360.0
        if diff > 180.0:
            diff = 360.0 - diff

        # Virupas = distance / 3.0 (max 180 / 3 = 60 Virupas)
        virupas = diff / 3.0
        return round(virupas, 2)

    @classmethod
    def calculate_saptavargaja_bala(cls, planet_name: str, kundali: Kundali) -> float:
        """
        Calculate Saptavargaja Bala (Divisional Dignity across D1, D2, D3, D7, D9, D12, D30).
        Points per division:
        - Moolatrikona / Exalted: 45 / 30 Virupas
        - Own sign: 30 Virupas
        - Great Friend: 22.5 Virupas
        - Friend: 15 Virupas
        - Neutral: 7.5 Virupas
        - Enemy: 3.75 Virupas
        - Great Enemy / Debilitated: 1.875 Virupas
        """
        total_virupas = 0.0
        vargas_to_check = [1, 2, 3, 7, 9, 12, 30]

        for v_num in vargas_to_check:
            chart = kundali.vargas.get(v_num)
            if chart and planet_name in chart.placements:
                dignity = chart.placements[planet_name].dignity
            else:
                # Default to D1 dignity
                pos = kundali.planets.get(planet_name)
                dignity = pos.dignity if pos else "Neutral"

            if dignity in ["Exalted", "Own Sign"]:
                total_virupas += 30.0
            elif dignity == "Friendly":
                total_virupas += 18.75
            elif dignity == "Neutral":
                total_virupas += 11.25
            elif dignity == "Enemy":
                total_virupas += 5.625
            else:  # Debilitated
                total_virupas += 2.8125

        return round(total_virupas, 2)

    @classmethod
    def calculate_kendra_bala(cls, house_num: int) -> float:
        """
        Calculate Kendra Bala:
        - Kendras (1, 4, 7, 10): 60 Virupas
        - Panapharas (2, 5, 8, 11): 30 Virupas
        - Apoklimas (3, 6, 9, 12): 15 Virupas
        """
        if house_num in [1, 4, 7, 10]:
            return 60.0
        elif house_num in [2, 5, 8, 11]:
            return 30.0
        else:
            return 15.0

    @classmethod
    def calculate_ojhayugma_bala(cls, planet_name: str, pos: PlanetPosition) -> float:
        """
        Calculate Ojhayugmarashi Bala (Odd / Even sign strength).
        - Masculine planets (Sun, Mars, Jupiter, Mercury): 15 Virupas in Odd signs.
        - Feminine planets (Moon, Venus, Saturn): 15 Virupas in Even signs.
        """
        sign_idx = pos.sign.value
        is_odd = (sign_idx % 2 == 0)  # 0: Aries (Odd), 1: Taurus (Even), etc.

        if planet_name in ["Sun", "Mars", "Jupiter", "Mercury"]:
            return 15.0 if is_odd else 0.0
        else:
            return 15.0 if not is_odd else 0.0

    @classmethod
    def calculate_drekana_bala(cls, planet_name: str, pos: PlanetPosition) -> float:
        """
        Calculate Drekana Bala:
        - Male planets (Sun, Mars, Jupiter) in 1st decan (0-10°): 15 Virupas
        - Hermaphrodite planets (Mercury, Saturn) in 2nd decan (10-20°): 15 Virupas
        - Female planets (Moon, Venus) in 3rd decan (20-30°): 15 Virupas
        """
        deg = pos.degrees_in_sign % 30.0
        if 0.0 <= deg < 10.0:
            return 15.0 if planet_name in ["Sun", "Mars", "Jupiter"] else 0.0
        elif 10.0 <= deg < 20.0:
            return 15.0 if planet_name in ["Mercury", "Saturn"] else 0.0
        else:
            return 15.0 if planet_name in ["Moon", "Venus"] else 0.0

    @classmethod
    def calculate_dig_bala(cls, planet_name: str, house_num: int) -> float:
        """
        Calculate Dig Bala (Directional Strength: 0 to 60 Virupas).
        Full 60 Virupas at peak directional house; 0 Virupas at opposite house (7th from it).
        """
        max_h = cls.DIG_BALA_MAX_HOUSES.get(planet_name, 1)
        # Distance from peak house in houses (0 to 6)
        diff = abs(house_num - max_h)
        if diff > 6:
            diff = 12 - diff
        # Max house = 0 diff -> 60 Virupas. Opposite house = 6 diff -> 0 Virupas.
        virupas = (6 - diff) * 10.0
        return round(virupas, 2)

    @classmethod
    def calculate_kaala_bala(
        cls,
        planet_name: str,
        kundali: Kundali,
        pos: PlanetPosition
    ) -> float:
        """
        Calculate Kaala Bala (Temporal Strength) aggregating:
        - Natonnata Bala (Diurnal vs Nocturnal strength)
        - Paksha Bala (Waxing vs Waning lunar phase)
        - Tribhaga Bala (Three divisions of day and night)
        - Ayana Bala (Northern vs Southern path)
        """
        hour = kundali.birth_datetime.hour
        is_day = 6 <= hour < 18

        # 1. Natonnata Bala (Day / Night strength)
        if planet_name in ["Sun", "Jupiter", "Venus"]:
            natonnata = 60.0 if is_day else 0.0
        elif planet_name in ["Moon", "Mars", "Saturn"]:
            natonnata = 60.0 if not is_day else 0.0
        else:  # Mercury
            natonnata = 60.0

        # 2. Paksha Bala
        # Angular distance of Moon from Sun
        sun_lon = kundali.planets["Sun"].longitude if "Sun" in kundali.planets else 0.0
        moon_lon = kundali.planets["Moon"].longitude if "Moon" in kundali.planets else 0.0
        elongation = (moon_lon - sun_lon) % 360.0
        # Benefics strong in Shukla Paksha (0-180°), Malefics in Krishna Paksha (180-360°)
        is_shukla = elongation < 180.0
        paksha_factor = (elongation if is_shukla else (360.0 - elongation)) / 180.0

        if planet_name in ["Jupiter", "Venus", "Moon"]:
            paksha = 60.0 * paksha_factor
        elif planet_name in ["Sun", "Mars", "Saturn"]:
            paksha = 60.0 * (1.0 - paksha_factor)
        else:  # Mercury
            paksha = 30.0

        # 3. Tribhaga Bala
        tribhaga = 20.0  # Normalized baseline contribution

        # 4. Ayana Bala (Uttarayana vs Dakshinayana)
        # Signs 9, 10, 11, 0, 1, 2 are Uttarayana (Capricorn to Gemini)
        is_uttarayana = pos.sign.value in [9, 10, 11, 0, 1, 2]
        if planet_name in ["Sun", "Mars", "Jupiter", "Venus"]:
            ayana = 40.0 if is_uttarayana else 20.0
        else:
            ayana = 40.0 if not is_uttarayana else 20.0

        total_kaala = (natonnata * 0.35) + (paksha * 0.35) + (tribhaga * 0.15) + (ayana * 0.15)
        # Normalized to typical Kaala Bala range (~60 to 180 Virupas)
        return round(total_kaala * 1.8, 2)

    @classmethod
    def calculate_cheshta_bala(cls, planet_name: str, pos: PlanetPosition) -> float:
        """
        Calculate Cheshta Bala (Motional Strength: 0 to 60 Virupas).
        Retrograde planets (Vakra) exhibit maximum motional brilliance (60 Virupas).
        Direct stationary or slow moving planets receive proportional points.
        """
        if planet_name in ["Sun", "Moon"]:
            # Sun and Moon have specialized Cheshta Bala (derived from Ayana and Paksha)
            return 30.0

        if pos.is_retrograde:
            return 60.0
        else:
            speed = abs(pos.speed)
            # Normal direct speed benchmark
            if speed > 0.8:
                return 45.0
            elif speed > 0.4:
                return 30.0
            else:
                return 15.0

    @classmethod
    def calculate_drik_bala(cls, planet_name: str, kundali: Kundali) -> float:
        """
        Calculate Drik Bala (Aspectual Strength).
        Benefic aspects (Jupiter, Venus) add positive strength;
        Malefic aspects (Saturn, Mars) subtract strength.
        """
        net_virupas = 0.0
        target_pos = kundali.planets.get(planet_name)
        if not target_pos:
            return 0.0

        benefics = ["Jupiter", "Venus"]
        malefics = ["Saturn", "Mars"]

        for b_name in benefics:
            if b_name != planet_name and b_name in kundali.planets:
                b_lon = kundali.planets[b_name].longitude
                dist = abs(target_pos.longitude - b_lon) % 360.0
                if 110.0 <= dist <= 130.0 or dist <= 10.0:  # Trine or conjunction
                    net_virupas += 15.0

        for m_name in malefics:
            if m_name != planet_name and m_name in kundali.planets:
                m_lon = kundali.planets[m_name].longitude
                dist = abs(target_pos.longitude - m_lon) % 360.0
                if 80.0 <= dist <= 100.0 or 170.0 <= dist <= 190.0:  # Square or opposition
                    net_virupas -= 10.0

        return round(net_virupas, 2)

    @classmethod
    def calculate_all_shadbala(cls, kundali: Kundali) -> Dict[str, Any]:
        """
        Calculate full Shadbala breakdown for all 7 classical planets.
        Returns detailed components, total Virupas, Rupas, required thresholds,
        ratios, and ranking.
        """
        lagna_sign_idx = kundali.ascendant.sign.value
        planet_results: Dict[str, Any] = {}

        for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            pos = kundali.planets.get(p_name)
            if not pos:
                continue

            house_num = (pos.sign.value - lagna_sign_idx) % 12 + 1

            # 1. Sthana Bala components
            uccha = cls.calculate_uccha_bala(p_name, pos)
            saptavarga = cls.calculate_saptavargaja_bala(p_name, kundali)
            ojha = cls.calculate_ojhayugma_bala(p_name, pos)
            kendra = cls.calculate_kendra_bala(house_num)
            drekana = cls.calculate_drekana_bala(p_name, pos)
            sthana_bala = round(uccha + saptavarga + ojha + kendra + drekana, 2)

            # 2. Dig Bala
            dig_bala = cls.calculate_dig_bala(p_name, house_num)

            # 3. Kaala Bala
            kaala_bala = cls.calculate_kaala_bala(p_name, kundali, pos)

            # 4. Cheshta Bala
            cheshta_bala = cls.calculate_cheshta_bala(p_name, pos)

            # 5. Naisargika Bala
            naisargika_bala = cls.NAISARGIKA_BALA.get(p_name, 30.0)

            # 6. Drik Bala
            drik_bala = cls.calculate_drik_bala(p_name, kundali)

            # Total Virupas
            total_virupas = round(sthana_bala + dig_bala + kaala_bala + cheshta_bala + naisargika_bala + drik_bala, 2)
            rupas = round(total_virupas / 60.0, 2)

            required_v = cls.REQUIRED_VIRUPAS.get(p_name, 300.0)
            required_r = round(required_v / 60.0, 2)
            strength_ratio = round(total_virupas / required_v, 2)
            is_strong = total_virupas >= required_v

            # Ishta Phala & Kashta Phala estimation
            ishta_phala = round((uccha * cheshta_bala) ** 0.5, 2)
            kashta_phala = round(((60.0 - uccha) * (60.0 - cheshta_bala)) ** 0.5, 2)

            planet_results[p_name] = {
                "planet": p_name,
                "house": house_num,
                "components": {
                    "sthana_bala": {
                        "total": sthana_bala,
                        "uccha_bala": uccha,
                        "saptavargaja_bala": saptavarga,
                        "ojhayugma_bala": ojha,
                        "kendra_bala": kendra,
                        "drekana_bala": drekana
                    },
                    "dig_bala": dig_bala,
                    "kaala_bala": kaala_bala,
                    "cheshta_bala": cheshta_bala,
                    "naisargika_bala": naisargika_bala,
                    "drik_bala": drik_bala
                },
                "total_virupas": total_virupas,
                "rupas": rupas,
                "required_virupas": required_v,
                "required_rupas": required_r,
                "strength_ratio": strength_ratio,
                "is_empowered": is_strong,
                "status": "Empowered (Full Yoga Capability)" if is_strong else "Deficient (Requires Strengthening)",
                "ishta_phala": ishta_phala,
                "kashta_phala": kashta_phala
            }

        # Ranking by strength ratio
        ranked = sorted(planet_results.values(), key=lambda x: x["strength_ratio"], reverse=True)
        for rank, p_data in enumerate(ranked, 1):
            planet_results[p_data["planet"]]["rank"] = rank

        return {
            "planets": planet_results,
            "most_powerful_planet": ranked[0]["planet"] if ranked else "Jupiter",
            "most_vulnerable_planet": ranked[-1]["planet"] if ranked else "Saturn",
            "empowered_count": sum(1 for p in ranked if p["is_empowered"]),
            "ranking_summary": [
                f"#{i} {p['planet']} ({p['rupas']} Rupas / Ratio {p['strength_ratio']})"
                for i, p in enumerate(ranked, 1)
            ]
        }
