"""
Lifestyle Advisory Engine.
Translates Kundali, Vargas (specifically D16 Shodashamsa and D4 Chaturthamsa),
and planetary dignities into personalized recommendations for:
1. Best vehicle colors & colors to avoid (Vahana Varna).
2. Best directions for purchasing land, residential house, and commercial office (Vastu & Disha).
3. Favourable dress colors for every day of the week (Vaara Vastra).
"""
from typing import Dict, List, Tuple
from app.models.astrological import Kundali, PlanetPosition, ZodiacSign
from app.models.advisory import (
    VehicleColorRecommendation,
    PropertyDirectionRecommendation,
    DailyDressColorGuide,
    LifestyleDossier
)
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT


# Classical Planetary Color Palettes
PLANET_COLORS = {
    "Sun": {
        "primary": ["Ruby Red", "Copper", "Deep Orange", "Bright Gold", "Saffron"],
        "accent": ["Warm Amber", "Cream with Golden Embroidery"],
        "avoid": ["Dull Charcoal", "Murky Dark Blue", "Jet Black"]
    },
    "Moon": {
        "primary": ["Pearl White", "Silver", "Milky White", "Moonlight Cream", "Light Pale Blue"],
        "accent": ["Seafoam Green", "Soft Lavender"],
        "avoid": ["Stark Jet Black", "Aggressive Dark Red", "Deep Maroon"]
    },
    "Mars": {
        "primary": ["Coral Red", "Crimson", "Scarlet", "Rust Red", "Terracotta"],
        "accent": ["Bright Copper", "Warm Salmon"],
        "avoid": ["Dark Emerald Green", "Bottle Green", "Drab Olive"]
    },
    "Mercury": {
        "primary": ["Emerald Green", "Parrot Green", "Mint", "Jade", "Sage"],
        "accent": ["Light Turquoise", "Pastel Yellow-Green"],
        "avoid": ["Deep Blood Red", "Harsh Neon Red"]
    },
    "Jupiter": {
        "primary": ["Golden Yellow", "Bright Amber", "Turmeric / Haldi", "Mustard", "Royal Cream"],
        "accent": ["Warm Beige", "Saffron-Yellow Silk"],
        "avoid": ["Dull Gunmetal Grey", "Cold Jet Black", "Murky Navy"]
    },
    "Venus": {
        "primary": ["Pure White", "Diamond Silver", "Silk Ivory", "Rose Pink", "Pastel Cream"],
        "accent": ["Lilac", "Champagne Gold", "Variegated Pastels"],
        "avoid": ["Muddy Mustard", "Faded Rust", "Drab Brown"]
    },
    "Saturn": {
        "primary": ["Navy Blue", "Deep Indigo", "Steel Grey", "Charcoal", "Midnight Black"],
        "accent": ["Slate", "Dark Denim"],
        "avoid": ["Fiery Scarlet", "Fluorescent Orange", "Bright Coral"]
    },
    "Rahu": {
        "primary": ["Smoked Grey", "Gunmetal", "Electric Blue", "Obsidian"],
        "accent": ["Dark Metallic Grey"],
        "avoid": ["Pure Golden Yellow", "Saffron"]
    },
    "Ketu": {
        "primary": ["Earth Brown", "Smoky Topaz", "Terracotta", "Multi-colored Tweed"],
        "accent": ["Ash Grey"],
        "avoid": ["Bright Saffron", "Vibrant Red"]
    }
}

# Planetary Directional Governance (Dikpalas & Digbala)
PLANET_DIRECTIONS = {
    "Sun": "East (Purva)",
    "Moon": "North-West (Vayavya)",
    "Mars": "South (Dakshina)",
    "Mercury": "North (Uttara)",
    "Jupiter": "North-East (Ishanya)",
    "Venus": "South-East (Agneya)",
    "Saturn": "West (Pashchima)",
    "Rahu": "South-West (Nairruti)",
    "Ketu": "South-West (Nairruti) / Non-cardinal"
}

