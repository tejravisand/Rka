"""
Main entry point for Kundali, Shodashavargas, Vimshottari Dasha-Bhuktis,
and Life Milestones calculation engine.
"""
import os
import sys
from pathlib import Path

# Ensure project root is in sys.path when running app/main.py directly
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from datetime import datetime, timezone, timedelta
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha
from app.core.milestones import LifeMilestoneEngine
from app.engines.lifestyle_advisor import LifestyleAdvisor
from app.visualizer.south_indian import render_south_indian_svg
from app.visualizer.north_indian import render_north_indian_svg
from app.core.constants import ZODIAC_SANSKRIT, SHODASHAVARGA_INFO


def generate_full_astrological_profile(
    birth_dt_local: datetime,
    tz_offset_hours: float,
    latitude: float,
    longitude: float,
    location_name: str = "Bengaluru, Karnataka",
    output_dir: str = "output"
):
    """
    Generate complete astrological calculations and export SVG charts.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Convert local time to UTC
    dt_utc = birth_dt_local - timedelta(hours=tz_offset_hours)

    print("=" * 80)
    print(f"VEDIC ASTROLOGICAL REPORT: KUNDALI, SHODASHAVARGAS, DASHAS & MILESTONES")
    print(f"Location: {location_name} (Lat: {latitude}°, Lon: {longitude}°)")
    print(f"Local Birth Time: {birth_dt_local.strftime('%Y-%m-%d %H:%M:%S')} (UTC: {dt_utc.strftime('%Y-%m-%d %H:%M:%S')})")
    print("=" * 80)

    # 1. Kundali & Bhavas Calculation
    kundali = calculate_kundali(dt_utc, latitude, longitude, tz_offset_hours)

    print(f"\nAyanamsa: {kundali.ayanamsa_name} = {kundali.ayanamsa_value:.4f}°")
    print(f"Ascendant (Lagna): {kundali.ascendant.sign.sanskrit_name} ({kundali.ascendant.degrees_in_sign:.2f}°)")
    print(f"Nakshatra: {kundali.ascendant.nakshatra_name} (Pada {kundali.ascendant.nakshatra_pada}) - Lord: {kundali.ascendant.nakshatra_lord}")

    print("\n--- PLANETARY POSITIONS (D1 RASI) ---")
    print(f"{'Planet':<10} | {'Longitude':<10} | {'Sign (Rasi)':<15} | {'Deg In Sign':<12} | {'Nakshatra':<16} | {'Pada':<4} | {'Dignity':<12} | {'Motion'}")
    print("-" * 95)
    for p_name, p in kundali.planets.items():
        motion = "Retrograde (R)" if p.is_retrograde else "Direct"
        print(f"{p_name:<10} | {p.longitude:<10.2f} | {p.sign.sanskrit_name:<15} | {p.degrees_in_sign:<12.2f} | {p.nakshatra_name:<16} | {p.nakshatra_pada:<4} | {p.dignity:<12} | {motion}")

    # 2. Bhavas (12 Houses)
    print("\n--- 12 BHAVAS (HOUSES) SUMMARY ---")
    for h in kundali.houses:
        planets_str = ", ".join([p.value for p in h.planets]) if h.planets else "Empty"
        print(f"House {h.number:>2}: {h.sign.sanskrit_name:<12} ({h.start_degree:>6.1f}° to {h.end_degree:>6.1f}°) | Planets: {planets_str}")

    # 3. Shodashavargas (16 Divisional Charts)
    print("\n" + "=" * 80)
    print("SHODASHAVARGA (16 DIVISIONAL CHARTS) DETAILS")
    print("=" * 80)

    vargas = calculate_all_vargas(kundali.ascendant, kundali.planets)
    kundali.vargas = vargas

    for div, v_chart in vargas.items():
        print(f"\n[{v_chart.sanskrit_name}] (Weight: {v_chart.vimsopaka_points} pts)")
        print(f"Purpose: {v_chart.purpose}")
        # Show key placements
        pl_items = []
        for ent_name, plc in v_chart.placements.items():
            pl_items.append(f"{ent_name[:3]}:{plc.sign.sanskrit_name[:4]}({plc.dignity[:3]})")
        print("  Placements: " + ", ".join(pl_items[:5]))
        print("              " + ", ".join(pl_items[5:]))

    # 4. Vimshottari Dasha-Bhuktis
    print("\n" + "=" * 80)
    print("VIMSHOTTARI DASHA & BHUKTI TIMELINE (120-YEAR CYCLE)")
    print("=" * 80)

    moon_lon = kundali.planets["Moon"].longitude
    dashas = calculate_vimshottari_dashas(birth_dt_local, moon_lon, max_lifespan_years=100.0)

    for m in dashas:
        print(f"\n▶ {m.lord} MAHADASHA ({m.duration_years:.2f} yrs) : {m.start_date.strftime('%Y-%m-%d')} to {m.end_date.strftime('%Y-%m-%d')}")
        print("  Antardashas (Bhuktis):")
        for a in m.sub_periods:
            p_sample = f" [Starts with {a.sub_periods[0].lord} Pratyantar]" if a.sub_periods else ""
            print(f"    - {m.lord}-{a.lord:<8} : {a.start_date.strftime('%Y-%m-%d')} to {a.end_date.strftime('%Y-%m-%d')} ({a.duration_years:.2f} yrs){p_sample}")

    # Active dasha today
    now = datetime.now()
    active_now = get_active_dasha(dashas, now)
    if active_now:
        print(f"\n★ CURRENTLY ACTIVE DASHA (Date: {now.strftime('%Y-%m-%d')}):")
        print(f"  Mahadasha     : {active_now['mahadasha']} ({active_now['mahadasha_start']} to {active_now['mahadasha_end']})")
        print(f"  Antardasha    : {active_now['antardasha']} ({active_now['antardasha_start']} to {active_now['antardasha_end']})")
        print(f"  Pratyantardasha: {active_now['pratyantardasha']} ({active_now['pratyantardasha_start']} to {active_now['pratyantardasha_end']})")

    # 5. Astrological Life Milestones
    print("\n" + "=" * 80)
    print("IMPORTANT LIFE MILESTONES (TRANSITS, TRANSITIONS & GOLDEN PERIODS)")
    print("=" * 80)

    milestones = LifeMilestoneEngine.calculate_all_milestones(kundali, dashas, max_age_years=85.0)

    for idx, m in enumerate(milestones, 1):
        print(f"\n{idx}. [{m.category.value}] ~Age {m.approx_age_years:.1f}")
        print(f"   Title    : {m.title} ({m.intensity} Impact)")
        print(f"   Window   : {m.start_date.strftime('%Y-%m-%d')} to {m.end_date.strftime('%Y-%m-%d')}")
        print(f"   Nature   : {m.description}")
        print(f"   Guidance : {m.recommended_focus}")
        if m.traditional_remedies:
            print(f"   Remedies : {', '.join(m.traditional_remedies)}")

    # 6. Lifestyle & Material Advisory (Vehicle Colors, Property Directions, Weekly Dress Colors)
    print("\n" + "=" * 80)
    print("PERSONALIZED LIFESTYLE & MATERIAL ADVISORY")
    print("=" * 80)

    dossier = LifestyleAdvisor.get_full_lifestyle_dossier(kundali)

    print(f"\n[A] VEHICLE COLOR RECOMMENDATION (4th House: {dossier.vehicle_advice.fourth_house_sign} - Lord: {dossier.vehicle_advice.fourth_house_lord}):")
    print(f"  ★ Primary Auspicious Colors : {', '.join(dossier.vehicle_advice.primary_lucky_colors)}")
    print(f"  ★ Secondary Favorable Colors: {', '.join(dossier.vehicle_advice.secondary_favorable_colors)}")
    print(f"  ⚠ Colors to Strictly Avoid  : {', '.join(dossier.vehicle_advice.colors_to_avoid)}")
    print(f"  ℹ D16 Shodashamsa Alignment : {dossier.vehicle_advice.d16_shodashamsa_guidance}")
    print(f"  💡 Practical Guidance       : {dossier.vehicle_advice.practical_advice}")

    print(f"\n[B] REAL ESTATE & PROPERTY DIRECTIONS (VASTU & CHARKHA DISHA):")
    res = dossier.residential_property_advice
    print(f"  1. Residential Land / House ({res.ruling_houses}):")
    print(f"     - Premier Directions     : {', '.join(res.primary_best_directions)}")
    print(f"     - Recommended Entrance   : {res.main_entrance_facing}")
    print(f"     - Directions to Avoid    : {', '.join(res.directions_to_avoid)}")
    print(f"     - Key Vastu Rule         : {res.vastu_key_principles[0]}")

    comm = dossier.commercial_office_advice
    print(f"  2. Commercial Office / Business Space ({comm.ruling_houses}):")
    print(f"     - Premier Directions     : {', '.join(comm.primary_best_directions)}")
    print(f"     - Recommended Entrance   : {comm.main_entrance_facing}")
    print(f"     - Directions to Avoid    : {', '.join(comm.directions_to_avoid)}")
    print(f"     - Key Vastu Rule         : {comm.vastu_key_principles[0]}")

    print(f"\n[C] WEEKLY WARDROBE COLOR GUIDE (VAARA VASTRA):")
    for day_k, g in dossier.weekly_dress_guide.items():
        print(f"  • {day_k:<9} ({g.ruling_planet:<7}) -> Best: {', '.join(g.primary_favorable_colors[:3])} | Avoid: {', '.join(g.colors_to_avoid_today[:2])}")
        print(f"    Fabrics: {g.recommended_fabrics} | Tip: {g.personalized_boost_tip}")

    print(f"\n[D] ETERNAL POWER & CAUTION COLORS:")
    print(f"  ★ Eternal Power Colors (Lagna & 9th Lords) : {', '.join(dossier.eternal_power_colors)}")
    print(f"  ⚠ Eternal Caution Colors (8th Dusthana Lord): {', '.join(dossier.eternal_caution_colors)}")

    # 7. Generate and Save SVG Visualizations
    d1_south_svg = render_south_indian_svg(kundali, varga_div=1, title="D1 Rasi Chart - South Indian")
    d1_north_svg = render_north_indian_svg(kundali, varga_div=1, title="D1 Rasi Chart - North Indian Diamond")
    d9_south_svg = render_south_indian_svg(kundali, varga_div=9, title="D9 Navamsa Chart - South Indian")
    d9_north_svg = render_north_indian_svg(kundali, varga_div=9, title="D9 Navamsa Chart - North Indian Diamond")

    with open(os.path.join(output_dir, "rasi_south.svg"), "w", encoding="utf-8") as f:
        f.write(d1_south_svg)
    with open(os.path.join(output_dir, "rasi_north.svg"), "w", encoding="utf-8") as f:
        f.write(d1_north_svg)
    with open(os.path.join(output_dir, "navamsa_south.svg"), "w", encoding="utf-8") as f:
        f.write(d9_south_svg)
    with open(os.path.join(output_dir, "navamsa_north.svg"), "w", encoding="utf-8") as f:
        f.write(d9_north_svg)

    print("\n" + "=" * 80)
    print(f"Generated 4 High-Resolution SVG Charts in '{output_dir}/':")
    print(f"  1. {output_dir}/rasi_south.svg      (D1 Rasi - South Indian)")
    print(f"  2. {output_dir}/rasi_north.svg      (D1 Rasi - North Indian Diamond)")
    print(f"  3. {output_dir}/navamsa_south.svg   (D9 Navamsa - South Indian)")
    print(f"  4. {output_dir}/navamsa_north.svg   (D9 Navamsa - North Indian Diamond)")
    print("=" * 80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Vedic Astrology Calculation & Lifestyle Advisory Engine")
    parser.add_argument("--date", type=str, default="1995-08-15", help="Birth date in YYYY-MM-DD format (default: 1995-08-15)")
    parser.add_argument("--time", type=str, default="10:30:00", help="Birth time in HH:MM:SS format (default: 10:30:00)")
    parser.add_argument("--lat", type=float, default=12.9716, help="Birth latitude in degrees (default: 12.9716 for Bengaluru)")
    parser.add_argument("--lon", type=float, default=77.5946, help="Birth longitude in degrees (default: 77.5946 for Bengaluru)")
    parser.add_argument("--tz", type=float, default=5.5, help="Timezone offset hours from UTC (default: 5.5 for IST)")
    parser.add_argument("--location", type=str, default="Bengaluru, Karnataka, India", help="Location name (default: Bengaluru, Karnataka, India)")
    parser.add_argument("--output", type=str, default="output", help="Output directory for SVG charts (default: output)")

    args = parser.parse_args()

    # Parse date and time
    dt_str = f"{args.date} {args.time}"
    birth_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

    generate_full_astrological_profile(
        birth_dt_local=birth_dt,
        tz_offset_hours=args.tz,
        latitude=args.lat,
        longitude=args.lon,
        location_name=args.location,
        output_dir=args.output
    )
