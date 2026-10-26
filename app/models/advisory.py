"""
Data models for personalized lifestyle, vehicle, property, and attire recommendations.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class VehicleColorRecommendation:
    primary_lucky_colors: List[str]
    secondary_favorable_colors: List[str]
    colors_to_avoid: List[str]
    fourth_house_lord: str
    fourth_house_sign: str
    venus_dignity: str
    d16_shodashamsa_guidance: str
    practical_advice: str


@dataclass
class PropertyDirectionRecommendation:
    property_type: str                   # "Residential House / Land" or "Commercial Office / Store"
    primary_best_directions: List[str]   # e.g., ["North", "North-East", "East"]
    secondary_acceptable_directions: List[str]
    directions_to_avoid: List[str]
    main_entrance_facing: str
    ruling_houses: str                   # "4th House (Sukha) & Lagna" or "10th House (Karma) & 11th (Labha)"
    astrological_rationale: str
    vastu_key_principles: List[str]


@dataclass
class DailyDressColorGuide:
    day_name: str                        # "Monday", "Tuesday", etc.
    ruling_planet: str                   # "Moon", "Mars", etc.
    primary_favorable_colors: List[str]
    accent_complementary_colors: List[str]
    colors_to_avoid_today: List[str]
    recommended_fabrics: str
    personalized_boost_tip: str


@dataclass
class LifestyleDossier:
    lagna_sign: str
    moon_sign: str
    vehicle_advice: VehicleColorRecommendation
    residential_property_advice: PropertyDirectionRecommendation
    commercial_office_advice: PropertyDirectionRecommendation
    weekly_dress_guide: Dict[str, DailyDressColorGuide]
    eternal_power_colors: List[str]      # Based on Lagna Lord & 9th Lord
    eternal_caution_colors: List[str]    # Based on 6th/8th/12th Dusthana lords
