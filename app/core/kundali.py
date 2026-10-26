"""
Kundali (Birth Chart / D1 Rasi) and Bhava (House) calculation engine.
Classical Vedic Whole Sign and Equal Bhava systems.
"""
from typing import Dict, List
from datetime import datetime, timezone
from app.models.astrological import Kundali, Bhava, PlanetPosition, Planet, ZodiacSign
from app.core.ephemeris import calculate_birth_positions, normalize_degrees


def calculate_kundali(
    birth_dt_utc: datetime,
    latitude: float,
    longitude: float,
    tz_offset_hours: float = 5.5
) -> Kundali:
    """
    Construct the full D1 Kundali with all 12 Bhavas and planetary positions.
    """
    ayanamsa_val, asc_pos, planets = calculate_birth_positions(birth_dt_utc, latitude, longitude)

    lagna_sign_idx = asc_pos.sign.value
    houses: List[Bhava] = []

    # Whole Sign House System (Classical Vedic Rasi-as-Bhava):
    # 1st House = Lagna Sign
    # 2nd House = Next Sign, ..., 12th House = 12th Sign
    for h in range(1, 13):
        sign_val = (lagna_sign_idx + (h - 1)) % 12
        start_deg = sign_val * 30.0
        mid_deg = start_deg + 15.0
        end_deg = (start_deg + 30.0) % 360.0

        # Find planets in this house sign
        planets_in_house: List[Planet] = []
        for p_name, p_pos in planets.items():
            if p_pos.sign.value == sign_val:
                planets_in_house.append(p_pos.planet)

        houses.append(Bhava(
            number=h,
            sign=ZodiacSign(sign_val),
            start_degree=start_deg,
            mid_degree=mid_deg,
            end_degree=end_deg,
            planets=planets_in_house
        ))

    return Kundali(
        birth_datetime=birth_dt_utc,
        latitude=latitude,
        longitude=longitude,
        timezone_offset_hours=tz_offset_hours,
        ayanamsa_name="Lahiri (Chitra Paksha)",
        ayanamsa_value=round(ayanamsa_val, 4),
        ascendant=asc_pos,
        planets=planets,
        houses=houses
    )


def get_house_lord(kundali: Kundali, house_num: int) -> str:
    """Get the ruling planet of a given house number (1 to 12)."""
    from app.core.constants import SIGN_LORDS
    if 1 <= house_num <= 12:
        house = kundali.houses[house_num - 1]
        return SIGN_LORDS[house.sign.value]
    raise ValueError(f"Invalid house number: {house_num}")


def get_planets_in_house(kundali: Kundali, house_num: int) -> List[str]:
    """Get list of planet names situated in a given house number."""
    if 1 <= house_num <= 12:
        house = kundali.houses[house_num - 1]
        return [p.value for p in house.planets]
    return []
