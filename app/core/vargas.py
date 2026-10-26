"""
Comprehensive Shodashavarga (16 Divisional Charts) Engine.
Implements the exact mathematical rules and deity mappings from
Brihat Parasara Hora Sastra (BPHS) Chapter 6.
"""
from typing import Dict, List, Tuple
from app.models.astrological import VargaChart, VargaPlacement, Planet, ZodiacSign, PlanetPosition
from app.core.constants import SHODASHAVARGA_INFO, SIGN_LORDS
from app.core.ephemeris import get_planet_dignity


# 60 Shashtiamsa Deities (Names and nature: True = Benefic, False = Malefic)
SHASHTIAMSA_DEITIES = [
    ("Ghora", False), ("Rakshasa", False), ("Deva", True), ("Kubera", True),
    ("Yaksha", True), ("Kinnara", True), ("Bhrashta", False), ("Kulaghna", False),
    ("Garala", False), ("Vahni", False), ("Maya", False), ("Purishaka", False),
    ("Apampati", True), ("Marutvan", True), ("Kaala", False), ("Sarpa", False),
    ("Amrita", True), ("Indu", True), ("Mridu", True), ("Komala", True),
    ("Heramba", True), ("Brahma", True), ("Vishnu", True), ("Maheshwara", True),
    ("Deva", True), ("Ardra", True), ("Kalinasa", True), ("Kshiteeswara", True),
    ("Kamalakara", True), ("Gulika", False), ("Mrityu", False), ("Kaala", False),
    ("Davagni", False), ("Ghora", False), ("Yama", False), ("Kantaka", False),
    ("Suddha", True), ("Amrita", True), ("Purna", True), ("Vishapradigdha", False),
    ("Kulanasa", False), ("Vamshakshaya", False), ("Utpata", False), ("Kala", False),
    ("Saumya", True), ("Komala", True), ("Sheetala", True), ("Karaladamshtra", False),
    ("Chandramukhi", True), ("Praveena", True), ("Kaalapavaka", False), ("Dandashuka", False),
    ("Nirmala", True), ("Subha", True), ("Ashubha", False), ("Atisheetala", True),
    ("Sudha", True), ("Payodhi", True), ("Bhramana", False), ("Indurekha", True)
]


