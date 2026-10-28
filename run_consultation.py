"""
Interactive Astrological Consultation Application.
Every time this software runs, it systematically asks:
1. Full Name
2. Date of Birth (DOB)
3. Time of Birth (TOB)
4. Place of Birth (POB)
5. Marital Status (Married or Unmarried)
6. Purpose of asking questions (Consultation Domain)
7. Presents 3 tailored question choices based on Purpose & Marital Status
8. Predicts the astrological answer using full Shastric calculations & transits
9. Finally generates a publication-grade PDF report!
"""
import os
import sys
import webbrowser
from datetime import datetime, date, time
from typing import Optional, Tuple

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.cities import lookup_city, get_default_coordinates
from app.engines.question_catalog import QuestionCatalogEngine, PURPOSE_CATALOG
from app.engines.multi_method_qa import (
    MasterAstrologyQAEngine,
    ClientProfile,
    QueryContext,
    MultiMethodQAResponse
)
from app.reports.multimethod_qa_pdf import generate_multimethod_qa_pdf
from qa_consultation_app import generate_html_consultation_dossier


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print("=" * 85)
    print("      卐 VEDIC & SCIENTIFIC MULTI-METHOD ASTROLOGICAL CONSULTATION 卐")
    print("   Parashara Hora • KP Sub-Lords • Dr. B. V. Raman • Lal Kitab • Numerology")
    print("=" * 85)
    print(" Welcome! Please answer the basic consultation questions to generate your report.\n")


def prompt_name() -> str:
    while True:
        val = input(" 1. Enter Full Name [e.g. Rahul Sharma]: ").strip()
        if val:
            return val
        print("    [!] Name cannot be empty. Please enter your name.")


def parse_flexible_date(val: str) -> Optional[date]:
    val = val.strip().replace("/", "-").replace(".", "-")
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%d-%b-%Y", "%d-%B-%Y", "%m-%d-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(val, fmt).date()
        except ValueError:
            continue
    return None


def prompt_dob() -> str:
    while True:
        val = input(" 2. Enter Date of Birth (YYYY-MM-DD or DD-MM-YYYY) [e.g. 1992-06-15]: ").strip()
        d = parse_flexible_date(val)
        if d:
            return d.strftime("%Y-%m-%d")
        print("    [!] Invalid date format. Please use YYYY-MM-DD (e.g. 1992-06-15) or DD-MM-YYYY.")


