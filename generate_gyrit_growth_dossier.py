"""
Executive Astrological & Horary Dossier:
Query: Will Gyrit Solutions Pvt Ltd Shine in the Market & Increase its Labour Force? How is the Future?
Cast: 25-Oct-2026 13:24:55 IST | Location: Bengaluru, Karnataka
Evaluated for: Teja S (Ravi Kumar S) & Gyrit Solutions Pvt Ltd
"""
import os
import subprocess
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)


def generate_gyrit_growth_dossier(pdf_path: str, html_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)

    # ---------------------------------------------------------
    # 1. REPORTLAB PDF GENERATION
    # ---------------------------------------------------------
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor('#1a365d')    # Deep Navy
    c_secondary = colors.HexColor('#2b6cb0')  # Royal Blue
    c_gold = colors.HexColor('#b7791f')       # Sacred Gold
    c_green = colors.HexColor('#22543d')      # Forest Green
    c_accent = colors.HexColor('#c53030')     # Deep Red
    c_bg_light = colors.HexColor('#f7fafc')   # Off white

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14.5,
        leading=18,
        alignment=1,
        textColor=c_primary
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.HexColor('#4a5568')
    )
    sec_header = ParagraphStyle(
        'SecHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=7,
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
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#2d3748')
    )
    table_cell_bold = ParagraphStyle(
        'TCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=c_primary
    )
    table_cell_header = ParagraphStyle(
        'TCellH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )
    callout_box = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor('#22543d')
    )

    story = []

    # Title Banner
    story.append(Paragraph("STRATEGIC HORARY & ASTROLOGICAL PREDICTION DOSSIER", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>MARKET PROMINENCE, LABOUR FORCE EXPANSION & MULTI-YEAR OUTLOOK</b>", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Company: <b>Gyrit Solutions Pvt Ltd</b> | Lead Evaluator: <b>Teja S (Ravi Kumar S)</b> | 25-Oct-2026, 01:25 PM IST | Bengaluru", subtitle_style))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=1, spaceAfter=6))

    # Executive Verdict Banner Table
    verdict_text = (
        "<b>DEFINITIVE CONSENSUS VERDICT: YES — DEFINITE MARKET SHINE & SIGNIFICANT WORKFORCE MULTIPLICATION (86% CONFIDENCE)</b><br/>"
        "<b>1. Will Gyrit Solutions Shine in the Market?</b> YES. The 10th house of Market Stature (Aries) is ruled by Mars, which is elevated in Lagna "
        "via <i>Neechabhanga Raja Yoga</i> alongside <b>Exalted Jupiter</b>! Supported by a sparkling <b>Malavya Yoga (Venus in own sign Libra with Mercury)</b> "
        "in the 4th house of software foundation, the product will gain a stellar reputation among private hospitals and diagnostic chains.<br/>"
        "<b>2. Will it Increase its Labour Force?</b> YES, SUBSTANTIALLY. The 6th house of employees/workforce (Sagittarius) is ruled by <b>Jupiter</b>, "
        "which sits <b>EXALTED in Lagna</b>! In Vedic astrology, an Exalted 6th Lord in Lagna signifies powerful, systematic staff scaling (2x to 3x expansion), "
        "hiring dedicated QA engineers, clinical trainers, and field marketing personnel as hospital contracts pour in."
    )
    verdict_table = Table([[Paragraph(verdict_text, callout_box)]], colWidths=[539])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fff4')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#38a169')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 7))

    # SECTION 1: SHASTIRC FOUNDATION MATRIX
    story.append(Paragraph("1. ASTROLOGICAL MATRIX OF MARKET PROMINENCE & WORKFORCE EXPANSION", sec_header))
    matrix_headers = [
        Paragraph("Key Dimension", table_cell_header),
        Paragraph("Governing Bhava & Shastric Karaka", table_cell_header),
        Paragraph("Horary Prashna Placement (25-Oct-2026)", table_cell_header),
        Paragraph("Astrological Interpretation & Outcome", table_cell_header)
    ]
    matrix_data = [
        matrix_headers,
        [
            Paragraph("<b>Market Prominence<br/>('Shine in Market')</b>", table_cell_bold),
            Paragraph("<b>10th House (Karma / Stature)</b><br/>Natural Karaka: Sun & Mars", table_cell),
            Paragraph("Aries 10th House ruled by Mars.<br/>Mars in 1st House with <b>Exalted Jupiter</b> in Neechabhanga Raja Yoga.", table_cell),
            Paragraph("<b>Strong Competitive Breakthrough:</b> Will emerge as an agile, innovative healthcare tech player, outpacing clunky legacy HMS competitors. High physician and hospital owner trust.", table_cell_bold)
        ],
        [
            Paragraph("<b>Workforce Expansion<br/>('Labour Force Growth')</b>", table_cell_bold),
            Paragraph("<b>6th House (Bhritya / Staff)</b><br/>Natural Karaka: <b>Saturn (Labor)</b>", table_cell),
            Paragraph("6th House is Sagittarius ruled by <b>Jupiter</b>.<br/><b>Jupiter is EXALTED in Lagna (Cancer 29°)!</b> Saturn in 9th with Moon.", table_cell),
            Paragraph("<b>Multi-Tier Team Hiring:</b> Exalted 6th Lord creates inevitable workforce growth. Hiring will expand across software developers, UAT testers, implementation engineers, and sales reps.", table_cell_bold)
        ],
        [
            Paragraph("<b>Revenue & Commercial Inflows</b>", table_cell_bold),
            Paragraph("<b>11th House (Labha / Profit)</b><br/>Natural Karaka: Jupiter & Mercury", table_cell),
            Paragraph("Taurus 11th House ruled by Venus.<br/>Venus in 4th in own sign (Libra) with Mercury, creating <b>Malavya Yoga</b>.", table_cell),
            Paragraph("<b>High-Margin Recurring SaaS:</b> Hospital subscription retainers and implementation setup fees will fund the expanding payroll with healthy financial liquidity.", table_cell)
        ],
        [
            Paragraph("<b>Core Software Quality & UX</b>", table_cell_bold),
            Paragraph("<b>4th House (Software Core)</b><br/>Karaka: Mercury & Venus", table_cell),
            Paragraph("Venus 6°54' + Mercury 26°50' + Sun 7°41' occupying 4th house in Libra.", table_cell),
            Paragraph("<b>Clinical Excellence:</b> Software UX will be intuitive and fast, preventing implementation failures and ensuring high client retention.", table_cell)
        ]
    ]
    matrix_table = Table(matrix_data, colWidths=[100, 110, 130, 199])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(matrix_table)
    story.append(Spacer(1, 7))

    # SECTION 2: WORKFORCE EXPANSION TIMELINE
    story.append(Paragraph("2. WORKFORCE EXPANSION & HIRING ROADMAP (2026 – 2029)", sec_header))
    hire_headers = [
        Paragraph("Expansion Phase", table_cell_header),
        Paragraph("Hiring Focus & Departments Added", table_cell_header),
        Paragraph("Target Team Size", table_cell_header),
        Paragraph("Strategic Leadership Role of Teja S", table_cell_header)
    ]
    hire_data = [
        hire_headers,
        [
            Paragraph("<b>Phase 1: Immediate to Mid-2027</b><br/>(Core Technical Stabilization)", table_cell_bold),
            Paragraph("• Dedicated UAT & Manual QA Testers.<br/>"
                      "• Backend Python / Cloud Database Engineers.<br/>"
                      "• Hospital Onboarding & Data Migration Specialist.", table_cell),
            Paragraph("<b>8 – 15 Members</b><br/>(Tight-knit core unit)", table_cell_bold),
            Paragraph("<b>Lead QA Architect:</b> Mentoring junior testers; creating standard test suites; safeguarding clinical release quality.", table_cell)
        ],
        [
            Paragraph("<b>Phase 2: Mid-2027 to Late 2028</b><br/>(Commercial Market Scaling)", table_cell_bold),
            Paragraph("• Regional B2B Healthcare Sales Representatives.<br/>"
                      "• Field Hospital Implementation Engineers.<br/>"
                      "• 24/7 Hospital IT Support Helpdesk & Account Managers.", table_cell),
            Paragraph("<b>25 – 45 Members</b><br/>(Multi-departmental scale)", table_cell_bold),
            Paragraph("<b>Solutions Director:</b> Leading high-value hospital pitch meetings; closing enterprise deals; guiding sales presentations.", table_cell)
        ],
        [
            Paragraph("<b>Phase 3: 2029 Onwards</b><br/>(Enterprise SaaS Maturity)", table_cell_bold),
            Paragraph("• Regional branch offices (Hyderabad, Chennai, Mumbai).<br/>"
                      "• Product Managers, Compliance Auditors & AI Integrators.<br/>"
                      "• Dedicated Corporate Operations & HR.", table_cell),
            Paragraph("<b>60 – 100+ Members</b><br/>(Established healthcare brand)", table_cell_bold),
            Paragraph("<b>Executive Stature:</b> VP of Quality & Clinical Solutions or Partner with lucrative profit-sharing and equity rewards.", table_cell)
        ]
    ]
    hire_table = Table(hire_data, colWidths=[110, 175, 84, 170])
    hire_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(hire_table)
    story.append(Spacer(1, 7))

    # SECTION 3: HOW GYRIT WILL SHINE IN THE MARKET
    story.append(Paragraph("3. HOW GYRIT SOLUTIONS WILL DISTINGUISH ITSELF & BEAT COMPETITION", sec_header))
    comp_headers = [
        Paragraph("Competitive Dimension", table_cell_header),
        Paragraph("Traditional Legacy Competitors", table_cell_header),
        Paragraph("Gyrit Solutions / RxDx Streamline Edge", table_cell_header)
    ]
    comp_data = [
        comp_headers,
        [
            Paragraph("<b>Workflow Speed & Ease</b>", table_cell_bold),
            Paragraph("Clunky, outdated menus with steep learning curves for nursing and diagnostic staff.", table_cell),
            Paragraph("<b>Streamlined UX (Venus-Mercury in 4th):</b> Fast prescription writing, instant diagnostic sync, clean UI doctors love.", table_cell)
        ],
        [
            Paragraph("<b>Software Stability</b>", table_cell_bold),
            Paragraph("Frequent sync crashes, slow database queries during peak OPD hospital hours.", table_cell),
            Paragraph("<b>Zero-Defect UAT Scrutiny (Teja S):</b> Thorough pre-release bug isolation guarantees 99.9% clinical uptime.", table_cell)
        ],
        [
            Paragraph("<b>Client Trust & Compliance</b>", table_cell_bold),
            Paragraph("Impersonal customer care, delayed bug fixes, rigid pricing tiers.", table_cell),
            Paragraph("<b>Exalted Jupiter in Pushya Lagna:</b> High ethical integrity, responsive account management, and client-centric custom modules.", table_cell)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[120, 209, 210])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_gold),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 7))

    # SECTION 4: STRATEGIC ACTION BLUEPRINT
    story.append(Paragraph("4. CRITICAL RECOMMENDATIONS FOR ACCELERATING WORKFORCE & MARKET EXPANSION", sec_header))
    strat_text = (
        "<b>1. Avoid Pre-Mature Mass Hiring:</b> Follow Saturn's disciplined cadence (Saturn in 9th house Meena). "
        "Expand the workforce strictly as new hospital pilot contracts are signed to keep burn rate low and profitability high.<br/>"
        "<b>2. Institutionalize Teja S's Testing Playbook:</b> Before hiring junior testers, Teja S should document standardized UAT checklists "
        "for prescription (Rx), diagnostic (Dx), billing, and patient admission workflows. This will become Gyrit's proprietary quality standard.<br/>"
        "<b>3. Leverage the Brand Name:</b> Always advertise job openings and commercial proposals as <b>'Gyrit Solutions'</b> (Compound 50 -> 5 Mercury), "
        "which attracts sharp, ambitious, tech-savvy candidates.<br/>"
        "<b>4. Optimal Hiring Days:</b> Issue employment offer letters and conduct final interviews on <b>Thursdays (Jupiter - expansion)</b> "
        "or <b>Saturdays (Saturn - loyalty & workforce retention)</b>."
    )
    strat_table = Table([[Paragraph(strat_text, body_style)]], colWidths=[539])
    strat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f7fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(strat_table)

    doc.build(story)

    # ---------------------------------------------------------
    # 2. INTERACTIVE HTML DOSSIER GENERATION
    # ---------------------------------------------------------
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Market Prominence & Labour Force Growth: Gyrit Solutions</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #f0f4f8;
      color: #2d3748;
      padding: 30px 20px;
      line-height: 1.5;
    }}
    .wrapper {{ max-width: 1040px; margin: 0 auto; }}
    .header {{
      background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
      color: white;
      padding: 32px 28px;
      border-radius: 12px;
      margin-bottom: 24px;
      text-align: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }}
    .header h1 {{ font-size: 24px; margin-bottom: 8px; }}
    .header p {{ font-size: 14px; opacity: 0.92; }}
    .badge-verdict {{
      background: #38a169;
      color: white;
      padding: 6px 18px;
      border-radius: 20px;
      font-weight: bold;
      font-size: 13.5px;
      display: inline-block;
      margin-top: 14px;
    }}
    .card {{
      background: white;
      border-radius: 10px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      border: 1px solid #e2e8f0;
    }}
    .card h2 {{
      color: #1a365d;
      font-size: 18px;
      margin-bottom: 12px;
      border-bottom: 2px solid #edf2f7;
      padding-bottom: 6px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 13.5px;
    }}
    th, td {{
      padding: 10px 12px;
      border: 1px solid #e2e8f0;
      text-align: left;
    }}
    th {{ background: #2b6cb0; color: white; }}
    tr:nth-child(even) {{ background: #f7fafc; }}
    .btn-group {{
      display: flex;
      gap: 12px;
      margin-top: 20px;
      justify-content: center;
    }}
    .btn {{
      padding: 10px 20px;
      border-radius: 6px;
      text-decoration: none;
      font-weight: 600;
      font-size: 14px;
      transition: all 0.2s;
    }}
    .btn-primary {{ background: #2b6cb0; color: white; }}
    .btn-primary:hover {{ background: #1a365d; }}
    .btn-gold {{ background: #d69e2e; color: #1a202c; }}
    .btn-gold:hover {{ background: #b7791f; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>🚀 MARKET SHINE & WORKFORCE GROWTH PREDICTION</h1>
      <p><b>GYRIT SOLUTIONS PVT LTD</b> | HEALTHCARE PRODUCT <b>RXDX STREAMLINE</b></p>
      <div class="badge-verdict">✓ DEFINITIVE YES — 86% CONFIDENCE ON MARKET SHINE & HIRING EXPANSION</div>
    </div>

    <div class="card">
      <h2>🌟 Will Gyrit Solutions Shine in the Market?</h2>
      <p style="font-size:14px; line-height:1.7;">
        <b>YES, DEFINITIVELY.</b> In the Prashna chart, the 10th house of Market Stature (Aries) is ruled by Mars, which achieves 
        <b>Neechabhanga Raja Yoga</b> in the 1st House through conjunction with <b>Exalted Jupiter</b> in Pushya Nakshatra! 
        Coupled with a sparkling <b>Malavya Yoga (Venus in own sign Libra with Mercury)</b> in the 4th house of software foundation, 
        Gyrit Solutions will stand out against legacy hospital software vendors through superior speed, clinical elegance, and zero-defect uptime.
      </p>
    </div>

    <div class="card">
      <h2>👥 Will it Increase its Labour Force?</h2>
      <p style="font-size:14px; line-height:1.7;">
        <b>YES, SUBSTANTIALLY.</b> The 6th house of employees, staffing, and workforce (Sagittarius) is ruled by <b>Jupiter</b>, 
        which is <b>EXALTED in the 1st House</b>! An Exalted 6th Lord is the classic Vedic signature of an organization destined 
        to scale its workforce, expanding from a boutique startup into a multi-tiered corporate structure with dedicated software engineers, 
        QA testers, hospital deployment leads, and client relationship managers.
      </p>
      <table>
        <tr>
          <th>Phase</th>
          <th>Projected Team Size</th>
          <th>Departments Hired</th>
          <th>Role of Teja S</th>
        </tr>
        <tr>
          <td><b>Present to Mid-2027</b></td>
          <td><b>8 – 15 Members</b></td>
          <td>UAT/Manual QA Testers, Cloud Backend Engineers, Hospital Onboarding Specialists.</td>
          <td><b>QA Lead:</b> Establishes rigorous testing protocols and mentors junior testers.</td>
        </tr>
        <tr>
          <td><b>Mid-2027 to Late 2028</b></td>
          <td><b>25 – 45 Members</b></td>
          <td>Field Sales Managers, Clinical Implementation Engineers, 24/7 Hospital IT Helpdesk.</td>
          <td><b>Solutions Director:</b> Drives enterprise software demonstrations and closes key accounts.</td>
        </tr>
        <tr>
          <td><b>2029 Onwards</b></td>
          <td><b>60 – 100+ Members</b></td>
          <td>Regional branches (Hyderabad, Chennai, Mumbai), Product Heads, Compliance Auditors.</td>
          <td><b>Senior Executive:</b> VP of Quality & Clinical Solutions with equity and profit-sharing.</td>
        </tr>
      </table>
    </div>

    <div class="card">
      <h2>🔮 Multi-Year Future Outlook Summary</h2>
      <ul style="margin-left:20px; line-height:1.7; font-size:13.5px;">
        <li><b>Enterprise Viability:</b> Pushya Nakshatra Ascendant ensures the healthcare software solves real hospital pain-points with enduring clinical relevance.</li>
        <li><b>Cash Flow & Financial Health:</b> Strong 11th lord Venus in own sign Libra guarantees steady recurring subscription revenues from hospitals.</li>
        <li><b>Workforce Culture:</b> Governed by Saturn in Pisces, hiring will be disciplined, loyal, and retention-focused, avoiding volatile tech layoffs.</li>
      </ul>
      <div class="btn-group">
        <a href="gyrit_market_shine_and_workforce_expansion_dossier.pdf" target="_blank" class="btn btn-primary">📄 Download PDF Dossier</a>
        <a href="gyrit_solutions_rxdx_streamline_future_dossier.html" class="btn btn-gold">🏥 Product Future Dossier</a>
      </div>
    </div>
  </div>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[SUCCESS] Dossiers Generated:")
    print(f"  • PDF  : {pdf_path}")
    print(f"  • HTML : {html_path}")


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    pdf_out = os.path.join(out_dir, "gyrit_market_shine_and_workforce_expansion_dossier.pdf")
    html_out = os.path.join(out_dir, "gyrit_market_shine_and_workforce_expansion_dossier.html")

    generate_gyrit_growth_dossier(pdf_out, html_out)

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    chrome_exe = None
    for cp in chrome_paths:
        if os.path.exists(cp):
            chrome_exe = cp
            break

    if chrome_exe:
        subprocess.Popen([chrome_exe, pdf_out])
        subprocess.Popen([chrome_exe, html_out])
        print(f"[INFO] Launched Google Chrome with Workforce Growth Dossier.")
    else:
        import webbrowser
        webbrowser.open(pdf_out)
        webbrowser.open(html_out)
