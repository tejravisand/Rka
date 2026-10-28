"""
Panchanga & Muhurtha Computational Engine
==========================================
Comprehensive Vedic 5-Limb Calendar and Muhurtha Engine:
1. Five Limbs of Time (Pancha Anga):
   - Tithi (30 Lunar days: Shukla & Krishna Pakshas with elongation & deity)
   - Vara (Solar weekday, Sanskrit name & ruling planetary energy)
   - Nakshatra (27 Lunar mansions with Pada, Lord, Deity, Gana, Yoni, Nadi)
   - Yoga (27 Nirayana Sun + Moon Yogas: Vishkambha to Vaidhriti, Benefic/Malefic nature)
   - Karana (60 Half-tithis: 4 Fixed Sthira + 7 Repeating Chara with Vishti/Bhadra alerts)
2. Muhurtha Timing Engine:
   - Rahu Kaalam (Inauspicious window ruled by Rahu)
   - Yamaganda (Challenging window ruled by Jupiter/Ketu)
   - Gulika Kaalam (Saturn's son Gulika's window)
   - Abhijit Muhurtha (8th Muhurtha around midday; universally auspicious except Wednesdays)
   - Brahma Muhurtha (Pre-dawn 96-48 mins before sunrise; supreme for meditation & study)
   - Choghadiya Tables (Day and Night auspicious / inauspicious intervals)
"""

import math
from datetime import datetime, timedelta, time
from typing import Dict, List, Any, Optional, Tuple
from app.models.astrological import Kundali
from app.core.constants import NAKSHATRAS


