"""
Vedic Medical Astrology Engine (Ayur-Jyotisha)
==============================================
Based on Brihat Parashara Hora Shastra (BPHS), classical Ayur-Veda,
and traditional Ayur-Jyotisha doctrines.

Implements:
1. Tridosha Analysis (Vata, Pitta, Kapha constitutional Prakriti & Vikriti).
2. Sapta Dhatu (Seven Biological Tissues: Rasa, Rakta, Mamsa, Meda, Asthi, Majja, Shukra).
3. Trika Bhavas (6th Roga, 8th Randhra/Mrityu, 12th Vyaya) & Maraka/Badhaka Sthanas.
4. Kaala Purusha Anatomical Mapping (12 Body Zones from Head to Feet).
5. D30 Trimshamsha Arishta & Disease Tendency Verification.
6. Clinical Vulnerability Checks (Cardiovascular, Metabolic/Diabetes, Neurological, Digestive Agni, etc.).
7. Classical Ayur-Jyotisha Chikitsa (Ayurvedic herbs, Ahara/diet, medical gemstone safety, and healing mantras).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from app.models.astrological import Kundali, PlanetPosition, ZodiacSign, Planet, Bhava
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT
from app.core.vargas import calculate_all_vargas


@dataclass
class DoshaProfile:
    vata_pct: float
    pitta_pct: float
    kapha_pct: float
    dominant_prakriti: str
    secondary_prakriti: str
    imbalance_risk: str
    description: str


@dataclass
class DhatuAssessment:
    dhatu_name: str
    sanskrit_name: str
    governing_planets: List[str]
    function: str
    status: str             # "Balanced", "Moderate Strain", "High Vulnerability"
    affliction_notes: str


@dataclass
class TrikaHouseHealth:
    house_num: int
    bhava_name: str
    sign: str
    lord: str
    lord_placement: str
    occupants: List[str]
    health_significance: str
    risk_level: str         # "Low", "Moderate", "Elevated", "Critical"
    indications: List[str]


@dataclass
class AnatomicalZoneAssessment:
    zone_num: int
    zone_name: str
    sign_name: str
    body_parts: str
    risk_level: str         # "Normal", "Mild Sensitivity", "Significant Vulnerability"
    afflicting_factors: List[str]
    recommendation: str


@dataclass
class MedicalDiagnosisSummary:
    cardiovascular_risk: str
    metabolic_diabetes_risk: str
    digestive_agni_strength: str
    mental_neurological_balance: str
    musculoskeletal_joint_health: str
    surgery_accident_vulnerability: str
    overall_vitality_ojas: str
    summary_verdict: str


@dataclass
class AyurJyotishaRemedies:
    ayurvedic_herbs: List[Dict[str, str]]
    dietary_guidelines_ahara: List[str]
    foods_to_avoid: List[str]
    healing_mantras: List[Dict[str, str]]
    medical_gemstone_cautions: List[str]
    lifestyle_vihara_recommendations: List[str]
    healing_charity_danam: List[str]


@dataclass
class MedicalAstrologyReport:
    client_name: str
    lagna_sign: str
    lagna_lord: str
    moon_sign: str
    sun_sign: str
    dosha_profile: DoshaProfile
    dhatu_assessments: List[DhatuAssessment]
    trika_houses: List[TrikaHouseHealth]
    maraka_badhaka_analysis: Dict[str, Any]
    anatomical_zones: List[AnatomicalZoneAssessment]
    d30_trimshamsha_insights: List[Dict[str, str]]
    diagnosis_summary: MedicalDiagnosisSummary
    remedial_chikitsa: AyurJyotishaRemedies


class VedicMedicalAstrologyEngine:
    """
    Complete Parashari Ayur-Jyotisha computational and diagnostic engine.
    """

    # Kaala Purusha 12 Zones
    ANATOMICAL_ZONES = [
        {"name": "Head & Brain", "parts": "Brain, skull, forehead, cranium, cerebral circulation, scalp"},
        {"name": "Face & Throat", "parts": "Face, right eye, mouth, teeth, tongue, throat, vocal cords, thyroid"},
        {"name": "Shoulders & Respiratory", "parts": "Shoulders, upper chest, arms, collarbone, trachea, bronchi, lungs"},
        {"name": "Chest & Heart Walls", "parts": "Chest, cardiac walls, breasts, pericardium, upper stomach, ribs"},
        {"name": "Solar Plexus & Liver", "parts": "Heart vitality, upper spine, stomach, solar plexus, liver, spleen"},
        {"name": "Lower Abdomen & Intestines", "parts": "Lower abdomen, intestines, appendix, colon, digestive enzymes, navel"},
        {"name": "Kidneys & Lumbar", "parts": "Kidneys, lumbar spine, groin, skin balance, adrenals, pelvic region"},
        {"name": "Genito-Urinary & Rectum", "parts": "Excretory organs, external genitalia, rectum, prostate, perineum"},
        {"name": "Hips & Arterial System", "parts": "Hips, thighs, sciatic nerve, femoral vessels, sacral plexus"},
        {"name": "Knees & Skeletal Structure", "parts": "Knees, patella, joints, skeletal framework, bone density"},
        {"name": "Calves & Peripheral Circulation", "parts": "Calves, shins, ankles, peripheral circulation, nerve impulses"},
        {"name": "Feet & Lymphatics", "parts": "Feet, toes, lymphatic system, left eye, immune barrier, sleep centres"}
    ]

    # Element and Dosha associations of signs
    SIGN_DOSHAS = [
        "Pitta",        # Aries - Fire
        "Vata-Kapha",   # Taurus - Earth
        "Vata",         # Gemini - Air
        "Kapha",        # Cancer - Water
        "Pitta",        # Leo - Fire
        "Vata",         # Virgo - Earth
        "Vata-Pitta",   # Libra - Air
        "Kapha-Pitta",  # Scorpio - Water
        "Pitta",        # Sagittarius - Fire
        "Vata",         # Capricorn - Earth
        "Vata",         # Aquarius - Air
        "Kapha"         # Pisces - Water
    ]

    # Planetary dosha assignments according to BPHS
    PLANET_DOSHAS = {
        "Sun": {"Pitta": 0.8, "Vata": 0.1, "Kapha": 0.1},
        "Moon": {"Pitta": 0.1, "Vata": 0.3, "Kapha": 0.6},
        "Mars": {"Pitta": 0.85, "Vata": 0.1, "Kapha": 0.05},
        "Mercury": {"Pitta": 0.25, "Vata": 0.5, "Kapha": 0.25},
        "Jupiter": {"Pitta": 0.15, "Vata": 0.15, "Kapha": 0.7},
        "Venus": {"Pitta": 0.1, "Vata": 0.4, "Kapha": 0.5},
        "Saturn": {"Pitta": 0.05, "Vata": 0.85, "Kapha": 0.1},
        "Rahu": {"Pitta": 0.2, "Vata": 0.7, "Kapha": 0.1},
        "Ketu": {"Pitta": 0.75, "Vata": 0.2, "Kapha": 0.05}
    }

    @classmethod
    def evaluate(
        cls,
        kundali: Kundali,
        client_name: str = "Native"
    ) -> MedicalAstrologyReport:
        """
        Executes full Parashari Medical Astrological Diagnostic.
        """
        # Ensure divisional charts including D30 Trimsamsa are calculated
        if not kundali.vargas or 30 not in kundali.vargas:
            kundali.vargas = calculate_all_vargas(kundali.ascendant, kundali.planets)

        lagna_sign_idx = kundali.ascendant.sign.value
        lagna_sign_name = ZODIAC_SANSKRIT[lagna_sign_idx]
        lagna_lord = SIGN_LORDS[lagna_sign_idx]

        moon_pos = kundali.planets.get("Moon")
        sun_pos = kundali.planets.get("Sun")
        moon_sign = ZODIAC_SANSKRIT[moon_pos.sign.value] if moon_pos else "Unknown"
        sun_sign = ZODIAC_SANSKRIT[sun_pos.sign.value] if sun_pos else "Unknown"

        # 1. Tridosha Profile
        dosha_profile = cls._calculate_dosha_profile(kundali)

        # 2. Sapta Dhatu Assessment
        dhatu_assessments = cls._assess_sapta_dhatus(kundali)

        # 3. Trika Houses (6th, 8th, 12th)
        trika_houses = cls._assess_trika_houses(kundali)

        # 4. Maraka & Badhaka Analysis
        maraka_badhaka = cls._assess_maraka_badhaka(kundali)

        # 5. Kaala Purusha 12 Anatomical Zones
        anatomical_zones = cls._assess_anatomical_zones(kundali)

        # 6. D30 Trimshamsha Medical Insights
        d30_insights = cls._assess_d30_trimshamsha(kundali)

        # 7. Clinical Diagnosis & Vulnerabilities
        diagnosis_summary = cls._synthesize_diagnosis(kundali, dosha_profile, trika_houses)

        # 8. Classical Ayur-Jyotisha Remedies
        remedies = cls._prescribe_chikitsa(kundali, dosha_profile, diagnosis_summary)

        return MedicalAstrologyReport(
            client_name=client_name,
            lagna_sign=lagna_sign_name,
            lagna_lord=lagna_lord,
            moon_sign=moon_sign,
            sun_sign=sun_sign,
            dosha_profile=dosha_profile,
            dhatu_assessments=dhatu_assessments,
            trika_houses=trika_houses,
            maraka_badhaka_analysis=maraka_badhaka,
            anatomical_zones=anatomical_zones,
            d30_trimshamsha_insights=d30_insights,
            diagnosis_summary=diagnosis_summary,
            remedial_chikitsa=remedies
        )

    # -------------------------------------------------------------------------
    # INTERNAL COMPUTATION METHODS
    # -------------------------------------------------------------------------

    @classmethod
    def _calculate_dosha_profile(cls, kundali: Kundali) -> DoshaProfile:
        """Computes weighted Vata, Pitta, Kapha constitutional scores."""
        scores = {"Vata": 0.0, "Pitta": 0.0, "Kapha": 0.0}

        # Weight 1: Ascendant Sign (Weight: 3.0)
        lagna_idx = kundali.ascendant.sign.value
        lagna_dosha_str = cls.SIGN_DOSHAS[lagna_idx]
        if lagna_dosha_str == "Vata":
            scores["Vata"] += 3.0
        elif lagna_dosha_str == "Pitta":
            scores["Pitta"] += 3.0
        elif lagna_dosha_str == "Kapha":
            scores["Kapha"] += 3.0
        elif "Vata" in lagna_dosha_str and "Kapha" in lagna_dosha_str:
            scores["Vata"] += 1.5
            scores["Kapha"] += 1.5
        elif "Vata" in lagna_dosha_str and "Pitta" in lagna_dosha_str:
            scores["Vata"] += 1.5
            scores["Pitta"] += 1.5
        elif "Kapha" in lagna_dosha_str and "Pitta" in lagna_dosha_str:
            scores["Kapha"] += 1.5
            scores["Pitta"] += 1.5

        # Weight 2: Lagna Lord (Weight: 3.0)
        lagna_lord = SIGN_LORDS[lagna_idx]
        if lagna_lord in cls.PLANET_DOSHAS:
            for d, w in cls.PLANET_DOSHAS[lagna_lord].items():
                scores[d] += w * 3.0

        # Weight 3: Moon Position (Weight: 2.5)
        moon_pos = kundali.planets.get("Moon")
        if moon_pos:
            moon_sign_idx = moon_pos.sign.value
            moon_dosha_str = cls.SIGN_DOSHAS[moon_sign_idx]
            if "Vata" in moon_dosha_str: scores["Vata"] += 1.25
            if "Pitta" in moon_dosha_str: scores["Pitta"] += 1.25
            if "Kapha" in moon_dosha_str: scores["Kapha"] += 1.25
            for d, w in cls.PLANET_DOSHAS["Moon"].items():
                scores[d] += w * 2.0

        # Weight 4: Sun Position (Weight: 2.0)
        sun_pos = kundali.planets.get("Sun")
        if sun_pos:
            sun_sign_idx = sun_pos.sign.value
            sun_dosha_str = cls.SIGN_DOSHAS[sun_sign_idx]
            if "Vata" in sun_dosha_str: scores["Vata"] += 1.0
            if "Pitta" in sun_dosha_str: scores["Pitta"] += 1.0
            if "Kapha" in sun_dosha_str: scores["Kapha"] += 1.0
            for d, w in cls.PLANET_DOSHAS["Sun"].items():
                scores[d] += w * 1.5

        # Weight 5: All Planets (Weight: 1.0 each)
        for p_name, pos in kundali.planets.items():
            if p_name in cls.PLANET_DOSHAS:
                for d, w in cls.PLANET_DOSHAS[p_name].items():
                    scores[d] += w * 1.0
                sign_dosha_str = cls.SIGN_DOSHAS[pos.sign.value]
                if "Vata" in sign_dosha_str: scores["Vata"] += 0.5
                if "Pitta" in sign_dosha_str: scores["Pitta"] += 0.5
                if "Kapha" in sign_dosha_str: scores["Kapha"] += 0.5

        total = sum(scores.values()) or 1.0
        v_pct = round((scores["Vata"] / total) * 100, 1)
        p_pct = round((scores["Pitta"] / total) * 100, 1)
        k_pct = round((scores["Kapha"] / total) * 100, 1)

        # Determine dominant and secondary
        sorted_doshas = sorted([("Vata", v_pct), ("Pitta", p_pct), ("Kapha", k_pct)], key=lambda x: x[1], reverse=True)
        dominant = sorted_doshas[0][0]
        secondary = sorted_doshas[1][0]

        if sorted_doshas[0][1] - sorted_doshas[1][1] < 8.0:
            prakriti = f"{dominant}-{secondary} Dual-Prakriti"
        else:
            prakriti = f"{dominant}-Dominant"

        imbalance = f"Vulnerability to {dominant} aggravation during adverse transits and related Dashas."
        desc = (
            f"Native has {prakriti} constitution (Vata: {v_pct}%, Pitta: {p_pct}%, Kapha: {k_pct}%). "
            f"Ayur-Jyotisha diagnostic indicates metabolic regulation should prioritize pacifying {dominant} "
            f"while sustaining balance in {secondary}."
        )

        return DoshaProfile(
            vata_pct=v_pct,
            pitta_pct=p_pct,
            kapha_pct=k_pct,
            dominant_prakriti=prakriti,
            secondary_prakriti=secondary,
            imbalance_risk=imbalance,
            description=desc
        )

    @classmethod
    def _assess_sapta_dhatus(cls, kundali: Kundali) -> List[DhatuAssessment]:
        """Assesses health and vulnerability of the 7 bodily tissues (Sapta Dhatus)."""
        dhatus_spec = [
            ("Rasa", "Plasma / Lymph / Intercellular Fluid", ["Moon", "Venus"], "Nourishment, circulation, bodily hydration"),
            ("Rakta", "Blood / Hemoglobin / Oxygenation", ["Mars", "Sun"], "Thermal distribution, tissue vitality, complexion"),
            ("Mamsa", "Muscle Tissue / Tendons", ["Mercury", "Mars"], "Structural motility, muscle strength, physical armor"),
            ("Meda", "Adipose Tissue / Fat", ["Jupiter"], "Lubrication, lipid reserves, internal organ cushion"),
            ("Asthi", "Bone Matrix / Teeth / Skeletal", ["Sun", "Saturn"], "Structural posture, marrow enclosure, calcium matrix"),
            ("Majja", "Bone Marrow & Nervous System", ["Mars", "Mercury", "Saturn"], "Neural conduction, hematopoiesis, brain substance"),
            ("Shukra", "Reproductive Tissue / Ojas Vitality", ["Venus", "Moon"], "Cellular regeneration, hormonal homeostasis, immunity")
        ]

        results = []
        for d_name, sanskrit_desc, rulers, func in dhatus_spec:
            afflicted_rulers = []
            for r in rulers:
                pos = kundali.planets.get(r)
                if pos:
                    if pos.dignity in ["Debilitated", "Enemy"]:
                        afflicted_rulers.append(f"{r} in {pos.dignity} dignity")
                    # Check if in 6th, 8th, or 12th house
                    h_num = cls._get_planet_house(pos, kundali)
                    if h_num in [6, 8, 12]:
                        afflicted_rulers.append(f"{r} situated in Dusthana House {h_num}")
                    if pos.is_retrograde and r in ["Mars", "Saturn", "Mercury"]:
                        afflicted_rulers.append(f"{r} Retrograde")

            if len(afflicted_rulers) >= 2:
                status = "High Vulnerability"
                notes = f"Significant strain on {d_name} Dhatu due to: {', '.join(afflicted_rulers)}. Requires specific dietary and herbal fortification."
            elif len(afflicted_rulers) == 1:
                status = "Moderate Strain"
                notes = f"Mild sensitivity observed: {afflicted_rulers[0]}. Monitor during active Bhuktis."
            else:
                status = "Balanced"
                notes = f"Governing planets ({', '.join(rulers)}) maintain sufficient functional strength. Tissues remain stable."

            results.append(DhatuAssessment(
                dhatu_name=d_name,
                sanskrit_name=sanskrit_desc,
                governing_planets=rulers,
                function=func,
                status=status,
                affliction_notes=notes
            ))

        return results

    @classmethod
    def _assess_trika_houses(cls, kundali: Kundali) -> List[TrikaHouseHealth]:
        """Assesses the Trika houses (6th Roga, 8th Randhra, 12th Vyaya)."""
        trika_defs = [
            (6, "Roga Bhava (Acute Sickness & Digestive Agni)", "Acute diseases, bacterial/viral infections, inflammation, ulcers, digestive fire, immune response"),
            (8, "Randhra / Mrityu Bhava (Chronic Illness & Longevity)", "Chronic degenerative diseases, surgeries, longevity risks, genetic predispositions, excretory/piles issues"),
            (12, "Vyaya Bhava (Hospitalization & Bedridden States)", "Hospital admissions, chronic sleep disorders, mental isolation, eye troubles, feet infections")
        ]

        results = []
        lagna_idx = kundali.ascendant.sign.value

        for h_num, name, significance in trika_defs:
            sign_idx = (lagna_idx + (h_num - 1)) % 12
            sign_name = ZODIAC_SANSKRIT[sign_idx]
            lord_name = SIGN_LORDS[sign_idx]

            # Find lord placement
            lord_pos = kundali.planets.get(lord_name)
            if lord_pos:
                lord_h = cls._get_planet_house(lord_pos, kundali)
                lord_placement = f"{lord_name} in House {lord_h} ({ZODIAC_SANSKRIT[lord_pos.sign.value]}) [{lord_pos.dignity}]"
            else:
                lord_placement = "Unknown"

            # Find occupants
            occupants = []
            for p_name, pos in kundali.planets.items():
                if cls._get_planet_house(pos, kundali) == h_num:
                    occupants.append(f"{p_name} ({pos.dignity})")

            # Determine risk
            risk = "Low"
            indications = []

            if occupants:
                indications.append(f"Occupied by: {', '.join(occupants)}")
            else:
                indications.append("House is vacant from planets")

            # Check malefic factors
            malefics_in_house = [occ for occ in occupants if any(m in occ for m in ["Saturn", "Mars", "Rahu", "Ketu"])]
            if len(malefics_in_house) >= 2 or (lord_pos and lord_pos.dignity == "Debilitated"):
                risk = "Elevated"
                indications.append(f"Multiple malefic influences or debilitated lord ({lord_name}) intensify clinical risk.")
            elif malefics_in_house or (lord_pos and lord_pos.dignity == "Enemy"):
                risk = "Moderate"
                indications.append(f"Moderate sensitivity observed through {lord_name} placement or occupants.")
            else:
                risk = "Low"
                indications.append("Favorable or benign positioning; minimal acute aggravation expected.")

            results.append(TrikaHouseHealth(
                house_num=h_num,
                bhava_name=name,
                sign=sign_name,
                lord=lord_name,
                lord_placement=lord_placement,
                occupants=occupants,
                health_significance=significance,
                risk_level=risk,
                indications=indications
            ))

        return results

    @classmethod
    def _assess_maraka_badhaka(cls, kundali: Kundali) -> Dict[str, Any]:
        """Calculates Maraka (2nd/7th lords) and Badhaka Sthana health triggers."""
        lagna_idx = kundali.ascendant.sign.value
        lagna_modality = kundali.ascendant.sign.modality  # "Movable", "Fixed", "Dual"

        # Maraka lords: 2nd and 7th houses
        maraka_2_idx = (lagna_idx + 1) % 12
        maraka_7_idx = (lagna_idx + 6) % 12
        maraka_2_lord = SIGN_LORDS[maraka_2_idx]
        maraka_7_lord = SIGN_LORDS[maraka_7_idx]

        # Badhaka Sthana per BPHS:
        # Movable sign -> 11th house
        # Fixed sign -> 9th house
        # Dual sign -> 7th house
        if lagna_modality == "Movable":
            badhaka_house = 11
        elif lagna_modality == "Fixed":
            badhaka_house = 9
        else:
            badhaka_house = 7

        badhaka_sign_idx = (lagna_idx + (badhaka_house - 1)) % 12
        badhaka_sign_name = ZODIAC_SANSKRIT[badhaka_sign_idx]
        badhaka_lord = SIGN_LORDS[badhaka_sign_idx]

        return {
            "maraka_lords": [maraka_2_lord, maraka_7_lord],
            "maraka_houses": [2, 7],
            "maraka_summary": f"Primary Maraka (vitality-draining) planets are {maraka_2_lord} (2nd lord) and {maraka_7_lord} (7th lord). Extra healthcare vigilance recommended during their Antardashas.",
            "badhaka_house": badhaka_house,
            "badhaka_sign": badhaka_sign_name,
            "badhaka_lord": badhaka_lord,
            "badhaka_summary": f"Since Lagna is {lagna_modality} ({ZODIAC_SANSKRIT[lagna_idx]}), Badhaka Sthana is House {badhaka_house} ({badhaka_sign_name}) ruled by {badhaka_lord}. This planet can trigger obscure or hard-to-diagnose ailments if afflicted."
        }

    @classmethod
    def _assess_anatomical_zones(cls, kundali: Kundali) -> List[AnatomicalZoneAssessment]:
        """Maps chart influences against the 12 Kaala Purusha anatomical zones."""
        results = []
        lagna_idx = kundali.ascendant.sign.value

        for i, zone in enumerate(cls.ANATOMICAL_ZONES):
            house_num = i + 1
            sign_idx = (lagna_idx + i) % 12
            sign_name = ZODIAC_SANSKRIT[sign_idx]
            sign_lord = SIGN_LORDS[sign_idx]

            afflictions = []
            # Check planets in this house
            for p_name, pos in kundali.planets.items():
                if cls._get_planet_house(pos, kundali) == house_num:
                    if p_name in ["Saturn", "Rahu", "Ketu", "Mars"]:
                        afflictions.append(f"{p_name} occupying ({pos.dignity})")
                    elif pos.dignity in ["Debilitated", "Enemy"]:
                        afflictions.append(f"{p_name} in {pos.dignity} dignity")

            # Check lord condition
            lord_pos = kundali.planets.get(sign_lord)
            if lord_pos and lord_pos.dignity == "Debilitated":
                afflictions.append(f"Zonal ruler {sign_lord} is Debilitated")

            if len(afflictions) >= 2:
                risk = "Significant Vulnerability"
                rec = f"Special prophylactic care required for {zone['name'].lower()}. Routine check-ups advised."
            elif len(afflictions) == 1:
                risk = "Mild Sensitivity"
                rec = f"Maintain mindful lifestyle; protect {zone['name'].lower()} from excessive physical strain or exposure."
            else:
                risk = "Normal"
                rec = f"{zone['name']} enjoys robust natural resilience. Maintain balanced daily regimen."

            results.append(AnatomicalZoneAssessment(
                zone_num=house_num,
                zone_name=zone["name"],
                sign_name=sign_name,
                body_parts=zone["parts"],
                risk_level=risk,
                afflicting_factors=afflictions if afflictions else ["None (Fortified)"],
                recommendation=rec
            ))

        return results

    @classmethod
    def _assess_d30_trimshamsha(cls, kundali: Kundali) -> List[Dict[str, str]]:
        """Extracts medical and disease propensity seeds from D30 Trimshamsha chart."""
        insights = []
        d30_chart = kundali.vargas.get(30)
        if not d30_chart or not d30_chart.placements:
            return [{"planet": "General", "insight": "D30 calculation indicates standard karmic endurance."}]

        # Trimsamsa planetary influences
        rulers_meaning = {
            "Mars": "Acute inflammations, cuts, fevers, surgeries, and blood toxicity",
            "Saturn": "Chronic sluggishness, joint stiffness, degenerative bone/nerve conditions",
            "Jupiter": "Liver congestion, lipid imbalance, endocrine or obesity vulnerabilities",
            "Mercury": "Nervous anxiety, skin allergies, respiratory spasms, mental restlessness",
            "Venus": "Renal, reproductive or urinary sensitivities, hormonal fluctuations"
        }

        for p_name, plc in d30_chart.placements.items():
            if p_name in ["Sun", "Moon", "Ascendant", "Mars", "Saturn"]:
                ruler = plc.sign_lord
                meaning = rulers_meaning.get(ruler, "General karmic resistance")
                insights.append({
                    "planet": p_name,
                    "d30_sign": ZODIAC_SANSKRIT[plc.sign.value],
                    "d30_lord": ruler,
                    "dignity": plc.dignity,
                    "interpretation": f"{p_name} placed in {ruler}'s Trimsamsa: potential sensitivity towards {meaning}."
                })

        return insights

    @classmethod
    def _synthesize_diagnosis(
        cls,
        kundali: Kundali,
        dosha: DoshaProfile,
        trika: List[TrikaHouseHealth]
    ) -> MedicalDiagnosisSummary:
        """Synthesizes clinical risk assessments across major body systems."""
        # 1. Cardiovascular
        sun = kundali.planets.get("Sun")
        mars = kundali.planets.get("Mars")
        cv_risk = "Normal"
        if sun and (sun.dignity in ["Debilitated", "Enemy"] or cls._get_planet_house(sun, kundali) in [6, 8, 12]):
            cv_risk = "Moderate - Watch Blood Pressure & Heart Vitality"
        if mars and cls._get_planet_house(mars, kundali) in [1, 4, 7, 8]:
            if cv_risk != "Normal":
                cv_risk = "Elevated - Comprehensive Cardio & BP Monitoring Recommended"

        # 2. Metabolic & Diabetes
        jup = kundali.planets.get("Jupiter")
        ven = kundali.planets.get("Venus")
        met_risk = "Low"
        if jup and (jup.dignity in ["Debilitated", "Enemy"] or cls._get_planet_house(jup, kundali) in [6, 8]):
            met_risk = "Moderate - Maintain Balanced Carbohydrate/Sugar Intake"
        if ven and (ven.dignity in ["Debilitated"] or cls._get_planet_house(ven, kundali) == 6):
            met_risk = "Elevated - Insulin & Pancreatic Care Advised"

        # 3. Digestive Agni
        h6 = next((h for h in trika if h.house_num == 6), None)
        if dosha.dominant_prakriti.startswith("Pitta"):
            agni = "Tikshnagni (Intense / Acidic Fire - prone to hyperacidity, ulcers, bile surge)"
        elif dosha.dominant_prakriti.startswith("Vata"):
            agni = "Vishamagni (Irregular / Variable Fire - prone to gas, bloating, erratic digestion)"
        elif dosha.dominant_prakriti.startswith("Kapha"):
            agni = "Mandagni (Sluggish / Slow Fire - prone to slow metabolism, heavy feeling, mucus)"
        else:
            agni = "Samagni (Balanced Digestive Fire)"

        # 4. Mental & Neurological
        moon = kundali.planets.get("Moon")
        mer = kundali.planets.get("Mercury")
        sat = kundali.planets.get("Saturn")
        rahu = kundali.planets.get("Rahu")
        neuro_status = "Stable & Alert"
        if moon and (moon.dignity in ["Debilitated", "Enemy"] or cls._get_planet_house(moon, kundali) in [6, 8, 12]):
            neuro_status = "Emotional Sensitivity / Stress Vulnerability"
        if mer and (mer.dignity in ["Debilitated", "Enemy"] or cls._get_planet_house(mer, kundali) in [6, 8, 12]):
            neuro_status = "Nervous Restlessness / Insomnia Susceptibility"

        # 5. Musculoskeletal & Joints
        bone_status = "Robust"
        if sat and (sat.dignity in ["Debilitated", "Enemy"] or sat.is_retrograde):
            bone_status = "Vata Joint Sensitivity / Stiffness Tendency"

        # 6. Surgery & Accident
        surgery_risk = "Low"
        if mars and cls._get_planet_house(mars, kundali) in [6, 8]:
            surgery_risk = "Moderate - Surgical Interventions or Injury Scars Indicated"
        ketu = kundali.planets.get("Ketu")
        if ketu and cls._get_planet_house(ketu, kundali) in [6, 8]:
            surgery_risk = "Elevated - Sharp Precision Procedures / Accidental Prick Caution"

        # 7. Ojas / Vitality
        lagna_lord_name = SIGN_LORDS[kundali.ascendant.sign.value]
        lagna_lord_pos = kundali.planets.get(lagna_lord_name)
        if lagna_lord_pos and lagna_lord_pos.dignity in ["Exalted", "Own", "Friendly"]:
            ojas = "Strong Vital Reserve (High Ojas & Immune Longevity)"
        else:
            ojas = "Moderate Vital Reserve (Requires Nourishing Rasayana Lifestyle)"

        verdict = (
            f"Overall constitutional vitality is guided by {ojas}. "
            f"Digestive Agni exhibits {agni}. Preventive lifestyle should focus on {cv_risk} "
            f"and {neuro_status}."
        )

        return MedicalDiagnosisSummary(
            cardiovascular_risk=cv_risk,
            metabolic_diabetes_risk=met_risk,
            digestive_agni_strength=agni,
            mental_neurological_balance=neuro_status,
            musculoskeletal_joint_health=bone_status,
            surgery_accident_vulnerability=surgery_risk,
            overall_vitality_ojas=ojas,
            summary_verdict=verdict
        )

    @classmethod
    def _prescribe_chikitsa(
        cls,
        kundali: Kundali,
        dosha: DoshaProfile,
        diag: MedicalDiagnosisSummary
    ) -> AyurJyotishaRemedies:
        """Prescribes classical Ayur-Jyotisha Ayurvedic herbs, diet, and spiritual therapies."""
        # Herbs
        herbs = [
            {"herb": "Guduchi (Giloy / Amrita)", "action": "Master immune modulator (Rasayana), balances all three doshas, cleanses liver, purifies blood"},
            {"herb": "Brahmi / Shankhpushpi", "action": "Calms mental agitation, nourishes Majja Dhatu, reduces cortisol and insomnia"},
            {"herb": "Amla (Amalaki)", "action": "Rich in natural antioxidants, fortifies Asthi & Rakta Dhatu, strengthens digestion without increasing Pitta"},
            {"herb": "Ashwagandha", "action": "Deep Vata pacifier, strengthens nervous system, enhances muscle vitality (Mamsa Dhatu)"},
            {"herb": "Triphala Churna", "action": "Gentle bowel regulator, clears metabolic endotoxins (Ama), tones digestive tract"}
        ]

        # Dietary guidance
        ahara = [
            "Favor freshly prepared, warm, easily digestible whole foods aligned with your dominant Prakriti.",
            "Incorporate digestive spices: Cumin, Coriander, Fennel, Cardamom, and Ginger to stabilize Agni.",
            "Stay well hydrated with warm water infused with a drop of lime or boiled with cumin seeds.",
            "Consume meals at regular circadian intervals: substantial lunch between 12:00 PM and 1:30 PM."
        ]

        foods_avoid = [
            "Extremely stale, heavily processed, deep-fried, or artificially preserved foods.",
            "Excessive raw or ice-cold beverages right before or after meals (quenches digestive fire).",
            "Excessively fiery, pungent, or chemically pungent condiments during high-stress periods."
        ]

        # Mantras
        mantras = [
            {
                "deity": "Lord Shiva / Maha Mrityunjaya",
                "mantra": "Om Tryambakam Yajamahe Sugandhim Pushti-Vardhanam | Urvarukamiva Bandhanan Mrityor Mukshiya Mamritat ||",
                "purpose": "Supreme Vedic healing and longevity shield; regenerates cellular vitality and wards off acute disease."
            },
            {
                "deity": "Lord Dhanvantari (Divine Physician)",
                "mantra": "Om Namo Bhagavate Vasudevaya Dhanvantaraye Amrita-Kalasha Hastaya Sarva Maya Vinashanaya Trailokya Nathaya Sri Mahavishnave Namaha ||",
                "purpose": "Invokes the primordial healer for swift diagnosis, cure, and therapeutic success."
            },
            {
                "deity": "Surya Bhagavan (Aditya)",
                "mantra": "Om Hram Hreem Hroum Sah Suryaya Namaha ||",
                "purpose": "Enhances systemic vitality, heart strength, bone mineral density, and inner fire (Ojas)."
            }
        ]

        # Gemstone safety
        gem_cautions = [
            "CRITICAL MEDICAL RULE: Never wear gemstones of the 6th, 8th, or 12th house lords without expert supervision, as they can amplify chronic illness.",
            "Do not wear cracked, chipped, or flawed gemstones which can induce sudden energetic distress.",
            "Favor Sattvic healing gemstones aligned only with your functional benefics (1st, 5th, or 9th lords)."
        ]

        # Vihara (Lifestyle)
        vihara = [
            "Practice gentle Nadi Shodhana (Alternate Nostril Pranayama) for 10-15 minutes daily to harmonize the autonomic nervous system.",
            "Adopt Abhyanga (warm Ayurvedic oil self-massage) with sesame oil (for Vata) or coconut oil (for Pitta) once or twice weekly.",
            "Establish a non-negotiable sleep schedule: lights off by 10:30 PM to optimize hepatic and cellular repair."
        ]

        # Danam (Healing charity)
        danam = [
            "Aushadha Danam: Sponsoring medicines or treatment expenses for impoverished patients on Tuesdays or Saturdays.",
            "Annadanam: Feeding green grass or fresh fodder to cows (Go-Seva) to pacify planetary afflictions.",
            "Planting and watering sacred trees: Neem, Peepal, or Tulsi, which radiate restorative biophysical pranic fields."
        ]

        return AyurJyotishaRemedies(
            ayurvedic_herbs=herbs,
            dietary_guidelines_ahara=ahara,
            foods_to_avoid=foods_avoid,
            healing_mantras=mantras,
            medical_gemstone_cautions=gem_cautions,
            lifestyle_vihara_recommendations=vihara,
            healing_charity_danam=danam
        )

    # -------------------------------------------------------------------------
    # HELPER UTILITIES
    # -------------------------------------------------------------------------

    @classmethod
    def _get_planet_house(cls, planet_pos: PlanetPosition, kundali: Kundali) -> int:
        """Returns 1-based house index (1 to 12) for a given planet position."""
        lagna_idx = kundali.ascendant.sign.value
        planet_sign_idx = planet_pos.sign.value
        return ((planet_sign_idx - lagna_idx) % 12) + 1
