"""
Western Medical Astrology Engine (Iatromathematics)
===================================================
Based on the classical traditions of Hippocrates, Galen, Ptolemy,
Hermes Trismegistus, and Nicholas Culpeper.

Implements:
1. Tropical (Sayana) Zodiac Conversion from Sidereal coordinates.
2. The Four Galenic Humors (Sanguine, Choleric, Melancholic, Phlegmatic).
3. Primary Elemental Qualities (Hot/Cold & Moist/Dry).
4. Homo Signorum (Zodiacal Man: Head-to-Toe organ rulership in Tropical Zodiac).
5. Western Decumbiture Aspects (Conjunction, Opposition, Square, Trine, Sextile).
6. Culpeper's Herbalism (Doctrine of Signatures, Cures by Sympathy & Antipathy).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from app.models.astrological import Kundali, PlanetPosition, ZodiacSign


WESTERN_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Elemental Qualities of Tropical Signs
# Fire = Hot & Dry (Choleric)
# Earth = Cold & Dry (Melancholic)
# Air = Hot & Moist (Sanguine)
# Water = Cold & Moist (Phlegmatic)
SIGN_HUMORAL_PROPERTIES = {
    "Aries": {"element": "Fire", "quality": "Hot & Dry", "humor": "Choleric", "organ": "Head, brain, skull, facial bones, eyesight"},
    "Taurus": {"element": "Earth", "quality": "Cold & Dry", "humor": "Melancholic", "organ": "Neck, throat, vocal cords, thyroid, carotid arteries"},
    "Gemini": {"element": "Air", "quality": "Hot & Moist", "humor": "Sanguine", "organ": "Shoulders, arms, hands, lungs, thymus, bronchi, nervous conduction"},
    "Cancer": {"element": "Water", "quality": "Cold & Moist", "humor": "Phlegmatic", "organ": "Chest, breasts, stomach, digestive fluids, womb, ribs"},
    "Leo": {"element": "Fire", "quality": "Hot & Dry", "humor": "Choleric", "organ": "Heart, spine, upper back, aorta, vital arterial blood"},
    "Virgo": {"element": "Earth", "quality": "Cold & Dry", "humor": "Melancholic", "organ": "Abdomen, small intestines, digestion, assimilation, spleen"},
    "Libra": {"element": "Air", "quality": "Hot & Moist", "humor": "Sanguine", "organ": "Kidneys, adrenal glands, lumbar spine, acid-alkaline balance"},
    "Scorpio": {"element": "Water", "quality": "Cold & Moist", "humor": "Phlegmatic", "organ": "Genitals, excretory organs, pelvis, prostate, reproductive organs"},
    "Sagittarius": {"element": "Fire", "quality": "Hot & Dry", "humor": "Choleric", "organ": "Hips, thighs, sciatic nerve, sacrum, arterial system"},
    "Capricorn": {"element": "Earth", "quality": "Cold & Dry", "humor": "Melancholic", "organ": "Knees, bones, skeletal joints, teeth, skin, connective tissue"},
    "Aquarius": {"element": "Air", "quality": "Hot & Moist", "humor": "Sanguine", "organ": "Calves, shins, ankles, peripheral circulation, electrical impulses"},
    "Pisces": {"element": "Water", "quality": "Cold & Moist", "humor": "Phlegmatic", "organ": "Feet, toes, lymphatic system, immune fluids, sleep centres"}
}

PLANET_HUMORAL_PROPERTIES = {
    "Sun": {"quality": "Hot & Dry", "humor": "Choleric", "governs": "Vitality, heart, sight, arterial blood"},
    "Moon": {"quality": "Cold & Moist", "humor": "Phlegmatic", "governs": "Fluid balance, brain, lymph, stomach, mucosa"},
    "Mars": {"quality": "Very Hot & Dry", "humor": "Choleric", "governs": "Muscles, gallbladder, inflammation, fevers, surgeries"},
    "Mercury": {"quality": "Cold & Dry (Variable)", "humor": "Melancholic", "governs": "Nervous system, intellect, respiratory channels, speech"},
    "Jupiter": {"quality": "Hot & Moist", "humor": "Sanguine", "governs": "Liver, arterial circulation, cellular growth, lipids"},
    "Venus": {"quality": "Cold & Moist", "humor": "Phlegmatic / Sanguine", "governs": "Venous blood, kidneys, reproductive hormones, skin"},
    "Saturn": {"quality": "Extremely Cold & Dry", "humor": "Melancholic", "governs": "Bones, joints, teeth, spleen, chronic degeneration, atrophy"},
    "Rahu": {"quality": "Cold & Dry", "humor": "Melancholic (Toxic)", "governs": "Psychosomatic conditions, sudden toxins, nervous spasms"},
    "Ketu": {"quality": "Hot & Dry", "humor": "Choleric (Fiery)", "governs": "Infections, hidden fevers, surgical interventions"}
}


@dataclass
class TropicalPosition:
    planet_name: str
    tropical_longitude: float
    sign_name: str
    degrees_in_sign: float
    element: str
    humor: str


@dataclass
class HumoralTemperament:
    choleric_pct: float     # Fire: Yellow bile (Hot & Dry)
    sanguine_pct: float     # Air: Blood (Hot & Moist)
    melancholic_pct: float  # Earth: Black bile (Cold & Dry)
    phlegmatic_pct: float   # Water: Phlegm (Cold & Moist)
    dominant_temperament: str
    constitutional_qualities: str
    clinical_implications: str


@dataclass
class WesternAspectAffliction:
    planet_1: str
    planet_2: str
    aspect_type: str        # "Opposition", "Square", "Conjunction", "Trine", "Sextile"
    orb: float
    nature: str             # "Harmful / Acute Crisis", "Harmful / Chronic Friction", "Benefic / Vital Flow"
    clinical_manifestation: str


@dataclass
class HomoSignorumVulnerability:
    sign_name: str
    body_region: str
    afflicting_planets: List[str]
    vulnerability_grade: str # "Normal", "Moderate", "High"
    preventive_care: str


@dataclass
class CulpeperHerbalPrescription:
    herb_name: str
    botanical_name: str
    ruling_planet: str
    temperament_action: str
    cure_mechanism: str     # "Cure by Sympathy" or "Cure by Antipathy"
    traditional_use: str


@dataclass
class WesternMedicalReport:
    client_name: str
    tropical_ascendant: TropicalPosition
    tropical_positions: Dict[str, TropicalPosition]
    temperament: HumoralTemperament
    homo_signorum_zones: List[HomoSignorumVulnerability]
    aspect_afflictions: List[WesternAspectAffliction]
    culpeper_remedies: List[CulpeperHerbalPrescription]
    diagnostic_summary: str


class WesternMedicalAstrologyEngine:
    """
    Western Medical Astrology (Iatromathematics) Engine.
    """

    @classmethod
    def evaluate(
        cls,
        kundali: Kundali,
        client_name: str = "Native"
    ) -> WesternMedicalReport:
        """
        Executes complete Western Iatromathematical analysis.
        """
        ayanamsa = kundali.ayanamsa_value

        # 1. Convert to Tropical (Sayana) Positions
        trop_asc = cls._to_tropical("Ascendant", kundali.ascendant.longitude, ayanamsa)
        trop_positions = {}
        for p_name, p_pos in kundali.planets.items():
            trop_positions[p_name] = cls._to_tropical(p_name, p_pos.longitude, ayanamsa)

        # 2. Four Humors Analysis (Hippocratic & Galenic)
        temperament = cls._calculate_humors(trop_asc, trop_positions)

        # 3. Homo Signorum (Zodiacal Man Organ Mapping)
        zones = cls._assess_homo_signorum(trop_asc, trop_positions)

        # 4. Decumbiture & Hard Aspects (Squares, Oppositions)
        aspects = cls._assess_aspects(trop_asc, trop_positions)

        # 5. Culpeper Herbalism
        remedies = cls._prescribe_culpeper_herbs(temperament, aspects)

        # 6. Diagnostic Summary
        summary = (
            f"Western Iatromathematical evaluation reveals a {temperament.dominant_temperament} constitution "
            f"with {temperament.constitutional_qualities}. "
            f"Tropical Ascendant is in {trop_asc.sign_name} ({trop_asc.degrees_in_sign:.1f}°), with Sun in "
            f"{trop_positions.get('Sun', trop_asc).sign_name}. Clinical focus emphasizes {temperament.clinical_implications}."
        )

        return WesternMedicalReport(
            client_name=client_name,
            tropical_ascendant=trop_asc,
            tropical_positions=trop_positions,
            temperament=temperament,
            homo_signorum_zones=zones,
            aspect_afflictions=aspects,
            culpeper_remedies=remedies,
            diagnostic_summary=summary
        )

    # -------------------------------------------------------------------------
    # INTERNAL METHODS
    # -------------------------------------------------------------------------

    @classmethod
    def _to_tropical(cls, name: str, sidereal_lon: float, ayanamsa: float) -> TropicalPosition:
        """Converts sidereal longitude to tropical longitude and properties."""
        trop_lon = (sidereal_lon + ayanamsa) % 360.0
        sign_idx = int(trop_lon / 30.0) % 12
        deg_in_sign = trop_lon % 30.0
        sign_name = WESTERN_SIGNS[sign_idx]

        props = SIGN_HUMORAL_PROPERTIES[sign_name]
        return TropicalPosition(
            planet_name=name,
            tropical_longitude=trop_lon,
            sign_name=sign_name,
            degrees_in_sign=deg_in_sign,
            element=props["element"],
            humor=props["humor"]
        )

    @classmethod
    def _calculate_humors(
        cls,
        trop_asc: TropicalPosition,
        trop_positions: Dict[str, TropicalPosition]
    ) -> HumoralTemperament:
        """Computes Galenic Four Humors distribution."""
        scores = {"Choleric": 0.0, "Sanguine": 0.0, "Melancholic": 0.0, "Phlegmatic": 0.0}

        # Weight 1: Tropical Ascendant Sign (Weight: 3.5)
        asc_humor = SIGN_HUMORAL_PROPERTIES[trop_asc.sign_name]["humor"]
        scores[asc_humor] += 3.5

        # Weight 2: Tropical Sun (Weight: 3.0)
        sun_pos = trop_positions.get("Sun")
        if sun_pos:
            sun_sign_humor = SIGN_HUMORAL_PROPERTIES[sun_pos.sign_name]["humor"]
            scores[sun_sign_humor] += 2.0
            scores["Choleric"] += 1.0  # Sun itself is naturally Choleric

        # Weight 3: Tropical Moon (Weight: 2.5)
        moon_pos = trop_positions.get("Moon")
        if moon_pos:
            moon_sign_humor = SIGN_HUMORAL_PROPERTIES[moon_pos.sign_name]["humor"]
            scores[moon_sign_humor] += 1.5
            scores["Phlegmatic"] += 1.0  # Moon is naturally Phlegmatic

        # Weight 4: Inner & Outer Planets (Weight: 1.0 each)
        for p_name, pos in trop_positions.items():
            if p_name in ["Sun", "Moon"]:
                continue
            sign_humor = SIGN_HUMORAL_PROPERTIES[pos.sign_name]["humor"]
            scores[sign_humor] += 0.5
            p_humor = PLANET_HUMORAL_PROPERTIES.get(p_name, {}).get("humor", "Sanguine")
            if "Choleric" in p_humor: scores["Choleric"] += 0.5
            if "Sanguine" in p_humor: scores["Sanguine"] += 0.5
            if "Melancholic" in p_humor: scores["Melancholic"] += 0.5
            if "Phlegmatic" in p_humor: scores["Phlegmatic"] += 0.5

        total = sum(scores.values()) or 1.0
        c_pct = round((scores["Choleric"] / total) * 100, 1)
        s_pct = round((scores["Sanguine"] / total) * 100, 1)
        m_pct = round((scores["Melancholic"] / total) * 100, 1)
        p_pct = round((scores["Phlegmatic"] / total) * 100, 1)

        # Rank
        humors_ranked = sorted([
            ("Choleric", c_pct, "Hot & Dry (Yellow Bile)"),
            ("Sanguine", s_pct, "Hot & Moist (Blood)"),
            ("Melancholic", m_pct, "Cold & Dry (Black Bile)"),
            ("Phlegmatic", p_pct, "Cold & Moist (Phlegm)")
        ], key=lambda x: x[1], reverse=True)

        primary = humors_ranked[0][0]
        secondary = humors_ranked[1][0]
        qualities = f"{humors_ranked[0][2]} with secondary {humors_ranked[1][2]}"

        if primary == "Choleric":
            clin = "Prone to acute heat, bilious irritability, inflammatory flare-ups, and arterial hypertension."
        elif primary == "Melancholic":
            clin = "Prone to chronic degenerative joint stiffness, dry skin, visceral coldness, and melancholic fatigue."
        elif primary == "Phlegmatic":
            clin = "Prone to lymphatic stagnation, fluid accumulation, sluggish endocrine metabolism, and mucus."
        else:
            clin = "Prone to rich blood plethoric congestion, palpitations, and vascular volatility."

        return HumoralTemperament(
            choleric_pct=c_pct,
            sanguine_pct=s_pct,
            melancholic_pct=m_pct,
            phlegmatic_pct=p_pct,
            dominant_temperament=f"{primary}-{secondary}",
            constitutional_qualities=qualities,
            clinical_implications=clin
        )

    @classmethod
    def _assess_homo_signorum(
        cls,
        trop_asc: TropicalPosition,
        trop_positions: Dict[str, TropicalPosition]
    ) -> List[HomoSignorumVulnerability]:
        """Maps planetary occupancy in the 12 Tropical Homo Signorum regions."""
        zones = []

        for sign in WESTERN_SIGNS:
            props = SIGN_HUMORAL_PROPERTIES[sign]
            afflicting = []
            for p_name, pos in trop_positions.items():
                if pos.sign_name == sign:
                    if p_name in ["Mars", "Saturn", "Rahu", "Ketu"]:
                        afflicting.append(f"{p_name} ({p_name} in {sign})")
                    else:
                        afflicting.append(p_name)

            if any(m in afflicting for m in ["Mars (Mars in " + sign, "Saturn (Saturn in " + sign]):
                grade = "High"
                care = f"Elevated clinical priority. Shield {props['organ'].lower()} against mechanical impact and humoral extremes."
            elif len(afflicting) >= 1:
                grade = "Moderate"
                care = f"Monitor {props['organ'].lower()} during seasonal shifts and hard transit aspects."
            else:
                grade = "Normal"
                care = f"{props['organ']} shows normal functional integrity."

            zones.append(HomoSignorumVulnerability(
                sign_name=sign,
                body_region=props["organ"],
                afflicting_planets=afflicting if afflicting else ["Unoccupied"],
                vulnerability_grade=grade,
                preventive_care=care
            ))

        return zones

    @classmethod
    def _assess_aspects(
        cls,
        trop_asc: TropicalPosition,
        trop_positions: Dict[str, TropicalPosition]
    ) -> List[WesternAspectAffliction]:
        """Calculates Ptolemaic aspects with health impact."""
        aspect_specs = [
            (0.0, 7.0, "Conjunction"),
            (90.0, 6.0, "Square"),
            (180.0, 7.0, "Opposition"),
            (120.0, 6.0, "Trine"),
            (60.0, 4.0, "Sextile")
        ]

        results = []
        planets_list = list(trop_positions.items())

        for i in range(len(planets_list)):
            p1_name, p1_pos = planets_list[i]
            for j in range(i + 1, len(planets_list)):
                p2_name, p2_pos = planets_list[j]

                diff = abs(p1_pos.tropical_longitude - p2_pos.tropical_longitude)
                if diff > 180.0:
                    diff = 360.0 - diff

                for target_angle, max_orb, aspect_name in aspect_specs:
                    orb = abs(diff - target_angle)
                    if orb <= max_orb:
                        nature, manifest = cls._interpret_aspect(p1_name, p2_name, aspect_name)
                        results.append(WesternAspectAffliction(
                            planet_1=p1_name,
                            planet_2=p2_name,
                            aspect_type=aspect_name,
                            orb=round(orb, 2),
                            nature=nature,
                            clinical_manifestation=manifest
                        ))
                        break

        return results

    @classmethod
    def _interpret_aspect(cls, p1: str, p2: str, asp: str) -> Tuple[str, str]:
        """Provides classical clinical interpretation for an aspect."""
        malefics = ["Mars", "Saturn", "Rahu", "Ketu"]
        is_hard = asp in ["Square", "Opposition"]

        if is_hard and (p1 in malefics or p2 in malefics):
            nature = "Harmful / Acute Friction" if "Mars" in [p1, p2] else "Harmful / Chronic Stagnation"
            manifest = f"Friction between {p1} and {p2} via {asp}: risk of acute strain, systemic tension, or inflammatory depletion."
        elif asp in ["Trine", "Sextile"]:
            nature = "Benefic / Vital Flow"
            manifest = f"Harmonious circulation between {p1} and {p2}: enhances cellular vitality and natural healing recuperation."
        else:
            nature = "Neutral / Dynamic Blend"
            manifest = f"Close interaction between {p1} and {p2}: focal point of bodily energy."

        return nature, manifest

    @classmethod
    def _prescribe_culpeper_herbs(
        cls,
        humors: HumoralTemperament,
        aspects: List[WesternAspectAffliction]
    ) -> List[CulpeperHerbalPrescription]:
        """Applies Culpeper's Herbal Astrological Pharmacopeia."""
        prescriptions = [
            CulpeperHerbalPrescription(
                herb_name="Hawthorn Berry & Flowers",
                botanical_name="Crataegus oxyacantha",
                ruling_planet="Mars & Sun",
                temperament_action="Balances Choleric heat, tones cardiovascular musculature",
                cure_mechanism="Cure by Sympathy",
                traditional_use="Strengthens weak pulse, stabilizes arterial blood pressure, and relieves cardiac oppression."
            ),
            CulpeperHerbalPrescription(
                herb_name="Milk Thistle",
                botanical_name="Silybum marianum",
                ruling_planet="Jupiter",
                temperament_action="Promotes Sanguine liver function, cools bilious excess",
                cure_mechanism="Cure by Sympathy",
                traditional_use="Protects hepatic parenchyma, regulates lipid metabolism, and counters sluggish portal circulation."
            ),
            CulpeperHerbalPrescription(
                herb_name="Willow Bark",
                botanical_name="Salix alba",
                ruling_planet="Moon (Water)",
                temperament_action="Cooling & Moistening; pacifies intense Choleric/Mars fire",
                cure_mechanism="Cure by Antipathy",
                traditional_use="Natural salicin source; dispels sharp fevers, relieves inflammatory joint stiffness, and calms nerve irritation."
            ),
            CulpeperHerbalPrescription(
                herb_name="Valerian Root",
                botanical_name="Valeriana officinalis",
                ruling_planet="Mercury & Saturn",
                temperament_action="Warms Melancholic dryness, relaxes spasmodic tension",
                cure_mechanism="Cure by Sympathy",
                traditional_use="Sedative for agitated neural circuits, relieves nocturnal restlessness, and relaxes visceral muscle spasms."
            ),
            CulpeperHerbalPrescription(
                herb_name="Horsetail",
                botanical_name="Equisetum arvense",
                ruling_planet="Saturn",
                temperament_action="Mineralizes cold/dry Melancholic tissues",
                cure_mechanism="Cure by Sympathy",
                traditional_use="Rich in bioavailable silica; strengthens brittle bones, fortifies connective tissue, and tones renal filtration."
            )
        ]
        return prescriptions
