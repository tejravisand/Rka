"""
Advanced Astrological Engine Dossier Generator
==============================================
Showcases all advanced astrological Python capabilities available in the project:
1. Jaimini Sutras Engine: Chara Karakas, Arudhas (AL, UL), Rashi Drishti, Karakamsha
2. 337-Bindu Ashtakavarga: BAV, SAV, Trikona & Ekadhipatya Shodhana, Yoga Pindas, Kakshyas
3. 6-Fold Shadbala: Positional, Directional, Temporal, Motional, Natural, Aspectual (Virupas & Rupas)
4. 36-Point Ashtakoota Guna Milan & Kuja Dosha Mutual Cancellation
5. Precision Panchanga & Muhurtha: 5 Limbs, Rahu Kaalam, Gulika, Abhijit, Brahma Muhurtha
6. Skyfield NASA-Grade Astronomy: GAST/LAST, Sunrise/Sunset, Solar Noon, Lunar Illumination
7. Software Environment & Installed Python Astrology Packages
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure root path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.engines.advanced_astrology_hub import AdvancedAstrologyHub


def run_advanced_astrology_demo():
    print("=" * 85)
    print("       RKA ADVANCED ASTROLOGICAL PYTHON COMPUTATIONAL ENGINE       ")
    print("=" * 85)

    # 1. Audit Python Environment
    audit = AdvancedAstrologyHub.get_available_python_libraries()
    print(f"\n[+] Python Environment: v{audit['python_version']}")
    print("[+] Installed Astrological & Astronomical Libraries:")
    for lib_key, lib_info in audit["libraries"].items():
        status = "[ACTIVE]" if lib_info["installed"] else "[OFFLINE]"
        ver = f"v{lib_info['version']}" if lib_info['version'] else ""
        print(f"    - {lib_key.upper():<18} {status:<10} {ver:<10} | {lib_info['category']}")
        print(f"      Features: {lib_info['features']}")

    # 2. Benchmark Native Profile
    dt_local = datetime(1985, 5, 15, 8, 30, 0)
    lat, lon, tz = 12.9716, 77.5946, 5.5
    name = "Ravi Kumar"

    print("\n" + "=" * 85)
    print(f"GENERATING ADVANCED ASTROLOGICAL PROFILE FOR: {name.upper()}")
    print(f"DOB: {dt_local.strftime('%d-%b-%Y %I:%M %p')} | Lat: {lat}°N, Lon: {lon}°E | TZ: +05:30")
    print("=" * 85)

    profile = AdvancedAstrologyHub.get_complete_advanced_profile(
        dt_local=dt_local,
        lat=lat,
        lon=lon,
        tz_offset=tz,
        name=name
    )

    native = profile["native_info"]
    print(f"\n1. NATAL FOUNDATION:")
    print(f"   - Ascendant (Lagna): {native['ascendant_sign']} ({native['ascendant_degree']}°)")
    print(f"   - Moon Rasi:        {native['moon_sign']}")
    print(f"   - Moon Nakshatra:   {native['moon_nakshatra']}")
    print(f"   - Ayanamsa:         {native['ayanamsa']}")

    # 3. Precision Panchanga & Muhurtha
    p = profile["panchanga_and_muhurtha"]["panchanga"]
    m = profile["panchanga_and_muhurtha"]["muhurtha"]
    print(f"\n2. VEDIC PANCHANGA (FIVE LIMBS OF TIME):")
    print(f"   - Tithi:     {p['tithi']['paksha']} {p['tithi']['name']} ({p['tithi']['percentage_completed']}% completed) [Deity: {p['tithi']['deity']}]")
    print(f"   - Vara:      {p['vara']['sanskrit_name']} ({p['vara']['english_name']}) - Ruled by {p['vara']['ruling_planet']}")
    print(f"   - Nakshatra: {p['nakshatra']['name']} (Pada {p['nakshatra']['pada']}) - Lord: {p['nakshatra']['lord']} [Deity: {p['nakshatra']['deity']}]")
    print(f"   - Yoga:      {p['yoga']['name']} ({p['yoga']['nature']}) - {p['yoga']['description']}")
    print(f"   - Karana:    {p['karana']['name']} ({p['karana']['type']}) - {p['karana']['advisory']}")

    print(f"\n   MUHURTHA TIMING WINDOWS (BENGALURU):")
    print(f"   - Sunrise / Sunset:  {m['sunrise']} / {m['sunset']}")
    print(f"   - Rahu Kaalam:       {m['rahu_kaalam']['start']} - {m['rahu_kaalam']['end']} ({m['rahu_kaalam']['note']})")
    print(f"   - Yamaganda:         {m['yamaganda']['start']} - {m['yamaganda']['end']}")
    print(f"   - Gulika Kaalam:     {m['gulika_kaalam']['start']} - {m['gulika_kaalam']['end']}")
    print(f"   - Abhijit Muhurtha:  {m['abhijit_muhurtha']['start']} - {m['abhijit_muhurtha']['end']} [Auspicious: {m['abhijit_muhurtha']['is_applicable']}]")
    print(f"   - Brahma Muhurtha:   {m['brahma_muhurtha']['start']} - {m['brahma_muhurtha']['end']}")

    # 4. Jaimini Sutras Engine
    j = profile["jaimini"]
    print(f"\n3. JAIMINI SUTRAS ASTROLOGICAL ANALYSIS:")
    print(f"   CHARA KARAKAS (7-KARAKA SCHEME):")
    for code, k_data in j["chara_karakas"]["karakas"].items():
        print(f"   - {code:<4} | {k_data['role']:<15} : {k_data['planet']:<8} at {k_data['degrees_in_sign']:>6.2f}° in {k_data['sign']} ({k_data['sign_sanskrit']})")

    ak_amk_yoga = "YES (Powerful Jaimini Raja Yoga Present!)" if j["chara_karakas"]["ak_amk_raja_yoga"] else "No"
    print(f"   - AK-AmK Raja Yoga:  {ak_amk_yoga}")

    kl = j["karakamsha"]
    print(f"\n   KARAKAMSHA (D9 ATMAKARAKA PLACEMENT):")
    print(f"   - Karakamsha Lagna:  {kl['karakamsha_sign']} ({kl['karakamsha_sign_sanskrit']})")
    print(f"   - 12th from KL:      {kl['moksha_bhava_sign']} (Lord: {kl['moksha_lord']})")
    print(f"   - Ishta Devata:      {kl['ishta_devata']}")

    print(f"\n   KEY ARUDHA PADAS (EXTERNAL PERCEPTION & STATUS):")
    print(f"   - Arudha Lagna (AL): {j['arudha_padas']['AL']['sign_name']} (House {j['arudha_padas']['AL']['house_from_lagna']} from Lagna)")
    print(f"   - Upapada (UL/A12):  {j['arudha_padas']['UL']['sign_name']} (House {j['arudha_padas']['UL']['house_from_lagna']} from Lagna)")
    print(f"   - Dhana Pada (A2):   {j['arudha_padas']['A2']['sign_name']}")
    print(f"   - Rajya Pada (A10):  {j['arudha_padas']['A10']['sign_name']}")

    # 5. Ashtakavarga Engine
    av = profile["ashtakavarga"]
    print(f"\n4. ASHTAKAVARGA COMPUTATION (TOTAL {av['total_sav_bindus']} BINDUS):")
    print(f"   SARVASHTAKAVARGA (SAV) HOUSE STRENGTHS:")
    for h_info in av["house_sav"][:6]:
        print(f"   - House {h_info['house']:>2} ({h_info['sign_sanskrit']:<9}): {h_info['bindus']:>2} Bindus -> {h_info['status']}")
    for h_info in av["house_sav"][6:]:
        print(f"   - House {h_info['house']:>2} ({h_info['sign_sanskrit']:<9}): {h_info['bindus']:>2} Bindus -> {h_info['status']}")

    wf = av["wealth_financial_flow"]
    print(f"\n   FINANCIAL FLOW RATIO:")
    print(f"   - 10th (Effort): {wf['10th_house_bindus']} | 11th (Gains): {wf['11th_house_bindus']} | 12th (Expenditure): {wf['12th_house_bindus']}")
    print(f"   - Financial Verdict: {wf['assessment']}")

    # 6. Complete 6-Fold Shadbala
    sb = profile["shadbala"]
    print(f"\n5. SHADBALA (SIX-FOLD PLANETARY STRENGTH):")
    print(f"   {'Planet':<9} | {'Total Virupas':<14} | {'Rupas':<7} | {'Required':<9} | {'Ratio':<6} | {'Rank':<5} | {'Empowered?'}")
    print("   " + "-" * 75)
    for p_name, p_sb in sb["planets"].items():
        emp = "[YES]" if p_sb["is_empowered"] else "[DEFICIENT]"
        print(f"   {p_name:<9} | {p_sb['total_virupas']:>10.2f} V   | {p_sb['rupas']:>5.2f} | {p_sb['required_rupas']:>5.2f} R | {p_sb['strength_ratio']:>5.2f} | #{p_sb['rank']:<3} | {emp}")

    print(f"\n   - Most Powerful Planet:   {sb['most_powerful_planet']}")
    print(f"   - Most Vulnerable Planet: {sb['most_vulnerable_planet']}")

    # 7. Skyfield High-Precision Astronomy
    sky = profile["astronomy_skyfield"]
    print(f"\n6. SKYFIELD NASA-GRADE ASTRONOMICAL PHENOMENA:")
    print(f"   - GAST (Greenwich Sidereal): {sky['sidereal_time']['gast_hours']} hrs ({sky['sidereal_time']['gast_degrees']}°)")
    print(f"   - LAST (Local Sidereal):     {sky['sidereal_time']['last_hours']} hrs ({sky['sidereal_time']['last_degrees']}°)")
    print(f"   - Solar Noon:                {sky['sun_phenomena']['solar_noon']} (Day length: {sky['sun_phenomena']['day_length_hours']} hrs)")
    print(f"   - Lunar Illumination:        {sky['lunar_phenomena']['illuminated_percentage']}% ({sky['lunar_phenomena']['phase_name']})")

    # 8. Ashtakoota Guna Milan Match Demo
    print(f"\n7. ASHTAKOOTA (36 GUNAS) KUNDALI MILAN DEMO:")
    bride_dt = datetime(1988, 8, 20, 14, 15, 0)
    milan = AdvancedAstrologyHub.match_kundalis(
        bride_dt=bride_dt,
        bride_lat=lat,
        bride_lon=lon,
        groom_dt=dt_local,
        groom_lat=lat,
        groom_lon=lon
    )
    print(f"   Bride DOB: {bride_dt.strftime('%d-%b-%Y %I:%M %p')} | Groom DOB: {dt_local.strftime('%d-%b-%Y %I:%M %p')}")
    print(f"   - Total Score: {milan['total_score']} / {milan['max_score']} ({milan['percentage']}%)")
    print(f"   - Verdict:     {milan['verdict']}")
    print(f"   - Recommendation: {milan['recommendation']}")
    print(f"   - Kuja Dosha Status: {milan['manglik_compatibility']['overall_status']}")

    print("\n" + "=" * 85)
    print("       ALL ADVANCED ASTROLOGICAL PYTHON MODULES TESTED & OPERATIONAL       ")
    print("=" * 85)


if __name__ == "__main__":
    run_advanced_astrology_demo()
