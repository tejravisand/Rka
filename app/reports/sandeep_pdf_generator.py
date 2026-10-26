"""
Dedicated Astrological Consultation & Prediction PDF Generator for Sandeep R.
Comprehensive Multi-Page Consultation Report covering:
1. Present Job Status & Confirmation Timeline.
2. Govt Job vs Private Job Comparison, Probability & Remedies.
3. Abroad Job / Foreign Settlement Timeline.
4. Marriage Prediction: Timing, Arranged vs Love, Intercaste/Background, Wife Profile & Harmony.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)

from app.engines.sandeep_consultation import SandeepQADossier, SandeepConsultationEngine
from app.reports.pdf_generator import draw_south_indian_chart, draw_north_indian_chart
from app.core.vargas import calculate_all_vargas
from app.core.dasha import calculate_vimshottari_dashas, get_active_dasha
from app.core.constants import SHODASHAVARGA_INFO


def generate_sandeep_pdf_report(
    dossier: SandeepQADossier,
    output_pdf_path: str,
    location_name: str
) -> str:
    """Generate a publication-grade consultation report for Sandeep R."""
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
        'STitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        alignment=1,
        textColor=colors.HexColor('#1a365d')
    )
    subtitle_style = ParagraphStyle(
        'SSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#4a5568')
    )
    section_h = ParagraphStyle(
        'SSecH',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=10,
        spaceAfter=5
    )
    q_style = ParagraphStyle(
        'SQStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1a365d')
    )
    body_style = ParagraphStyle(
        'SBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#2d3748')
    )
    bold_body = ParagraphStyle(
        'SBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []
    kundali = dossier.kundali

    # =========================================================================
    # PAGE 1: COVER & HOROSCOPE OVERVIEW
    # =========================================================================
    story.append(Paragraph("VEDIC HOROSCOPE & PREDICTIVE CONSULTATION DOSSIER", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(f"Client: <b>{dossier.client_name}</b> | DOB: 05-Feb-2000, 07:45 AM IST | ESI Hospital, Rajajinagar, Bengaluru", subtitle_style))
    story.append(Spacer(1, 6))

    meta_data = [
        [Paragraph("<b>Lagna (Ascendant):</b>", body_style), Paragraph(f"<b>{kundali.ascendant.sign.sanskrit_name}</b> ({kundali.ascendant.degrees_in_sign:.2f}°)", body_style),
         Paragraph("<b>Janma Rasi (Moon):</b>", body_style), Paragraph(f"<b>{kundali.planets['Moon'].sign.sanskrit_name}</b> ({kundali.planets['Moon'].degrees_in_sign:.2f}°)", body_style)],
        [Paragraph("<b>Janma Nakshatra:</b>", body_style), Paragraph(f"{kundali.planets['Moon'].nakshatra_name} (Pada {kundali.planets['Moon'].nakshatra_pada})", body_style),
         Paragraph("<b>Surya Rasi (Sun):</b>", body_style), Paragraph(f"<b>{kundali.planets['Sun'].sign.sanskrit_name}</b> (6th House)", body_style)],
        [Paragraph("<b>Lahiri Ayanamsa:</b>", body_style), Paragraph(f"{kundali.ayanamsa_value:.4f}°", body_style),
         Paragraph("<b>Active Dasha (2026):</b>", body_style), Paragraph(f"<b>{dossier.active_dasha['mahadasha']} - {dossier.active_dasha['antardasha']}</b> ({dossier.active_dasha['pratyantardasha']})", body_style)]
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

    # Dual Charts
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
    story.append(Paragraph("2. Planetary Positions & Dignities (D1 Rasi)", section_h))
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
    # PAGE 2: EXECUTIVE VERDICTS & JOB STATUS / CONFIRMATION
    # =========================================================================
    story.append(Paragraph("3. Executive Verdict Matrix for Sandeep R", section_h))

    sum_matrix = [
        [Paragraph("<b>Core Question</b>", bold_body), Paragraph("<b>Astrological Verdict</b>", bold_body), Paragraph("<b>Timeline / Key Dates</b>", bold_body)],
        [
            Paragraph("<b>1. Current Job Confirmation?</b>", body_style),
            Paragraph("<font color='#22543d'><b>CONFIRMED WITH CERTAINTY</b></font>", body_style),
            Paragraph("<b>Jan 2027 – Apr 2027</b> (Probation cleared)", body_style)
        ],
        [
            Paragraph("<b>2. Govt Job Possibility vs Private?</b>", body_style),
            Paragraph("<b>65%–70% Govt Chance</b>. Dual-track advised.", body_style),
            Paragraph("Window open until <b>July 2027</b> (Rahu-Sun)", body_style)
        ],
        [
            Paragraph("<b>3. Abroad Job / Foreign Travel?</b>", body_style),
            Paragraph("<font color='#22543d'><b>100% CONFIRMED</b></font> (Rahu in 12th House)", body_style),
            Paragraph("• Wave 1: <b>Jul 2027 – Jan 2029</b><br/>• Settlement: <b>2029 – 2032</b>", body_style)
        ],
        [
            Paragraph("<b>4. When will he marry? (Age & Date)</b>", body_style),
            Paragraph("<b>Age 28.5 to 29 Years</b>", body_style),
            Paragraph("<b>Mid-2028 to Early 2029</b> (Rahu-Moon)", body_style)
        ],
        [
            Paragraph("<b>5. Love vs Arranged?</b>", body_style),
            Paragraph("<b>Arranged-cum-Love</b> (Self-Choice + Family)", body_style),
            Paragraph("Met through professional/education circle", body_style)
        ],
        [
            Paragraph("<b>6. Intercaste or Relatives? Origin?</b>", body_style),
            Paragraph("<b>Inter-subcaste / Different community</b>.<br/><b>Far-off place (NOT relatives)</b>.", body_style),
            Paragraph("Different city/state/overseas location", body_style)
        ],
        [
            Paragraph("<b>7. Wife Supportive? Marriage Life?</b>", body_style),
            Paragraph("<font color='#22543d'><b>HIGHLY SUPPORTIVE & WORKING</b></font><br/>Harmony: <b>8.0 / 10</b> (Very Prosperous)", body_style),
            Paragraph("Venus in own sign in D9 Navamsa", body_style)
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

    # Detailed Job Confirmation Section
    jc = dossier.job_confirmation
    story.append(Paragraph("4. Present Job Status & Exact Confirmation Timeline", section_h))
    jc_box = [
        [Paragraph("<b>Question: What is his present job status? Will the current job be confirmed or not, and what is the timeline?</b>", q_style)],
        [Paragraph(f"<b>Current Situation:</b> {jc.current_status}", body_style)],
        [Paragraph(f"<b>Confirmation Verdict:</b> {jc.confirmation_verdict}", body_style)],
        [Paragraph(f"<b>Exact Timeline for Confirmation:</b><br/>{jc.confirmation_timeline.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph(f"<b>Probation Clearance Factors:</b> {jc.probation_clearance_factors}", body_style)],
        [Paragraph("<b>Recommended Immediate Actions:</b><br/>• " + "<br/>• ".join(jc.immediate_actions), body_style)]
    ]
    jc_t = Table(jc_box, colWidths=[520])
    jc_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#cbd5e0')),
        ('LINEBELOW', (0, 3), (-1, 3), 0.5, colors.HexColor('#cbd5e0')),
    ]))
    story.append(jc_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: GOVT JOB VS PRIVATE JOB & REMEDIES
    # =========================================================================
    gv = dossier.govt_vs_private
    story.append(Paragraph("5. Government Job vs. Private Job Comparison & Remedies", section_h))

    story.append(Paragraph(f"<b>Government Job Probability: {gv.govt_job_probability}</b>", bold_body))
    story.append(Paragraph("Sandeep R's Lagna Lord Sun sits in the 6th house (Shatru/Competition Bhava) and is <b>EXALTED in Aries in D10 Dasamsa</b>. This gives strong capability to clear competitive government examinations.", body_style))
    story.append(Spacer(1, 4))

    # Comparative Table
    comp_rows = [[Paragraph("<b>Feature</b>", bold_body), Paragraph("<b>Government Sector</b>", bold_body), Paragraph("<b>Private / MNC Sector</b>", bold_body)]]
    for feat, govt_f, pvt_f in gv.comparative_matrix:
        comp_rows.append([
            Paragraph(f"<b>{feat}</b>", body_style),
            Paragraph(govt_f, body_style),
            Paragraph(pvt_f, body_style)
        ])
    comp_t = Table(comp_rows, colWidths=[120, 200, 200])
    comp_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(comp_t)
    story.append(Spacer(1, 8))

    # Strategic Verdict Box
    gv_box = [
        [Paragraph("<b>Strategic Career Verdict:</b>", q_style)],
        [Paragraph(gv.strategic_career_verdict, body_style)],
        [Paragraph("<b>Target Government Sectors:</b><br/>• " + "<br/>• ".join(gv.govt_job_sectors), body_style)],
        [Paragraph("<b>Astrological Remedies to Secure / Confirm Job:</b><br/>• " + "<br/>• ".join(gv.effective_remedies), body_style)]
    ]
    gv_box_t = Table(gv_box, colWidths=[520])
    gv_box_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffaf0')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dd6b20')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.HexColor('#feebc8')),
    ]))
    story.append(gv_box_t)
    story.append(Spacer(1, 10))

    # =========================================================================
    # ABROAD JOB SECTION
    # =========================================================================
    ab = dossier.abroad_job
    story.append(Paragraph("6. Abroad Job & Foreign Travel Prediction", section_h))

    ab_box = [
        [Paragraph(f"<b>Abroad Job Possibility: {ab.abroad_possibility}</b>", q_style)],
        [Paragraph(f"<b>Astrological Drivers:</b> {ab.astrological_drivers}", body_style)],
        [Paragraph(f"<b>Timeline for First Overseas Opportunity:</b> <b>{ab.timeline_first_wave}</b>", body_style)],
        [Paragraph(f"<b>Timeline for Long-term Foreign Relocation:</b> <b>{ab.timeline_longterm_relocation}</b>", body_style)],
        [Paragraph("<b>Target Geographies & Profile:</b><br/>• " + "<br/>• ".join(ab.target_geographies) + f"<br/><i>Role Profile: {ab.career_profile_abroad}</i>", body_style)]
    ]
    ab_t = Table(ab_box, colWidths=[520])
    ab_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ebf8ff')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3182ce')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(ab_t)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: MARRIAGE, SPOUSE, HARMONY & QUALITIES
    # =========================================================================
    m_info = dossier.marriage
    story.append(Paragraph("7. Marriage Prediction & Relationship Analysis", section_h))

    m_table_data = [
        [Paragraph("<b>Consultation Dimension</b>", bold_body), Paragraph("<b>Astrological Analysis & Prediction for Sandeep R</b>", bold_body)],
        [
            Paragraph("<b>When will he marry? (Timing & Age)</b>", body_style),
            Paragraph(f"<b>{m_info.marriage_timing}</b><br/>Ideal Age at Wedding: <b>{m_info.ideal_age_at_marriage}</b>.<br/>Alliance finalization begins in late 2027; wedding solemnized in 2028/early 2029.", body_style)
        ],
        [
            Paragraph("<b>Love vs. Arranged Marriage?</b>", body_style),
            Paragraph(f"<b>{m_info.marriage_type}</b>.<br/>Venus sits in the 5th house (Purva Ashadha - romantic inclinations), while 7th Lord Saturn is in the 9th with Jupiter. He will date, select, or know the partner through work/study, followed by full family arrangement.", body_style)
        ],
        [
            Paragraph("<b>Intercaste or Inter-religion?</b>", body_style),
            Paragraph(f"<b>{m_info.caste_and_background}</b>", body_style)
        ],
        [
            Paragraph("<b>Within Relatives or Far-Off Place?</b>", body_style),
            Paragraph(f"<b>{m_info.geographical_origin}</b>.<br/>7th Lord Saturn in 9th house (distance) and Rahu in 12th house (foreign/distant) strictly indicate a spouse from outside family kinship circles.", body_style)
        ],
        [
            Paragraph("<b>Wife's Nature & Career</b>", body_style),
            Paragraph(f"<b>{m_info.wife_personality_and_career}</b>", body_style)
        ],
        [
            Paragraph("<b>Marital Life Quality & Harmony</b>", body_style),
            Paragraph(f"<b>Harmony Score: {m_info.marital_harmony_score}</b>.<br/>Marriage brings significant financial luck, stability, and societal respect. Post-marriage fortunes rise rapidly.", body_style)
        ],
        [
            Paragraph("<b>Remedies & Cautionary Notes</b>", body_style),
            Paragraph("• " + "<br/>• ".join(m_info.potential_challenges_and_remedies), body_style)
        ]
    ]
    m_table = Table(m_table_data, colWidths=[140, 380])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 10))

    # Divisional Chart Foundations Table
    story.append(Paragraph("8. Astrological Foundations (D1, D9 Navamsa, D10 Dasamsa)", section_h))
    found_data = [
        [Paragraph("<b>Chart</b>", bold_body), Paragraph("<b>Key Configuration in Sandeep R's Horoscope</b>", bold_body), Paragraph("<b>Real-Life Manifestation</b>", bold_body)],
        [
            Paragraph("<b>D1 Rasi</b>", body_style),
            Paragraph("Leo Lagna, Sun+Moon+Ketu in 6th, Mercury in 7th, Rahu in 12th", body_style),
            Paragraph("Shatru-hanta Yoga (destroying competition); strong overseas inclination.", body_style)
        ],
        [
            Paragraph("<b>D9 Navamsa</b>", body_style),
            Paragraph("Gemini Lagna, <b>Venus in OWN sign (Libra) in 5th</b>, Moon Exalted in Taurus", body_style),
            Paragraph("Guarantees an attractive, loving, accomplished, and supportive wife.", body_style)
        ],
        [
            Paragraph("<b>D10 Dasamsa</b>", body_style),
            Paragraph("Libra Lagna, <b>Sun EXALTED in Aries in 7th</b>, Mars in own sign Scorpio", body_style),
            Paragraph("High administrative status, authority, and ability to clear exams/gain promotion.", body_style)
        ],
        [
            Paragraph("<b>Active Dasha</b>", body_style),
            Paragraph("Rahu Mahadasha (in 12th House) – Sun Antardasha (Lagna Lord)", body_style),
            Paragraph("Period of formal job confirmation, career elevation, and overseas groundwork.", body_style)
        ]
    ]
    found_t = Table(found_data, colWidths=[80, 240, 200])
    found_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(found_t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<i>Prepared for Sandeep R under the principles of Brihat Parasara Hora Sastra using the Lahiri Ayanamsa.</i>", subtitle_style))

    doc.build(story)
    return output_pdf_path