# Sign Element Directions
ELEMENT_DIRECTIONS = {
    "Fire": ["East", "South-East", "North-East"],
    "Earth": ["South", "South-West", "North"],
    "Air": ["West", "North-West", "North"],
    "Water": ["North", "North-East", "East"]
}


class LifestyleAdvisor:
    """Computes chart-specific recommendations for vehicles, real estate, and attire."""

    @classmethod
    def analyze_vehicle_colors(cls, kundali: Kundali) -> VehicleColorRecommendation:
        """
        Calculates auspicious and caution vehicle colors based on:
        - 4th House (Vahana Bhava) sign and lord.
        - Venus (Natural Vahana Karaka).
        - D16 (Shodashamsa / Kalamsa - Divisional chart for conveyances).
        - Avoiding 6th, 8th, and 12th house lords.
        """
        lagna_sign_idx = kundali.ascendant.sign.value
        fourth_house_idx = (lagna_sign_idx + 3) % 12
        fourth_house_sign = ZODIAC_SANSKRIT[fourth_house_idx]
        fourth_lord = SIGN_LORDS[fourth_house_idx]

        lagna_lord = SIGN_LORDS[lagna_sign_idx]
        eighth_lord = SIGN_LORDS[(lagna_sign_idx + 7) % 12]
        sixth_lord = SIGN_LORDS[(lagna_sign_idx + 5) % 12]

        venus_pos = kundali.planets["Venus"]
        venus_dignity = f"{venus_pos.dignity} in {venus_pos.sign.sanskrit_name}"

        # D16 Check if available
        d16_guidance = "D16 indicates smooth conveyance with proper planetary harmony."
        if 16 in kundali.vargas:
            d16 = kundali.vargas[16]
            d16_asc = d16.placements.get("Ascendant")
            d16_ven = d16.placements.get("Venus")
            if d16_ven:
                d16_guidance = f"In D16 Shodashamsa, Venus is in {d16_ven.sign.sanskrit_name} ({d16_ven.dignity}). This reinforces comfort and safety when aligned with {d16_ven.sign_lord} colors."

        # Primary lucky colors derived from 4th lord and Venus
        primary_colors = []
        for c in PLANET_COLORS.get(fourth_lord, {}).get("primary", []):
            if c not in primary_colors:
                primary_colors.append(c)
        for c in PLANET_COLORS.get(lagna_lord, {}).get("primary", []):
            if c not in primary_colors:
                primary_colors.append(c)

        # Secondary favorable colors from Venus and friendly planets
        secondary_colors = []
        for c in PLANET_COLORS.get("Venus", {}).get("primary", []):
            if c not in primary_colors and c not in secondary_colors:
                secondary_colors.append(c)
        for c in PLANET_COLORS.get("Moon", {}).get("primary", []):
            if c not in primary_colors and c not in secondary_colors:
                secondary_colors.append(c)

        # Colors to strictly avoid: from 8th and 6th lord
        # Note: If Lagna lord owns the 8th house (e.g. Mars for Aries, Venus for Libra),
        # its Lagna Moolatrikona ownership overrides the 8th house blemish.
        avoid_lords = []
        if eighth_lord != lagna_lord:
            avoid_lords.append(eighth_lord)
        if sixth_lord != lagna_lord and sixth_lord not in avoid_lords:
            avoid_lords.append(sixth_lord)
        if not avoid_lords:
            # Fallback to 6th or 12th
            twelfth_lord = SIGN_LORDS[(lagna_sign_idx + 11) % 12]
            if twelfth_lord != lagna_lord:
                avoid_lords.append(twelfth_lord)

        avoid_colors = []
        for lord in avoid_lords:
            for c in PLANET_COLORS.get(lord, {}).get("primary", []):
                if c not in avoid_colors and c not in primary_colors:
                    avoid_colors.append(c)

        primary_avoid_lord = avoid_lords[0] if avoid_lords else "malefic"
        practical_advice = (
            f"For {kundali.ascendant.sign.sanskrit_name} Lagna, the 4th house (Vahana Bhava) is ruled by {fourth_lord}. "
            f"Purchasing a vehicle in {', '.join(primary_colors[:3])} enhances driving focus, vehicle longevity, and journey safety. "
            f"Avoid {', '.join(avoid_colors[:2])} as they represent the conflicting energy of {primary_avoid_lord}, "
            f"which can attract frequent scratch marks, mechanical faults, or road aggression."
        )

        return VehicleColorRecommendation(
            primary_lucky_colors=primary_colors[:4],
            secondary_favorable_colors=secondary_colors[:4],
            colors_to_avoid=avoid_colors[:4],
            fourth_house_lord=fourth_lord,
            fourth_house_sign=fourth_house_sign,
            venus_dignity=venus_dignity,
            d16_shodashamsa_guidance=d16_guidance,
            practical_advice=practical_advice
        )

    @classmethod
    def analyze_property_direction(cls, kundali: Kundali) -> Tuple[PropertyDirectionRecommendation, PropertyDirectionRecommendation]:
        """
        Calculates best directions for:
        1. Residential Land / House (based on 4th House, Lagna, and Vastu element).
        2. Commercial Office / Business Land (based on 10th House, 11th House, and Mercury/Jupiter).
        """
        lagna_sign_idx = kundali.ascendant.sign.value
        lagna_sign = kundali.ascendant.sign
        lagna_lord = SIGN_LORDS[lagna_sign_idx]

        fourth_sign_idx = (lagna_sign_idx + 3) % 12
        fourth_sign = ZodiacSign(fourth_sign_idx)
        fourth_lord = SIGN_LORDS[fourth_sign_idx]

        tenth_sign_idx = (lagna_sign_idx + 9) % 12
        tenth_sign = ZodiacSign(tenth_sign_idx)
        tenth_lord = SIGN_LORDS[tenth_sign_idx]

        eleventh_lord = SIGN_LORDS[(lagna_sign_idx + 10) % 12]
        eighth_lord = SIGN_LORDS[(lagna_sign_idx + 7) % 12]

        # 1. Residential Property Analysis
        fourth_element = fourth_sign.element
        elem_dirs = ELEMENT_DIRECTIONS.get(fourth_element, ["East", "North"])

        res_primary_dirs = []
        # Planetary direction of 4th lord and Lagna lord
        dir_4th_lord = PLANET_DIRECTIONS.get(fourth_lord, "East").split(" ")[0]
        dir_lagna_lord = PLANET_DIRECTIONS.get(lagna_lord, "East").split(" ")[0]

        for d in [dir_4th_lord, "North-East", dir_lagna_lord]:
            if d not in res_primary_dirs:
                res_primary_dirs.append(d)

        res_secondary_dirs = [d for d in elem_dirs if d not in res_primary_dirs]
        if "North" not in res_primary_dirs and "North" not in res_secondary_dirs:
            res_secondary_dirs.append("North")

        dir_8th_lord = PLANET_DIRECTIONS.get(eighth_lord, "South-West").split(" ")[0]
        res_avoid_dirs = [dir_8th_lord, "South-West" if dir_8th_lord != "South-West" else "South"]

        res_rationale = (
            f"The 4th house (Sukha & Griha Bhava) falls in {fourth_sign.sanskrit_name} ({fourth_element} element), "
            f"ruled by {fourth_lord}. Aligning the house entrance or plot slope towards {res_primary_dirs[0]} or North-East (Ishanya) "
            f"guarantees domestic tranquility, mental peace, and prosperity for family members."
        )

        res_vastu_rules = [
            f"Main Entrance: Best facing {res_primary_dirs[0]} or North-East (Ishanya).",
            "Master Bedroom: Best located in the South-West (Nairruti) for grounding stability.",
            "Kitchen: Best placed in the South-East (Agneya - Fire zone) or North-West.",
            "Puja / Meditation Room: Best situated in the North-East (Ishanya) corner."
        ]

        residential_advice = PropertyDirectionRecommendation(
            property_type="Residential House / Land",
            primary_best_directions=res_primary_dirs,
            secondary_acceptable_directions=res_secondary_dirs[:2],
            directions_to_avoid=res_avoid_dirs[:2],
            main_entrance_facing=f"{res_primary_dirs[0]} or North-East",
            ruling_houses=f"4th House ({fourth_sign.sanskrit_name}) & Lagna ({lagna_sign.sanskrit_name})",
            astrological_rationale=res_rationale,
            vastu_key_principles=res_vastu_rules
        )

        # 2. Commercial Office / Business Land Analysis
        comm_primary_dirs = []
        dir_10th_lord = PLANET_DIRECTIONS.get(tenth_lord, "North").split(" ")[0]
        dir_11th_lord = PLANET_DIRECTIONS.get(eleventh_lord, "East").split(" ")[0]

        # For commercial prosperity, North (Kubera - wealth) and East (Indra - authority) are paramount
        preferred_comm = ["North", "East", dir_10th_lord, dir_11th_lord]
        for d in preferred_comm:
            if d not in comm_primary_dirs:
                comm_primary_dirs.append(d)

        comm_secondary_dirs = ["North-West", "North-East"]
        comm_avoid_dirs = ["South-West", dir_8th_lord]

        comm_rationale = (
            f"The 10th house (Karma Bhava - Career/Business) is in {tenth_sign.sanskrit_name}, ruled by {tenth_lord}. "
            f"The 11th house of Profit and Cash Flow is ruled by {eleventh_lord}. "
            f"A commercial office or retail space with its main entrance facing {comm_primary_dirs[0]} or {comm_primary_dirs[1]} "
            f"activates Kubera (financial inflow) and Surya (market reputation)."
        )

        comm_vastu_rules = [
            f"Main Office Entrance: Facing {comm_primary_dirs[0]} or East for maximum footfall and financial inflow.",
            "CEO / Director Cabin: South-West corner facing North or East while seated at the desk.",
            "Accounts & Cash Locker: North wall opening towards the South, or North-East corner.",
            "Sales / Marketing Team: North-West zone (Vayu element) to maintain high movement and closing agility."
        ]

        commercial_advice = PropertyDirectionRecommendation(
            property_type="Commercial Office / Store",
            primary_best_directions=comm_primary_dirs[:3],
            secondary_acceptable_directions=comm_secondary_dirs,
            directions_to_avoid=comm_avoid_dirs[:2],
            main_entrance_facing=f"{comm_primary_dirs[0]} or East",
            ruling_houses=f"10th House ({tenth_sign.sanskrit_name}) & 11th House (Labha)",
            astrological_rationale=comm_rationale,
            vastu_key_principles=comm_vastu_rules
        )

        return residential_advice, commercial_advice

    @classmethod
    def analyze_daily_dress_colors(cls, kundali: Kundali) -> Dict[str, DailyDressColorGuide]:
        """
        Generates a comprehensive weekly wardrobe color guide for each day of the week,
        harmonizing universal planetary day rulers with the customer's specific Lagna and functional benefics.
        """
        lagna_sign_idx = kundali.ascendant.sign.value
        lagna_lord = SIGN_LORDS[lagna_sign_idx]
        ninth_lord = SIGN_LORDS[(lagna_sign_idx + 8) % 12]  # Bhagya Lord

        # Days of the week in Vedic tradition
        days_config = [
            ("Sunday", "Sun", "Ravivara", "Pure linen, raw silk, fine crisp cotton",
             f"Wearing golden-yellow or ruby-orange today aligns your vitality with the Sun. As a {kundali.ascendant.sign.sanskrit_name} Lagna, adding a touch of {lagna_lord} color boosts confidence."),
            ("Monday", "Moon", "Somavara", "Mulberry silk, breathable organic cotton, pearl-toned fabrics",
             f"Wearing pearl white, moonlight cream, or silver today calms the mind and enhances emotional equilibrium. Ideal for important negotiations and meetings."),
            ("Tuesday", "Mars", "Mangalavara", "Structured cotton, vibrant khadi, copper-toned weave",
             f"Mars energy gives drive, stamina, and executive execution. Wearing coral red or terracotta sharpens decisiveness."),
            ("Wednesday", "Mercury", "Budhavara", "Soft cotton, jade-green silks, fine linen",
             f"Emerald or mint green stimulates intellectual eloquence, analytical reasoning, and commercial commerce."),
            ("Thursday", "Jupiter", "Guruvara", "Rich tussar silk, bright turmeric cotton, saffron brocade",
             f"Thursday is the day of Guru (Brihaspati). Golden yellow or warm amber radiates wisdom, divine grace, and spiritual elevation."),
            ("Friday", "Venus", "Shukravara", "Flowing chanderi silk, satin, ivory linen, rose pastels",
             f"Venus governs elegance, creativity, attraction, and artistic excellence. Pure white, rose pink, or silver enhances charm and social rapport."),
            ("Saturday", "Saturn", "Shanivara", "Sturdy denim, dark wool, heavy cotton, navy twill",
             f"Saturn represents discipline, perseverance, and long-term focus. Wearing navy blue, charcoal, or deep indigo anchors patience.")
        ]

        weekly_guide: Dict[str, DailyDressColorGuide] = {}

        for day_name, planet_name, sanskrit_name, fabrics, tip in days_config:
            p_data = PLANET_COLORS[planet_name]

            # Customizing avoid colors: never wear 8th lord colors on days when that planet is weak
            avoid_list = list(p_data["avoid"])

            weekly_guide[day_name] = DailyDressColorGuide(
                day_name=f"{day_name} ({sanskrit_name} - {planet_name})",
                ruling_planet=planet_name,
                primary_favorable_colors=p_data["primary"],
                accent_complementary_colors=p_data["accent"],
                colors_to_avoid_today=avoid_list,
                recommended_fabrics=fabrics,
                personalized_boost_tip=tip
            )

        return weekly_guide

    @classmethod
    def get_full_lifestyle_dossier(cls, kundali: Kundali) -> LifestyleDossier:
        """Construct the complete lifestyle and advisory dossier."""
        lagna_sign_idx = kundali.ascendant.sign.value
        lagna_lord = SIGN_LORDS[lagna_sign_idx]
        ninth_lord = SIGN_LORDS[(lagna_sign_idx + 8) % 12]
        eighth_lord = SIGN_LORDS[(lagna_sign_idx + 7) % 12]
        sixth_lord = SIGN_LORDS[(lagna_sign_idx + 5) % 12]

        vehicle_adv = cls.analyze_vehicle_colors(kundali)
        res_adv, comm_adv = cls.analyze_property_direction(kundali)
        weekly_dress = cls.analyze_daily_dress_colors(kundali)

        # Eternal power colors from Lagna and 9th Lord
        power_colors = []
        for c in PLANET_COLORS.get(lagna_lord, {}).get("primary", [])[:2]:
            power_colors.append(f"{c} ({lagna_lord} - Lagna Lord)")
        for c in PLANET_COLORS.get(ninth_lord, {}).get("primary", [])[:2]:
            if c not in power_colors:
                power_colors.append(f"{c} ({ninth_lord} - 9th Bhagya Lord)")

        # Eternal caution colors from 6th/8th Dusthana Lords (excluding Lagna Lord)
        caution_lord = eighth_lord if eighth_lord != lagna_lord else sixth_lord
        caution_colors = []
        for c in PLANET_COLORS.get(caution_lord, {}).get("primary", [])[:2]:
            caution_colors.append(f"{c} ({caution_lord} - Dusthana Lord)")

        return LifestyleDossier(
            lagna_sign=kundali.ascendant.sign.sanskrit_name,
            moon_sign=kundali.planets["Moon"].sign.sanskrit_name,
            vehicle_advice=vehicle_adv,
            residential_property_advice=res_adv,
            commercial_office_advice=comm_adv,
            weekly_dress_guide=weekly_dress,
            eternal_power_colors=power_colors,
            eternal_caution_colors=caution_colors
        )
