"""
North Indian Diamond Chart SVG Visualizer.
In North Indian astrology, houses are fixed in geometry:
House 1 (Lagna) is always the central top diamond.
Houses count counter-clockwise: 1 (top), 2 (top-left), 3, 4 (left), 5, 6, 7 (bottom), 8, 9, 10 (right), 11, 12.
The zodiac sign number (1 to 12) is displayed in each house according to the rising sign.
"""
from typing import Dict, List, Tuple
from app.models.astrological import Kundali, PlanetPosition


# Centers of the 12 houses in a North Indian chart (normalized 0 to 1)
NORTH_HOUSE_CENTERS = {
    1:  (0.50, 0.28),  # 1st House: Top center diamond
    2:  (0.28, 0.14),  # 2nd House: Top-left triangle
    3:  (0.14, 0.28),  # 3rd House: Left-top triangle
    4:  (0.28, 0.50),  # 4th House: Left diamond
    5:  (0.14, 0.72),  # 5th House: Left-bottom triangle
    6:  (0.28, 0.86),  # 6th House: Bottom-left triangle
    7:  (0.50, 0.72),  # 7th House: Bottom center diamond
    8:  (0.72, 0.86),  # 8th House: Bottom-right triangle
    9:  (0.86, 0.72),  # 9th House: Right-bottom triangle
    10: (0.72, 0.50),  # 10th House: Right diamond
    11: (0.86, 0.28),  # 11th House: Right-top triangle
    12: (0.72, 0.14),  # 12th House: Top-right triangle
}

# Sign number positions in each house (offset slightly from center)
NORTH_SIGN_NUM_POS = {
    1:  (0.50, 0.42),
    2:  (0.38, 0.22),
    3:  (0.22, 0.38),
    4:  (0.42, 0.50),
    5:  (0.22, 0.62),
    6:  (0.38, 0.78),
    7:  (0.50, 0.58),
    8:  (0.62, 0.78),
    9:  (0.78, 0.62),
    10: (0.58, 0.50),
    11: (0.78, 0.38),
    12: (0.62, 0.22),
}


def render_north_indian_svg(
    kundali: Kundali,
    varga_div: int = 1,
    title: str = "Kundali (D1) - North Indian Diamond Style",
    width: int = 600,
    height: int = 600
) -> str:
    """Generate high-quality SVG markup for a North Indian diamond astrological chart."""
    # Determine Lagna sign (1 to 12)
    if varga_div == 1 or varga_div not in kundali.vargas:
        lagna_sign_idx = kundali.ascendant.sign.value
    else:
        varga = kundali.vargas[varga_div]
        lagna_sign_idx = varga.placements["Ascendant"].sign.value

    # Map house number to zodiac sign number (1-12)
    # House 1 = Lagna sign + 1
    # House h = (lagna_sign_idx + h - 1) % 12 + 1
    house_signs = {h: ((lagna_sign_idx + h - 1) % 12) + 1 for h in range(1, 13)}

    # Group planets by house
    house_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}

    if varga_div == 1 or varga_div not in kundali.vargas:
        # Lagna in House 1
        asc_deg = kundali.ascendant.degrees_in_sign
        house_planets[1].append(f"<tspan fill='#d9534f' font-weight='bold'>ASC {asc_deg:.1f}°</tspan>")

        for p_name, p_pos in kundali.planets.items():
            p_sign_idx = p_pos.sign.value
            # Find house number for this sign: (p_sign_idx - lagna_sign_idx) % 12 + 1
            h_num = ((p_sign_idx - lagna_sign_idx) % 12) + 1
            retro = "(R)" if p_pos.is_retrograde else ""
            abbr = p_name[:2].upper()
            color = "#204a87" if not p_pos.is_retrograde else "#c41515"
            deg = p_pos.degrees_in_sign
            house_planets[h_num].append(f"<tspan fill='{color}'>{abbr}{retro} {deg:.1f}°</tspan>")
    else:
        varga = kundali.vargas[varga_div]
        asc_varga_sign = varga.placements["Ascendant"].sign.value
        house_planets[1].append(f"<tspan fill='#d9534f' font-weight='bold'>ASC</tspan>")

        for ent_name, plc in varga.placements.items():
            if ent_name == "Ascendant":
                continue
            p_sign_idx = plc.sign.value
            h_num = ((p_sign_idx - asc_varga_sign) % 12) + 1
            abbr = ent_name[:2].upper()
            house_planets[h_num].append(f"<tspan fill='#204a87'>{abbr} {plc.degrees_in_varga:.1f}°</tspan>")

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" style="background-color: #faf8f5; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">')

    # Title header
    svg.append(f'<text x="{width / 2}" y="24" text-anchor="middle" font-size="15" font-weight="bold" fill="#2c3e50">{title}</text>')

    # Outer chart frame
    pad = 35
    w = width - 2 * pad
    h = height - 2 * pad
    x0, y0 = pad, pad
    x1, y1 = pad + w, pad + h
    xc, yc = pad + w / 2.0, pad + h / 2.0

    # Outer square
    svg.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#fffdf9" stroke="#333333" stroke-width="2.5"/>')

    # Main diagonals (corner to corner)
    svg.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#444444" stroke-width="1.8"/>')
    svg.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y0}" stroke="#444444" stroke-width="1.8"/>')

    # Inner diamond connecting edge midpoints
    svg.append(f'<polygon points="{xc},{y0} {x1},{yc} {xc},{y1} {x0},{yc}" fill="none" stroke="#444444" stroke-width="1.8"/>')

    # Render house sign numbers and planetary occupants
    for h in range(1, 13):
        # 1. Sign Number (in Vedic notation, 1=Aries .. 12=Pisces)
        sn_x = pad + NORTH_SIGN_NUM_POS[h][0] * w
        sn_y = pad + NORTH_SIGN_NUM_POS[h][1] * h
        sign_num = house_signs[h]
        svg.append(f'<text x="{sn_x}" y="{sn_y}" font-size="12" font-weight="bold" fill="#888888" text-anchor="middle">{sign_num}</text>')

        # 2. Occupant Planets
        hc_x = pad + NORTH_HOUSE_CENTERS[h][0] * w
        hc_y = pad + NORTH_HOUSE_CENTERS[h][1] * h
        planets_list = house_planets[h]

        if planets_list:
            total_lines = len(planets_list)
            start_y = hc_y - (total_lines - 1) * 7.0
            for i, p_str in enumerate(planets_list):
                curr_y = start_y + (i * 14.0)
                svg.append(f'<text x="{hc_x}" y="{curr_y}" font-size="11" text-anchor="middle">{p_str}</text>')

    svg.append('</svg>')
    return '\n'.join(svg)
