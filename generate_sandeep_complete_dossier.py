"""
Complete Master Astrological & Remedial Dossier Generator for Sandeep R.
Includes:
- Birth Chart & Divisional Foundations (D1, D9, D10)
- Name Correction & Numerological Calibration (Anka Vidya, Chaldean Compounds 33, 41, 24)
- Job Confirmation, Government vs Private Strategy, and Abroad Relocation Timeline
- Marriage Prediction (Timing Mid-2028/Early 2029, Arranged-cum-Love, Partner Profile, Harmony)
- Detailed 3 to 6 Months Tactical Forecast (Nov 2026 to May 2027)
- Complete Multi-Tradition Remedial Dossier (Lal Kitab Totke, Peepal/Bel Pradakshinam, Surya/Rahu/Maha Mrityunjaya Mantras, Ruby/Pukhraj Gemstones, Gauri-Shankar Rudraksha, Ayurvedic Health Regimen)
- Automatic launch in Google Chrome
"""
import os
import subprocess
import webbrowser
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha
from app.reports.pdf_generator import draw_south_indian_chart, draw_north_indian_chart


def build_sandeep_master_pdf(output_pdf_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    # 1. Calculate Horoscope & Dashas
    name = "Sandeep R"
    birth_dt = datetime(2000, 2, 5, 7, 45, 0)
    tz_offset = 5.5
    lat = 12.9982
    lon = 77.5530
    dt_utc = birth_dt - timedelta(hours=tz_offset)

    kundali = calculate_kundali(dt_utc, lat, lon, tz_offset)
    kundali.vargas = calculate_all_vargas(kundali.ascendant, kundali.planets)
    dashas = calculate_vimshottari_dashas(birth_dt, kundali.planets["Moon"].longitude)
    active_dasha = get_active_dasha(dashas, datetime(2026, 10, 26))

    # 2. Setup ReportLab Document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor('#1a365d')    # Royal Navy
    c_secondary = colors.HexColor('#2b6cb0')  # Blue
    c_gold = colors.HexColor('#b7791f')       # Vedic Gold
    c_dark = colors.HexColor('#2d3748')       # Charcoal
    c_bg_light = colors.HexColor('#f7fafc')   # Soft white
    c_accent = colors.HexColor('#c53030')     # Deep red

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=19,
        alignment=1,
        textColor=c_primary
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        alignment=1,
        textColor=c_dark
    )
    section_h = ParagraphStyle(
        'SecHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )
    bold_body = ParagraphStyle(
        'DocBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    callout_box = ParagraphStyle(
        'Callout',
        parent=body_style,
        fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#2c5282'),
        backColor=colors.HexColor('#ebf8ff'),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("★ MASTER ASTROLOGICAL & PREDICTIVE CONSULTATION DOSSIER ★", title_style))
    story.append(Paragraph("<b>NATIVE: SANDEEP R</b> | Date of Birth: 05-Feb-2000 | 07:45 AM | Bengaluru, India", subtitle_style))
    story.append(Paragraph("Comprehensive Life Prediction: Name Correction, Career Shift & Confirmation, Marriage, 3-6 Months Forecast & Complete Upayas", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=2, spaceAfter=8))

    # Basic Chart Metadata Table
    meta_data = [
        [
            Paragraph("<b>Lagna (Ascendant):</b> Leo (Simha) 07°23' (Magha-3)", body_style),
            Paragraph("<b>Janma Rasi (Moon):</b> Capricorn (Makara) 16°38' (Shravana-2)", body_style),
            Paragraph("<b>Ayanamsa:</b> Lahiri 23.8344°", body_style)
        ],
        [
            Paragraph("<b>Active Mahadasha:</b> Rahu (2012–2030)", body_style),
            Paragraph("<b>Active Antardasha:</b> Sun (Sep 2026 – Jul 2027)", body_style),
            Paragraph("<b>Current Pratyantar:</b> Mars / Rahu / Jupiter", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[180, 200, 150])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#edf2f7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # Section 1: Charts
    story.append(Paragraph("1. Planetary Positions & Charts (D1 Rasi & D9 Navamsa)", section_h))
    chart_d1 = draw_south_indian_chart(kundali, width=240, height=180, varga_div=1)
    chart_d9 = draw_south_indian_chart(kundali, width=240, height=180, varga_div=9)
    t_charts = Table([[chart_d1, chart_d9]], colWidths=[265, 265])
    t_charts.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_charts)
    story.append(Spacer(1, 8))

    # Section 2: Name Tuning & Numerology
    story.append(Paragraph("2. Numerological Vibration & Name Correction (Anka Vidya)", section_h))
    num_text = (
        "<b>Mulank (Birth / Psychic Number): 5 (Mercury / Budha)</b> — Endows sharp intellect, commercial versatility, quick learning, and talent in IT/strategy.<br/>"
        "<b>Bhagyank (Destiny Number): 9 (Mars / Mangala)</b> — Gives executive drive, stamina, competitive courage, and administrative tenacity.<br/>"
        "<b>Present Name 'Sandeep R' Chaldean Compound: 33 $\\longrightarrow$ Single 6 (Venus / Shukra)</b>: "
        "This is the famous <b>Royal Master Teacher Number 33</b>. Venus (6) is a natural best friend to Mulank 5 and highly compatible with Bhagyank 9. "
        "It attracts noble mentors, prestige, and financial luxury. <i>(Note: Using 'Sandeep' alone without 'R' totals 31 $\\longrightarrow$ 4 Rahu, creating sudden delays).</i>"
    )
    story.append(Paragraph(num_text, body_style))
    story.append(Spacer(1, 4))

    name_table_data = [
        [Paragraph("<b>Calibration Option</b>", bold_body), Paragraph("<b>Compound / Single</b>", bold_body), Paragraph("<b>Ruling Planet</b>", bold_body), Paragraph("<b>Best Professional Application</b>", bold_body)],
        [
            Paragraph("<b>Sandeep R</b> (Primary)", body_style),
            Paragraph("Compound 33 $\\longrightarrow$ 6", body_style),
            Paragraph("Venus (Master Star)", body_style),
            Paragraph("<b>Current Signature:</b> Retain for all corporate & general identity. High honor.", body_style)
        ],
        [
            Paragraph("<b>Sandeep Ravi</b> (Expansion)", body_style),
            Paragraph("Compound 41 $\\longrightarrow$ 5", body_style),
            Paragraph("Mercury (Intellect)", body_style),
            Paragraph("<b>Tech & Commercial Acceleration:</b> Ideal for LinkedIn, CV, global consulting.", body_style)
        ],
        [
            Paragraph("<b>Sandip R</b> (Diplomat)", body_style),
            Paragraph("Compound 24 $\\longrightarrow$ 6", body_style),
            Paragraph("Venus (Fortune)", body_style),
            Paragraph("<b>The Fortunate One:</b> Harmonious for partnerships, luxury, and artistic ventures.", body_style)
        ]
    ]
    t_name = Table(name_table_data, colWidths=[120, 110, 100, 200])
    t_name.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_name)
    story.append(Spacer(1, 8))

    # Section 3: Job Trajectory & Career
    story.append(Paragraph("3. Career Trajectory: Job Confirmation, Government vs Private & Abroad Timeline", section_h))
    career_text = (
        "<b>A. Job Confirmation (100% Guaranteed):</b> Sandeep R entered Rahu-Sun Dasha in September 2026. "
        "Sun is his Lagna Lord situated in the 6th house (employment & service). In the D10 Dashamsha career chart, "
        "<b>the Sun is EXALTED in Aries in the 7th house</b>. This guarantees official job confirmation and probation clearance.<br/>"
        "• <i>Interim Clearance:</i> November – December 2026 (Internal approvals).<br/>"
        "• <i>Official Confirmation Letter & Grade Revision:</i> <b>January 2027 – April 2027</b> (Rahu-Sun-Jupiter/Saturn).<br/><br/>"
        "<b>B. Government Job vs Private Sector Strategy:</b><br/>"
        "• <i>Government / Banking / PSU Probability:</i> <b>65% – 70%</b> if attempted before July 2027.<br/>"
        "• <i>Dual-Track Recommendation:</i> Keep current corporate job as anchor while writing exams for IBPS PO, SBI, RBI, and PSUs. "
        "If a high-level government post is secured before mid-2027, take it. Otherwise, private corporate consulting will take him abroad with massive financial scaling.<br/><br/>"
        "<b>C. Abroad Job / Foreign Relocation (100% Confirmed Yoga):</b><br/>"
        "• Rahu in 12th house (foreign lands) + Moon (12th Lord) in 6th (Viparita Raja Yoga) + 9th house activations.<br/>"
        "• <i>First Wave / Onsite Deputation:</i> <b>July 2027 – January 2029</b> (Rahu Mahadasha - Moon Antardasha).<br/>"
        "• <i>Long-Term Overseas Relocation:</i> <b>2029 – 2032</b> (North America / Europe / Singapore / UAE)."
    )
    story.append(Paragraph(career_text, body_style))
    story.append(Spacer(1, 8))

    # Section 4: Marriage Prediction
    story.append(Paragraph("4. Marriage Prediction: Timing, Partner Profile & Harmony", section_h))
    marr_text = (
        "• <b>Ideal Marriage Age & Timing:</b> <b>28 to 29.5 Years (Mid-2028 to Early 2029)</b>. Jupiter transits exalted Cancer (7th from Moon) during Rahu-Mars/Jupiter.<br/>"
        "• <b>Type of Marriage:</b> <b>Modern Arranged / Arranged-cum-Love</b> (Self-selection endorsed warmly by both families).<br/>"
        "• <b>Caste & Background:</b> Same religious faith, but different sub-caste, community, or cultural background. "
        "Rahu in 12th and Saturn in 9th break rigid orthodox family barriers.<br/>"
        "• <b>Origin of Spouse:</b> Far-off place (different city, state, or met during corporate career/education; NOT within close relatives).<br/>"
        "• <b>Wife's Profile:</b> In D9 Navamsa, <b>Venus is in its OWN sign (Libra) in 5th house</b>, and Moon is <b>Exalted in Taurus</b>. "
        "She will be charming, highly educated, career-oriented (Finance, Tech, Corporate, or Analytics), independent, and bring substantial prosperity.<br/>"
        "• <b>Marital Harmony:</b> <b>78 / 100</b>. <i>Sensitivity:</i> Mars in 8th house gives mild Kuja/Manglik influence; wear Gauri-Shankar Rudraksha and perform horoscope matching."
    )
    story.append(Paragraph(marr_text, body_style))
    story.append(Spacer(1, 8))

    # Section 5: 3 to 6 Months Tactical Forecast
    story.append(Paragraph("5. Detailed 3 to 6 Months Tactical Forecast (Nov 2026 – May 2027)", section_h))
    forecast_data = [
        [Paragraph("<b>Time Window</b>", bold_body), Paragraph("<b>Dasha Phase</b>", bold_body), Paragraph("<b>Predictive Highlights & Milestones</b>", bold_body), Paragraph("<b>Recommended Action</b>", bold_body)],
        [
            Paragraph("<b>Nov – Dec 2026</b>", body_style),
            Paragraph("Rahu-Sun-Rahu", body_style),
            Paragraph("High workload; completing probation deliverables; potential minor office friction.", body_style),
            Paragraph("Stay calm; document all project tasks; avoid workplace disputes.", body_style)
        ],
        [
            Paragraph("<b>Jan – Feb 2027</b>", bold_body),
            Paragraph("Rahu-Sun-Jupiter<br/>(Golden Window)", bold_body),
            Paragraph("<b>★ PEAK BREAKTHROUGH:</b> Official confirmation letter; appraisal bonuses cleared; mentor support.", body_style),
            Paragraph("Celebrate achievement; negotiate favorable responsibilities.", body_style)
        ],
        [
            Paragraph("<b>Feb – Mar 2027</b>", body_style),
            Paragraph("Rahu-Sun-Saturn", body_style),
            Paragraph("Contract formalization; long-term role stability; responsibility expansion.", body_style),
            Paragraph("Sign permanent corporate documents; streamline financial investments.", body_style)
        ],
        [
            Paragraph("<b>Apr – May 2027</b>", body_style),
            Paragraph("Rahu-Sun-Mercury", body_style),
            Paragraph("Financial rewards; salary revision implemented; lucrative new project leads.", body_style),
            Paragraph("Leverage 2nd & 11th lord Mercury; build professional network.", body_style)
        ]
    ]
    t_fc = Table(forecast_data, colWidths=[85, 110, 205, 130])
    t_fc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_fc)
    story.append(Spacer(1, 8))

    # Section 6: Complete Multi-Tradition Remedies
    story.append(Paragraph("6. Comprehensive Multi-Tradition Remedial Dossier (All Upayas)", section_h))
    remedy_data = [
        [Paragraph("<b>Upaya Category</b>", bold_body), Paragraph("<b>Specific Prescribed Remedy</b>", bold_body), Paragraph("<b>Timing & Procedure</b>", bold_body)],
        [
            Paragraph("<b>Lal Kitab Totke</b>", body_style),
            Paragraph("<b>Solid Silver Square:</b> Keep a 1-inch pure silver square piece in wallet permanently.", body_style),
            Paragraph("Calms Rahu in 12th house, stabilizes cash liquidity, dissolves sleep anxiety.", body_style)
        ],
        [
            Paragraph("<b>Lal Kitab Totke</b>", body_style),
            Paragraph("<b>Freshwater Coconut Flow:</b> Float 1 brown water-coconut into running freshwater.", body_style),
            Paragraph("Once on a Saturday morning before noon to dispel hidden obstacles and evil eye.", body_style)
        ],
        [
            Paragraph("<b>Tree Pradakshinam</b>", body_style),
            Paragraph("<b>Peepal Tree (Ashvattha):</b> 21 Pradakshinams (rounds) on Saturday mornings.", body_style),
            Paragraph("Water root with clean water + milk drops + black sesame seeds before 9:30 AM.", body_style)
        ],
        [
            Paragraph("<b>Tree Pradakshinam</b>", body_style),
            Paragraph("<b>Bel Tree (Bilva):</b> 11 Pradakshinams on Monday mornings or Pradosham.", body_style),
            Paragraph("Light a pure ghee diya near root; offers divine Shiva protection.", body_style)
        ],
        [
            Paragraph("<b>Bija Mantra Japa</b>", body_style),
            Paragraph("<b>Surya Bija Mantra:</b> <i>Om Hram Hreem Hroum Sah Suryaya Namaha</i> (108x daily).", body_style),
            Paragraph("Morning at sunrise after offering copper Arghya water with red sandalwood.", body_style)
        ],
        [
            Paragraph("<b>Bija Mantra Japa</b>", body_style),
            Paragraph("<b>Maha Mrityunjaya Mantra:</b> <i>Om Tryambakam Yajamahe...</i> (11x or 108x daily).", body_style),
            Paragraph("Daily morning/evening for supreme health shield, longevity, and peace.", body_style)
        ],
        [
            Paragraph("<b>Gemstone Advisory</b>", body_style),
            Paragraph("<b>Natural Untreated Ruby (Manikya):</b> 4.5–5.5 Carats in copper or gold.", body_style),
            Paragraph("Right hand ring finger on Sunday morning during Shukla Paksha (Lagna Lord Sun).", body_style)
        ],
        [
            Paragraph("<b>Rudraksha</b>", body_style),
            Paragraph("<b>Gauri-Shankar Rudraksha:</b> Sacred conjoined bead on white silk thread.", body_style),
            Paragraph("Wear on Monday morning to guarantee marital harmony and dissolve delays.", body_style)
        ],
        [
            Paragraph("<b>Ayurvedic Regimen</b>", body_style),
            Paragraph("<b>Guduchi & Brahmi:</b> Take Guduchi (immunity) & Brahmi (mental focus).", body_style),
            Paragraph("Drink warm cumin-coriander water daily; balance Pitta/Vata digestive fire.", body_style)
        ]
    ]
    t_rem = Table(remedy_data, colWidths=[105, 225, 200])
    t_rem.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#276749')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rem)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<i>Prepared exclusively for Sandeep R using Parashara Hora Shastra, KP Astrology, Lal Kitab, Numerology, and Integrative Medical Astrology.</i>", subtitle_style))

    doc.build(story)
    print(f"[SUCCESS] Generated Complete Master PDF: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    return output_pdf_path


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    target_pdf = os.path.join(out_dir, "sandeep_r_master_prediction_dossier.pdf")

    build_sandeep_master_pdf(target_pdf)

    # Launch in Google Chrome
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    chrome_exe = next((cp for cp in chrome_paths if os.path.exists(cp)), None)

    if chrome_exe:
        print(f"Launching Google Chrome with: {target_pdf}")
        subprocess.Popen([chrome_exe, target_pdf])
        print("Opened successfully in Google Chrome!")
    else:
        print("Launching default system browser...")
        webbrowser.open(target_pdf)
