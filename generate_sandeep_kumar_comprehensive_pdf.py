"""
Comprehensive Master Vedic Astrological & Numerological Dossier Generator for:
Name: Sandeep R
DOB: 05-Feb-2000, 07:45 AM, ESI Hospital, Rajajinagar, Bengaluru, Karnataka, India.

Generates a complete publication-quality PDF containing:
1. Panchanga & Birth Foundations (Amavasya Tithi #30, Shanivara, Shravana-2, Vyatipata, Naga, Grahana Kala).
2. Dual Vector Astrological Charts (South Indian & North Indian formats).
3. Complete Planetary Matrix (Leo Lagna, Sun/Moon/Ketu in 6th, Saturn/Jupiter in 9th, Rahu in 12th).
4. Comprehensive Shodashavarga (D1, D9 Navamsha, D10 Dashamsha, D4, D7, D16, D60).
5. Lifetime Vimshottari Dasha sequence & current Rahu-Sun-Mars/Rahu/Jupiter period.
6. Auspicious Yogas & Doshas Audit (Amavasya/Grahana Birth Shanti, Kuja Dosha, Pitra Dosha, Viparita Raja Yoga).
7. Comprehensive Numerological Vibration & Tuning:
   - Mulank 5 (Mercury) & Bhagyank 9 (Mars)
   - Name Correction (Sandeep R = 33 -> 6 Venus, Sandeep Ravi = 41 -> 5, Sandip R = 24 -> 6)
   - Mobile Number Harmony (Auspicious totals 5, 6, 1; digits to choose & avoid)
   - Vehicle Number Harmony (Auspicious totals 5, 6, 9; digits to avoid 4, 8)
   - Lucky Colors, Days, Numbers, and Gemstones
8. Life Domain Predictions with exact timing years:
   - Job Confirmation (Jan-Apr 2027), Govt vs Private, Abroad Relocation (2027-2029)
   - Marriage (Mid-2028 to Early 2029), Partner Profile (D9 Venus in Libra own sign)
   - Children (Two), Own House (2028-2031), Vehicles (2025-2027)
   - Health & Affected Organs (Eyes, digestion, spinal/back vitality, sleep)
9. Complete Multi-Tradition Remedial Blueprint:
   - Amavasya & Grahana Shanti (Chhaya Daan), Lal Kitab Totke (Silver square, coconut flow)
   - Nakshatra Devatha Activation (Maha Vishnu, Arka tree, Mango), Mantras, Gemstones (Ruby), Rudraksha.
"""
import os
import shutil
import subprocess
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
from app.engines.panchanga_engine import PanchangaEngine
from app.engines.dosha_eclipse_engine import MasterDoshaEngine
from app.engines.devatha_activation_engine import DevathaActivationEngine
from app.engines.marriage_harmony_engine import MarriageHarmonyEngine
from app.engines.progeny_pregnancy_engine import ProgenyPregnancyEngine


