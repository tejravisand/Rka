"""
Data models for life milestones and major astrological transitions.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional
from enum import Enum


class MilestoneCategory(Enum):
    SADE_SATI = "Sade Sati (Saturn 7.5 Year Cycle)"
    ASHTAMA_SHANI = "Ashtama Shani (Saturn in 8th)"
    KANTAKA_SHANI = "Kantaka Shani (Saturn in 4th/7th/10th)"
    JUPITER_RETURN = "Guru Gochara (Jupiter 12-Year Return)"
    NODAL_RETURN = "Rahu-Ketu Karmic Nodal Cycle"
    DASHA_SANDHI = "Dasha Sandhi / Chidra Dasha (Phase Handoff)"
    MARAKA_PERIOD = "Maraka Period (Health & Crisis Milestone)"
    RAJA_YOGA_ACTIVATION = "Raja Yoga / Dhana Yoga Golden Period"


@dataclass
class SadeSatiCycle:
    cycle_number: int              # 1st (Youth), 2nd (Mid-life), 3rd (Mature)
    start_date: datetime
    end_date: datetime
    phase1_start: datetime        # Saturn enters 12th from Moon (Rising)
    phase1_end: datetime
    phase2_start: datetime        # Saturn enters Janma Rasi (Peak)
    phase2_end: datetime
    phase3_start: datetime        # Saturn enters 2nd from Moon (Setting)
    phase3_end: datetime
    moon_sign: str
    impact_theme: str


@dataclass
class LifeMilestone:
    category: MilestoneCategory
    title: str
    start_date: datetime
    end_date: datetime
    approx_age_years: float
    description: str
    intensity: str                 # "High", "Medium", "Transformational", "Auspicious"
    recommended_focus: str
    traditional_remedies: List[str] = field(default_factory=list)
