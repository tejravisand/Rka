"""
Comprehensive Astrological Remedies Engine.
Provides complete, multi-tradition remedial prescriptions:
1. Vedic, Puranic, and Tantric / Bija Mantras (with prescribed counts, japa mala, and timings).
2. Sacred Plants & Trees Pradakshinam (Circumambulations with exact counts, days, timings, and rituals).
3. Authentic Lal Kitab Totke / Upayas.
4. Sacred Danam (Donations, food grains, metals, and recipients).
5. Gemstones, Rudraksha Mukhis, and Yantras.
6. Vratas, Fasting Guidelines, and Daily Lifestyle Upayas.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MantraPrescription:
    planet_or_deity: str
    vedic_mantra: str
    bija_mantra: str
    prescribed_japa_count: int
    japa_mala: str
    optimal_time: str
    facing_direction: str
    asana_color: str
    guidelines: str


@dataclass
class SacredPlantPradakshinam:
    plant_name: str
    sanskrit_name: str
    botanical_name: str
    presiding_deity: str
    associated_planets: List[str]
    prescribed_pradakshinam_rounds: int
    auspicious_day: str
    auspicious_timing: str
    ritual_offerings: List[str]
    sacred_sankalpa_shloka: str
    afflictions_cured: List[str]
    special_precautions: str


@dataclass
class GemstoneRudrakshaPrescription:
    primary_gemstone: str
    substitute_upratna: str
    metal: str
    finger_to_wear: str
    day_and_time_to_wear: str
    rudraksha_mukhi: str
    sacred_yantra: str
    energization_mantra: str


@dataclass
class DanamPrescription:
    item_name: str
    associated_planet: str
    suitable_day: str
    recipient: str
    significance: str


@dataclass
class ComprehensiveRemedialDossier:
    primary_mantras: List[MantraPrescription]
    sacred_plant_pradakshinams: List[SacredPlantPradakshinam]
    lal_kitab_upayas: List[str]
    danam_prescriptions: List[DanamPrescription]
    gemstone_rudraksha: GemstoneRudrakshaPrescription
    vratas_and_diet: List[str]
    lifestyle_and_energy_upayas: List[str]


# 1. Master Sacred Trees / Plants Pradakshinam Database
SACRED_PLANTS_CATALOG: Dict[str, SacredPlantPradakshinam] = {
    "Peepal": SacredPlantPradakshinam(
        plant_name="Peepal Tree (Ashvattha)",
        sanskrit_name="Ashvattha (Vriksha Raja)",
        botanical_name="Ficus religiosa",
        presiding_deity="Lord Vishnu & Lord Shani (Sanctified by Trimurti)",
        associated_planets=["Saturn", "Jupiter", "Rahu", "Ketu"],
        prescribed_pradakshinam_rounds=21,  # 7, 21, or 108
        auspicious_day="Saturday (for Saturn/Rahu) or Thursday (for Jupiter/Pitrus)",
        auspicious_timing="Morning between Sunrise and 9:30 AM (Strictly avoid touching after sunset)",
        ritual_offerings=[
            "Pure water mixed with raw unboiled cow milk, black sesame seeds (Til), and a little sugar",
            "Light a mustard oil (Sarson) or sesame oil (Til tel) lamp at the base on Saturdays",
            "Offer white flowers or yellow flowers at the root"
        ],
        sacred_sankalpa_shloka="Moolato Brahma-roopaya, Madhyato Vishnu-roopine, Agratah Shiva-roopaya, Vriksha-rajaya te namah.",
        afflictions_cured=[
            "Severe Shani Sade Sati and Kantaka/Ashtama Shani delays",
            "Pitru Dosha and delayed career promotions / stagnation",
            "Rahu-Ketu psychic restlessness, chronic anxiety, and obstacles in life milestones"
        ],
        special_precautions="Never touch the Peepal tree on Sundays or after sunset on any day. Circumambulate clockwise in a clean, footwear-free state."
    ),
    "Shami": SacredPlantPradakshinam(
        plant_name="Shami Tree (Jammi Chettu / Khejri)",
        sanskrit_name="Shami Vriksha",
        botanical_name="Prosopis cineraria",
        presiding_deity="Lord Shiva, Shani Bhagavan & Goddess Durga",
        associated_planets=["Saturn", "Mars"],
        prescribed_pradakshinam_rounds=19,  # 9 or 19
        auspicious_day="Saturday evening (Twilight / Sandhya Kaal) or Tuesday",
        auspicious_timing="Sunset to 7:30 PM (Sandhya Kaal)",
        ritual_offerings=[
            "Light an earthen lamp with sesame oil (Til tel) or mustard oil",
            "Offer blue Aparajita flowers and whole black urad dal grains at the base",
            "Sprinkle water mixed with red vermillion (kumkum) or chandan"
        ],
        sacred_sankalpa_shloka="Shami Shamayate Papam, Shami Shatru Vinashini, Arjunasya Dhanurdhari, Ramasya Priya Darshini.",
        afflictions_cured=[
            "Court litigations, rivalries, harassment by hidden enemies",
            "Severe Saturn debility, bone/joint ailments, acute workplace persecution",
            "Manglik Dosha and volatile anger pacification"
        ],
        special_precautions="Chant the Shami prayer while circumambulating. Best performed near a Shiva or Navagraha temple premises."
    ),
    "Tulsi": SacredPlantPradakshinam(
        plant_name="Holy Basil (Tulsi)",
        sanskrit_name="Vrinda / Tulasi",
        botanical_name="Ocimum sanctum",
        presiding_deity="Goddess Lakshmi & Lord Maha Vishnu / Krishna",
        associated_planets=["Mercury", "Venus", "Moon"],
        prescribed_pradakshinam_rounds=7,  # 3, 7, or 11
        auspicious_day="Daily (excluding Ekadashi, Sundays, and eclipses for plucking leaves)",
        auspicious_timing="Morning immediately after bath, facing East",
        ritual_offerings=[
            "Fresh clean water poured with devotion",
            "Pinch of turmeric (Haldi) and kumkum on the Vrindavan planter",
            "Pure cow-ghee earthen lamp in the morning or evening"
        ],
        sacred_sankalpa_shloka="Maha-Prasada Janani, Sarva Saubhagya Vardhini, Aadhi Vyadhi Haran Nityam, Tulasi Tvam Namostute.",
        afflictions_cured=[
            "Budha (Mercury) afflictions: speech stutter, business miscommunications, memory fatigue",
            "Financial leakage, domestic arguments, and negative electromagnetic vibrations",
            "Respiratory ailments and mental restlessness"
        ],
        special_precautions="Do not offer water or touch Tulsi on Sundays or late at night. Do not pluck leaves with fingernails."
    ),
    "Vata": SacredPlantPradakshinam(
        plant_name="Banyan Tree (Vata / Nyagrodha)",
        sanskrit_name="Vata Vriksha",
        botanical_name="Ficus benghalensis",
        presiding_deity="Lord Shiva, Lord Yama & Kala Bhairava",
        associated_planets=["Mars", "Saturn", "Sun"],
        prescribed_pradakshinam_rounds=28,  # 7 or 28
        auspicious_day="Tuesday morning or Amavasya / Purnima",
        auspicious_timing="Morning before 10:00 AM",
        ritual_offerings=[
            "Clean water mixed with red chandan (sandalwood) and unrefined jaggery",
            "Tie raw white cotton thread (Kacha Soot) 7 times around the main trunk",
            "Offer red flowers at the aerial roots"
        ],
        sacred_sankalpa_shloka="Namaste Vata Vrikshaya, Dirghayushe Namo Namah, Shivaya Sarva-bhutaya, Kshemam Kuru Sada Mama.",
        afflictions_cured=[
            "Ayushya (longevity) vulnerabilities, frequent accidents, fear of unnatural death",
            "Ancestral curse (Vamsha Dosha) and chronic inability to establish deep life roots",
            "Property disputes and unstable relocations"
        ],
        special_precautions="Approach with deep reverence; circumambulate in a quiet, meditative state."
    ),
    "Bilva": SacredPlantPradakshinam(
        plant_name="Bel Tree (Bilva)",
        sanskrit_name="Bilva Vriksha",
        botanical_name="Aegle marmelos",
        presiding_deity="Lord Shiva & Lord Surya Narayana",
        associated_planets=["Sun", "Mars"],
        prescribed_pradakshinam_rounds=11,  # 3, 11, or 21
        auspicious_day="Monday morning, Pradosham, or Sunday",
        auspicious_timing="Morning hours (before noon)",
        ritual_offerings=[
            "Fresh water mixed with unboiled milk and unbroken raw rice (Akshata)",
            "Offer trifoliate unblemished Bel leaves with chandan",
            "Light a pure cow-ghee lamp"
        ],
        sacred_sankalpa_shloka="Tridalam Trigunakaaram, Trinetram Cha Triyayusham, Trijanma Papa Samharam, Eka Bilvam Shivarpanam.",
        afflictions_cured=[
            "Sun afflictions: lack of government clearance, bureaucratic penalties, father-son friction",
            "Heart and spine vitality deficits, loss of vital stamina, self-doubt",
            "Elimination of three lifetimes of negative karmic residue"
        ],
        special_precautions="Ensure leaves offered are free of insect holes and always complete in groups of three leaflets."
    ),
    "Amla": SacredPlantPradakshinam(
        plant_name="Indian Gooseberry (Amla / Dhatri)",
        sanskrit_name="Dhatri Vriksha",
        botanical_name="Phyllanthus emblica",
        presiding_deity="Lord Vishnu & Goddess Maha Lakshmi",
        associated_planets=["Jupiter", "Venus", "Moon"],
        prescribed_pradakshinam_rounds=11,  # 11 or 27
        auspicious_day="Thursday or Shukla Paksha Ekadashi / Kartika Masa",
        auspicious_timing="Morning before 11:00 AM",
        ritual_offerings=[
            "Sweet water mixed with turmeric, unboiled milk, and yellow flowers",
            "Light a cow-ghee lamp at the base",
            "Offer a yellow or green thread around the stem"
        ],
        sacred_sankalpa_shloka="Dhatri Devi Namastestu, Vishnu-vakshasthala-sthite, Aayur Aarogyam Aishwaryam, Dehi Me Paramam Sukham.",
        afflictions_cured=[
            "Financial stagnation, depletion of accumulated family savings, sluggish trade",
            "Impaired digestion, skin luster degradation, and immune weakness",
            "Lack of spiritual illumination and Guru grace"
        ],
        special_precautions="Sitting or consuming meals under the shade of an Amla tree on Kartika Ekadashi brings supreme health."
    ),
    "Banana": SacredPlantPradakshinam(
        plant_name="Banana Tree (Kadali)",
        sanskrit_name="Kadali Vriksha",
        botanical_name="Musa acuminata / paradisiaca",
        presiding_deity="Lord Brihaspati (Guru) & Lord Vishnu",
        associated_planets=["Jupiter"],
        prescribed_pradakshinam_rounds=16,  # 9 or 16
        auspicious_day="Thursday morning",
        auspicious_timing="Morning between 7:00 AM and 9:00 AM",
        ritual_offerings=[
            "Water mixed with turmeric (Haldi) powder and a few drops of raw milk",
            "Offer soaked Chana Dal (split Bengal gram) and jaggery at the base",
            "Light a ghee lamp and tie a yellow moli (sacred thread) around the trunk"
        ],
        sacred_sankalpa_shloka="Om Gram Greem Groum Sah Gurave Namah. Devanam cha Rishinam cha Gurum Kanchana-sannibham.",
        afflictions_cured=[
            "Delayed marriage for brides, inability to find a suitable life partner",
            "Obstacles in higher education, institutional exams, and career promotions",
            "Childlessness / progeny complications (Putra Dosha)"
        ],
        special_precautions="The person performing this ritual should strictly abstain from consuming bananas on Thursdays."
    ),
    "Neem": SacredPlantPradakshinam(
        plant_name="Neem Tree (Vepa / Arishta)",
        sanskrit_name="Nimba Vriksha",
        botanical_name="Azadirachta indica",
        presiding_deity="Sheetala Mata, Goddess Mariamman & Durga",
        associated_planets=["Mars", "Ketu"],
        prescribed_pradakshinam_rounds=7,
        auspicious_day="Tuesday or Sunday morning",
        auspicious_timing="Morning before 9:00 AM",
        ritual_offerings=[
            "Water mixed with turmeric (Haldi) and neem leaves",
            "Apply vermillion (Sindoor/Kumkum) to the trunk",
            "Light a sesame oil deepam"
        ],
        sacred_sankalpa_shloka="Nimba-vriksha-nivasinyai, Sheetala-matre Namo Namah, Sarva-roga-prashamani, Shanti-dayini Te Namah.",
        afflictions_cured=[
            "Chronic skin infections, persistent blood impurities, fiery inflammation",
            "Banishment of evil eye (Drishti), psychic heaviness, phantom fears",
            "Anger flare-ups and Mars-Ketu psychic conflicts"
        ],
        special_precautions="Perform with reverence to the divine mother; use fresh morning well/tap water."
    )
}

# 2. Master Navagraha Mantras Database
NAVAGRAHA_MANTRAS: Dict[str, MantraPrescription] = {
    "Sun": MantraPrescription(
        planet_or_deity="Surya (Sun) / Aditya",
        vedic_mantra="Om Aadityaya Vidmahe Sahasra-kiranaya Dheemahi, Tanno Sooryah Prachodayaat.",
        bija_mantra="Om Hram Hreem Hroum Sah Suryaya Namah.",
        prescribed_japa_count=7000,
        japa_mala="Red Sandalwood (Rakta Chandana) or 12-Mukhi Rudraksha",
        optimal_time="Sunday morning at Sunrise",
        facing_direction="East",
        asana_color="Red or Saffron woolen mat",
        guidelines="Offer water (Arghya) in a pure copper pot with red kumkum and red flowers to the rising Sun before starting japa."
    ),
    "Moon": MantraPrescription(
        planet_or_deity="Chandra (Moon) / Shiva",
        vedic_mantra="Om Ksheera-putraya Vidmahe Amrita-tattvaya Dheemahi, Tanno Chandra-h Prachodayaat.",
        bija_mantra="Om Shram Shreem Shroum Sah Chandraya Namah.",
        prescribed_japa_count=11000,
        japa_mala="Sphatik (Crystal Quartz) or Pearl (Moti) Mala or 2-Mukhi Rudraksha",
        optimal_time="Monday evening or night (during Moon rise)",
        facing_direction="North-West",
        asana_color="White or Moonlight Cream silk mat",
        guidelines="Chant with a tranquil mind; keep pure water in a silver vessel nearby and sip it as consecrated theertha."
    ),
    "Mars": MantraPrescription(
        planet_or_deity="Mangala (Mars) / Kartikeya & Hanuman",
        vedic_mantra="Om Angarakaya Vidmahe Shakti-hastaya Dheemahi, Tanno Bhaumah Prachodayaat.",
        bija_mantra="Om Kram Kreem Kroum Sah Bhaumaya Namah.",
        prescribed_japa_count=10000,
        japa_mala="Red Coral (Moonga) or 3-Mukhi Rudraksha Mala",
        optimal_time="Tuesday morning after sunrise",
        facing_direction="South or East",
        asana_color="Deep Red or Terracotta woolen mat",
        guidelines="Recite Hanuman Chalisa or Sundarakanda Chapter 1 before commencing Mars japa. Light a jasmine/sesame oil lamp."
    ),
    "Mercury": MantraPrescription(
        planet_or_deity="Budha (Mercury) / Maha Vishnu",
        vedic_mantra="Om Gajadhvajaya Vidmahe Sukha-hastaya Dheemahi, Tanno Budhah Prachodayaat.",
        bija_mantra="Om Bram Breem Broum Sah Budhaya Namah.",
        prescribed_japa_count=17000,
        japa_mala="Tulsi Mala or Green Hakik / Jade Mala or 4-Mukhi Rudraksha",
        optimal_time="Wednesday morning between 7:00 AM and 9:00 AM",
        facing_direction="North",
        asana_color="Emerald Green or Mint silk mat",
        guidelines="Chant with clear, articulate pronunciation. Keep fresh green tulsi leaves on the altar; recite Vishnu Sahasranama."
    ),
    "Jupiter": MantraPrescription(
        planet_or_deity="Guru (Jupiter) / Brihaspati & Dakshinamurthy",
        vedic_mantra="Om Vrshabha-dhvajaya Vidmahe Kruni-hastaya Dheemahi, Tanno Guruh Prachodayaat.",
        bija_mantra="Om Gram Greem Groum Sah Gurave Namah.",
        prescribed_japa_count=19000,
        japa_mala="Haldi (Turmeric) Mala or Yellow Hakik or 5-Mukhi Rudraksha",
        optimal_time="Thursday morning during Shukla Paksha",
        facing_direction="North-East (Ishanya)",
        asana_color="Bright Golden Yellow or Saffron mat",
        guidelines="Apply pure saffron/turmeric tilak on forehead; chant with reverence to teachers, sages, and sacred wisdom."
    ),
    "Venus": MantraPrescription(
        planet_or_deity="Shukra (Venus) / Maha Lakshmi",
        vedic_mantra="Om Ashwadhvajaya Vidmahe Dhanur-hastaya Dheemahi, Tanno Shukrah Prachodayaat.",
        bija_mantra="Om Shram Shreem Shroum Sah Shukraya Namah.",
        prescribed_japa_count=16000,
        japa_mala="Sphatik (Crystal Quartz) or White Sandalwood or 6-Mukhi Rudraksha",
        optimal_time="Friday morning or dusk (Sandhya Kaal)",
        facing_direction="South-East",
        asana_color="Pure White or Rose Pink silk mat",
        guidelines="Offer white fragrant flowers (Jasmine/Mogra) and burn pure sandalwood incense. Recite Sri Suktam."
    ),
    "Saturn": MantraPrescription(
        planet_or_deity="Shani (Saturn) / Lord Shiva & Yama",
        vedic_mantra="Om Kaka-dhvajaya Vidmahe Khadga-hastaya Dheemahi, Tanno Mandah Prachodayaat.",
        bija_mantra="Om Pram Preem Proum Sah Shanaischaraya Namah.",
        prescribed_japa_count=23000,
        japa_mala="Blue Hakik or Black Agate or 7-Mukhi Rudraksha",
        optimal_time="Saturday evening after sunset (Pradosha Kaal)",
        facing_direction="West",
        asana_color="Dark Navy Blue or Black woolen mat",
        guidelines="Light a sesame oil or mustard oil lamp. Recite Dasharatha Shani Stotra and Maha Mrityunjaya Mantra before japa."
    ),
    "Rahu": MantraPrescription(
        planet_or_deity="Rahu / Goddess Durga & Kala Bhairava",
        vedic_mantra="Om Naka-dhvajaya Vidmahe Padma-hastaya Dheemahi, Tanno Rahuh Prachodayaat.",
        bija_mantra="Om Bhram Bhreem Bhroum Sah Rahave Namah.",
        prescribed_japa_count=18000,
        japa_mala="Gomeda / Hessonite Mala or 8-Mukhi Rudraksha",
        optimal_time="Saturday or Wednesday night (after 8:00 PM)",
        facing_direction="South-West",
        asana_color="Smoky Grey or Dark Blue blanket",
        guidelines="Chant Durga Saptashati Chapter 4 (Sakra-dayah Stuti) or Kala Bhairava Ashtakam to nullify phantom delusions."
    ),
    "Ketu": MantraPrescription(
        planet_or_deity="Ketu / Lord Ganesha & Matsya Avatara",
        vedic_mantra="Om Ashwa-dhvajaya Vidmahe Shoola-hastaya Dheemahi, Tanno Ketuh Prachodayaat.",
        bija_mantra="Om Stram Streem Stroum Sah Ketave Namah.",
        prescribed_japa_count=17000,
        japa_mala="Cat's Eye or 9-Mukhi Rudraksha Mala",
        optimal_time="Tuesday or Saturday early morning (Brahma Muhurta)",
        facing_direction="North-East or South-West",
        asana_color="Multi-colored or Earth-Brown mat",
        guidelines="Chant Ganesha Atharvashirsha. Feed multi-colored stray dogs with sweet rotis."
    )
}


class RemediesEngine:
    """Orchestrates comprehensive remedies across Mantras, Pradakshinams, Upayas, and Danam."""

    @classmethod
    def generate_remedies_dossier(
        cls,
        afflicted_planets: List[str],
        query_category: str,
        lagna_sign: str,
        moon_sign: str
    ) -> ComprehensiveRemedialDossier:
        """
        Synthesizes a personalized, all-inclusive remedial portfolio tailored to the native's
        current planetary afflictions and query domain.
        """
        # Ensure at least 2 primary planets are evaluated
        if not afflicted_planets:
            afflicted_planets = ["Saturn", "Jupiter"]

        # 1. Mantras
        primary_mantras: List[MantraPrescription] = []
        for p in afflicted_planets[:2]:
            if p in NAVAGRAHA_MANTRAS:
                primary_mantras.append(NAVAGRAHA_MANTRAS[p])

        # 2. Sacred Plant Pradakshinams
        # Map afflictions and query to trees
        cat_lower = query_category.lower()
        selected_plants: List[SacredPlantPradakshinam] = []

        if any(w in cat_lower for w in ["job", "career", "promotion", "business"]):
            selected_plants.append(SACRED_PLANTS_CATALOG["Peepal"])
            selected_plants.append(SACRED_PLANTS_CATALOG["Shami"])
        elif any(w in cat_lower for w in ["marriage", "relationship", "spouse"]):
            selected_plants.append(SACRED_PLANTS_CATALOG["Banana"])
            selected_plants.append(SACRED_PLANTS_CATALOG["Tulsi"])
        elif any(w in cat_lower for w in ["property", "land", "real estate"]):
            selected_plants.append(SACRED_PLANTS_CATALOG["Shami"])
            selected_plants.append(SACRED_PLANTS_CATALOG["Vata"])
        elif any(w in cat_lower for w in ["foreign", "abroad", "visa"]):
            selected_plants.append(SACRED_PLANTS_CATALOG["Peepal"])
            selected_plants.append(SACRED_PLANTS_CATALOG["Amla"])
        elif any(w in cat_lower for w in ["finance", "money", "wealth"]):
            selected_plants.append(SACRED_PLANTS_CATALOG["Amla"])
            selected_plants.append(SACRED_PLANTS_CATALOG["Tulsi"])
        else:
            selected_plants.append(SACRED_PLANTS_CATALOG["Peepal"])
            selected_plants.append(SACRED_PLANTS_CATALOG["Bilva"])

        # Deduplicate
        selected_plants = list({p.plant_name: p for p in selected_plants}.values())

        # 3. Lal Kitab Upayas
        lal_kitab_upayas = [
            "Keep a solid square piece of pure silver (1 inch x 1 inch) in your wallet to stabilize the Moon and cash liquidity.",
            "Float a round copper coin with a center hole in a running clean freshwater river on a Sunday morning before noon.",
            "Feed black stray dogs with sweet rotis (cooked with unrefined jaggery) on Saturday evenings to clear Ketu/Saturn hurdles.",
            "Pour water mixed with raw unboiled cow milk at the roots of the sacred Peepal tree on Thursday/Saturday morning.",
            "Never accept broken or secondhand electronic items, free watches, or rusty iron tools into your residence."
        ]

        # 4. Danam (Donations)
        danam_list = [
            DanamPrescription(
                item_name="Black Sesame Seeds (Til), Mustard Oil & Black Blanket",
                associated_planet="Saturn (Shani)",
                suitable_day="Saturday after sunset",
                recipient="Underprivileged sweepers, laborers, or elderly indigent persons",
                significance="Absorbs heavy karmic debt and accelerates clearance of chronic workplace delays."
            ),
            DanamPrescription(
                item_name="Yellow Split Chana Dal, Jaggery, Turmeric & Yellow Cloth",
                associated_planet="Jupiter (Guru)",
                suitable_day="Thursday morning",
                recipient="Vedic scholars, teachers, religious priests, or temple treasury",
                significance="Awakens divine wisdom, blesses marital alliances, and guarantees institutional promotion."
            ),
            DanamPrescription(
                item_name="Green Whole Moong Dal & Bronze/Copper Vessel",
                associated_planet="Mercury (Budha)",
                suitable_day="Wednesday morning",
                recipient="Young orphan girls or students in need of educational supplies",
                significance="Sharpens commercial contracts, restores fluent communication, and clears trade debts."
            )
        ]

        # 5. Gemstones & Rudraksha Prescription
        # Based on primary planet
        lead_planet = afflicted_planets[0]
        gemstone_map = {
            "Sun": ("Ruby (Manikya) 3.5-5 carats", "Red Garnet", "Copper / Gold", "Ring finger (Anamika)", "Sunday sunrise", "12-Mukhi Rudraksha", "Surya Yantra", "Om Hram Hreem Hroum Sah Suryaya Namah"),
            "Moon": ("Natural Pearl (Mukta) 4-6 carats", "Moonstone", "Pure Silver", "Little finger (Kanishtha)", "Monday evening", "2-Mukhi Rudraksha", "Chandra Yantra", "Om Shram Shreem Shroum Sah Chandraya Namah"),
            "Mars": ("Red Coral (Moonga) 6-8 carats", "Carnelian", "Copper / Silver / Gold", "Ring finger", "Tuesday morning", "3-Mukhi Rudraksha", "Mangala Yantra", "Om Kram Kreem Kroum Sah Bhaumaya Namah"),
            "Mercury": ("Emerald (Panna) 4-5 carats", "Green Tourmaline / Peridot", "Gold / Bronze", "Little finger", "Wednesday morning", "4-Mukhi Rudraksha", "Budha Yantra", "Om Bram Breem Broum Sah Budhaya Namah"),
            "Jupiter": ("Yellow Sapphire (Pukhraj) 4-6 carats", "Yellow Topaz", "Pure Gold / Brass", "Index finger (Tarjani)", "Thursday morning", "5-Mukhi Rudraksha", "Guru Yantra", "Om Gram Greem Groum Sah Gurave Namah"),
            "Venus": ("Diamond (Heera) or White Zircon 1-2 carats", "White Sapphire", "Platinum / Silver", "Middle or Little finger", "Friday morning", "6-Mukhi Rudraksha", "Shukra Yantra", "Om Shram Shreem Shroum Sah Shukraya Namah"),
            "Saturn": ("Blue Sapphire (Neelam) 4-6 carats (Test for 3 days)", "Amethyst / Blue Topaz", "Panchadhatu / Iron ring", "Middle finger (Madhyama)", "Saturday evening", "7-Mukhi Rudraksha", "Shani Yantra", "Om Pram Preem Proum Sah Shanaischaraya Namah"),
            "Rahu": ("Hessonite (Gomeda) 5-7 carats", "Spessartite Garnet", "Silver / Ashtadhatu", "Middle finger", "Saturday night", "8-Mukhi Rudraksha", "Rahu Yantra", "Om Bhram Bhreem Bhroum Sah Rahave Namah"),
            "Ketu": ("Cat's Eye (Vaidoorya) 4-6 carats", "Chrysoberyl", "Silver", "Little finger", "Tuesday morning", "9-Mukhi Rudraksha", "Ketu Yantra", "Om Stram Streem Stroum Sah Ketave Namah"),
        }
        g_data = gemstone_map.get(lead_planet, gemstone_map["Jupiter"])

        gemstone_prescription = GemstoneRudrakshaPrescription(
            primary_gemstone=g_data[0],
            substitute_upratna=g_data[1],
            metal=g_data[2],
            finger_to_wear=g_data[3],
            day_and_time_to_wear=g_data[4],
            rudraksha_mukhi=g_data[5],
            sacred_yantra=g_data[6],
            energization_mantra=g_data[7]
        )

        # 6. Vratas & Fasting Guidelines
        vratas = [
            f"Observe a satvik fast on {primary_mantras[0].optimal_time.split()[0]}s: abstain from heavy grains, salt, and onion/garlic until dusk.",
            "Break the fast after twilight with fruit milk, soaked almonds, or sweet rice porridge (Kheer).",
            "Perform Ekadashi vrata twice a month (consuming solely fruits and water) to cleanse generational karmic blocks."
        ]

        # 7. Lifestyle & Energy Upayas
        lifestyle = [
            "Practice Pradakshinam with mindful breathing (Pranayama); walk barefoot on early morning dewy grass to ground mental fire.",
            "Place a brass vessel containing water and fresh fragrant flowers in the North-East corner of your living room; change it every morning.",
            "Avoid sleeping with your head pointed toward the North; ensure your head is oriented toward South or East for revitalizing sleep.",
            "Regularly chant the sacred Omkar (108 times) at dawn to align all 7 chakras with cosmic planetary frequencies."
        ]

        return ComprehensiveRemedialDossier(
            primary_mantras=primary_mantras,
            sacred_plant_pradakshinams=selected_plants,
            lal_kitab_upayas=lal_kitab_upayas,
            danam_prescriptions=danam_list,
            gemstone_rudraksha=gemstone_prescription,
            vratas_and_diet=vratas,
            lifestyle_and_energy_upayas=lifestyle
        )
