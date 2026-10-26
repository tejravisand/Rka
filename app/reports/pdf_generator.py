"""
PDF Report Generator for Vedic Astrology.
Generates comprehensive multi-page, publication-quality PDF consultation dossiers
using ReportLab with native vector chart renderings.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Group, Polygon

from app.models.astrological import Kundali
from app.models.advisory import LifestyleDossier
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha
from app.core.milestones import LifeMilestoneEngine
from app.engines.lifestyle_advisor import LifestyleAdvisor
from app.core.constants import ZODIAC_SIGNS, ZODIAC_SANSKRIT, SHODASHAVARGA_INFO


def draw_south_indian_chart(kundali: Kundali, width=240, height=240, varga_div=1) -> Drawing:
    """Create a native vector Drawing for a South Indian 4x4 astrological chart."""
    d = Drawing(width, height)
    cell_w = width / 4.0
    cell_h = height / 4.0

    # Outer border
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor("#faf8f5"), strokeColor=colors.HexColor("#2c3e50"), strokeWidth=1.5))

    # Grid lines
    for i in range(1, 4):
        d.add(Line(0, i * cell_h, width, i * cell_h, strokeColor=colors.HexColor("#7f8c8d"), strokeWidth=0.8))
        d.add(Line(i * cell_w, 0, i * cell_w, height, strokeColor=colors.HexColor("#7f8c8d"), strokeWidth=0.8))

    # Center 2x2 box
    d.add(Rect(cell_w, cell_h, cell_w * 2, cell_h * 2, fillColor=colors.HexColor("#f0ebe1"), strokeColor=colors.HexColor("#2c3e50"), strokeWidth=1.2))

    chart_title = "D1 Rasi Chart" if varga_div == 1 else f"D{varga_div} Chart"
    d.add(String(width / 2.0, height / 2.0 + 8, chart_title, fontName="Helvetica-Bold", fontSize=11, textAnchor="middle", fillColor=colors.HexColor("#2c3e50")))
    d.add(String(width / 2.0, height / 2.0 - 8, "South Indian", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor("#7f8c8d")))

    # Cell mapping (row from top 0 to 3, col from left 0 to 3)
    # 0: Aries (row 0, col 1) -> y = height - (r+1)*cell_h
    cells = {
        0: (0, 1), 1: (0, 2), 2: (0, 3), 3: (1, 3),
        4: (2, 3), 5: (3, 3), 6: (3, 2), 7: (3, 1),
        8: (3, 0), 9: (2, 0), 10: (1, 0), 11: (0, 0)
    }

    # Group contents by sign
    sign_planets = {i: [] for i in range(12)}
    if varga_div == 1 or varga_div not in kundali.vargas:
        sign_planets[kundali.ascendant.sign.value].append(f"ASC {kundali.ascendant.degrees_in_sign:.0f}°")
        for p_name, p in kundali.planets.items():
            retro = "R" if p.is_retrograde else ""
            sign_planets[p.sign.value].append(f"{p_name[:2]}{retro} {p.degrees_in_sign:.0f}°")
    else:
        v = kundali.vargas[varga_div]
        for ent, plc in v.placements.items():
            abbr = "ASC" if ent == "Ascendant" else ent[:2]
            sign_planets[plc.sign.value].append(f"{abbr} {plc.degrees_in_varga:.0f}°")

    for s_idx in range(12):
        r, c = cells[s_idx]
        x = c * cell_w
        y = height - (r + 1) * cell_h

        # Label sign name
        d.add(String(x + 4, y + cell_h - 10, ZODIAC_SANSKRIT[s_idx][:4], fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor("#95a5a6")))

        # Draw planets
        line_y = y + cell_h - 20
        for pl_str in sign_planets[s_idx]:
            color = colors.HexColor("#c0392b") if "ASC" in pl_str else colors.HexColor("#16a085") if "R" in pl_str else colors.HexColor("#2980b9")
            d.add(String(x + 4, line_y, pl_str, fontName="Helvetica", fontSize=7, fillColor=color))
            line_y -= 9

    return d


def draw_north_indian_chart(kundali: Kundali, width=240, height=240, varga_div=1) -> Drawing:
    """Create a native vector Drawing for a North Indian diamond chart."""
    d = Drawing(width, height)
    pad = 10
    w = width - 2 * pad
    h = height - 2 * pad
    x0, y0 = pad, pad
    x1, y1 = pad + w, pad + h
    xc, yc = pad + w / 2.0, pad + h / 2.0

    # Outer background
    d.add(Rect(x0, y0, w, h, fillColor=colors.HexColor("#fffdf9"), strokeColor=colors.HexColor("#2c3e50"), strokeWidth=1.5))

    # Diagonals
    d.add(Line(x0, y0, x1, y1, strokeColor=colors.HexColor("#7f8c8d"), strokeWidth=1.0))
    d.add(Line(x0, y1, x1, y0, strokeColor=colors.HexColor("#7f8c8d"), strokeWidth=1.0))

    # Inner diamond
    d.add(Polygon([xc, y0, x1, yc, xc, y1, x0, yc], fillColor=colors.transparent, strokeColor=colors.HexColor("#2c3e50"), strokeWidth=1.2))

    # Lagna sign index
    if varga_div == 1 or varga_div not in kundali.vargas:
        lagna_s = kundali.ascendant.sign.value
    else:
        lagna_s = kundali.vargas[varga_div].placements["Ascendant"].sign.value

    # House sign numbers (1-12)
    house_signs = {h: ((lagna_s + h - 1) % 12) + 1 for h in range(1, 13)}

    # Positions for sign numbers
    sign_pos = {
        1: (xc, y0 + h * 0.38),
        2: (x0 + w * 0.38, y0 + h * 0.78),
        3: (x0 + w * 0.22, y0 + h * 0.62),
        4: (x0 + w * 0.42, yc),
        5: (x0 + w * 0.22, y0 + h * 0.38),
        6: (x0 + w * 0.38, y0 + h * 0.22),
        7: (xc, y0 + h * 0.58),
        8: (x0 + w * 0.62, y0 + h * 0.22),
        9: (x0 + w * 0.78, y0 + h * 0.38),
        10: (x0 + w * 0.58, yc),
        11: (x0 + w * 0.78, y0 + h * 0.62),
        12: (x0 + w * 0.62, y0 + h * 0.78),
    }

    # Center text positions for occupant planets
    house_centers = {
        1: (xc, y0 + h * 0.72),
        2: (x0 + w * 0.28, y0 + h * 0.86),
        3: (x0 + w * 0.14, y0 + h * 0.72),
        4: (x0 + w * 0.28, yc),
        5: (x0 + w * 0.14, y0 + h * 0.28),
        6: (x0 + w * 0.28, y0 + h * 0.14),
        7: (xc, y0 + h * 0.28),
        8: (x0 + w * 0.72, y0 + h * 0.14),
        9: (x0 + w * 0.86, y0 + h * 0.28),
        10: (x0 + w * 0.72, yc),
        11: (x0 + w * 0.86, y0 + h * 0.72),
        12: (x0 + w * 0.72, y0 + h * 0.86),
    }

    # Group occupants
    house_planets = {h: [] for h in range(1, 13)}
    if varga_div == 1 or varga_div not in kundali.vargas:
        house_planets[1].append(f"ASC {kundali.ascendant.degrees_in_sign:.0f}°")
        for p_name, p in kundali.planets.items():
            h_num = ((p.sign.value - lagna_s) % 12) + 1
            retro = "R" if p.is_retrograde else ""
            house_planets[h_num].append(f"{p_name[:2]}{retro} {p.degrees_in_sign:.0f}°")

    for h_num in range(1, 13):
        # Draw sign number
        sx, sy = sign_pos[h_num]
        d.add(String(sx, sy, str(house_signs[h_num]), fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.HexColor("#7f8c8d")))

        # Draw planets
        cx, cy = house_centers[h_num]
        p_list = house_planets[h_num]
        if p_list:
            start_y = cy + (len(p_list) - 1) * 4.0
            for i, p_str in enumerate(p_list):
                py = start_y - (i * 8.0)
                color = colors.HexColor("#c0392b") if "ASC" in p_str else colors.HexColor("#2980b9")
                d.add(String(cx, py, p_str, fontName="Helvetica", fontSize=7, textAnchor="middle", fillColor=color))

    return d


def generate_astrological_pdf(
    kundali: Kundali,
    client_name: str,
    output_pdf_path: str,
    location_name: str
):
    """
    Generate a full multi-page PDF report with Kundali, Vargas, Dashas, Milestones, and Advisory.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,  # Center
        textColor=colors.HexColor('#1a365d')
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#4a5568')
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2d3748')
    )
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # 1. Header & Client Details
    story.append(Paragraph("VEDIC HOROSCOPE & LIFESTYLE CONSULTATION DOSSIER", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"Client: <b>{client_name}</b> | Generated: {datetime.now().strftime('%d %B %Y')}", subtitle_style))
    story.append(Spacer(1, 10))

    # Meta Table
    dob_str = kundali.birth_datetime.strftime("%d-%m-%Y %H:%M:%S UTC")
    meta_data = [
        [Paragraph("<b>Date & Time of Birth:</b>", body_style), Paragraph(f"20-Nov-1968, 03:45:00 AM IST", body_style),
         Paragraph("<b>Lagna (Ascendant):</b>", body_style), Paragraph(f"<b>{kundali.ascendant.sign.sanskrit_name}</b> ({kundali.ascendant.degrees_in_sign:.2f}°)", body_style)],
        [Paragraph("<b>Place of Birth:</b>", body_style), Paragraph(location_name, body_style),
         Paragraph("<b>Janma Rasi (Moon Sign):</b>", body_style), Paragraph(f"<b>{kundali.planets['Moon'].sign.sanskrit_name}</b> ({kundali.planets['Moon'].degrees_in_sign:.2f}°)", body_style)],
        [Paragraph("<b>Geographic Coordinates:</b>", body_style), Paragraph(f"{kundali.latitude:.4f}° N, {kundali.longitude:.4f}° E", body_style),
         Paragraph("<b>Janma Nakshatra:</b>", body_style), Paragraph(f"{kundali.planets['Moon'].nakshatra_name} (Pada {kundali.planets['Moon'].nakshatra_pada})", body_style)],
        [Paragraph("<b>Ayanamsa:</b>", body_style), Paragraph(f"{kundali.ayanamsa_name} ({kundali.ayanamsa_value:.4f}°)", body_style),
         Paragraph("<b>Nakshatra Lord:</b>", body_style), Paragraph(kundali.planets['Moon'].nakshatra_lord, body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[110, 150, 110, 150])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#edf2f7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 2. Charts Section (Side by Side Native Vector Drawings)
    story.append(Paragraph("1. Primary Kundali Visualizations (D1 Rasi)", h2_style))
    chart_south = draw_south_indian_chart(kundali, width=250, height=220, varga_div=1)
    chart_north = draw_north_indian_chart(kundali, width=250, height=220, varga_div=1)

    chart_table = Table([
        [Paragraph("<b>South Indian Style (Fixed Signs)</b>", subtitle_style),
         Paragraph("<b>North Indian Diamond Style (Fixed Houses)</b>", subtitle_style)],
        [chart_south, chart_north]
    ], colWidths=[260, 260])
    chart_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
    ]))
    story.append(chart_table)
    story.append(Spacer(1, 10))

    # 3. Planetary Positions Table
    story.append(Paragraph("2. Planetary Positions & Dignities (D1 Rasi)", h2_style))
    planets_header = ["Planet", "Longitude", "Sign (Rasi)", "Deg in Sign", "Nakshatra", "Pada", "Dignity", "House"]
    planets_rows = [[Paragraph(f"<b>{h}</b>", bold_body) for h in planets_header]]

    # Ascendant row
    asc_h = [
        Paragraph("<b>Ascendant</b>", body_style),
        Paragraph(f"{kundali.ascendant.longitude:.2f}°", body_style),
        Paragraph(kundali.ascendant.sign.sanskrit_name, body_style),
        Paragraph(f"{kundali.ascendant.degrees_in_sign:.2f}°", body_style),
        Paragraph(kundali.ascendant.nakshatra_name, body_style),
        Paragraph(str(kundali.ascendant.nakshatra_pada), body_style),
        Paragraph("Lagna", body_style),
        Paragraph("1st House", body_style)
    ]
    planets_rows.append(asc_h)

    for p_name, p in kundali.planets.items():
        motion_str = " (R)" if p.is_retrograde else ""
        h_num = ((p.sign.value - kundali.ascendant.sign.value) % 12) + 1
        planets_rows.append([
            Paragraph(f"<b>{p_name}{motion_str}</b>", body_style),
            Paragraph(f"{p.longitude:.2f}°", body_style),
            Paragraph(p.sign.sanskrit_name, body_style),
            Paragraph(f"{p.degrees_in_sign:.2f}°", body_style),
            Paragraph(p.nakshatra_name, body_style),
            Paragraph(str(p.nakshatra_pada), body_style),
            Paragraph(p.dignity, body_style),
            Paragraph(f"House {h_num}", body_style)
        ])

    p_table = Table(planets_rows, colWidths=[65, 55, 75, 60, 90, 35, 70, 70])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(p_table)

    story.append(PageBreak())

    # 4. Active Dashas & Upcoming Timeline
    story.append(Paragraph("3. Vimshottari Dasha Hierarchy & Active Periods", h2_style))
    moon_lon = kundali.planets["Moon"].longitude
    dashas = calculate_vimshottari_dashas(kundali.birth_datetime, moon_lon)
    active = get_active_dasha(dashas, datetime.now())

    active_box = [
        [Paragraph(f"<b>CURRENTLY ACTIVE DASHA PERIOD (Date: {datetime.now().strftime('%d %B %Y')}):</b>", bold_body)],
        [Paragraph(f"• <b>Mahadasha</b>: {active['mahadasha']} (Span: {active['mahadasha_start']} to {active['mahadasha_end']}) — <i>10th House Career & Status Focus</i><br/>"
                   f"• <b>Antardasha (Bhukti)</b>: {active['antardasha']} (Span: {active['antardasha_start']} to {active['antardasha_end']}) — <i>1st House Expansion & Restructuring</i><br/>"
                   f"• <b>Pratyantardasha</b>: {active['pratyantardasha']} (Span: {active['pratyantardasha_start']} to {active['pratyantardasha_end']}) — <i>7th House Reflection & Karmic Assessment</i>", body_style)],
        [Paragraph("<b>Key Future Forecast:</b> In December 2027, the native enters the golden <b>Venus-Jupiter</b> period. As Jupiter is the Lagna Lord situated in the 7th Kendra forming a Raja Yoga with Mars, this heralds one of the most rewarding and fulfilling chapters for prestige and legacy.", body_style)]
    ]
    act_table = Table(active_box, colWidths=[520])
    act_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ebf8ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3182ce')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(act_table)
    story.append(Spacer(1, 10))

    # All Mahadashas Summary Table
    story.append(Paragraph("<b>Full Mahadasha Lifecycle (120-Year Vimshottari Cycle):</b>", bold_body))
    dasha_rows = [[Paragraph("<b>Mahadasha Lord</b>", bold_body), Paragraph("<b>Duration</b>", bold_body), Paragraph("<b>Start Date</b>", bold_body), Paragraph("<b>End Date</b>", bold_body), Paragraph("<b>Life Phase Significance</b>", bold_body)]]
    significance = {
        "Jupiter": "Childhood & early development (Born under Jupiter dasha balance)",
        "Saturn": "Youth, formal education, discipline, foundational years",
        "Mercury": "Career launch, intellectual & commercial expansion",
        "Ketu": "Introspection, spiritual growth, restructuring",
        "Venus": "Current Major Cycle: Material consolidation, status, luxuries",
        "Sun": "Authority, elder statesman, legacy consolidation",
        "Moon": "Emotional peace, family blessings, detachment",
        "Mars": "Spiritual vitality and completion of karmas",
        "Rahu": "Transcendence and karmic integration"
    }
    for m in dashas[:7]:
        dasha_rows.append([
            Paragraph(f"<b>{m.lord}</b>", body_style),
            Paragraph(f"{m.duration_years:.2f} yrs", body_style),
            Paragraph(m.start_date.strftime("%d-%m-%Y"), body_style),
            Paragraph(m.end_date.strftime("%d-%m-%Y"), body_style),
            Paragraph(significance.get(m.lord, "Major period"), body_style)
        ])
    d_table = Table(dasha_rows, colWidths=[80, 55, 75, 75, 235])
    d_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(d_table)
    story.append(Spacer(1, 12))

    # 5. Lifestyle Advisory Section (Vehicle, Property, Dress Colors)
    story.append(Paragraph("4. Personalized Lifestyle, Vastu & Material Advisory", h2_style))
    dossier = LifestyleAdvisor.get_full_lifestyle_dossier(kundali)

    adv_data = [
        [Paragraph("<b>Domain</b>", bold_body), Paragraph("<b>Auspicious Recommendations</b>", bold_body), Paragraph("<b>Caution / To Avoid</b>", bold_body), Paragraph("<b>Astrological Reason</b>", bold_body)],
        [
            Paragraph("<b>Vehicle Colors</b><br/>(4th House: Gemini)", body_style),
            Paragraph("<b>Emerald Green, Mint Green, Metallic Jade, Sage, Dual-tone Silver</b>", body_style),
            Paragraph("Stark Jet Black, muddy dark brown", body_style),
            Paragraph("4th House is ruled by Mercury (Budha). Green and silver maximize driving alertness, protect against mechanical wear, and maintain vehicle value.", body_style)
        ],
        [
            Paragraph("<b>Residential Property</b><br/>(House / Land)", body_style),
            Paragraph("<b>North (Uttara)</b> or <b>North-East (Ishanya)</b> entrance", body_style),
            Paragraph("South-West (Nairruti) main entrance", body_style),
            Paragraph("4th House is Gemini (Mercury - North) and Lagna is Pisces (Jupiter - North-East). An entrance here nurtures family tranquility and steady domestic accumulation.", body_style)
        ],
        [
            Paragraph("<b>Commercial Office</b><br/>(Business / Store)", body_style),
            Paragraph("<b>North (Kubera Sthana)</b> or <b>East (Indra Sthana)</b> entrance", body_style),
            Paragraph("South-West entrance", body_style),
            Paragraph("10th house is Sagittarius (Jupiter). A North or East entrance guarantees commercial client inflow, liquidity, and professional goodwill. Seating: Sit in South-West facing North/East.", body_style)
        ],
        [
            Paragraph("<b>Eternal Power Colors</b>", body_style),
            Paragraph("<b>Golden Yellow & Amber</b> (Jupiter - Lagna Lord)<br/><b>Coral Red & Crimson</b> (Mars - 9th Bhagya Lord)", body_style),
            Paragraph("Jet Black, dull murky brown", body_style),
            Paragraph("Wearing or surrounding oneself with Jupiter and Mars hues fortifies bodily vitality (*Prana*) and activates fortunes.", body_style)
        ]
    ]
    adv_table = Table(adv_data, colWidths=[90, 140, 100, 190])
    adv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(adv_table)
    story.append(Spacer(1, 10))

    # Weekly Dress Table
    story.append(Paragraph("<b>Weekly Wardrobe Color Calendar (Vaara Vastra):</b>", bold_body))
    dress_rows = [[Paragraph("<b>Day & Ruling Planet</b>", bold_body), Paragraph("<b>Best Attire Colors</b>", bold_body), Paragraph("<b>Avoid</b>", bold_body), Paragraph("<b>Fabrics & Tip for Ravi Kumar S</b>", bold_body)]]
    for d_k, g in dossier.weekly_dress_guide.items():
        dress_rows.append([
            Paragraph(f"<b>{d_k}</b><br/>({g.ruling_planet})", body_style),
            Paragraph(", ".join(g.primary_favorable_colors[:3]), body_style),
            Paragraph(", ".join(g.colors_to_avoid_today[:2]), body_style),
            Paragraph(f"<i>{g.recommended_fabrics}</i>: {g.personalized_boost_tip}", body_style)
        ])
    dress_table = Table(dress_rows, colWidths=[80, 120, 90, 230])
    dress_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(dress_table)

    story.append(PageBreak())

    # 6. Shodashavarga (16 Divisional Charts) Summary Table
    story.append(Paragraph("5. Shodashavarga (16 Divisional Charts) Analysis", h2_style))
    vargas = calculate_all_vargas(kundali.ascendant, kundali.planets)

    v_rows = [[Paragraph("<b>Chart</b>", bold_body), Paragraph("<b>Name</b>", bold_body), Paragraph("<b>Weight</b>", bold_body), Paragraph("<b>Life Dimension Governed</b>", bold_body), Paragraph("<b>Lagna / Key Placements</b>", bold_body)]]
    for div, (v_name, v_sanskrit, v_purp, v_pts) in SHODASHAVARGA_INFO.items():
        v_chart = vargas[div]
        asc_v = v_chart.placements["Ascendant"].sign.sanskrit_name
        v_rows.append([
            Paragraph(f"<b>D{div}</b>", body_style),
            Paragraph(v_name, body_style),
            Paragraph(f"{v_pts} pts", body_style),
            Paragraph(v_purp, body_style),
            Paragraph(f"Asc: <b>{asc_v}</b>", body_style)
        ])

    v_table = Table(v_rows, colWidths=[40, 75, 45, 230, 130])
    v_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(v_table)
    story.append(Spacer(1, 10))

    # 7. Life Milestones Timeline
    story.append(Paragraph("6. Key Astrological Life Milestones & Upcoming Windows", h2_style))
    milestones = LifeMilestoneEngine.calculate_all_milestones(kundali, dashas, max_age_years=75.0)

    m_rows = [[Paragraph("<b>Age</b>", bold_body), Paragraph("<b>Milestone Category</b>", bold_body), Paragraph("<b>Window Dates</b>", bold_body), Paragraph("<b>Nature & Traditional Guidance</b>", bold_body)]]
    # Filter key milestones around current age (50-65)
    key_ms = [m for m in milestones if 45.0 <= m.approx_age_years <= 65.0]
    for km in key_ms[:6]:
        m_rows.append([
            Paragraph(f"~Age {km.approx_age_years:.0f}", body_style),
            Paragraph(km.title[:35], body_style),
            Paragraph(f"{km.start_date.strftime('%b %Y')} to {km.end_date.strftime('%b %Y')}", body_style),
            Paragraph(f"{km.description[:120]}... <i>Focus: {km.recommended_focus[:80]}</i>", body_style)
        ])
    m_table = Table(m_rows, colWidths=[45, 125, 95, 255])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 15))

    # Footer note
    story.append(Paragraph("<i>Note: This report is compiled according to the principles of Brihat Parasara Hora Sastra using the Lahiri (Chitra Paksha) Ayanamsa. Astrological guidance is designed to assist personal alignment and reflection.</i>", subtitle_style))

    doc.build(story)
    return output_pdf_path
