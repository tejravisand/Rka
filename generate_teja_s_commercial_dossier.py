"""
Executive Commercial Name & Astrological Analysis Dossier Generator for:
Native: Ravi Kumar S (DOB: 20-Nov-1968, 03:45 AM, Malleswaram, Bangalore)
Commercial / Professional Name: "Teja S" (or "Teja.S")
Domain: Software UAT Testing + Healthcare Software (HMS - Hospital Management System) Marketing
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


def generate_teja_s_dossier(pdf_path: str, html_path: str):
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
    story.append(Paragraph("COMMERCIAL NAME CALIBRATION & ASTROLOGICAL STRATEGY DOSSIER", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("EVALUATING <b>'TEJA S'</b> FOR SOFTWARE UAT TESTING & HEALTHCARE HMS MARKETING", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Client: <b>Ravi Kumar S</b> | DOB: 20-Nov-1968, 03:45 AM | Bengaluru, India | Evaluated: October 2026", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=1, spaceAfter=6))

    # Executive Verdict Banner Table
    verdict_text = (
        "<b>EXECUTIVE VERDICT: SUPREMELY AUSPICIOUS COMMERCIAL UPGRADE (96% COMPATIBILITY)</b><br/>"
        "Transitioning from legal name compound <b>28 (The Trusting Soul)</b> to commercial name <b>'Teja S' (Chaldean Compound 14 -> Mercury 5)</b> "
        "directly dissolves past associate-trust frictions and activates high-velocity commercial magnetism. "
        "Root 5 (Mercury) perfectly governs <b>Software UAT defect isolation</b> and <b>B2B Healthcare Software (HMS) sales closures</b>. "
        "No government ID alterations required; highly effective for LinkedIn, business cards, pitch decks, and commercial signatures."
    )
    verdict_table = Table([[Paragraph(verdict_text, callout_box)]], colWidths=[539])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fff4')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#38a169')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 7))

    # SECTION 1: NUMEROLOGICAL COMPARISON MATRIX
    story.append(Paragraph("1. MATHEMATICAL NUMEROLOGY COMPARISON: PRESENT VS PROPOSED NAMES", sec_header))
    num_headers = [
        Paragraph("Metric / Vibration", table_cell_header),
        Paragraph("Present Legal Name:<br/>'Ravi Kumar S'", table_cell_header),
        Paragraph("Proposed Commercial Name:<br/>'Teja S' (or 'Teja.S')", table_cell_header),
        Paragraph("Alternative Variant:<br/>'Tejas S'", table_cell_header),
        Paragraph("Single Name:<br/>'Tejas' (Calling Name)", table_cell_header)
    ]
    num_data = [
        num_headers,
        [
            Paragraph("<b>Chaldean Compound</b>", table_cell_bold),
            Paragraph("<b>28</b> (2+8 = 10 -> Root 1)", table_cell),
            Paragraph("<b>14</b> (1+4 -> Root <b>5 Mercury</b>)", table_cell_bold),
            Paragraph("<b>17</b> (1+7 -> Root <b>8 Saturn</b>)", table_cell),
            Paragraph("<b>14</b> (1+4 -> Root <b>5 Mercury</b>)", table_cell_bold)
        ],
        [
            Paragraph("<b>Chaldean Shastric Archetype</b>", table_cell_bold),
            Paragraph("<i>'The Trusting Soul'</i> — Prone to opposition, associates taking undue advantage, career restarts.", table_cell),
            Paragraph("<i>'Movement & Challenge'</i> — Supreme number of <b>commercial trade, IT agility & deal-making</b>.", table_cell),
            Paragraph("<i>'The Star of the Magi'</i> — Highly spiritual/protective, but causes sales delays & red-tape.", table_cell),
            Paragraph("<i>'Movement & Challenge'</i> — Identical to 'Teja S'; excellent for verbal calling.", table_cell)
        ],
        [
            Paragraph("<b>Pythagorean Compound & Root</b>", table_cell_bold),
            Paragraph("<b>43</b> -> Root 7 (Ketu / Detached)", table_cell),
            Paragraph("<b>10</b> -> Root <b>1 (Sun / Executive Command)</b>", table_cell_bold),
            Paragraph("<b>11</b> -> Master 11 (Moon / Emotional)", table_cell),
            Paragraph("<b>10</b> -> Root <b>1 (Sun / Executive Command)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Synergy with Mulank 2 & Bhagyank 1</b>", table_cell_bold),
            Paragraph("Moderate friction; attracts unsupportive partners.", table_cell),
            Paragraph("<b>100% Harmonic Resonance</b> (Mercury 5 is close friend to both Moon 2 & Sun 1).", table_cell_bold),
            Paragraph("Conflicted (Saturn 8 is inimical to Sun 1).", table_cell),
            Paragraph("<b>100% Harmonic Resonance</b> with birth numbers.", table_cell_bold)
        ],
        [
            Paragraph("<b>Commercial Suitability</b>", table_cell_bold),
            Paragraph("Sluggish deals, unrewarded toil in B2B.", table_cell),
            Paragraph("⭐⭐⭐⭐⭐ <b>SUPREMELY RECOMMENDED (96%)</b>", table_cell_bold),
            Paragraph("⚠️ Not recommended for rapid sales.", table_cell),
            Paragraph("⭐⭐⭐⭐⭐ Excellent verbal calling brand.", table_cell_bold)
        ]
    ]
    num_table = Table(num_data, colWidths=[95, 110, 115, 110, 109])
    num_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(num_table)
    story.append(Spacer(1, 7))

    # SECTION 2: DUAL-ROLE ALIGNMENT
    story.append(Paragraph("2. DUAL-ROLE ASTROLOGICAL & FUNCTIONAL ALIGNMENT", sec_header))
    role_headers = [
        Paragraph("Professional Role", table_cell_header),
        Paragraph("Astrological Karaka & Natal Synergy", table_cell_header),
        Paragraph("How 'Teja S' (Compound 14 -> 5) Empowers the Role", table_cell_header)
    ]
    role_data = [
        role_headers,
        [
            Paragraph("<b>Software UAT Tester</b><br/>(Quality Assurance, Flaw Detection, Validation & Verification)", table_cell_bold),
            Paragraph(
                "• <b>Mercury (Budha):</b> Supreme Karaka of logic, test scripts, bug tracking, and validation protocols.<br/>"
                "• <b>Natal 8th House Placement:</b> In natal Meena Lagna chart, Mercury occupies 8th house (Libra) conjunct Moon (5th lord). "
                "The 8th house governs <i>investigative scrutiny, QA edge-case detection, and forensic audits</i>.<br/>"
                "• <b>Mercury's Lordship:</b> Governs 4th house (Mithuna - computing architectures) and 7th house (Kanya - client sign-offs).",
                table_cell
            ),
            Paragraph(
                "• Compounds to Root <b>5 (Mercury)</b>, directly energizing intellectual scrutiny and bug-hunting intuition.<br/>"
                "• Prevents test-cycle oversights; elevates stature from routine tester to high-value Quality Architect.<br/>"
                "• Facilitates smooth, authoritative communication between technical developers and business stakeholders.",
                table_cell
            )
        ],
        [
            Paragraph("<b>Healthcare Software (HMS) Marketing</b><br/>(Hospital Management Systems, B2B Demos & Closures)", table_cell_bold),
            Paragraph(
                "• <b>Meaning of 'Tejas':</b> Radiance, life vitality, and therapeutic brilliance (*Ojas & Tejas*).<br/>"
                "• <b>Healthcare & Virgo (7th House):</b> Natural 6th sign Virgo rules clinical workflows, hospitals, and diseases. "
                "In his chart, Virgo is the 7th house (contracts/clients) housing <b>Guru-Mangala Yoga (Jupiter 7°40' + Mars 13°32' + Ketu 13°25')</b>.<br/>"
                "• <b>Surya (Sun) in 9th House:</b> Natural *Aarogya Karaka* and 6th lord of healing, sitting in 9th house of Dharma, conferring deep trust with doctors and CEOs.",
                table_cell
            ),
            Paragraph(
                "• Pythagorean Root <b>1 (Sun)</b> gives executive presence when pitching to Medical Directors, Hospital CEOs, and Chief Medical Officers.<br/>"
                "• Chaldean <b>14 (Mercury)</b> accelerates enterprise sales cycles, commercial contract negotiations, and payment releases.<br/>"
                "• Bridges technical product knowledge with commercial deal magnetism effortlessly.",
                table_cell
            )
        ]
    ]
    role_table = Table(role_data, colWidths=[120, 209, 210])
    role_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(role_table)
    story.append(Spacer(1, 7))

    # SECTION 3: COMMERCIAL ADOPTION PROTOCOL & VASTU REMEDIES
    story.append(Paragraph("3. PRACTICAL COMMERCIAL ADOPTION PROTOCOL & REMEDIAL ACTIVATION", sec_header))
    proto_headers = [
        Paragraph("Action Domain", table_cell_header),
        Paragraph("Specific Recommendation & Execution Instructions", table_cell_header)
    ]
    proto_data = [
        proto_headers,
        [
            Paragraph("<b>Government & Bank Records</b>", table_cell_bold),
            Paragraph("<b>LEAVE COMPLETELY UNTOUCHED:</b> Maintain Passport, Aadhaar, PAN card, and Bank Accounts as 'Ravi Kumar S'. No legal gazette filings needed.", table_cell)
        ],
        [
            Paragraph("<b>LinkedIn & Professional Bio</b>", table_cell_bold),
            Paragraph("Update display name to <b>'Teja S'</b>. Headline: <i>'Teja S | Senior QA Specialist & Healthcare Software (HMS) Solutions Consultant'</i>.", table_cell)
        ],
        [
            Paragraph("<b>Corporate Email Signature</b>", table_cell_bold),
            Paragraph("Format: <b>Teja S (Ravi Kumar)</b> | Senior UAT Specialist & HMS Solutions Consultant | Healthcare Technology Division.", table_cell)
        ],
        [
            Paragraph("<b>Daily Signature Calibration</b>", table_cell_bold),
            Paragraph("Sign <b>'Teja S'</b> 21 times daily in an unruled notebook at a <b>15° upward angle</b> using <b>Emerald Green or Royal Blue ink</b> on Wednesday mornings.", table_cell)
        ],
        [
            Paragraph("<b>Power Day for Hospital Sales</b>", table_cell_bold),
            Paragraph("Schedule major UAT releases, hospital demo calls, and pricing proposals on <b>Wednesdays (Budhavara)</b> during Budha Hora (07:00–08:00 AM or 02:00–03:00 PM).", table_cell)
        ],
        [
            Paragraph("<b>Demo Apparel Color Therapy</b>", table_cell_bold),
            Paragraph("Wear <b>Mint Green, Pastel Green, or Crisp Ivory White shirts</b> during hospital client pitches. Avoid dull black or dark charcoal in sales meetings.", table_cell)
        ],
        [
            Paragraph("<b>Workdesk Vastu & Healing Shlokas</b>", table_cell_bold),
            Paragraph("Face <b>North</b> during client marketing calls. Place a small potted <b>Lucky Bamboo / Jade Plant</b> on the North-East desk corner. "
                      "Recite <b>Lord Dhanvantari Shloka</b> and <b>Budha Gayatri Mantra</b> (11 times) prior to major hospital client demos.", table_cell)
        ]
    ]
    proto_table = Table(proto_data, colWidths=[130, 409])
    proto_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_gold),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(proto_table)
    story.append(Spacer(1, 8))

    # Footer note
    footer_text = (
        "<i>CONFIDENTIAL & PROPRIETARY — PREPARED EXCLUSIVELY FOR RAVI KUMAR S (COMMERCIAL IDENTITY: TEJA S). "
        "SYNTHESIZING PARASHARA HORA, KP SUB-LORDS, B. V. RAMAN YOGAS, LAL KITAB & CHALDEAN NUMEROLOGY.</i>"
    )
    story.append(Paragraph(footer_text, subtitle_style))

    doc.build(story)

    # ---------------------------------------------------------
    # 2. INTERACTIVE HTML DOSSIER GENERATION
    # ---------------------------------------------------------
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Commercial Name Analysis — 'Teja S' for Ravi Kumar S</title>
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
      padding: 6px 16px;
      border-radius: 20px;
      font-weight: bold;
      font-size: 13px;
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
      <h1>🌟 COMMERCIAL NAME CALIBRATION: 'TEJA S'</h1>
      <p>Astrological & Numerological Evaluation for Software UAT Testing & Healthcare HMS Marketing</p>
      <div class="badge-verdict">✓ SUPREMELY AUSPICIOUS UPGRADE — 96% SYNERGY SCORE</div>
    </div>

    <div class="card">
      <h2>📊 Numerological Comparison: 'Ravi Kumar S' vs 'Teja S'</h2>
      <table>
        <tr>
          <th>Attribute</th>
          <th>Present Legal Name: 'Ravi Kumar S'</th>
          <th>Proposed Commercial: 'Teja S' (or 'Teja.S')</th>
          <th>Alternative: 'Tejas S'</th>
        </tr>
        <tr>
          <td><b>Chaldean Compound</b></td>
          <td><b>28</b> (Reduces to Root 1 Sun)</td>
          <td><b>14</b> (Reduces to Root <b>5 Mercury</b>)</td>
          <td><b>17</b> (Reduces to Root 8 Saturn)</td>
        </tr>
        <tr>
          <td><b>Chaldean Meaning</b></td>
          <td><i>'The Trusting Soul'</i> — Vulnerable to associate opposition.</td>
          <td><i>'Movement & Challenge'</i> — Supreme for <b>IT, QA & commercial trade</b>.</td>
          <td><i>'The Star of the Magi'</i> — Causes sales deal delays.</td>
        </tr>
        <tr>
          <td><b>Pythagorean Value</b></td>
          <td>43 -> Root 7 (Ketu)</td>
          <td><b>10 -> Root 1 (Sun - Executive Command)</b></td>
          <td>11 -> Master 11 (Moon)</td>
        </tr>
        <tr>
          <td><b>Synergy with Birth Numbers</b></td>
          <td>Moderate / Friction with partners</td>
          <td><b>100% Harmonic Resonance</b> with Mulank 2 & Bhagyank 1</td>
          <td>Inimical to Bhagyank 1 (Saturn vs Sun)</td>
        </tr>
        <tr>
          <td><b>Commercial Verdict</b></td>
          <td>Sluggish enterprise sales closures</td>
          <td><b>⭐⭐⭐⭐⭐ SUPREMELY RECOMMENDED (96%)</b></td>
          <td>⚠️ Not recommended for rapid B2B sales</td>
        </tr>
      </table>
    </div>

    <div class="card">
      <h2>🎯 Functional Role Alignment (UAT Testing + Healthcare HMS Marketing)</h2>
      <table>
        <tr>
          <th>Role</th>
          <th>Astrological & Shastric Basis</th>
          <th>How 'Teja S' (Compound 14 -> 5) Empowers You</th>
        </tr>
        <tr>
          <td><b>Software UAT Tester</b><br/>(Validation & Flaw Detection)</td>
          <td>Mercury rules logic, test scripts, validation, and bug reporting. In natal chart, Mercury sits in 8th house Libra conjunct Moon (5th lord), giving sharp investigative scrutiny.</td>
          <td>Compounds to Root <b>5 (Mercury)</b>, directly energizing intellectual scrutiny, defect isolation, and clear technical communication between developers and business analysts.</td>
        </tr>
        <tr>
          <td><b>Healthcare Software (HMS) Marketing</b><br/>(Hospital Enterprise Demos & Closures)</td>
          <td>'Tejas' represents vital healing radiance. Natural Virgo (7th house of clients) houses Guru-Mangala Yoga (Jupiter + Mars + Ketu) governing medical workflows. Sun in 9th is Aarogya Karaka.</td>
          <td>Pythagorean Root <b>1 (Sun)</b> gives executive authority when pitching to Hospital CEOs & Medical Directors. Chaldean <b>14 (Mercury)</b> accelerates software commercial contract closures.</td>
        </tr>
      </table>
    </div>

    <div class="card">
      <h2>📝 Implementation Blueprint & Practical Guidelines</h2>
      <ul style="margin-left:20px; line-height:1.7; font-size:13.5px;">
        <li><b>Legal IDs:</b> Keep Passport, Aadhaar, PAN, and Bank Accounts as <b>'Ravi Kumar S'</b>. No gazette changes needed.</li>
        <li><b>LinkedIn & Social Profiles:</b> Display as <b>Teja S</b> (Headline: <i>Senior QA Specialist & Healthcare Software (HMS) Solutions Consultant</i>).</li>
        <li><b>Corporate Email Signature:</b> Use <code>Teja S (Ravi Kumar) | Senior UAT Specialist & HMS Solutions Consultant</code>.</li>
        <li><b>Daily Signature Exercise:</b> Sign <b>Teja S</b> 21 times daily at a <b>15° upward angle</b> using <b>Emerald Green or Royal Blue ink</b>.</li>
        <li><b>Power Days:</b> Schedule hospital software demos, commercial pricing proposals, and UAT sign-offs on <b>Wednesdays (Budhavara)</b>.</li>
        <li><b>Demo Apparel Color:</b> Wear <b>Pastel Green, Mint Green, or Crisp Ivory White shirts</b> during hospital client meetings.</li>
      </ul>
      <div class="btn-group">
        <a href="teja_s_commercial_name_analysis_dossier.pdf" target="_blank" class="btn btn-primary">📄 Download PDF Dossier</a>
        <a href="OPEN_MULTI_METHOD_CONSULTATION.html" class="btn btn-gold">🔮 Open Master Portal</a>
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
    pdf_out = os.path.join(out_dir, "teja_s_commercial_name_analysis_dossier.pdf")
    html_out = os.path.join(out_dir, "teja_s_commercial_name_analysis_dossier.html")

    generate_teja_s_dossier(pdf_out, html_out)

    # Launch Chrome directly
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
        print(f"[INFO] Launched Google Chrome with Dossier files.")
    else:
        import webbrowser
        webbrowser.open(pdf_out)
        webbrowser.open(html_out)
