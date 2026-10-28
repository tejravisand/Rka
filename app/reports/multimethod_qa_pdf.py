"""
Comprehensive Multi-Method Astrological Q&A PDF Report Generator.
Renders an executive, publication-grade consultation report integrating:
1. Parashara Hora Method
2. Krishnamurti Padhdhati (KP Astrology: 249 Sub-Lords)
3. Dr. B. V. Raman Method (300 Combinations & Prasna Marga)
4. Lal Kitab Method (Pakka Ghar & Karmic Rin)
5. Numerology (Chaldean & Pythagorean)
6. Real-Time Present Gochara (Transit) at Enquiry Moment & Diagnostic
7. Comprehensive Shastric Planetary Aspects (Drishti Matrix - Mars 4/8, Jupiter 5/9, Saturn 3/10)
8. Present Name Diagnostic & General-Purpose Alternate Names (Non-legal adoption)
9. Education Stream, Education Break Risk & Academic Remedies
10. Profession, Vocational Trajectory & D10 Dashamsha Career Direction
11. Marriage Longevity & Breakup / Separation Risk Mitigation
12. Favourable & Unfavourable Mobile and Vehicle Registration Numbers
13. All types of remedies: Mantras, Sacred Plant Pradakshinams, Lal Kitab Upayas, Danam & Gemstones.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from app.engines.multi_method_qa import MultiMethodQAResponse


def generate_multimethod_qa_pdf(
    response: MultiMethodQAResponse,
    output_pdf_path: str
) -> str:
    """Generates an executive multi-page consultation PDF."""
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    # Palette
    c_primary = colors.HexColor('#1a365d')    # Deep Navy
    c_secondary = colors.HexColor('#2b6cb0')  # Royal Blue
    c_accent = colors.HexColor('#c53030')     # Deep Red
    c_gold = colors.HexColor('#b7791f')       # Sacred Gold
    c_bg_light = colors.HexColor('#f7fafc')   # Off white

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15.5,
        leading=19,
        alignment=1,
        textColor=c_primary
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#4a5568')
    )
    sec_header = ParagraphStyle(
        'SecHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#2d3748')
    )
    table_cell = ParagraphStyle(
        'TCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#2d3748')
    )
    table_cell_bold = ParagraphStyle(
        'TCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=c_primary
    )
    table_header = ParagraphStyle(
        'THeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )
    verdict_badge = ParagraphStyle(
        'VerdictBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=c_accent
    )

    story = []

    # =========================================================================
    # HEADER / BANNER
    # =========================================================================
    story.append(Paragraph("VEDIC & SCIENTIFIC ASTROLOGICAL CONSULTATION DOSSIER", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "Parashara Hora • KP (249 Sub-Lords) • Dr. B. V. Raman • Lal Kitab • Numerology • Real-Time Gochara • Aspects (Drishti)",
        subtitle_style
    ))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_secondary, spaceBefore=1, spaceAfter=5))

    # Client & Prashna Info Table
    c = response.client
    q = response.query
    k = response.natal_kundali

    meta_data = [
        [
            Paragraph("<b>Client Name:</b>", table_cell_bold),
            Paragraph(f"<b>{c.name}</b>", table_cell),
            Paragraph("<b>Prashna Time (Query):</b>", table_cell_bold),
            Paragraph(q.query_datetime_local.strftime("%d-%b-%Y %I:%M %p"), table_cell)
        ],
        [
            Paragraph("<b>Birth Date & Time:</b>", table_cell_bold),
            Paragraph(c.birth_datetime_local.strftime("%d-%b-%Y %I:%M %p"), table_cell),
            Paragraph("<b>Prashna Place:</b>", table_cell_bold),
            Paragraph(q.query_place_name, table_cell)
        ],
        [
            Paragraph("<b>Birth Place:</b>", table_cell_bold),
            Paragraph(f"{c.place_name} ({c.latitude:.2f}°N, {c.longitude:.2f}°E)", table_cell),
            Paragraph("<b>Marital Status:</b>", table_cell_bold),
            Paragraph(f"<b>{getattr(c, 'marital_status', 'Unmarried')}</b>", table_cell)
        ],
        [
            Paragraph("<b>Lagna / Janma Rasi:</b>", table_cell_bold),
            Paragraph(f"{k.ascendant.sign.sanskrit_name} Lagna / {k.planets['Moon'].sign.sanskrit_name} Rasi ({k.planets['Moon'].nakshatra_name})", table_cell),
            Paragraph("<b>Active Dasha:</b>", table_cell_bold),
            Paragraph(f"{response.current_active_dasha['mahadasha']}-{response.current_active_dasha['antardasha']}", table_cell)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[105, 160, 115, 160])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5))

    # Question & Consensus Verdict Box
    q_box_data = [
        [
            Paragraph(f"<b>CONSULTATION QUESTION:</b> \"{q.question_text}\"", ParagraphStyle('QBox', parent=body_style, fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_primary)),
            Paragraph(f"<b>CATEGORY:</b> {q.question_category.upper()}", ParagraphStyle('QCat', parent=body_style, fontName='Helvetica-Bold', fontSize=8, textColor=c_secondary, alignment=2))
        ],
        [
            Paragraph(f"<b>UNIFIED CONSENSUS VERDICT:</b> {response.unified_verdict}", verdict_badge),
            Paragraph(f"<b>CONFIDENCE INDEX:</b> {response.consensus_probability_percent}%", ParagraphStyle('Score', parent=verdict_badge, textColor=c_secondary))
        ]
    ]
    q_table = Table(q_box_data, colWidths=[390, 150])
    q_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffaf0')),
        ('BOX', (0, 0), (-1, -1), 1.2, c_gold),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#fbd38d')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(q_table)
    story.append(Spacer(1, 5))

    # Dedicated Targeted Astrological Prediction & Timeline Box
    t_pred = getattr(response, 'targeted_prediction', None)
    if t_pred:
        t_box_data = [
            [
                Paragraph("<b>TARGETED ASTROLOGICAL PREDICTION & TIMELINE</b>", table_cell_bold),
                Paragraph(f"<b>Timeline:</b> {t_pred.primary_timeline_window}", ParagraphStyle('TTime', parent=table_cell, textColor=c_gold, fontName='Helvetica-Bold'))
            ],
            [
                Paragraph(t_pred.core_prediction_narrative, table_cell),
                Paragraph(f"<b>Marital Profile:</b> {t_pred.marital_status}<br/><b>Mechanics:</b> {t_pred.astrological_mechanics}", table_cell)
            ]
        ]
        t_table = Table(t_box_data, colWidths=[360, 180])
        t_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fff4')),
            ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#38a169')),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#9ae6b4')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t_table)
        story.append(Spacer(1, 5))

    # =========================================================================
    # SECTION 1: REAL-TIME PRESENT GOCHARA (TRANSIT) AT ENQUIRY MOMENT
    # =========================================================================
    story.append(Paragraph("1. REAL-TIME PRESENT GOCHARA (TRANSIT) AT MOMENT OF ENQUIRY", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    goc = response.present_gochara
    goc_data = [
        [
            Paragraph("<b>Why This Question Arose Now:</b>", table_cell_bold),
            Paragraph(goc.why_this_question_now_diagnostic, table_cell)
        ],
        [
            Paragraph("<b>Transiting Saturn (Shani Gochara):</b>", table_cell_bold),
            Paragraph(goc.saturn_transit_verdict, table_cell)
        ],
        [
            Paragraph("<b>Transiting Jupiter (Guru Bala):</b>", table_cell_bold),
            Paragraph(goc.jupiter_transit_verdict, table_cell)
        ],
        [
            Paragraph("<b>Transiting Rahu-Ketu Axis:</b>", table_cell_bold),
            Paragraph(goc.rahu_ketu_transit_verdict, table_cell)
        ]
    ]
    goc_table = Table(goc_data, colWidths=[130, 410])
    goc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffaf0')),
        ('BOX', (0, 0), (-1, -1), 0.8, c_gold),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#fbd38d')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(goc_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 2: COMPREHENSIVE PLANETARY ASPECTS (DRISHTI MATRIX)
    # =========================================================================
    story.append(Paragraph("2. COMPREHENSIVE SHASTRIC PLANETARY ASPECTS (DRISHTI MATRIX)", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    asp = response.detailed_aspects
    asp_rows = [
        [
            Paragraph("Key Focal Target Point", table_header),
            Paragraph("Aspecting Planets (Special Drishti)", table_header),
            Paragraph("Net Astrological Influence & Interpretation", table_header)
        ]
    ]
    for kp in asp.key_points_aspects[:5]:
        asp_rows.append([
            Paragraph(f"<b>{kp.target_point}</b>", table_cell_bold),
            Paragraph(", ".join(kp.aspecting_planets), table_cell),
            Paragraph(f"<b>{kp.net_influence}:</b> {kp.detailed_interpretation}", table_cell)
        ])

    asp_table = Table(asp_rows, colWidths=[130, 130, 280])
    asp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(asp_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 3: PRESENT NAME DIAGNOSTIC & ALTERNATE NAME SUGGESTIONS
    # =========================================================================
    story.append(Paragraph("3. PRESENT NAME DIAGNOSTIC & GENERAL-PURPOSE ALTERNATE NAMES", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    nt = response.name_tuning
    cal_bullets = "".join([
        f"• <b>\"{cal.calibrated_name}\"</b> (Compound {cal.chaldean_compound} &rarr; {cal.chaldean_single}) : {cal.vibration_title} — {cal.vibration_benefit}<br/>"
        for cal in nt.spelling_calibration_suggestions
    ])
    vedic_bullets = "".join([
        f"• <b>\"{vn.suggested_name}\"</b> ({vn.meaning}) : Compound {vn.chaldean_compound} &rarr; {vn.chaldean_single} ({vn.planetary_ruler.split('(')[0]})<br/>"
        for vn in nt.vedic_nakshatra_name_options[:3]
    ])

    name_data = [
        [
            Paragraph("<b>Present Name Diagnostic:</b>", table_cell_bold),
            Paragraph(f"\"{nt.present_name}\" : Chaldean Compound <b>{nt.present_chaldean_compound}</b> &rarr; Single <b>{nt.present_chaldean_single}</b>.<br/><i>Diagnostic:</i> {nt.present_name_status}<br/><i>Meaning:</i> {nt.present_compound_meaning}", table_cell)
        ],
        [
            Paragraph("<b>Spelling Calibrations:</b><br/><i>(For Visiting Cards, LinkedIn & Signature)</i>", table_cell_bold),
            Paragraph(cal_bullets + "<i>Protocol: Keep Passport/Aadhaar/PAN legal records untouched. Use calibrated spelling for professional bylines.</i>", table_cell)
        ],
        [
            Paragraph(f"<b>Vedic Nakshatra Names:</b><br/><i>(Syllable \"{nt.vedic_nakshatra_syllable}\")</i>", table_cell_bold),
            Paragraph(vedic_bullets, table_cell)
        ]
    ]

    name_table = Table(name_data, colWidths=[130, 410])
    name_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7fafc')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(name_table)
    story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: EDUCATION STREAM, BREAK RISK & PROFESSION
    # =========================================================================
    story.append(Paragraph("4. EDUCATION STREAM, EDUCATION BREAK RISK & PROFESSION PROFILE", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    ed = response.education_stream
    br = response.education_break
    pf = response.profession

    edu_prof_data = [
        [
            Paragraph("<b>Education Stream & Degrees:</b>", table_cell_bold),
            Paragraph(f"<b>{ed.primary_stream}</b> (Secondary: {ed.secondary_stream})<br/><i>Degrees:</i> {', '.join(ed.recommended_degrees)}<br/><i>D24:</i> {ed.d24_siddhamsa_summary}", table_cell)
        ],
        [
            Paragraph("<b>Education Break Assessment:</b>", table_cell_bold),
            Paragraph(f"<b>Risk Level:</b> {br.break_risk_level} | <i>Vulnerable Windows:</i> {', '.join(br.vulnerable_age_windows)}<br/><i>Drivers & Recovery:</i> {br.astrological_drivers} — {br.resumption_and_recovery}<br/><i>Academic Remedy:</i> {br.academic_remedies[0]}", table_cell)
        ],
        [
            Paragraph("<b>Profession Trajectory:</b>", table_cell_bold),
            Paragraph(f"<b>{pf.career_path_verdict}</b><br/><i>Amatyakaraka:</i> {pf.amatyakaraka_planet} ({pf.amatyakaraka_guidance})<br/><i>Top Domains:</i> {', '.join(pf.top_recommended_domains)}<br/><i>D10 Dashamsha:</i> {pf.d10_dashamsha_confirmation}", table_cell)
        ]
    ]

    edu_prof_table = Table(edu_prof_data, colWidths=[130, 410])
    edu_prof_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fff4')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#9ae6b4')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c6f6d5')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(edu_prof_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 5: MARRIAGE LONGEVITY & BREAKUP / SEPARATION RISK MITIGATION
    # =========================================================================
    story.append(Paragraph("5. MARRIAGE LONGEVITY & BREAKUP / SEPARATION RISK MITIGATION", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    mb = response.marriage_breakup
    marr_data = [
        [
            Paragraph("<b>Marital Longevity & Breakup Risk:</b>", table_cell_bold),
            Paragraph(f"<b>Score: {mb.marital_longevity_score} / 100</b> (Risk: <b>{mb.breakup_risk_level}</b>) | Kuja/Manglik: <b>{mb.manglik_dosha_status}</b>", table_cell)
        ],
        [
            Paragraph("<b>7th & 8th House Dynamics:</b>", table_cell_bold),
            Paragraph(f"{mb.seventh_house_dynamics} | {mb.eighth_house_mangalya_status}<br/><i>Upapada Lagna:</i> {mb.upapada_lagna_analysis} | <i>KP:</i> {mb.kp_sub_lord_separation_indicator}", table_cell)
        ],
        [
            Paragraph("<b>Conflict Triggers & Remedies:</b>", table_cell_bold),
            Paragraph(f"<i>Conflict Triggers:</i> {'; '.join(mb.primary_conflict_triggers)}<br/><i>Marriage Shield:</i> Wear <b>Gauri-Shankar Rudraksha</b> on Monday; chant Katyayani Mantra: <i>'{mb.preventive_remedies_for_harmony[1]}'</i>", table_cell)
        ]
    ]

    marr_table = Table(marr_data, colWidths=[130, 410])
    marr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff5f5')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#feb2b2')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#fed7d7')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(marr_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 6: FAVOURABLE & UNFAVOURABLE MOBILE AND VEHICLE NUMBERS
    # =========================================================================
    story.append(Paragraph("6. FAVOURABLE & UNFAVOURABLE MOBILE AND VEHICLE REGISTRATION NUMBERS", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    mob = response.mobile_guidance
    veh = response.vehicle_guidance

    num_data = [
        [
            Paragraph("<b>Mobile Numbers Guidance:</b>", table_cell_bold),
            Paragraph(
                f"<b>Favourable Single Sums:</b> {', '.join(map(str, mob.favourable_single_totals))} (Compounds: {', '.join(map(str, mob.favourable_compound_totals))})<br/>"
                f"<b>Single Sums to AVOID:</b> {', '.join(map(str, mob.unfavourable_single_totals))} | <i>Avoid Clustered Triples:</i> {', '.join(map(str, mob.digits_to_avoid_repeating))}<br/>"
                f"<b>Tested Custom Mobile:</b> {mob.evaluated_custom_number.mobile_number} (Sum {mob.evaluated_custom_number.total_digits_sum}->{mob.evaluated_custom_number.reduced_single_digit}) : <b>{mob.evaluated_custom_number.compatibility_verdict.split('(')[0]}</b>" if mob.evaluated_custom_number else "No custom mobile passed.",
                table_cell
            )
        ],
        [
            Paragraph("<b>Vehicle & 4-Wheeler Diagnosis:</b>", table_cell_bold),
            Paragraph(
                f"<b>4th Vahana Lord:</b> {veh.fourth_house_lord} | <b>4-Wheeler Status:</b> {veh.four_wheeler_feasibility}<br/>"
                f"<b>Diagnosis:</b> {veh.vehicle_ownership_diagnosis}<br/>"
                f"<b>Favourable 4-Digit Sums:</b> {', '.join(map(str, veh.favourable_plate_single_sums))} | <b>Avoid (Accident Triggers):</b> {', '.join(map(str, veh.unfavourable_plate_single_sums))}<br/>"
                f"<b>Lucky Colors:</b> {', '.join(veh.lucky_vehicle_colors)} | <b>Avoid:</b> {', '.join(veh.caution_vehicle_colors)} | <b>Parking:</b> {veh.auspicious_parking_direction}<br/>"
                f"<b>Tested Vehicle Plate:</b> {veh.evaluated_custom_plate.plate_number} (Sum {veh.evaluated_custom_plate.four_digit_sum}->{veh.evaluated_custom_plate.four_digit_reduced}) : <b>{veh.evaluated_custom_plate.safety_and_fortune_verdict.split('(')[0]}</b>" if veh.evaluated_custom_plate else "No custom plate passed.",
                table_cell
            )
        ]
    ]

    num_table = Table(num_data, colWidths=[130, 410])
    num_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ebf8ff')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#90cdf4')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#bee3f8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(num_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 7: TIMELINE & ACTIONABLE FORECAST
    # =========================================================================
    story.append(Paragraph("7. CHRONOLOGICAL FULFILLMENT TIMELINE & ACTIONABLE FORECAST", sec_header))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_secondary, spaceBefore=1, spaceAfter=3))

    timeline_data = [
        [
            Paragraph("<b>Phased Forecast:</b>", table_cell_bold),
            Paragraph(response.primary_timeline_forecast.replace('\n', '<br/>'), table_cell)
        ],
        [
            Paragraph("<b>Lucky Numerological Days:</b>", table_cell_bold),
            Paragraph(f"{', '.join(response.numerology.lucky_days)} | Favorable Dates: {', '.join(map(str, response.numerology.lucky_numbers))}", table_cell)
        ]
    ]
    t_table = Table(timeline_data, colWidths=[130, 410])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fff4')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#9ae6b4')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#c6f6d5')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 6))

    # =========================================================================
    # SECTION 8: COMPREHENSIVE REMEDIES DOSSIER
    # =========================================================================
    story.append(Paragraph("8. ALL-INCLUSIVE MASTER REMEDIAL DOSSIER", sec_header))
    story.append(HRFlowable(width="100%", thickness=1.0, color=c_secondary, spaceBefore=1, spaceAfter=3))

    # Sacred Plants Table
    plant_rows = [
        [
            Paragraph("Sacred Plant / Tree", table_header),
            Paragraph("Pradakshinam Rounds", table_header),
            Paragraph("Auspicious Day & Time", table_header),
            Paragraph("Ritual Offerings & Sacred Sankalpa Shloka", table_header)
        ]
    ]
    for pl in response.remedies.sacred_plant_pradakshinams:
        plant_rows.append([
            Paragraph(f"<b>{pl.plant_name}</b><br/><i>({pl.botanical_name})</i>", table_cell),
            Paragraph(f"<b>{pl.prescribed_pradakshinam_rounds} Rounds</b><br/>(Clockwise)", table_cell_bold),
            Paragraph(f"<b>Day:</b> {pl.auspicious_day.split('(')[0]}<br/><b>Time:</b> {pl.auspicious_timing}", table_cell),
            Paragraph(f"<b>Offerings:</b> {pl.ritual_offerings[0]}<br/><b>Shloka:</b> <i>\"{pl.sacred_sankalpa_shloka}\"</i>", table_cell)
        ])

    plant_table = Table(plant_rows, colWidths=[120, 95, 115, 210])
    plant_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#22543d')),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#9ae6b4')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fff4')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(plant_table)
    story.append(Spacer(1, 6))

    # Mantras Table
    mantra_rows = [
        [
            Paragraph("Planetary Energy", table_header),
            Paragraph("Bija / Vedic Mantra", table_header),
            Paragraph("Prescribed Japa Count", table_header),
            Paragraph("Rosary (Mala), Time & Direction", table_header)
        ]
    ]
    for m in response.remedies.primary_mantras:
        mantra_rows.append([
            Paragraph(f"<b>{m.planet_or_deity}</b>", table_cell_bold),
            Paragraph(f"<b>Bija:</b> <i>\"{m.bija_mantra}\"</i><br/><b>Vedic:</b> <i>\"{m.vedic_mantra}\"</i>", table_cell),
            Paragraph(f"<b>{m.prescribed_japa_count:,} Recitations</b>", table_cell),
            Paragraph(f"<b>Mala:</b> {m.japa_mala}<br/><b>Time:</b> {m.optimal_time}<br/><b>Facing:</b> {m.facing_direction}", table_cell)
        ])

    mantra_table = Table(mantra_rows, colWidths=[105, 205, 95, 135])
    mantra_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(mantra_table)
    story.append(Spacer(1, 6))

    # Lal Kitab Totke & Gemstone
    gr = response.remedies.gemstone_rudraksha
    totke_items = "".join([f"• {upaya}<br/>" for upaya in response.remedies.lal_kitab_upayas[:3]])
    gem_summary = f"<b>Gemstone:</b> {gr.primary_gemstone} on {gr.finger_to_wear} ({gr.metal}) | <b>Rudraksha:</b> {gr.rudraksha_mukhi} | <b>Yantra:</b> {gr.sacred_yantra}"

    upaya_gem_data = [
        [
            Paragraph("<b>Lal Kitab Practical Totke:</b>", table_cell_bold),
            Paragraph(totke_items, table_cell)
        ],
        [
            Paragraph("<b>Gemstone & Rudraksha:</b>", table_cell_bold),
            Paragraph(gem_summary, table_cell)
        ]
    ]
    upaya_gem_table = Table(upaya_gem_data, colWidths=[130, 410])
    upaya_gem_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffaf0')),
        ('BOX', (0, 0), (-1, -1), 0.8, c_gold),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#fbd38d')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(upaya_gem_table)
    story.append(Spacer(1, 6))

    # Footer notice
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#cbd5e0'), spaceBefore=2, spaceAfter=2))
    story.append(Paragraph(
        "<i>Astrological Notice: This consultation dossier is prepared through classical shastric mathematical calculations. "
        "Astrological science reveals probabilities, timing trends, and remedial pathways to optimize human effort and free will.</i>",
        subtitle_style
    ))

    doc.build(story)
    return output_pdf_path
