"""
Astrological constants: Zodiac signs, Nakshatras, Dignities, Vimshottari parameters, and Shodashavarga definitions.
"""
from typing import Dict, List, Tuple

# 12 Zodiac Signs
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

ZODIAC_SANSKRIT = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanus", "Makara", "Kumbha", "Meena"
]

# Sign Rulers (Classical 7 planets)
SIGN_LORDS = [
    "Mars",     # Aries
    "Venus",    # Taurus
    "Mercury",  # Gemini
    "Moon",     # Cancer
    "Sun",      # Leo
    "Mercury",  # Virgo
    "Venus",    # Libra
    "Mars",     # Scorpio
    "Jupiter",  # Sagittarius
    "Saturn",   # Capricorn
    "Saturn",   # Aquarius
    "Jupiter"   # Pisces
]

# Exaltation & Debilitation signs and deep degrees
# Planet: (Exaltation_Sign_Index, Exaltation_Degree, Debilitation_Sign_Index, Debilitation_Degree)
PLANET_DIGNITY_DEGREES = {
    "Sun": (0, 10.0, 6, 10.0),       # Exalted in Aries 10°, Debilitated in Libra 10°
    "Moon": (1, 3.0, 7, 3.0),        # Exalted in Taurus 3°, Debilitated in Scorpio 3°
    "Mars": (9, 28.0, 3, 28.0),      # Exalted in Capricorn 28°, Debilitated in Cancer 28°
    "Mercury": (5, 15.0, 11, 15.0),  # Exalted in Virgo 15°, Debilitated in Pisces 15°
    "Jupiter": (3, 5.0, 9, 5.0),     # Exalted in Cancer 5°, Debilitated in Capricorn 5°
    "Venus": (11, 27.0, 5, 27.0),    # Exalted in Pisces 27°, Debilitated in Virgo 27°
    "Saturn": (6, 20.0, 0, 20.0),    # Exalted in Libra 20°, Debilitated in Aries 20°
    "Rahu": (1, 20.0, 7, 20.0),      # Exalted in Taurus, Debilitated in Scorpio (some say Gemini/Sagittarius)
    "Ketu": (7, 20.0, 1, 20.0),      # Exalted in Scorpio, Debilitated in Taurus
}

# 27 Nakshatras: Name, Lord, Starting Degree
NAKSHATRAS = [
    {"name": "Ashwini", "lord": "Ketu", "deity": "Ashwini Kumaras", "syllables": ["Chu", "Che", "Cho", "La"]},
    {"name": "Bharani", "lord": "Venus", "deity": "Yama", "syllables": ["Lee", "Lu", "Le", "Lo"]},
    {"name": "Krittika", "lord": "Sun", "deity": "Agni", "syllables": ["A", "Ee", "U", "Ea"]},
    {"name": "Rohini", "lord": "Moon", "deity": "Brahma / Prajapati", "syllables": ["O", "Va", "Vi", "Vu"]},
    {"name": "Mrigashira", "lord": "Mars", "deity": "Soma", "syllables": ["Ve", "Vo", "Ka", "Kee"]},
    {"name": "Ardra", "lord": "Rahu", "deity": "Rudra", "syllables": ["Ku", "Gha", "Ng", "Chha"]},
    {"name": "Punarvasu", "lord": "Jupiter", "deity": "Aditi", "syllables": ["Ke", "Ko", "Ha", "Hee"]},
    {"name": "Pushya", "lord": "Saturn", "deity": "Brihaspati", "syllables": ["Hu", "He", "Ho", "Da"]},
    {"name": "Ashlesha", "lord": "Mercury", "deity": "Nagas / Sarpas", "syllables": ["Dee", "Du", "De", "Do"]},
    {"name": "Magha", "lord": "Ketu", "deity": "Pitrus", "syllables": ["Ma", "Mee", "Mu", "Me"]},
    {"name": "Purva Phalguni", "lord": "Venus", "deity": "Bhaga", "syllables": ["Mo", "Ta", "Tee", "Tu"]},
    {"name": "Uttara Phalguni", "lord": "Sun", "deity": "Aryaman", "syllables": ["Te", "To", "Paa", "Pee"]},
    {"name": "Hasta", "lord": "Moon", "deity": "Savitr / Surya", "syllables": ["Pu", "Sha", "Na", "Tha"]},
    {"name": "Chitra", "lord": "Mars", "deity": "Tvashtar / Vishvakarma", "syllables": ["Pe", "Po", "Ra", "Ree"]},
    {"name": "Swati", "lord": "Rahu", "deity": "Vayu", "syllables": ["Ru", "Re", "Ro", "Taa"]},
    {"name": "Vishakha", "lord": "Jupiter", "deity": "Indragni", "syllables": ["Tee", "Tue", "Te", "To"]},
    {"name": "Anuradha", "lord": "Saturn", "deity": "Mitra", "syllables": ["Na", "Nee", "Nu", "Ne"]},
    {"name": "Jyeshtha", "lord": "Mercury", "deity": "Indra", "syllables": ["No", "Ya", "Yee", "Yu"]},
    {"name": "Moola", "lord": "Ketu", "deity": "Nirriti", "syllables": ["Ye", "Yo", "Bha", "Bhee"]},
    {"name": "Purva Ashadha", "lord": "Venus", "deity": "Apas (Water God)", "syllables": ["Bhu", "Dha", "Pha", "Dha"]},
    {"name": "Uttara Ashadha", "lord": "Sun", "deity": "Vishvadevas", "syllables": ["Bhe", "Bho", "Ja", "Jee"]},
    {"name": "Shravana", "lord": "Moon", "deity": "Vishnu", "syllables": ["Khee", "Khu", "Khe", "Kho"]},
    {"name": "Dhanishta", "lord": "Mars", "deity": "Ashta Vasus", "syllables": ["Ga", "Gee", "Gu", "Ge"]},
    {"name": "Shatabhisha", "lord": "Rahu", "deity": "Varuna", "syllables": ["Go", "Sa", "See", "Su"]},
    {"name": "Purva Bhadrapada", "lord": "Jupiter", "deity": "Aja Ekapada", "syllables": ["Se", "So", "Dha", "Dhee"]},
    {"name": "Uttara Bhadrapada", "lord": "Saturn", "deity": "Ahirbudhnya", "syllables": ["Du", "Shya", "Jna", "Tha"]},
    {"name": "Revati", "lord": "Mercury", "deity": "Pushan", "syllables": ["De", "Do", "Chaa", "Chee"]}
]

