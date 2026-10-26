"""
Interactive Multi-Method Astrological Q&A Consultation Application.
Provides targeted, deep-dive question-and-answer predictions using:
1. Parashara Hora Method
2. Krishnamurti Padhdhati (KP Astrology)
3. Dr. B. V. Raman Method
4. Lal Kitab Method
5. Numerology (Chaldean & Pythagorean)
6. Education Stream, Education Break Risk & Academic Remedies
7. Profession & D10 Dashamsha Career Direction
8. Marriage Breakup / Separation Risk Assessment & Preventive Healing Upayas
9. Favourable & Unfavourable Mobile Numbers (Vibrations, Repeated Digits, Compounds)
10. Favourable & Unfavourable Vehicle Registration Numbers (Vahana Bhava, Safety, Colors)
11. Present Name Diagnostic & General-Purpose Alternate Name Suggestions (Non-legal adoption)
12. Comprehensive Shastric Planetary Aspects (Drishti Matrix - Special Mars 4/8, Jupiter 5/9, Saturn 3/10)
13. Real-Time Present Gochara (Transit) at Query/Enquiry Moment & Immediate Diagnostic
14. All types of remedies: Mantras, Sacred Plant Pradakshinams, Lal Kitab Upayas, Danam & Gemstones.
"""
import os
import sys
import argparse
import http.server
import json
import urllib.parse
from datetime import datetime, date
from typing import Optional

from app.engines.multi_method_qa import (
    MasterAstrologyQAEngine,
    ClientProfile,
    QueryContext,
    MultiMethodQAResponse
)
from app.reports.multimethod_qa_pdf import generate_multimethod_qa_pdf


