"""
Master Unified Vedic Astrological Consultation & Q&A Dossier Generator.
Combines Full Horoscope, Kundali Charts, Q&A on Career & Real Estate,
Lifestyle Advisory, Shodashavargas, and Dasha Milestones into a single master PDF.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon

from app.models.astrological import Kundali
from app.engines.qa_consultation import ComprehensiveQADossier, QAConsultationEngine
from app.engines.lifestyle_advisor import LifestyleAdvisor
from app.reports.pdf_generator import draw_south_indian_chart, draw_north_indian_chart
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha
from app.core.milestones import LifeMilestoneEngine
from app.core.constants import SHODASHAVARGA_INFO


def generate_master_astrological_dossier(
    kundali: Kundali,
    client_name: str,
    output_pdf_path: str,
    location_name: str
) -> str:
    """Generate a single unified master publication-grade consultation dossier."""
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()

    # Typography styles
    title_style = ParagraphStyle(
        'MasterTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        alignment=1,
        textColor=colors.HexColor('#1a365d')
    )
    subtitle_style = ParagraphStyle(
        'MasterSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#4a5568')
    )
    section_h = ParagraphStyle(
        'MasterSecH',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=10,
        spaceAfter=5
    )
    q_style = ParagraphStyle(
        'MasterQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1a365d')
    )
    body_style = ParagraphStyle(
        'MasterBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#2d3748')
    )
    bold_body = ParagraphStyle(
        'MasterBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER HEADER, DUAL CHARTS, PLANETARY POSITIONS
    # =========================================================================
    story.append(Paragraph("VEDIC ASTROLOGICAL CONSULTATION & ADVISORY DOSSIER", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"Client: <b>{client_name}</b> | DOB: 20-Nov-1968, 03:45 AM IST | Malleshwaram, Bengaluru, India", subtitle_style))
    story.append(Spacer(1, 6))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Lagna (Ascendant):</b>", body_style), Paragraph(f"<b>{kundali.ascendant.sign.sanskrit_name}</b> ({kundali.ascendant.degrees_in_sign:.2f}°)", body_style),
         Paragraph("<b>Janma Rasi (Moon):</b>", body_style), Paragraph(f"<b>{kundali.planets['Moon'].sign.sanskrit_name}</b> ({kundali.planets['Moon'].degrees_in_sign:.2f}°)", body_style)],
        [Paragraph("<b>Janma Nakshatra:</b>", body_style), Paragraph(f"{kundali.planets['Moon'].nakshatra_name} (Pada {kundali.planets['Moon'].nakshatra_pada})", body_style),
         Paragraph("<b>Surya Rasi (Sun):</b>", body_style), Paragraph(f"<b>{kundali.planets['Sun'].sign.sanskrit_name}</b> (9th House)", body_style)],
        [Paragraph("<b>Lahiri Ayanamsa:</b>", body_style), Paragraph(f"{kundali.ayanamsa_value:.4f}°", body_style),
         Paragraph("<b>Active Dasha:</b>", body_style), Paragraph("<b>Venus - Rahu - Ketu</b> (Dec 2024 – Dec 2027)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[110, 150, 110, 150])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#edf2f7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Side by side charts
    story.append(Paragraph("1. Primary Kundali Visualizations (D1 Rasi)", section_h))
    c_south = draw_south_indian_chart(kundali, width=245, height=205, varga_div=1)
    c_north = draw_north_indian_chart(kundali, width=245, height=205, varga_div=1)
    chart_table = Table([
        [Paragraph("<b>South Indian Style (Fixed Signs)</b>", subtitle_style),
         Paragraph("<b>North Indian Diamond Style (Fixed Houses)</b>", subtitle_style)],
        [c_south, c_north]
    ], colWidths=[260, 260])
    chart_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
    ]))
    story.append(chart_table)
    story.append(Spacer(1, 6))

    # Planetary Positions Table
    story.append(Paragraph("2. Planetary Positions & Bhavas (D1 Rasi)", section_h))
    planets_header = ["Planet", "Longitude", "Sign (Rasi)", "Deg in Sign", "Nakshatra", "Pada", "Dignity", "House"]
    planets_rows = [[Paragraph(f"<b>{h}</b>", bold_body) for h in planets_header]]

    # Ascendant
    planets_rows.append([
        Paragraph("<b>Ascendant</b>", body_style),
        Paragraph(f"{kundali.ascendant.longitude:.2f}°", body_style),
        Paragraph(kundali.ascendant.sign.sanskrit_name, body_style),
        Paragraph(f"{kundali.ascendant.degrees_in_sign:.2f}°", body_style),
        Paragraph(kundali.ascendant.nakshatra_name, body_style),
        Paragraph(str(kundali.ascendant.nakshatra_pada), body_style),
        Paragraph("Lagna", body_style),
        Paragraph("1st House", body_style)
    ])
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
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(p_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: Q&A PART I - CAREER, PROMOTION, SALARY, TENURE & OWN BUSINESS
    # =========================================================================
    story.append(Paragraph("3. Executive Verdict Matrix for Ravi Kumar S", section_h))
    qa_engine = QAConsultationEngine.evaluate_ravi_kumar(kundali)

    sum_matrix = [
        [Paragraph("<b>Question Posed by Client</b>", bold_body), Paragraph("<b>Astrological Verdict</b>", bold_body), Paragraph("<b>Key Dates / Timeline</b>", bold_body)],
        [
            Paragraph("<b>Promotion & Increment in current company?</b>", body_style),
            Paragraph("<font color='#22543d'><b>CONFIRMED</b></font> (Two-stage progression)", body_style),
            Paragraph("• Phase 1: <b>Feb – Apr 2027</b><br/>• Phase 2: <b>Dec 2027 – Apr 2028</b>", body_style)
        ],
        [
            Paragraph("<b>Tenure in present company? Last company?</b>", body_style),
            Paragraph("<b>1.0 to 1.5 Years remaining. NOT his last company.</b>", body_style),
            Paragraph("Decisive job change: <b>Dec 2027 – mid 2028</b>", body_style)
        ],
        [
            Paragraph("<b>Can he start his own company?</b>", body_style),
            Paragraph("<font color='#22543d'><b>HIGHLY RECOMMENDED</b></font> (Guru-Mangala Yoga)", body_style),
            Paragraph("Optimal Launch: <b>Dec 2027 – Aug 2028</b>", body_style)
        ],
        [
            Paragraph("<b>Denkanikottai/Hosur Land: Keep or Sell?</b>", body_style),
            Paragraph("<font color='#2b6cb0'><b>KEEP (HOLD) FOR NOW</b></font>. Do not sell in 2026.", body_style),
            Paragraph("Selling now = undervaluation.<br/>Hold until <b>late 2027 / 2028</b>", body_style)
        ],
        [
            Paragraph("<b>Profit or Loss on Land Sale?</b>", body_style),
            Paragraph("<font color='#22543d'><b>SUBSTANTIAL PROFIT (ZERO RISK OF LOSS)</b></font>", body_style),
            Paragraph("Exalted Venus in D4 guarantees strong appreciation", body_style)
        ],
        [
            Paragraph("<b>When will the Land Sale happen?</b>", body_style),
            Paragraph("<b>Optimal: Apr 2028 – Sep 2028</b> (Venus-Jupiter-Saturn)", body_style),
            Paragraph("Early window: <b>Aug 2027 – Nov 2027</b>", body_style)
        ]
    ]
    sum_t = Table(sum_matrix, colWidths=[165, 185, 170])
    sum_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(sum_t)
    story.append(Spacer(1, 8))

    # Career Detail Box
    c_qa = qa_engine.career_qa
    story.append(Paragraph("4. Career Trajectory & Enterprise Roadmap", section_h))
    career_box_data = [
        [Paragraph("<b>Q1.1: What is his status in current company? When will promotion & increment happen?</b>", q_style)],
        [Paragraph(f"<b>Current Situation:</b> {c_qa.current_status}", body_style)],
        [Paragraph(f"<b>Promotion & Increment Timeline:</b><br/>{c_qa.promotion_timeline.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph("<b>Q1.2: How many years in current company? Is this his last company?</b>", q_style)],
        [Paragraph(f"<b>Tenure & Next Step:</b> {c_qa.company_tenure_forecast} {c_qa.job_change_vs_last_company}", body_style)],
        [Paragraph("<b>Q1.3: Whether he can start his own company?</b>", q_style)],
        [Paragraph(f"<b>Feasibility & Best Sectors:</b> {c_qa.own_business_feasibility}<br/>"
                   f"<b>Recommended Domains:</b> • " + "<br/>• ".join(c_qa.best_business_domains) + "<br/>"
                   f"<b>Optimal Launch Window:</b> <b>{c_qa.best_business_launch_window}</b>", body_style)],
        [Paragraph("<b>Strategic Career Action Plan:</b><br/>• " + "<br/>• ".join(c_qa.strategic_career_advice), body_style)]
    ]
    c_table = Table(career_box_data, colWidths=[520])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 2), (-1, 2), 0.5, colors.HexColor('#cbd5e0')),
        ('LINEBELOW', (0, 4), (-1, 4), 0.5, colors.HexColor('#cbd5e0')),
        ('LINEBELOW', (0, 6), (-1, 6), 0.5, colors.HexColor('#cbd5e0')),
    ]))
    story.append(c_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: Q&A PART II - REAL ESTATE (DENKANIKOTTAI / HOSUR LAND)
    # =========================================================================
    r_qa = qa_engine.real_estate_qa
    story.append(Paragraph("5. Real Estate Advisory: Denkanikottai / Hosur Land Plot", section_h))

    re_box_data = [
        [Paragraph("<b>Subject Property:</b> Land plot in Denkanikottai (Denkanikotta), near Hosur, Krishnagiri District, Tamil Nadu.", q_style)],
        [Paragraph(f"<b>Astrological Analysis of Land:</b> {r_qa.current_market_astrology}", body_style)],
        [Paragraph("<b>Q2.1: Whether to KEEP the land or SELL it right now?</b>", q_style)],
        [Paragraph(f"<b>Verdict:</b> {r_qa.keep_vs_sell_verdict.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph("<b>Q2.2: Will he get PROFIT or LOSS on this land?</b>", q_style)],
        [Paragraph(f"<b>Profitability:</b> {r_qa.profit_vs_loss_verdict}", body_style)],
        [Paragraph("<b>Q2.3: WHEN will the land sale happen if he decides to sell?</b>", q_style)],
        [Paragraph(f"<b>Optimal Timing for Sale:</b><br/>{r_qa.best_selling_window.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph(f"<b>Financial Outcome:</b> {r_qa.financial_outcome_forecast}", body_style)],
        [Paragraph("<b>Strategic Real Estate Guidelines:</b><br/>• " + "<br/>• ".join(r_qa.strategic_real_estate_advice), body_style)],
        [Paragraph("<b>Remedies for Smooth Land Realization & Maximized Value:</b><br/>• " + "<br/>• ".join(r_qa.remedy_for_smooth_transaction), body_style)]
    ]
    re_table = Table(re_box_data, colWidths=[520])
    re_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fff4')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#68d391')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.HexColor('#c6f6d5')),
        ('LINEBELOW', (0, 3), (-1, 3), 0.5, colors.HexColor('#c6f6d5')),
        ('LINEBELOW', (0, 5), (-1, 5), 0.5, colors.HexColor('#c6f6d5')),
        ('LINEBELOW', (0, 8), (-1, 8), 0.5, colors.HexColor('#c6f6d5')),
    ]))
    story.append(re_table)
    story.append(Spacer(1, 10))

    # Astrological Mechanics Table
    story.append(Paragraph("<b>Astrological Mechanics & Scriptural Rationale:</b>", bold_body))
    mech_data = [
        [Paragraph("<b>Divisional Chart</b>", bold_body), Paragraph("<b>Placement & Scriptural Mechanism</b>", bold_body)],
        [
            Paragraph("<b>D4 Chaturthamsa (Land)</b>", body_style),
            Paragraph("Sagittarius Lagna with <b>Jupiter in OWN sign in 1st</b>, Mars in 1st, and <b>Venus EXALTED in Pisces in 4th</b>. This ensures that land acquired by him carries extraordinary built-in capital appreciation.", body_style)
        ],
        [
            Paragraph("<b>D10 Dasamsa (Career)</b>", body_style),
            Paragraph("Cancer Lagna with <b>Jupiter EXALTED in 1st house</b>, Moon in OWN sign, and Sun in OWN sign. Establishes strong executive authority and consulting leadership.", body_style)
        ],
        [
            Paragraph("<b>7th House Raja Yoga</b>", body_style),
            Paragraph("Lagna Lord Jupiter + 9th Lord Mars in Virgo Kendra forms a classical Guru-Mangala Raja Yoga.", body_style)
        ]
    ]
    mech_t = Table(mech_data, colWidths=[140, 380])
    mech_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(mech_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: LIFESTYLE ADVISORY (VEHICLE, PROPERTY, DRESS COLORS)
    # =========================================================================
    story.append(Paragraph("6. Lifestyle, Vastu & Material Color Advisory", section_h))
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
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(adv_table)
    story.append(Spacer(1, 8))

    # Weekly Wardrobe Table
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
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(dress_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: VIMSHOTTARI DASHA HIERARCHY & TIMELINE
    # =========================================================================
    story.append(Paragraph("7. Vimshottari Dasha Hierarchy & Active Periods", section_h))
    moon_lon = kundali.planets["Moon"].longitude
    dashas = calculate_vimshottari_dashas(kundali.birth_datetime, moon_lon)
    active = get_active_dasha(dashas, datetime.now())

    active_box = [
        [Paragraph(f"<b>ACTIVE DASHA TODAY (Date: {datetime.now().strftime('%d %B %Y')}):</b>", bold_body)],
        [Paragraph(f"• <b>Mahadasha</b>: {active['mahadasha']} ({active['mahadasha_start']} to {active['mahadasha_end']}) — <i>10th House Career/Status Focus</i><br/>"
                   f"• <b>Antardasha (Bhukti)</b>: {active['antardasha']} ({active['antardasha_start']} to {active['antardasha_end']}) — <i>1st House Restructuring</i><br/>"
                   f"• <b>Pratyantardasha</b>: {active['pratyantardasha']} ({active['pratyantardasha_start']} to {active['pratyantardasha_end']}) — <i>7th House Karmic Assessment</i>", body_style)],
        [Paragraph("<b>Strategic Insight:</b> In December 2027, the native enters the golden <b>Venus-Jupiter</b> period. As Jupiter is the Lagna Lord situated in the 7th Kendra forming Raja Yoga with Mars, 2028–2030 will be one of his most rewarding professional and financial chapters.", body_style)]
    ]
    act_table = Table(active_box, colWidths=[520])
    act_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ebf8ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3182ce')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(act_table)
    story.append(Spacer(1, 8))

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

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: SHODASHAVARGAS & LIFE MILESTONES
    # =========================================================================
    story.append(Paragraph("8. Shodashavarga (16 Divisional Charts) Analysis", section_h))
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
    story.append(Spacer(1, 8))

    # Milestones
    story.append(Paragraph("9. Key Astrological Life Milestones (~Age 45–65)", section_h))
    milestones = LifeMilestoneEngine.calculate_all_milestones(kundali, dashas, max_age_years=75.0)
    m_rows = [[Paragraph("<b>Age</b>", bold_body), Paragraph("<b>Milestone Category</b>", bold_body), Paragraph("<b>Window Dates</b>", bold_body), Paragraph("<b>Nature & Guidance</b>", bold_body)]]
    key_ms = [m for m in milestones if 45.0 <= m.approx_age_years <= 65.0]
    for km in key_ms[:6]:
        m_rows.append([
            Paragraph(f"~Age {km.approx_age_years:.0f}", body_style),
            Paragraph(km.title[:35], body_style),
            Paragraph(f"{km.start_date.strftime('%b %Y')} to {km.end_date.strftime('%b %Y')}", body_style),
            Paragraph(f"{km.description[:110]}... <i>Focus: {km.recommended_focus[:70]}</i>", body_style)
        ])
    m_table = Table(m_rows, colWidths=[45, 125, 95, 255])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<i>Prepared for Ravi Kumar S under the principles of Brihat Parasara Hora Sastra and Jaimini Sutras.</i>", subtitle_style))

    doc.build(story)
    return output_pdf_path
