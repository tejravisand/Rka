"""
Lal Kitab (Red Book) Astrology Engine.
Implements:
1. Lal Kitab Pakka Ghar (Permanent House Significations) and House Placements.
2. Sleeping Houses (Soya Ghar) and Sleeping Planets (Soya Grah) detection.
3. Masnuyi (Synthetic / Artificial) Planetary Interactions.
4. Karmic Debts (Rin) Analysis:
   - Pitru Rin (Forefathers' Debt)
   - Matru Rin (Mother's Debt)
   - Stri Rin (Wife / Women's Debt)
   - Swa Rin (Self / Soul Debt)
   - Kanya / Behan Rin (Daughter / Sister Debt)
   - Zaaliman Rin (Cruelty Debt)
   - Kudrati Rin (Divine / Nature's Debt)
5. Practical Lal Kitab Totke / Upayas tailored to current query and planetary afflictions.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.models.astrological import Kundali, PlanetPosition


# Lal Kitab Permanent House Rulers (Pakka Ghar)
LAL_KITAB_PAKKA_GHAR = {
    1: {"planet": "Sun / Mars", "sign": "Aries", "signification": "Self, vitality, honor, initiative"},
    2: {"planet": "Jupiter / Venus", "sign": "Taurus", "signification": "Wealth, family temple, speech, accumulated assets"},
    3: {"planet": "Mars / Mercury", "sign": "Gemini", "signification": "Brothers, courage, hands, enterprise"},
    4: {"planet": "Moon", "sign": "Cancer", "signification": "Mother, ancestral peace, cold water, pure emotions"},
    5: {"planet": "Jupiter / Sun", "sign": "Leo", "signification": "Children, intellect, fame, future destiny"},
    6: {"planet": "Mercury / Ketu", "sign": "Virgo", "signification": "Maternal uncle, debts, illnesses, underground energies"},
    7: {"planet": "Venus / Mercury", "sign": "Libra", "signification": "Spouse, domestic happiness, partnerships, daily commerce"},
    8: {"planet": "Mars / Saturn", "sign": "Scorpio", "signification": "Longevity, sudden shocks, secrets, occult depths"},
    9: {"planet": "Jupiter", "sign": "Sagittarius", "signification": "Father, religion, fortune, divine grace"},
    10: {"planet": "Saturn", "sign": "Capricorn", "signification": "Profession, karmic deeds, authority, government ties"},
    11: {"planet": "Saturn / Jupiter", "sign": "Aquarius", "signification": "Income, elder siblings, worldly gains, wishes"},
    12: {"planet": "Jupiter / Rahu", "sign": "Pisces", "signification": "Expenditure, bedroom, overseas, spiritual liberation"}
}


@dataclass
class LalKitabDebt:
    debt_name: str
    is_present: bool
    afflicted_planet: str
    cause: str
    symptoms_in_life: str
    farman_remedy: str


@dataclass
class LalKitabHouseState:
    house_number: int
    pakka_lord: str
    planets_present: List[str]
    is_sleeping: bool
    activation_upaya: str


@dataclass
class LalKitabAssessment:
    sleeping_houses: List[int]
    active_karmic_debts: List[LalKitabDebt]
    masnuyi_influences: List[str]
    specific_totke_for_query: List[str]
    general_lal_kitab_rules: List[str]


class LalKitabEngine:
    """Lal Kitab calculation and remediation engine."""

    @classmethod
    def evaluate_kundali(
        cls,
        kundali: Kundali,
        query_category: str
    ) -> LalKitabAssessment:
        """
        Maps the native's chart to Lal Kitab principles and evaluates sleeping houses,
        karmic debts (Rin), and authentic upayas.
        """
        # Determine planets in each house (1 to 12)
        house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
        lagna_sign = kundali.ascendant.sign.value

        planet_house_map: Dict[str, int] = {}
        for p_name, p_pos in kundali.planets.items():
            h_num = (p_pos.sign.value - lagna_sign) % 12 + 1
            house_planets[h_num].append(p_name)
            planet_house_map[p_name] = h_num

        # 1. Sleeping Houses (Soya Ghar)
        sleeping_houses = [h for h, plist in house_planets.items() if len(plist) == 0]

        # 2. Masnuyi (Synthetic) Planets Evaluation
        masnuyi_notes = []
        sun_h = planet_house_map.get("Sun")
        sat_h = planet_house_map.get("Saturn")
        mars_h = planet_house_map.get("Mars")
        mer_h = planet_house_map.get("Mercury")
        ven_h = planet_house_map.get("Venus")
        jup_h = planet_house_map.get("Jupiter")
        rahu_h = planet_house_map.get("Rahu")
        ketu_h = planet_house_map.get("Ketu")

        if sun_h == sat_h:
            masnuyi_notes.append("Sun + Saturn Conjunction creates Masnuyi Venus effect (Requires balancing marriage and status).")
        if mars_h == mer_h:
            masnuyi_notes.append("Mars + Mercury Conjunction creates Masnuyi Ketu effect (Sudden sharp intellect and quick reactions).")
        if sun_h == ven_h:
            masnuyi_notes.append("Sun + Venus Conjunction creates Masnuyi Ketu effect (Need to nourish eyesight and family vitality).")
        if jup_h == sat_h:
            masnuyi_notes.append("Jupiter + Saturn Conjunction creates Masnuyi Rahu effect (High vision, but prone to sudden delays).")

        # 3. Karmic Debts (Rin) Detection
        debts: List[LalKitabDebt] = []

        # Pitru Rin (Forefathers' Debt): Jupiter afflicted by Venus/Mercury/Saturn or in 6/8/12
        pitru_afflicted = jup_h in [6, 8, 10] or (jup_h in [ven_h, mer_h, sat_h])
        debts.append(LalKitabDebt(
            debt_name="Pitru Rin (Forefathers' Karmic Debt)",
            is_present=pitru_afflicted,
            afflicted_planet="Jupiter (Guru)",
            cause="Ancestors engaged in temple disrespect or breach of trust with religious teachers.",
            symptoms_in_life="Unexplained delays in career recognition, lack of paternal support, fluctuating prosperity.",
            farman_remedy=(
                "Collect equal money/grains from all blood relatives and perform service/donation at a temple. "
                "Water the sacred Peepal tree without touching its roots on Thursdays; offer yellow saffron tilak daily."
            )
        ))

        # Matru Rin (Mother's Debt): Moon afflicted by Ketu or in 6th/8th
        matru_afflicted = planet_house_map.get("Moon") in [6, 8] or (planet_house_map.get("Moon") == ketu_h)
        debts.append(LalKitabDebt(
            debt_name="Matru Rin (Mother's / Water Debt)",
            is_present=matru_afflicted,
            afflicted_planet="Moon (Chandra)",
            cause="Disrespect to mother, disrespecting water bodies, or causing grief to animals.",
            symptoms_in_life="Mental agitation, sudden cash-flow dryness, emotional insecurity, frequent head cold.",
            farman_remedy=(
                "Collect equal silver coins or silver pieces from all blood relatives and immerse them in a running river. "
                "Always touch mother's feet and take her blessings before beginning important journeys or investments."
            )
        ))

        # Stri Rin (Wife's / Women's Debt): Venus afflicted by Rahu/Sun/Mars or in 6th
        stri_afflicted = ven_h in [6] or (ven_h in [rahu_h, sun_h])
        debts.append(LalKitabDebt(
            debt_name="Stri Rin (Women's / Laxmi Debt)",
            is_present=stri_afflicted,
            afflicted_planet="Venus (Shukra)",
            cause="Harsh behavior toward women or dishonoring sacred matrimonial bonds in past lineage.",
            symptoms_in_life="Marital friction, obstacles in purchasing luxury comforts, sudden domestic misunderstandings.",
            farman_remedy=(
                "Feed 100 cows with green grass, fodder, or unrefined jaggery (Gud). "
                "Keep a clean white fragrant square silk handkerchief; offer pure cow ghee at Lakshmi temple on Fridays."
            )
        ))

        # Swa Rin (Self / Soul Debt): Sun afflicted by Saturn or Rahu or in 10th/11th
        swa_afflicted = sun_h in [sat_h, rahu_h] or sun_h in [6, 8]
        debts.append(LalKitabDebt(
            debt_name="Swa Rin (Self / Soul Karmic Debt)",
            is_present=swa_afflicted,
            afflicted_planet="Sun (Surya)",
            cause="Past life misuse of royal power, breach of duty toward community or elders.",
            symptoms_in_life="Lack of recognition despite heavy hard work, government or administrative friction, fatigue.",
            farman_remedy=(
                "Collect equal copper coins from blood relatives and perform a Surya Arghya / Homa. "
                "Float a round copper coin with a central hole in a flowing freshwater river on Sunday before noon."
            )
        ))

        # Kanya / Behan Rin (Daughter / Sister Debt): Mars afflicted by Mercury or Ketu in 3rd/6th
        kanya_afflicted = mars_h in [mer_h, ketu_h] or (mars_h in [3, 6] and mer_h in [1, 7])
        debts.append(LalKitabDebt(
            debt_name="Kanya / Behan Rin (Sister / Daughter Debt)",
            is_present=kanya_afflicted,
            afflicted_planet="Mars & Mercury (Mangala-Budha)",
            cause="Depriving sisters, daughters, or young girls of their rightful joy, dowry, or inheritance.",
            symptoms_in_life="Fluctuating speech, sudden business misunderstandings, tension with siblings.",
            farman_remedy=(
                "Distribute yellow sweets and green clothes to young girls (Kanya Puja); gift silver items to sisters. "
                "Pierce ears/nose with gold (or wear gold studs) to pacify the negative vibrations."
            )
        ))

        # Zaaliman Rin (Cruelty / Tyranny Debt): Saturn afflicted by Sun or Mars
        zaaliman_afflicted = sat_h in [sun_h, mars_h] or sat_h in [1, 2]
        debts.append(LalKitabDebt(
            debt_name="Zaaliman Rin (Cruelty / Labor Debt)",
            is_present=zaaliman_afflicted,
            afflicted_planet="Saturn (Shani)",
            cause="Harassment of servants, laborers, stray animals, or taking land unjustly.",
            symptoms_in_life="Sudden legal hassles, joint/bone stiffness, recurring delays in building/buying property.",
            farman_remedy=(
                "Feed 100 fish with flour balls (Aata peda); regularly feed black stray dogs with sweet tandoori rotis. "
                "Never accept iron items, electronic goods, or leather goods free of charge."
            )
        ))

        # Kudrati Rin (Nature's / Divine Debt): Rahu or Ketu in adverse mutual affliction
        kudrati_afflicted = (rahu_h in [1, 5, 9]) and (sat_h in [6, 8, 12])
        debts.append(LalKitabDebt(
            debt_name="Kudrati Rin (Divine / Nature's Debt)",
            is_present=kudrati_afflicted,
            afflicted_planet="Rahu & Ketu",
            cause="Harm caused to innocent creatures, destruction of bird nests, or disrespect to nature.",
            symptoms_in_life="Sudden unexpected phantom fears, sleeplessness, erratic highs and lows.",
            farman_remedy=(
                "Feed sweet porridge or grains to ants and wild birds every day. "
                "Keep a small silver box containing pure river sand or a pearl at home; serve physically challenged people."
            )
        ))

        # Filter active debts
        active_debts = [d for d in debts if d.is_present]

        # 4. Specific Totke (Remedies) for Query Category
        cat_lower = query_category.lower()
        specific_totke = []

        if any(w in cat_lower for w in ["job", "career", "promotion", "business", "work"]):
            specific_totke.extend([
                "Float a round copper coin with a central hole in a running clean river on a Sunday morning (removes Rahu-Sun career blockage).",
                "Feed 10 sweet rotis (cooked on an open flame with jaggery) to a stray black dog on Saturday evenings.",
                "Keep a pure solid square piece of silver (approx 1x1 inch) in your wallet or chest pocket at all times.",
                "Never keep non-functional wristwatches, dead wall clocks, or rusted iron scrap in your work premises."
            ])
        elif any(w in cat_lower for w in ["marriage", "relationship", "spouse", "love"]):
            specific_totke.extend([
                "Offer a pair of unboiled sweet curd (dahi) and unrefined sugar at a Lakshmi-Narayana temple for 7 consecutive Fridays.",
                "Feed cows with freshly kneaded dough balls rolled in turmeric and jaggery.",
                "Keep a small round silver ball in a clean pouch in your bedroom.",
                "Avoid wearing murky dark brown or unwashed clothing on Fridays."
            ])
        elif any(w in cat_lower for w in ["property", "land", "house", "real estate"]):
            specific_totke.extend([
                "Bury a small rectangular copper coin or terracotta pot with honey in an uninhabited earthen land (pacifies Mars).",
                "Light a mustard oil lamp at the base of a Shami or Peepal tree on Saturday evening.",
                "Feed crows with fried snacks (savories) and biscuits before starting property registrations.",
                "Never accept building materials or iron tools as free gifts."
            ])
        elif any(w in cat_lower for w in ["foreign", "visa", "abroad", "relocation"]):
            specific_totke.extend([
                "Feed whole yellow bananas or soaked chana dal to temple elephants or sacred cows on Thursdays.",
                "Float 8 dry coconuts with coir in flowing water on a Wednesday evening (pacifies Rahu foreign blockage).",
                "Keep a small flask of holy Ganga water sealed with a silver lid in the North-East of your home.",
                "Wear an unjointed pure brass bangle on your right wrist."
            ])
        elif any(w in cat_lower for w in ["finance", "money", "debt", "wealth"]):
            specific_totke.extend([
                "Place a solid pure silver square in your cash locker or business safe wrapped in yellow silk.",
                "Feed stray cows with green spinach or fodder every Wednesday.",
                "Never let the tap in your bathroom or kitchen drip; repair leaking water immediately to stop financial leakage.",
                "Offer milk mixed with saffron to the roots of a Banyan tree on Thursdays."
            ])
        else:
            specific_totke.extend([
                "Chant Maha Mrityunjaya Mantra 11 times daily and feed stray birds with mixed grains (Satnaja).",
                "Keep a solid silver square piece in your pocket for emotional tranquility.",
                "Donate black blankets or warm clothes to needy laborers on Saturdays."
            ])

        # 5. General Lal Kitab Farman Golden Rules
        general_rules = [
            "Never accept free gifts, electrical gadgets, or secondhand iron machinery from outsiders.",
            "Always maintain cordial relationships with in-laws and maternal uncles to avoid Rahu and Mercury afflictions.",
            "Keep the main entrance and North-East corner of the residence impeccably clean and clutter-free.",
            "Do not consume alcohol or non-vegetarian food on Tuesdays, Thursdays, and Saturdays.",
            "Always touch the feet of elderly family members before commencing major endeavors."
        ]

        return LalKitabAssessment(
            sleeping_houses=sleeping_houses,
            active_karmic_debts=active_debts,
            masnuyi_influences=masnuyi_notes,
            specific_totke_for_query=specific_totke,
            general_lal_kitab_rules=general_rules
        )