class ConsultationServerHandler(http.server.SimpleHTTPRequestHandler):
    """Integrated HTTP server handler for interactive web consultations."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ["/", "/index.html", "/consultation"]:
            portal_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OPEN_MULTI_METHOD_CONSULTATION.html")
            if os.path.exists(portal_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(portal_path, "rb") as f:
                    self.wfile.write(f.read())
                return
        elif parsed.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "active", "timestamp": datetime.now().isoformat()}).encode("utf-8"))
            return

        # Fallback to default static file handler
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/consult":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode("utf-8"))
                name = data.get("name", "Client Profile")
                dob = data.get("dob", "1990-01-01")
                tob = data.get("tob", "12:00:00")
                place = data.get("place", "Bengaluru, Karnataka")
                lat = float(data.get("lat", 12.9716))
                lon = float(data.get("lon", 77.5946))
                tz = float(data.get("tz", 5.5))
                question = data.get("question", "What is my immediate life trajectory and career milestone?")
                category = data.get("category", "Career")
                mobile = data.get("mobile", None)
                vehicle = data.get("vehicle", None)

                response = run_consultation_flow(
                    name=name,
                    dob_str=dob,
                    tob_str=tob,
                    place=place,
                    lat=lat,
                    lon=lon,
                    tz_offset=tz,
                    question=question,
                    category=category,
                    query_dt=datetime.now(),
                    output_prefix="web_consultation",
                    mobile_test=mobile,
                    vehicle_test=vehicle
                )

                slug = name.lower().replace(" ", "_").replace(".", "")
                pdf_url = f"/output/{slug}_web_consultation.pdf"
                html_url = f"/output/{slug}_web_consultation.html"

                res_payload = {
                    "status": "success",
                    "client_name": response.client.name,
                    "unified_verdict": response.unified_verdict,
                    "confidence_score": response.consensus_probability_percent,
                    "timeline": response.primary_timeline_forecast,
                    "education_stream": response.education_stream.primary_stream,
                    "education_break_risk": f"{response.education_break.break_probability_percent}% ({response.education_break.risk_level})",
                    "profession_trajectory": response.profession.primary_career_direction,
                    "marriage_longevity_score": f"{response.marriage_breakup.marital_longevity_score}/100 ({response.marriage_breakup.separation_risk_level})",
                    "mobile_compatibility": response.mobile_guidance.evaluation_of_specific_mobile.compatibility_status if response.mobile_guidance.evaluation_of_specific_mobile else "N/A",
                    "vehicle_compatibility": response.vehicle_guidance.evaluation_of_specific_plate.compatibility_status if response.vehicle_guidance.evaluation_of_specific_plate else "N/A",
                    "present_name_compound": response.name_tuning.present_chaldean_compound,
                    "present_name_status": response.name_tuning.present_name_status,
                    "alternate_names": [cal.calibrated_name for cal in response.name_tuning.spelling_calibration_suggestions],
                    "pdf_url": pdf_url,
                    "html_url": html_url
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(res_payload).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def start_consultation_server(port: int = 8080):
    """Runs a dedicated local web server for interactive consultations."""
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, ConsultationServerHandler)
    print("=" * 80)
    print(f"🌟 ASTROLOGICAL CONSULTATION WEB PORTAL RUNNING ON http://localhost:{port}")
    print(f"   • Interactive Web Portal : http://localhost:{port}/")
    print(f"   • Real-Time API Endpoint : http://localhost:{port}/api/consult (POST JSON)")
    print("   Press Ctrl+C to terminate the server.")
    print("=" * 80)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server gracefully stopped.")
        httpd.server_close()


def print_dossier_summary(resp: MultiMethodQAResponse):
    """Prints a clear, rich CLI presentation of the consultation results."""
    c = resp.client
    q = resp.query
    k = resp.natal_kundali

    print("=" * 95)
    print("      MULTI-METHOD VEDIC & SCIENTIFIC ASTROLOGICAL CONSULTATION DOSSIER")
    print("=" * 95)
    print(f"Client Name     : {c.name}")
    print(f"Birth Details   : {c.birth_datetime_local.strftime('%d-%b-%Y %I:%M %p')} | {c.place_name} ({c.latitude}°N, {c.longitude}°E)")
    print(f"Lagna & Rasi    : {k.ascendant.sign.sanskrit_name} Lagna | {k.planets['Moon'].sign.sanskrit_name} Rasi ({k.planets['Moon'].nakshatra_name})")
    print(f"Active Dasha    : {resp.current_active_dasha['mahadasha']} Mahadasha - {resp.current_active_dasha['antardasha']} Antardasha")
    print(f"Query Timestamp : {q.query_datetime_local.strftime('%d-%b-%Y %I:%M %p')} at {q.query_place_name}")
    print("-" * 95)
    print(f"CONSULTATION QUESTION: \"{q.question_text}\"")
    print(f"QUESTION DOMAIN      : {q.question_category.upper()}")
    print("=" * 95)

    print("\n" + "★" * 38 + " UNIFIED CONSENSUS VERDICT " + "★" * 38)
    print(f"VERDICT         : {resp.unified_verdict}")
    print(f"CONFIDENCE SCORE: {resp.consensus_probability_percent}%")
    print("★" * 95)

    # 1. Real-Time Present Gochara at Enquiry Moment
    goc = resp.present_gochara
    print("\n" + "-" * 95)
    print("1. REAL-TIME PRESENT GOCHARA (TRANSIT) AT ENQUIRY MOMENT")
    print("-" * 95)
    print(f"▶ ENQUIRY MOMENT DIAGNOSTIC:")
    print(f"  {goc.why_this_question_now_diagnostic}")
    print(f"\n▶ MAJOR PLANETARY TRANSITS RELATIVE TO JANMA RASI ({goc.natal_moon_sign}) & LAGNA ({goc.natal_lagna_sign}):")
    print(f"  • Saturn (Shani) Gochara  : {goc.saturn_transit_verdict}")
    print(f"  • Jupiter (Guru) Bala     : {goc.jupiter_transit_verdict}")
    print(f"  • Rahu-Ketu Nodal Shifts  : {goc.rahu_ketu_transit_verdict}")
    print(f"\n▶ IMMEDIATE ACTIONABLE TRANSIT TIMELINE:")
    print(f"  {goc.immediate_30_60_90_day_forecast}")

    # 2. Detailed Planetary Aspects (Drishti Matrix)
    asp = resp.detailed_aspects
    print("\n" + "-" * 95)
    print("2. COMPREHENSIVE SHASTRIC PLANETARY ASPECTS (DRISHTI MATRIX)")
    print("-" * 95)
    for kp in asp.key_points_aspects[:5]:
        print(f"  • {kp.target_point:<40} : Aspected by {', '.join(kp.aspecting_planets)}")
        print(f"    Net Energy: {kp.net_influence} — {kp.detailed_interpretation}")
    print(f"\n  ★ Mutual 7th Aspects Active : {asp.mutual_planetary_aspects[0] if asp.mutual_planetary_aspects else 'None'}")

    # 3. Present Name Diagnostic & General-Purpose Alternate Names
    nt = resp.name_tuning
    print("\n" + "-" * 95)
    print("3. PRESENT NAME DIAGNOSTIC & GENERAL-PURPOSE ALTERNATE NAME SUGGESTIONS")
    print("   (For Social, Display, Business Card, & Signature use — No Government Gazette changes required)")
    print("-" * 95)
    print(f"▶ PRESENT NAME EVALUATION:")
    print(f"  • Present Name            : \"{nt.present_name}\"")
    print(f"  • Chaldean Compound       : {nt.present_chaldean_compound} -> Single {nt.present_chaldean_single}")
    print(f"  • Compound Meaning        : {nt.present_compound_meaning}")
    print(f"  • Astrological Diagnostic : {nt.present_name_status}")

    print(f"\n▶ STRATEGY 1: MINOR SPELLING CALIBRATIONS (DISPLAY / SOCIAL USE):")
    for cal in nt.spelling_calibration_suggestions:
        print(f"  • \"{cal.calibrated_name}\" (Compound {cal.chaldean_compound} -> {cal.chaldean_single})")
        print(f"    Vibration: {cal.vibration_title} — {cal.vibration_benefit}")

    print(f"\n▶ STRATEGY 2: VEDIC JANMA NAKSHATRA NAMA-AKSHARA SUGGESTIONS (Syllable: \"{nt.vedic_nakshatra_syllable}\"):")
    for vn in nt.vedic_nakshatra_name_options[:4]:
        print(f"  • \"{vn.suggested_name}\" ({vn.meaning}) | Compound: {vn.chaldean_compound} -> {vn.chaldean_single} ({vn.planetary_ruler.split('(')[0]})")

    print(f"\n▶ NON-LEGAL ADOPTION PROTOCOL:")
    print(f"  • {nt.non_legal_adoption_guidelines[0]}")
    print(f"  • {nt.non_legal_adoption_guidelines[1]}")
    print(f"  • {nt.non_legal_adoption_guidelines[2]}")

    # 4. Five Main Methods Breakdown
    print("\n" + "-" * 95)
    print("4. METHOD-BY-METHOD PREDICTIVE BREAKDOWN")
    print("-" * 95)

    print(f"▶ PARASHARA HORA METHOD:")
    print(f"  • Primary Bhavas Evaluated: {', '.join(map(str, resp.parashara_verdict.primary_bhavas))}")
    print(f"  • D10/D9 Divisional Status: {resp.parashara_verdict.varga_confirmations}")
    print(f"  • Parashari Verdict       : {resp.parashara_verdict.parashara_verdict}")

    print(f"\n▶ KRISHNAMURTI PADHDHATI (KP ASTROLOGY METHOD):")
    print(f"  • Primary House Cusp      : {resp.kp_verdict.primary_cusp_number}th Cusp | Sub-Lord: {resp.kp_verdict.sub_lord}")
    print(f"  • Prashna Ruling Planets  : {', '.join(resp.kp_ruling_planets.strong_rulers[:4])}")
    print(f"  • KP Horary Verdict       : {resp.kp_verdict.verdict} (Probability: {resp.kp_verdict.probability_percentage}%)")

    print(f"\n▶ DR. B. V. RAMAN METHOD:")
    print(f"  • Raman Ayanamsa Value    : {resp.raman_ayanamsa_value:.4f}°")
    print(f"  • 300 Important Yogas     : {', '.join([y.name for y in resp.raman_detected_yogas[:4]]) if resp.raman_detected_yogas else 'Standard Kendra Placements'}")
    print(f"  • Raman Prasna Verdict    : {resp.raman_prasna.raman_verdict}")

    print(f"\n▶ LAL KITAB METHOD (RED BOOK):")
    print(f"  • Active Karmic Debts     : {len(resp.lal_kitab.active_karmic_debts)} Active ({', '.join([d.debt_name.split('(')[0].strip() for d in resp.lal_kitab.active_karmic_debts]) or 'None'})")

    print(f"\n▶ NUMEROLOGY METHOD (ANKA VIDYA):")
    print(f"  • Mulank: {resp.numerology.mulank} ({resp.numerology.mulank_ruler}) | Bhagyank: {resp.numerology.bhagyank} ({resp.numerology.bhagyank_ruler})")
    print(f"  • Current Personal Year   : {resp.numerology.personal_year_theme}")
    print(f"  • Query Timing Verdict    : {resp.numerology.query_timing_verdict}")

    # 5. Education, Profession & Marriage Horizon
    ed = resp.education_stream
    br = resp.education_break
    pf = resp.profession
    mb = resp.marriage_breakup
    print("\n" + "-" * 95)
    print("5. EDUCATION STREAM, EDUCATION BREAK RISK, PROFESSION & MARRIAGE HARMONY")
    print("-" * 95)
    print(f"▶ EDUCATION STREAM        : {ed.primary_stream} (Degrees: {', '.join(ed.recommended_degrees[:2])})")
    print(f"▶ EDUCATION BREAK RISK    : {br.break_risk_level} | Windows: {', '.join(br.vulnerable_age_windows)}")
    print(f"▶ PROFESSION TRAJECTORY   : {pf.career_path_verdict} (AmK: {pf.amatyakaraka_planet})")
    print(f"▶ MARITAL LONGEVITY SCORE : {mb.marital_longevity_score} / 100 (Risk: {mb.breakup_risk_level})")
    print(f"  Kuja/Manglik Status     : {mb.manglik_dosha_status}")

    # 6. Mobile & Vehicle Numbers Guidance
    mob = resp.mobile_guidance
    veh = resp.vehicle_guidance
    print("\n" + "-" * 95)
    print("6. MOBILE NUMBERS & VEHICLE REGISTRATION NUMBERS GUIDANCE")
    print("-" * 95)
    print(f"▶ MOBILE NUMBERS          : Favourable sums: {', '.join(map(str, mob.favourable_single_totals))} | AVOID: {', '.join(map(str, mob.unfavourable_single_totals))}")
    if mob.evaluated_custom_number:
        em = mob.evaluated_custom_number
        print(f"  ★ Tested Custom Mobile  : {em.mobile_number} (Sum {em.total_digits_sum}->{em.reduced_single_digit}) : {em.compatibility_verdict}")

    print(f"▶ VEHICLE REGISTRATION    : 4th Lord {veh.fourth_house_lord} | Favourable sums: {', '.join(map(str, veh.favourable_plate_single_sums))} | AVOID: {', '.join(map(str, veh.unfavourable_plate_single_sums))}")
    print(f"  Lucky Vehicle Colors    : {', '.join(veh.lucky_vehicle_colors)} | Avoid: {', '.join(veh.caution_vehicle_colors)}")
    if veh.evaluated_custom_plate:
        ev = veh.evaluated_custom_plate
        print(f"  ★ Tested Vehicle Plate  : {ev.plate_number} (Sum {ev.four_digit_sum}->{ev.four_digit_reduced}) : {ev.safety_and_fortune_verdict}")

    # 7. Comprehensive Remedies
    print("\n" + "=" * 95)
    print("7. COMPREHENSIVE MULTI-TRADITION REMEDIAL DOSSIER")
    print("=" * 95)
    for pl in resp.remedies.sacred_plant_pradakshinams:
        print(f"  • Sacred Tree Pradakshinam: {pl.plant_name} — {pl.prescribed_pradakshinam_rounds} Rounds on {pl.auspicious_day.split('(')[0]} ({pl.auspicious_timing})")
        print(f"    Sankalpa Shloka: \"{pl.sacred_sankalpa_shloka}\"")
    for m in resp.remedies.primary_mantras:
        print(f"  • Mantra: {m.planet_or_deity} — Bija: \"{m.bija_mantra}\" ({m.prescribed_japa_count:,} recitations with {m.japa_mala})")
    print(f"  • Marriage Harmony: {resp.marriage_breakup.preventive_remedies_for_harmony[0]}")
    for u in resp.remedies.lal_kitab_upayas[:3]:
        print(f"  • Lal Kitab Totke: {u}")
    print("=" * 95)


def generate_html_consultation_dossier(
    resp: MultiMethodQAResponse,
    output_html_path: str
) -> str:
    """Generates an interactive, beautiful HTML consultation dashboard."""
    os.makedirs(os.path.dirname(os.path.abspath(output_html_path)), exist_ok=True)
    c = resp.client
    q = resp.query
    k = resp.natal_kundali

    # Build plant rows
    plant_html = ""
    for pl in resp.remedies.sacred_plant_pradakshinams:
        plant_html += f"""
        <div style="background:#f0fff4; border-left:4px solid #38a169; padding:12px; margin-bottom:12px; border-radius:6px;">
            <h4 style="margin:0 0 6px 0; color:#22543d;">🌿 {pl.plant_name} <i>({pl.botanical_name})</i></h4>
            <p style="margin:2px 0;"><b>Prescribed Pradakshinams:</b> <span style="color:#2f855a; font-weight:bold;">{pl.prescribed_pradakshinam_rounds} Rounds (Clockwise)</span></p>
            <p style="margin:2px 0;"><b>Auspicious Day & Time:</b> {pl.auspicious_day} ({pl.auspicious_timing})</p>
            <p style="margin:2px 0;"><b>Offerings:</b> {pl.ritual_offerings[0]}</p>
            <p style="margin:2px 0; font-style:italic; color:#2d3748;"><b>Sankalpa Shloka:</b> "{pl.sacred_sankalpa_shloka}"</p>
            <p style="margin:2px 0; font-size:12px; color:#c53030;"><b>Precaution:</b> {pl.special_precautions}</p>
        </div>
        """

    # Build mantra rows
    mantra_html = ""
    for m in resp.remedies.primary_mantras:
        mantra_html += f"""
        <div style="background:#ebf8ff; border-left:4px solid #3182ce; padding:12px; margin-bottom:12px; border-radius:6px;">
            <h4 style="margin:0 0 6px 0; color:#2b6cb0;">🕉️ {m.planet_or_deity}</h4>
            <p style="margin:2px 0;"><b>Bija Mantra:</b> <code style="background:#bee3f8; padding:2px 6px; border-radius:4px;">{m.bija_mantra}</code></p>
            <p style="margin:2px 0;"><b>Vedic Mantra:</b> <i>"{m.vedic_mantra}"</i></p>
            <p style="margin:2px 0;"><b>Prescription:</b> {m.prescribed_japa_count:,} recitations with {m.japa_mala} facing {m.facing_direction} ({m.optimal_time})</p>
        </div>
        """

    # Spelling calibrations html
    cal_html = ""
    for cal in resp.name_tuning.spelling_calibration_suggestions:
        cal_html += f"""
        <div style="background:#fffaf0; border:1px solid #fbd38d; padding:10px 14px; border-radius:6px; margin-bottom:8px;">
            <b>"{cal.calibrated_name}"</b> — <span style="color:#b7791f; font-weight:bold;">Compound {cal.chaldean_compound} &rarr; {cal.chaldean_single}</span><br/>
            <span style="font-size:13px; color:#4a5568;">{cal.vibration_title}: {cal.vibration_benefit}</span>
        </div>
        """

    # Aspects summary html
    asp_html = ""
    for kp in resp.detailed_aspects.key_points_aspects[:5]:
        asp_html += f"""
        <tr>
            <th>{kp.target_point}</th>
            <td>{', '.join(kp.aspecting_planets)}</td>
            <td><b>{kp.net_influence}</b>: {kp.detailed_interpretation}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Method Astrological Consultation - {c.name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #f0f4f8;
            color: #2d3748;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            border-radius: 12px;
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
            color: #ffffff;
            padding: 28px 32px;
            text-align: center;
        }}
        .header h1 {{ margin: 0 0 8px 0; font-size: 24px; }}
        .header p {{ margin: 0; opacity: 0.9; font-size: 14px; }}
        .content {{ padding: 28px 32px; }}
        .verdict-box {{
            background: #fffaf0;
            border: 2px solid #dd6b20;
            border-radius: 8px;
            padding: 18px 24px;
            margin: 20px 0;
            text-align: center;
        }}
        .method-card {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 16px;
        }}
        .method-card h3 {{
            margin-top: 0;
            color: #2b6cb0;
            border-bottom: 2px solid #edf2f7;
            padding-bottom: 6px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0;
        }}
        th, td {{
            padding: 10px 12px;
            border: 1px solid #e2e8f0;
            text-align: left;
            font-size: 13.5px;
        }}
        th {{ background: #edf2f7; color: #4a5568; }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>VEDIC & SCIENTIFIC ASTROLOGICAL CONSULTATION DOSSIER</h1>
            <p>Parashara • KP (249 Subs) • Dr. B. V. Raman • Lal Kitab • Numerology</p>
        </div>
        <div class="content">
            <table>
                <tr>
                    <th>Client Name</th><td><b>{c.name}</b></td>
                    <th>Prashna Query Time</th><td>{q.query_datetime_local.strftime('%d-%b-%Y %I:%M %p')}</td>
                </tr>
                <tr>
                    <th>Birth Details</th><td>{c.birth_datetime_local.strftime('%d-%b-%Y %I:%M %p')} ({c.place_name})</td>
                    <th>Active Dasha</th><td><b>{resp.current_active_dasha['mahadasha']}-{resp.current_active_dasha['antardasha']}</b></td>
                </tr>
                <tr>
                    <th>Lagna & Moon Sign</th><td>{k.ascendant.sign.sanskrit_name} Lagna / {k.planets['Moon'].sign.sanskrit_name} Rasi</td>
                    <th>Numerology</th><td>Mulank {resp.numerology.mulank} | Bhagyank {resp.numerology.bhagyank} | Personal Year {resp.numerology.personal_year}</td>
                </tr>
            </table>

            <div class="verdict-box">
                <div style="font-size: 15px; color:#744210; margin-bottom: 4px;">CONSULTATION QUESTION:</div>
                <div style="font-size: 18px; font-weight: bold; color:#1a365d; margin-bottom: 12px;">"{q.question_text}"</div>
                <div style="font-size: 20px; font-weight: bold; color: #c53030;">{resp.unified_verdict}</div>
                <div style="font-size: 14px; color: #4a5568; margin-top: 4px;">Consensus Confidence Index: <b>{resp.consensus_probability_percent}%</b></div>
            </div>

            <h2>1. Real-Time Present Gochara (Transit) at Moment of Enquiry</h2>
            <div class="method-card" style="background:#fffaf0; border-left:4px solid #dd6b20;">
                <h3 style="color:#744210;">⚡ Why This Question Arose Right Now (Enquiry Diagnostic)</h3>
                <p>{resp.present_gochara.why_this_question_now_diagnostic}</p>
                <p><b>Saturn Transit:</b> {resp.present_gochara.saturn_transit_verdict}</p>
                <p><b>Jupiter Transit:</b> {resp.present_gochara.jupiter_transit_verdict}</p>
                <p><b>Immediate Timeline:</b><br/>{resp.present_gochara.immediate_30_60_90_day_forecast.replace(chr(10), '<br/>')}</p>
            </div>

            <h2>2. Comprehensive Shastric Planetary Aspects (Drishti Matrix)</h2>
            <table>
                <tr>
                    <th>Target Point</th>
                    <th>Aspecting Planets</th>
                    <th>Net Life Influence</th>
                </tr>
                {asp_html}
            </table>

            <h2>3. Present Name Diagnostic & General-Purpose Alternate Names</h2>
            <div class="method-card">
                <h3>📝 Present Name & Spelling Tuning (Non-Legal Usage)</h3>
                <p><b>Present Name:</b> "{resp.name_tuning.present_name}" (Compound {resp.name_tuning.present_chaldean_compound} &rarr; {resp.name_tuning.present_chaldean_single})</p>
                <p><b>Diagnostic:</b> {resp.name_tuning.present_name_status}</p>
                <h4>Recommended Minor Spelling Calibrations (For LinkedIn, Visiting Cards & Email Signatures):</h4>
                {cal_html}
                <p style="font-size:12px; color:#718096; margin-top:8px;"><i>Note: Keep your government documents (Aadhaar, Passport, PAN) untouched. Use the calibrated spelling for professional bylines and daily signatures.</i></p>
            </div>

            <h2>4. Education Stream, Education Break Risk & Profession</h2>
            <div class="grid-2">
                <div class="method-card">
                    <h3>🎓 Education Stream & Degrees</h3>
                    <p><b>Primary Stream:</b> {resp.education_stream.primary_stream}</p>
                    <p><b>Recommended Degrees:</b> {', '.join(resp.education_stream.recommended_degrees)}</p>
                </div>
                <div class="method-card">
                    <h3>⚠️ Education Break Assessment</h3>
                    <p><b>Break Risk Level:</b> <b>{resp.education_break.break_risk_level}</b></p>
                    <p><b>Vulnerable Windows:</b> {', '.join(resp.education_break.vulnerable_age_windows)}</p>
                </div>
            </div>

            <div class="method-card">
                <h3>💼 Profession, Vocational Trajectory & D10 Dashamsha</h3>
                <p><b>Career Path:</b> <b>{resp.profession.career_path_verdict}</b></p>
                <p><b>Amatyakaraka:</b> {resp.profession.amatyakaraka_planet} — {resp.profession.amatyakaraka_guidance}</p>
                <p><b>Top Domains:</b> {', '.join(resp.profession.top_recommended_domains)}</p>
            </div>

            <h2>5. Marriage Longevity & Breakup / Separation Risk Mitigation</h2>
            <div class="method-card">
                <h3>💍 Marital Stability & Longevity</h3>
                <p><b>Marital Longevity Score:</b> <b>{resp.marriage_breakup.marital_longevity_score} / 100</b> (Risk Level: <b>{resp.marriage_breakup.breakup_risk_level}</b>)</p>
                <p><b>Kuja / Manglik Dosha:</b> {resp.marriage_breakup.manglik_dosha_status}</p>
                <p><b>Conflict Triggers:</b> {'; '.join(resp.marriage_breakup.primary_conflict_triggers)}</p>
                <p><b>Sacred Remedy:</b> Wear certified <b>Gauri-Shankar Rudraksha</b> on Monday morning and chant Katyayani Mantra.</p>
            </div>

            <h2>6. Favourable & Unfavourable Mobile and Vehicle Numbers</h2>
            <div class="grid-2">
                <div class="method-card">
                    <h3>📱 Mobile Numbers Guidance</h3>
                    <p><b>Favourable Single Sums:</b> <span style="color:#2f855a; font-weight:bold;">{', '.join(map(str, resp.mobile_guidance.favourable_single_totals))}</span></p>
                    <p><b>Avoid Single Sums:</b> <span style="color:#c53030; font-weight:bold;">{', '.join(map(str, resp.mobile_guidance.unfavourable_single_totals))}</span></p>
                </div>
                <div class="method-card">
                    <h3>🚗 Vehicle Numbers (Vahana Bhava)</h3>
                    <p><b>4th House Vahana Lord:</b> {resp.vehicle_guidance.fourth_house_lord}</p>
                    <p><b>Favourable Plate Sums:</b> <span style="color:#2f855a; font-weight:bold;">{', '.join(map(str, resp.vehicle_guidance.favourable_plate_single_sums))}</span></p>
                    <p><b>Avoid Sums (Accident Triggers):</b> <span style="color:#c53030; font-weight:bold;">{', '.join(map(str, resp.vehicle_guidance.unfavourable_plate_single_sums))}</span></p>
                </div>
            </div>

            <h2>7. Comprehensive Master Remedial Dossier</h2>
            <h3>A. Sacred Plants & Trees Pradakshinam</h3>
            {plant_html}

            <h3>B. Prescribed Vedic & Bija Mantras</h3>
            {mantra_html}

            <div style="margin-top:24px; text-align:center; font-size:12px; color:#a0aec0; border-top:1px solid #e2e8f0; padding-top:12px;">
                Generated by Master Unified Multi-Method Astrology Consultation Engine.
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_html_path


def run_consultation_flow(
    name: str,
    dob_str: str,
    tob_str: str,
    place: str,
    lat: float,
    lon: float,
    tz_offset: float,
    question: str,
    category: str,
    query_dt: Optional[datetime] = None,
    output_prefix: str = "consultation",
    mobile_test: Optional[str] = None,
    vehicle_test: Optional[str] = None
) -> MultiMethodQAResponse:
    """Core consultation pipeline runner."""
    b_dt_str = f"{dob_str} {tob_str}"
    birth_dt = datetime.strptime(b_dt_str, "%Y-%m-%d %H:%M:%S")

    if not query_dt:
        query_dt = datetime.now()

    client = ClientProfile(
        name=name,
        birth_datetime_local=birth_dt,
        tz_offset_hours=tz_offset,
        latitude=lat,
        longitude=lon,
        place_name=place
    )

    query = QueryContext(
        question_text=question,
        question_category=category,
        query_datetime_local=query_dt,
        query_latitude=lat,
        query_longitude=lon,
        query_place_name=place,
        specific_mobile=mobile_test,
        specific_vehicle_plate=vehicle_test
    )

    response = MasterAstrologyQAEngine.evaluate_consultation(client, query)

    # Print summary to console
    print_dossier_summary(response)

    # Export PDF and HTML reports
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)

    slug = name.lower().replace(" ", "_").replace(".", "")
    pdf_filename = f"{slug}_{output_prefix}.pdf"
    html_filename = f"{slug}_{output_prefix}.html"

    pdf_path = os.path.join(out_dir, pdf_filename)
    html_path = os.path.join(out_dir, html_filename)

    generate_multimethod_qa_pdf(response, pdf_path)
    generate_html_consultation_dossier(response, html_path)

    print(f"\n[SUCCESS] Master Consultation Dossier Exported:")
    print(f"  • PDF Report : {pdf_path}")
    print(f"  • HTML Report: {html_path}")

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Method Astrological Q&A Consultation Engine")
    parser.add_argument("--name", type=str, default="Ravi Kumar S", help="Client Full Name")
    parser.add_argument("--dob", type=str, default="1983-05-15", help="Date of Birth (YYYY-MM-DD)")
    parser.add_argument("--tob", type=str, default="10:30:00", help="Time of Birth (HH:MM:SS)")
    parser.add_argument("--place", type=str, default="Bengaluru, Karnataka", help="Place of Birth")
    parser.add_argument("--lat", type=float, default=12.9716, help="Latitude")
    parser.add_argument("--lon", type=float, default=77.5946, help="Longitude")
    parser.add_argument("--tz", type=float, default=5.5, help="Timezone offset hours (e.g. 5.5 for IST)")
    parser.add_argument("--question", type=str, default="", help="Custom question to predict")
    parser.add_argument("--category", type=str, default="Career", help="Question category")
    parser.add_argument("--query-dt", type=str, default="", help="Enquiry datetime (YYYY-MM-DD HH:MM:SS), defaults to current clock moment")
    parser.add_argument("--mobile", type=str, default="9845012345", help="Optional 10-digit mobile number to test")
    parser.add_argument("--vehicle", type=str, default="KA 01 AB 1234", help="Optional vehicle plate to test")
    parser.add_argument("--prefix", type=str, default="multi_method_consultation", help="Output filename prefix")
    parser.add_argument("--open-chrome", action="store_true", help="Automatically open generated PDF and HTML in Chrome")
    parser.add_argument("--serve", action="store_true", help="Launch interactive web server on specified port")
    parser.add_argument("--port", type=int, default=8080, help="Port for the interactive web server (default: 8080)")

    args = parser.parse_args()

    if args.serve:
        start_consultation_server(port=args.port)
        sys.exit(0)

    q_text = args.question
    q_cat = args.category
    if not q_text:
        q_text = "What is my complete life trajectory, career & wealth peak, marriage harmony, education evaluation, favourable mobile/vehicle numbers, and current real-time Gochara forecast with complete remedies?"
        q_cat = "Comprehensive Life & Destiny"

    enquiry_dt = None
    if args.query_dt:
        enquiry_dt = datetime.strptime(args.query_dt, "%Y-%m-%d %H:%M:%S")
    else:
        enquiry_dt = datetime.now()

    response = run_consultation_flow(
        name=args.name,
        dob_str=args.dob,
        tob_str=args.tob,
        place=args.place,
        lat=args.lat,
        lon=args.lon,
        tz_offset=args.tz,
        question=q_text,
        category=q_cat,
        query_dt=enquiry_dt,
        output_prefix=args.prefix,
        mobile_test=args.mobile,
        vehicle_test=args.vehicle
    )

    if args.open_chrome:
        slug = args.name.lower().replace(" ", "_").replace(".", "")
        pdf_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", f"{slug}_{args.prefix}.pdf")
        html_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", f"{slug}_{args.prefix}.html")
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        chrome_exe = None
        for cp in chrome_paths:
            if os.path.exists(cp):
                chrome_exe = cp
                break
        
        import subprocess
        if chrome_exe:
            if os.path.exists(pdf_f):
                subprocess.Popen([chrome_exe, pdf_f])
            if os.path.exists(html_f):
                subprocess.Popen([chrome_exe, html_f])
            print(f"[INFO] Successfully launched Chrome with PDF: {pdf_f}")
        else:
            import webbrowser
            if os.path.exists(pdf_f):
                webbrowser.open(pdf_f)
            if os.path.exists(html_f):
                webbrowser.open(html_f)
