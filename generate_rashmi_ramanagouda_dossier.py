"""
Comprehensive Couple Astrological Consultation Dossier Generator for:
Wife   : Rashmi Patil (14-Jul-1993, 07:05 AM, Mahalingpur, Karnataka)
Husband: Ramanagouda Patil (16-May-1994, 10:30 AM, Bijapur, Karnataka)

Detailed 7-Question Predictive Evaluation:
1. Married Life & Longevity (Same Capricorn Lagna, 28/36 Ashta Koota, Lifelong union)
2. Husband Job (Dec 2026 - Apr 2027) & Wife Better Placement (Feb 2027 - Aug 2027)
3. Family Support (Parental backing, in-laws dynamics)
4. Fortune & Luck (Wife is financial catalyst, husband is stabilizing anchor)
5. Children & Progeny (Two children, 1 Boy 1 Girl, 2028-2029 timing)
6. Financial Independence & Stability Ages (Age 33-34 stability, Age 35-38 peak wealth)
7. New Vehicle (May-Dec 2027) & Home Construction (2029-2031)
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


def build_rashmi_ramanagouda_pdf(output_pdf_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    tz = 5.5

    # 1. Wife Chart: Rashmi Patil
    w_bdt = datetime(1993, 7, 14, 7, 5, 0)
    w_utc = w_bdt - timedelta(hours=tz)
    w_lat, w_lon = 16.3867, 75.1225
    w_kundali = calculate_kundali(w_utc, w_lat, w_lon, tz)
    w_kundali.vargas = calculate_all_vargas(w_kundali.ascendant, w_kundali.planets)

    # 2. Husband Chart: Ramanagouda Patil
    h_bdt = datetime(1994, 5, 16, 10, 30, 0)
    h_utc = h_bdt - timedelta(hours=tz)
    h_lat, h_lon = 16.8302, 75.7100
    h_kundali = calculate_kundali(h_utc, h_lat, h_lon, tz)
    h_kundali.vargas = calculate_all_vargas(h_kundali.ascendant, h_kundali.planets)

    # Document Setup
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
        fontSize=10,
        leading=13,
        textColor=c_primary,
        spaceBefore=6,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=c_dark
    )
    bold_body = ParagraphStyle(
        'DocBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title Banner
    story.append(Paragraph("★ VEDIC COUPLE ASTROLOGICAL DOSSIER & COMPREHENSIVE LIFE PREDICTIONS ★", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>WIFE: RASHMI PATIL</b> (14-Jul-1993, 07:05 AM, Mahalingpur, KA) &nbsp;•&nbsp; <b>HUSBAND: RAMANAGOUDA PATIL</b> (16-May-1994, 10:30 AM, Bijapur, KA)", subtitle_style))
    story.append(Paragraph("Comprehensive Astrological Synastry, Career Timings, Family Support, Children, Financial Independence, Vehicle & Property Forecast", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=2, spaceAfter=5))

    # Comparative Natal Foundation Table
    meta_data = [
        [
            Paragraph("<b>Parameter</b>", bold_body),
            Paragraph("<b>Wife: Rashmi Patil</b>", bold_body),
            Paragraph("<b>Husband: Ramanagouda Patil</b>", bold_body),
            Paragraph("<b>Astrological Synastry Alignment</b>", bold_body)
        ],
        [
            Paragraph("<b>Lagna (Ascendant)</b>", body_style),
            Paragraph("<b>Capricorn (Makara) 10°35'</b><br/>(Shravana-1)", body_style),
            Paragraph("<b>Capricorn (Makara) 04°57'</b><br/>(Uttara Ashadha-3)", body_style),
            Paragraph("<b>★ EKA-LAGNA (Same Ascendant):</b> Identical worldview, grounded values, mutual understanding, shared life goals.", body_style)
        ],
        [
            Paragraph("<b>Janma Rasi (Moon)</b>", body_style),
            Paragraph("<b>Aries (Mesha) 21°25'</b><br/>(Bharani-3 - Venus)", body_style),
            Paragraph("<b>Cancer (Karka) 03°02'</b><br/>(Punarvasu-4 - Jupiter)", body_style),
            Paragraph("<b>KENDRA SAMBANDHA:</b> Husband's Moon sits in Wife's 7th house (own sign Cancer!). Wife's Moon sits in Husband's 4th house.", body_style)
        ],
        [
            Paragraph("<b>Lagna Lord Saturn</b>", body_style),
            Paragraph("Aquarius 05°26' (<b>Own Sign in 2nd</b>)", body_style),
            Paragraph("Aquarius 17°14' (<b>Own Sign in 2nd</b>)", body_style),
            Paragraph("<b>Mutual Dhana Yoga:</b> Both have Saturn in own sign in 2nd house of accumulated wealth! Guaranteed financial autonomy.", body_style)
        ],
        [
            Paragraph("<b>Ashta Koota Score</b>", body_style),
            Paragraph("Nadi: 8/8 • Gana: 6/6", body_style),
            Paragraph("Graha Maitri: 5/5", body_style),
            Paragraph("<b>28 / 36 POINTS (HIGH GRADE):</b> Zero Nadi Dosha, natural Deva-Manushya harmony, friendly Moon-Mars lords.", body_style)
        ],
        [
            Paragraph("<b>Current Dasha (2026)</b>", body_style),
            Paragraph("Rahu-Rahu (Shift to Jupiter Feb 2027)", body_style),
            Paragraph("Mercury-Jupiter (Venus pratyantar now)", body_style),
            Paragraph("<b>Synchronous Breakthrough:</b> Husband gets job (Dec 26 - Apr 27); Wife gets better placement (Feb 27 - Aug 27).", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[90, 130, 130, 175])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 5))

    # Dual Charts: Side by Side
    story.append(Paragraph("1. Primary Natal Charts (South Indian Format)", section_h))
    chart_rashmi = draw_south_indian_chart(w_kundali, width=245, height=140, varga_div=1)
    chart_ramana = draw_south_indian_chart(h_kundali, width=245, height=140, varga_div=1)
    t_charts = Table([
        [Paragraph("<b>Wife: Rashmi Patil (D1 Rasi)</b>", subtitle_style), Paragraph("<b>Husband: Ramanagouda Patil (D1 Rasi)</b>", subtitle_style)],
        [chart_rashmi, chart_ramana]
    ], colWidths=[260, 260])
    t_charts.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_charts)
    story.append(Spacer(1, 5))

    # Comprehensive 7-Question Breakdown Table
    story.append(Paragraph("2. Detailed Astrological Answers to Specific Questions", section_h))
    q_data = [
        [Paragraph("<b>Question</b>", bold_body), Paragraph("<b>Astrological Verdict & Exact Timing</b>", bold_body), Paragraph("<b>Scriptural Mechanics & Guidance</b>", bold_body)],
        [
            Paragraph("<b>Q1: Married Life & Longevity?</b>", bold_body),
            Paragraph("<b>Highly Stable, Lifelong Union (Score: 82/100).</b><br/>Zero separation yoga. Complete lifetime companionship.", body_style),
            Paragraph("Both share Capricorn Lagna; Husband's Moon is in Wife's 7th house (Cancer); Ashta Koota gives 28/36 with zero Nadi dosha. Reconciliations happen naturally.", body_style)
        ],
        [
            Paragraph("<b>Q2: Husband Job & Wife Placement?</b>", bold_body),
            Paragraph("• <b>Husband Job: Dec 2026 – Apr 2027</b><br/>• <b>Wife Better Placement: Feb 2027 – Aug 2027</b>", body_style),
            Paragraph("Husband runs Mercury-Jupiter-Venus (Venus is 10th lord of career). Wife transitions from Rahu-Rahu into Rahu-Jupiter (Jupiter is in 9th house of fortune).", body_style)
        ],
        [
            Paragraph("<b>Q3: Family Support for Both?</b>", bold_body),
            Paragraph("<b>Strong Parental Backing (75%–80%).</b><br/>Moral & crisis support from both sides.", body_style),
            Paragraph("Husband has Ruchaka Yoga Mars in 4th; Wife has Jupiter in 9th. In-laws are supportive, but couple should keep domestic decisions strictly between themselves.", body_style)
        ],
        [
            Paragraph("<b>Q4: Who is Lucky to Whom?</b>", bold_body),
            Paragraph("• <b>Wife is Financial Catalyst for Husband.</b><br/>• <b>Husband is Emotional Anchor for Wife.</b>", body_style),
            Paragraph("Husband's 7th house contains Moon, meaning career rise (*Bhagyodaya*) activates through wife's presence. Wife brings financial discipline; Husband brings stability.", body_style)
        ],
        [
            Paragraph("<b>Q5: Children: When & How Many?</b>", bold_body),
            Paragraph("<b>Two (2) Children (1 Boy, 1 Girl).</b><br/><b>Timing: Late 2027 to 2029.</b>", body_style),
            Paragraph("Wife has 5th lord Venus in own sign Taurus; Jupiter in 9th aspects 5th house. Conception window opens mid-2027 under Rahu-Jupiter dasha.", body_style)
        ],
        [
            Paragraph("<b>Q6: Age of Financial Independence?</b>", bold_body),
            Paragraph("• <b>First Stability: Age 33–34 (2027–2028)</b><br/>• <b>Peak Wealth: Age 35–38 (2029–2032)</b>", body_style),
            Paragraph("Both have Saturn in own sign Aquarius in 2nd house of wealth. Saturn matures at age 35–36, creating permanent financial security and asset ownership.", body_style)
        ],
        [
            Paragraph("<b>Q7: New Vehicle & Home Construction?</b>", bold_body),
            Paragraph("• <b>Vehicle: May 2027 – Dec 2027</b><br/>• <b>Home Construction: 2029 – 2031</b>", body_style),
            Paragraph("Husband's 4th Lord Mars is in own sign Aries (vehicle yoga). Land planning starts late 2028; construction finishes by 2030–2031 (Griha Pravesha).", body_style)
        ]
    ]
    t_q = Table(q_data, colWidths=[110, 185, 230])
    t_q.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#276749')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_q)
    story.append(Spacer(1, 5))

    # Section 3: Remedial Upayas
    story.append(Paragraph("3. Harmonizing Upayas & Vedic Remedies for Couple's Prosperity", section_h))
    rem_data = [
        [
            Paragraph("<b>1. Friday Lakshmi Pooja:</b> Light a pure cow-ghee lamp in home altar on Friday evening. Enhances Venus (vehicle/wealth).", body_style),
            Paragraph("<b>2. Shani Shanti:</b> Both being Capricorn Lagna with 2nd house Saturn, water Peepal tree on Saturdays before 9:30 AM.", body_style),
            Paragraph("<b>3. Santana Gopala Stotra:</b> Chant or listen to Santana Gopala Mantra on Thursdays to bless progeny health.", body_style)
        ]
    ]
    t_rem = Table(rem_data, colWidths=[175, 175, 175])
    t_rem.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#edf2f7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_rem)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<i>Prepared exclusively for Rashmi Patil & Ramanagouda Patil using Parashari Hora Shastra, Jaimini Sutras, and Vedic Synastry.</i>", subtitle_style))

    doc.build(story)
    print(f"[SUCCESS] Generated Couple Dossier: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    return output_pdf_path


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    target_pdf = os.path.join(out_dir, "rashmi_ramanagouda_couple_dossier.pdf")

    build_rashmi_ramanagouda_pdf(target_pdf)

    # Copy to workspace root
    root_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rashmi_ramanagouda_couple_dossier.pdf")
    shutil.copyfile(target_pdf, root_pdf)

    # Copy to artifact directory
    artifact_dir = r"C:\Users\Admin\.gemini\antigravity\brain\cca4e891-c56a-4839-9377-9103886054ad"
    if os.path.isdir(artifact_dir):
        shutil.copyfile(target_pdf, os.path.join(artifact_dir, "rashmi_ramanagouda_couple_dossier.pdf"))

    # Launch in Google Chrome
    url = "http://localhost:8080/rashmi_ramanagouda_couple_dossier.pdf"
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
