"""
Comprehensive Master Vedic Astrological Dossier Generator for:
Name: Ravi Kumar S
DOB: 20-Nov-1968, 03:45 AM, K.C. General Hospital, Malleswaram, Bengaluru, Karnataka, India.

Generates a complete publication-quality PDF containing:
1. Panchanga & Birth Foundations (Amavasya Tithi #30, Mangalavara, Vishakha-3, Shobhana, Naga).
2. Dual Vector Astrological Charts (South Indian & North Indian formats).
3. Complete Planetary Matrix with speeds, dignities, and functional natures.
4. Comprehensive Shodashavarga (D1, D9, D10, D4, D7, D16, D60) evaluations.
5. Lifetime Vimshottari Dasha sequence & active Venus-Rahu-Ketu/Venus breakdown.
6. Auspicious Yogas & Doshas Audit (Amavasya Janma Dosha, Kuja Dosha, Shani-Rahu Yoga).
7. Life Domain Predictions with exact timing years:
   - Education, Profession/Career Peak, Marriage (Strictly One), Children (Two),
     Own House (2004-2007, 2018-2020, 2027-2030), Conveyances / 4-Wheeler Diagnosis (2028-2029 Window),
     Health & Affected Organs.
8. Complete Remedial Blueprint:
   - Amavasya Janma Shanti (Kalastha Ghee Chhaya Daan, Pitru Tarpanam).
   - Lal Kitab Upayas (Silver plate, sealed river water pot, dog seva).
   - Nakshatra & Tithi Devatha Activation (Indragni, Kaitha tree, Wood Apple).
   - Vedic Mantras, Gemstones (Yellow Sapphire + Silver Kada), Rudraksha (5-Mukhi & Gauri-Shankar), Go-Seva.
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
from app.engines.progeny_pregnancy_engine import ProgenyPregnancyEngine
from app.engines.devatha_activation_engine import DevathaActivationEngine
from app.engines.dosha_eclipse_engine import MasterDoshaEngine
from app.engines.marriage_harmony_engine import MarriageHarmonyEngine


def build_ravi_kumar_comprehensive_dossier(output_pdf_path: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    tz_offset = 5.5

    # 1. Astronomical Calculation
    bdt_local = datetime(1968, 11, 20, 3, 45, 0)
    bdt_utc = bdt_local - timedelta(hours=tz_offset)
    lat, lon = 13.0068, 77.5713
    location_name = "KC General Hospital, Malleswaram, Bengaluru, Karnataka, India"

    k = calculate_kundali(bdt_utc, lat, lon, tz_offset)
    k.vargas = calculate_all_vargas(k.ascendant, k.planets)
    dashas = calculate_vimshottari_dashas(bdt_local, k.planets['Moon'].longitude)
    active_d = get_active_dasha(dashas, datetime.now())
    panch = PanchangaEngine.get_complete_panchanga(k)
    doshas = MasterDoshaEngine.evaluate(k)
    devatha = DevathaActivationEngine.evaluate(k)
    marriage = MarriageHarmonyEngine.evaluate(k)
    progeny = ProgenyPregnancyEngine.evaluate(k, is_female=False)

    # 2. Document Setup
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
    c_secondary = colors.HexColor('#2b6cb0')  # Deep Sky Blue
    c_gold = colors.HexColor('#b7791f')       # Vedic Gold
    c_dark = colors.HexColor('#2d3748')       # Charcoal Body Text
    c_maroon = colors.HexColor('#7b1113')     # Sacred Sindoor
    c_bg_light = colors.HexColor('#f7fafc')   # Soft White
    c_accent = colors.HexColor('#276749')     # Forest Green (Remedies)

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
    subhead_style = ParagraphStyle(
        'SubHead',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=c_secondary,
        spaceBefore=4,
        spaceAfter=2
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
    story.append(Paragraph("★ MASTER VEDIC ASTROLOGICAL DOSSIER: COMPREHENSIVE HOROSCOPE ★", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"<b>NATIVE: RAVI KUMAR S</b> &nbsp;|&nbsp; <b>DOB: 20-Nov-1968, 03:45 AM (IST)</b> &nbsp;|&nbsp; <b>Place: {location_name}</b>", subtitle_style))
    story.append(Paragraph("<b>Lagna: Pisces (Meena) 26°37'</b> &nbsp;•&nbsp; <b>Moon Sign: Libra (Tula) 28°26'</b> &nbsp;•&nbsp; <b>Birth Star: Vishakha-3</b> &nbsp;•&nbsp; <b>Amavasya Tithi (#30)</b>", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=2, spaceAfter=5))

    # Section 1: Panchanga Table
    story.append(Paragraph("1. Vedic Panchanga (Five Cosmic Limbs of Time at Birth)", section_h))
    panch_data = [
        [Paragraph("<b>Panchanga Limb</b>", bold_body), Paragraph("<b>Astronomical Placement</b>", bold_body), Paragraph("<b>Deity & Cosmic Significance</b>", bold_body)],
        [
            Paragraph("<b>Tithi (Lunar Day)</b>", body_style),
            Paragraph("<b>Krishna Amavasya (Tithi #30 - New Moon)</b><br/>Elongation: 354.19° (Sun-Moon separation: 5.81°)", body_style),
            Paragraph("<b>Pitrus (Ancestors)</b>: Ksheena Chandra (Depleted Lunar Light). Grants deep intuition, occult research intellect, but delicate infant vitality.", body_style)
        ],
        [
            Paragraph("<b>Vara (Solar Day)</b>", body_style),
            Paragraph("<b>Mangalavara (Tuesday Night / Pre-Dawn Wednesday)</b>", body_style),
            Paragraph("<b>Mars (Mangala)</b>: Endows perseverance, moral bravery, and energetic resistance under pressure.", body_style)
        ],
        [
            Paragraph("<b>Janma Nakshatra</b>", body_style),
            Paragraph("<b>Vishakha (27 Constellations) — Pada 3</b><br/>Lord: Jupiter (Guru) | Navamsha: Gemini (Mithuna)", body_style),
            Paragraph("<b>Indragni (Indra + Agni)</b>: Sacred Tree: <i>Kaitha / Wood Apple</i>. Gives high ambition, executive mastery, and eloquence.", body_style)
        ],
        [
            Paragraph("<b>Nitya Yoga</b>", body_style),
            Paragraph("<b>Shobhana (#5 — Auspicious Benefic)</b>", body_style),
            Paragraph("Endows natural charisma, social goodwill, artistic taste, and virtuous speech.", body_style)
        ],
        [
            Paragraph("<b>Karana (Half-Tithi)</b>", body_style),
            Paragraph("<b>Naga (#60 — Fixed / Sthira Karana)</b>", body_style),
            Paragraph("Ruled by Serpent Deities; bestows tactical wisdom, patience, and victory in competitive affairs.", body_style)
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

    # Dual Charts (South Indian & North Indian)
    story.append(Paragraph("2. Primary Birth Charts (South Indian & North Indian Vector Projections)", section_h))
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
        [Paragraph("<b>Lagna (Asc)</b>", body_style), Paragraph("Pisces (Meena)", body_style), Paragraph("1st", body_style), Paragraph("26°37'", body_style), Paragraph("Revati - 3 (Mercury)", body_style), Paragraph("Dual Water Sign | Soul & Physical Foundation", body_style)],
        [Paragraph("<b>Sun (Surya)</b>", body_style), Paragraph("Scorpio (Vrischika)", body_style), Paragraph("9th", body_style), Paragraph("04°15'", body_style), Paragraph("Anuradha - 1 (Saturn)", body_style), Paragraph("Friendly | 6th Lord in 9th (Viparita Bhagya)", body_style)],
        [Paragraph("<b>Moon (Chandra)</b>", body_style), Paragraph("Libra (Tula)", body_style), Paragraph("8th", body_style), Paragraph("28°26'", body_style), Paragraph("Vishakha - 3 (Jupiter)", body_style), Paragraph("Neutral (Ksheena Amavasya) | 5th Lord in 8th", body_style)],
        [Paragraph("<b>Mars (Mangala)</b>", body_style), Paragraph("Virgo (Kanya)", body_style), Paragraph("7th", body_style), Paragraph("13°32'", body_style), Paragraph("Hasta - 2 (Moon)", body_style), Paragraph("Enemy | 2nd & 9th Lord in 7th (Kuja Dosha)", body_style)],
        [Paragraph("<b>Mercury (Budha)</b>", body_style), Paragraph("Libra (Tula)", body_style), Paragraph("8th", body_style), Paragraph("24°40'", body_style), Paragraph("Vishakha - 2 (Jupiter)", body_style), Paragraph("Neutral | 4th (Property) & 7th (Marriage) Lord in 8th", body_style)],
        [Paragraph("<b>Jupiter (Guru)</b>", body_style), Paragraph("Virgo (Kanya)", body_style), Paragraph("7th", body_style), Paragraph("07°40'", body_style), Paragraph("Uttara Phalguni - 4", body_style), Paragraph("<b>Lagna & 10th Lord in 7th Kendra (Guru-Mangala Yoga)</b>", body_style)],
        [Paragraph("<b>Venus (Shukra)</b>", body_style), Paragraph("Sagittarius (Dhanus)", body_style), Paragraph("10th", body_style), Paragraph("12°29'", body_style), Paragraph("Moola - 4 (Ketu)", body_style), Paragraph("<b>10th House Occupant (Amala Yoga) | Current MD Lord</b>", body_style)],
        [Paragraph("<b>Saturn (Shani)</b>", body_style), Paragraph("Pisces (Meena)", body_style), Paragraph("1st", body_style), Paragraph("26°43'", body_style), Paragraph("Revati - 4 (Mercury)", body_style), Paragraph("Neutral | 11th & 12th Lord in Lagna (High Discipline)", body_style)],
        [Paragraph("<b>Rahu (North Node)</b>", body_style), Paragraph("Pisces (Meena)", body_style), Paragraph("1st", body_style), Paragraph("13°25'", body_style), Paragraph("Uttara Bhadrapada - 4", body_style), Paragraph("Karmic Catalyst in Lagna (Deep Introspection)", body_style)],
        [Paragraph("<b>Ketu (South Node)</b>", body_style), Paragraph("Virgo (Kanya)", body_style), Paragraph("7th", body_style), Paragraph("13°25'", body_style), Paragraph("Hasta - 2 (Moon)", body_style), Paragraph("Spiritual detachment in 7th Kendra with Guru & Mars", body_style)],
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

    # ================= PAGE 2: SHODASHAVARGAS & DASHAS & YOGAS =================
    story.append(PageBreak())
    story.append(Paragraph("4. Shodashavarga (Divisional Charts) & Hidden Strengths Analysis", section_h))
    vargas_text = (
        "• <b>D9 Navamsha (Spouse, Dharma & Soul Capacity):</b> Navamsha Lagna is Aquarius (*Kumbha*). "
        "<b>Jupiter sits in its OWN SIGN PISCES (*Swakshetra*) in D9!</b> This provides extraordinary inner spiritual fortitude (*Vargottama-grade*). "
        "Saturn also sits in Pisces in D9, stabilizing mental peace. Venus is in Cancer, requiring domestic balance.<br/>"
        "• <b>D10 Dashamsha (Career, Authority & Public Eminence):</b> Dashamsha Lagna is Cancer (*Karka*). "
        "<b>Jupiter is EXALTED in Cancer in the 1st House conjoined with Moon in own sign (*Gajakesari & Hamsa Mahapurusha Yoga in D10*)!</b> "
        "Sun sits in its own sign Leo in the 2nd house. This guarantees high corporate/administrative authority, honor, and enduring professional leadership.<br/>"
        "• <b>D4 Chaturthamsha (Own House, Real Estate & Fixed Assets):</b> D4 Lagna is Sagittarius. "
        "<b>VENUS IS EXALTED IN PISCES IN THE 4TH HOUSE OF D4 (*Shukra in Uchha*)!</b> Lagna Lord Jupiter sits in Lagna. "
        "This confirms substantial independent property holdings, architectural luxury, and immovable asset creation.<br/>"
        "• <b>D7 Saptamsha (Children & Lineage):</b> D7 Lagna is Pisces. 5th Lord Moon conjoins Jupiter in Aries (2nd house of family), assuring two noble, successful children.<br/>"
        "• <b>D16 Shodashamsha (Vehicles & Conveyances Diagnostic):</b> D16 Lagna is Aquarius. While Saturn is in 1st, <b>Mars (vehicle karaka) is DEBILITATED in Cancer in the 6th house conjoined with Rahu, Ketu & Moon</b>. Combined with natal 4th Lord Mercury in the 8th house, this explains the absence of a 4-wheeler car to date (favoring practical two-wheelers/commute)."
    )
    story.append(Paragraph(vargas_text, body_style))
    story.append(Spacer(1, 5))

    # Section 5: Dasha Timeline
    story.append(Paragraph("5. Lifetime Vimshottari Dasha Sequence & Active Periods", section_h))
    dasha_summary = (
        f"<b>Born in Jupiter Mahadasha balance: 5 Years, 10 Months, 17 Days.</b><br/>"
        f"• <b>Jupiter MD (1968 - 1974):</b> Early infancy under grandfather's care.<br/>"
        f"• <b>Saturn MD (1974 - 1993):</b> Foundational education, discipline, structural mindset.<br/>"
        f"• <b>Mercury MD (1993 - 2010):</b> Higher learning, Marriage (03-May-1999), Children (2000-2005), and First Property (2004-2007).<br/>"
        f"• <b>Ketu MD (2010 - 2017):</b> Career re-calibration, spiritual introspections.<br/>"
        f"• <b>VENUS MAHADASHA (07-Oct-2017 to 07-Oct-2037 — ACTIVE NOW):</b> Golden period for worldly achievements, asset creation, and authority.<br/>"
        f"&nbsp;&nbsp;&nbsp;» <b>Current Running Antardasha: VENUS - RAHU (06-Dec-2024 to 07-Dec-2027)</b>: High commercial expansion, network growth.<br/>"
        f"&nbsp;&nbsp;&nbsp;» <b>Upcoming Pinnacle: VENUS - JUPITER (07-Dec-2027 to 07-Aug-2030)</b>: Highest wealth, property peak, children's elevation.<br/>"
        f"• <b>Sun MD (2037 - 2043) & Moon MD (2043 - 2053):</b> Advisory roles, spiritual legacy, and family fulfillment."
    )
    story.append(Paragraph(dasha_summary, body_style))
    story.append(Spacer(1, 5))

    # Section 6: Yogas & Doshas Audit
    story.append(Paragraph("6. Auspicious Yogas & Astrological Doshas Audit", section_h))
    yd_data = [
        [Paragraph("<b>Astrological Yoga / Dosha</b>", bold_body), Paragraph("<b>Presence in Chart</b>", bold_body), Paragraph("<b>Shastric Impact & Cancellation Status</b>", bold_body)],
        [
            Paragraph("<b>Guru-Mangala Yoga</b>", bold_body),
            Paragraph("<b>PRESENT (7th House)</b><br/>Jupiter conjunct Mars", body_style),
            Paragraph("<b>HIGHLY AUSPICIOUS:</b> Gives unyielding moral courage, organizational authority, and protective matrimonial alliance.", body_style)
        ],
        [
            Paragraph("<b>Amala Yoga</b>", bold_body),
            Paragraph("<b>PRESENT (10th House)</b><br/>Benefic Venus in 10th", body_style),
            Paragraph("<b>CAREER EMINENCE:</b> Gives an unblemished professional reputation, social respect, and prosperity through ethical commerce.", body_style)
        ],
        [
            Paragraph("<b>Amavasya Janma Dosha</b>", bold_body),
            Paragraph("<b>PRESENT (Tithi #30)</b><br/>Moon within 5.8° of Sun", body_style),
            Paragraph("<b>REQUIRES SHANTI:</b> Ksheena Chandra (Depleted Lunar Prana). Early childhood fragility, emotional reserve, subconscious anxiety. Fully cured via Kalastha Ghee Chhaya Daan.", body_style)
        ],
        [
            Paragraph("<b>Kuja / Manglik Dosha</b>", bold_body),
            Paragraph("<b>Present in 7th House</b><br/>Mars in Virgo", body_style),
            Paragraph("<b>100% CANCELLED:</b> Neutralized by Lagna Lord Jupiter's conjunction in D1 and balanced by wife Amudha's 1st house Mars (*Kuja Dosha Samyam*).", body_style)
        ],
        [
            Paragraph("<b>Shani-Rahu in Lagna</b>", bold_body),
            Paragraph("<b>PRESENT in Pisces Lagna</b><br/>Saturn + Rahu", body_style),
            Paragraph("<b>PSYCHOLOGICAL STATIC:</b> Tendency to overthink, carry excessive family responsibility, sleep restlessness; pacified by pure solid silver.", body_style)
        ],
        [
            Paragraph("<b>Kala Sarpa Yoga</b>", bold_body),
            Paragraph("<b>ABSENT (0% Affliction)</b>", body_style),
            Paragraph("Planets are distributed across the zodiac; no nodal entrapment.", body_style)
        ]
    ]
    t_yd = Table(yd_data, colWidths=[120, 140, 275])
    t_yd.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7b1113')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_yd)

    # ================= PAGE 3: PREDICTIONS & TIMING =================
    story.append(PageBreak())
    story.append(Paragraph("7. Comprehensive Life Predictions & Exact Timing of Milestones", section_h))

    pred_table_data = [
        [Paragraph("<b>Life Domain</b>", bold_body), Paragraph("<b>Astrological Analysis & Promise</b>", bold_body), Paragraph("<b>Exact Manifestation Years & Milestones</b>", bold_body)],
        [
            Paragraph("<b>Education & Learning</b>", bold_body),
            Paragraph("4th Lord Mercury in 8th with Moon; 5th House Cancer. Schooling under Saturn MD imparted deep focus, discipline, and practical technical competence.", body_style),
            Paragraph("• <b>1974–1986:</b> Schooling under Saturn MD.<br/>• <b>1987–1993:</b> Higher technical / commercial studies under Saturn-Jupiter & Saturn-Mercury.", body_style)
        ],
        [
            Paragraph("<b>Profession & Career Trajectory</b>", bold_body),
            Paragraph("10th Lord Jupiter in 7th Kendra; Venus in 10th (Amala Yoga); Exalted Jupiter & Moon in D10. Excels in business operations, administration, strategy, and advisory governance.", body_style),
            Paragraph("• <b>1993–2010:</b> Steady corporate climb.<br/>• <b>2017–2037:</b> Golden 20-year Venus MD.<br/>• <b>2024–2027:</b> High commercial networking.<br/>• <b>Dec 2027 – Aug 2030 (Venus-Jupiter): PINNACLE PEAK</b>.", body_style)
        ],
        [
            Paragraph("<b>Marriage & Matrimony</b>", bold_body),
            Paragraph("<b>STRICTLY ONE LIFELONG MARRIAGE:</b> Lagna Lord Jupiter in 7th Kendra protects marital sanctity through Dharma. Wife Amudha has Exalted Jupiter in 2nd from Upapada Lagna.", body_style),
            Paragraph("• <b>Solemnized on: 03-May-1999</b> (Age 30).<br/>• Manifested in exact <b>Mercury MD - Venus AD</b> (7th Lord MD + Kalatrakaraka AD). 27+ years of resilient bond.", body_style)
        ],
        [
            Paragraph("<b>Children & Progeny</b>", bold_body),
            Paragraph("5th House Cancer; D7 Moon conjunct Jupiter in 2nd house confirms <b>Two (2) Children (1 Son, 1 Daughter)</b>. 5th Lord in 8th caused early conception anxiety, overcome by grace.", body_style),
            Paragraph("• <b>First Child (Son):</b> Born 2000–2001 (Mercury-Sun/Moon).<br/>• <b>Second Child (Daughter):</b> Born 2003–2005 (Mercury-Mars/Rahu). Both high achievers.", body_style)
        ],
        [
            Paragraph("<b>Own House & Real Estate</b>", bold_body),
            Paragraph("<b>EXALTED VENUS IN 4TH HOUSE OF D4 (Chaturthamsha):</b> Assures prime independent residential and commercial real estate ownership.", body_style),
            Paragraph("• <b>First Own House:</b> Acquired in <b>2004–2007</b> (Mercury-Rahu/Jupiter).<br/>• <b>Major Upgrade:</b> <b>2018–2020</b> (Venus-Venus).<br/>• <b>Next Land / Real Estate Peak: Dec 2027 to Aug 2030</b>.", body_style)
        ],
        [
            Paragraph("<b>Vehicles & Conveyances<br/>(4-Wheeler Diagnosis)</b>", bold_body),
            Paragraph("<b>4th Lord Mercury in 8th House (Obstacles/Delays)</b> conjoined with Amavasya Moon; Saturn-Rahu in Lagna creates extreme caution/frugality. In D16, Mars is debilitated in 6th house with Rahu/Ketu, explaining absence of a 4-wheeler to date.", body_style),
            Paragraph("• <b>Past Periods:</b> 2002–2003 & 2019–2020 supported 2-wheelers/commute, <b>NOT 4-wheeler car</b>.<br/>• <b>Current Dasha:</b> Venus-Rahu (driving caution).<br/>• <b>Auspicious 4-Wheeler Window:</b> <b>2028–2029 (Venus-Jupiter)</b>.", body_style)
        ],
        [
            Paragraph("<b>Health & Affected Organs</b>", bold_body),
            Paragraph("Pisces Lagna (Feet/Lymphatics); Saturn-Rahu in 1st (Head/Nerves/Anxiety); Moon-Mercury in 8th (Kidneys/Groin/Lower Digestion); Mars-Ketu in 7th (Pitta heat/Liver/Acidity).", body_style),
            Paragraph("• <b>Vulnerable Organs:</b> Nervous system fatigue, acidity/bile, kidney hydration balance, ankle stiffness.<br/>• <b>Mitigation:</b> Brahmi oil head massage, cooling diet.", body_style)
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

    # ================= PAGE 4: COMPLETE REMEDIES BLUEPRINT =================
    story.append(PageBreak())
    story.append(Paragraph("8. Complete Remedial Blueprint (Amavasya Shanti, Lal Kitab & Vedic Upayas)", section_h))

    rem_intro = (
        "Because Ravi Kumar S was born on <b>Krishna Amavasya (New Moon Day)</b> with <b>Saturn and Rahu in Lagna</b> and "
        "<b>Moon in the 8th House</b>, remedies must specifically address lunar revitalization (*Chandra Posha*), ancestral peace (*Pitru Tattva*), "
        "and physical nervous grounding."
    )
    story.append(Paragraph(rem_intro, body_style))
    story.append(Spacer(1, 4))

    rem_table_data = [
        [Paragraph("<b>Category</b>", bold_body), Paragraph("<b>Prescribed Remedy / Upaya</b>", bold_body), Paragraph("<b>Procedure & Expected Astrological Benefit</b>", bold_body)],
        [
            Paragraph("<b>1. Amavasya Janma Shanti</b>", bold_body),
            Paragraph("<b>Kalastha Ghee Chhaya Daan:</b> Pour warm pure cow's ghee into a bronze bowl (*Kamsa Patra*). Look at your reflection until face is clearly seen.", body_style),
            Paragraph("Donate this bowl along with black sesame seeds, raw rice, and dakshina to a temple priest on an Amavasya morning. Neutralizes the birth eclipse shadow and restores cellular vitality.", body_style)
        ],
        [
            Paragraph("<b>2. Pitru Tarpanam</b>", bold_body),
            Paragraph("<b>Amavasya Water Offering:</b> Offer clean water mixed with black sesame seeds facing South every monthly New Moon day.", body_style),
            Paragraph("Pacifies the Tithi Devatha (Pitrus); clears subconscious guilt and unlocks uninterrupted professional progress.", body_style)
        ],
        [
            Paragraph("<b>3. Lal Kitab Totke (Moon in 8th)</b>", bold_body),
            Paragraph("<b>Sealed River Water Pot:</b> Keep sacred well water or flowing river water in a sealed pure silver pot in the home pooja room.", body_style),
            Paragraph("Never construct an underground water tank in the center of the house. Never donate pure milk on Monday nights. Touch mother's/elderly women's feet daily.", body_style)
        ],
        [
            Paragraph("<b>4. Lal Kitab Totke (Saturn-Rahu in 1st)</b>", bold_body),
            Paragraph("<b>Solid Silver Square Plate:</b> Keep a 1-inch square solid pure silver piece in your wallet or pocket at all times.", body_style),
            Paragraph("Grounds the mental static of Saturn-Rahu in Lagna. Avoid accepting free iron or electronic gifts. Float whole water coconuts in a river on Saturday afternoons.", body_style)
        ],
        [
            Paragraph("<b>5. Lal Kitab Totke (Mars-Ketu in 7th)</b>", bold_body),
            Paragraph("<b>Solid Silver Ball & Sweet Roti:</b> Carry a solid silver ball (Goli). Feed sweet rotis kneaded with jaggery to stray dogs on Tuesdays.", body_style),
            Paragraph("Pacifies fiery domestic temperaments and cools the 7th house martial energy.", body_style)
        ],
        [
            Paragraph("<b>6. Nakshatra Devatha Activation</b>", bold_body),
            Paragraph("<b>Indragni & Kaitha Tree Worship:</b> Water the Kaitha / Wood Apple or Bilva tree whenever Moon transits Vishakha Nakshatra.", body_style),
            Paragraph("Offer Wood Apple / Starfruit and recite <b>'Om Indragnibhyam Namah'</b> 108 times at sunrise on Vishakha days to awaken career ambition and leadership.", body_style)
        ],
        [
            Paragraph("<b>7. Vedic Mantra Sadhana</b>", bold_body),
            Paragraph("<b>Guru Beej & Maha Mrityunjaya:</b><br/>• Jupiter: <i>Om Gram Greem Graum Sah Gurave Namah</i> (108x Thursdays).<br/>• Maha Mrityunjaya: 11x daily morning.", body_style),
            Paragraph("Fortifies Lagna Lord Jupiter in 7th Kendra and establishes an impenetrable divine shield against health vulnerabilities.", body_style)
        ],
        [
            Paragraph("<b>8. Gemstones & Sacred Metals</b>", bold_body),
            Paragraph("<b>Yellow Sapphire (Pushparaja) + Silver Kada:</b><br/>• Natural Yellow Sapphire (4.5–5.5 carats) in Gold/Panchadhatu on right index finger on Thursday.<br/>• Pure Solid Silver Kada on right wrist.", body_style),
            Paragraph("Yellow Sapphire magnifies Jupiter's executive authority; pure silver on wrist acts as a biological capacitor soothing the Amavasya Moon and calming the nervous system.", body_style)
        ],
        [
            Paragraph("<b>9. Sacred Rudraksha</b>", bold_body),
            Paragraph("<b>5-Mukhi & Gauri-Shankar Rudraksha:</b> Wear a certified natural Gauri-Shankar bead conjoined with a 5-Mukhi bead around the neck on a white silk thread.", body_style),
            Paragraph("Gauri-Shankar harmonizes marital bliss and lunar energy; 5-Mukhi brings mental peace, blood pressure regulation, and spiritual wisdom.", body_style)
        ],
        [
            Paragraph("<b>10. Go-Seva & Hospital Danam</b>", bold_body),
            Paragraph("<b>Cow Service & Birthday Charity:</b> Feed cows green grass, jaggery, and boiled rice on Tuesdays and Amavasya. Donate medicines to a general hospital on your birthday.", body_style),
            Paragraph("Honors birth at K.C. General Hospital and dissolves lingering karmic medical debts.", body_style)
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

    story.append(Paragraph("<i>Prepared exclusively for Ravi Kumar S using authentic Brihat Parasara Hora Sastra, Jaimini Sutras, Lal Kitab (1952), and Shodashavarga principles.</i>", subtitle_style))

    doc.build(story)
    print(f"[SUCCESS] Generated Comprehensive Horoscope PDF: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    return output_pdf_path


if __name__ == "__main__":
    # Generate in output folder
    pdf_out = os.path.abspath(os.path.join("output", "ravi_kumar_comprehensive_horoscope_dossier.pdf"))
    build_ravi_kumar_comprehensive_dossier(pdf_out)

    # Copy to workspace root
    root_pdf = os.path.abspath("ravi_kumar_comprehensive_horoscope_dossier.pdf")
    shutil.copyfile(pdf_out, root_pdf)
    print(f"[COPIED] Workspace Root PDF: {root_pdf}")

    # Copy to artifact dir if exists
    art_dir = r"C:\Users\Admin\.gemini\antigravity\brain\c6407968-23cc-4dd9-8faf-26146765a15d"
    if os.path.isdir(art_dir):
        art_pdf = os.path.join(art_dir, "ravi_kumar_comprehensive_horoscope_dossier.pdf")
        shutil.copyfile(pdf_out, art_pdf)
        print(f"[COPIED] Artifact PDF: {art_pdf}")
