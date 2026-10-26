"""
Executive Astrological & Numerological Future Forecast Dossier for:
Company: Gyrit Solutions Pvt Ltd (Commercial Brand: Gyrit Solutions)
Product: RxDx Streamline (HMS / Healthcare Software)
Key Stakeholder / Evaluator: Teja S (Ravi Kumar S) - UAT Tester & HMS Marketing Specialist
Inquiry Timestamp: 25-Oct-2026 13:12:26 IST | Location: Bengaluru, Karnataka
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


def generate_gyrit_dossier(pdf_path: str, html_path: str):
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
    story.append(Paragraph("ENTERPRISE & PRODUCT FUTURE PREDICTION DOSSIER", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>GYRIT SOLUTIONS PVT LTD</b> | HEALTHCARE PRODUCT: <b>RXDX STREAMLINE (HMS)</b>", subtitle_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Evaluator / Native: <b>Teja S (Ravi Kumar S)</b> | Horary Time: 25-Oct-2026, 01:12 PM IST | Bengaluru, India", subtitle_style))
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=1, spaceAfter=6))

    # Executive Verdict Banner Table
    verdict_text = (
        "<b>EXECUTIVE VERDICT: HIGHLY PROMISING ENTERPRISE WITH STRONG SYSTEMIC LONGEVITY (82% CONFIDENCE)</b><br/>"
        "<b>1. Numerological Power:</b> Commercial brand <b>'Gyrit Solutions' (Chaldean 50 -> Mercury 5)</b> matches <b>Teja S (Chaldean 14 -> Mercury 5)</b> "
        "in an exact 1-to-1 root harmony! Teja S will act as an energetic catalyst for commercial sales closures.<br/>"
        "<b>2. Product Dynamics:</b> 'RxDx' carries compound <b>16 (The Citadel)</b>, indicating complex clinical logic where rigorous UAT testing is essential "
        "to prevent software workflow glitches. 'Streamline' carries Master Royal Compound <b>33 (Universal Harmony)</b>, bringing strong hospital adoption.<br/>"
        "<b>3. Horary Prashna Lagna:</b> Cancer 16° in <b>Pushya Nakshatra</b> (the supreme healing star of nourishment) with <b>Exalted Jupiter in Lagna</b> "
        "forming <i>Neechabhanga Raja Yoga</i> with Mars! Transiting Moon at Meena 26°33' precisely conjoins Teja S's natal Lagna (26°36')!"
    )
    verdict_table = Table([[Paragraph(verdict_text, callout_box)]], colWidths=[539])
    verdict_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fff4')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#38a169')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 7))

    # SECTION 1: NUMEROLOGICAL PROFILE OF COMPANY & PRODUCT
    story.append(Paragraph("1. NUMEROLOGICAL VIBRATION ANALYSIS: COMPANY & PRODUCT BRANDS", sec_header))
    num_headers = [
        Paragraph("Entity / Brand Name", table_cell_header),
        Paragraph("Chaldean Sum", table_cell_header),
        Paragraph("Single Root", table_cell_header),
        Paragraph("Pythagorean", table_cell_header),
        Paragraph("Shastric Archetype & Business Significance", table_cell_header)
    ]
    num_data = [
        num_headers,
        [
            Paragraph("<b>Gyrit Solutions</b><br/>(Primary Commercial Brand)", table_cell_bold),
            Paragraph("<b>50</b>", table_cell_bold),
            Paragraph("<b>5 (Mercury)</b>", table_cell_bold),
            Paragraph("70 -> <b>7 (Ketu)</b>", table_cell),
            Paragraph("<b>Outstanding Commercial Vibration:</b> 50 brings digital intelligence, B2B software sales agility, and rapid market networking. Perfectly mirrors Teja S (14->5).", table_cell)
        ],
        [
            Paragraph("<b>Gyrit Solutions Pvt Ltd</b><br/>(Full Registered Entity)", table_cell_bold),
            Paragraph("<b>79</b>", table_cell),
            Paragraph("<b>7 (Ketu)</b>", table_cell),
            Paragraph("92 -> <b>2 (Moon)</b>", table_cell),
            Paragraph("Governs high-tech research, proprietary IP, and specialized niche healthcare algorithms. Advises strong institutional contracts and clear hospital SLAs.", table_cell)
        ],
        [
            Paragraph("<b>Gyrit</b><br/>(Root Word Alone)", table_cell_bold),
            Paragraph("<b>11</b>", table_cell),
            Paragraph("<b>2 (Moon)</b>", table_cell),
            Paragraph("34 -> <b>7 (Ketu)</b>", table_cell),
            Paragraph("<i>'The Muzzled Lion'</i> — Intuitive but emotionally sensitive if used alone. <b>Guideline:</b> Always promote as <b>'Gyrit Solutions'</b> to maintain Mercury 5 power.", table_cell)
        ],
        [
            Paragraph("<b>RxDx Streamline</b><br/>(Standard Product Name)", table_cell_bold),
            Paragraph("<b>49</b><br/>(16 + 33)", table_cell_bold),
            Paragraph("<b>4 (Rahu)</b>", table_cell),
            Paragraph("69 -> <b>6 (Venus)</b>", table_cell_bold),
            Paragraph("<b>Disruptive Modern Platform:</b> 'RxDx' (16) demands rigorous UAT testing; 'Streamline' (33 - Master Teacher) brings high clinical harmony and doctor trust. Rahu (4) + Venus (6) gives UI elegance.", table_cell)
        ],
        [
            Paragraph("<b>RxDx Stremline</b><br/>(Spelling as Written)", table_cell_bold),
            Paragraph("<b>48</b><br/>(16 + 32)", table_cell),
            Paragraph("<b>3 (Jupiter)</b>", table_cell_bold),
            Paragraph("68 -> <b>5 (Mercury)</b>", table_cell_bold),
            Paragraph("Jupiter 3 governs hospitals, medical ethics, and physician trust; Pythagorean 5 accelerates software trade and commercial demos.", table_cell)
        ]
    ]
    num_table = Table(num_data, colWidths=[110, 60, 65, 65, 239])
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

    # SECTION 2: HORARY PRASHNA CHART (OCTOBER 25, 2026, 01:12 PM)
    story.append(Paragraph("2. REAL-TIME PRASHNA HORARY ASTROLOGY (TIME OF ENQUIRY)", sec_header))
    prashna_headers = [
        Paragraph("Astrological Dimension", table_cell_header),
        Paragraph("Horary Placement & Configuration", table_cell_header),
        Paragraph("Direct Impact on Gyrit Solutions & RxDx Streamline", table_cell_header)
    ]
    prashna_data = [
        prashna_headers,
        [
            Paragraph("<b>Prashna Lagna</b><br/>(Ascendant at Query)", table_cell_bold),
            Paragraph("<b>Cancer (Karka) 16°02'</b><br/>Nakshatra: <b>Pushya (Pada 4)</b><br/>Lord: Saturn | Deity: Brihaspati", table_cell),
            Paragraph("Pushya is the supreme auspicious star of <b>healing, nourishment, and sustaining care</b>. Confirms that the product solves an authentic, essential healthcare need.", table_cell)
        ],
        [
            Paragraph("<b>Jupiter in Lagna</b><br/>(Divine Blessing)", table_cell_bold),
            Paragraph("<b>Jupiter at 29°05' Cancer</b><br/><b>EXALTED IN 1st HOUSE</b><br/>With Debilitated Mars (20°49')", table_cell),
            Paragraph("<b>Neechabhanga Raja Yoga & Guru-Mangala Yoga in Lagna!</b> Exalted Jupiter completely protects the company from premature failure, blessing it with institutional credibility.", table_cell)
        ],
        [
            Paragraph("<b>Prashna Moon & Native Synergy</b>", table_cell_bold),
            Paragraph("<b>Moon at Meena 26°33' (Revati)</b><br/>9th House of Fortune & Grace<br/>Saturn at 14°48' Meena", table_cell),
            Paragraph("<b>Astonishing Cosmic Synchronicity:</b> Transiting Moon (26°33') is <b>within 3 minutes of arc</b> of Teja S's Janma Lagna (26°36')! Confirms Teja S's destiny is tightly linked to this product.", table_cell)
        ],
        [
            Paragraph("<b>4th House (Software Architecture)</b>", table_cell_bold),
            Paragraph("<b>Venus 6°54' (Own sign Libra)</b><br/>+ Mercury 26°50' + Sun 7°41'<br/>Forms <b>Malavya Mahapurusha Yoga</b>", table_cell),
            Paragraph("Software design, clinical workflow engine, and user interface possess high aesthetic and functional quality. Doctors and hospital staff will find the system intuitive.", table_cell)
        ],
        [
            Paragraph("<b>10th House (Market Trajectory)</b>", table_cell_bold),
            Paragraph("Aries (Mesha) ruled by Mars.<br/>Mars in 1st in Neechabhanga with Exalted Jupiter.", table_cell),
            Paragraph("Initial cash flow and deployment friction will be successfully conquered through high resilience and proactive client demonstrations.", table_cell)
        ]
    ]
    prashna_table = Table(prashna_data, colWidths=[120, 160, 259])
    prashna_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(prashna_table)
    story.append(Spacer(1, 7))

    # SECTION 3: FUTURE TIMELINE FORECAST & CATALYTIC ACTION PLAN
    story.append(Paragraph("3. MULTI-YEAR FUTURE TRAJECTORY & CATALYTIC ACTION BLUEPRINT", sec_header))
    time_headers = [
        Paragraph("Phase / Window", table_cell_header),
        Paragraph("Operational Focus & Key Milestones", table_cell_header),
        Paragraph("Teja S's Role & Impact", table_cell_header)
    ]
    time_data = [
        time_headers,
        [
            Paragraph("<b>Phase 1: Present to Mid-2027</b><br/>(Product Hardening & Pilots)", table_cell_bold),
            Paragraph("• Intensive UAT stabilization; eliminating prescription (Rx) and diagnostic (Dx) workflow corner-case bugs.<br/>"
                      "• Piloting in 3–5 mid-sized private hospitals, polyclinics, and diagnostic centers.<br/>"
                      "• Gradual revenue accumulation; focus on client retention rather than massive marketing spend.", table_cell),
            Paragraph("<b>UAT Tester Backbone:</b> Teja S's investigative scrutiny (Mercury in 8th house) will prevent embarrassing live hospital crashes and build product trust.", table_cell)
        ],
        [
            Paragraph("<b>Phase 2: Mid-2027 to Late 2028</b><br/>(Regional Commercial Expansion)", table_cell_bold),
            Paragraph("• Transiting Jupiter enters Leo/Virgo, illuminating the 2nd and 3rd houses from Cancer Prashna Lagna.<br/>"
                      "• Influx of hospital client contracts across Bengaluru, tier-2 Karnataka, and South Indian medical clusters.<br/>"
                      "• Launching specialized inpatient (IP), billing, and pharmacy add-on modules.", table_cell),
            Paragraph("<b>HMS Marketing Accelerator:</b> Teja S leverages commercial name vibration (14->5) and Wednesday pitch timing to close enterprise hospital software deals.", table_cell)
        ],
        [
            Paragraph("<b>Phase 3: 2029 Onwards</b><br/>(Maturity & SaaS Valuation Peak)", table_cell_bold),
            Paragraph("• Stable, recurring SaaS subscription model established across multiple healthcare networks.<br/>"
                      "• RxDx Streamline achieves recognized regional market share as a dependable HMS provider.<br/>"
                      "• Potential institutional funding, strategic corporate alliances, or enterprise acquisition interest.", table_cell),
            Paragraph("<b>Senior Leadership:</b> Transitioning to Product Quality Director or Chief Solutions Consultant with lucrative commission and equity upside.", table_cell)
        ]
    ]
    time_table = Table(time_data, colWidths=[120, 240, 179])
    time_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_gold),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(time_table)
    story.append(Spacer(1, 7))

    # SECTION 4: STRATEGIC RECOMMENDATIONS
    story.append(Paragraph("4. STRATEGIC RECOMMENDATIONS FOR MAXIMUM COMMERCIAL SUCCESS", sec_header))
    strat_text = (
        "<b>1. Commercial Branding Rule:</b> Always present the company publicly as <b>'Gyrit Solutions'</b> (Chaldean Compound 50 -> Mercury 5) "
        "rather than using 'Gyrit' alone (11 -> Moon, which carries hesitation). The phrase 'Gyrit Solutions' creates the exact 5-to-5 harmonic resonance with Teja S.<br/>"
        "<b>2. Product Name Presentation:</b> Brand the product clearly as <b>'RxDx Streamline'</b> (with standard English spelling 'Streamline', Compound 33). "
        "The tagline should read: <i>'Streamlining Hospital Workflows, Prescriptions & Diagnostics with Clinical Precision'</i>.<br/>"
        "<b>3. UAT is the Sales Engine:</b> In healthcare, software demos do not fail on design; they fail when a doctor experiences a latency freeze or prescription sync error. "
        "Teja S's dual capability in UAT testing ensures that the software is bug-proof before client demos take place.<br/>"
        "<b>4. Optimal Pitch Timings:</b> Schedule high-stakes hospital software demonstrations on <b>Wednesdays (Mercury) or Thursdays (Jupiter)</b> "
        "during mid-morning (09:30 AM to 11:30 AM) to maximize contract sign-offs."
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
  <title>Future Prediction: Gyrit Solutions & RxDx Streamline</title>
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
      <h1>🏥 FUTURE PREDICTION DOSSIER</h1>
      <p><b>GYRIT SOLUTIONS PVT LTD</b> & HEALTHCARE PRODUCT <b>RXDX STREAMLINE (HMS)</b></p>
      <div class="badge-verdict">✓ HIGHLY PROMISING FUTURE — 82% CONFIDENCE SCORE</div>
    </div>

    <div class="card">
      <h2>📊 Numerological Vibration Matrix</h2>
      <table>
        <tr>
          <th>Entity / Brand</th>
          <th>Chaldean Sum</th>
          <th>Single Root</th>
          <th>Strategic Business Significance</th>
        </tr>
        <tr>
          <td><b>Gyrit Solutions</b> (Commercial Brand)</td>
          <td><b>50</b></td>
          <td><b>5 (Mercury)</b></td>
          <td><b>Supreme Commercial Harmony:</b> Matches Teja S (14->5) in a direct 1-to-1 root resonance! Fuels agile B2B healthcare sales closures.</td>
        </tr>
        <tr>
          <td><b>Gyrit Solutions Pvt Ltd</b> (Legal Entity)</td>
          <td><b>79</b></td>
          <td><b>7 (Ketu)</b></td>
          <td>Governs high-tech research and specialized medical algorithms. Advises structured hospital contracts and clear SLA terms.</td>
        </tr>
        <tr>
          <td><b>RxDx Streamline</b> (Standard Product)</td>
          <td><b>49 (16 + 33)</b></td>
          <td><b>4 (Rahu)</b></td>
          <td>'RxDx' (16) demands rigorous UAT testing; 'Streamline' (33 Master Teacher) creates high doctor trust and clinical workflow elegance.</td>
        </tr>
      </table>
    </div>

    <div class="card">
      <h2>🪐 Prashna Horary Astrological Assessment (Cast at Query Moment)</h2>
      <ul style="margin-left:20px; line-height:1.7; font-size:13.5px;">
        <li><b>Prashna Lagna: Cancer (Karka) 16° in Pushya Nakshatra</b> — Pushya is the supreme auspicious Vedic star of healing, nourishment, and sustaining care, confirming that the product serves a vital clinical need.</li>
        <li><b>Exalted Jupiter in Lagna:</b> Blesses the company with institutional credibility, high hospital respect, and protection against premature failure.</li>
        <li><b>Neechabhanga Raja Yoga in Lagna:</b> Debilitated Mars is cancelled and exalted by Jupiter, forming <i>Guru-Mangala Yoga</i> (strong medical technology infrastructure).</li>
        <li><b>Malavya Yoga in 4th House:</b> Venus in own sign Libra with Mercury creates an intuitive, appealing UI and clean software architecture.</li>
        <li><b>Cosmic Synchronicity with Teja S:</b> Transiting Moon at Meena 26°33' precisely conjoins Teja S's natal Lagna (26°36') within 3 minutes of arc, proving Teja S is karmically destined to catalyze this product's commercial success!</li>
      </ul>
    </div>

    <div class="card">
      <h2>🚀 Multi-Year Commercial Growth Forecast</h2>
      <table>
        <tr>
          <th>Phase</th>
          <th>Operational Focus</th>
          <th>Role of Teja S</th>
        </tr>
        <tr>
          <td><b>Present to Mid-2027</b><br/>(Product Hardening)</td>
          <td>UAT bug elimination, pilot runs in 3–5 mid-sized private hospitals and polyclinics, achieving 99.9% uptime.</td>
          <td><b>UAT Backbone:</b> Teja S's 8th-house Mercury scrutiny prevents live hospital software crashes.</td>
        </tr>
        <tr>
          <td><b>Mid-2027 to Late 2028</b><br/>(Commercial Expansion)</td>
          <td>Hospital client contracts accelerate across Karnataka and South India; introduction of IP and billing modules.</td>
          <td><b>Marketing Catalyst:</b> Teja S closes high-value enterprise hospital software licenses.</td>
        </tr>
        <tr>
          <td><b>2029 Onwards</b><br/>(Market Stature)</td>
          <td>Established SaaS subscription revenue, recognized regional market share, and potential strategic acquisition offers.</td>
          <td><b>Executive Elevation:</b> Senior Solutions Director with lucrative commission and equity upside.</td>
        </tr>
      </table>
      <div class="btn-group">
        <a href="gyrit_solutions_rxdx_streamline_future_dossier.pdf" target="_blank" class="btn btn-primary">📄 Download PDF Dossier</a>
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
    pdf_out = os.path.join(out_dir, "gyrit_solutions_rxdx_streamline_future_dossier.pdf")
    html_out = os.path.join(out_dir, "gyrit_solutions_rxdx_streamline_future_dossier.html")

    generate_gyrit_dossier(pdf_out, html_out)

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
        print(f"[INFO] Launched Google Chrome with Gyrit Dossier files.")
    else:
        import webbrowser
        webbrowser.open(pdf_out)
        webbrowser.open(html_out)
