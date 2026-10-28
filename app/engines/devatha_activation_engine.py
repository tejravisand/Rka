"""
Nakshatra Devatha & Tithi Devatha Activation Engine.
Implements:
1. Complete 27 Nakshatra directory with Presiding Devatha, Cosmic Shakti, Sacred Vriksha (Tree),
   Sacred Fruit, and authentic Vedic/Puranic Beej Mantra.
2. Complete Tithi directory (1-30) with Ruling Tithi Devatha, Governing Planet, Sacred Offering,
   and Tithi Activation Mantra.
3. Awakening / Activation (Jagriti) protocols: Vriksha Seva, Pradakshinam, Tithi fasting,
   and deity invocation for mental clarity (Nakshatra) and emotional/financial flow (Tithi).
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from app.models.astrological import Kundali


# Full 27 Nakshatras Directory
NAKSHATRA_DIRECTORY: Dict[int, Dict[str, str]] = {
    0: {"name": "Ashwini", "devatha": "Ashvini Kumaras", "shakti": "Healing & Swift Initiation", "vriksha": "Kuchila (Strychnos nux-vomica)", "fruit": "Wild Ber / Pomegranate", "mantra": "Om Ashwibhyam Namah"},
    1: {"name": "Bharani", "devatha": "Yama (God of Dharma)", "shakti": "Restraint & Transformation", "vriksha": "Amla (Emblica officinalis)", "fruit": "Fresh Amla / Pomegranate", "mantra": "Om Yamaya Namah"},
    2: {"name": "Krittika", "devatha": "Agni (Fire God)", "shakti": "Purification & Digestion", "vriksha": "Udumbara / Gular (Ficus glomerata)", "fruit": "Anjeer (Figs)", "mantra": "Om Agnaye Namah"},
    3: {"name": "Rohini", "devatha": "Prajapati / Brahma", "shakti": "Creative Fertility & Growth", "vriksha": "Jamun (Syzygium cumini)", "fruit": "Black Jamun / White Grapes", "mantra": "Om Prajapataye Namah"},
    4: {"name": "Mrigashira", "devatha": "Soma (Moon God)", "shakti": "Nectar & Joy of Searching", "vriksha": "Khair (Acacia catechu)", "fruit": "Fresh Coconut / Water Chestnut", "mantra": "Om Somaya Namah"},
    5: {"name": "Ardra", "devatha": "Rudra (Storm Dissolver)", "shakti": "Destruction of Toxic Ego", "vriksha": "Agarwood / Krishna Wood", "fruit": "Sour Lime / Green Apple", "mantra": "Om Rudraya Namah"},
    6: {"name": "Punarvasu", "devatha": "Aditi (Cosmic Mother)", "shakti": "Boundless Renewal & Return", "vriksha": "Vamsha (Bamboo - Bambusa vulgaris)", "fruit": "Sugarcane / Sweet Lime", "mantra": "Om Aditaye Namah"},
    7: {"name": "Pushya", "devatha": "Brihaspati (Divine Guru)", "shakti": "Spiritual Nourishment & Dharma", "vriksha": "Peepal (Ficus religiosa)", "fruit": "Yellow Banana / Bael Fruit", "mantra": "Om Brihaspataye Namah"},
    8: {"name": "Ashlesha", "devatha": "Sarpas (Naga Rajas)", "shakti": "Kundalini & Intuition", "vriksha": "Nagakesar (Mesua ferrea)", "fruit": "Black Grapes / Custard Apple", "mantra": "Om Sarpebhyo Namah"},
    9: {"name": "Magha", "devatha": "Pitrus (Ancestors)", "shakti": "Lineage Authority & Honor", "vriksha": "Banyan / Vata (Ficus benghalensis)", "fruit": "Royal Mango / Sweet Fig", "mantra": "Om Pitribhyo Namah"},
    10: {"name": "Purva Phalguni", "devatha": "Bhaga (God of Fortune)", "shakti": "Conjugal Bliss & Prosperity", "vriksha": "Palasa / Dhak (Butea monosperma)", "fruit": "Sweet Orange / Rose Apple", "mantra": "Om Bhagaya Namah"},
    11: {"name": "Uttara Phalguni", "devatha": "Aryaman (Noble Patron)", "shakti": "Social Honor & Contracts", "vriksha": "Plaksha (Ficus rumphii)", "fruit": "Sweet Apple / Papaya", "mantra": "Om Aryamne Namah"},
    12: {"name": "Hasta", "devatha": "Savitur (Solar Awakening)", "shakti": "Dexterity & Manifestation", "vriksha": "Chameli / Jasmine / Amba", "fruit": "Sweet Guava / Muskmelon", "mantra": "Om Savitre Namah"},
    13: {"name": "Chitra", "devatha": "Vishwakarma (Cosmic Architect)", "shakti": "Sacred Design & Radiance", "vriksha": "Bilva / Bael (Aegle marmelos)", "fruit": "Fresh Bael fruit", "mantra": "Om Twashtre Namah"},
    14: {"name": "Swati", "devatha": "Vayu (Wind God)", "shakti": "Pranic Vitality & Independence", "vriksha": "Arjuna (Terminalia arjuna)", "fruit": "Crisp Pear / Custard Apple", "mantra": "Om Vayave Namah"},
    15: {"name": "Vishakha", "devatha": "Indragni (Indra + Agni)", "shakti": "Focused Ambition & Triumph", "vriksha": "Kaitha / Wood Apple (Limonia acidissima)", "fruit": "Wood Apple / Starfruit", "mantra": "Om Indragnibhyam Namah"},
    16: {"name": "Anuradha", "devatha": "Mitra (God of Friendship)", "shakti": "Devotion & Unshakable Trust", "vriksha": "Bakula / Maulsari (Mimusops elengi)", "fruit": "Mulberry / Jamun", "mantra": "Om Mitraya Namah"},
    17: {"name": "Jyeshtha", "devatha": "Indra (King of Gods)", "shakti": "Seniority & Courageous Defense", "vriksha": "Semal (Bombax ceiba)", "fruit": "Pomegranate / Wood Apple", "mantra": "Om Indraya Namah"},
    18: {"name": "Moola", "devatha": "Nirriti (Root Dissolver)", "shakti": "Root Investigation & Renunciation", "vriksha": "Sal / Sarjaha (Shorea robusta)", "fruit": "Black Berries / Dried Figs", "mantra": "Om Nirritaye Namah"},
    19: {"name": "Purvashadha", "devatha": "Apas (Water Deities)", "shakti": "Invincible Purity & Victory", "vriksha": "Ashoka (Saraca asoca)", "fruit": "Tender Coconut Water / Melon", "mantra": "Om Adbhyo Namah"},
    20: {"name": "Uttarashadha", "devatha": "Vishvadevas (Universal Gods)", "shakti": "Universal Alignment & Righteousness", "vriksha": "Jackfruit / Phanas (Artocarpus heterophyllus)", "fruit": "Ripe Jackfruit / Banana", "mantra": "Om Vishvedevebhyo Namah"},
    21: {"name": "Shravana", "devatha": "Maha Vishnu", "shakti": "Divine Listening & Learning", "vriksha": "Madar / Arka (Calotropis gigantea)", "fruit": "Sweet Yellow Mango / Banana", "mantra": "Om Vishnave Namah"},
    22: {"name": "Dhanishta", "devatha": "Ashta Vasus (Elemental Gods)", "shakti": "Wealth, Rhythm & Harmony", "vriksha": "Shami (Prosopis cineraria)", "fruit": "Blackberry / Dried Fig", "mantra": "Om Vasubhyo Namah"},
    23: {"name": "Shatabhisha", "devatha": "Varuna (Cosmic Healer)", "shakti": "Divine Medicine & 100 Physicians", "vriksha": "Kadamba (Neolamarckia cadamba)", "fruit": "Pomegranate / Citrus Fruit", "mantra": "Om Varunaya Namah"},
    24: {"name": "Purva Bhadrapada", "devatha": "Aja Ekapada", "shakti": "Mystical Tapasya & Purification", "vriksha": "Neem (Azadirachta indica)", "fruit": "Bitter Gourd / Neem Berries", "mantra": "Om Aja Ekapade Namah"},
    25: {"name": "Uttara Bhadrapada", "devatha": "Ahirbudhnya (Deep Serpent)", "shakti": "Foundational Serenity & Wisdom", "vriksha": "Amra (Mangifera indica)", "fruit": "Royal Mango / Coconut", "mantra": "Om Ahirbudhnyaya Namah"},
    26: {"name": "Revati", "devatha": "Pushan (Soul Protector)", "shakti": "Safe Travel & Abundance", "vriksha": "Mahua (Madhuca longifolia)", "fruit": "Sweet Grapes / Dates", "mantra": "Om Pushne Namah"}
}

# Tithi Directory (1 to 15 for Shukla, 16 to 30 for Krishna)
TITHI_DIRECTORY: Dict[int, Dict[str, str]] = {
    1: {"name": "Pratipada", "devatha": "Agni", "planet": "Sun", "offering": "Pure Ghee & Red Pomegranate", "mantra": "Om Agnaye Svaha"},
    2: {"name": "Dwitiya", "devatha": "Brahma", "planet": "Moon", "offering": "Tulsi, Sweet Milk, Banana", "mantra": "Om Brahmane Namah"},
    3: {"name": "Tritiya", "devatha": "Gauri (Parvati)", "planet": "Mars", "offering": "Jaggery (Gur) & Sweet Papaya", "mantra": "Om Gauraye Namah"},
    4: {"name": "Chaturthi", "devatha": "Ganesha", "planet": "Mercury", "offering": "Modak, Guava, Durva grass", "mantra": "Om Gam Ganapataye Namah"},
    5: {"name": "Panchami", "devatha": "Nagas (Serpent Kings)", "planet": "Jupiter", "offering": "Fresh Cow Milk & Honey", "mantra": "Om Sarpebhyo Namah"},
    6: {"name": "Shashti", "devatha": "Kartikeya (Skanda)", "planet": "Venus", "offering": "Almonds, Red Flowers, Figs", "mantra": "Om Saravanabhavaya Namah"},
    7: {"name": "Saptami", "devatha": "Surya (Sun God)", "planet": "Saturn", "offering": "Red Apple & Sweet Rice Payasam", "mantra": "Om Suryaya Namah"},
    8: {"name": "Ashtami", "devatha": "Ashta Vasus / Rudra", "planet": "Rahu", "offering": "Coconut, Bilva leaf, Black Plum", "mantra": "Om Rudraya Namah"},
    9: {"name": "Navami", "devatha": "Durga", "planet": "Sun", "offering": "Pomegranate, Sweet Lime, Honey", "mantra": "Om Dum Durgaye Namah"},
    10: {"name": "Dashami", "devatha": "Yama / Dharmaraja", "planet": "Moon", "offering": "Curd Rice & Water Chestnut", "mantra": "Om Dharmarajaya Namah"},
    11: {"name": "Ekadashi", "devatha": "Vishvadevas / Rudra", "planet": "Mars", "offering": "Fresh Fruits (Grainless Fasting)", "mantra": "Om Vishve-devebhyo Namah"},
    12: {"name": "Dwadashi", "devatha": "Maha Vishnu", "planet": "Mercury", "offering": "Yellow Bananas, Tulsi Water", "mantra": "Om Namo Bhagavate Vasudevaya"},
    13: {"name": "Trayodashi", "devatha": "Kamadeva / Shiva", "planet": "Jupiter", "offering": "Panchamrita & Bael Fruit", "mantra": "Om Namah Shivaya"},
    14: {"name": "Chaturdashi", "devatha": "Shiva / Kali", "planet": "Venus", "offering": "Bilva leaves & Black Grapes", "mantra": "Om Hreem Dakshina Kalike Namah"},
    15: {"name": "Purnima", "devatha": "Sri Lalita / Chandra", "planet": "Saturn", "offering": "Kheer / Sweet White Coconut", "mantra": "Om Sri Tripurasundaryai Namah"},
    30: {"name": "Amavasya", "devatha": "Pitrus (Ancestors)", "planet": "Rahu", "offering": "Black Sesame Seeds, Kusa Grass, Rice", "mantra": "Om Pitribhya Svadha Namah"}
}


@dataclass
class DevathaActivationDossier:
    nakshatra_number: int
    nakshatra_name: str
    nakshatra_devatha: str
    nakshatra_cosmic_shakti: str
    sacred_tree: str
    sacred_fruit: str
    nakshatra_beej_mantra: str
    tithi_number: int
    tithi_name: str
    tithi_paksha: str
    tithi_devatha: str
    tithi_governing_planet: str
    tithi_sacred_offering: str
    tithi_activation_mantra: str
    complete_activation_protocol: List[str]


class DevathaActivationEngine:
    """Calculates and prescribes exact activation rituals for Nakshatra and Tithi Devathas."""

    @classmethod
    def evaluate(cls, kundali: Kundali) -> DevathaActivationDossier:
        # 1. Nakshatra calculation
        moon_pos = kundali.planets["Moon"]
        nak_idx = moon_pos.nakshatra_number % 27
        nak_data = NAKSHATRA_DIRECTORY.get(nak_idx, NAKSHATRA_DIRECTORY[0])

        # 2. Tithi calculation: (Moon Longitude - Sun Longitude) / 12 deg
        moon_lon = moon_pos.longitude
        sun_lon = kundali.planets["Sun"].longitude
        elongation = (moon_lon - sun_lon) % 360
        tithi_raw = int(elongation / 12.0) + 1

        paksha = "Shukla Paksha (Waxing Moon)" if tithi_raw <= 15 else "Krishna Paksha (Waning Moon)"
        tithi_display_num = tithi_raw if tithi_raw <= 15 else tithi_raw - 15
        if tithi_raw == 30:
            tithi_lookup = 30
        else:
            tithi_lookup = tithi_display_num

        tithi_data = TITHI_DIRECTORY.get(tithi_lookup, TITHI_DIRECTORY[1])

        # 3. Activation Protocol
        protocols = [
            f"1. Vriksha Seva: Nurture or water your sacred tree '{nak_data['vriksha']}' whenever Moon transits {nak_data['name']}.",
            f"2. Fruit Offering: Offer fresh {nak_data['fruit']} to {nak_data['devatha']} and consume as prasadam to infuse cellular prana.",
            f"3. Nakshatra Japa: Recite '{nak_data['mantra']}' 108 times at sunrise on your Janma Nakshatra day.",
            f"4. Tithi Harmonization: Observe a partial or salt-free fast on {paksha} {tithi_data['name']}.",
            f"5. Tithi Offering: Present {tithi_data['offering']} and recite '{tithi_data['mantra']}' at twilight to awaken emotional and financial grace."
        ]

        return DevathaActivationDossier(
            nakshatra_number=nak_idx + 1,
            nakshatra_name=nak_data["name"],
            nakshatra_devatha=nak_data["devatha"],
            nakshatra_cosmic_shakti=nak_data["shakti"],
            sacred_tree=nak_data["vriksha"],
            sacred_fruit=nak_data["fruit"],
            nakshatra_beej_mantra=nak_data["mantra"],
            tithi_number=tithi_raw,
            tithi_name=f"{tithi_data['name']} (Tithi #{tithi_raw})",
            tithi_paksha=paksha,
            tithi_devatha=tithi_data["devatha"],
            tithi_governing_planet=tithi_data["planet"],
            tithi_sacred_offering=tithi_data["offering"],
            tithi_activation_mantra=tithi_data["mantra"],
            complete_activation_protocol=protocols
        )
