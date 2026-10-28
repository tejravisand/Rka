"""
Progeny, Conception, and Pregnancy Loss (Miscarriage & Abortion) Predictive Engine.
Implements:
1. 5th House (Putra Bhava), 5th Lord placement, and Putrakaraka (Jupiter) dignity.
2. Prediction of Living Children count & Vamsha Vriddhi Yoga.
3. Spontaneous Miscarriage (Garbha Srava) vulnerability (5th Lord in 8th / Saturn-Ketu coldness).
4. Induced / Surgical Abortion (Garbha Pata) vulnerability (Mars-Rahu surgical affliction to 5th / 8th / 12th).
5. Female Kshetra Sphuta (Moon + Mars + Jupiter) & Male Beeja Sphuta (Sun + Venus + Jupiter) fertility indices.
6. D7 Saptamsha Chart verification for microscopic confirmation of pregnancy outcomes.
7. Month-wise Gestation Risk Rulers (Varahamihira & Parashara Garbhadhana protocol).
8. Specific protective Vedic Upayas for pregnancy protection and lineage continuation.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from app.models.astrological import Kundali, PlanetPosition, ZodiacSign
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT
from app.core.vargas import calculate_all_vargas


@dataclass
class MonthWiseGestationRisk:
    month_number: int
    ruling_planet: str
    fetal_development_stage: str
    astrological_vulnerability: str
    safeguard_upaya: str


@dataclass
class ProgenyPregnancyAssessment:
    progeny_vitality_score: int                 # 0 to 100 points
    living_children_verdict: str               # "Confirmed: 2 Children (Vamsha Vriddhi Yoga)", etc.
    miscarriage_risk_level: str                # "Low / Minimal (<20%)", "Moderate (25-45%)", "Elevated / Severe (>50%)"
    abortion_surgical_risk_level: str          # "Minimal / Unlikely", "Elevated Surgical Vulnerability"
    fertility_sphuta_analysis: str             # Female Kshetra Sphuta or Male Beeja Sphuta details
    fifth_house_and_lord_dynamics: str         # 5th house sign, lord placement, occupants
    d7_saptamsha_confirmation: str              # Microscopic outcome in D7
    key_vulnerability_triggers: List[str]      # Specific risk triggers identified
    vulnerable_gestation_timeline: List[MonthWiseGestationRisk] # Gestation months requiring vigilance
    protective_pregnancy_remedies: List[str]   # Upayas to avert losses and protect children


class ProgenyPregnancyEngine:
    """Predictive engine for progeny, womb fertility, and miscarriage/abortion risks."""

    GESTATION_PLANETS = [
        (1, "Venus", "Semen and ovum combine into fluid (Kalala)", "Chemical pregnancy, failed implantation"),
        (2, "Mars", "Solidification of tissue (Ghana)", "Peak risk of spontaneous bleeding / miscarriage"),
        (3, "Jupiter", "Sprouting of limbs and vital organs (Ankura)", "Embryonic arrest, structural defects"),
        (4, "Sun", "Skeletal formation and heart vitality (Asthi)", "Maternal fever or vitality drop"),
        (5, "Moon", "Skin, blood vessels, and mind (Rakta/Tvak)", "Amniotic fluid imbalance, maternal anxiety"),
        (6, "Saturn", "Hair, nails, bodily strength (Snayu)", "Cervical insufficiency, IUGR growth lag"),
        (7, "Mercury", "Consciousness and nervous system (Chetana)", "Neurological vulnerability, premature labor"),
        (8, "Lagna Lord", "Nourishment through umbilical cord", "Pre-eclampsia, maternal exhaustion"),
        (9, "Sun", "Readiness for birth & fetal movement", "Early contractions"),
        (10, "Moon", "Labor and delivery (Prasava)", "Labor complications")
    ]

    @classmethod
    def evaluate(
        cls,
        kundali: Kundali,
        is_female: bool = True,
        d7_varga: Optional[Any] = None
    ) -> ProgenyPregnancyAssessment:
        lagna_idx = kundali.ascendant.sign.value
        h5_idx = (lagna_idx + 4) % 12
        h8_idx = (lagna_idx + 7) % 12

        lord_5 = SIGN_LORDS[h5_idx]
        pos_5 = kundali.planets[lord_5]
        h5_lord_house = (pos_5.sign.value - lagna_idx) % 12 + 1

        planet_signs = {p: pos.sign.value for p, pos in kundali.planets.items()}
        planet_houses = {p: (sign - lagna_idx) % 12 + 1 for p, sign in planet_signs.items()}

        mars_h = planet_houses.get("Mars", 1)
        rahu_h = planet_houses.get("Rahu", 1)
        sat_h = planet_houses.get("Saturn", 1)
        sun_h = planet_houses.get("Sun", 1)
        jup_h = planet_houses.get("Jupiter", 1)
        jup_pos = kundali.planets["Jupiter"]

        triggers = []
        miscarry_risk_score = 0
        abortion_risk_score = 0

        # 1. 5th Lord in Dusthanas (especially 8th: 4th from 5th = termination of embryo)
        if h5_lord_house == 8:
            miscarry_risk_score += 35
            triggers.append(f"5th Lord ({lord_5}) placed in 8th House (4th from 5th: classic Parashari indicator of initial pregnancy crisis, chemical loss, or spontaneous miscarriage).")
        elif h5_lord_house in [6, 12]:
            miscarry_risk_score += 20
            triggers.append(f"5th Lord ({lord_5}) in Dusthana House {h5_lord_house} (prone to hormonal deficiency, immune challenge, or bed-rest requirement).")

        # 2. Malefics occupying or aspecting 5th House
        planets_in_5 = [p for p, h in planet_houses.items() if h == 5]
        if "Mars" in planets_in_5:
            miscarry_risk_score += 25
            abortion_risk_score += 25
            triggers.append("Mars occupies 5th House (Excessive Pitta heat, pelvic cramping, risk of spontaneous bleeding/Garbha Pata).")
        if "Rahu" in planets_in_5:
            miscarry_risk_score += 25
            abortion_risk_score += 30
            triggers.append("Rahu in 5th House (Sarpa Dosha imprint: sudden unexpected loss, blighted ovum, or medical anomaly).")
        if "Ketu" in planets_in_5:
            miscarry_risk_score += 20
            abortion_risk_score += 20
            triggers.append("Ketu in 5th House (Detachment/severance energy, surgical D&C vulnerability).")
        if "Saturn" in planets_in_5:
            miscarry_risk_score += 20
            triggers.append("Saturn in 5th House (Coldness, progesterone sluggishness, delayed conception).")

        # 3. Mars aspecting 5th House or 5th Lord
        # Mars aspects 4th, 7th, 8th from itself
        mars_aspect_houses = [(mars_h + 3 - 1) % 12 + 1, (mars_h + 6 - 1) % 12 + 1, (mars_h + 7 - 1) % 12 + 1]
        if 5 in mars_aspect_houses and "Mars" not in planets_in_5:
            miscarry_risk_score += 18
            abortion_risk_score += 15
            triggers.append(f"Mars in House {mars_h} casts direct aspect onto 5th House (bleeding/rupture vulnerability).")

        # 4. Exalted Jupiter & Vamsha Vriddhi Yoga Protection
        jup_is_exalted = (jup_pos.sign.value == 3) # Cancer
        jup_in_5 = (jup_h == 5)
        jup_conjunct_l5 = (planet_signs.get("Jupiter") == pos_5.sign.value)

        living_children = "Average Progeny Potential (1 to 2 Children with proper medical care)"
        if jup_is_exalted and (jup_conjunct_l5 or jup_in_5 or jup_h in [1, 5, 9]):
            living_children = "Assured Living Progeny: 2 Children (Vamsha Vriddhi Yoga via Exalted Putrakaraka Jupiter)"
            miscarry_risk_score = max(5, miscarry_risk_score - 25)
            triggers.append("★ SUPREME BLESSING: Exalted Jupiter strongly fortifies 5th Lord/House, ensuring living children survive any initial early hurdles.")
        elif jup_in_5 or jup_conjunct_l5:
            living_children = "Blessed Lineage: 2 Children assured through divine grace."
            miscarry_risk_score = max(5, miscarry_risk_score - 15)

        # 5. Fertility Sphuta (Kshetra Sphuta for Female / Beeja Sphuta for Male)
        if is_female:
            moon_lon = kundali.planets["Moon"].longitude
            mars_lon = kundali.planets["Mars"].longitude
            jup_lon = jup_pos.longitude
            kshetra_deg = (moon_lon + mars_lon + jup_lon) % 360
            ks_sign_idx = int(kshetra_deg / 30)
            ks_deg_in_sign = kshetra_deg % 30
            is_fertile_sign = (ks_sign_idx % 2 == 1) # Even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces)
            sphuta_summary = (
                f"Female Kshetra Sphuta: {ZODIAC_SIGNS[ks_sign_idx]} {ks_deg_in_sign:.2f}° "
                f"({'Fertile Even Sign — Resilient Womb Vitality' if is_fertile_sign else 'Odd/Fiery Sign — Prone to High Pitta / Womb Heat'})"
            )
            if not is_fertile_sign:
                miscarry_risk_score += 10
                triggers.append("Kshetra Sphuta falls in an Odd/Fiery sign, denoting elevated metabolic heat in reproductive tissues.")
        else:
            sun_lon = kundali.planets["Sun"].longitude
            ven_lon = kundali.planets["Venus"].longitude
            jup_lon = jup_pos.longitude
            beeja_deg = (sun_lon + ven_lon + jup_lon) % 360
            b_sign_idx = int(beeja_deg / 30)
            b_deg_in_sign = beeja_deg % 30
            is_fertile_male = (b_sign_idx % 2 == 0) # Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius)
            sphuta_summary = (
                f"Male Beeja Sphuta: {ZODIAC_SIGNS[b_sign_idx]} {b_deg_in_sign:.2f}° "
                f"({'Fertile Odd Sign — Strong Seed Vitality' if is_fertile_male else 'Even Sign — Seed Sluggishness / Semen Quality Check Needed'})"
            )

        # 6. D7 Saptamsha Confirmation
        vargas = getattr(kundali, "vargas", {}) or calculate_all_vargas(kundali.ascendant, kundali.planets)
        d7 = vargas.get(7)
        d7_summary = "D7 Saptamsha confirms normal progeny development."
        if d7:
            d7_lagna_idx = d7.placements["Ascendant"].sign.value
            d7_h5_sign = (d7_lagna_idx + 4) % 12
            d7_l5_name = SIGN_LORDS[d7_h5_sign]
            d7_l5_plc = d7.placements.get(d7_l5_name)
            if d7_l5_plc:
                d7_l5_h = (d7_l5_plc.sign.value - d7_lagna_idx) % 12 + 1
                if d7_l5_h in [6, 8, 12]:
                    miscarry_risk_score += 18
                    d7_summary = f"In D7 Saptamsha, 5th Lord {d7_l5_name} is in House {d7_l5_h} (Dusthana) — signifies initial conception fragility or early chemical loss."
                else:
                    d7_summary = f"In D7 Saptamsha, 5th Lord {d7_l5_name} is favorably placed in House {d7_l5_h}."

        # Risk level grading
        total_miscarry = min(miscarry_risk_score, 85)
        if total_miscarry >= 50:
            miscarry_level = "Elevated / Severe (>50% — High Vulnerability to Early Miscarriage / Garbha Srava)"
        elif total_miscarry >= 25:
            miscarry_level = "Moderate (25-45% — Prone to Initial Pregnancy Delays / Hormone Fluctuations)"
        else:
            miscarry_level = "Low / Minimal (<20% — High Gestational Stability)"

        abortion_level = "Elevated Surgical / Medical Termination Risk" if abortion_risk_score >= 35 else "Minimal / Unlikely"

        h5_info = (
            f"5th House in {ZODIAC_SANSKRIT[h5_idx]} ruled by {lord_5} (placed in House {h5_lord_house}). "
            f"Occupants: {', '.join(planets_in_5) or 'Unoccupied'}. Putrakaraka Jupiter is in {ZODIAC_SANSKRIT[jup_pos.sign.value]} (House {jup_h})."
        )

        # Gestation Timeline Matrix
        gestation_risks = []
        for m_num, r_planet, stage, vul in cls.GESTATION_PLANETS:
            upaya = "Maintain sattvic calm & light cooling diet."
            if r_planet == "Mars":
                upaya = "Avoid hot spices/papaya; strict bed-rest in month 2; recite Mangala Kavacham."
            elif r_planet == "Venus":
                upaya = "Progesterone support as advised by OBGYN; avoid travel in month 1."
            elif r_planet == "Saturn":
                upaya = "Monitor cervical length; light til-oil lamp on Saturdays."
            gestation_risks.append(MonthWiseGestationRisk(
                month_number=m_num,
                ruling_planet=r_planet,
                fetal_development_stage=stage,
                astrological_vulnerability=vul,
                safeguard_upaya=upaya
            ))

        remedies = [
            "Chant the sacred Santana Gopala Mantra 108 times daily facing East: 'Om Devaki Suta Govinda Vasudeva Jagatpate, Dehi Me Tanayam Krishna Tvamaham Sharanam Gatah'.",
            "Read or listen to the sacred Harivamsa Purana (specifically the Santana Gopala chapter) during the 2nd and 3rd trimesters.",
            "Wear a certified 5-Mukhi or Gauri-Shankar Rudraksha to balance hormonal vitality and calm autonomic anxiety.",
            "Avoid spicy, excessive red-meat, or high-Pitta foods during the first 12 weeks of gestation.",
            "Water the sacred Peepal (Ficus religiosa) or Ashoka tree on Thursday and Friday mornings."
        ]

        vitality_score = max(15, 100 - total_miscarry + (20 if jup_is_exalted else 0))

        return ProgenyPregnancyAssessment(
            progeny_vitality_score=min(100, vitality_score),
            living_children_verdict=living_children,
            miscarriage_risk_level=miscarry_level,
            abortion_surgical_risk_level=abortion_level,
            fertility_sphuta_analysis=sphuta_summary,
            fifth_house_and_lord_dynamics=h5_info,
            d7_saptamsha_confirmation=d7_summary,
            key_vulnerability_triggers=triggers if triggers else ["No major malefic afflictions identified in 5th house/lord."],
            vulnerable_gestation_timeline=gestation_risks[:6], # Key first 6 months
            protective_pregnancy_remedies=remedies
        )
