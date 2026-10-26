"""
Name Tuning & General-Purpose Alternate Name Suggestion Engine.
Implements:
1. Present Name Numerological & Astrological Diagnostic:
   - Full Chaldean compound, Pythagorean single, and root vibration.
   - Analysis of karmic obstacles or friction in the current spelling.
2. Minor Spelling Calibrations (Social / Signature / Business Card use):
   - Subtle letter additions/adjustments that keep pronunciation intact while shifting
     the compound to a Royal Star of Fortune (e.g. 19, 23, 24, 32, 37, 41, 42, 46).
3. Vedic Janma Nakshatra Nama-Akshara Suggestions:
   - Generates auspicious classical and modern names starting with the exact Vedic syllable
     governed by the native's Moon Nakshatra and Pada.
4. Non-Legal Adoption Guidelines:
   - Practical protocol to activate name vibration for general/social/professional purposes
     without altering legal government records (Passport, PAN, Aadhaar, Bank accounts).
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from app.models.astrological import Kundali
from app.core.constants import NAKSHATRAS
from app.engines.numerology_engine import (
    CHALDEAN_MAP,
    CHALDEAN_COMPOUNDS,
    NUMBER_RELATIONS,
    NUMBER_RULERS,
    reduce_to_single_digit
)


@dataclass
class NameCalibrationOption:
    calibrated_name: str
    chaldean_compound: int
    chaldean_single: int
    vibration_title: str
    vibration_benefit: str
    recommended_usage: str              # "Business cards, LinkedIn, Email signature, Creative bylines"


@dataclass
class VedicNakshatraNameOption:
    starting_syllable: str
    suggested_name: str
    meaning: str
    chaldean_compound: int
    chaldean_single: int
    planetary_ruler: str


@dataclass
class NameTuningDossier:
    present_name: str
    present_chaldean_compound: int
    present_chaldean_single: int
    present_compound_meaning: str
    present_name_status: str            # "Challenging / Obstacle Prone", "Moderate", "Harmonious"
    compatibility_with_birth_numbers: str
    spelling_calibration_suggestions: List[NameCalibrationOption]
    vedic_nakshatra_syllable: str
    vedic_nakshatra_name_options: List[VedicNakshatraNameOption]
    non_legal_adoption_guidelines: List[str]


# Curated catalog of auspicious Vedic & Modern names indexed by Nakshatra Syllables
NAKSHATRA_SYLLABLE_NAMES: Dict[str, List[Tuple[str, str]]] = {
    # Ashwini
    "Chu": [("Chudan", "Crest Jewel"), ("Chunilal", "Precious Stone")],
    "Che": [("Chetan", "Conscious Vitality"), ("Chetas", "Mind & Spirit")],
    "Cho": [("Chokalingam", "Auspicious Shiva"), ("Chola", "Dynasty Leader")],
    "La": [("Lalit", "Graceful & Attractive"), ("Lavanya", "Elegance"), ("Lakshman", "Auspicious Brother")],
    # Bharani
    "Lee": [("Leela", "Divine Play"), ("Leeladhar", "Lord Vishnu")],
    "Lu": [("Lokesh", "Lord of the World"), ("Loknath", "Protector of People")],
    "Le": [("Lekh", "Destiny / Sacred Writing"), ("Lekhraj", "Leader of Destiny")],
    "Lo": [("Lokendra", "Universal Leader"), ("Lohit", "Red Radiance / Mars")],
    # Krittika
    "A": [("Aditya", "Sun God / Radiant"), ("Abhay", "Fearless"), ("Anand", "Pure Bliss"), ("Aarav", "Peaceful Sound")],
    "Ee": [("Eeshan", "Lord Shiva / North-East"), ("Eshwar", "Supreme Divinity")],
    "U": [("Uday", "Rising Sun"), ("Utkarsh", "Prosperity & Rise"), ("Umang", "Enthusiasm")],
    "Ea": [("Ekant", "Tranquil Focus"), ("Ekalavya", "Devoted Learner")],
    # Rohini
    "O": [("Omkar", "Primordial Sound"), ("Ojas", "Vital Spiritual Energy")],
    "Va": [("Varun", "Cosmic Lord of Waters"), ("Vardhan", "Bringer of Growth"), ("Vasudev", "Lord Krishna")],
    "Vi": [("Vijay", "Victory"), ("Vikram", "Valorous Leader"), ("Vishal", "Immense & Grand"), ("Vivek", "Discernment")],
    "Vu": [("Vrishabh", "Strength & Steadiness"), ("Vrajesh", "Lord of Vraja")],
    # Mrigashira
    "Ve": [("Vedant", "Ultimate Wisdom of the Vedas"), ("Ved", "Sacred Knowledge"), ("Veer", "Brave Leader")],
    "Vo": [("Vomesh", "Lord of the Skies"), ("Voshit", "Composed Mind")],
    "Ka": [("Kartik", "Victorious Commander"), ("Kailash", "Abode of Shiva"), ("Karan", "Noble Benefactor")],
    "Kee": [("Ketan", "Banner of Honor"), ("Keerthi", "Eternal Fame"), ("Keshava", "Lord Vishnu")],
    # Ardra
    "Ku": [("Kushal", "Skilled & Prosperous"), ("Kuldeep", "Light of the Lineage")],
    "Gha": [("Ghanashyam", "Lord Krishna"), ("Ghanshyam", "Bringer of Rain")],
    "Ng": [("Navin", "Fresh & Progressive"), ("Nayan", "Guiding Eye")],
    "Chha": [("Chhatrapati", "Sovereign Ruler"), ("Chhagan", "Gentle Soul")],
    # Punarvasu
    "Ke": [("Keval", "Pure & Absolute"), ("Kedar", "Lord Shiva of Himalayas")],
    "Ko": [("Komal", "Gentle Grace"), ("Kovid", "Wise Scholar")],
    "Ha": [("Harish", "Lord Shiva / Vishnu"), ("Harsh", "Joy & Radiance"), ("Hari", "Preserver of Universe")],
    "Hee": [("Heer", "Diamond"), ("Hemant", "Golden Winter / Prosperity")],
    # Pushya
    "Hu": [("Hrishikesh", "Master of Senses / Vishnu"), ("Hulash", "Joyful Celebration")],
    "He": [("Hemendra", "Lord of Gold"), ("Hemant", "Auspicious Season")],
    "Ho": [("Hotravahan", "Sacred Agni"), ("Hoshang", "Noble Character")],
    "Da": [("Damodar", "Lord Krishna"), ("Darshan", "Divine Vision"), ("Dayanand", "Joy in Compassion")],
    # Ashlesha
    "Dee": [("Deepak", "Lamp of Illumination"), ("Devesh", "Lord of Gods")],
    "Du": [("Durgadas", "Protector Servant of Durga"), ("Dushyant", "Royal Hero")],
    "De": [("Devan", "Divine Ruler"), ("Devrat", "Spiritual Vow")],
    "Do": [("Dron", "Master Archer Teacher"), ("Doshi", "Keen Mind")],
    # Magha
    "Ma": [("Madhav", "Sweet Lord Krishna"), ("Manish", "Lord of the Mind"), ("Mayur", "Peacock / Grace")],
    "Mee": [("Mehul", "Auspicious Rain"), ("Meeran", "Saintly Leader")],
    "Mu": [("Mukesh", "Lord Shiva / Conquering Illusion"), ("Mukul", "Blossoming Soul")],
    "Me": [("Mihir", "Radiant Sun"), ("Medhansh", "Born with High Intellect")],
    # Purva Phalguni
    "Mo": [("Mohan", "Charming & Magnetic"), ("Mohit", "Enchanted Soul")],
    "Ta": [("Tanmay", "Engrossed in Meditation"), ("Tarun", "Ever Youthful")],
    "Tee": [("Tejas", "Luster, Radiance & Power"), ("Teerth", "Sacred Waters")],
    "Tu": [("Tushar", "Pure Dew / Snow"), ("Tulsidas", "Devoted Soul")],
    # Uttara Phalguni
    "Te": [("Tejesh", "Lord of Bright Radiance"), ("Tejvir", "Heroic Light")],
    "To": [("Toshit", "Satisfied & Joyous"), ("Toran", "Auspicious Archway")],
    "Paa": [("Parth", "Arjuna the Victor"), ("Pavan", "Sacred Breeze / Hanuman"), ("Pranav", "Sacred Omkar")],
    "Pee": [("Peeyush", "Nectar of Immortality"), ("Peetambar", "Golden Silk")],
    # Hasta
    "Pu": [("Puneet", "Pure & Sacred"), ("Pushkar", "Lotus Flower / Sacred Lake"), ("Punit", "Sanctified")],
    "Sha": [("Shashank", "Lord Moon"), ("Sharad", "Auspicious Autumn"), ("Shailesh", "Lord of the Mountain")],
    "Na": [("Nakul", "Graceful & Attractive"), ("Navin", "Modern Innovator"), ("Naveen", "Always Fresh")],
    "Tha": [("Thaman", "Valuable Asset"), ("Thavanesh", "Lord Shiva")],
    # Chitra
    "Pe": [("Peshan", "Honorable"), ("Perumal", "Lord Vishnu")],
    "Po": [("Poojan", "Worshipful Soul"), ("Poornesh", "Lord of Fulfillment")],
    "Ra": [("Rahul", "Conqueror of Miseries"), ("Rajan", "King / Leader"), ("Rajiv", "Blue Lotus Flower"), ("Ravi", "The Sun")],
    "Ree": [("Ritesh", "Lord of Truth / Seasons"), ("Rishi", "Sage of Divine Sight")],
    # Swati
    "Ru": [("Rudra", "Mighty Lord Shiva"), ("Rupesh", "Lord of Beauty"), ("Rustom", "Valorous Warrior")],
    "Re": [("Revant", "Son of Surya / Master of Horses"), ("Reyansh", "Ray of Divine Light")],
    "Ro": [("Rohan", "Ascending to Greatness"), ("Rohit", "First Ray of Dawn")],
    "Taa": [("Tarak", "Star / Deliverer of Souls"), ("Tapas", "Spiritual Discipline")],
    # Vishakha
    "Tue": [("Tulik", "Creative Brush"), ("Tushaar", "Fine Mist")],
    # Anuradha
    "Nee": [("Neel", "Deep Blue / Sky"), ("Neeraj", "Lotus Blooming in Water"), ("Nikhil", "Complete & Whole")],
    "Nu": [("Nupur", "Graceful Footsteps"), ("Nutan", "New Dawn")],
    # Jyeshtha
    "No": [("Noman", "Honored"), ("Noshir", "Courageous")],
    "Ya": [("Yash", "Glory, Fame & Honor"), ("Yatin", "Devoted Ascetic"), ("Yashwant", "Possessor of Glory")],
    "Yee": [("Yashodhar", "Holder of Fame"), ("Yuvraj", "Crown Prince")],
    "Yu": [("Yuvraj", "Heir to the Throne"), ("Yugesh", "Lord of the Era")],
    # Moola
    "Ye": [("Yetharth", "Truth / Reality"), ("Yenesh", "Lord of Prosperity")],
    "Yo": [("Yogesh", "Master of Yoga"), ("Yogendra", "Lord of Meditation")],
    "Bha": [("Bharat", "Universal King / Protector"), ("Bhavesh", "Lord of the World"), ("Bhupesh", "Lord of the Earth")],
    "Bhee": [("Bheem", "Towering Strength"), ("Bheeshma", "Unshakeable Vow")],
    # Purva Ashadha
    "Bhu": [("Bhuvnesh", "Lord of the Cosmos"), ("Bhupal", "Protector of People")],
    "Dha": [("Dharmesh", "Lord of Righteousness"), ("Dhananjay", "Arjuna the Wealth Winner")],
    "Pha": [("Phalguna", "Born under Fortunate Star"), ("Phaneendra", "Lord of Serpent Energy")],
    # Uttara Ashadha
    "Bhe": [("Bheshaj", "Lord Vishnu the Healer"), ("Bheru", "Courageous")],
    "Bho": [("Bhoj", "Generous King"), ("Bhola", "Innocent Shiva")],
    "Ja": [("Jayant", "Victorious Conqueror"), ("Jagdish", "Lord of the Universe"), ("Janak", "Father / Wise King")],
    "Jee": [("Jeevan", "Life & Vitality"), ("Jeetesh", "Lord of Victory")],
    # Shravana
    "Khee": [("Khitish", "Lord of the Earth"), ("Khemraj", "Protector of Welfare")],
    "Khu": [("Khushal", "Prosperous & Happy"), ("Khursheed", "Radiant Sun")],
    "Khe": [("Khemchand", "Moon of Welfare"), ("Khetram", "Protector of Sacred Land")],
    "Kho": [("Khotan", "Noble Traveler"), ("Khomen", "Courteous Soul")],
    # Dhanishta
    "Ga": [("Ganesh", "Lord of New Beginnings"), ("Gaurav", "Prestige & Honor"), ("Girish", "Lord of the Mountain")],
    "Gee": [("Geet", "Melodious Song"), ("Geetesh", "Lord of Sacred Hymns")],
    "Gu": [("Gulshan", "Garden of Blossoms"), ("Guneet", "Full of Virtues")],
    "Ge": [("Geyan", "Sacred Knowledge"), ("Genesh", "Master Leader")],
    # Shatabhisha
    "Go": [("Gopal", "Protector of Cows / Krishna"), ("Govind", "Seeker of Wisdom"), ("Gokul", "Sacred Abode")],
    "Sa": [("Sanjay", "Triumphant"), ("Samar", "Courageous"), ("Samarth", "Capable & Powerful"), ("Saurabh", "Fragrance of Glory")],
    "See": [("Seetaram", "Divine Couple"), ("Seemanth", "Crown of Prosperity")],
    "Su": [("Suresh", "Ruler of the Gods"), ("Sumit", "Well-measured & Wise"), ("Suraj", "The Glorious Sun")],
    # Purva Bhadrapada
    "Se": [("Setu", "Bridge of Harmony"), ("Sevagan", "Selfless Server")],
    "So": [("Sohan", "Good Looking & Gentle"), ("Somesh", "Lord of the Moon / Shiva")],
    # Uttara Bhadrapada
    "Du": [("Durgesh", "Lord of Fortresses"), ("Durvasa", "Powerful Sage")],
    "Shya": [("Shyam", "Beloved Dark-complexioned Krishna"), ("Shyamal", "Gentle Beauty")],
    "Jna": [("Jnanesh", "Lord of Supreme Knowledge"), ("Jnanadev", "Light of Wisdom")],
    # Revati
    "De": [("Dev", "Divine Being"), ("Deep", "Radiant Light"), ("Devansh", "Part of Divinity")],
    "Do": [("Dorai", "Chief / Noble"), ("Doreswamy", "Lordly Soul")],
    "Chaa": [("Charan", "Sacred Feet"), ("Chandan", "Fragrant Sandalwood"), ("Charit", "Noble Character")]
}


class NameTuningEngine:
    """Computes present name diagnostic and alternate name suggestions for non-legal use."""

    @classmethod
    def evaluate_name(
        cls,
        present_name: str,
        kundali: Kundali,
        mulank: int,
        bhagyank: int
    ) -> NameTuningDossier:
        """
        Diagnoses present name and provides minor spelling calibrations + Vedic Nakshatra names.
        """
        clean_name = "".join(ch.upper() for ch in present_name if ch.isalpha())
        compound = sum(CHALDEAN_MAP.get(ch, 0) for ch in clean_name)
        single = reduce_to_single_digit(compound)

        # Meaning of compound
        compound_meaning = CHALDEAN_COMPOUNDS.get(
            compound,
            f"Compound {compound} reduces to root {single} ({NUMBER_RULERS[single]['planet']})."
        )

        friendly_m = NUMBER_RELATIONS[mulank]["friendly"]
        inimical_m = NUMBER_RELATIONS[mulank]["inimical"]

        # Royal Compounds
        royal_compounds = [19, 23, 24, 27, 32, 33, 37, 41, 42, 45, 46, 50]

        # Diagnosis
        if compound in [16, 18, 26, 28, 29, 43, 44]:
            status = f"Challenging Compound {compound} (Prone to delays, blind trust breaches, or career friction)"
            compat = f"Single digit {single} clashes or under-delivers relative to your Mulank {mulank}."
        elif compound in royal_compounds:
            c_label = CHALDEAN_COMPOUNDS.get(compound, f"Royal Compound {compound}").split("—")[0].strip()
            status = f"Supremely Fortunate Royal Compound {compound} ({c_label})"
            compat = f"Possesses high cosmic vibration and natural fortune; perfectly synergistic with your destiny trajectory."
        elif single in friendly_m:
            status = f"Harmonious Vibration (Compound {compound} reduces to friendly {single})"
            compat = f"Harmonizes well with your Birth Number {mulank} ({NUMBER_RULERS[mulank]['planet'].split('(')[0]})."
        else:
            status = f"Moderate / Neutral Vibration (Compound {compound} -> {single})"
            compat = f"Neutral resonance; can be elevated to a Royal Star compound (23, 24, 32, 37, 41)."

        # -------------------------------------------------------------
        # 1. Spelling Calibrations of Present Name
        # -------------------------------------------------------------
        calibrations: List[NameCalibrationOption] = []
        target_royal_compounds = [19, 23, 24, 27, 32, 33, 37, 41, 42, 45, 46, 50]

        # Try subtle variations
        # Split words
        words = present_name.strip().split()
        candidate_names = []

        if len(words) == 1:
            w = words[0]
            candidate_names.extend([
                f"{w}a", f"{w}i", f"{w}r", f"A{w}", f"{w}h", f"{w}e", f"{w}s",
                f"{w[0]}{w}", f"Sri {w}", f"{w} Kumar"
            ])
        elif len(words) == 2:
            first, last = words[0], words[1]
            candidate_names.extend([
                f"{first} {last}a",
                f"{first}a {last}",
                f"{first} {last[0]}{last}",
                f"{first} {last}h",
                f"{first[0]}{first} {last}",
                f"{first} {last}i",
                f"{first} K {last}",
                f"{first} R {last}",
                f"{first} S {last}",
                f"{first} A {last}",
                f"{first} {last}aa",
                f"{first} {last}e"
            ])
        else:
            first, mid, last = words[0], words[1], words[2]
            candidate_names.extend([
                f"{first} {mid} {last}a",
                f"{first} {mid}a {last}",
                f"{first} {mid} {last}h",
                f"{first} {mid[0]} {last}",
                f"{first} {mid} {last}i",
                f"{first} {mid} {last}aa",
                f"{first}a {mid} {last}",
                f"{first} {mid} {last[0]}{last}"
            ])

        for cand in candidate_names:
            c_clean = "".join(ch.upper() for ch in cand if ch.isalpha())
            c_comp = sum(CHALDEAN_MAP.get(ch, 0) for ch in c_clean)
            c_sing = reduce_to_single_digit(c_comp)

            if c_comp in target_royal_compounds or (c_sing in friendly_m and c_comp not in [16, 18, 26, 28]):
                c_title = CHALDEAN_COMPOUNDS.get(c_comp, f"Fortunate Compound {c_comp}").split("—")[0].strip()
                c_benefit = CHALDEAN_COMPOUNDS.get(c_comp, "Bestows high fortune and commercial triumph.")
                calibrations.append(NameCalibrationOption(
                    calibrated_name=cand,
                    chaldean_compound=c_comp,
                    chaldean_single=c_sing,
                    vibration_title=c_title,
                    vibration_benefit=c_benefit,
                    recommended_usage="LinkedIn, Visiting Cards, Email Signature, Social Handles, Display Profiles"
                ))

        # Deduplicate
        seen_comps = set()
        unique_calibrations = []
        for cal in calibrations:
            if cal.chaldean_compound not in seen_comps:
                seen_comps.add(cal.chaldean_compound)
                unique_calibrations.append(cal)
            if len(unique_calibrations) >= 3:
                break

        # Fallback if no simple candidate matched
        if not unique_calibrations:
            for suffix in [" A", " K", " S", " R", "h"]:
                fb_name = f"{present_name}{suffix}"
                fb_clean = "".join(ch.upper() for ch in fb_name if ch.isalpha())
                fb_comp = sum(CHALDEAN_MAP.get(ch, 0) for ch in fb_clean)
                fb_sing = reduce_to_single_digit(fb_comp)
                if fb_comp not in [16, 18, 26, 28]:
                    fb_title = CHALDEAN_COMPOUNDS.get(fb_comp, f"Compound {fb_comp}").split("—")[0].strip()
                    fb_benefit = CHALDEAN_COMPOUNDS.get(fb_comp, "Bestows enhanced vitality and social charisma.")
                    unique_calibrations.append(NameCalibrationOption(
                        calibrated_name=fb_name,
                        chaldean_compound=fb_comp,
                        chaldean_single=fb_sing,
                        vibration_title=fb_title,
                        vibration_benefit=fb_benefit,
                        recommended_usage="Social platforms and communication bylines"
                    ))
                    break

        # -------------------------------------------------------------
        # 2. Vedic Nakshatra Nama-Akshara Names
        # -------------------------------------------------------------
        moon_pos = kundali.planets["Moon"]
        nak_idx = moon_pos.nakshatra_number
        pada = moon_pos.nakshatra_pada

        nak_data = NAKSHATRAS[nak_idx]
        syllables = nak_data.get("syllables", ["A", "Ra", "Sa", "Ka"])
        syl = syllables[min(pada - 1, len(syllables) - 1)]

        vedic_names: List[VedicNakshatraNameOption] = []
        available_list = NAKSHATRA_SYLLABLE_NAMES.get(syl, [("Aarav", "Peaceful & Auspicious"), ("Aditya", "Lord Sun")])

        for n_name, n_mean in available_list[:4]:
            n_clean = "".join(ch.upper() for ch in n_name if ch.isalpha())
            n_comp = sum(CHALDEAN_MAP.get(ch, 0) for ch in n_clean)
            n_sing = reduce_to_single_digit(n_comp)
            ruler = NUMBER_RULERS[n_sing]["planet"]

            vedic_names.append(VedicNakshatraNameOption(
                starting_syllable=syl,
                suggested_name=n_name,
                meaning=n_mean,
                chaldean_compound=n_comp,
                chaldean_single=n_sing,
                planetary_ruler=ruler
            ))

        # -------------------------------------------------------------
        # 3. Non-Legal Adoption Guidelines
        # -------------------------------------------------------------
        guidelines = [
            "NO GOVERNMENT GAZETTE OR LEGAL CHANGES REQUIRED: Keep your Passport, Aadhaar, PAN card, and Bank Accounts exactly as they are.",
            "DISPLAY / SOCIAL / PROFESSIONAL USAGE: Adopt the calibrated spelling on your LinkedIn profile, business visiting cards, email sign-offs, and social media.",
            "SIGNATURE RE-CALIBRATION: Begin signing your daily documents, notes, and registers with the calibrated spelling at a 15° upward slant in blue or gold ink.",
            "CALLING NAME REINFORCEMENT: Encourage colleagues, friends, and family to address you with the calibrated phonetic vibration.",
            "ALTAR / MEDITATION AFFIRMATION: Write your calibrated name 21 times in a notebook with red or green ink on Wednesday or Sunday mornings to imprint the vibration into your subconscious aura."
        ]

        return NameTuningDossier(
            present_name=present_name,
            present_chaldean_compound=compound,
            present_chaldean_single=single,
            present_compound_meaning=compound_meaning,
            present_name_status=status,
            compatibility_with_birth_numbers=compat,
            spelling_calibration_suggestions=unique_calibrations,
            vedic_nakshatra_syllable=syl,
            vedic_nakshatra_name_options=vedic_names,
            non_legal_adoption_guidelines=guidelines
        )
