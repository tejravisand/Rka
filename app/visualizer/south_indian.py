"""
South Indian Chart SVG Visualizer.
In South Indian astrology, the 12 zodiac signs occupy fixed positions in a 4x4 square grid:
Top Row: Pisces (11), Aries (0), Taurus (1), Gemini (2)
Right Col: Cancer (3), Leo (4)
Bottom Row: Virgo (5), Libra (6), Scorpio (7), Sagittarius (8)
Left Col: Capricorn (9), Aquarius (10)
Clockwise progression.
"""
from typing import Dict, List
from app.models.astrological import Kundali, PlanetPosition, VargaChart
from app.core.constants import ZODIAC_SIGNS, ZODIAC_SANSKRIT


# Coordinates of the 12 signs in the 4x4 South Indian grid: (row 0-3, col 0-3)
# 0: Aries (row 0, col 1)
# 1: Taurus (row 0, col 2)
# 2: Gemini (row 0, col 3)
# 3: Cancer (row 1, col 3)
# 4: Leo (row 2, col 3)
# 5: Virgo (row 3, col 3)
# 6: Libra (row 3, col 2)
# 7: Scorpio (row 3, col 1)
# 8: Sagittarius (row 3, col 0)
# 9: Capricorn (row 2, col 0)
# 10: Aquarius (row 1, col 0)
# 11: Pisces (row 0, col 0)
SOUTH_INDIAN_SIGN_CELLS = {
    0: (0, 1),
    1: (0, 2),
    2: (0, 3),
    3: (1, 3),
    4: (2, 3),
    5: (3, 3),
    6: (3, 2),
    7: (3, 1),
    8: (3, 0),
    9: (2, 0),
    10: (1, 0),
    11: (0, 0),
}


def render_south_indian_svg(
    kundali: Kundali,
    varga_div: int = 1,
    title: str = "Rasi Chart (D1) - South Indian Style",
    width: int = 600,
    height: int = 600
) -> str:
    """Generate high-quality SVG markup for a South Indian astrological chart."""
    cell_w = width / 4.0
    cell_h = height / 4.0

    # Group entities by sign
    sign_contents: Dict[int, List[str]] = {i: [] for i in range(12)}

    # Check if we are rendering D1 or another Varga
    if varga_div == 1 or varga_div not in kundali.vargas:
        # Ascendant
        asc_sign = kundali.ascendant.sign.value
        asc_deg = kundali.ascendant.degrees_in_sign
        sign_contents[asc_sign].append(f"<tspan fill='#d9534f' font-weight='bold'>ASC {asc_deg:.1f}°</tspan>")

        for p_name, p_pos in kundali.planets.items():
            s_idx = p_pos.sign.value
            deg = p_pos.degrees_in_sign
            retro = "(R)" if p_pos.is_retrograde else ""
            abbr = p_name[:2].upper()
            color = "#204a87" if not p_pos.is_retrograde else "#c41515"
            sign_contents[s_idx].append(f"<tspan fill='{color}'>{abbr}{retro} {deg:.1f}°</tspan>")
    else:
        varga = kundali.vargas[varga_div]
        for ent_name, plc in varga.placements.items():
            s_idx = plc.sign.value
            abbr = "ASC" if ent_name == "Ascendant" else ent_name[:2].upper()
            color = "#d9534f" if ent_name == "Ascendant" else "#204a87"
            sign_contents[s_idx].append(f"<tspan fill='{color}'>{abbr} {plc.degrees_in_varga:.1f}°</tspan>")

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: #faf8f5; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">')

    # Draw outer border and 4x4 grid lines
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#faf8f5" stroke="#333333" stroke-width="3"/>')

    # Horizontal grid lines
    for r in range(1, 4):
        y = r * cell_h
        svg.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#666666" stroke-width="1.5"/>')

    # Vertical grid lines
    for c in range(1, 4):
        x = c * cell_w
        svg.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="#666666" stroke-width="1.5"/>')

    # Center 2x2 box cover
    svg.append(f'<rect x="{cell_w}" y="{cell_h}" width="{cell_w * 2}" height="{cell_h * 2}" fill="#f0ebe1" stroke="#333333" stroke-width="2"/>')

    # Title inside center box
    svg.append(f'<text x="{width / 2}" y="{height / 2 - 25}" text-anchor="middle" font-size="18" font-weight="bold" fill="#2c3e50">{title}</text>')
    subtext = f"Ayanamsa: {kundali.ayanamsa_name} ({kundali.ayanamsa_value:.2f}°)"
    svg.append(f'<text x="{width / 2}" y="{height / 2 + 5}" text-anchor="middle" font-size="13" fill="#555555">{subtext}</text>')
    dt_str = kundali.birth_datetime.strftime("%Y-%m-%d %H:%M UTC")
    svg.append(f'<text x="{width / 2}" y="{height / 2 + 30}" text-anchor="middle" font-size="12" fill="#777777">{dt_str}</text>')

    # Populate 12 sign cells
    for sign_idx in range(12):
        r, c = SOUTH_INDIAN_SIGN_CELLS[sign_idx]
        x = c * cell_w
        y = r * cell_h

        # Sign name label
        sign_label = f"{ZODIAC_SANSKRIT[sign_idx]}"
        svg.append(f'<text x="{x + 8}" y="{y + 18}" font-size="11" font-weight="600" fill="#888888">{sign_label}</text>')

        # Content in cell
        items = sign_contents[sign_idx]
        line_y = y + 36
        for it in items:
            svg.append(f'<text x="{x + 10}" y="{line_y}" font-size="12">{it}</text>')
            line_y += 18

    svg.append('</svg>')
    return '\n'.join(svg)
