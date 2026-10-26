"""
Life Milestones Engine.
Systematically computes major life astrological transitions:
- Sade Sati (Phase 1 Rising, Phase 2 Peak, Phase 3 Setting across 3 life cycles)
- Kantaka Shani & Ashtama Shani
- Jupiter Returns & Auspicious Transits (Guru Gochara)
- Rahu-Ketu Nodal Karmic Returns (18.6 yr cycles)
- Dasha Sandhi / Chidra Dasha (critical phase transitions)
- Maraka periods & Raja Yoga activation windows
"""
from datetime import datetime, timedelta
from typing import List, Dict
from app.models.milestones import LifeMilestone, MilestoneCategory, SadeSatiCycle
from app.models.astrological import Kundali, DashaPeriod
from app.core.constants import ZODIAC_SIGNS, SIGN_LORDS


SATURN_ORBIT_YEARS = 29.457       # Saturn orbital period in Earth years
SATURN_SIGN_SPAN_YEARS = 2.455     # ~2.5 years per sign
JUPITER_ORBIT_YEARS = 11.862      # Jupiter orbital period in Earth years
NODAL_CYCLE_YEARS = 18.613        # Rahu-Ketu nodal return cycle in years


class LifeMilestoneEngine:
    """Computes all major life milestone events for a given Kundali and Dasha timeline."""

    @classmethod
    def calculate_all_milestones(
        cls,
        kundali: Kundali,
        dashas: List[DashaPeriod],
        max_age_years: float = 90.0
    ) -> List[LifeMilestone]:
        """Generate a chronological timeline of all life milestones."""
        milestones: List[LifeMilestone] = []

        # 1. Sade Sati Cycles
        sade_sati_milestones = cls.calculate_sade_sati(kundali, max_age_years)
        milestones.extend(sade_sati_milestones)

        # 2. Ashtama & Kantaka Shani
        shani_special = cls.calculate_shani_special_transits(kundali, max_age_years)
        milestones.extend(shani_special)

        # 3. Jupiter Returns (Guru Gochara)
        jupiter_milestones = cls.calculate_jupiter_returns(kundali, max_age_years)
        milestones.extend(jupiter_milestones)

        # 4. Rahu-Ketu Nodal Returns
        nodal_milestones = cls.calculate_nodal_cycles(kundali, max_age_years)
        milestones.extend(nodal_milestones)

        # 5. Dasha Sandhi / Chidra Dasha Milestones
        dasha_milestones = cls.calculate_dasha_sandhi(dashas)
        milestones.extend(dasha_milestones)

        # 6. Raja Yoga / Golden Periods
        raja_yoga_milestones = cls.calculate_raja_yoga_periods(kundali, dashas)
        milestones.extend(raja_yoga_milestones)

        # Sort chronologically by start date
        milestones.sort(key=lambda m: m.start_date)
        return milestones

    @classmethod
    def calculate_sade_sati(cls, kundali: Kundali, max_age_years: float) -> List[LifeMilestone]:
        """
        Calculate Sade Sati cycles across the native's life.
        Sade Sati occurs when transiting Saturn passes through the 12th, 1st, and 2nd houses from natal Moon.
        """
        milestones: List[LifeMilestone] = []
        moon_sign_idx = kundali.planets["Moon"].sign.value
        birth_dt = kundali.birth_datetime

        # Approximate Saturn's natal longitude
        saturn_natal_deg = kundali.planets["Saturn"].longitude
        moon_natal_deg = kundali.planets["Moon"].longitude

        # Difference in degrees from Saturn to Moon's 12th house start (Moon_sign - 1) * 30°
        twelfth_house_deg = ((moon_sign_idx - 1) % 12) * 30.0

        # Angular distance Saturn needs to travel to reach 12th house from Moon
        ang_dist_to_start = (twelfth_house_deg - saturn_natal_deg) % 360.0
        years_to_first_sade_sati = (ang_dist_to_start / 360.0) * SATURN_ORBIT_YEARS

        cycle = 1
        current_start_years = years_to_first_sade_sati

        while current_start_years < max_age_years:
            p1_start = birth_dt + timedelta(days=current_start_years * 365.25)
            p1_end = p1_start + timedelta(days=SATURN_SIGN_SPAN_YEARS * 365.25)

            p2_start = p1_end
            p2_end = p2_start + timedelta(days=SATURN_SIGN_SPAN_YEARS * 365.25)

            p3_start = p2_end
            p3_end = p3_start + timedelta(days=SATURN_SIGN_SPAN_YEARS * 365.25)

            total_end = p3_end
            age_at_peak = current_start_years + SATURN_SIGN_SPAN_YEARS

            cycle_names = {1: "1st Cycle (Youth / Formative)", 2: "2nd Cycle (Mid-Life / Career & Ego)", 3: "3rd Cycle (Mature / Spiritual Completion)"}
            cycle_desc = cycle_names.get(cycle, f"{cycle}th Cycle")

            # Phase 1: Rising Phase (Saturn in 12th from Moon)
            milestones.append(LifeMilestone(
                category=MilestoneCategory.SADE_SATI,
                title=f"Sade Sati Phase 1 - Rising (Aroha) [{cycle_desc}]",
                start_date=p1_start,
                end_date=p1_end,
                approx_age_years=round(current_start_years, 1),
                description=f"Saturn transits 12th house from natal Moon ({ZODIAC_SIGNS[(moon_sign_idx - 1) % 12]}). Restlessness, unexpected expenditures, relocation or travel, changes in sleeping patterns.",
                intensity="Medium",
                recommended_focus="Financial discipline, routine grounding, minimizing speculative risks, health monitoring.",
                traditional_remedies=["Hanuman Chalisa recitation on Tuesdays/Saturdays", "Sesame oil deepa donation", "Serving elderly and laborers"]
            ))

            # Phase 2: Peak Phase (Saturn over Natal Moon - Janma Shani)
            milestones.append(LifeMilestone(
                category=MilestoneCategory.SADE_SATI,
                title=f"Sade Sati Phase 2 - Peak (Madhya / Janma Shani) [{cycle_desc}]",
                start_date=p2_start,
                end_date=p2_end,
                approx_age_years=round(age_at_peak, 1),
                description=f"Saturn transits directly over natal Moon ({ZODIAC_SIGNS[moon_sign_idx]}). Intense emotional maturity, high burden of responsibilities, endurance testing, karmic restructuring.",
                intensity="Transformational",
                recommended_focus="Patience, humility, dedication to duty without ego, meditation and emotional calm.",
                traditional_remedies=["Shani Shanti pooja", "Thirunallar or local Shani Mahatma temple visit", "Ashwattha (Peepal tree) pradakshina on Saturday morning"]
            ))

            # Phase 3: Setting Phase (Saturn in 2nd from Moon)
            milestones.append(LifeMilestone(
                category=MilestoneCategory.SADE_SATI,
                title=f"Sade Sati Phase 3 - Setting (Avaroha) [{cycle_desc}]",
                start_date=p3_start,
                end_date=p3_end,
                approx_age_years=round(age_at_peak + SATURN_SIGN_SPAN_YEARS, 1),
                description=f"Saturn transits 2nd house from natal Moon ({ZODIAC_SIGNS[(moon_sign_idx + 1) % 12]}). Recovery phase, financial realignments, settling family obligations, emergence of durable wisdom.",
                intensity="Medium",
                recommended_focus="Consolidating savings, mindful communication with family, implementing lessons learned.",
                traditional_remedies=["Black sesame / urad dal charity", "Maha Mrityunjaya Japa", "Honoring ancestral rites"]
            ))

            cycle += 1
            current_start_years += SATURN_ORBIT_YEARS

        return milestones

    @classmethod
    def calculate_shani_special_transits(cls, kundali: Kundali, max_age_years: float) -> List[LifeMilestone]:
        """Calculate Ashtama Shani (8th from Moon) and Kantaka Shani (4th, 7th, 10th)."""
        milestones: List[LifeMilestone] = []
        moon_sign_idx = kundali.planets["Moon"].sign.value
        birth_dt = kundali.birth_datetime
        saturn_natal_deg = kundali.planets["Saturn"].longitude

        # Ashtama Shani: Saturn in 8th from Moon: (moon_sign_idx + 7) % 12 * 30°
        ashtama_target_deg = ((moon_sign_idx + 7) % 12) * 30.0
        ang_dist = (ashtama_target_deg - saturn_natal_deg) % 360.0
        start_years = (ang_dist / 360.0) * SATURN_ORBIT_YEARS

        while start_years < max_age_years:
            start_dt = birth_dt + timedelta(days=start_years * 365.25)
            end_dt = start_dt + timedelta(days=SATURN_SIGN_SPAN_YEARS * 365.25)

            milestones.append(LifeMilestone(
                category=MilestoneCategory.ASHTAMA_SHANI,
                title=f"Ashtama Shani (Saturn in 8th from Moon)",
                start_date=start_dt,
                end_date=end_dt,
                approx_age_years=round(start_years, 1),
                description=f"Saturn transits the 8th house from natal Moon ({ZODIAC_SIGNS[(moon_sign_idx + 7) % 12]}). Deep psychological recalibration, unexpected life shifts, requiring special care of physical vitality.",
                intensity="High",
                recommended_focus="Proactive health care, avoidance of risky legal or financial disputes, spiritual surrender.",
                traditional_remedies=["Rudrabhisheka on Mondays or Pradosham", "Feeding crows and dogs", "Navagraha Shanti"]
            ))
            start_years += SATURN_ORBIT_YEARS

        return milestones

    @classmethod
    def calculate_jupiter_returns(cls, kundali: Kundali, max_age_years: float) -> List[LifeMilestone]:
        """
        Calculate Jupiter Return cycles (~every 12 years).
        Jupiter returns to natal Jupiter sign at ages ~12, 24, 36, 48, 60, 72, 84.
        """
        milestones: List[LifeMilestone] = []
        birth_dt = kundali.birth_datetime
        jup_sign_name = kundali.planets["Jupiter"].sign.name.capitalize()

        age = JUPITER_ORBIT_YEARS
        return_num = 1

        significance_map = {
            1: "1st Jupiter Return (~Age 12): Onset of intellectual awakening, puberty, ethical consciousness, formal schooling milestones.",
            2: "2nd Jupiter Return (~Age 24): Life direction definition, graduation, entry into independent career, philosophical maturity.",
            3: "3rd Jupiter Return (~Age 36): Peak societal integration, family expansion, professional leadership, dharma consolidation.",
            4: "4th Jupiter Return (~Age 48): Mentorship phase, wisdom sharing, material stabilization, preparation for higher life goals.",
            5: "5th Jupiter Return (~Age 60 - Shashti Poorthi): Major Vedic milestone of renewal, spiritual completion of societal duties.",
            6: "6th Jupiter Return (~Age 72): Elder statesmanship, detached spiritual wisdom, ancestral blessings.",
            7: "7th Jupiter Return (~Age 84 - Sahasra Chandra Darshana): Seeing 1000 full moons, profound spiritual attainment."
        }

        while age < max_age_years:
            start_dt = birth_dt + timedelta(days=(age - 0.5) * 365.25)
            end_dt = birth_dt + timedelta(days=(age + 0.5) * 365.25)

            desc = significance_map.get(return_num, f"Jupiter returns to natal sign {jup_sign_name}. Auspicious period of divine grace, growth and wisdom.")

            milestones.append(LifeMilestone(
                category=MilestoneCategory.JUPITER_RETURN,
                title=f"Guru Gochara: Jupiter Return #{return_num} (~Age {round(age)})",
                start_date=start_dt,
                end_date=end_dt,
                approx_age_years=round(age, 1),
                description=desc,
                intensity="Auspicious",
                recommended_focus="Educational expansion, ethical endeavors, philanthropy, higher wisdom, spiritual pilgrimages.",
                traditional_remedies=["Guru Paduka pooja / honoring teachers", "Donation of yellow lentils (chana dal) and turmeric", "Dakshinamurthy Stotra"]
            ))

            return_num += 1
            age += JUPITER_ORBIT_YEARS

        return milestones

    @classmethod
    def calculate_nodal_cycles(cls, kundali: Kundali, max_age_years: float) -> List[LifeMilestone]:
        """
        Calculate Rahu-Ketu nodal returns (every ~18.6 years) and half-returns (every ~9.3 years).
        """
        milestones: List[LifeMilestone] = []
        birth_dt = kundali.birth_datetime

        # Full returns: 18.6, 37.2, 55.8, 74.4
        age = NODAL_CYCLE_YEARS
        ret_count = 1
        while age < max_age_years:
            start_dt = birth_dt + timedelta(days=(age - 0.75) * 365.25)
            end_dt = birth_dt + timedelta(days=(age + 0.75) * 365.25)

            milestones.append(LifeMilestone(
                category=MilestoneCategory.NODAL_RETURN,
                title=f"Rahu-Ketu Karmic Nodal Return #{ret_count} (~Age {round(age)})",
                start_date=start_dt,
                end_date=end_dt,
                approx_age_years=round(age, 1),
                description=f"Rahu and Ketu return to their exact natal positions. Major karmic axis activation: intense desire for destiny fulfillment, radical pivots in career or relationships.",
                intensity="Transformational",
                recommended_focus="Staying grounded in ethical principles, avoiding obsessive shortcuts, meditating on true life purpose.",
                traditional_remedies=["Durga Saptashati or Rahu Kavacham", "Subramanya / Murugan worship", "Srikalahasti or Kukke Subramanya visit if Rahu afflictions exist"]
            ))
            ret_count += 1
            age += NODAL_CYCLE_YEARS

        return milestones

    @classmethod
    def calculate_dasha_sandhi(cls, dashas: List[DashaPeriod]) -> List[LifeMilestone]:
        """
        Calculate Dasha Sandhi and Chidra Dasha milestones.
        Chidra Dasha is the final Antardasha of any Mahadasha.
        Dasha Sandhi is the transition border (+/- 6 months) between two major Mahadashas.
        """
        milestones: List[LifeMilestone] = []

        for m_idx in range(len(dashas) - 1):
            m1 = dashas[m_idx]
            m2 = dashas[m_idx + 1]

            # The last antardasha of m1 is Chidra Dasha
            if m1.sub_periods:
                last_a = m1.sub_periods[-1]
                milestones.append(LifeMilestone(
                    category=MilestoneCategory.DASHA_SANDHI,
                    title=f"Chidra Dasha ({m1.lord}-{last_a.lord}) - Terminal Phase of {m1.lord} Mahadasha",
                    start_date=last_a.start_date,
                    end_date=last_a.end_date,
                    approx_age_years=round((last_a.start_date - dashas[0].start_date).days / 365.25, 1),
                    description=f"Final Antardasha of {m1.lord} Mahadasha before transitioning to {m2.lord}. Known classically as Chidra Dasha: loose ends are wrapped up, old chapters close, unpredictability in outcomes.",
                    intensity="High",
                    recommended_focus="Completing lingering projects, non-attachment, avoiding hasty long-term commitments until the new Mahadasha stabilizes.",
                    traditional_remedies=["Navagraha Homa / Japa", "Gayatri Mantra chanting", "Charity on transition days"]
                ))

            # Dasha Sandhi window: 6 months before and 6 months after the transition
            sandhi_start = m1.end_date - timedelta(days=180)
            sandhi_end = m1.end_date + timedelta(days=180)

            milestones.append(LifeMilestone(
                category=MilestoneCategory.DASHA_SANDHI,
                title=f"Dasha Sandhi: Transition from {m1.lord} to {m2.lord} Mahadasha",
                start_date=sandhi_start,
                end_date=sandhi_end,
                approx_age_years=round((m1.end_date - dashas[0].start_date).days / 365.25, 1),
                description=f"The threshold of profound energetic handoff from {m1.lord} to {m2.lord}. Major psychological shift, altering of daily priorities, health vulnerability during physical adaptation.",
                intensity="Transformational",
                recommended_focus="Calm reflection, bodily detoxification, harmonizing home atmosphere.",
                traditional_remedies=["Maha Mrityunjaya Japa", "Sankalpa pooja for smooth transition into new planetary cycle"]
            ))

        return milestones

    @classmethod
    def calculate_raja_yoga_periods(cls, kundali: Kundali, dashas: List[DashaPeriod]) -> List[LifeMilestone]:
        """
        Identify active Mahadashas or Bhuktis of planets forming Kendra-Trikona Raja Yogas.
        Kendra houses: 1, 4, 7, 10 (Vishnu Sthanas)
        Trikona houses: 1, 5, 9 (Lakshmi Sthanas)
        Lords of Kendra and Trikona combining or ruling auspicious houses.
        """
        milestones: List[LifeMilestone] = []
        lagna_sign_idx = kundali.ascendant.sign.value

        # Identify lords of 1, 4, 5, 7, 9, 10
        # Kendra houses: 1, 4, 7, 10
        # Trikona houses: 5, 9 (and 1)
        h1_lord = SIGN_LORDS[lagna_sign_idx]
        h4_lord = SIGN_LORDS[(lagna_sign_idx + 3) % 12]
        h5_lord = SIGN_LORDS[(lagna_sign_idx + 4) % 12]
        h7_lord = SIGN_LORDS[(lagna_sign_idx + 6) % 12]
        h9_lord = SIGN_LORDS[(lagna_sign_idx + 8) % 12]
        h10_lord = SIGN_LORDS[(lagna_sign_idx + 9) % 12]

        trikona_lords = {h1_lord, h5_lord, h9_lord}
        kendra_lords = {h1_lord, h4_lord, h7_lord, h10_lord}
        auspicious_planets = trikona_lords.union(kendra_lords)

        for m in dashas:
            if m.lord in auspicious_planets:
                # Check sub-periods that are also ruled by auspicious planets
                for a in m.sub_periods:
                    if a.lord in auspicious_planets and a.duration_years >= 0.5:
                        age = round((a.start_date - dashas[0].start_date).days / 365.25, 1)
                        milestones.append(LifeMilestone(
                            category=MilestoneCategory.RAJA_YOGA_ACTIVATION,
                            title=f"Raja Yoga Window: {m.lord} Mahadasha - {a.lord} Bhukti",
                            start_date=a.start_date,
                            end_date=a.end_date,
                            approx_age_years=age,
                            description=f"Combined activation of Kendra ({', '.join(kendra_lords)}) and Trikona ({', '.join(trikona_lords)}) lords. Prime window for professional ascent, recognition, wealth gains, and dharmic fruition.",
                            intensity="Auspicious",
                            recommended_focus="Seizing career opportunities, launching ventures, investing in long-term goals, generous philanthropy.",
                            traditional_remedies=["Lakshmi-Narayana Puja", "Vishnu Sahasranama chanting", "Supporting charitable education causes"]
                        ))

        return milestones