def parse_flexible_time(val: str) -> Optional[time]:
    val = val.strip().upper()
    formats = [
        "%H:%M:%S", "%H:%M",
        "%I:%M:%S %p", "%I:%M %p",
        "%I:%M:%S%p", "%I:%M%p"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(val, fmt).time()
        except ValueError:
            continue
    return None


def prompt_tob() -> str:
    while True:
        val = input(" 3. Enter Time of Birth (HH:MM:SS or HH:MM AM/PM) [e.g. 07:30:00 or 07:30 AM]: ").strip()
        t = parse_flexible_time(val)
        if t:
            return t.strftime("%H:%M:%S")
        print("    [!] Invalid time format. Please use HH:MM:SS (24-hour) or HH:MM AM/PM.")


def prompt_place() -> Tuple[str, float, float, float]:
    while True:
        val = input(" 4. Enter Place of Birth (City / Location) [e.g. Bengaluru, Chennai, Mumbai, Delhi]: ").strip()
        if not val:
            val = "Bengaluru, Karnataka"

        coords = lookup_city(val)
        if coords:
            lat, lon, tz, canonical = coords
            print(f"    ✓ Resolved City: {canonical} (Lat: {lat:.4f}°, Lon: {lon:.4f}°, TZ: UTC+{tz})")
            return canonical, lat, lon, tz
        else:
            print(f"    [i] City '{val}' not in quick database. Using standard coordinates.")
            # Prompt for coordinates or fallback
            sub = input(f"    Use default Bengaluru (IST +5.5) or enter custom Lat, Lon? [1=Default Bengaluru, 2=Custom]: ").strip()
            if sub == "2":
                try:
                    lat = float(input("    Enter Latitude (°N/S) [e.g. 13.08]: ").strip())
                    lon = float(input("    Enter Longitude (°E/W) [e.g. 80.27]: ").strip())
                    tz = float(input("    Enter Timezone Offset hours [default: 5.5]: ").strip() or "5.5")
                    return val, lat, lon, tz
                except ValueError:
                    print("    Invalid input. Falling back to Bengaluru coordinates.")
            lat, lon, tz, canonical = get_default_coordinates(val)
            return val, lat, lon, tz


def prompt_marital_status() -> str:
    while True:
        print("\n 5. What is your Marital Status?")
        print("    [1] Unmarried (Single / Looking for marriage / Relationship)")
        print("    [2] Married (Conjugal Life / Family Harmony / Spousal Prosperity)")
        choice = input("    Select Marital Status [1 or 2, default: 1]: ").strip()
        if not choice or choice in ["1", "unmarried", "u", "single"]:
            return "Unmarried"
        elif choice in ["2", "married", "m"]:
            return "Married"
        print("    [!] Please enter 1 for Unmarried or 2 for Married.")


def prompt_purpose() -> Tuple[str, str]:
    purposes = [
        ("career", "Career, Job & Business Expansion"),
        ("marriage", "Marriage, Relationship & Conjugal Harmony"),
        ("finance", "Finance, Wealth & Investments"),
        ("health", "Health, Vitality & Medical Astrology"),
        ("property", "Property, Real Estate & Vehicles (Vahana)"),
        ("children", "Children & Family Growth (Santan Prapti)"),
        ("education", "Education, Higher Studies & Competitive Exams"),
        ("foreign", "Foreign Travel, Relocation & Visa"),
        ("spiritual", "Spiritual Growth, Life Purpose & Karma")
    ]

    print("\n" + "-" * 85)
    print(" 6. What is the Purpose of asking questions? (Choose Consultation Domain):")
    print("-" * 85)
    for idx, (k, title) in enumerate(purposes, 1):
        print(f"    [{idx}] {title}")
    print("    [10] Other / Specific Life Concern")

    while True:
        ch = input("\n    Select Purpose number [1 to 10, default: 1]: ").strip()
        if not ch or ch == "1":
            return "career", purposes[0][1]
        if ch.isdigit():
            num = int(ch)
            if 1 <= num <= 9:
                return purposes[num - 1][0], purposes[num - 1][1]
            elif num == 10:
                custom = input("    Enter your specific purpose: ").strip()
                resolved = QuestionCatalogEngine.resolve_purpose_key(custom)
                return resolved, custom if custom else "Specific Life Consultation"
        # Match by text
        resolved = QuestionCatalogEngine.resolve_purpose_key(ch)
        return resolved, QuestionCatalogEngine.get_purpose_title(resolved)


def prompt_question_choice(purpose_key: str, marital_status: str) -> str:
    choices = QuestionCatalogEngine.get_three_question_choices(purpose_key, marital_status)

    print("\n" + "=" * 85)
    print(f" 7. 3 TAILORED QUESTION CHOICES FOR: {QuestionCatalogEngine.get_purpose_title(purpose_key).upper()}")
    print(f"    (Customized for: {marital_status.upper()} Profile)")
    print("=" * 85)
    for i, q in enumerate(choices, 1):
        print(f"    [{i}] \"{q}\"")
    print(f"    [4] Enter my own custom question")

    while True:
        sel = input(f"\n    Select your question choice [1, 2, 3, or 4]: ").strip()
        if sel in ["1", ""]:
            return choices[0]
        elif sel == "2":
            return choices[1]
        elif sel == "3":
            return choices[2]
        elif sel == "4":
            custom_q = input("    Type your custom question: ").strip()
            if custom_q:
                return custom_q
            return choices[0]
        print("    [!] Please select 1, 2, 3, or 4.")


def run_interactive_consultation():
    clear_screen()
    print_banner()

    # Step 1: Basic Information
    name = prompt_name()
    dob = prompt_dob()
    tob = prompt_tob()
    place, lat, lon, tz = prompt_place()
    marital_status = prompt_marital_status()

    # Step 2: Purpose
    purpose_key, purpose_title = prompt_purpose()
    category = QuestionCatalogEngine.get_category_name(purpose_key)

    # Step 3: Question Choices (3 Choices tailored to Purpose + Marital Status)
    chosen_question = prompt_question_choice(purpose_key, marital_status)

    print("\n" + "=" * 85)
    print(f" 🔮 CALCULATING ASTROLOGICAL PREDICTION FOR:")
    print(f"    Native          : {name}")
    print(f"    Birth           : {dob} at {tob} ({place})")
    print(f"    Marital Status  : {marital_status}")
    print(f"    Purpose Domain  : {purpose_title}")
    print(f"    Selected Question: \"{chosen_question}\"")
    print("=" * 85)
    print(" [⏳] Synchronizing Ephemeris, Bhavas, Dashas & Real-Time Transits...\n")

    # Step 4: Run Astrological Calculations
    b_dt_str = f"{dob} {tob}"
    birth_dt = datetime.strptime(b_dt_str, "%Y-%m-%d %H:%M:%S")
    query_dt = datetime.now()

    client = ClientProfile(
        name=name,
        birth_datetime_local=birth_dt,
        tz_offset_hours=tz,
        latitude=lat,
        longitude=lon,
        place_name=place,
        marital_status=marital_status
    )

    query = QueryContext(
        question_text=chosen_question,
        question_category=category,
        query_datetime_local=query_dt,
        query_latitude=lat,
        query_longitude=lon,
        query_place_name=place
    )

    response: MultiMethodQAResponse = MasterAstrologyQAEngine.evaluate_consultation(client, query)

    # Step 5: Output Prediction Results to Terminal
    k = response.natal_kundali
    t_pred = response.targeted_prediction

    print("\n" + "★" * 85)
    print(f"               ASTROLOGICAL PREDICTION & TIMELINE REPORT")
    print("★" * 85)
    print(f"  CLIENT NAME       : {client.name}")
    print(f"  MARITAL STATUS    : {client.marital_status}")
    print(f"  LAGNA & MOON RASI : {k.ascendant.sign.sanskrit_name} Lagna | {k.planets['Moon'].sign.sanskrit_name} Rasi ({k.planets['Moon'].nakshatra_name})")
    print(f"  ACTIVE DASHA      : {response.current_active_dasha['mahadasha']} Mahadasha - {response.current_active_dasha['antardasha']} Antardasha")
    print("-" * 85)
    print(f"  CONSULTATION QUESTION: \"{chosen_question}\"")
    print(f"  PURPOSE / DOMAIN     : {purpose_title.upper()}")
    print("-" * 85)
    print(f"  ★ UNIFIED VERDICT    : {response.unified_verdict}")
    print(f"  ★ CONFIDENCE SCORE   : {response.consensus_probability_percent}%")
    if t_pred:
        print(f"  ★ PRIMARY TIMELINE   : {t_pred.primary_timeline_window}")
    print("=" * 85)

    if t_pred:
        print("\n▶ DETAILED ASTROLOGICAL PREDICTION & SYNTHESIS:")
        print(f"  {t_pred.core_prediction_narrative}")
        print(f"\n▶ ASTROLOGICAL MECHANICS & PLANETARY DYNAMICS:")
        print(f"  • {t_pred.astrological_mechanics}")
        print(f"  • {t_pred.specific_house_analysis}")
        print(f"  • Dasha Impact: {t_pred.active_dasha_impact}")
        print(f"  • Gochara Trigger: {t_pred.gochara_transit_trigger}")

        print("\n▶ RECOMMENDED VEDIC REMEDIES & LIFESTYLE UPAYAS:")
        for r_item in t_pred.tailored_remedies:
            print(f"  • {r_item}")

        print("\n▶ AUSPICIOUS ATTRIBUTES:")
        for ak, av in t_pred.auspicious_recommendations.items():
            print(f"  • {ak}: {av}")

    print("=" * 85)

    # Step 6: Generate Publication-Grade PDF Report
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    slug = name.lower().replace(" ", "_").replace(".", "")
    pdf_path = os.path.join(out_dir, f"{slug}_prediction_report.pdf")
    html_path = os.path.join(out_dir, f"{slug}_prediction_report.html")

    print("\n[⏳] Generating Publication-Grade Multi-Page PDF Report...")
    generate_multimethod_qa_pdf(response, pdf_path)
    generate_html_consultation_dossier(response, html_path)

    print("\n" + "✓" * 85)
    print("  [SUCCESS] CONSULTATION DOSSIER & PDF REPORT GENERATED!")
    print(f"  • PDF Report Path : {pdf_path}")
    print(f"  • HTML Dashboard  : {html_path}")
    print("✓" * 85)

    # Step 7: Prompt to open PDF directly
    open_now = input("\nWould you like to open the generated PDF report now? [Y/n, default: Y]: ").strip().lower()
    if open_now in ["", "y", "yes"]:
        try:
            if os.name == 'nt':
                os.startfile(pdf_path)
            else:
                webbrowser.open(f"file://{os.path.abspath(pdf_path)}")
            print("✓ PDF opened in default viewer.")
        except Exception as e:
            print(f"Notice: Could not automatically open PDF ({e}). File is at: {pdf_path}")

    # Prompt to run another consultation
    again = input("\nWould you like to run another consultation for another person or question? [y/N]: ").strip().lower()
    if again in ["y", "yes"]:
        run_interactive_consultation()
    else:
        print("\nThank you for using the Vedic Astrology Consultation System. Hari Om Tat Sat!\n")


if __name__ == "__main__":
    run_interactive_consultation()
