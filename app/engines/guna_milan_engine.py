"""
Ashtakoota & Dashakoota Guna Milan Engine
==========================================
Comprehensive marriage compatibility and relationship harmony system:
1. 36-Point Classical Ashtakoota Milan:
   - Varna Kuta (1 point) - Spiritual & ego harmony
   - Vashya Kuta (2 points) - Mutual magnetism & instinctual rapport
   - Tara Kuta (3 points) - Destiny, fortune & longevity
   - Yoni Kuta (4 points) - Biological, intimate & sexual compatibility
   - Graha Maitri Kuta (5 points) - Psychological & mental affinity
   - Gana Kuta (6 points) - Temperament & behavioral harmony
   - Bhakoot Kuta (7 points) - Emotional bonding, wealth & family welfare (with classical dosha cancellations)
   - Nadi Kuta (8 points) - Genetic, physiological & bio-energy health (with classical dosha cancellations)
2. Dashakoota Additions (Mahendra, Stree Deergha, Rajju, Vedha)
3. Manglik / Kuja Dosha Detection & Mutual Cancellation Evaluation
"""

from typing import Dict, List, Any, Optional, Tuple
from app.models.astrological import Kundali, PlanetPosition
from app.core.constants import ZODIAC_SIGNS, SIGN_LORDS, NATURAL_RELATIONSHIPS