# Vimshottari Dasha Order & Durations (in Solar Years)
VIMSHOTTARI_ORDER = [
    ("Ketu", 7.0),
    ("Venus", 20.0),
    ("Sun", 6.0),
    ("Moon", 10.0),
    ("Mars", 7.0),
    ("Rahu", 18.0),
    ("Jupiter", 16.0),
    ("Saturn", 19.0),
    ("Mercury", 17.0)
]

VIMSHOTTARI_YEARS = {lord: yrs for lord, yrs in VIMSHOTTARI_ORDER}
TOTAL_VIMSHOTTARI_YEARS = 120.0

# Shodashavarga (16 Divisional Charts) Definitions from Brihat Parasara Hora Sastra (BPHS)
# division: (Name, Sanskrit_Name, Purpose, Vimsopaka_Points_out_of_20)
SHODASHAVARGA_INFO = {
    1: ("Rasi", "D1 - Rasi Chart", "Physical body, general existence, life path, constitution", 3.5),
    2: ("Hora", "D2 - Hora", "Wealth, finances, prosperity, speech, family assets", 1.0),
    3: ("Drekkana", "D3 - Drekkana", "Siblings, courage, vitality, energy, initiatives", 1.0),
    4: ("Chaturthamsa", "D4 - Chaturthamsa", "Fixed assets, real estate, home, conveyances, fortune", 0.5),
    7: ("Saptamsa", "D7 - Saptamsa", "Children, progeny, lineage, creative potential", 0.5),
    9: ("Navamsa", "D9 - Navamsa", "Dharma, marriage, spouse, soul purpose, internal strength", 3.0),
    10: ("Dasamsa", "D10 - Dasamsa", "Career, profession, worldly success, power, reputation", 0.5),
    12: ("Dwadasamsa", "D12 - Dwadasamsa", "Parents, ancestry, heritage, past karma from parents", 0.5),
    16: ("Shodashamsa", "D16 - Kalamsa", "Vehicles, luxuries, general comforts, conveyance safety", 2.0),
    20: ("Vimsamsa", "D20 - Vimsamsa", "Spiritual devotion, Upasana, meditation, religious progress", 0.5),
    24: ("Chaturvimsamsa", "D24 - Siddhamsa", "Higher learning, intellect, education, academic skill", 0.5),
    27: ("Saptavimsamsa", "D27 - Bhamsha", "Subconscious strengths, physical stamina, weaknesses", 0.5),
    30: ("Trimsamsa", "D30 - Trimsamsa", "Misfortunes, health hazards, character blemishes, doshas", 1.0),
    40: ("Khavedamsa", "D40 - Khavedamsa", "Auspicious and inauspicious karmas, emotional well-being", 0.5),
    45: ("Akshavedamsa", "D45 - Akshavedamsa", "Character purity, moral integrity, subtle karma", 0.5),
    60: ("Shashtiamsa", "D60 - Shashtiamsa", "Past life karma, root causes of destiny, overall verification", 4.0)
}

# Natural Relationships between Planets (Naisargika Sambandha)
NATURAL_RELATIONSHIPS = {
    "Sun": {
        "friends": ["Moon", "Mars", "Jupiter"],
        "neutrals": ["Mercury"],
        "enemies": ["Venus", "Saturn", "Rahu", "Ketu"]
    },
    "Moon": {
        "friends": ["Sun", "Mercury"],
        "neutrals": ["Mars", "Jupiter", "Venus", "Saturn"],
        "enemies": ["Rahu", "Ketu"]
    },
    "Mars": {
        "friends": ["Sun", "Moon", "Jupiter"],
        "neutrals": ["Venus", "Saturn"],
        "enemies": ["Mercury", "Rahu", "Ketu"]
    },
    "Mercury": {
        "friends": ["Sun", "Venus"],
        "neutrals": ["Mars", "Jupiter", "Saturn"],
        "enemies": ["Moon"]
    },
    "Jupiter": {
        "friends": ["Sun", "Moon", "Mars"],
        "neutrals": ["Saturn"],
        "enemies": ["Mercury", "Venus"]
    },
    "Venus": {
        "friends": ["Mercury", "Saturn"],
        "neutrals": ["Mars", "Jupiter"],
        "enemies": ["Sun", "Moon"]
    },
    "Saturn": {
        "friends": ["Mercury", "Venus"],
        "neutrals": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"]
    },
    "Rahu": {
        "friends": ["Venus", "Saturn", "Mercury"],
        "neutrals": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"]
    },
    "Ketu": {
        "friends": ["Mars", "Jupiter"],
        "neutrals": ["Mercury", "Venus", "Saturn"],
        "enemies": ["Sun", "Moon"]
    }
}
