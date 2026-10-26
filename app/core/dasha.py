"""
Vimshottari Dasha Engine.
Calculates birth dasha balance, Mahadashas, Antardashas (Bhuktis),
and Pratyantardashas with precise calendar dates.
"""
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
from app.models.astrological import DashaPeriod, PlanetPosition
from app.core.constants import VIMSHOTTARI_ORDER, VIMSHOTTARI_YEARS, TOTAL_VIMSHOTTARI_YEARS, NAKSHATRAS


DAYS_PER_YEAR = 365.2425  # Standard astronomical solar year days


def calculate_birth_dasha_balance(moon_longitude: float) -> Tuple[str, float, float]:
    """
    Calculate the starting Mahadasha lord, balance fraction remaining,
    and remaining balance in solar years at the moment of birth.
    Each Nakshatra spans 13° 20' = 800 minutes of arc.
    """
    nak_span_deg = 360.0 / 27.0  # 13.333333333333334°
    norm_lon = moon_longitude % 360.0

    nak_idx = int(norm_lon / nak_span_deg)
    nak_idx = min(nak_idx, 26)

    # Arc traversed within this nakshatra in degrees
    traversed_deg = norm_lon - (nak_idx * nak_span_deg)
    fraction_traversed = traversed_deg / nak_span_deg
    fraction_remaining = 1.0 - fraction_traversed

    nak_lord = NAKSHATRAS[nak_idx]["lord"]
    total_lord_years = VIMSHOTTARI_YEARS[nak_lord]
    balance_years = fraction_remaining * total_lord_years

    return nak_lord, fraction_remaining, balance_years


def calculate_vimshottari_dashas(
    birth_dt: datetime,
    moon_longitude: float,
    max_lifespan_years: float = 100.0,
    calculate_pratyantardasha: bool = True
) -> List[DashaPeriod]:
    """
    Calculate all Mahadashas and their respective Antardashas (Bhuktis)
    from birth date up to max_lifespan_years.
    """
    first_lord, fraction_remaining, balance_years = calculate_birth_dasha_balance(moon_longitude)

    # Locate the starting planet index in VIMSHOTTARI_ORDER
    lord_names = [lord for lord, _ in VIMSHOTTARI_ORDER]
    start_idx = lord_names.index(first_lord)

    mahadashas: List[DashaPeriod] = []
    current_time = birth_dt
    years_elapsed = 0.0

    # We iterate through the 9 Mahadasha cycles
    for cycle_offset in range(len(VIMSHOTTARI_ORDER) + 1):
        if years_elapsed >= max_lifespan_years:
            break

        idx = (start_idx + cycle_offset) % len(VIMSHOTTARI_ORDER)
        m_lord, full_m_duration = VIMSHOTTARI_ORDER[idx]

        # For the first dasha, duration is the remaining balance
        if cycle_offset == 0:
            m_duration = balance_years
        else:
            m_duration = full_m_duration

        m_end_time = current_time + timedelta(days=m_duration * DAYS_PER_YEAR)

        # Build Antardashas (Bhuktis)
        antardashas: List[DashaPeriod] = []
        m_lord_idx = lord_names.index(m_lord)
        a_current_time = current_time

        # For cycle 0, we must find which Antardasha the birth happened in
        if cycle_offset == 0:
            # Full antardashas for this planet
            # Find where within the Mahadasha the birth fell
            traversed_m_years = full_m_duration * (1.0 - fraction_remaining)
            cum_a_years = 0.0

            for a_offset in range(len(VIMSHOTTARI_ORDER)):
                a_idx = (m_lord_idx + a_offset) % len(VIMSHOTTARI_ORDER)
                a_lord, a_base_duration = VIMSHOTTARI_ORDER[a_idx]
                a_duration_full = (full_m_duration * a_base_duration) / TOTAL_VIMSHOTTARI_YEARS

                if cum_a_years + a_duration_full <= traversed_m_years:
                    cum_a_years += a_duration_full
                    continue  # Already finished before birth

                # If birth fell inside this antardasha
                if cum_a_years <= traversed_m_years < cum_a_years + a_duration_full:
                    # Portion remaining after birth
                    remaining_in_a = (cum_a_years + a_duration_full) - traversed_m_years
                    a_end_time = a_current_time + timedelta(days=remaining_in_a * DAYS_PER_YEAR)

                    pratyantars = []
                    if calculate_pratyantardasha:
                        pratyantars = _calculate_pratyantars(m_lord, a_lord, a_current_time, a_end_time, remaining_in_a)

                    antardashas.append(DashaPeriod(
                        level=2,
                        level_name="Antardasha (Bhukti)",
                        lord=a_lord,
                        start_date=a_current_time,
                        end_date=a_end_time,
                        duration_years=round(remaining_in_a, 4),
                        sub_periods=pratyantars
                    ))
                    a_current_time = a_end_time
                    cum_a_years += a_duration_full
                else:
                    # Antardashas following the birth antardasha
                    a_end_time = a_current_time + timedelta(days=a_duration_full * DAYS_PER_YEAR)
                    pratyantars = []
                    if calculate_pratyantardasha:
                        pratyantars = _calculate_pratyantars(m_lord, a_lord, a_current_time, a_end_time, a_duration_full)

                    antardashas.append(DashaPeriod(
                        level=2,
                        level_name="Antardasha (Bhukti)",
                        lord=a_lord,
                        start_date=a_current_time,
                        end_date=a_end_time,
                        duration_years=round(a_duration_full, 4),
                        sub_periods=pratyantars
                    ))
                    a_current_time = a_end_time
                    cum_a_years += a_duration_full
        else:
            # Subsequent full Mahadashas
            for a_offset in range(len(VIMSHOTTARI_ORDER)):
                a_idx = (m_lord_idx + a_offset) % len(VIMSHOTTARI_ORDER)
                a_lord, a_base_duration = VIMSHOTTARI_ORDER[a_idx]
                a_duration = (m_duration * a_base_duration) / TOTAL_VIMSHOTTARI_YEARS
                a_end_time = a_current_time + timedelta(days=a_duration * DAYS_PER_YEAR)

                pratyantars = []
                if calculate_pratyantardasha:
                    pratyantars = _calculate_pratyantars(m_lord, a_lord, a_current_time, a_end_time, a_duration)

                antardashas.append(DashaPeriod(
                    level=2,
                    level_name="Antardasha (Bhukti)",
                    lord=a_lord,
                    start_date=a_current_time,
                    end_date=a_end_time,
                    duration_years=round(a_duration, 4),
                    sub_periods=pratyantars
                ))
                a_current_time = a_end_time

        mahadashas.append(DashaPeriod(
            level=1,
            level_name="Mahadasha",
            lord=m_lord,
            start_date=current_time,
            end_date=m_end_time,
            duration_years=round(m_duration, 4),
            sub_periods=antardashas
        ))

        years_elapsed += m_duration
        current_time = m_end_time

    return mahadashas