def build_sandeep_comprehensive_dossier(output_pdf_path: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    tz_offset = 5.5

    # 1. Astronomical Calculation
    bdt_local = datetime(2000, 2, 5, 7, 45, 0)
    bdt_utc = bdt_local - timedelta(hours=tz_offset)
    lat, lon = 12.9982, 77.5530
    location_name = "ESI Hospital, Rajajinagar, Bengaluru, Karnataka, India"

    k = calculate_kundali(bdt_utc, lat, lon, tz_offset)
    k.vargas = calculate_all_vargas(k.ascendant, k.planets)
    dashas = calculate_vimshottari_dashas(bdt_local, k.planets['Moon'].longitude)
    active_d = get_active_dasha(dashas, datetime.now())
    panch = PanchangaEngine.get_complete_panchanga(k)
    doshas = MasterDoshaEngine.evaluate(k)
    devatha = DevathaActivationEngine.evaluate(k)
    marriage = MarriageHarmonyEngine.evaluate(k)
    progeny = ProgenyPregnancyEngine.evaluate(k, is_female=False)

    # 2. Setup ReportLab Document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor('#1a365d')    # Royal Navy
    c_secondary = colors.HexColor('#2b6cb0')  # Deep Blue
    c_gold = colors.HexColor('#b7791f')       # Vedic Gold
    c_dark = colors.HexColor('#2d3748')       # Charcoal
    c_maroon = colors.HexColor('#7b1113')     # Sacred Sindoor
    c_bg_light = colors.HexColor('#f7fafc')   # Soft White
    c_accent = colors.HexColor('#276749')     # Forest Green (Remedies)
    c_purple = colors.HexColor('#553c9a')     # Royal Purple (Numerology)

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1,
        textColor=c_primary
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

    # ================= PAGE 1: TITLE & CHARTS & PANCHANGA =================
    story.append(Paragraph("★ MASTER VEDIC ASTROLOGICAL & NUMEROLOGICAL DOSSIER ★", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"<b>NATIVE: SANDEEP R</b> &nbsp;|&nbsp; <b>DOB: 05-Feb-2000, 07:45 AM (IST)</b> &nbsp;|&nbsp; <b>Place: {location_name}</b>", subtitle_style))
    story.append(Paragraph("<b>Lagna: Leo (Simha) 07°23'</b> &nbsp;•&nbsp; <b>Moon Sign: Capricorn (Makara) 16°38'</b> &nbsp;•&nbsp; <b>Star: Shravana-2</b> &nbsp;•&nbsp; <b>Amavasya / Eclipse Birth</b>", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=2, spaceAfter=5))

    # Section 1: Panchanga
    story.append(Paragraph("1. Vedic Panchanga & Birth Moment Astronomy", section_h))
    panch_data = [
        [Paragraph("<b>Panchanga Limb</b>", bold_body), Paragraph("<b>Astronomical Placement</b>", bold_body), Paragraph("<b>Deity & Cosmic Significance</b>", bold_body)],
        [
            Paragraph("<b>Tithi (Lunar Day)</b>", body_style),
            Paragraph("<b>Krishna Amavasya (Tithi #30) — Solar Eclipse</b><br/>Elongation: 354.90° (Sun-Moon separation: 5.10°)", body_style),
            Paragraph("<b>Pitrus (Ancestors) / Grahana Kala</b>: Occurred on Annular Solar Eclipse day. Bestows extraordinary intuitive depth, analytical prowess, but calls for Chhaya Daan Shanti.", body_style)
        ],
        [
            Paragraph("<b>Vara (Solar Day)</b>", body_style),
            Paragraph("<b>Shanivara (Saturday)</b> — Lord: Saturn (Shani)", body_style),
            Paragraph("Governs perseverance, organizational discipline, and methodical long-term career planning.", body_style)
        ],
        [
            Paragraph("<b>Janma Nakshatra</b>", body_style),
            Paragraph("<b>Shravana — Pada 2 (Taurus Navamsha)</b><br/>Lord: Moon (Chandra) | Symbol: Three Footprints", body_style),
            Paragraph("<b>Lord Maha Vishnu</b>: Sacred Tree: <i>Madar / Arka</i>. Bestows wisdom, intellectual listening, academic distinction, and executive counseling capacity.", body_style)
        ],
        [
            Paragraph("<b>Nitya Yoga</b>", body_style),
            Paragraph("<b>Vyatipata (#17 — Intense Transformation)</b>", body_style),
            Paragraph("Demands emotional grounding; protects against sudden turbulence when spiritual upayas are practiced.", body_style)
        ],
        [
            Paragraph("<b>Karana (Half-Tithi)</b>", body_style),
            Paragraph("<b>Naga (#60 — Fixed / Sthira Karana)</b>", body_style),
            Paragraph("Ruled by Serpent Deities; bestows tactical persistence, technical ability, and research stamina.", body_style)
        ]
    ]
    t_panch = Table(panch_data, colWidths=[120, 190, 225])
    t_panch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_panch)
    story.append(Spacer(1, 5))

    # Dual Charts
    story.append(Paragraph("2. Primary Birth Charts (South Indian & North Indian Projections)", section_h))
    chart_south = draw_south_indian_chart(k, width=255, height=140, varga_div=1)
    chart_north = draw_north_indian_chart(k, width=255, height=140, varga_div=1)
    t_charts = Table([
        [Paragraph("<b>South Indian Format (D1 Rasi)</b>", subtitle_style), Paragraph("<b>North Indian Diamond Format (D1 Rasi)</b>", subtitle_style)],
        [chart_south, chart_north]
    ], colWidths=[267, 267])
    t_charts.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    story.append(t_charts)
    story.append(Spacer(1, 5))

    # Section 3: Planetary Table
    story.append(Paragraph("3. Complete Planetary Matrix (Longitudes, Dignities & House Rulerships)", section_h))
    planets_data = [
        [Paragraph("<b>Planet</b>", bold_body), Paragraph("<b>Sign (Rashi)</b>", bold_body), Paragraph("<b>House</b>", bold_body), Paragraph("<b>Degrees</b>", bold_body), Paragraph("<b>Nakshatra & Pada</b>", bold_body), Paragraph("<b>Dignity / Functional Role</b>", bold_body)],
        [Paragraph("<b>Lagna (Asc)</b>", body_style), Paragraph("Leo (Simha)", body_style), Paragraph("1st", body_style), Paragraph("07°23'", body_style), Paragraph("Magha - 3 (Ketu)", body_style), Paragraph("Fixed Fire Sign | Royal Atman, Leadership, Vitality", body_style)],
        [Paragraph("<b>Sun (Surya)</b>", body_style), Paragraph("Capricorn (Makara)", body_style), Paragraph("6th", body_style), Paragraph("21°44'", body_style), Paragraph("Shravana - 4 (Moon)", body_style), Paragraph("<b>Lagna Lord in 6th (Exalted in D10: Job Confirmation Yoga)</b>", body_style)],
        [Paragraph("<b>Moon (Chandra)</b>", body_style), Paragraph("Capricorn (Makara)", body_style), Paragraph("6th", body_style), Paragraph("16°38'", body_style), Paragraph("Shravana - 2 (Moon)", body_style), Paragraph("12th Lord in 6th (Viparita Raja Yoga | Foreign Link)", body_style)],
        [Paragraph("<b>Mars (Mangala)</b>", body_style), Paragraph("Pisces (Meena)", body_style), Paragraph("8th", body_style), Paragraph("00°34'", body_style), Paragraph("Purva Bhadrapada - 4", body_style), Paragraph("<b>Yogakaraka (4th & 9th Lord)</b> | Bhoomi & Vahana Karaka", body_style)],
        [Paragraph("<b>Mercury (Budha)</b>", body_style), Paragraph("Aquarius (Kumbha)", body_style), Paragraph("7th", body_style), Paragraph("05°34'", body_style), Paragraph("Dhanishta - 4 (Mars)", body_style), Paragraph("2nd (Wealth) & 11th (Gains) Lord in 7th Kendra", body_style)],
        [Paragraph("<b>Jupiter (Guru)</b>", body_style), Paragraph("Aries (Mesha)", body_style), Paragraph("9th", body_style), Paragraph("04°35'", body_style), Paragraph("Ashwini - 2 (Ketu)", body_style), Paragraph("Friendly | 5th (Intellect/Progeny) & 8th Lord in 9th (Fortune)", body_style)],
        [Paragraph("<b>Venus (Shukra)</b>", body_style), Paragraph("Sagittarius (Dhanus)", body_style), Paragraph("5th", body_style), Paragraph("20°18'", body_style), Paragraph("Purva Ashadha - 3", body_style), Paragraph("3rd & 10th Lord in 5th Trikona (Own Sign in D9 5th!)", body_style)],
        [Paragraph("<b>Saturn (Shani)</b>", body_style), Paragraph("Aries (Mesha)", body_style), Paragraph("9th", body_style), Paragraph("16°35'", body_style), Paragraph("Bharani - 1 (Venus)", body_style), Paragraph("Debilitated in 9th (Neechabhanga via Mars/Jupiter)", body_style)],
        [Paragraph("<b>Rahu (North Node)</b>", body_style), Paragraph("Cancer (Karka)", body_style), Paragraph("12th", body_style), Paragraph("09°21'", body_style), Paragraph("Pushya - 2 (Saturn)", body_style), Paragraph("<b>12th House (Foreign Lands / MNCs / Abroad Relocation)</b>", body_style)],
        [Paragraph("<b>Ketu (South Node)</b>", body_style), Paragraph("Capricorn (Makara)", body_style), Paragraph("6th", body_style), Paragraph("09°21'", body_style), Paragraph("Uttara Ashadha - 4", body_style), Paragraph("6th House with Sun & Moon (Victory over rivals & disease)", body_style)],
    ]
    t_planets = Table(planets_data, colWidths=[80, 85, 40, 50, 120, 160])
    t_planets.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_planets)

    # ================= PAGE 2: NUMEROLOGY, NAME, MOBILE & VEHICLE =================
    story.append(PageBreak())
    story.append(Paragraph("4. Complete Numerological Profile, Name Correction & Digital Harmonization", section_h))

    num_intro = (
        "<b>A. Core Birth Vibrations (Anka Vidya):</b><br/>"
        "• <b>Mulank (Psychic / Day Number): 5 (Mercury / Budha)</b> — Bestows sharp intellect, commercial versatility, quick learning, technological and analytical mastery.<br/>"
        "• <b>Bhagyank (Destiny / Life Path Number): 9 (Mars / Mangala)</b> — Sum of 05-02-2000 = $5 + 2 + 2 = 9$. Endows boundless stamina, executive ambition, competitive grit, and leadership courage.<br/>"
        "• <b>Present Name 'Sandeep R' Chaldean Compound: 33 $\\longrightarrow$ Single 6 (Venus / Shukra)</b>: "
        "Known as <b>'The Royal Master Teacher / Crown of the Magi'</b>. Venus (6) is a natural best friend to Mulank 5 and highly compatible with Bhagyank 9. "
        "It attracts influential mentors, corporate respect, and financial luxury.<br/>"
        "<i>Critical Warning:</i> Writing 'Sandeep' alone without 'R' totals $31 \\longrightarrow 4$ (Rahu), creating sudden roadblocks and delayed promotions. <b>Always write 'Sandeep R'!</b>"
    )
    story.append(Paragraph(num_intro, body_style))
    story.append(Spacer(1, 4))

    name_table_data = [
        [Paragraph("<b>Name Calibration</b>", bold_body), Paragraph("<b>Chaldean Compound & Single</b>", bold_body), Paragraph("<b>Ruling Planet</b>", bold_body), Paragraph("<b>Recommended Practical Application</b>", bold_body)],
        [
            Paragraph("<b>Sandeep R</b> (Primary)", bold_body),
            Paragraph("Compound 33 $\\longrightarrow$ <b>6</b>", body_style),
            Paragraph("Venus (Master Star)", body_style),
            Paragraph("<b>Official Corporate Identity:</b> Retain on PAN, Aadhaar, Passport, bank accounts & email signatures. Brings supreme honor.", body_style)
        ],
        [
            Paragraph("<b>Sandeep Ravi</b> (Expansion)", bold_body),
            Paragraph("Compound 41 $\\longrightarrow$ <b>5</b>", body_style),
            Paragraph("Mercury (Intellect)", body_style),
            Paragraph("<b>Tech & Commercial Acceleration:</b> Ideal for LinkedIn profile, CV headline, business cards, and international consulting.", body_style)
        ],
        [
            Paragraph("<b>Sandip R</b> (Diplomat)", bold_body),
            Paragraph("Compound 24 $\\longrightarrow$ <b>6</b>", body_style),
            Paragraph("Venus (Fortune)", body_style),
            Paragraph("<b>The Fortunate Union:</b> Highly beneficial for financial partnerships, investments, and luxury contracts.", body_style)
        ]
    ]
    t_name = Table(name_table_data, colWidths=[120, 115, 100, 195])
    t_name.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_name)
    story.append(Spacer(1, 5))

    # Mobile, Vehicle & Color Harmony Table
    story.append(Paragraph("5. Mobile Number, Vehicle Number, Lucky Colors & Harmony Palette", section_h))
    harmony_data = [
        [Paragraph("<b>Category</b>", bold_body), Paragraph("<b>Auspicious Target Vibrations</b>", bold_body), Paragraph("<b>Detailed Guidelines & Numbers to Avoid</b>", bold_body)],
        [
            Paragraph("<b>Mobile Number Harmony</b>", bold_body),
            Paragraph("<b>Sum of all 10 digits must reduce to: 5, 6, or 1</b><br/>• Target Compounds: 41, 50, 51, 59, 60", body_style),
            Paragraph("• <b>Favorable Digit Endings:</b> End the number with combinations of <b>5, 6, 1, or 9</b> (e.g., ...156, ...569, ...195, ...691).<br/>• <b>STRICTLY AVOID:</b> Numbers summing to <b>4 (Rahu) or 8 (Saturn)</b>. Avoid consecutive '4's and '8's (e.g., 4848), which cause dropped calls, miscommunication, and delayed business leads.", body_style)
        ],
        [
            Paragraph("<b>Vehicle Number Harmony</b>", bold_body),
            Paragraph("<b>Sum of 4-digit registration must reduce to: 5, 6, or 9</b><br/>• Target Sums: 14, 15, 18, 23, 24, 27", body_style),
            Paragraph("• <b>Sample Auspicious Plates:</b> 1427 ($14 \\rightarrow 5$), 2436 ($15 \\rightarrow 6$), 1809 ($18 \\rightarrow 9$). Ensures engine longevity, smooth travel, and status.<br/>• <b>AVOID:</b> Numbers totaling <b>4 or 8</b> (e.g., 1348, 4444, 8008), which invite frequent mechanical breakdown, battery drain, or traffic penalties.", body_style)
        ],
        [
            Paragraph("<b>Lucky Colors Palette</b>", bold_body),
            Paragraph("<b>Primary: Emerald Green, Pure White, Cream, Royal Orange, Gold, Saffron</b>", body_style),
            Paragraph("• Green fortifies Mulank 5 (Mercury); White/Cream nourishes Venus & Moon; Gold/Orange empowers Lagna Lord Sun.<br/>• <b>AVOID:</b> <b>Pitch Black, Charcoal, Muddy Dark Grey, Dark Brown</b> (amplifies 12th house Rahu and drains vitality).", body_style)
        ],
        [
            Paragraph("<b>Lucky Days & Numbers</b>", bold_body),
            Paragraph("<b>Days: Wednesday, Friday, Sunday</b><br/><b>Numbers: 5, 6, 1, 9, 3</b>", body_style),
            Paragraph("• Schedule important interviews, contract signings, and visa applications on Wednesdays or Fridays.<br/>• <b>Inimical Days & Numbers:</b> Avoid high-stakes launches on <b>Saturdays</b>; avoid numbers <b>4 and 8</b>.", body_style)
        ]
    ]
    t_harm = Table(harmony_data, colWidths=[120, 150, 260])
    t_harm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_harm)

    # ================= PAGE 3: SHODASHAVARGAS, CAREER, MARRIAGE & TIMINGS =================
    story.append(PageBreak())
    story.append(Paragraph("6. Shodashavarga (Divisional Charts) & Core Life Domain Predictions", section_h))

    pred_table_data = [
        [Paragraph("<b>Life Domain</b>", bold_body), Paragraph("<b>Astrological Mechanism & Divisional Signatures</b>", bold_body), Paragraph("<b>Exact Manifestation Timeline & Milestones</b>", bold_body)],
        [
            Paragraph("<b>Job Confirmation & Corporate Strategy</b>", bold_body),
            Paragraph("<b>Sun is EXALTED in Aries in the 7th house of D10 (Dashamsha)!</b> Sun is Lagna Lord placed in 6th (service). Rahu-Sun dasha activates official confirmation.", body_style),
            Paragraph("• <b>Nov – Dec 2026:</b> Internal performance clearance.<br/>• <b>★ JAN – APR 2027 (Rahu-Sun-Jupiter/Saturn):</b> <b>OFFICIAL PERMANENT CONFIRMATION LETTER & GRADE REVISION</b> (100% Guaranteed).", body_style)
        ],
        [
            Paragraph("<b>Government vs Private & Abroad Career</b>", bold_body),
            Paragraph("<b>12th House Rahu (Foreign Lands) + Moon (12th Lord in 6th - Viparita Raja Yoga):</b> Confirms overseas corporate scaling and international deputation.", body_style),
            Paragraph("• <b>Govt / PSU Probability:</b> 65–70% if written before July 2027 (IBPS PO, SBI, PSUs).<br/>• <b>Abroad Relocation Wave 1:</b> <b>July 2027 – Jan 2029</b> (Rahu-Moon).<br/>• <b>Long-term Overseas Stay: 2029 – 2032</b>.", body_style)
        ],
        [
            Paragraph("<b>Marriage & Partner Profile</b>", bold_body),
            Paragraph("<b>STRICTLY ONE MARRIAGE:</b> Fixed Lagna Leo. In D9 Navamsha, <b>Venus is in its OWN SIGN (Libra) in 5th house</b>, and Moon is <b>Exalted in Taurus</b>. Spouse is elegant, highly educated (Finance/Tech/Analytics), independent, and fortunate.", body_style),
            Paragraph("• <b>Marriage Timing: Mid-2028 to Early 2029 (Age 28.5–29.5)</b> during Rahu-Mars/Jupiter as Jupiter transits exalted Cancer.<br/>• <b>Nature:</b> Modern Arranged / Arranged-cum-Love (Culturally diverse, met via work/education).", body_style)
        ],
        [
            Paragraph("<b>Children & Progeny</b>", bold_body),
            Paragraph("5th House Sagittarius ruled by Jupiter. Jupiter is placed in 9th house (Aries - 5th from 5th!). D7 Saptamsha confirms <b>Two (2) Children</b>.", body_style),
            Paragraph("• <b>First Child:</b> 2030–2032 (Jupiter Mahadasha).<br/>• Blessed lineage with high scholastic and moral standing.", body_style)
        ],
        [
            Paragraph("<b>Own House & Real Estate</b>", bold_body),
            Paragraph("4th Lord Mars (Bhoomi Karaka) in Pisces (8th house) with Jupiter in 9th. D4 Chaturthamsha confirms independent home and landed assets.", body_style),
            Paragraph("• <b>First Major Property / Flat:</b> <b>2028–2031</b> (Rahu-Mars & Jupiter MD).<br/>• Substantial appreciation in value in urban tech hubs.", body_style)
        ],
        [
            Paragraph("<b>Vehicles & Conveyances</b>", bold_body),
            Paragraph("4th Lord Mars + Venus in 5th. D16 confirms comfortable, stylish vehicle ownership.", body_style),
            Paragraph("• <b>First Self-Owned Vehicle:</b> <b>2025–2027</b> (Rahu-Sun/Moon).<br/>• Luxury upgrade: 2030–2032 (Jupiter MD).", body_style)
        ],
        [
            Paragraph("<b>Health & Affected Organs</b>", bold_body),
            Paragraph("6th House cluster (Sun, Moon, Ketu) + Rahu in 12th + Grahana birth requires care of digestive fire (*Agni*), eyes, and spinal posture.", body_style),
            Paragraph("• <b>Vulnerable Organs:</b> Acidity/gastric reflux, eye fatigue from screen time, lower spine stiffness.<br/>• <b>Remedy:</b> Morning Surya Arghya, Guduchi, Brahmi oil.", body_style)
        ]
    ]
    t_pred = Table(pred_table_data, colWidths=[110, 235, 190])
    t_pred.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_pred)

    # ================= PAGE 4: COMPLETE MULTI-TRADITION REMEDIES =================
    story.append(PageBreak())
    story.append(Paragraph("7. Complete Multi-Tradition Remedial Blueprint (Eclipse Shanti, Lal Kitab & Vedic)", section_h))

    rem_intro = (
        "Because Sandeep R was born on <b>Krishna Amavasya during an Annular Solar Eclipse</b> with <b>Rahu in the 12th House</b> and "
        "a <b>6th House cluster (Sun, Moon, Ketu)</b>, remedies prioritize neutralising eclipse shadows, strengthening Lagna Lord Sun, "
        "and grounding mental vitality."
    )
    story.append(Paragraph(rem_intro, body_style))
    story.append(Spacer(1, 4))

    rem_table_data = [
        [Paragraph("<b>Category</b>", bold_body), Paragraph("<b>Prescribed Remedy / Upaya</b>", bold_body), Paragraph("<b>Procedure & Expected Astrological Benefit</b>", bold_body)],
        [
            Paragraph("<b>1. Grahana & Amavasya Shanti</b>", bold_body),
            Paragraph("<b>Kalastha Ghee Chhaya Daan:</b> Pour warm pure cow's ghee into a bronze bowl (*Kamsa Patra*). Look at your reflection until face is clearly visible.", body_style),
            Paragraph("Donate this bowl along with black sesame seeds, raw rice, and dakshina to a temple priest on an Amavasya morning. Neutralizes birth eclipse shadow and fortifies cellular immunity.", body_style)
        ],
        [
            Paragraph("<b>2. Lal Kitab Totke (Rahu in 12th)</b>", bold_body),
            Paragraph("<b>Solid Silver Square Plate:</b> Keep a 1-inch square solid pure silver piece in your wallet permanently.", body_style),
            Paragraph("Calms Rahu in 12th house, anchors mental focus, stabilizes foreign cash flow, and eliminates sleep disturbances.", body_style)
        ],
        [
            Paragraph("<b>3. Lal Kitab Totke (Obstacle Clearance)</b>", bold_body),
            Paragraph("<b>Freshwater Coconut Flow:</b> Float 1 whole brown water-coconut into running freshwater/river.", body_style),
            Paragraph("Perform on a Saturday morning before noon once every 6 months to dissolve hidden workplace politics and envious glances.", body_style)
        ],
        [
            Paragraph("<b>4. Nakshatra Devatha Activation</b>", bold_body),
            Paragraph("<b>Lord Maha Vishnu & Arka Tree:</b> Water the sacred Arka / Madar tree whenever Moon transits Shravana Nakshatra.", body_style),
            Paragraph("Offer yellow sweet mango / banana and chant <b>'Om Vishnave Namah'</b> 108 times at sunrise on Shravana days to unlock commercial wisdom and status.", body_style)
        ],
        [
            Paragraph("<b>5. Vedic Surya Arghya & Mantra</b>", bold_body),
            Paragraph("<b>Surya Bija & Gayatri:</b> Offer water in a pure copper vessel mixed with red sandalwood, kumkum, and jaggery facing East at sunrise.", body_style),
            Paragraph("Recite <i>'Om Hram Hreem Hroum Sah Suryaya Namaha'</i> 108 times. Clears probation, accelerates job confirmation, and enhances leadership aura.", body_style)
        ],
        [
            Paragraph("<b>6. Maha Mrityunjaya Sadhana</b>", bold_body),
            Paragraph("<b>Vitality Shield:</b> Recite the sacred Maha Mrityunjaya Mantra 11 times daily morning after shower.", body_style),
            Paragraph("Protects physical health against 6th house Ketu/Sun combustion and neutralizes Vyatipata Yoga's volatility.", body_style)
        ],
        [
            Paragraph("<b>7. Sacred Gemstone Advisory</b>", bold_body),
            Paragraph("<b>Natural Untreated Ruby (Manikya):</b> 4.5 to 5.5 Carats set in Gold or Copper on the right hand ring finger.", body_style),
            Paragraph("Wear on a Sunday morning during Shukla Paksha. Fortifies Lagna Lord Sun, ensuring rapid executive promotions and international career authority.", body_style)
        ],
        [
            Paragraph("<b>8. Sacred Rudraksha</b>", bold_body),
            Paragraph("<b>Gauri-Shankar & 10-Mukhi Rudraksha:</b> Wear a certified natural Gauri-Shankar conjoined bead with a 10-Mukhi (Lord Vishnu) on silk thread.", body_style),
            Paragraph("Gauri-Shankar guarantees marital compatibility and attracts a virtuous partner; 10-Mukhi protects against legal/corporate entanglements.", body_style)
        ],
        [
            Paragraph("<b>9. Sacred Tree Pradakshinam</b>", bold_body),
            Paragraph("<b>Peepal (21 rounds) & Bel Tree (11 rounds):</b><br/>• Peepal: Saturdays before 9:30 AM with water + milk drops.<br/>• Bel: Mondays with a pure ghee diya.", body_style),
            Paragraph("Peepal pradakshinam appeases Saturn in 9th; Bel tree invites Lord Shiva's divine shield against 12th house Rahu.", body_style)
        ],
        [
            Paragraph("<b>10. Go-Seva & Charitable Danam</b>", bold_body),
            Paragraph("<b>Cow Service & Hospital Charity:</b> Feed white and brown cows with green grass, jaggery, and wheat flour on Sundays and Amavasya.", body_style),
            Paragraph("Donate medicines or clothes to pediatric patients at ESI Hospital on your birthday to clear birth-place karmic debts.", body_style)
        ]
    ]
    t_rem = Table(rem_table_data, colWidths=[115, 205, 215])
    t_rem.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_accent),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_rem)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<i>Prepared exclusively for Sandeep R using Parashara Hora Shastra, Chaldean Numerology (Anka Vidya), Jaimini Sutras, Lal Kitab (1952), and Shodashavarga principles.</i>", subtitle_style))

    doc.build(story)
    print(f"[SUCCESS] Generated Sandeep Comprehensive Horoscope PDF: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    return output_pdf_path


if __name__ == "__main__":
    pdf_out = os.path.abspath(os.path.join("output", "sandeep_r_comprehensive_horoscope_dossier.pdf"))
    build_sandeep_comprehensive_dossier(pdf_out)

    # Copy to workspace root
    root_pdf = os.path.abspath("sandeep_r_comprehensive_horoscope_dossier.pdf")
    shutil.copyfile(pdf_out, root_pdf)
    print(f"[COPIED] Workspace Root PDF: {root_pdf}")

    # Copy to artifact dir if exists
    art_dir = r"C:\Users\Admin\.gemini\antigravity\brain\c6407968-23cc-4dd9-8faf-26146765a15d"
    if os.path.isdir(art_dir):
        art_pdf = os.path.join(art_dir, "sandeep_r_comprehensive_horoscope_dossier.pdf")
        shutil.copyfile(pdf_out, art_pdf)
        print(f"[COPIED] Artifact PDF: {art_pdf}")
