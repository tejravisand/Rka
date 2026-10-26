"""
Dedicated Q&A Consultation PDF Report Generator for Ravi Kumar S.
Focuses specifically on:
1. Career, Promotion, Salary Increment, Company Tenure, Job Change & Own Business.
2. Real Estate: Denkanikottai/Hosur Land, Keep vs Sell, Profit vs Loss, Ideal Selling Timeline.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

from app.engines.qa_consultation import ComprehensiveQADossier, QAConsultationEngine
from app.core.kundali import calculate_kundali


def generate_qa_consultation_pdf(
    dossier: ComprehensiveQADossier,
    output_pdf_path: str
) -> str:
    """Generate a clean, executive Q&A consultation PDF."""
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
        'QATitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#1a365d')
    )
    subtitle_style = ParagraphStyle(
        'QASub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#4a5568')
    )
    section_h1 = ParagraphStyle(
        'QASecH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=12,
        spaceAfter=6
    )
    question_style = ParagraphStyle(
        'QAQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1a365d')
    )
    verdict_style = ParagraphStyle(
        'QAVerdict',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#c53030')
    )
    verdict_green = ParagraphStyle(
        'QAVerdictGreen',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#22543d')
    )
    body_style = ParagraphStyle(
        'QABody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#2d3748')
    )
    body_bold = ParagraphStyle(
        'QABold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("VEDIC ASTROLOGICAL CONSULTATION & ADVISORY DOSSIER", title_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("CONFIDENTIAL REPORT ON CAREER TRAJECTORY & REAL ESTATE LIQUIDATION", subtitle_style))
    story.append(Spacer(1, 8))

    # Client Info Table
    kundali = dossier.kundali
    meta_table_data = [
        [Paragraph("<b>Client Name:</b>", body_style), Paragraph(f"<b>{dossier.client_name}</b>", body_style),
         Paragraph("<b>Lagna (Ascendant):</b>", body_style), Paragraph(f"<b>{kundali.ascendant.sign.sanskrit_name}</b> ({kundali.ascendant.degrees_in_sign:.2f}°)", body_style)],
        [Paragraph("<b>Date of Birth:</b>", body_style), Paragraph("20-Nov-1968, 03:45 AM IST", body_style),
         Paragraph("<b>Janma Rasi (Moon):</b>", body_style), Paragraph(f"<b>{kundali.planets['Moon'].sign.sanskrit_name}</b> ({kundali.planets['Moon'].degrees_in_sign:.2f}°)", body_style)],
        [Paragraph("<b>Place of Birth:</b>", body_style), Paragraph("Malleshwaram, Bengaluru, India", body_style),
         Paragraph("<b>Janma Nakshatra:</b>", body_style), Paragraph(f"{kundali.planets['Moon'].nakshatra_name} (Pada {kundali.planets['Moon'].nakshatra_pada})", body_style)],
        [Paragraph("<b>Active Dasha:</b>", body_style), Paragraph(f"<b>{dossier.active_dasha['mahadasha']} - {dossier.active_dasha['antardasha']}</b> ({dossier.active_dasha['pratyantardasha']})", body_style),
         Paragraph("<b>Upcoming Dasha:</b>", body_style), Paragraph("<b>Venus - Jupiter</b> (From Dec 2027)", body_style)]
    ]
    meta_table = Table(meta_table_data, colWidths=[105, 155, 105, 155])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#edf2f7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Verdict Matrix
    story.append(Paragraph("Executive Verdict Matrix (Quick Summary)", section_h1))
    summary_matrix = [
        [Paragraph("<b>Core Question</b>", body_bold), Paragraph("<b>Astrological Verdict</b>", body_bold), Paragraph("<b>Key Timeline / Date</b>", body_bold)],
        [
            Paragraph("<b>1. Promotion & Salary Increment?</b>", body_style),
            Paragraph("<font color='#22543d'><b>CONFIRMED</b></font> (Two-phase elevation)", body_style),
            Paragraph("• Phase 1: <b>Feb – Apr 2027</b><br/>• Phase 2: <b>Dec 2027 – Apr 2028</b>", body_style)
        ],
        [
            Paragraph("<b>2. Remaining Tenure in Current Company?</b>", body_style),
            Paragraph("<b>1.0 to 1.5 Years</b> (Until late 2027)", body_style),
            Paragraph("Transition window opens <b>late 2027</b>", body_style)
        ],
        [
            Paragraph("<b>3. Is this his last company? New Job?</b>", body_style),
            Paragraph("<b>NO, NOT LAST COMPANY.</b> Definite job pivot or independent venture.", body_style),
            Paragraph("New role / enterprise: <b>Dec 2027 – mid 2028</b>", body_style)
        ],
        [
            Paragraph("<b>4. Can he start his own company?</b>", body_style),
            Paragraph("<font color='#22543d'><b>HIGHLY RECOMMENDED</b></font> (Guru-Mangala Yoga)", body_style),
            Paragraph("Optimal Launch: <b>Dec 2027 – Aug 2028</b>", body_style)
        ],
        [
            Paragraph("<b>5. Denkanikottai/Hosur Land: Keep or Sell?</b>", body_style),
            Paragraph("<font color='#2b6cb0'><b>KEEP (HOLD) FOR NOW</b></font>. Do not sell in 2026.", body_style),
            Paragraph("Selling in 2026 = undervaluation.<br/>Hold until <b>late 2027 / 2028</b>", body_style)
        ],
        [
            Paragraph("<b>6. Profit or Loss on Land Sale?</b>", body_style),
            Paragraph("<font color='#22543d'><b>SUBSTANTIAL PROFIT (NO LOSS)</b></font>", body_style),
            Paragraph("Exalted Venus in D4 guarantees strong appreciation", body_style)
        ],
        [
            Paragraph("<b>7. When will the Land Sale happen?</b>", body_style),
            Paragraph("<b>Best Window: Apr 2028 – Sep 2028</b><br/>(Early window: Aug 2027 – Nov 2027)", body_style),
            Paragraph("Under Venus-Jupiter-Saturn dasha", body_style)
        ]
    ]
    sum_table = Table(summary_matrix, colWidths=[160, 190, 170])
    sum_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sum_table)
    story.append(Spacer(1, 12))

    # SECTION 1: CAREER & PROFESSIONAL TRAJECTORY
    c_qa = dossier.career_qa
    story.append(Paragraph("Part I: Detailed Career, Job & Enterprise Consultation", section_h1))

    c_box = [
        [Paragraph("<b>Question 1.1: What is the status in the current company? When will promotion and increment happen?</b>", question_style)],
        [Paragraph(f"<b>Current Situation:</b> {c_qa.current_status}", body_style)],
        [Paragraph(f"<b>Astrological Verdict:</b> {c_qa.promotion_increment_verdict}", body_style)],
        [Paragraph(f"<b>Exact Timeline for Promotion & Increment:</b><br/>{c_qa.promotion_timeline.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph("<b>Question 1.2: How many years will he work in the present company? Is this his last company?</b>", question_style)],
        [Paragraph(f"<b>Tenure Forecast:</b> {c_qa.company_tenure_forecast}", body_style)],
        [Paragraph(f"<b>Job Change / Next Chapter:</b> {c_qa.job_change_vs_last_company}", body_style)],
        [Paragraph("<b>Question 1.3: Whether he can start his own company?</b>", question_style)],
        [Paragraph(f"<b>Feasibility & Strength:</b> {c_qa.own_business_feasibility}", body_style)],
        [Paragraph(f"<b>Best Business Sectors:</b><br/>• " + "<br/>• ".join(c_qa.best_business_domains), body_style)],
        [Paragraph(f"<b>Optimal Launch Window:</b> <b>{c_qa.best_business_launch_window}</b>", body_style)],
        [Paragraph("<b>Strategic Career Advice for Ravi Kumar S:</b><br/>• " + "<br/>• ".join(c_qa.strategic_career_advice), body_style)]
    ]
    career_table = Table(c_box, colWidths=[520])
    career_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 3), (-1, 3), 0.5, colors.HexColor('#cbd5e0')),
        ('LINEBELOW', (0, 6), (-1, 6), 0.5, colors.HexColor('#cbd5e0')),
    ]))
    story.append(career_table)

    story.append(PageBreak())

    # SECTION 2: REAL ESTATE & LAND IN DENKANIKOTTAI / HOSUR
    r_qa = dossier.real_estate_qa
    story.append(Paragraph("Part II: Real Estate Consultation — Denkanikottai / Hosur Land", section_h1))

    r_box = [
        [Paragraph("<b>Subject Property:</b> Land plot in Denkanikottai (Denkanikotta), near Hosur, Krishnagiri District, Tamil Nadu.", question_style)],
        [Paragraph(f"<b>Astrological Land Analysis:</b> {r_qa.current_market_astrology}", body_style)],
        [Paragraph("<b>Question 2.1: Whether to KEEP the land or SELL it right now?</b>", question_style)],
        [Paragraph(f"<b>Verdict:</b> {r_qa.keep_vs_sell_verdict.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph("<b>Question 2.2: Will he get PROFIT or LOSS on this land?</b>", question_style)],
        [Paragraph(f"<b>Profitability Analysis:</b> {r_qa.profit_vs_loss_verdict}", body_style)],
        [Paragraph("<b>Question 2.3: WHEN will the sale happen if he decides to liquidate?</b>", question_style)],
        [Paragraph(f"<b>Optimal Timing for Sale:</b><br/>{r_qa.best_selling_window.replace(chr(10), '<br/>')}", body_style)],
        [Paragraph(f"<b>Financial Outcome:</b> {r_qa.financial_outcome_forecast}", body_style)],
        [Paragraph("<b>Strategic Real Estate Guidelines:</b><br/>• " + "<br/>• ".join(r_qa.strategic_real_estate_advice), body_style)],
        [Paragraph("<b>Remedies for Smooth Land Realization & Maximized Value:</b><br/>• " + "<br/>• ".join(r_qa.remedy_for_smooth_transaction), body_style)]
    ]
    re_table = Table(r_box, colWidths=[520])
    re_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fff4')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#68d391')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 1), (-1, 1), 0.5, colors.HexColor('#c6f6d5')),
        ('LINEBELOW', (0, 3), (-1, 3), 0.5, colors.HexColor('#c6f6d5')),
        ('LINEBELOW', (0, 5), (-1, 5), 0.5, colors.HexColor('#c6f6d5')),
        ('LINEBELOW', (0, 8), (-1, 8), 0.5, colors.HexColor('#c6f6d5')),
    ]))
    story.append(re_table)
    story.append(Spacer(1, 12))

    # SECTION 3: ASTROLOGICAL MECHANICS & SCRIPTURAL REFERENCES
    story.append(Paragraph("Part III: Astrological Foundations & Divisional Chart Mechanics", section_h1))
    notes_data = [
        [Paragraph("<b>Astrological Factor</b>", body_bold), Paragraph("<b>Classical Mechanism in Ravi Kumar S's Kundali</b>", body_bold)],
        [
            Paragraph("<b>D10 Dasamsa (Career)</b>", body_style),
            Paragraph("Cancer Lagna in D10 with <b>Jupiter EXALTED in 1st house</b>, Moon in OWN sign, and Sun in OWN sign in 2nd house. This establishes an executive leader / independent authority profile rather than a subservient employee.", body_style)
        ],
        [
            Paragraph("<b>D4 Chaturthamsa (Land)</b>", body_style),
            Paragraph("Sagittarius Lagna in D4 with <b>Jupiter in OWN sign in 1st house</b>, Mars (Bhumi Karaka) in friendly sign, and <b>Venus EXALTED in 4th house (Pisces)</b>. Real estate purchased under his chart commands exceptional long-term capital multiplication.", body_style)
        ],
        [
            Paragraph("<b>7th Kendra Raja Yoga</b>", body_style),
            Paragraph("Lagna Lord Jupiter combines with 9th Lord Mars in Virgo, forming a textbook Kendra-Trikona Raja Yoga. This guarantees commercial success in partnership and independent ventures.", body_style)
        ],
        [
            Paragraph("<b>Dasha Shift (Dec 2027)</b>", body_style),
            Paragraph("Transition from Venus-Rahu into <b>Venus-Jupiter</b> activates the 10th and 7th houses simultaneously, triggering major financial appreciation and professional autonomy.", body_style)
        ]
    ]
    notes_table = Table(notes_data, colWidths=[150, 370])
    notes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<i>Prepared for Ravi Kumar S under the principles of Brihat Parasara Hora Sastra and Jaimini Sutras.</i>", subtitle_style))

    doc.build(story)
    return output_pdf_path
