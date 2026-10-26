"""
Education Stream, Education Break, and Profession Predictive Engine.
Implements:
1. Education Stream: Primary & Secondary academic fields based on 4th House (Vidya),
   5th House (Buddhi / Intellect), 9th House (Higher Education), D24 (Siddhamsa / Chaturvimshamsha),
   and Karakas (Mercury, Jupiter, Mars, Sun, Venus, Rahu, Ketu, Saturn).
2. Education Break: Interruption, gap-year, backlog, or stream-change risk evaluation,
   vulnerable age windows, astrological root causes, and academic Saraswati remedies.
3. Profession: Vocational trajectory, Corporate vs Govt vs Own Business vs Advisory,
   10th House (Karma), 6th House (Seva), D10 Dashamsha, Amatyakaraka, and top industry sectors.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.models.astrological import Kundali, PlanetPosition, ZodiacSign
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT
from app.core.vargas import calculate_all_vargas


@dataclass
class EducationStreamProfile:
    primary_stream: str                 # e.g., "Engineering & Technology (STEM / Computer Science)"
    secondary_stream: str               # e.g., "Management & Commercial Analytics (MBA / Finance)"
    key_planetary_influences: List[str] # Planets shaping intellect
    fourth_house_status: str            # Foundational education & degrees
    fifth_house_status: str             # Intellect, analytical faculty & specialization
    ninth_house_status: str             # Masters, research & higher learning
    d24_siddhamsa_summary: str          # D24 divisional confirmation
    recommended_degrees: List[str]      # e.g., ["B.Tech / M.Tech in CS/AI", "MBA / MS", "Data Science"]


@dataclass
class EducationBreakAssessment:
    break_risk_level: str               # "Low / Minimal (<15%)", "Moderate (30-45%)", "High / Significant (>60%)"
    vulnerable_age_windows: List[str]   # e.g., ["Ages 17-19 (Secondary to Tertiary Transition)", "Ages 21-23"]
    astrological_drivers: str           # Dusthana lords, Rahu-Ketu axis, Saturn aspect
    break_nature: str                   # "Course correction / change of stream", "Health/relocation drag", "Smooth flow"
    resumption_and_recovery: str        # How the native completes/recovers from academic hurdles
    academic_remedies: List[str]        # Saraswati Mantra, study directions, gems, fasting


@dataclass
class ProfessionProfile:
    career_path_verdict: str            # "Corporate Executive / Salaried Leadership", "Independent Business", "Govt/PSU"
    tenth_house_status: str             # 10th Karma Bhava sign, lord, aspects
    sixth_vs_seventh_balance: str       # Service (6th) vs Business / Partnership (7th)
    d10_dashamsha_confirmation: str     # Sun dignity, 10th lord in D10
    amatyakaraka_planet: str            # Planet with 2nd highest degree
    amatyakaraka_guidance: str
    top_recommended_domains: List[str]  # Industry domains
    leadership_timeline: str            # Key Dasha phases of professional elevation


class EducationProfessionEngine:
    """Calculates education stream, breaks, and profession."""

    @classmethod
    def evaluate_education_stream(cls, kundali: Kundali) -> EducationStreamProfile:
        lagna_idx = kundali.ascendant.sign.value
        h4_idx = (lagna_idx + 3) % 12
        h5_idx = (lagna_idx + 4) % 12
        h9_idx = (lagna_idx + 8) % 12

        lord_4 = SIGN_LORDS[h4_idx]
        lord_5 = SIGN_LORDS[h5_idx]
        lord_9 = SIGN_LORDS[h9_idx]

        mer_pos = kundali.planets["Mercury"]
        jup_pos = kundali.planets["Jupiter"]
        mars_pos = kundali.planets["Mars"]
        sun_pos = kundali.planets["Sun"]
        ven_pos = kundali.planets["Venus"]
        sat_pos = kundali.planets["Saturn"]
        rahu_pos = kundali.planets["Rahu"]

        # Check D24 (Siddhamsa) if present
        vargas = getattr(kundali, "vargas", {}) or calculate_all_vargas(kundali.ascendant, kundali.planets)
        d24 = vargas.get(24)
        d24_text = "D24 Siddhamsa confirms strong academic aptitude."
        if d24:
            d24_jup = d24.placements.get("Jupiter")
            d24_mer = d24.placements.get("Mercury")
            if d24_jup and d24_mer:
                d24_text = (
                    f"In D24 Siddhamsa, Jupiter is in {d24_jup.sign.sanskrit_name} ({d24_jup.dignity}) "
                    f"and Mercury is in {d24_mer.sign.sanskrit_name} ({d24_mer.dignity}), confirming high academic retention."
                )

        # Stream Determination Logic
        # Mars + Mercury or Rahu + Mercury/Mars -> Engineering / Tech / IT / Data
        # Sun + Jupiter or Mars + Sun -> Medicine / Surgery / Biotech / Civil Services
        # Mercury + Venus or Jupiter + Mercury -> Finance / Commerce / CA / Economics
        # Jupiter + Sun or Mars -> Law / Governance / Political Science
        # Venus + Mercury -> Architecture / Design / Media / Digital Arts
        intellect_planets = [lord_5, mer_pos.planet.value, jup_pos.planet.value]
        if mars_pos.planet.value in [lord_4, lord_5] or mer_pos.sign.value in [0, 7, 9]:
            primary_stream = "Engineering, Computer Science & Applied Technology (STEM / IT / AI / Electronics)"
            secondary_stream = "Operations Research, Technical Project Management & Industrial Systems"
            degrees = ["B.Tech / B.E. in Computer Science / ECE / Mechanical", "M.S. in Data Analytics / AI", "MBA in Tech Management"]
        elif sun_pos.planet.value in [lord_4, lord_5] or jup_pos.sign.value in [3, 8]:
            primary_stream = "Medicine, Life Sciences, Healthcare & Administrative Governance"
            secondary_stream = "Biotechnology, Public Health Policy & Pharmaceutical Sciences"
            degrees = ["MBBS / BDS / MD", "B.Pharm / M.Pharm", "M.Sc. in Biotechnology / Genetics", "UPSC / Civil Services"]
        elif ven_pos.planet.value in [lord_4, lord_5] or mer_pos.sign.value in [1, 2, 5, 6]:
            primary_stream = "Commerce, Financial Economics, Corporate Accounting & Business Analytics"
            secondary_stream = "Corporate Law, International Banking & Chartered Accountancy (CA / CFA)"
            degrees = ["B.Com / BBA (Finance)", "Chartered Accountancy (CA) / CFA", "M.Sc. Financial Engineering", "MBA in Finance"]
        else:
            primary_stream = "Management, Strategic Consulting, Law & Applied Sciences"
            secondary_stream = "Information Systems, Corporate Communications & Digital Media"
            degrees = ["B.Tech / BCA followed by MBA", "Integrated Corporate Law (B.A. LL.B)", "M.S. in Information Systems"]

        h4_desc = f"House 4 in {ZODIAC_SANSKRIT[h4_idx]} ruled by {lord_4} establishes foundational academic discipline."
        h5_desc = f"House 5 in {ZODIAC_SANSKRIT[h5_idx]} ruled by {lord_5} grants sharp analytical intellect and quick problem-solving."
        h9_desc = f"House 9 in {ZODIAC_SANSKRIT[h9_idx]} ruled by {lord_9} supports advanced professional certifications and higher degrees."

        return EducationStreamProfile(
            primary_stream=primary_stream,
            secondary_stream=secondary_stream,
            key_planetary_influences=intellect_planets,
            fourth_house_status=h4_desc,
            fifth_house_status=h5_desc,
            ninth_house_status=h9_desc,
            d24_siddhamsa_summary=d24_text,
            recommended_degrees=degrees
        )

    @classmethod
    def evaluate_education_break(cls, kundali: Kundali) -> EducationBreakAssessment:
        lagna_idx = kundali.ascendant.sign.value
        h4_idx = (lagna_idx + 3) % 12
        h5_idx = (lagna_idx + 4) % 12

        lord_4 = SIGN_LORDS[h4_idx]
        lord_5 = SIGN_LORDS[h5_idx]

        # Dusthana houses
        dusthana_signs = [(lagna_idx + 5) % 12, (lagna_idx + 7) % 12, (lagna_idx + 11) % 12]  # 6, 8, 12

        l4_sign = kundali.planets[lord_4].sign.value
        l5_sign = kundali.planets[lord_5].sign.value

        rahu_sign = kundali.planets["Rahu"].sign.value
        sat_sign = kundali.planets["Saturn"].sign.value

        # Count break indicators
        risk_score = 0
        reasons = []

        if l4_sign in dusthana_signs:
            risk_score += 1
            reasons.append(f"4th Lord ({lord_4}) placed in Dusthana (House of obstacles/relocation).")
        if l5_sign in dusthana_signs:
            risk_score += 1
            reasons.append(f"5th Lord ({lord_5}) placed in Dusthana, indicating distraction or curriculum shift.")
        if rahu_sign in [h4_idx, h5_idx]:
            risk_score += 1
            reasons.append("Rahu influences academic houses, creating unconventional study paths or sudden stream switches.")
        if sat_sign in [h4_idx, h5_idx]:
            risk_score += 1
            reasons.append("Saturn's presence or aspect induces procedural delays, heavy workload stress, or gap semesters.")

        if risk_score >= 3:
            level = "High / Pronounced Vulnerability (60-75%)"
            windows = ["Ages 17-19 (Pre-University to College Transition)", "Ages 21-23 (Final Degree Completion Phase)"]
            nature = "Formal break of 6-12 months, change of academic discipline, or temporary backlog clearance."
            resumption = "Complete resumption guaranteed post-remedial pacification; final degree achieved with resilience."
        elif risk_score >= 1:
            level = "Moderate / Temporary Friction (25-40%)"
            windows = ["Ages 18-20 (First/Second year of Degree)", "Exam season under malefic Antardasha"]
            nature = "Temporary pause, drop for competitive exam preparation (e.g. JEE/NEET/GATE/CAT), or degree change."
            resumption = "Smooth recovery through disciplined revision; no permanent disruption of academic credentials."
        else:
            level = "Low / Minimal (<15%)"
            windows = ["Nominal exam stress under Saturn transit"]
            nature = "Unbroken, steady academic progression with consistent grades."
            resumption = "Clear sailing through higher degrees and professional certifications."

        remedies = [
            "Chant the sacred Saraswati Bija Mantra 108 times daily facing North-East: 'Om Aim Saraswatyai Namah'.",
            "Wear a natural 4-Mukhi Rudraksha (ruled by Lord Brahma & Mercury) to sharpen memory and concentration.",
            "Study facing North or East; keep the study desk clutter-free and place a small brass idol of Saraswati or a crystal pencil on the desk.",
            "Feed green whole moong dal to sacred cows or wild birds on Wednesday mornings to neutralize Budha afflictions.",
            "Donate stationery, notebooks, and pens to underprivileged students on Shukla Paksha Wednesdays."
        ]

        return EducationBreakAssessment(
            break_risk_level=level,
            vulnerable_age_windows=windows,
            astrological_drivers="; ".join(reasons) if reasons else "Benefic planetary alignment shields against education breaks.",
            break_nature=nature,
            resumption_and_recovery=resumption,
            academic_remedies=remedies
        )

    @classmethod
    def evaluate_profession(cls, kundali: Kundali) -> ProfessionProfile:
        lagna_idx = kundali.ascendant.sign.value
        h10_idx = (lagna_idx + 9) % 12
        h6_idx = (lagna_idx + 5) % 12
        h7_idx = (lagna_idx + 6) % 12

        lord_10 = SIGN_LORDS[h10_idx]
        lord_6 = SIGN_LORDS[h6_idx]
        lord_7 = SIGN_LORDS[h7_idx]

        # Calculate Amatyakaraka (AmK): planet with 2nd highest degrees (excluding Rahu/Ketu)
        classical_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        sorted_by_deg = sorted(
            [(p, kundali.planets[p].degrees_in_sign) for p in classical_planets],
            key=lambda x: x[1],
            reverse=True
        )
        amk_planet = sorted_by_deg[1][0] if len(sorted_by_deg) > 1 else "Mercury"

        amk_meanings = {
            "Sun": "Executive leadership, government contracts, authoritative administration, director-level status.",
            "Moon": "Public relations, human resources, institutional advisory, hospitality, healthcare management.",
            "Mars": "Technical engineering, real estate execution, defense/police, industrial operations, surgery.",
            "Mercury": "Consulting, financial analysis, software architecture, commerce, strategic negotiation.",
            "Jupiter": "Corporate governance, higher legal advisory, wealth management, institutional education.",
            "Venus": "Creative luxury, media entertainment, architectural design, corporate lifestyle branding.",
            "Saturn": "Large-scale organizational structure, manufacturing, infrastructure projects, labor relations."
        }

        # Check D10 Dashamsha
        vargas = getattr(kundali, "vargas", {}) or calculate_all_vargas(kundali.ascendant, kundali.planets)
        d10 = vargas.get(10)
        d10_text = "D10 Dashamsha validates executive authority and career elevation."
        if d10:
            sun_d10 = d10.placements.get("Sun")
            l10_d10 = d10.placements.get(lord_10)
            if sun_d10:
                d10_text = f"In D10 Dashamsha, Sun is placed in {sun_d10.sign.sanskrit_name} ({sun_d10.dignity}), confirming professional stature and leadership."

        # Balance between Service (6th) and Business/Enterprise (7th/10th)
        if lord_10 in ["Mars", "Sun", "Jupiter"] or amk_planet in ["Sun", "Mars", "Jupiter"]:
            path = "Corporate Salaried Executive transitioning into Independent Consulting / Enterprise Directorship"
            balance = "Potent 10th-6th nexus indicates steady rise in structured organizations followed by independent directorship."
            domains = [
                "Industrial Engineering / Infrastructure Project Management",
                "High-Tech IT / Software Solutions & Enterprise Consulting",
                "Strategic Advisory / Corporate Governance & Quality Control",
                "Real Estate Project Development & Commercial Land Advisory"
            ]
        elif lord_10 in ["Mercury", "Venus"] or amk_planet in ["Mercury", "Venus"]:
            path = "Commercial Enterprise, High-Finance Advisory & Technology Consulting"
            balance = "Strong 7th-10th commercial linkage favors independent consulting, trade, and financial partnerships."
            domains = [
                "Financial Analytics, Wealth Management & Investment Consulting",
                "Digital Technology, Media Architecture & Product Solutions",
                "Commercial Trade Partnerships & International Business",
                "Executive Recruitment & Corporate Operations Advisory"
            ]
        else:
            path = "Institutional Leadership & Senior Corporate Management"
            balance = "Balanced 6th-10th Upachaya configuration guarantees steady professional elevation through merit."
            domains = [
                "Organizational Operations & Supply Chain Logistics",
                "Corporate Legal Compliance & Institutional Management",
                "Public Sector Enterprise / Semi-Government Authority",
                "Technical Advisory & Engineering Services"
            ]

        h10_status = f"House 10 (Karma Bhava) in {ZODIAC_SANSKRIT[h10_idx]} governed by {lord_10} drives executive ambition and reputation."
        timeline = "Major professional leap occurs during the Antardasha of the 10th Lord or Amatyakaraka, bringing title elevation and fiscal expansion."

        return ProfessionProfile(
            career_path_verdict=path,
            tenth_house_status=h10_status,
            sixth_vs_seventh_balance=balance,
            d10_dashamsha_confirmation=d10_text,
            amatyakaraka_planet=amk_planet,
            amatyakaraka_guidance=amk_meanings.get(amk_planet, "Empowers professional achievement."),
            top_recommended_domains=domains,
            leadership_timeline=timeline
        )