class PanchangaEngine:
    """
    Precision astronomical Panchanga and Muhurtha calculator.
    """

    TITHI_NAMES = [
        "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima"
    ]

    TITHI_DEITIES = [
        "Agni", "Brahma", "Gauri", "Ganesha", "Nagas / Snake Gods",
        "Kartikeya (Murugan)", "Surya", "Shiva / Rudra", "Durga", "Yama / Dharma",
        "Vishvadevas", "Vishnu", "Kamadeva", "Shiva", "Chandra / Moon"
    ]

    VARA_DATA = [
        {"name": "Ravivara", "english": "Sunday", "lord": "Sun", "quality": "Energy, authority, leadership, vitality"},
        {"name": "Somavara", "english": "Monday", "lord": "Moon", "quality": "Mind, emotion, public interaction, mother"},
        {"name": "Mangalavara", "english": "Tuesday", "lord": "Mars", "quality": "Courage, physical vitality, engineering, defense"},
        {"name": "Budhavara", "english": "Wednesday", "lord": "Mercury", "quality": "Intellect, business, communication, analytics"},
        {"name": "Guruvara", "english": "Thursday", "lord": "Jupiter", "quality": "Wisdom, spirituality, expansion, advisory"},
        {"name": "Shukravara", "english": "Friday", "lord": "Venus", "quality": "Creativity, arts, finance, diplomacy, luxury"},
        {"name": "Shanivara", "english": "Saturday", "lord": "Saturn", "quality": "Discipline, perseverance, long-term planning, service"}
    ]

    YOGA_NAMES = [
        ("Vishkambha", "Malefic", "Obstruction, requiring extra perseverance"),
        ("Priti", "Benefic", "Affection, mutual attraction, social goodwill"),
        ("Ayushman", "Benefic", "Longevity, health, lasting accomplishments"),
        ("Saubhagya", "Benefic", "Good fortune, prosperity, marital bliss"),
        ("Shobhana", "Benefic", "Radiance, artistic charm, eloquence"),
        ("Atiganda", "Malefic", "Sudden hurdles, caution in travel/agreements"),
        ("Sukarma", "Benefic", "Virtuous deeds, high integrity, noble actions"),
        ("Dhriti", "Benefic", "Patience, mental steadfastness, endurance"),
        ("Shoola", "Malefic", "Pain, sharp conflicts, medical sensitivity"),
        ("Ganda", "Malefic", "Complications, karmic knots, requiring care"),
        ("Vriddhi", "Benefic", "Growth, compounding financial gains, expansion"),
        ("Dhruva", "Benefic", "Stability, permanently grounded achievements"),
        ("Vyaghata", "Malefic", "Fierce obstacles, intense encounters"),
        ("Harshana", "Benefic", "Joy, cheerfulness, delight, celebration"),
        ("Vajra", "Malefic", "Rigid conditions, power struggles"),
        ("Siddhi", "Benefic", "Mastery, successful execution, spiritual fruition"),
        ("Vyatipata", "Malefic", "Major volatility, caution in investments"),
        ("Variyan", "Benefic", "Comfort, ease, luxurious enjoyment"),
        ("Parigha", "Malefic", "Barriers, restraint, delay in expansion"),
        ("Shiva", "Benefic", "Benevolence, divine protection, auspiciousness"),
        ("Siddha", "Benefic", "Accomplishment of goals, perfection"),
        ("Sadhya", "Benefic", "Achievable objectives, peaceful mediation"),
        ("Shubha", "Benefic", "Auspicious welfare, purity, moral clarity"),
        ("Shukla", "Benefic", "Radiant clarity, enlightenment, illumination"),
        ("Brahma", "Benefic", "Creative intelligence, higher scholarship"),
        ("Indra", "Benefic", "Executive leadership, sovereign status, authority"),
        ("Vaidhriti", "Malefic", "Contradictory forces, requires spiritual grounding")
    ]

    # Repeating Karanas (7 Chara)
    CHARA_KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti (Bhadra)"]

    # Rahu Kaalam 8th-division index by weekday (0: Sunday, 1: Monday, ... 6: Saturday)
    # Divisions are 0-indexed (0 to 7) representing the 8 segments of the daytime (approx 1.5h each)
    RAHU_KAALAM_INTERVALS = {
        0: (7, "16:30 - 18:00"),  # Sunday: 8th segment
        1: (1, "07:30 - 09:00"),  # Monday: 2nd segment
        2: (6, "15:00 - 16:30"),  # Tuesday: 7th segment
        3: (4, "12:00 - 13:30"),  # Wednesday: 5th segment
        4: (5, "13:30 - 15:00"),  # Thursday: 6th segment
        5: (3, "10:30 - 12:00"),  # Friday: 4th segment
        6: (2, "09:00 - 10:30")   # Saturday: 3rd segment
    }

    YAMAGANDA_INTERVALS = {
        0: (4, "12:00 - 13:30"),  # Sunday
        1: (3, "10:30 - 12:00"),  # Monday
        2: (2, "09:00 - 10:30"),  # Tuesday
        3: (1, "07:30 - 09:00"),  # Wednesday
        4: (0, "06:00 - 07:30"),  # Thursday
        5: (6, "15:00 - 16:30"),  # Friday
        6: (5, "13:30 - 15:00")   # Saturday
    }

    GULIKA_INTERVALS = {
        0: (6, "15:00 - 16:30"),  # Sunday
        1: (5, "13:30 - 15:00"),  # Monday
        2: (4, "12:00 - 13:30"),  # Tuesday
        3: (3, "10:30 - 12:00"),  # Wednesday
        4: (2, "09:00 - 10:30"),  # Thursday
        5: (1, "07:30 - 09:00"),  # Friday
        6: (0, "06:00 - 07:30")   # Saturday
    }

    # Day Choghadiya sequence by weekday lord starting order
    # Lords order: Udveg (Sun), Char (Venus), Labh (Mercury), Amrit (Moon), Kaal (Saturn), Shubh (Jupiter), Rog (Mars)
    CHOGHADIYA_TYPES = {
        "Amrit": {"nature": "Best", "color": "Green", "significance": "All auspicious activities, contracts, new ventures"},
        "Shubh": {"nature": "Good", "color": "Green", "significance": "Ceremonies, education, purchases, meetings"},
        "Labh": {"nature": "Gainful", "color": "Green", "significance": "Commercial trade, business deals, financial investments"},
        "Char": {"nature": "Neutral", "color": "Blue", "significance": "Travel, mobility, routine communications"},
        "Rog": {"nature": "Inauspicious", "color": "Red", "significance": "Debates, conflicts, avoid new beginnings"},
        "Kaal": {"nature": "Inauspicious", "color": "Red", "significance": "Loss, delay, avoid auspicious ceremonies"},
        "Udveg": {"nature": "Inauspicious", "color": "Red", "significance": "Anxiety, administrative friction, government work only"}
    }

    @classmethod
    def calculate_tithi(cls, sun_lon: float, moon_lon: float) -> Dict[str, Any]:
        """
        Calculate Tithi (Lunar Day: 1 to 30) from solar-lunar elongation.
        Each Tithi = 12° of separation.
        """
        diff = (moon_lon - sun_lon) % 360.0
        tithi_idx = int(diff / 12.0)  # 0 to 29
        tithi_num = tithi_idx + 1

        is_shukla = tithi_num <= 15
        paksha = "Shukla Paksha" if is_shukla else "Krishna Paksha"

        name_idx = (tithi_num - 1) % 15
        if is_shukla and tithi_num == 15:
            tithi_name = "Purnima (Full Moon)"
        elif not is_shukla and tithi_num == 30:
            tithi_name = "Amavasya (New Moon)"
        else:
            tithi_name = f"{cls.TITHI_NAMES[name_idx]}"

        deg_in_tithi = diff % 12.0
        pct_completed = round((deg_in_tithi / 12.0) * 100.0, 1)
        remaining_deg = round(12.0 - deg_in_tithi, 2)

        deity = cls.TITHI_DEITIES[name_idx]

        return {
            "tithi_number": tithi_num,
            "name": tithi_name,
            "paksha": paksha,
            "deity": deity,
            "elongation_degrees": round(diff, 2),
            "degrees_elapsed_in_tithi": round(deg_in_tithi, 2),
            "percentage_completed": pct_completed,
            "degrees_remaining": remaining_deg
        }

    @classmethod
    def calculate_vara(cls, dt: datetime) -> Dict[str, Any]:
        """
        Calculate Vara (Solar Weekday: Sunday=0 to Saturday=6).
        Python weekday: Monday=0 to Sunday=6 -> Map to Sunday=0.
        """
        py_weekday = dt.weekday()  # Mon=0, Sun=6
        vara_idx = (py_weekday + 1) % 7  # Sun=0, Mon=1, ..., Sat=6
        v_data = cls.VARA_DATA[vara_idx]

        return {
            "vara_index": vara_idx,
            "sanskrit_name": v_data["name"],
            "english_name": v_data["english"],
            "ruling_planet": v_data["lord"],
            "cosmic_quality": v_data["quality"]
        }

    @classmethod
    def calculate_yoga(cls, sun_lon: float, moon_lon: float) -> Dict[str, Any]:
        """
        Calculate Nirayana Sun + Moon Yoga (1 to 27).
        Sum = (Sun_Lon + Moon_Lon) % 360° / 13°20' (13.333333°).
        """
        total = (sun_lon + moon_lon) % 360.0
        yoga_span = 360.0 / 27.0  # 13.333333333333334
        yoga_idx = int(total / yoga_span)
        yoga_idx = min(26, yoga_idx)

        name, nature, desc = cls.YOGA_NAMES[yoga_idx]
        deg_in_yoga = total % yoga_span
        pct_completed = round((deg_in_yoga / yoga_span) * 100.0, 1)

        return {
            "yoga_number": yoga_idx + 1,
            "name": name,
            "nature": nature,
            "description": desc,
            "sum_degrees": round(total, 2),
            "percentage_completed": pct_completed
        }

    @classmethod
    def calculate_karana(cls, sun_lon: float, moon_lon: float) -> Dict[str, Any]:
        """
        Calculate Karana (Half-tithi: 1 to 60).
        Each Karana = 6° of elongation.
        4 Fixed Karanas:
        - Shakuni (57th half-tithi)
        - Chatushpada (58th)
        - Naga (59th)
        - Kintughna (1st half-tithi of Shukla Pratipada)
        7 Repeating Chara Karanas (repeat across the remaining 56 half-tithis).
        """
        diff = (moon_lon - sun_lon) % 360.0
        karana_num = int(diff / 6.0) + 1  # 1 to 60

        if karana_num == 1:
            name = "Kintughna"
            k_type = "Fixed (Sthira)"
            is_vishti = False
        elif karana_num == 58:
            name = "Shakuni"
            k_type = "Fixed (Sthira)"
            is_vishti = False
        elif karana_num == 59:
            name = "Chatushpada"
            k_type = "Fixed (Sthira)"
            is_vishti = False
        elif karana_num == 60:
            name = "Naga"
            k_type = "Fixed (Sthira)"
            is_vishti = False
        else:
            # Repeating 7 chara karanas
            idx = (karana_num - 2) % 7
            name = cls.CHARA_KARANAS[idx]
            k_type = "Repeating (Chara)"
            is_vishti = "Vishti" in name

        deg_in_karana = diff % 6.0
        pct_completed = round((deg_in_karana / 6.0) * 100.0, 1)

        return {
            "karana_number": karana_num,
            "name": name,
            "type": k_type,
            "is_vishti_bhadra": is_vishti,
            "advisory": "Vishti (Bhadra) active: Postpone contract signings, weddings, and journeys" if is_vishti else "Normal favorable Karana.",
            "percentage_completed": pct_completed
        }

    @classmethod
    def calculate_muhurtha_intervals(
        cls,
        dt: datetime,
        sunrise: Optional[datetime] = None,
        sunset: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculate exact Rahu Kaalam, Yamaganda, Gulika Kaalam, Abhijit Muhurtha,
        and Brahma Muhurtha for the given date.
        If sunrise/sunset are not specified, standard 06:00 to 18:00 baseline is used.
        """
        date_base = dt.date()
        if not sunrise:
            sunrise = datetime.combine(date_base, time(6, 0))
        if not sunset:
            sunset = datetime.combine(date_base, time(18, 0))

        day_duration = (sunset - sunrise).total_seconds()
        part_duration = day_duration / 8.0  # 1/8th of daytime

        py_weekday = dt.weekday()
        vara_idx = (py_weekday + 1) % 7  # Sun=0, Mon=1, ..., Sat=6

        # Rahu Kaalam
        rahu_segment, _ = cls.RAHU_KAALAM_INTERVALS[vara_idx]
        rahu_start = sunrise + timedelta(seconds=rahu_segment * part_duration)
        rahu_end = rahu_start + timedelta(seconds=part_duration)

        # Yamaganda
        yama_segment, _ = cls.YAMAGANDA_INTERVALS[vara_idx]
        yama_start = sunrise + timedelta(seconds=yama_segment * part_duration)
        yama_end = yama_start + timedelta(seconds=part_duration)

        # Gulika Kaalam
        guli_segment, _ = cls.GULIKA_INTERVALS[vara_idx]
        guli_start = sunrise + timedelta(seconds=guli_segment * part_duration)
        guli_end = guli_start + timedelta(seconds=part_duration)

        # Abhijit Muhurtha: Midday 8th Muhurtha (day divided into 15 Muhurthas of 48 mins each)
        muhurtha_len = day_duration / 15.0
        abhijit_start = sunrise + timedelta(seconds=7 * muhurtha_len)
        abhijit_end = abhijit_start + timedelta(seconds=muhurtha_len)
        abhijit_applicable = (vara_idx != 3)  # Wednesday (Budhavara) cancels Abhijit Muhurtha

        # Brahma Muhurtha: 96 mins to 48 mins before sunrise
        brahma_start = sunrise - timedelta(minutes=96)
        brahma_end = sunrise - timedelta(minutes=48)

        # Check if current time falls in any critical window
        current_dt = dt
        in_rahu = rahu_start <= current_dt <= rahu_end
        in_yama = yama_start <= current_dt <= yama_end
        in_gulika = guli_start <= current_dt <= guli_end
        in_abhijit = abhijit_start <= current_dt <= abhijit_end and abhijit_applicable

        return {
            "sunrise": sunrise.strftime("%H:%M:%S"),
            "sunset": sunset.strftime("%H:%M:%S"),
            "rahu_kaalam": {
                "start": rahu_start.strftime("%H:%M"),
                "end": rahu_end.strftime("%H:%M"),
                "is_active_now": in_rahu,
                "note": "Avoid launching new ventures or executing agreements."
            },
            "yamaganda": {
                "start": yama_start.strftime("%H:%M"),
                "end": yama_end.strftime("%H:%M"),
                "is_active_now": in_yama,
                "note": "Caution with major travels and investments."
            },
            "gulika_kaalam": {
                "start": guli_start.strftime("%H:%M"),
                "end": guli_end.strftime("%H:%M"),
                "is_active_now": in_gulika,
                "note": "Favorable for repetitive work and building foundations."
            },
            "abhijit_muhurtha": {
                "start": abhijit_start.strftime("%H:%M"),
                "end": abhijit_end.strftime("%H:%M"),
                "is_active_now": in_abhijit,
                "is_applicable": abhijit_applicable,
                "note": "Universally auspicious 8th Muhurtha for all high-stakes beginnings." if abhijit_applicable else "Abhijit Muhurtha neutralized on Wednesdays."
            },
            "brahma_muhurtha": {
                "start": brahma_start.strftime("%H:%M"),
                "end": brahma_end.strftime("%H:%M"),
                "note": "Supreme window for spiritual practices, mantra meditation, and intellectual study."
            }
        }

    @classmethod
    def get_complete_panchanga(cls, kundali: Kundali) -> Dict[str, Any]:
        """
        Assemble the complete 5-limb Vedic Panchanga and auspicious Muhurtha dossier
        for a birth chart or consultation moment.
        """
        sun_lon = kundali.planets["Sun"].longitude if "Sun" in kundali.planets else 0.0
        moon_lon = kundali.planets["Moon"].longitude if "Moon" in kundali.planets else 0.0
        dt = kundali.birth_datetime

        tithi_data = cls.calculate_tithi(sun_lon, moon_lon)
        vara_data = cls.calculate_vara(dt)
        yoga_data = cls.calculate_yoga(sun_lon, moon_lon)
        karana_data = cls.calculate_karana(sun_lon, moon_lon)

        # Nakshatra info from Moon
        moon_pos = kundali.planets.get("Moon")
        if moon_pos:
            nak_data = {
                "number": moon_pos.nakshatra_number + 1,
                "name": moon_pos.nakshatra_name,
                "pada": moon_pos.nakshatra_pada,
                "lord": moon_pos.nakshatra_lord,
                "deity": NAKSHATRAS[moon_pos.nakshatra_number]["deity"] if moon_pos.nakshatra_number < len(NAKSHATRAS) else "Universal Deity"
            }
        else:
            nak_data = {"number": 1, "name": "Ashwini", "pada": 1, "lord": "Ketu", "deity": "Ashwini Kumaras"}

        muhurtha_data = cls.calculate_muhurtha_intervals(dt)

        return {
            "panchanga": {
                "tithi": tithi_data,
                "vara": vara_data,
                "nakshatra": nak_data,
                "yoga": yoga_data,
                "karana": karana_data
            },
            "muhurtha": muhurtha_data,
            "overall_summary": (
                f"Panchanga: {tithi_data['paksha']} {tithi_data['name']}, "
                f"{vara_data['sanskrit_name']} ({vara_data['english_name']}), "
                f"Nakshatra {nak_data['name']} (Pada {nak_data['pada']}), "
                f"Yoga {yoga_data['name']} ({yoga_data['nature']}), "
                f"Karana {karana_data['name']} ({karana_data['type']})."
            )
        }