class VargaCalculator:
    """Calculates divisional sign placements for all 16 Shodashavargas."""

    @staticmethod
    def calculate_d1(sign_idx: int, deg: float) -> Tuple[int, float]:
        """D1 - Rasi Chart (1 x 30°)"""
        return sign_idx, deg

    @staticmethod
    def calculate_d2(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D2 - Hora (2 x 15°):
        Odd signs: 0-15° Sun (Leo, 4), 15-30° Moon (Cancer, 3)
        Even signs: 0-15° Moon (Cancer, 3), 15-30° Sun (Leo, 4)
        """
        part = int(deg / 15.0)  # 0 or 1
        rem = (deg % 15.0) * 2.0
        is_odd = (sign_idx % 2 == 0)  # 0-indexed: Aries=0 is odd sign

        if is_odd:
            mapped_sign = 4 if part == 0 else 3
        else:
            mapped_sign = 3 if part == 0 else 4

        return mapped_sign, rem

    @staticmethod
    def calculate_d3(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D3 - Drekkana (3 x 10°):
        Part 0 (0-10°): 1st house (same sign)
        Part 1 (10-20°): 5th house (+4 signs)
        Part 2 (20-30°): 9th house (+8 signs)
        """
        part = int(deg / 10.0)
        part = min(part, 2)
        rem = (deg % 10.0) * 3.0
        offset = [0, 4, 8][part]
        mapped_sign = (sign_idx + offset) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d4(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D4 - Chaturthamsa (4 x 7°30'):
        Part 0: Same sign (+0)
        Part 1: 4th sign (+3)
        Part 2: 7th sign (+6)
        Part 3: 10th sign (+9)
        """
        span = 30.0 / 4.0  # 7.5°
        part = int(deg / span)
        part = min(part, 3)
        rem = (deg % span) * 4.0
        mapped_sign = (sign_idx + part * 3) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d7(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D7 - Saptamsa (7 x 4°17'8.57"):
        Odd signs: starts from sign itself.
        Even signs: starts from 7th sign from it (+6).
        """
        span = 30.0 / 7.0
        part = int(deg / span)
        part = min(part, 6)
        rem = (deg % span) * 7.0
        is_odd = (sign_idx % 2 == 0)

        start = sign_idx if is_odd else (sign_idx + 6) % 12
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d9(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D9 - Navamsa (9 x 3°20' = 3.333333°):
        Movable (0, 3, 6, 9): starts from sign itself.
        Fixed (1, 4, 7, 10): starts from 9th sign from it (+8).
        Dual (2, 5, 8, 11): starts from 5th sign from it (+4).
        """
        span = 30.0 / 9.0  # 3.3333333333333335°
        part = int(deg / span)
        part = min(part, 8)
        rem = (deg % span) * 9.0

        modality = sign_idx % 3  # 0=Movable, 1=Fixed, 2=Dual
        if modality == 0:
            start = sign_idx
        elif modality == 1:
            start = (sign_idx + 8) % 12
        else:
            start = (sign_idx + 4) % 12

        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d10(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D10 - Dasamsa (10 x 3°):
        Odd signs: starts from sign itself.
        Even signs: starts from 9th sign from it (+8).
        """
        span = 3.0
        part = int(deg / span)
        part = min(part, 9)
        rem = (deg % span) * 10.0
        is_odd = (sign_idx % 2 == 0)

        start = sign_idx if is_odd else (sign_idx + 8) % 12
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d12(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D12 - Dwadasamsa (12 x 2°30' = 2.5°):
        Starts from the sign itself and counts consecutively.
        """
        span = 2.5
        part = int(deg / span)
        part = min(part, 11)
        rem = (deg % span) * 12.0
        mapped_sign = (sign_idx + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d16(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D16 - Shodashamsa / Kalamsa (16 x 1°52'30"):
        Movable signs: starts from Aries (0).
        Fixed signs: starts from Leo (4).
        Dual signs: starts from Sagittarius (8).
        """
        span = 30.0 / 16.0
        part = int(deg / span)
        part = min(part, 15)
        rem = (deg % span) * 16.0

        modality = sign_idx % 3
        start = [0, 4, 8][modality]
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d20(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D20 - Vimsamsa (20 x 1°30' = 1.5°):
        Movable signs: starts from Aries (0).
        Fixed signs: starts from Sagittarius (8).
        Dual signs: starts from Leo (4).
        """
        span = 1.5
        part = int(deg / span)
        part = min(part, 19)
        rem = (deg % span) * 20.0

        modality = sign_idx % 3
        start = [0, 8, 4][modality]
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d24(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D24 - Chaturvimsamsa / Siddhamsa (24 x 1°15' = 1.25°):
        Odd signs: starts from Leo (4).
        Even signs: starts from Cancer (3).
        """
        span = 1.25
        part = int(deg / span)
        part = min(part, 23)
        rem = (deg % span) * 24.0
        is_odd = (sign_idx % 2 == 0)

        start = 4 if is_odd else 3
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d27(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D27 - Saptavimsamsa / Bhamsha (27 x 1°6'40" = 30°/27):
        Fiery signs (0, 4, 8): starts from Aries (0).
        Earthy signs (1, 5, 9): starts from Cancer (3).
        Airy signs (2, 6, 10): starts from Libra (6).
        Watery signs (3, 7, 11): starts from Capricorn (9).
        """
        span = 30.0 / 27.0
        part = int(deg / span)
        part = min(part, 26)
        rem = (deg % span) * 27.0

        element = sign_idx % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
        start = [0, 3, 6, 9][element]
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d30(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D30 - Trimsamsa (30 unequal degrees per BPHS):
        Odd signs:
          0-5°: Mars (Aries, 0)
          5-10°: Saturn (Aquarius, 10)
          10-18°: Jupiter (Sagittarius, 8)
          18-25°: Mercury (Gemini, 2)
          25-30°: Venus (Libra, 6)
        Even signs:
          0-5°: Venus (Taurus, 1)
          5-12°: Mercury (Virgo, 5)
          12-20°: Jupiter (Pisces, 11)
          20-25°: Saturn (Capricorn, 9)
          25-30°: Mars (Scorpio, 7)
        """
        is_odd = (sign_idx % 2 == 0)

        if is_odd:
            if deg < 5.0:
                return 0, deg * 6.0
            elif deg < 10.0:
                return 10, (deg - 5.0) * 6.0
            elif deg < 18.0:
                return 8, (deg - 10.0) * 3.75
            elif deg < 25.0:
                return 2, (deg - 18.0) * 4.2857
            else:
                return 6, (deg - 25.0) * 6.0
        else:
            if deg < 5.0:
                return 1, deg * 6.0
            elif deg < 12.0:
                return 5, (deg - 5.0) * 4.2857
            elif deg < 20.0:
                return 11, (deg - 12.0) * 3.75
            elif deg < 25.0:
                return 9, (deg - 20.0) * 6.0
            else:
                return 7, (deg - 25.0) * 6.0

    @staticmethod
    def calculate_d40(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D40 - Khavedamsa (40 x 0°45' = 0.75°):
        Odd signs: starts from Aries (0).
        Even signs: starts from Libra (6).
        """
        span = 0.75
        part = int(deg / span)
        part = min(part, 39)
        rem = (deg % span) * 40.0
        is_odd = (sign_idx % 2 == 0)

        start = 0 if is_odd else 6
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d45(sign_idx: int, deg: float) -> Tuple[int, float]:
        """
        D45 - Akshavedamsa (45 x 0°40' = 2/3°):
        Movable signs: starts from Aries (0).
        Fixed signs: starts from Leo (4).
        Dual signs: starts from Sagittarius (8).
        """
        span = 30.0 / 45.0
        part = int(deg / span)
        part = min(part, 44)
        rem = (deg % span) * 45.0

        modality = sign_idx % 3
        start = [0, 4, 8][modality]
        mapped_sign = (start + part) % 12
        return mapped_sign, rem

    @staticmethod
    def calculate_d60(sign_idx: int, deg: float) -> Tuple[int, float, str, bool]:
        """
        D60 - Shashtiamsa (60 x 0°30' = 0.5°):
        Starts from sign itself, moves through all 12 signs sequentially.
        Also returns the Shashtiamsa deity name and whether it is benefic or malefic.
        """
        span = 0.5
        part = int(deg / span)
        part = min(part, 59)
        rem = (deg % span) * 60.0

        mapped_sign = (sign_idx + part) % 12
        deity_name, is_benefic = SHASHTIAMSA_DEITIES[part]
        return mapped_sign, rem, deity_name, is_benefic


def calculate_all_vargas(
    ascendant_pos: PlanetPosition,
    planets: Dict[str, PlanetPosition]
) -> Dict[int, VargaChart]:
    """
    Compute all 16 Shodashavarga charts for Lagna and all planets.
    """
    division_dispatch = {
        1: VargaCalculator.calculate_d1,
        2: VargaCalculator.calculate_d2,
        3: VargaCalculator.calculate_d3,
        4: VargaCalculator.calculate_d4,
        7: VargaCalculator.calculate_d7,
        9: VargaCalculator.calculate_d9,
        10: VargaCalculator.calculate_d10,
        12: VargaCalculator.calculate_d12,
        16: VargaCalculator.calculate_d16,
        20: VargaCalculator.calculate_d20,
        24: VargaCalculator.calculate_d24,
        27: VargaCalculator.calculate_d27,
        30: VargaCalculator.calculate_d30,
        40: VargaCalculator.calculate_d40,
        45: VargaCalculator.calculate_d45,
    }

    all_entities = {"Ascendant": ascendant_pos}
    all_entities.update(planets)

    varga_charts: Dict[int, VargaChart] = {}

    for div, (name, sanskrit, purpose, weight) in SHODASHAVARGA_INFO.items():
        chart = VargaChart(
            division=div,
            name=name,
            sanskrit_name=sanskrit,
            purpose=purpose,
            vimsopaka_points=weight,
            placements={}
        )

        for ent_name, pos in all_entities.items():
            sign_idx = pos.sign.value
            deg = pos.degrees_in_sign

            if div == 60:
                mapped_sign, rem_deg, deity, is_shubha = VargaCalculator.calculate_d60(sign_idx, deg)
            else:
                calc_func = division_dispatch[div]
                mapped_sign, rem_deg = calc_func(sign_idx, deg)

            sign_lord = SIGN_LORDS[mapped_sign]
            dignity = get_planet_dignity(ent_name, mapped_sign, rem_deg)

            chart.placements[ent_name] = VargaPlacement(
                planet=pos.planet,
                sign=ZodiacSign(mapped_sign),
                degrees_in_varga=round(rem_deg, 4),
                sign_lord=sign_lord,
                dignity=dignity
            )

        varga_charts[div] = chart

    return varga_charts
