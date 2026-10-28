"""
Jaimini Astrological Calculation Engine
=======================================
Implements the classical Jaimini Upadesha Sutras system:
1. Chara Karakas (7-Karaka and 8-Karaka schemes: Atmakaraka, Amatyakaraka, Bhratrikaraka,
   Matrikaraka, Putrakaraka, Gnatikaraka, Darakaraka)
2. Arudha Padas (A1 to A12, including Arudha Lagna AL and Upapada Lagna UL with classical exceptions)
3. Rashi Drishti (Jaimini Sign Aspects: Movable aspects Fixed, Fixed aspects Movable, Dual aspects Dual)
4. Argala & Virodhargala (Intervention & Obstruction)
5. Karakamsha & Swamsha analysis (Atmakaraka in Navamsha D9)
6. Chara Dasha sign dasha period calculator
"""

import math
from typing import Dict, List, Any, Optional, Tuple
from app.models.astrological import Kundali, Planet, PlanetPosition, ZodiacSign
from app.core.constants import ZODIAC_SIGNS, ZODIAC_SANSKRIT, SIGN_LORDS


class JaiminiEngine:
    """
    Comprehensive computational engine for the Jaimini Sutras astrological tradition.
    """

    # Classical 7 Chara Karaka roles and spiritual/mundane significations
    KARAKA_ROLES_7 = [
        ("Atmakaraka", "AK", "King of Horoscope; Soul, true self, ego, spiritual destiny, longevity"),
        ("Amatyakaraka", "AmK", "Minister / Prime Counselor; Career, profession, intellect, status, financial capacity"),
        ("Bhratrikaraka", "BK", "Siblings, companions, father/Guru, courage, motivation"),
        ("Matrikaraka", "MK", "Mother, vehicles, real estate, emotional happiness, inner peace"),
        ("Putrakaraka", "PK", "Children, progeny, intellect, creativity, disciples, past good karma"),
        ("Gnatikaraka", "GK", "Obstacles, kinsmen/relatives, diseases, litigation, rivals, competition"),
        ("Darakaraka", "DK", "Spouse, partnership, business relations, sexual union, public interaction")
    ]

    @classmethod
    def calculate_chara_karakas(
        cls,
        kundali: Kundali,
        include_rahu: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate Jaimini Chara Karakas based on planetary degrees in sign.
        According to Jaimini Sutras, the planet with the highest longitude in any sign
        (from 0° to 30°) becomes the Atmakaraka (AK), followed by AmK, BK, MK, PK, GK, DK.
        Rahu moves retrograde; when Rahu is included, its degree from the end of the sign (30° - deg)
        is traditionally considered in the 8-karaka scheme.
        """
        eligible_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        planet_degrees: List[Tuple[str, float, PlanetPosition]] = []

        for p_name in eligible_planets:
            pos = kundali.planets.get(p_name)
            if pos:
                planet_degrees.append((p_name, pos.degrees_in_sign, pos))

        if include_rahu:
            rahu_pos = kundali.planets.get("Rahu")
            if rahu_pos:
                # In 8-karaka scheme, Rahu's degree is measured as 30 - deg due to retrograde motion
                effective_deg = 30.0 - (rahu_pos.degrees_in_sign % 30.0)
                planet_degrees.append(("Rahu", effective_deg, rahu_pos))

        # Sort descending by degrees in sign
        planet_degrees.sort(key=lambda x: x[1], reverse=True)

        karakas: Dict[str, Dict[str, Any]] = {}
        roles = cls.KARAKA_ROLES_7

        for idx, (p_name, deg, pos) in enumerate(planet_degrees):
            if idx < len(roles):
                role_name, code, desc = roles[idx]
                karakas[code] = {
                    "role": role_name,
                    "code": code,
                    "planet": p_name,
                    "degrees_in_sign": round(deg, 4),
                    "sign": pos.sign.name,
                    "sign_sanskrit": pos.sign.sanskrit_name,
                    "sign_index": pos.sign.value,
                    "signification": desc
                }

        atmakaraka_info = karakas.get("AK", {})
        amatyakaraka_info = karakas.get("AmK", {})
        darakaraka_info = karakas.get("DK", {})

        # Evaluate AK-AmK relationship (Raja Yoga if conjunct or mutually aspecting)
        raja_yoga = False
        ak_sign = atmakaraka_info.get("sign_index", 0)
        amk_sign = amatyakaraka_info.get("sign_index", 0)
        if ak_sign == amk_sign or (amk_sign in cls.get_rashi_drishti_for_sign(ak_sign)):
            raja_yoga = True

        return {
            "scheme": "7-Karaka" if not include_rahu else "8-Karaka",
            "karakas": karakas,
            "atmakaraka": atmakaraka_info,
            "amatyakaraka": amatyakaraka_info,
            "darakaraka": darakaraka_info,
            "ak_amk_raja_yoga": raja_yoga,
            "interpretation": {
                "AK_Planet": atmakaraka_info.get("planet"),
                "AK_Sign": atmakaraka_info.get("sign"),
                "Spiritual_Mission": f"The soul's evolutionary destiny is guided by {atmakaraka_info.get('planet')} in {atmakaraka_info.get('sign')}.",
                "Career_Drive": f"Worldly success and intellectual mastery are directed by Amatyakaraka {amatyakaraka_info.get('planet')}."
            }
        }

    @classmethod
    def calculate_arudha_padas(cls, kundali: Kundali) -> Dict[str, Dict[str, Any]]:
        """
        Calculate all 12 Arudha Padas (A1 to A12) according to Jaimini Sutras.
        Rule:
        - For house N, find the lord of the sign in house N.
        - Count houses from house N to the lord's house (say X houses).
        - Count X houses from the lord's house -> Arudha Pada.
        Classical Exceptions (Jaimini Sutra 1.1.30-31):
        - If the lord is in the house itself (X=1), the Arudha falls in the 10th house from it.
        - If the lord is in the 7th house from the house (X=7), the Arudha falls in the 4th house from it (or 10th from lord).
        """
        lagna_sign_idx = kundali.ascendant.sign.value
        padas: Dict[str, Dict[str, Any]] = {}

        pada_names = {
            1: ("Arudha Lagna", "AL", "Public image, status, perceived self, external reputation"),
            2: ("Dhana Pada", "A2", "Tangible financial assets, speech recognition, material accumulation"),
            3: ("Bhratri Pada", "A3", "Courage, communication, younger siblings, ventures"),
            4: ("Matru Pada", "A4", "Vehicles, home properties, mother's status, public comforts"),
            5: ("Putra Pada", "A5", "Fame, followers, intellect, creative creations, progeny status"),
            6: ("Shatru Pada", "A6", "Litigation, enemies, competitive struggles, maternal uncles"),
            7: ("Dara Pada", "A7", "Partnerships, spouse's societal background, trade, business relations"),
            8: ("Roga/Mrityu Pada", "A8", "Longevity perception, sudden transformations, hidden debts"),
            9: ("Bhagya Pada", "A9", "Fortune, higher learning, Guru, piety, spiritual reputation"),
            10: ("Rajya Pada", "A10", "Executive power, political rank, profession, career prominence"),
            11: ("Labha Pada", "A11", "Actual financial inflows, professional network, fulfilled aspirations"),
            12: ("Upapada Lagna", "UL", "Spouse's family status, marital durability, secret expenses")
        }

        for h in range(1, 13):
            house_sign_idx = (lagna_sign_idx + (h - 1)) % 12
            lord_name = SIGN_LORDS[house_sign_idx]
            lord_pos = kundali.planets.get(lord_name)
            
            if not lord_pos:
                lord_sign_idx = house_sign_idx
            else:
                lord_sign_idx = lord_pos.sign.value

            # Count distance from house to lord (inclusive, 1 to 12)
            distance = (lord_sign_idx - house_sign_idx) % 12 + 1

            # Count that same distance from lord
            raw_arudha_sign_idx = (lord_sign_idx + (distance - 1)) % 12

            # Classical Jaimini Exceptions:
            # If distance == 1 (lord in own house): Arudha is in 10th house from it (+9 signs)
            # If distance == 7 (lord in 7th from house): Arudha is in 10th from house (+9 signs or 4th from lord)
            final_arudha_sign_idx = raw_arudha_sign_idx
            exception_applied = None

            if distance == 1:
                final_arudha_sign_idx = (house_sign_idx + 9) % 12
                exception_applied = "Lord in Own House (Exception: 10th from House)"
            elif distance == 7:
                final_arudha_sign_idx = (house_sign_idx + 9) % 12
                exception_applied = "Lord in 7th House (Exception: 10th from House / 4th from Lord)"

            # House from Lagna
            arudha_house_from_lagna = (final_arudha_sign_idx - lagna_sign_idx) % 12 + 1

            title, code, desc = pada_names[h]
            padas[code] = {
                "house_number": h,
                "name": title,
                "code": code,
                "sign_index": final_arudha_sign_idx,
                "sign_name": ZODIAC_SIGNS[final_arudha_sign_idx],
                "sign_sanskrit": ZODIAC_SANSKRIT[final_arudha_sign_idx],
                "house_from_lagna": arudha_house_from_lagna,
                "lord": lord_name,
                "exception_applied": exception_applied,
                "description": desc
            }

        return padas

    @classmethod
    def get_rashi_drishti_for_sign(cls, sign_idx: int) -> List[int]:
        """
        Calculate Jaimini Rashi Drishti (Sign Aspects).
        Classical Rule:
        - Movable (Chara) signs (0, 3, 6, 9 -> Aries, Cancer, Libra, Capricorn)
          aspect all Fixed signs EXCEPT the adjacent one.
        - Fixed (Sthira) signs (1, 4, 7, 10 -> Taurus, Leo, Scorpio, Aquarius)
          aspect all Movable signs EXCEPT the adjacent one.
        - Dual (Dwisvabhava) signs (2, 5, 8, 11 -> Gemini, Virgo, Sagittarius, Pisces)
          aspect all other Dual signs.
        """
        modality = sign_idx % 3  # 0: Movable, 1: Fixed, 2: Dual
        aspects: List[int] = []

        if modality == 0:  # Movable
            # Aspects all Fixed (1, 4, 7, 10) except the adjacent sign (sign_idx + 1)
            fixed_signs = [1, 4, 7, 10]
            adjacent = (sign_idx + 1) % 12
            aspects = [s for s in fixed_signs if s != adjacent]
        elif modality == 1:  # Fixed
            # Aspects all Movable (0, 3, 6, 9) except the adjacent previous sign (sign_idx - 1)
            movable_signs = [0, 3, 6, 9]
            adjacent = (sign_idx - 1) % 12
            aspects = [s for s in movable_signs if s != adjacent]
        else:  # Dual
            # Aspects all other Dual signs (2, 5, 8, 11) except itself
            dual_signs = [2, 5, 8, 11]
            aspects = [s for s in dual_signs if s != sign_idx]

        return aspects

    @classmethod
    def calculate_all_rashi_drishti(cls, kundali: Kundali) -> Dict[str, Dict[str, Any]]:
        """
        Calculate Jaimini sign aspects for all 12 signs, including planets posited in aspecting signs.
        """
        result: Dict[str, Dict[str, Any]] = {}

        # Map planets to sign index
        planets_in_sign: Dict[int, List[str]] = {i: [] for i in range(12)}
        for p_name, pos in kundali.planets.items():
            planets_in_sign[pos.sign.value].append(p_name)

        for s_idx in range(12):
            aspecting_signs = cls.get_rashi_drishti_for_sign(s_idx)
            aspecting_planets = []
            for a_sign in aspecting_signs:
                aspecting_planets.extend(planets_in_sign[a_sign])

            s_name = ZODIAC_SIGNS[s_idx]
            result[s_name] = {
                "sign_index": s_idx,
                "sign_name": s_name,
                "aspects_signs": [ZODIAC_SIGNS[a] for a in aspecting_signs],
                "aspects_sign_indices": aspecting_signs,
                "planets_aspecting_this_sign": aspecting_planets,
                "planets_present": planets_in_sign[s_idx]
            }

        return result

    @classmethod
    def calculate_argala(cls, kundali: Kundali) -> Dict[str, Any]:
        """
        Calculate Jaimini Argala (Intervention) and Virodhargala (Obstruction) for Lagna.
        Primary Argala:
        - 2nd house (Dhana / food / wealth): Obstructed by 12th house (Virodha).
        - 4th house (Vehicles / happiness): Obstructed by 10th house (Virodha).
        - 11th house (Gains / friends): Obstructed by 3rd house (Virodha).
        Secondary Argala:
        - 5th house (Progeny / intellect): Obstructed by 9th house (Virodha).
        """
        lagna_idx = kundali.ascendant.sign.value
        planets_in_house: Dict[int, List[str]] = {h: [] for h in range(1, 13)}

        for p_name, pos in kundali.planets.items():
            h = (pos.sign.value - lagna_idx) % 12 + 1
            planets_in_house[h].append(p_name)

        argala_pairs = [
            ("2nd House (Dhana)", 2, 12, "12th House (Vyaya)"),
            ("4th House (Sukha)", 4, 10, "10th House (Karma)"),
            ("11th House (Labha)", 11, 3, "3rd House (Bhatru)"),
            ("5th House (Putra)", 5, 9, "9th House (Dharma)")
        ]

        argalas: List[Dict[str, Any]] = []
        for name, arg_h, vir_h, vir_name in argala_pairs:
            arg_planets = planets_in_house[arg_h]
            vir_planets = planets_in_house[vir_h]
            has_argala = len(arg_planets) > 0
            is_obstructed = len(vir_planets) >= len(arg_planets) if has_argala else False

            argalas.append({
                "type": name,
                "argala_house": arg_h,
                "argala_planets": arg_planets,
                "virodha_house": vir_h,
                "virodha_name": vir_name,
                "virodha_planets": vir_planets,
                "active_argala": has_argala and not is_obstructed,
                "status": "Active Unobstructed Argala" if (has_argala and not is_obstructed) else (
                    "Obstructed by Virodha" if (has_argala and is_obstructed) else "No Argala"
                )
            })

        return {"lagna_argalas": argalas}

    @classmethod
    def analyze_karakamsha(cls, kundali: Kundali) -> Dict[str, Any]:
        """
        Analyze Karakamsha Lagna (KL) - the sign occupied by Atmakaraka (AK) in Navamsha (D9).
        According to Jaimini Sutras, Karakamsha reveals:
        - Spiritual path, Ishta Devata, and ultimate soul liberation (Moksha)
        - Inherent intellectual strengths and highest career attainments
        """
        chara_data = cls.calculate_chara_karakas(kundali)
        ak_planet_name = chara_data["atmakaraka"].get("planet")
        if not ak_planet_name:
            return {}

        # Look up D9 Navamsha chart
        d9_chart = kundali.vargas.get(9)
        kl_sign_idx = 0
        kl_sign_name = "Aries"

        if d9_chart and ak_planet_name in d9_chart.placements:
            d9_pos = d9_chart.placements[ak_planet_name]
            kl_sign_idx = d9_pos.sign.value
            kl_sign_name = d9_pos.sign.name
        else:
            # Fallback calculate Navamsha sign directly from longitude
            ak_pos = kundali.planets[ak_planet_name]
            nav_span = 30.0 / 9.0  # 3°20' = 3.333333°
            nav_num = int((ak_pos.degrees_in_sign % 30.0) / nav_span)
            sign_element = ak_pos.sign.value % 4
            # Fire starts at Aries(0), Earth starts at Capricorn(9), Air starts at Libra(6), Water starts at Cancer(3)
            base_signs = [0, 9, 6, 3]
            kl_sign_idx = (base_signs[sign_element] + nav_num) % 12
            kl_sign_name = ZODIAC_SIGNS[kl_sign_idx]

        # 12th from Karakamsha indicates Ishta Devata / Moksha
        moksha_sign_idx = (kl_sign_idx + 11) % 12
        moksha_sign_name = ZODIAC_SIGNS[moksha_sign_idx]

        # Ishta Devata deity associations based on 12th from Karakamsha
        lord_of_12th_from_kl = SIGN_LORDS[moksha_sign_idx]
        deity_map = {
            "Sun": "Lord Shiva / Rama / Gayatri",
            "Moon": "Goddess Gauri / Parvati / Krishna",
            "Mars": "Lord Kartikeya (Murugan) / Narasimha / Hanuman",
            "Mercury": "Lord Vishnu / Narayana / Saraswati",
            "Jupiter": "Lord Samba Shiva / Brihaspati / Dattatreya",
            "Venus": "Goddess Lakshmi / Radharani / Sri Vidya",
            "Saturn": "Lord Kurma Avatara / Shani Deva / Yama",
            "Rahu": "Goddess Durga / Chhinnamasta / Sarpa Devata",
            "Ketu": "Lord Ganesha / Matsya Avatara / Muktidatri"
        }

        ishta_devata = deity_map.get(lord_of_12th_from_kl, "Lord Vishnu / Shiva")

        return {
            "atmakaraka_planet": ak_planet_name,
            "karakamsha_sign": kl_sign_name,
            "karakamsha_sign_sanskrit": ZODIAC_SANSKRIT[kl_sign_idx],
            "karakamsha_sign_index": kl_sign_idx,
            "moksha_bhava_sign": moksha_sign_name,
            "moksha_lord": lord_of_12th_from_kl,
            "ishta_devata": ishta_devata,
            "spiritual_path_guidance": f"With {ak_planet_name} in {kl_sign_name} in Navamsha, the soul attains spiritual realization through devotion to {ishta_devata}."
        }

    @classmethod
    def calculate_chara_dasha(
        cls,
        kundali: Kundali,
        years: int = 72
    ) -> List[Dict[str, Any]]:
        """
        Calculate Jaimini Chara Dasha sign dasha sequence and periods.
        Order of Progression:
        - Direct (Savya): Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius
        - Indirect / Reverse (Apasavya): Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces
        Period Length:
        - Number of signs counted from the Dasha sign to its ruling lord minus 1 year
          (or counted backwards for Apasavya signs; full 12 years if lord is in own sign).
        """
        lagna_idx = kundali.ascendant.sign.value
        direct_progression_signs = [0, 1, 2, 6, 7, 8]  # Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius
        is_direct = lagna_idx in direct_progression_signs

        dasha_sequence: List[int] = []
        if is_direct:
            dasha_sequence = [(lagna_idx + i) % 12 for i in range(12)]
        else:
            dasha_sequence = [(lagna_idx - i) % 12 for i in range(12)]

        periods: List[Dict[str, Any]] = []
        current_year = kundali.birth_datetime.year
        birth_month = kundali.birth_datetime.month
        birth_day = kundali.birth_datetime.day

        total_elapsed_years = 0
        cycle = 0

        while total_elapsed_years < years and cycle < 3:
            cycle += 1
            for sign_idx in dasha_sequence:
                if total_elapsed_years >= years:
                    break

                lord_name = SIGN_LORDS[sign_idx]
                lord_pos = kundali.planets.get(lord_name)
                lord_sign_idx = lord_pos.sign.value if lord_pos else sign_idx

                # Calculate duration
                sign_is_direct = sign_idx in direct_progression_signs
                if sign_is_direct:
                    span = (lord_sign_idx - sign_idx) % 12
                else:
                    span = (sign_idx - lord_sign_idx) % 12

                duration = 12 if span == 0 else span

                start_yr = current_year + total_elapsed_years
                end_yr = start_yr + duration
                total_elapsed_years += duration

                periods.append({
                    "cycle": cycle,
                    "sign": ZODIAC_SIGNS[sign_idx],
                    "sign_sanskrit": ZODIAC_SANSKRIT[sign_idx],
                    "sign_index": sign_idx,
                    "lord": lord_name,
                    "duration_years": duration,
                    "start_year": start_yr,
                    "end_year": end_yr,
                    "start_period": f"{birth_day:02d}/{birth_month:02d}/{start_yr}",
                    "end_period": f"{birth_day:02d}/{birth_month:02d}/{end_yr}"
                })

        return periods
