"""
Data models for astrological calculations.
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from enum import Enum


class ZodiacSign(Enum):
    ARIES = 0
    TAURUS = 1
    GEMINI = 2
    CANCER = 3
    LEO = 4
    VIRGO = 5
    LIBRA = 6
    SCORPIO = 7
    SAGITTARIUS = 8
    CAPRICORN = 9
    AQUARIUS = 10
    PISCES = 11

    @property
    def sanskrit_name(self) -> str:
        names = [
            "Mesha", "Vrishabha", "Mithuna", "Karka",
            "Simha", "Kanya", "Tula", "Vrischika",
            "Dhanus", "Makara", "Kumbha", "Meena"
        ]
        return names[self.value]

    @property
    def element(self) -> str:
        # Fire, Earth, Air, Water
        elements = ["Fire", "Earth", "Air", "Water"]
        return elements[self.value % 4]

    @property
    def modality(self) -> str:
        # Movable (Chara), Fixed (Sthira), Dual (Dwisvabhava)
        modalities = ["Movable", "Fixed", "Dual"]
        return modalities[self.value % 3]


class Planet(Enum):
    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"
    ASCENDANT = "Ascendant"  # Lagna

    @property
    def sanskrit_name(self) -> str:
        names = {
            "Sun": "Surya",
            "Moon": "Chandra",
            "Mars": "Mangala",
            "Mercury": "Budha",
            "Jupiter": "Guru",
            "Venus": "Shukra",
            "Saturn": "Shani",
            "Rahu": "Rahu",
            "Ketu": "Ketu",
            "Ascendant": "Lagna"
        }
        return names.get(self.value, self.value)


@dataclass
class PlanetPosition:
    planet: Planet
    longitude: float               # 0.0 to 360.0 degrees (sidereal)
    sign: ZodiacSign               # 0 to 11
    degrees_in_sign: float         # 0.0 to 30.0 degrees
    nakshatra_number: int          # 0 to 26
    nakshatra_name: str            # e.g., "Rohini"
    nakshatra_pada: int            # 1 to 4
    nakshatra_lord: str            # e.g., "Moon"
    is_retrograde: bool = False
    speed: float = 0.0             # degrees per day
    dignity: str = "Neutral"       # Exalted, Own, Friendly, Neutral, Enemy, Debilitated


@dataclass
class Bhava:
    number: int                    # 1 to 12
    sign: ZodiacSign
    start_degree: float
    mid_degree: float              # Bhava Madhya
    end_degree: float
    planets: List[Planet] = field(default_factory=list)


@dataclass
class VargaPlacement:
    planet: Planet
    sign: ZodiacSign
    degrees_in_varga: float
    sign_lord: str
    dignity: str = "Neutral"


@dataclass
class VargaChart:
    division: int                  # e.g., 1, 9, 10, 60
    name: str                      # e.g., "Navamsa", "Dasamsa"
    sanskrit_name: str             # e.g., "D9 - Navamsa"
    purpose: str                   # e.g., "Dharma, Spouse, Inner Potential"
    vimsopaka_points: float        # Weight out of 20
    placements: Dict[str, VargaPlacement] = field(default_factory=dict)


@dataclass
class DashaPeriod:
    level: int                     # 1 = Mahadasha, 2 = Antardasha (Bhukti), 3 = Pratyantardasha, 4 = Sookshma
    level_name: str                # "Mahadasha", "Antardasha (Bhukti)", etc.
    lord: str                      # Planet name
    start_date: datetime
    end_date: datetime
    duration_years: float
    sub_periods: List['DashaPeriod'] = field(default_factory=list)

    @property
    def duration_days(self) -> float:
        return (self.end_date - self.start_date).total_seconds() / 86400.0


@dataclass
class Kundali:
    birth_datetime: datetime
    latitude: float
    longitude: float
    timezone_offset_hours: float
    ayanamsa_name: str
    ayanamsa_value: float
    ascendant: PlanetPosition
    planets: Dict[str, PlanetPosition]
    houses: List[Bhava]
    vargas: Dict[int, VargaChart] = field(default_factory=dict)