def _calculate_pratyantars(
    m_lord: str,
    a_lord: str,
    a_start: datetime,
    a_end: datetime,
    a_duration_years: float
) -> List[DashaPeriod]:
    """Calculate the 9 Pratyantardashas within a given Antardasha."""
    lord_names = [lord for lord, _ in VIMSHOTTARI_ORDER]
    a_lord_idx = lord_names.index(a_lord)

    pratyantars: List[DashaPeriod] = []
    p_current_time = a_start

    for p_offset in range(len(VIMSHOTTARI_ORDER)):
        p_idx = (a_lord_idx + p_offset) % len(VIMSHOTTARI_ORDER)
        p_lord, p_base_duration = VIMSHOTTARI_ORDER[p_idx]

        # Proportion of antardasha
        p_duration_years = a_duration_years * (p_base_duration / TOTAL_VIMSHOTTARI_YEARS)
        p_end_time = p_current_time + timedelta(days=p_duration_years * DAYS_PER_YEAR)

        pratyantars.append(DashaPeriod(
            level=3,
            level_name="Pratyantardasha",
            lord=p_lord,
            start_date=p_current_time,
            end_date=p_end_time,
            duration_years=round(p_duration_years, 4),
            sub_periods=[]
        ))
        p_current_time = p_end_time

    return pratyantars


def get_active_dasha(dashas: List[DashaPeriod], target_date: datetime) -> Optional[Dict[str, str]]:
    """
    Identify the active Mahadasha, Antardasha (Bhukti), and Pratyantardasha
    for any target calendar date.
    """
    for m in dashas:
        if m.start_date <= target_date < m.end_date:
            active_info = {
                "mahadasha": m.lord,
                "mahadasha_start": m.start_date.strftime("%Y-%m-%d"),
                "mahadasha_end": m.end_date.strftime("%Y-%m-%d"),
                "antardasha": "",
                "antardasha_start": "",
                "antardasha_end": "",
                "pratyantardasha": "",
                "pratyantardasha_start": "",
                "pratyantardasha_end": "",
            }
            for a in m.sub_periods:
                if a.start_date <= target_date < a.end_date:
                    active_info["antardasha"] = a.lord
                    active_info["antardasha_start"] = a.start_date.strftime("%Y-%m-%d")
                    active_info["antardasha_end"] = a.end_date.strftime("%Y-%m-%d")

                    for p in a.sub_periods:
                        if p.start_date <= target_date < p.end_date:
                            active_info["pratyantardasha"] = p.lord
                            active_info["pratyantardasha_start"] = p.start_date.strftime("%Y-%m-%d")
                            active_info["pratyantardasha_end"] = p.end_date.strftime("%Y-%m-%d")
                            break
                    break
            return active_info
    return None
