"""
Consultation Question Catalog & Dynamic Choices Engine.
Defines consultation purposes and dynamically serves exactly 3 highly targeted
astrological question choices conditioned on Purpose and Marital Status (Unmarried vs Married).
"""
from typing import Dict, List, Tuple, Optional


PURPOSE_CATALOG = {
    "career": {
        "title": "Career, Job & Business",
        "description": "Employment, promotions, business expansion, job changes, workplace dynamics",
        "category_key": "Career",
        "unmarried_questions": [
            "When will I get my next job promotion, salary increment, or significant career growth?",
            "Is private corporate service, government job, or independent business best suited for my chart?",
            "Will I get an opportunity to relocate abroad or travel overseas for work in my current Dasha?"
        ],
        "married_questions": [
            "When will my career reach peak leadership authority and long-term financial stability for my family?",
            "Should I venture into an independent business or partnership, and is spousal luck supporting it?",
            "How can I overcome current workplace politics, job burnout, and stagnation through Vedic remedies?"
        ]
    },
    "marriage": {
        "title": "Marriage, Relationship & Conjugal Life",
        "description": "Marriage timing, spouse profile, relationship harmony, separation prevention",
        "category_key": "Marriage",
        "unmarried_questions": [
            "When will I get married, and what are my most favorable astrological timing windows?",
            "What will my future spouse / life partner be like (temperament, profession, background, and direction)?",
            "Are there any delays, Kuja/Manglik doshas, or obstacles affecting my marriage, and what are the remedies?"
        ],
        "married_questions": [
            "How can my spouse and I resolve marital misunderstandings and restore deep affection and harmony?",
            "Is there any risk of separation, divorce, or third-party interference in our current Dasha, and how to protect our marriage?",
            "When will our joint family prosperity, mutual happiness, and spousal career experience a major breakthrough?"
        ]
    },
    "finance": {
        "title": "Finance, Wealth & Investments",
        "description": "Income growth, savings, investment sectors, debt clearance, sudden gains",
        "category_key": "Finance",
        "unmarried_questions": [
            "When will my financial inflow increase and what are my peak wealth-building years?",
            "Which investment sectors (stocks, real estate, gold, technology) align best with my 2nd and 11th houses?",
            "How can I clear pending debts, student loans, and protect against sudden unexpected financial drains?"
        ],
        "married_questions": [
            "When will our family experience major wealth accumulation, asset growth, and financial security?",
            "Which joint investment avenues (property purchase, mutual funds, gold) will yield the safest high returns?",
            "How can we overcome family financial liabilities, manage household debts, and ensure long-term savings?"
        ]
    },
    "health": {
        "title": "Health, Longevity & Medical Astrology",
        "description": "Vitality, organ vulnerabilities, chronic illness relief, Ayurvedic balance",
        "category_key": "Health",
        "unmarried_questions": [
            "What are my vulnerable organ systems and health tendencies based on my 6th/8th houses and Rogakaraka?",
            "When will my current physical stress, fatigue, or chronic issues improve according to planetary transits?",
            "What Ayurvedic dosha balancing (Vata/Pitta/Kapha), daily lifestyle regimen, and protective mantras are recommended?"
        ],
        "married_questions": [
            "What health vulnerabilities require proactive care for myself and my spouse in the active Dasha?",
            "How will my overall vitality, mental peace, and physical stamina hold up over the next 3 to 5 years?",
            "What specific Vedic Mahamrityunjaya, dietary, and gemstone upayas will protect my family's well-being?"
        ]
    },
    "property": {
        "title": "Property, Real Estate & Vehicles (Vahana)",
        "description": "Buying home/flat/land, vehicle selection, number plate numerology, assets",
        "category_key": "Real Estate",
        "unmarried_questions": [
            "When will I purchase my first self-acquired home, flat, or commercial property (4th house fruition)?",
            "Which vehicle type (2-wheeler vs 4-wheeler), colors, and lucky number plate sums are safe and auspicious for me?",
            "Will there be any property disputes, inheritance delays, or rental challenges, and how can they be remedied?"
        ],
        "married_questions": [
            "When will my spouse and I buy or construct our dream family home, and is joint registration auspicious?",
            "Which 4-wheeler vehicle, safe registration plate combinations, and colors will bless our family with fortune?",
            "How will ancestral property divisions or real estate asset appreciation unfold in our current Dasha period?"
        ]
    },
    "children": {
        "title": "Children & Family Growth (Santan Prapti)",
        "description": "Conception timing, progeny blessings, children's future, family harmony",
        "category_key": "Children",
        "unmarried_questions": [
            "What does my 5th house and Jupiter (Putrakaraka) indicate regarding children and parental blessings in my future life?",
            "Are there any planetary afflictions (Putra Dosha or Rahu-Ketu in 5th) that require timely remedies?",
            "How will my relationship with family, future children, and lineage continuity be supported by my chart?"
        ],
        "married_questions": [
            "When is our most auspicious and fruitful astrological timing window for conceiving a child (Santan Prapti)?",
            "Are there any doshas (Pitri Dosha, Kuja, Rahu-Ketu axis) causing conception delays, and what are the Vedic remedies?",
            "What specific Santana Gopala rituals, sacred tree pradakshinams, and medical-astrological guidance will ensure a healthy birth?"
        ]
    },
    "education": {
        "title": "Education, Higher Studies & Exams",
        "description": "Academic stream, competitive exams, study abroad, overcoming breaks",
        "category_key": "Education",
        "unmarried_questions": [
            "Which higher education stream, specialization, or competitive exams are most aligned with my intellectual yogas?",
            "Is there any risk of education break, concentration lapses, or exam stress in my current Dasha, and how to counter it?",
            "Will I succeed in securing admission into prestigious institutions or pursuing foreign higher education?"
        ],
        "married_questions": [
            "Is this a favorable time for me to pursue executive education, professional certifications, or career upskilling?",
            "How can I balance family responsibilities with demanding study or competitive exam schedules successfully?",
            "Which specialized knowledge domains or executive degrees will guarantee high career promotion dividends?"
        ]
    },
    "foreign": {
        "title": "Foreign Travel, Visa & Relocation",
        "description": "Overseas job, visa approval, permanent settlement (PR/Green Card), travels",
        "category_key": "Foreign",
        "unmarried_questions": [
            "Does my horoscope support permanent foreign settlement (Green Card/PR) or only short-term overseas assignments?",
            "When is the exact timing window for visa approvals, international job offers, or travel clearances?",
            "Which geographical directions and foreign countries are most astrologically harmonious for my prosperity?"
        ],
        "married_questions": [
            "When is the favorable timing window for relocating abroad together with my spouse and family?",
            "Will international relocation bring financial growth and domestic happiness, or cause cultural/emotional adjustment stress?",
            "What travel-enhancing planetary upayas and Rahu/12th-house remedies will smoothen our overseas immigration process?"
        ]
    },
    "spiritual": {
        "title": "Spiritual Growth, Life Purpose & Karma",
        "description": "Atmakaraka path, Ishta Devata, karmic debts clearance, peace of mind",
        "category_key": "Spiritual",
        "unmarried_questions": [
            "What is my soul's higher karmic purpose (Atmakaraka) and spiritual path in this lifetime?",
            "Which Ishta Devata and sacred meditation practices will bring me profound peace, clarity, and protection?",
            "How can I dissolve past-life karmic burdens (Prarabdha Karma) and achieve emotional mastery?"
        ],
        "married_questions": [
            "How can my spouse and I walk a dharmic, spiritually fulfilling path together while fulfilling worldly responsibilities?",
            "What family ancestral rituals (Pitru Tarpanam, Kuladevata activation) will bring divine blessings to our household?",
            "Which pilgrimage, charitable Danam, and spiritual sadhana will clear obstacles and elevate our family consciousness?"
        ]
    }
}


