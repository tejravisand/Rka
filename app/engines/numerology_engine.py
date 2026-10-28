"""
Numerology (Anka Vidya) Engine.
Implements:
1. Mulank (Psychic / Birth Number) from birth day (1-31).
2. Bhagyank (Destiny / Life Path Number) from full date of birth.
3. Namank (Name Number) using authentic Chaldean and Pythagorean systems.
4. Cheiro Compound Number vibrations (e.g., 14, 19, 23, 24, 28, 32, 37, 41, 46).
5. Personal Year, Personal Month, and Personal Day calculations at the moment of asking questions.
6. Number Harmony, Lucky Colors, Lucky Days, Inimical Numbers, and Name Vibration tuning.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple, Any


# Chaldean Alphabet Value Table (9 is omitted as sacred in Chaldean)
CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

# Pythagorean Alphabet Value Table (1 to 9 cyclical)
PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

# Planetary Rulers of Numbers
NUMBER_RULERS = {
    1: {"planet": "Sun (Surya)", "nature": "Leadership, vitality, ambition, administrative initiative"},
    2: {"planet": "Moon (Chandra)", "nature": "Intuition, diplomacy, emotional warmth, partnerships"},
    3: {"planet": "Jupiter (Guru)", "nature": "Wisdom, expansion, counseling, creative intellect"},
    4: {"planet": "Rahu (Uranus)", "nature": "Unconventional intellect, sudden turns, structural stamina"},
    5: {"planet": "Mercury (Budha)", "nature": "Commercial acumen, adaptability, quick wit, communication"},
    6: {"planet": "Venus (Shukra)", "nature": "Harmony, luxury, elegance, magnetic charisma, responsibility"},
    7: {"planet": "Ketu (Neptune)", "nature": "Mysticism, analytical research, spiritual depth, detachment"},
    8: {"planet": "Saturn (Shani)", "nature": "Perseverance, executive authority, karmic trials, lasting wealth"},
    9: {"planet": "Mars (Mangala)", "nature": "Courage, energy, competitive drive, humanitarian passion"}
}

# Number Harmony / Friendship Matrix
NUMBER_RELATIONS = {
    1: {"friendly": [1, 2, 3, 5, 9], "neutral": [4, 7], "inimical": [6, 8]},
    2: {"friendly": [1, 2, 3, 5], "neutral": [7, 9], "inimical": [4, 6, 8]},
    3: {"friendly": [1, 2, 3, 9], "neutral": [5], "inimical": [4, 6, 7, 8]},
    4: {"friendly": [1, 5, 6, 7], "neutral": [8], "inimical": [2, 4, 9]},
    5: {"friendly": [1, 2, 3, 5, 6], "neutral": [7, 8, 9], "inimical": [4]},
    6: {"friendly": [1, 4, 5, 6, 7], "neutral": [8, 9], "inimical": [2, 3]},
    7: {"friendly": [1, 4, 5, 6], "neutral": [2], "inimical": [3, 8, 9]},
    8: {"friendly": [3, 5, 6, 7], "neutral": [4], "inimical": [1, 2, 9]},
    9: {"friendly": [1, 2, 3, 5], "neutral": [6, 7], "inimical": [4, 8]}
}

# Lucky Attributes
LUCKY_ATTRIBUTES = {
    1: {"days": ["Sunday", "Monday"], "colors": ["Gold", "Orange", "Copper", "Bright Yellow"], "dates": [1, 10, 19, 28]},
    2: {"days": ["Monday", "Sunday"], "colors": ["Pearl White", "Cream", "Silver", "Soft Green"], "dates": [2, 11, 20, 29]},
    3: {"days": ["Thursday", "Tuesday"], "colors": ["Bright Yellow", "Saffron", "Turmeric Gold", "Amber"], "dates": [3, 12, 21, 30]},
    4: {"days": ["Wednesday", "Saturday"], "colors": ["Electric Blue", "Grey", "Silver Grey", "Pastels"], "dates": [4, 13, 22, 31]},
    5: {"days": ["Wednesday", "Friday"], "colors": ["Emerald Green", "Mint", "Turquoise", "Sage"], "dates": [5, 14, 23]},
    6: {"days": ["Friday", "Wednesday"], "colors": ["Pure White", "Pastel Pink", "Rose", "Cream"], "dates": [6, 15, 24]},
    7: {"days": ["Monday", "Thursday"], "colors": ["Light Green", "White", "Smoky Topaz", "Pastel Yellow"], "dates": [7, 16, 25]},
    8: {"days": ["Saturday", "Wednesday"], "colors": ["Dark Navy Blue", "Charcoal", "Indigo", "Steel Grey"], "dates": [8, 17, 26]},
    9: {"days": ["Tuesday", "Thursday"], "colors": ["Coral Red", "Scarlet", "Crimson", "Terracotta"], "dates": [9, 18, 27]}
}

# Classical Chaldean Compound Number Meaning
CHALDEAN_COMPOUNDS = {
    10: "The Wheel of Fortune — Rise and fall, honor, faith, will accomplish plans.",
    11: "A Lion Muzzled — Clashing desires, hidden emotional tests, high intuition.",
    12: "The Sacrifice — Suffering for others, inner anxiety, need for clear boundaries.",
    13: "Regeneration & Upheaval — Power through transformation, breaking obsolete shackles.",
    14: "Movement & Challenge — Fortunate with risk management, commercial contracts.",
    15: "The Magician / Charisma — Highly fortunate for material gains, artistic eloquence.",
    16: "The Shattered Citadel — Vulnerable to sudden pride, requires ethical grounding.",
    17: "The Star of the Magi — Immense spiritual protection, lasting peace and name.",
    18: "Spiritual Conflict — Danger from hidden foes and deception, demands vigilance.",
    19: "The Prince of Heaven — Extremely fortunate, victory, light, supreme success.",
    20: "The Awakening — Call to duty, strategic re-evaluation, renewal of ambitions.",
    21: "The Crown of the Magi — Glorious achievement, elevation after steady perseverance.",
    22: "The Master Builder — Enormous potential, transforming vast dreams into physical reality.",
    23: "The Royal Star of the Lion — Highly auspicious, success in enterprise and diplomacy.",
    24: "Fortunate Union — Support from patrons, steady monetary security, harmonious partnership.",
    25: "Wisdom through Experience — Analytical mind, gains after overcoming early struggles.",
    26: "Karmic Partnerships — Warning against hazardous joint liabilities, needs self-reliance.",
    27: "The Sceptre — High intellectual leadership, authority in writing, consulting, and command.",
    28: "The Trusting Heart — Warning against blind trust in business; legal scrutiny required.",
    29: "Uncertainty & Grace — Spiritual depth, fluctuating friendships, triumph through faith.",
    30: "The Contemplative Mind — Intellectual brilliance, philosophical insight, quiet victory.",
    31: "The Solitary Thinker — Self-contained intellectual capacity, independent wealth creation.",
    32: "The Winged Messenger — Commercial prowess, powerful international or public connections.",
    33: "The Master Teacher — Universal benevolence, high guidance, exceptional honor.",
    34: "Practical Wisdom — Hard work crowned with enduring financial stability.",
    35: "Harmonious Ventures — Cooperative enterprise, steady progressive climb.",
    36: "Authority through Labor — Victory achieved through sheer perseverance and stamina.",
    37: "The Royal Alliance — Superb fortune in business, love, and partnership.",
    38: "Diplomatic Acumen — Navigating conflicting factions with tact and insight.",
    39: "Dynamic Speech — Eloquent persuasion, literary and public recognition.",
    40: "The Fortress — Security, structured routine, slow but solid progress.",
    41: "The Sovereign Key — Leadership, executive mastery, overcoming severe bottlenecks.",
    42: "The Peaceful Haven — Household contentment, artistic success, gentle prosperity.",
    43: "Unconventional Path — Sudden pivots, breakthroughs against conventional odds.",
    44: "Double Mastery — Heavy responsibility paired with enormous industrial execution.",
    45: "The Adventurer — Commercial travel, international networking, rapid trade gains.",
    46: "The Crown of Prosperity — High popularity, luxury status, universal goodwill."
}


def reduce_to_single_digit(num: int, preserve_master: bool = False) -> int:
    """Reduce integer to single digit 1-9 (or keep 11, 22, 33 if preserve_master is True)."""
    while num > 9:
        if preserve_master and num in [11, 22, 33]:
            return num
        num = sum(int(d) for d in str(num))
    return num


@dataclass
class NumerologyProfile:
    full_name: str
    birth_date: date
    query_date: date
    mulank: int                         # Birth / Psychic Number (1-9)
    mulank_ruler: str
    bhagyank: int                       # Life Path / Destiny Number (1-9)
    bhagyank_ruler: str
    chaldean_name_compound: int         # Compound Name Number
    chaldean_name_single: int           # Reduced Name Number
    chaldean_vibration_meaning: str
    pythagorean_name_single: int
    name_compatibility_status: str     # Harmonious, Moderate, Discordant
    personal_year: int                  # Personal Year at query date
    personal_year_theme: str
    personal_month: int
    personal_day: int
    lucky_numbers: List[int]
    lucky_days: List[str]
    lucky_colors: List[str]
    inimical_numbers: List[int]
    query_timing_verdict: str
    numerological_upayas: List[str]


class NumerologyEngine:
    """Calculates comprehensive numerological parameters and answers current situation questions."""

    @classmethod
    def calculate_chaldean_name(cls, name: str) -> Tuple[int, int]:
        """Calculates Chaldean compound and reduced single-digit name number."""
        clean_name = "".join(ch.upper() for ch in name if ch.isalpha())
        compound = sum(CHALDEAN_MAP.get(ch, 0) for ch in clean_name)
        single = reduce_to_single_digit(compound)
        return compound, single

    @classmethod
    def calculate_namank(cls, name: str) -> Dict[str, Any]:
        """Calculates Chaldean compound, single digit, and planetary ruler for any name."""
        comp, single = cls.calculate_chaldean_name(name)
        ruler = NUMBER_RULERS.get(single, {}).get("planet", "Sun (Surya)")
        nature = NUMBER_RULERS.get(single, {}).get("nature", "Dynamic")
        return {
            "chaldean_compound": comp,
            "chaldean_single": single,
            "ruling_planet": ruler,
            "traits": nature
        }

    @classmethod
    def calculate_pythagorean_name(cls, name: str) -> int:
        """Calculates Pythagorean reduced single-digit name number."""
        clean_name = "".join(ch.upper() for ch in name if ch.isalpha())
        total = sum(PYTHAGOREAN_MAP.get(ch, 0) for ch in clean_name)
        return reduce_to_single_digit(total)

    @classmethod
    def calculate_personal_cycles(
        cls,
        birth_date: date,
        query_date: date
    ) -> Tuple[int, int, int]:
        """
        Personal Year = Birth Day + Birth Month + Current Year reduced to single digit.
        Personal Month = Personal Year + Current Month reduced to single digit.
        Personal Day = Personal Month + Current Day reduced to single digit.
        """
        py_raw = birth_date.day + birth_date.month + query_date.year
        personal_year = reduce_to_single_digit(py_raw)

        pm_raw = personal_year + query_date.month
        personal_month = reduce_to_single_digit(pm_raw)

        pd_raw = personal_month + query_date.day
        personal_day = reduce_to_single_digit(pd_raw)

        return personal_year, personal_month, personal_day

    @classmethod
    def evaluate(
        cls,
        name: str,
        birth_date: date,
        query_date: date,
        query_category: str
    ) -> NumerologyProfile:
        """
        Generates full numerological analysis and evaluates question alignment at query date.
        """
        # 1. Mulank (Birth / Psychic Number)
        mulank = reduce_to_single_digit(birth_date.day)
        mulank_ruler = NUMBER_RULERS[mulank]["planet"]

        # 2. Bhagyank (Destiny Number)
        dob_sum = birth_date.day + birth_date.month + birth_date.year
        bhagyank = reduce_to_single_digit(dob_sum)
        bhagyank_ruler = NUMBER_RULERS[bhagyank]["planet"]

        # 3. Name Numbers
        ch_comp, ch_single = cls.calculate_chaldean_name(name)
        py_single = cls.calculate_pythagorean_name(name)
        vibration_meaning = CHALDEAN_COMPOUNDS.get(
            ch_comp,
            f"Compound {ch_comp} reduces to {ch_single} ({NUMBER_RULERS[ch_single]['planet']}). Brings energy of expansion."
        )

        # 4. Name Compatibility
        m_friends = NUMBER_RELATIONS[mulank]["friendly"]
        b_friends = NUMBER_RELATIONS[bhagyank]["friendly"]
        if ch_single in m_friends and ch_single in b_friends:
            comp_status = "EXCELLENT SYNERGY (Triple Harmony between Name, Birth Date, and Life Path)"
        elif ch_single in m_friends or ch_single in b_friends:
            comp_status = "GOOD / MODERATE HARMONY (Favorable alignment with key planetary vibrations)"
        else:
            comp_status = "DISCORDANT VIBRATION (Minor spelling calibration recommended for peak fortune)"

        # 5. Personal Cycles at Query Date
        py, pm, pd = cls.calculate_personal_cycles(birth_date, query_date)

        py_themes = {
            1: "Personal Year 1: Initiation, New Horizons, Self-Reliance, Major Career Pivots",
            2: "Personal Year 2: Collaboration, Diplomacy, Relationships, Patience & Incubation",
            3: "Personal Year 3: Creative Expansion, Recognition, Public Impact, Financial Multiplication",
            4: "Personal Year 4: Foundation Building, Rigorous Discipline, Organizational Structure",
            5: "Personal Year 5: Dynamic Transformation, Relocation, High Velocity Changes, Travel",
            6: "Personal Year 6: Domestic Commitments, Marriage, Property Acquisition, Family Duties",
            7: "Personal Year 7: Deep Introspection, Research, Spiritual Realignment, Wise Caution",
            8: "Personal Year 8: Executive Authority, Massive Material Attainment, Karmic Harvest",
            9: "Personal Year 9: Culmination, Closure of Obsolete Chapters, Global Fulfillment"
        }
        personal_year_theme = py_themes[py]

        # 6. Query Timing Verdict
        cat_lower = query_category.lower()
        if any(w in cat_lower for w in ["job", "career", "promotion", "business"]):
            if py in [1, 3, 5, 8]:
                timing_verdict = f"HIGHLY AUSPICIOUS TIMING! Running Personal Year {py} which directly triggers career elevation and commercial breakthrough."
            elif py in [4, 7]:
                timing_verdict = f"STABILIZATION PHASE. Personal Year {py} requires meticulous groundwork and patience; breakthroughs materialize in the second half of the year."
            else:
                timing_verdict = f"BALANCED CYCLE. Personal Year {py} encourages collaborative alliances and strategic preparation."
        elif any(w in cat_lower for w in ["marriage", "relationship", "spouse"]):
            if py in [2, 6]:
                timing_verdict = f"SUPREMELY FAVORABLE FOR MATRIMONY! Personal Year {py} is the universal year of unions, domestic bliss, and sacred partnerships."
            elif py in [1, 3, 5]:
                timing_verdict = f"FAVORABLE WINDOW. New social circles and romantic connections are highly active this cycle."
            else:
                timing_verdict = f"TRANSITIONAL CYCLE. Focus on mutual understanding and clearing past emotional baggage."
        elif any(w in cat_lower for w in ["property", "land", "real estate"]):
            if py in [4, 6, 8]:
                timing_verdict = f"GOLDEN CYCLE FOR ASSET ACQUISITION! Personal Year {py} strongly supports land, brick-and-mortar investments, and property deals."
            else:
                timing_verdict = f"PROCEED WITH DUE DILIGENCE. Verify documentation thoroughly before closing transactions."
        elif any(w in cat_lower for w in ["foreign", "travel", "visa"]):
            if py in [1, 3, 5, 9]:
                timing_verdict = f"RAPID TRAVEL & VISA SUCCESS! Personal Year {py} vibrates with border crossings, foreign postings, and international gains."
            else:
                timing_verdict = f"MODERATE PACE. Prepare visa dossiers systematically; expect approval in the upcoming quarter."
        else:
            timing_verdict = f"Personal Year {py} brings constructive unfolding. Align critical decisions with lucky dates ({', '.join(map(str, LUCKY_ATTRIBUTES[mulank]['dates']))})."

        # 7. Lucky Attributes & Inimical Numbers
        lucky_attr = LUCKY_ATTRIBUTES[mulank]
        inimical = NUMBER_RELATIONS[mulank]["inimical"]

        # 8. Numerological Upayas
        numerological_upayas = [
            f"Sign important contracts, submit vital applications, and schedule crucial interviews on your lucky dates: {', '.join(map(str, lucky_attr['dates']))}.",
            f"Incorporate your lucky colors ({', '.join(lucky_attr['colors'])}) in professional meetings, interviews, or your daily attire.",
            f"Avoid finalizing high-stakes financial pacts on inimical numbers: {', '.join(map(str, inimical))}.",
            f"Use a blue ink or golden metallic pen for your daily signature; sign at an upward slant of 15° to activate progressive growth energy.",
            f"Keep a 3x3 square grid containing your favorable vibration numbers on your work desk."
        ]

        return NumerologyProfile(
            full_name=name,
            birth_date=birth_date,
            query_date=query_date,
            mulank=mulank,
            mulank_ruler=mulank_ruler,
            bhagyank=bhagyank,
            bhagyank_ruler=bhagyank_ruler,
            chaldean_name_compound=ch_comp,
            chaldean_name_single=ch_single,
            chaldean_vibration_meaning=vibration_meaning,
            pythagorean_name_single=py_single,
            name_compatibility_status=comp_status,
            personal_year=py,
            personal_year_theme=personal_year_theme,
            personal_month=pm,
            personal_day=pd,
            lucky_numbers=lucky_attr["dates"],
            lucky_days=lucky_attr["days"],
            lucky_colors=lucky_attr["colors"],
            inimical_numbers=inimical,
            query_timing_verdict=timing_verdict,
            numerological_upayas=numerological_upayas
        )