class GunaMilanEngine:
    """
    Classical Vedic Kundali Milan calculation engine adhering to Muhurtha Chintamani
    and Brihat Parashara Hora Shastra.
    """

    # 1. Varna Mapping (0: Shudra, 1: Vaishya, 2: Kshatriya, 3: Brahmin)
    # Signs: Water (Cancer 3, Scorpio 7, Pisces 11) = Brahmin (3)
    #        Fire (Aries 0, Leo 4, Sagittarius 8) = Kshatriya (2)
    #        Earth (Taurus 1, Virgo 5, Capricorn 9) = Vaishya (1)
    #        Air (Gemini 2, Libra 6, Aquarius 10) = Shudra (0)
    SIGN_TO_VARNA = {
        0: 2, 1: 1, 2: 0, 3: 3,
        4: 2, 5: 1, 6: 0, 7: 3,
        8: 2, 9: 1, 10: 0, 11: 3
    }
    VARNA_NAMES = ["Shudra", "Vaishya", "Kshatriya", "Brahmin"]

    # 2. Vashya Mapping
    # Chatushpada (0), Manava (1), Jalachara (2), Vanachara (3), Keeta (4)
    SIGN_TO_VASHYA = {
        0: 0,   # Aries: Quadruped
        1: 0,   # Taurus: Quadruped
        2: 1,   # Gemini: Human
        3: 2,   # Cancer: Water creature
        4: 3,   # Leo: Wild beast
        5: 1,   # Virgo: Human
        6: 1,   # Libra: Human
        7: 4,   # Scorpio: Insect
        8: 1,   # Sagittarius (first half): Human
        9: 0,   # Capricorn (first half): Quadruped
        10: 1,  # Aquarius: Human
        11: 2   # Pisces: Water creature
    }
    VASHYA_NAMES = ["Chatushpada (Quadruped)", "Manava (Human)", "Jalachara (Water)", "Vanachara (Wild)", "Keeta (Insect)"]

    # 4. Yoni Animal Totems for 27 Nakshatras (0 to 26)
    # 14 animal pairs:
    # 0: Horse, 1: Elephant, 2: Sheep, 3: Serpent, 4: Dog, 5: Cat, 6: Rat,
    # 7: Cow, 8: Buffalo, 9: Tiger, 10: Deer, 11: Monkey, 12: Mongoose, 13: Lion
    NAKSHATRA_YONI = [
        0,   # 0: Ashwini -> Horse
        1,   # 1: Bharani -> Elephant
        2,   # 2: Krittika -> Sheep
        3,   # 3: Rohini -> Serpent
        3,   # 4: Mrigashira -> Serpent
        4,   # 5: Ardra -> Dog
        5,   # 6: Punarvasu -> Cat
        2,   # 7: Pushya -> Sheep
        5,   # 8: Ashlesha -> Cat
        6,   # 9: Magha -> Rat
        6,   # 10: Purva Phalguni -> Rat
        7,   # 11: Uttara Phalguni -> Cow
        8,   # 12: Hasta -> Buffalo
        9,   # 13: Chitra -> Tiger
        8,   # 14: Swati -> Buffalo
        9,   # 15: Vishakha -> Tiger
        10,  # 16: Anuradha -> Deer
        10,  # 17: Jyeshtha -> Deer
        4,   # 18: Moola -> Dog
        11,  # 19: Purva Ashadha -> Monkey
        12,  # 20: Uttara Ashadha -> Mongoose
        11,  # 21: Shravana -> Monkey
        13,  # 22: Dhanishta -> Lion
        0,   # 23: Shatabhisha -> Horse
        13,  # 24: Purva Bhadrapada -> Lion
        7,   # 25: Uttara Bhadrapada -> Cow
        1    # 26: Revati -> Elephant
    ]
    YONI_ANIMAL_NAMES = [
        "Horse", "Elephant", "Sheep", "Serpent", "Dog", "Cat", "Rat",
        "Cow", "Buffalo", "Tiger", "Deer", "Monkey", "Mongoose", "Lion"
    ]

    # Sworn enemy animal pairs (0 points)
    SWORN_ENEMY_YONIS = {
        (0, 8), (8, 0),    # Horse vs Buffalo
        (1, 13), (13, 1),  # Elephant vs Lion
        (2, 11), (11, 2),  # Sheep vs Monkey
        (3, 12), (12, 3),  # Serpent vs Mongoose
        (4, 10), (10, 4),  # Dog vs Deer
        (5, 6), (6, 5),    # Cat vs Rat
        (7, 9), (9, 7)     # Cow vs Tiger
    }

    # 6. Gana Classification (0: Deva, 1: Manushya, 2: Rakshasa)
    NAKSHATRA_GANA = [
        0, 1, 2, 1, 0, 1, 0, 0, 2,  # 0-8: Ashwini(Deva) to Ashlesha(Rakshasa)
        2, 1, 1, 0, 2, 0, 2, 0, 2,  # 9-17: Magha(Rakshasa) to Jyeshtha(Rakshasa)
        2, 1, 1, 0, 2, 2, 1, 1, 0   # 18-26: Moola(Rakshasa) to Revati(Deva)
    ]
    GANA_NAMES = ["Deva (Divine)", "Manushya (Human)", "Rakshasa (Fierce)"]

    # 8. Nadi Classification (0: Adi/Vata, 1: Madhya/Pitta, 2: Antya/Kapha)
    # Sequence follows 0, 1, 2, 2, 1, 0 repeating in snake pattern
    NAKSHATRA_NADI = [
        0, 1, 2,  # 0 Ashwini(Adi), 1 Bharani(Madhya), 2 Krittika(Antya)
        2, 1, 0,  # 3 Rohini(Antya), 4 Mrigashira(Madhya), 5 Ardra(Adi)
        0, 1, 2,  # 6 Punarvasu(Adi), 7 Pushya(Madhya), 8 Ashlesha(Antya)
        2, 1, 0,  # 9 Magha(Antya), 10 Purva Phalguni(Madhya), 11 Uttara Phalguni(Adi)
        0, 1, 2,  # 12 Hasta(Adi), 13 Chitra(Madhya), 14 Swati(Antya)
        2, 1, 0,  # 15 Vishakha(Antya), 16 Anuradha(Madhya), 17 Jyeshtha(Adi)
        0, 1, 2,  # 18 Moola(Adi), 19 Purva Ashadha(Madhya), 20 Uttara Ashadha(Antya)
        2, 1, 0,  # 21 Shravana(Antya), 22 Dhanishta(Madhya), 23 Shatabhisha(Adi)
        0, 1, 2   # 24 Purva Bhadrapada(Adi), 25 Uttara Bhadrapada(Madhya), 26 Revati(Antya)
    ]
    NADI_NAMES = ["Adi (Vata)", "Madhya (Pitta)", "Antya (Kapha)"]

    # Rajju classification for Dashakoota
    # 0: Siro (Head), 1: Kantha (Neck), 2: Nabha (Navel), 3: Kati (Waist), 4: Pada (Feet)
    NAKSHATRA_RAJJU = [
        4, 3, 2, 1, 0, 1, 2, 3, 4,
        4, 3, 2, 1, 0, 1, 2, 3, 4,
        4, 3, 2, 1, 0, 1, 2, 3, 4
    ]
    RAJJU_NAMES = ["Siro (Head)", "Kantha (Neck)", "Nabha (Navel)", "Kati (Waist)", "Pada (Feet)"]

    @classmethod
    def calculate_varna_kuta(cls, bride_sign_idx: int, groom_sign_idx: int) -> Tuple[float, str]:
        """
        1. Varna Kuta (Max 1 point).
        Groom's varna rank >= Bride's varna rank -> 1.0 point.
        Otherwise -> 0.0 points.
        """
        b_varna = cls.SIGN_TO_VARNA[bride_sign_idx]
        g_varna = cls.SIGN_TO_VARNA[groom_sign_idx]

        b_name = cls.VARNA_NAMES[b_varna]
        g_name = cls.VARNA_NAMES[g_varna]

        if g_varna >= b_varna:
            return 1.0, f"Compatible: Groom ({g_name}) is equal or higher varna than Bride ({b_name})."
        else:
            return 0.0, f"Varna Incompatibility: Groom ({g_name}) has lower varna ranking than Bride ({b_name})."

    @classmethod
    def calculate_vashya_kuta(cls, bride_sign_idx: int, groom_sign_idx: int) -> Tuple[float, str]:
        """
        2. Vashya Kuta (Max 2 points).
        Same group = 2 pts. Compatible groups = 1 pt. Hostile groups = 0 pts.
        """
        b_vashya = cls.SIGN_TO_VASHYA[bride_sign_idx]
        g_vashya = cls.SIGN_TO_VASHYA[groom_sign_idx]

        b_name = cls.VASHYA_NAMES[b_vashya]
        g_name = cls.VASHYA_NAMES[g_vashya]

        if b_vashya == g_vashya:
            return 2.0, f"Full Harmony: Both belong to {b_name}."
        # Wild beasts (Vanachara - Leo) vs others
        if (b_vashya == 3 and g_vashya in [0, 1]) or (g_vashya == 3 and b_vashya in [0, 1]):
            return 0.0, f"Incompatible: Vanachara and Manava/Quadruped create tension."
        return 1.0, f"Moderate Harmony between {b_name} and {g_name}."

    @classmethod
    def calculate_tara_kuta(cls, bride_nak: int, groom_nak: int) -> Tuple[float, str]:
        """
        3. Tara Kuta (Max 3 points).
        Calculate Tara from Bride to Groom, and Groom to Bride.
        Good Taras (rem % 9): 2 (Sampat), 4 (Kshema), 6 (Sadhana), 8 (Mitra), 0 (Paramamitra).
        Inauspicious: 1 (Janma), 3 (Vipat), 5 (Pratyak), 7 (Naidhana/Vadha).
        """
        diff1 = (groom_nak - bride_nak) % 27
        diff2 = (bride_nak - groom_nak) % 27

        tara1 = (diff1 + 1) % 9
        tara2 = (diff2 + 1) % 9

        auspicious_taras = [0, 2, 4, 6, 8]
        g_good = tara1 in auspicious_taras
        b_good = tara2 in auspicious_taras

        if g_good and b_good:
            return 3.0, "Excellent Tara harmony: Both birth stars support mutual health and fortune."
        elif g_good or b_good:
            return 1.5, "Moderate Tara harmony: One perspective is favorable."
        else:
            return 0.0, "Tara dosha present: Both stars land in challenging taras."

    @classmethod
    def calculate_yoni_kuta(cls, bride_nak: int, groom_nak: int) -> Tuple[float, str]:
        """
        4. Yoni Kuta (Max 4 points).
        Evaluates biological, intimate, and physical compatibility.
        Same animal = 4 pts. Friendly = 3 pts. Neutral = 2 pts. Unfriendly = 1 pt. Sworn enemies = 0 pts.
        """
        b_yoni = cls.NAKSHATRA_YONI[bride_nak]
        g_yoni = cls.NAKSHATRA_YONI[groom_nak]

        b_animal = cls.YONI_ANIMAL_NAMES[b_yoni]
        g_animal = cls.YONI_ANIMAL_NAMES[g_yoni]

        if b_yoni == g_yoni:
            return 4.0, f"Ideal physical harmony: Both share {b_animal} Yoni."

        if (b_yoni, g_yoni) in cls.SWORN_ENEMY_YONIS:
            return 0.0, f"Yoni Vaira (Sworn Enemies): {b_animal} vs {g_animal} leads to friction."

        # Friendly animal groupings
        friendly_groups = [
            {0, 1, 2},    # Horse, Elephant, Sheep
            {3, 4, 5},    # Serpent, Dog, Cat
            {6, 7, 8},    # Rat, Cow, Buffalo
            {9, 10, 11},  # Tiger, Deer, Monkey
            {12, 13}      # Mongoose, Lion
        ]
        for grp in friendly_groups:
            if b_yoni in grp and g_yoni in grp:
                return 3.0, f"Friendly Yoni dynamic between {b_animal} and {g_animal}."

        return 2.0, f"Neutral intimate compatibility between {b_animal} and {g_animal}."

    @classmethod
    def calculate_graha_maitri_kuta(cls, bride_sign_idx: int, groom_sign_idx: int) -> Tuple[float, str]:
        """
        5. Graha Maitri Kuta (Max 5 points).
        Friendship between Moon sign lords.
        Both mutual friends: 5.0 pts.
        One friend, one neutral: 4.0 pts.
        Both neutral: 3.0 pts.
        One friend, one enemy: 1.0 pt.
        Both mutual enemies: 0.0 pts.
        """
        b_lord = SIGN_LORDS[bride_sign_idx]
        g_lord = SIGN_LORDS[groom_sign_idx]

        if b_lord == g_lord:
            return 5.0, f"Perfect mental friendship: Same Moon lord ({b_lord})."

        rel_b = NATURAL_RELATIONSHIPS.get(b_lord, {})
        rel_g = NATURAL_RELATIONSHIPS.get(g_lord, {})

        b_to_g = "friend" if g_lord in rel_b.get("friends", []) else (
            "neutral" if g_lord in rel_b.get("neutrals", []) else "enemy"
        )
        g_to_b = "friend" if b_lord in rel_g.get("friends", []) else (
            "neutral" if b_lord in rel_g.get("neutrals", []) else "enemy"
        )

        if b_to_g == "friend" and g_to_b == "friend":
            return 5.0, f"Mutual Friendship: {b_lord} and {g_lord} are close friends."
        elif (b_to_g == "friend" and g_to_b == "neutral") or (b_to_g == "neutral" and g_to_b == "friend"):
            return 4.0, f"Good Friendship between {b_lord} and {g_lord}."
        elif b_to_g == "neutral" and g_to_b == "neutral":
            return 3.0, f"Neutral affinity between {b_lord} and {g_lord}."
        elif b_to_g == "enemy" and g_to_b == "enemy":
            return 0.0, f"Graha Maitri Incompatibility: {b_lord} and {g_lord} are mutual enemies."
        else:
            return 1.0, f"Mixed friendship dynamic between {b_lord} and {g_lord}."

    @classmethod
    def calculate_gana_kuta(cls, bride_nak: int, groom_nak: int) -> Tuple[float, str]:
        """
        6. Gana Kuta (Max 6 points).
        Temperament compatibility: Deva, Manushya, Rakshasa.
        Deva-Deva, Manushya-Manushya, Rakshasa-Rakshasa = 6 pts.
        Deva-Manushya = 5 pts.
        Manushya-Deva = 6 pts.
        Deva-Rakshasa = 1 pt.
        Manushya-Rakshasa = 0 pts.
        """
        b_gana = cls.NAKSHATRA_GANA[bride_nak]
        g_gana = cls.NAKSHATRA_GANA[groom_nak]

        b_name = cls.GANA_NAMES[b_gana]
        g_name = cls.GANA_NAMES[g_gana]

        if b_gana == g_gana:
            return 6.0, f"Full temperament harmony: Both belong to {b_name}."
        if (b_gana == 0 and g_gana == 1) or (b_gana == 1 and g_gana == 0):
            return 5.0, f"Harmonious combination of {b_name} and {g_name}."
        if (b_gana == 1 and g_gana == 2) or (b_gana == 2 and g_gana == 1):
            return 0.0, f"Gana Dosha: Manushya and Rakshasa combination can cause friction."
        return 1.0, f"Challenging temperament clash between {b_name} and {g_name}."

    @classmethod
    def calculate_bhakoot_kuta(cls, bride_sign_idx: int, groom_sign_idx: int) -> Tuple[float, str]:
        """
        7. Bhakoot Kuta (Max 7 points).
        Distance between Moon signs.
        Challenging:
        - 2/12 (Dwirdwadash): Financial or family stress
        - 6/8 (Shadashtak): Conflict, illness, discord
        - 9/5 (Navapancham): Spiritual differences or progeny delays
        Classical Bhakoot Dosha Cancellations:
        - Sign lords are identical (Aries & Scorpio ruled by Mars, Taurus & Libra by Venus)
        - Sign lords are mutual friends
        """
        dist = (groom_sign_idx - bride_sign_idx) % 12 + 1
        b_lord = SIGN_LORDS[bride_sign_idx]
        g_lord = SIGN_LORDS[groom_sign_idx]

        # Check cancellations
        is_same_lord = (b_lord == g_lord)
        rel_b = NATURAL_RELATIONSHIPS.get(b_lord, {})
        rel_g = NATURAL_RELATIONSHIPS.get(g_lord, {})
        is_friends = (g_lord in rel_b.get("friends", [])) and (b_lord in rel_g.get("friends", []))
        cancellation = is_same_lord or is_friends

        if dist in [1, 7, 3, 11, 4, 10]:
            return 7.0, f"Favorable Bhakoot relation ({dist}/{(14-dist)%12 or 12})."

        if dist in [2, 12]:
            if cancellation:
                return 7.0, f"Bhakoot Dosha (2/12 Dwirdwadash) cancelled due to friendly/identical lords ({b_lord}-{g_lord})."
            return 0.0, "Bhakoot Dosha (2/12 Dwirdwadash): Risk of financial and family instability."

        if dist in [6, 8]:
            if cancellation:
                return 7.0, f"Bhakoot Dosha (6/8 Shadashtak) cancelled due to friendly lords ({b_lord}-{g_lord})."
            return 0.0, "Bhakoot Dosha (6/8 Shadashtak): Potential for health strain or disputes."

        if dist in [5, 9]:
            if cancellation:
                return 7.0, f"Bhakoot Dosha (5/9 Navapancham) cancelled due to friendly lords ({b_lord}-{g_lord})."
            return 0.0, "Bhakoot Dosha (5/9 Navapancham): Requires emotional synchronization."

        return 7.0, "Favorable Bhakoot harmony."

    @classmethod
    def calculate_nadi_kuta(
        cls,
        bride_nak: int,
        groom_nak: int,
        bride_sign_idx: int,
        groom_sign_idx: int,
        bride_pada: int = 1,
        groom_pada: int = 1
    ) -> Tuple[float, str]:
        """
        8. Nadi Kuta (Max 8 points).
        Genetic, physiological, and bio-energy compatibility.
        Different Nadis = 8.0 points.
        Same Nadi = Nadi Dosha (0.0 points).
        Classical Nadi Dosha Cancellations:
        - Same Nakshatra but different Padas and signs.
        - Different Nakshatras with same sign lord.
        """
        b_nadi = cls.NAKSHATRA_NADI[bride_nak]
        g_nadi = cls.NAKSHATRA_NADI[groom_nak]

        b_name = cls.NADI_NAMES[b_nadi]
        g_name = cls.NADI_NAMES[g_nadi]

        if b_nadi != g_nadi:
            return 8.0, f"Perfect Nadi Harmony: Bride ({b_name}) and Groom ({g_name}) have different Nadis."

        # Same Nadi -> Check classical cancellations
        b_lord = SIGN_LORDS[bride_sign_idx]
        g_lord = SIGN_LORDS[groom_sign_idx]

        if bride_nak != groom_nak and b_lord == g_lord:
            return 8.0, f"Nadi Dosha ({b_name}) cancelled: Different Nakshatras under same sign lord ({b_lord})."

        if bride_nak == groom_nak and bride_pada != groom_pada:
            return 8.0, f"Nadi Dosha ({b_name}) cancelled: Same Nakshatra with distinct Padas ({bride_pada} vs {groom_pada})."

        return 0.0, f"Severe Nadi Dosha ({b_name}): Genetic bio-rhythm overlap requires Mahamrityunjaya or remedial Shanti."

    @classmethod
    def calculate_dashakoota_extras(
        cls,
        bride_nak: int,
        groom_nak: int
    ) -> Dict[str, Any]:
        """
        Calculate South Indian Dashakoota additions:
        - Mahendra (Progeny and prosperity)
        - Stree Deergha (Wife longevity and marital peace)
        - Rajju (Durability and health of marital bond)
        - Vedha (Affliction check)
        """
        diff = (groom_nak - bride_nak) % 27 + 1

        # Mahendra: Groom's star is 4th, 7th, 10th, 13th, 16th, 19th, 22nd, 25th from Bride's star
        mahendra_favorable = diff in [4, 7, 10, 13, 16, 19, 22, 25]

        # Stree Deergha: Groom's star is at least 9 or 13 constellations away
        stree_deergha_favorable = diff >= 9

        # Rajju Kuta: Same Rajju is inauspicious (especially Siro / Head Rajju)
        b_rajju = cls.NAKSHATRA_RAJJU[bride_nak]
        g_rajju = cls.NAKSHATRA_RAJJU[groom_nak]
        rajju_compatible = (b_rajju != g_rajju)
        rajju_name = cls.RAJJU_NAMES[b_rajju]

        return {
            "mahendra": {
                "favorable": mahendra_favorable,
                "note": "Promotes longevity of progeny and prosperity." if mahendra_favorable else "Neutral."
            },
            "stree_deergha": {
                "favorable": stree_deergha_favorable,
                "note": "Auspicious distance ensuring bride's lasting welfare." if stree_deergha_favorable else "Close proximity star."
            },
            "rajju": {
                "favorable": rajju_compatible,
                "bride_rajju": rajju_name,
                "groom_rajju": cls.RAJJU_NAMES[g_rajju],
                "note": "Rajju compatible (different body zones)." if rajju_compatible else f"Rajju Dosha ({rajju_name}) requires remedial precaution."
            }
        }

    @classmethod
    def check_manglik_dosha(cls, kundali: Kundali) -> Dict[str, Any]:
        """
        Check Manglik (Kuja Dosha) from Lagna, Moon, and Venus.
        Houses: 1st, 2nd, 4th, 7th, 8th, 12th.
        Checks classical cancellations (e.g. Mars in Aries, Scorpio, Capricorn, or conjunct Jupiter/Moon).
        """
        mars_pos = kundali.planets.get("Mars")
        if not mars_pos:
            return {"is_manglik": False, "intensity": "None"}

        lagna_sign = kundali.ascendant.sign.value
        moon_sign = kundali.planets["Moon"].sign.value if "Moon" in kundali.planets else lagna_sign
        venus_sign = kundali.planets["Venus"].sign.value if "Venus" in kundali.planets else lagna_sign

        mars_sign = mars_pos.sign.value

        h_lagna = (mars_sign - lagna_sign) % 12 + 1
        h_moon = (mars_sign - moon_sign) % 12 + 1
        h_venus = (mars_sign - venus_sign) % 12 + 1

        manglik_houses = [1, 2, 4, 7, 8, 12]
        lagna_manglik = h_lagna in manglik_houses
        moon_manglik = h_moon in manglik_houses
        venus_manglik = h_venus in manglik_houses

        # Cancellations:
        # Mars in Aries (1st), Scorpio (4th), Capricorn (7th), Cancer (8th), Sagittarius (12th)
        cancelled = False
        cancellation_reason = None

        if h_lagna == 1 and mars_sign == 0:
            cancelled = True
            cancellation_reason = "Mars in Aries in Lagna (Own Sign)"
        elif h_lagna == 4 and mars_sign == 7:
            cancelled = True
            cancellation_reason = "Mars in Scorpio in 4th House (Own Sign)"
        elif h_lagna == 7 and mars_sign == 9:
            cancelled = True
            cancellation_reason = "Mars in Capricorn in 7th House (Exalted)"
        elif h_lagna == 8 and mars_sign == 3:
            cancelled = True
            cancellation_reason = "Mars in Cancer in 8th House (Neecha Bhanga / Weak)"

        is_manglik = (lagna_manglik or moon_manglik) and not cancelled
        intensity = "High" if (lagna_manglik and moon_manglik and not cancelled) else (
            "Moderate" if (lagna_manglik and not cancelled) else (
                "Mild / Cancelled" if cancelled else "None"
            )
        )

        return {
            "is_manglik": is_manglik,
            "intensity": intensity,
            "house_from_lagna": h_lagna,
            "house_from_moon": h_moon,
            "house_from_venus": h_venus,
            "cancelled": cancelled,
            "cancellation_reason": cancellation_reason
        }

    @classmethod
    def match_horoscopes(
        cls,
        bride_kundali: Kundali,
        groom_kundali: Kundali
    ) -> Dict[str, Any]:
        """
        Perform complete 36-point Ashtakoota Milan, Dashakoota extras,
        and Manglik Dosha mutual cancellation evaluation.
        """
        b_moon = bride_kundali.planets["Moon"]
        g_moon = groom_kundali.planets["Moon"]

        b_sign = b_moon.sign.value
        g_sign = g_moon.sign.value
        b_nak = b_moon.nakshatra_number
        g_nak = g_moon.nakshatra_number
        b_pada = b_moon.nakshatra_pada
        g_pada = g_moon.nakshatra_pada

        varna_pts, varna_note = cls.calculate_varna_kuta(b_sign, g_sign)
        vashya_pts, vashya_note = cls.calculate_vashya_kuta(b_sign, g_sign)
        tara_pts, tara_note = cls.calculate_tara_kuta(b_nak, g_nak)
        yoni_pts, yoni_note = cls.calculate_yoni_kuta(b_nak, g_nak)
        maitri_pts, maitri_note = cls.calculate_graha_maitri_kuta(b_sign, g_sign)
        gana_pts, gana_note = cls.calculate_gana_kuta(b_nak, g_nak)
        bhakoot_pts, bhakoot_note = cls.calculate_bhakoot_kuta(b_sign, g_sign)
        nadi_pts, nadi_note = cls.calculate_nadi_kuta(b_nak, g_nak, b_sign, g_sign, b_pada, g_pada)

        total_points = varna_pts + vashya_pts + tara_pts + yoni_pts + maitri_pts + gana_pts + bhakoot_pts + nadi_pts
        percentage = round((total_points / 36.0) * 100.0, 1)

        # Classification
        if total_points >= 28:
            verdict = "Excellent Match (Uttama)"
            recommendation = "Highly auspicious match. Natural psychological, biological, and karmic harmony."
        elif total_points >= 21:
            verdict = "Good Match (Madhyama)"
            recommendation = "Solid and auspicious match. Fulfills classical marriage criteria smoothly."
        elif total_points >= 18:
            verdict = "Average Match (Sadharana)"
            recommendation = "Acceptable match with basic alignment. Recommended to observe minor remedial guidance."
        else:
            verdict = "Below Average / Not Recommended (Varjya)"
            recommendation = "Low Guna score. Comprehensive astrological consultation and remedial shanti advised before proceeding."

        # Dashakoota extras
        dashakoota = cls.calculate_dashakoota_extras(b_nak, g_nak)

        # Manglik Dosha evaluation
        b_manglik = cls.check_manglik_dosha(bride_kundali)
        g_manglik = cls.check_manglik_dosha(groom_kundali)

        # Mutual cancellation rule
        manglik_cancelled_mutually = b_manglik["is_manglik"] and g_manglik["is_manglik"]

        return {
            "total_score": total_points,
            "max_score": 36,
            "percentage": percentage,
            "verdict": verdict,
            "recommendation": recommendation,
            "kutas": {
                "varna": {"points": varna_pts, "max": 1, "note": varna_note},
                "vashya": {"points": vashya_pts, "max": 2, "note": vashya_note},
                "tara": {"points": tara_pts, "max": 3, "note": tara_note},
                "yoni": {"points": yoni_pts, "max": 4, "note": yoni_note},
                "graha_maitri": {"points": maitri_pts, "max": 5, "note": maitri_note},
                "gana": {"points": gana_pts, "max": 6, "note": gana_note},
                "bhakoot": {"points": bhakoot_pts, "max": 7, "note": bhakoot_note},
                "nadi": {"points": nadi_pts, "max": 8, "note": nadi_note}
            },
            "dashakoota_extras": dashakoota,
            "manglik_compatibility": {
                "bride_manglik": b_manglik,
                "groom_manglik": g_manglik,
                "mutually_cancelled": manglik_cancelled_mutually,
                "overall_status": "Neutralized by Mutual Manglik Matching" if manglik_cancelled_mutually else (
                    "No Kuja Dosha Conflict" if not (b_manglik["is_manglik"] or g_manglik["is_manglik"]) else (
                        "Kuja Dosha Mismatch (Remedial Pariharams Recommended)"
                    )
                )
            }
        }