class QuestionCatalogEngine:
    """Manages consultation purposes and generates dynamic 3 question choices."""

    @classmethod
    def list_purposes(cls) -> List[Tuple[str, str, str]]:
        """Returns list of (key, title, description)."""
        return [(k, v["title"], v["description"]) for k, v in PURPOSE_CATALOG.items()]

    @classmethod
    def normalize_marital_status(cls, status_input: str) -> str:
        """Normalizes marital status input to 'Married' or 'Unmarried'."""
        if not status_input:
            return "Unmarried"
        s = status_input.strip().lower()
        if s in ["2", "m", "married", "yes", "true", "y"]:
            return "Married"
        return "Unmarried"

    @classmethod
    def resolve_purpose_key(cls, input_str: str) -> str:
        """Resolves user input (numeric index or keyword) to catalog key."""
        s = input_str.strip().lower()
        keys = list(PURPOSE_CATALOG.keys())

        # If user entered a number 1..9
        if s.isdigit():
            idx = int(s) - 1
            if 0 <= idx < len(keys):
                return keys[idx]

        # Match keywords
        for k, v in PURPOSE_CATALOG.items():
            if k in s or v["title"].lower() in s or v["category_key"].lower() in s:
                return k
        if "job" in s or "work" in s or "profession" in s or "biz" in s:
            return "career"
        if "relation" in s or "partner" in s or "love" in s or "spouse" in s:
            return "marriage"
        if "money" in s or "wealth" in s or "investment" in s or "cash" in s:
            return "finance"
        if "health" in s or "disease" in s or "medical" in s:
            return "health"
        if "car" in s or "home" in s or "house" in s or "flat" in s or "land" in s:
            return "property"
        if "child" in s or "baby" in s or "pregnancy" in s or "santan" in s:
            return "children"
        if "study" in s or "exam" in s or "college" in s or "degree" in s:
            return "education"
        if "abroad" in s or "visa" in s or "travel" in s or "relocat" in s:
            return "foreign"
        if "god" in s or "puja" in s or "karma" in s or "moksha" in s:
            return "spiritual"

        return "career"  # default

    @classmethod
    def get_three_question_choices(cls, purpose_key: str, marital_status: str) -> List[str]:
        """
        Returns exactly 3 curated question choices based on the purpose
        and marital status (Married vs Unmarried).
        """
        key = cls.resolve_purpose_key(purpose_key)
        data = PURPOSE_CATALOG[key]
        status = cls.normalize_marital_status(marital_status)

        if status == "Married":
            return list(data["married_questions"])
        return list(data["unmarried_questions"])

    @classmethod
    def get_category_name(cls, purpose_key: str) -> str:
        key = cls.resolve_purpose_key(purpose_key)
        return PURPOSE_CATALOG[key]["category_key"]

    @classmethod
    def get_purpose_title(cls, purpose_key: str) -> str:
        key = cls.resolve_purpose_key(purpose_key)
        return PURPOSE_CATALOG[key]["title"]
