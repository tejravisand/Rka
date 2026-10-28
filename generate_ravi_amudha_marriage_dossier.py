"""
Comprehensive Couple Astrological & Marital Consultation Dossier Generator for:
Husband: Ravi Kumar S (20-Nov-1968, 03:45 AM, Bangalore)
Wife   : Amudha R (14-Jul-1979, 04:10 PM, Chittoor)
Married: 03-May-1999 (27+ Years of Marriage)

Evaluates:
1. Couple Planetary Placements & Synastry Matrix (Chandra-Lagna Sambandha)
2. Children & Progeny Analysis (D1 5th house, D7 Saptamsa, Exalted Jupiter in Wife's chart, 2 Children verdict)
3. Marital Life Quality & Psychological Dynamics (Strengths, Friction points, Emotional Anchors)
4. Comprehensive Dosha Evaluation (Kuja/Manglik Dosha Samyam Cancellation, Bhakoot Cancellation, 0 Nadi Dosha, Rahu-Ketu Axis)
5. Harmonizing Upayas & Vedic Remedies
"""
import os
import shutil
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
from app.reports.pdf_generator import draw_south_indian_chart


def build_couple_dossier_pdf(output_pdf_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    tz = 5.5

    # 1. Husband Chart: Ravi Kumar S
    r_bdt = datetime(1968, 11, 20, 3, 45, 0)
    r_utc = r_bdt - timedelta(hours=tz)
    r_lat, r_lon = 13.0068, 77.5713
    r_kundali = calculate_kundali(r_utc, r_lat, r_lon, tz)
    r_kundali.vargas = calculate_all_vargas(r_kundali.ascendant, r_kundali.planets)
    r_dashas = calculate_vimshottari_dashas(r_bdt, r_kundali.planets['Moon'].longitude)
    r_active = get_active_dasha(r_dashas, datetime(2026, 10, 27))

    # 2. Wife Chart: Amudha R
    a_bdt = datetime(1979, 7, 14, 16, 10, 0)
    a_utc = a_bdt - timedelta(hours=tz)
    a_lat, a_lon = 13.2172, 79.1003
    a_kundali = calculate_kundali(a_utc, a_lat, a_lon, tz)
    a_kundali.vargas = calculate_all_vargas(a_kundali.ascendant, a_kundali.planets)
    a_dashas = calculate_vimshottari_dashas(a_bdt, a_kundali.planets['Moon'].longitude)
    a_active = get_active_dasha(a_dashas, datetime(2026, 10, 27))

    # 3. Document Setup
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor('#1a365d')    # Royal Navy
    c_secondary = colors.HexColor('#2b6cb0')  # Blue
    c_gold = colors.HexColor('#b7791f')       # Vedic Gold
    c_dark = colors.HexColor('#2d3748')       # Charcoal
    c_bg_light = colors.HexColor('#f7fafc')   # Soft white
    c_maroon = colors.HexColor('#7b1113')     # Auspicious Sindoor

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1,
        textColor=c_maroon
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=c_dark
    )
    section_h = ParagraphStyle(
        'SecHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=c_primary,
        spaceBefore=7,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )
    bold_body = ParagraphStyle(
        'DocBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title Banner
    story.append(Paragraph("★ VEDIC COUPLE ASTROLOGICAL DOSSIER: MARITAL EVALUATION ★", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>HUSBAND: RAVI KUMAR S</b> (20-Nov-1968 | 03:45 AM | Bengaluru) &nbsp;•&nbsp; <b>WIFE: AMUDHA R</b> (14-Jul-1979 | 04:10 PM | Chittoor)", subtitle_style))
    story.append(Paragraph("<b>Solemnized on: 03-May-1999</b> &nbsp;|&nbsp; <b>Marital Journey: 27+ Years of Committed Union</b> &nbsp;|&nbsp; Progeny, Marital Life & Complete Dosha Audit", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=2, spaceAfter=6))

    # Comparative Natal Foundation Table
    meta_data = [
        [
            Paragraph("<b>Astrological Factor</b>", bold_body),
            Paragraph("<b>Husband: Ravi Kumar S</b>", bold_body),
            Paragraph("<b>Wife: Amudha R</b>", bold_body),
            Paragraph("<b>Synastry / Compatibility Verdict</b>", bold_body)
        ],
        [
            Paragraph("<b>Lagna (Ascendant)</b>", body_style),
            Paragraph("<b>Pisces (Meena) 26°37'</b><br/>(Revati - Mercury)", body_style),
            Paragraph("<b>Taurus (Vrishabha) 22°46'</b><br/>(Rohini - Moon)", body_style),
            Paragraph("<b>Sextile 3/11 Alignment:</b> Friendly, collaborative rapport. Wife grounds husband's visionary ideals.", body_style)
        ],
        [
            Paragraph("<b>Janma Rasi (Moon)</b>", body_style),
            Paragraph("<b>Libra (Tula) 28°26'</b><br/>(Vishakha-3 - Jupiter)", body_style),
            Paragraph("<b>Pisces (Meena) 01°25'</b><br/>(Purva Bhadrapada-4 - Jupiter)", body_style),
            Paragraph("<b>★ SUPREME CHANDRA-LAGNA BOND:</b> Wife's Moon sits in Husband's Lagna! Deep instinctive emotional empathy.", body_style)
        ],
        [
            Paragraph("<b>Nakshatra Lord</b>", body_style),
            Paragraph("<b>Jupiter (Guru)</b>", body_style),
            Paragraph("<b>Jupiter (Guru)</b>", body_style),
            Paragraph("<b>Same Lord (*Ekadhipatya*):</b> Both ruled by Guru. Nullifies theoretical Bhakoot and Gana frictions.", body_style)
        ],
        [
            Paragraph("<b>Mars Placement</b>", body_style),
            Paragraph("Virgo 13°32' (<b>7th House</b>)", body_style),
            Paragraph("Taurus 19°15' (<b>1st House</b>)", body_style),
            Paragraph("<b>KUJA DOSHA SAMYAM:</b> 7th Mars in Husband balanced by 1st Mars in Wife. Mutual complete cancellation.", body_style)
        ],
        [
            Paragraph("<b>Putrakaraka (Guru)</b>", body_style),
            Paragraph("Virgo 07°40' (7th House)", body_style),
            Paragraph("Cancer 20°16' (<b>EXALTED in 3rd</b>)", body_style),
            Paragraph("<b>Supreme Progeny Yoga:</b> Exalted Jupiter conjunct Wife's 5th Lord Mercury guarantees noble, successful lineage.", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[90, 130, 130, 175])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # Dual Charts: Side by Side
    story.append(Paragraph("1. Primary Natal Charts (South Indian Format)", section_h))
    chart_ravi = draw_south_indian_chart(r_kundali, width=245, height=155, varga_div=1)
    chart_amudha = draw_south_indian_chart(a_kundali, width=245, height=155, varga_div=1)
    t_charts = Table([
        [Paragraph("<b>Husband: Ravi Kumar S (D1 Rasi)</b>", subtitle_style), Paragraph("<b>Wife: Amudha R (D1 Rasi)</b>", subtitle_style)],
        [chart_ravi, chart_amudha]
    ], colWidths=[260, 260])
    t_charts.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_charts)
    story.append(Spacer(1, 6))

    # Section 2: Children Analysis
    story.append(Paragraph("2. Children & Progeny Analysis (Santan Bhava & D7 Saptamsa)", section_h))
    prog_text = (
        "<b>A. Astrological Progeny Verdict:</b> <b>Confirmed for Two (2) Children (Classically 1 Son and 1 Daughter)</b>.<br/>"
        "• <b>Wife's Chart (The Core Deciding Factor):</b> In Amudha's horoscope, the 5th house of children is Virgo (*Kanya*). "
        "The 5th Lord Mercury is placed in Cancer directly conjunct <b>EXALTED JUPITER (*Guru in Uchha*) at 20°</b>. "
        "In Brihat Parasara Hora Sastra, 5th lord conjoining Exalted Putrakaraka Jupiter is considered the supreme *Vamsha Vriddhi Yoga* (assured, blessed progeny).<br/>"
        "• <b>Husband's Chart:</b> Ravi Kumar's 5th house is Cancer (*Karka* - fruitful water sign), ruled by Moon. In D7 Saptamsa, Jupiter sits in Aries in 2nd house of family.<br/>"
        "• <b>Childbirth Timing:</b> Both entered Mercury Mahadasha around 2000 (Amudha's Mercury is 5th Lord; Ravi's was in Mercury-Moon). "
        "Children were born during the <b>2000 to 2005 window</b>, now grown into young adults completing higher education or early professional careers."
    )
    story.append(Paragraph(prog_text, body_style))
    story.append(Spacer(1, 6))

    # Section 3: Marital Life Quality
    story.append(Paragraph("3. Married Life Evaluation: Strengths, Dynamics & Resilience", section_h))
    marr_text = (
        "<b>A. 27+ Years of Resilient Foundation:</b> Having solemnized their wedding on <b>03-May-1999</b>, this union has endured "
        "nearly three decades of shared responsibilities, proving that their spiritual anchors outweigh temporary planetary frictions.<br/>"
        "• <b>The Soul Connection:</b> Amudha's Janma Moon is in Pisces, which is Ravi Kumar's exact Lagna. This generates an unspoken emotional resonance "
        "where the wife instinctively senses the husband's stress, offering steady home-based grounding.<br/>"
        "• <b>Husband's Temperament in Marriage:</b> Ravi has Saturn & Rahu in Lagna with Jupiter, Mars, Ketu in 7th. He carries deep devotion and heavy responsibility for family security. "
        "Occasional stress or work overload can make him withdrawn, but <b>Jupiter in 7th Kendra (*Guru-Mangala Yoga*)</b> always restores fairness and care.<br/>"
        "• <b>Wife's Temperament in Marriage:</b> Amudha has Mars in Taurus in Lagna with Sun & Venus in 2nd. She is strong-willed, protective, practical, and candid in speech. "
        "She manages household operations with authority and will not tolerate disrespect.<br/>"
        "• <b>Friction Triggers & Mitigation:</b> Both partners have strong conviction and pride (Mars on 1st/7th axis). Disagreements arise over domestic priorities or extended family matters, "
        "but Jupiter's grace ensures quarrels dissolve into mature consensus without endangering the marital bond."
    )
    story.append(Paragraph(marr_text, body_style))
    story.append(Spacer(1, 6))

    # Section 4: Comprehensive Dosha Audit
    story.append(Paragraph("4. Comprehensive Astrological Dosha Audit & Cancellations", section_h))
    dosha_data = [
        [Paragraph("<b>Dosha Category</b>", bold_body), Paragraph("<b>Presence in Chart</b>", bold_body), Paragraph("<b>Shastric Evaluation & Cancellation Status</b>", bold_body)],
        [
            Paragraph("<b>Kuja / Manglik Dosha</b>", bold_body),
            Paragraph("<b>Present in Both:</b><br/>• Ravi: Mars in 7th<br/>• Amudha: Mars in 1st", body_style),
            Paragraph("<b>100% CANCELLED (*Kuja Dosha Samyam*):</b> Classical rule (*Bhavartha Ratnakara*): Mars in Kuja house of husband neutralized by Mars in Kuja house of wife. Furthermore, Ravi's Mars is conjoined with Jupiter.", body_style)
        ],
        [
            Paragraph("<b>Nadi Dosha</b>", bold_body),
            Paragraph("<b>ZERO DOSHA (0% Affliction)</b><br/>• Ravi: Antya Nadi<br/>• Amudha: Adya Nadi", body_style),
            Paragraph("<b>PERFECT 8 / 8 POINTS:</b> Different Nadis guarantee genetic vitality, physiological harmony, and healthy lineage continuation.", body_style)
        ],
        [
            Paragraph("<b>Bhakoot (6/8 Shadashtaka)</b>", bold_body),
            Paragraph("<b>Present between Moons:</b><br/>• Libra to Pisces = 6/8", body_style),
            Paragraph("<b>FULLY CANCELLED (*Ekadhipatya Bhanga*):</b> Both Janma Nakshatras (Vishakha & Purva Bhadrapada) are ruled by the <b>SAME LORD: JUPITER</b>. Rule: <i>'Ekadhipatye tu dosho na vidyate'</i>.", body_style)
        ],
        [
            Paragraph("<b>Rahu-Ketu Axis</b>", bold_body),
            Paragraph("• Ravi: 1st/7th Nodal Axis<br/>• Amudha: 4th/10th Axis (Saturn-Rahu)", body_style),
            Paragraph("<b>MILD DOMESTIC ANXIETY:</b> Occasional property or health worries. Amudha's Saturn-Rahu in 4th can give fatigue; pacified through regular Shiva/Durga prayers.", body_style)
        ]
    ]
    t_dosha = Table(dosha_data, colWidths=[120, 140, 265])
    t_dosha.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7b1113')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_dosha)
    story.append(Spacer(1, 6))

    # Section 5: Remedies
    story.append(Paragraph("5. Recommended Upayas & Harmonizing Remedies for Ongoing Prosperity", section_h))
    rem_data = [
        [Paragraph("<b>Category</b>", bold_body), Paragraph("<b>Prescribed Spiritual Remedy</b>", bold_body), Paragraph("<b>Procedure & Benefit for the Couple</b>", bold_body)],
        [
            Paragraph("<b>Joint Family Pooja</b>", body_style),
            Paragraph("<b>Friday Lakshmi-Narayana Ghee Deepam:</b> Light a pure cow-ghee lamp in the home prayer altar every Friday evening.", body_style),
            Paragraph("Chant *Om Namo Bhagavate Vasudevaya* 11 times together; invites sustained wealth, domestic peace, and emotional warmth.", body_style)
        ],
        [
            Paragraph("<b>Lord Shiva Archana</b>", body_style),
            Paragraph("<b>Pradosham Bilva Archana:</b> Offer Bilva leaves and milk abhishekam to Lord Shiva on Shukla & Krishna Pradosham.", body_style),
            Paragraph("Dissolves residual fiery stress from Mars-Ketu and calms the Rahu-Saturn axis.", body_style)
        ],
        [
            Paragraph("<b>Lal Kitab Upaya</b>", body_style),
            Paragraph("<b>Solid Silver Square:</b> Place a 1-inch pure silver square piece in the domestic cash locker or pooja room.", body_style),
            Paragraph("Fortifies Chandra (Moon) and stabilizes household liquidity and peace (*Sukha Bhava*).", body_style)
        ]
    ]
    t_rem = Table(rem_data, colWidths=[105, 205, 215])
    t_rem.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#276749')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rem)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<i>Prepared exclusively for Ravi Kumar S & Amudha R using classical Brihat Parasara Hora Sastra, Bhavartha Ratnakara, and Vedic Synastry principles.</i>", subtitle_style))

    doc.build(story)
    print(f"[SUCCESS] Generated Couple Consultation PDF: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    return output_pdf_path


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    target_pdf = os.path.join(out_dir, "ravi_amudha_marriage_consultation_dossier.pdf")

    build_couple_dossier_pdf(target_pdf)

    # Copy to workspace root
    root_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ravi_amudha_marriage_consultation_dossier.pdf")
    shutil.copyfile(target_pdf, root_pdf)

    # Copy to artifact directory if available
    artifact_dir = r"C:\Users\Admin\.gemini\antigravity\brain\cca4e891-c56a-4839-9377-9103886054ad"
    if os.path.isdir(artifact_dir):
        shutil.copyfile(target_pdf, os.path.join(artifact_dir, "ravi_amudha_marriage_consultation_dossier.pdf"))

    # Launch in Google Chrome
    url = "http://localhost:8080/ravi_amudha_marriage_consultation_dossier.pdf"
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    chrome_exe = next((cp for cp in chrome_paths if os.path.exists(cp)), None)

    if chrome_exe:
        print(f"Launching Google Chrome with: {url}")
        subprocess.Popen([chrome_exe, url])
        print("Opened successfully in Google Chrome!")
    else:
        print("Launching default system browser...")
        webbrowser.open(url)
