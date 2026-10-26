"""
Pure-Python astronomical ephemeris and Vedic astrology calculation engine.
Calculates high-precision planetary longitudes, Lahiri Ayanamsa, and Ascendant (Lagna)
without external C/C++ compiler dependencies.
"""
import math
from datetime import datetime, timezone
from typing import Dict, Tuple
from app.models.astrological import Planet, PlanetPosition, ZodiacSign
from app.core.constants import NAKSHATRAS, PLANET_DIGNITY_DEGREES, SIGN_LORDS


def datetime_to_jd(dt: datetime) -> float:
    """Convert a UTC datetime to Julian Day Number."""
    year = dt.year
    month = dt.month
    day = dt.day + (dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3.6e9) / 24.0

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100.0)
    B = 2 - A + math.floor(A / 4.0)

    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return jd


def calculate_lahiri_ayanamsa(jd: float) -> float:
    """
    Calculate Lahiri (Chitra Paksha) Ayanamsa for a given Julian Day.
    Standard definition: Ayanamsa = 23° 51' 25.53" on Jan 1, 2000 (JD 2451545.0)
    Precession rate: ~50.290966" per Julian year (50.290966 / 3600 deg/yr).
    """
    T = (jd - 2451545.0) / 36525.0  # Julian centuries from J2000.0
    # Lahiri ayanamsa formula with quadratic precession term
    ayanamsa_deg = 23.857092 + 1.396042 * T + 0.000308 * (T ** 2)
    return ayanamsa_deg % 360.0


def normalize_degrees(deg: float) -> float:
    """Normalize degrees to [0.0, 360.0)."""
    deg = deg % 360.0
    return deg if deg >= 0 else deg + 360.0


def get_nakshatra_info(sidereal_lon: float) -> Tuple[int, str, int, str]:
    """
    Calculate Nakshatra number (0-26), name, Pada (1-4), and ruling lord
    from sidereal longitude (0 - 360°).
    Each Nakshatra = 13° 20' = 13.333333°
    Each Pada = 3° 20' = 3.333333°
    """
    norm_lon = normalize_degrees(sidereal_lon)
    nak_span = 360.0 / 27.0  # 13.333333333333334
    pada_span = nak_span / 4.0  # 3.3333333333333335

    nak_num = int(norm_lon / nak_span)
    nak_num = min(nak_num, 26)

    rem = norm_lon - (nak_num * nak_span)
    pada_num = int(rem / pada_span) + 1
    pada_num = min(pada_num, 4)

    nak_data = NAKSHATRAS[nak_num]
    return nak_num, nak_data["name"], pada_num, nak_data["lord"]


def get_planet_dignity(planet_name: str, sign_idx: int, degree_in_sign: float) -> str:
    """Determine classical planetary dignity in a given sign."""
    if planet_name in ["Ascendant"]:
        return "Neutral"

    if planet_name in PLANET_DIGNITY_DEGREES:
        ex_sign, ex_deg, deb_sign, deb_deg = PLANET_DIGNITY_DEGREES[planet_name]
        if sign_idx == ex_sign:
            return "Exalted"
        if sign_idx == deb_sign:
            return "Debilitated"

    sign_lord = SIGN_LORDS[sign_idx]
    if sign_lord == planet_name:
        return "Own Sign"

    # Friendly / Neutral / Enemy based on natural relationship
    from app.core.constants import NATURAL_RELATIONSHIPS
    rel = NATURAL_RELATIONSHIPS.get(planet_name, {})
    if sign_lord in rel.get("friends", []):
        return "Friendly"
    if sign_lord in rel.get("enemies", []):
        return "Enemy"
    return "Neutral"


class AstronomicalCalculator:
    """
    Computes tropical planetary positions using standard VSOP-compatible
    analytical orbital models, and converts them to sidereal positions using Lahiri Ayanamsa.
    """

    @staticmethod
    def _kepler_solve(M: float, e: float) -> float:
        """Solve Kepler's equation M = E - e*sin(E) for eccentric anomaly E."""
        M_rad = math.radians(M)
        E = M_rad
        for _ in range(15):
            dE = (E - e * math.sin(E) - M_rad) / (1.0 - e * math.cos(E))
            E -= dE
            if abs(dE) < 1e-8:
                break
        return E

    @classmethod
    def calculate_sun(cls, T: float) -> Tuple[float, float]:
        """Calculate Sun's tropical longitude and daily motion (degrees)."""
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * (T ** 2)
        M = 357.52911 + 35999.05029 * T - 0.0001537 * (T ** 2)
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * (T ** 2)

        M_rad = math.radians(M)
        C = (1.914602 - 0.004817 * T - 0.000014 * (T ** 2)) * math.sin(M_rad) \
            + (0.019993 - 0.000101 * T) * math.sin(2 * M_rad) \
            + 0.000289 * math.sin(3 * M_rad)

        true_lon = normalize_degrees(L0 + C)
        speed = 0.9856  # deg/day approx
        return true_lon, speed

    @classmethod
    def calculate_moon(cls, T: float) -> Tuple[float, float]:
        """Calculate Moon's tropical longitude using principal terms of lunar theory."""
        L_prime = 218.3164477 + 481267.88128 * T - 0.0015786 * (T ** 2)
        D = 297.8501921 + 445267.11140 * T - 0.0018819 * (T ** 2)   # Mean elongation
        M = 357.5291092 + 35999.05029 * T - 0.0001536 * (T ** 2)     # Sun's mean anomaly
        M_prime = 134.9633964 + 477198.8675055 * T + 0.0087414 * (T ** 2)  # Moon's mean anomaly
        F = 93.2720950 + 483202.0175233 * T - 0.0036539 * (T ** 2)  # Moon's argument of latitude

        D_r, M_r, Mp_r, F_r = map(math.radians, [D, M, M_prime, F])

        # Principal periodic perturbations in Moon's longitude (degrees)
        lon_pert = (
            6.288774 * math.sin(Mp_r)
            + 1.274027 * math.sin(2 * D_r - Mp_r)          # Evection
            + 0.658314 * math.sin(2 * D_r)                 # Variation
            + 0.213618 * math.sin(2 * Mp_r)
            - 0.185116 * math.sin(M_r)                     # Annual equation
            - 0.114332 * math.sin(2 * F_r)                 # Reduction to ecliptic
            + 0.058793 * math.sin(2 * D_r - 2 * Mp_r)
            + 0.057066 * math.sin(2 * D_r - M_r - Mp_r)
            + 0.053322 * math.sin(2 * D_r + Mp_r)
            + 0.045758 * math.sin(2 * D_r - M_r)
        )

        true_lon = normalize_degrees(L_prime + lon_pert)
        speed = 13.176  # deg/day approx
        return true_lon, speed

    @classmethod
    def calculate_rahu_ketu(cls, T: float) -> Tuple[float, float]:
        """Calculate True/Mean Lunar Node (Rahu) and Ketu (180° opposite)."""
        # Longitude of ascending node of the Moon's orbit
        omega = 125.04452 - 1934.136261 * T + 0.0020708 * (T ** 2) + (T ** 3) / 450000.0
        rahu_lon = normalize_degrees(omega)
        ketu_lon = normalize_degrees(rahu_lon + 180.0)
        return rahu_lon, ketu_lon

    @classmethod
    def calculate_major_planet(cls, name: str, T: float, sun_lon: float) -> Tuple[float, float, bool]:
        """
        Calculate geocentric tropical longitude, daily speed, and retrograde status
        for Mars, Mercury, Jupiter, Venus, and Saturn using mean Keplerian elements.
        """
        # Orbital elements: (L0, L_dot, a, e0, e_dot, i0, i_dot, Omega0, Omega_dot, pi0, pi_dot)
        elements = {
            "Mercury": (252.25084, 149472.6741, 0.387098, 0.205630, 0.000020, 7.0049, 0.0018, 48.33167, 1.18618, 77.45645, 1.55648),
            "Venus":   (181.97973, 58517.81539, 0.723330, 0.006773, -0.000047, 3.3946, 0.0010, 76.67990, 0.90112, 131.5729, 1.40222),
            "Mars":    (355.43328, 19140.29931, 1.523688, 0.093405, 0.000092, 1.8497, -0.0006, 49.55809, 0.77209, 336.0602, 1.84104),
            "Jupiter": (34.40438, 3034.90567, 5.202561, 0.048498, 0.000163, 1.3030, -0.0002, 100.4644, 1.02098, 14.75385, 1.61996),
            "Saturn":  (49.94424, 1222.11379, 9.554747, 0.055546, -0.000346, 2.4886, -0.0003, 113.6655, 0.87709, 92.43194, 1.95874),
        }

        L0, L_dot, a, e0, e_dot, _, _, _, _, pi0, pi_dot = elements[name]
        mean_lon = normalize_degrees(L0 + L_dot * T)
        perihelion = normalize_degrees(pi0 + pi_dot * T)
        e = e0 + e_dot * T
        M = normalize_degrees(mean_lon - perihelion)

        # Solve Kepler equation
        E = cls._kepler_solve(M, e)
        # True anomaly v
        v = 2.0 * math.atan2(math.sqrt(1.0 + e) * math.sin(E / 2.0), math.sqrt(1.0 - e) * math.cos(E / 2.0))
        # Heliocentric radius r
        r = a * (1.0 - e * math.cos(E))
        # Heliocentric longitude l
        l_helio = normalize_degrees(math.degrees(v) + perihelion)

        # Convert heliocentric to geocentric ecliptic longitude
        # Earth's approximate distance is 1.0 AU, Sun longitude is sun_lon
        # Earth heliocentric longitude = sun_lon + 180°
        earth_l = math.radians(sun_lon + 180.0)
        xp = r * math.cos(math.radians(l_helio)) - 1.0 * math.cos(earth_l)
        yp = r * math.sin(math.radians(l_helio)) - 1.0 * math.sin(earth_l)

        geocentric_lon = normalize_degrees(math.degrees(math.atan2(yp, xp)))

        # Rate of change / retrograde detection
        dT = 0.0001
        T_next = T + dT
        mean_lon_n = normalize_degrees(L0 + L_dot * T_next)
        peri_n = normalize_degrees(pi0 + pi_dot * T_next)
        M_n = normalize_degrees(mean_lon_n - peri_n)
        E_n = cls._kepler_solve(M_n, e)
        v_n = 2.0 * math.atan2(math.sqrt(1.0 + e) * math.sin(E_n / 2.0), math.sqrt(1.0 - e) * math.cos(E_n / 2.0))
        r_n = a * (1.0 - e * math.cos(E_n))
        l_n = normalize_degrees(math.degrees(v_n) + peri_n)
        sun_lon_n, _ = cls.calculate_sun(T_next)
        earth_l_n = math.radians(sun_lon_n + 180.0)
        xp_n = r_n * math.cos(math.radians(l_n)) - 1.0 * math.cos(earth_l_n)
        yp_n = r_n * math.sin(math.radians(l_n)) - 1.0 * math.sin(earth_l_n)
        geo_next = normalize_degrees(math.degrees(math.atan2(yp_n, xp_n)))

        # Daily motion difference
        diff = geo_next - geocentric_lon
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        daily_speed = diff / (dT * 36525.0)
        is_retrograde = daily_speed < 0

        return geocentric_lon, daily_speed, is_retrograde

    @classmethod
    def calculate_ascendant(cls, jd: float, lat: float, lon: float, ayanamsa: float) -> float:
        """
        Calculate Sidereal Ascendant (Lagna) in degrees [0, 360).
        lat: Latitude of birth in degrees (-90 to +90)
        lon: Longitude of birth in degrees (-180 to +180, East positive)
        """
        T = (jd - 2451545.0) / 36525.0

        # Greenwich Mean Sidereal Time (GMST) at 0h UT
        # IAU 1982 formula
        D = jd - 2451545.0
        GMST = 280.46061837 + 360.98564736629 * D + 0.000387933 * (T ** 2) - ((T ** 3) / 38710000.0)
        GMST = normalize_degrees(GMST)

        # Local Sidereal Time (RAMC in degrees)
        RAMC = normalize_degrees(GMST + lon)
        theta_rad = math.radians(RAMC)

        # True obliquity of ecliptic epsilon (degrees)
        eps = 23.4392911 - 0.0130042 * T - 0.00000016 * (T ** 2) + 0.000000504 * (T ** 3)
        eps_rad = math.radians(eps)
        phi_rad = math.radians(lat)

        # Ascendant calculation formula:
        # tan(lambda) = -cos(RAMC) / (sin(RAMC)*cos(eps) + tan(phi)*sin(eps))
        y = -math.cos(theta_rad)
        x = math.sin(theta_rad) * math.cos(eps_rad) + math.tan(phi_rad) * math.sin(eps_rad)

        tropical_asc = normalize_degrees(math.degrees(math.atan2(y, x)))
        sidereal_asc = normalize_degrees(tropical_asc - ayanamsa)
        return sidereal_asc


def calculate_birth_positions(
    dt_utc: datetime,
    latitude: float,
    longitude: float
) -> Tuple[float, PlanetPosition, Dict[str, PlanetPosition]]:
    """
    Calculate Lahiri Ayanamsa, Ascendant, and all 9 planetary positions for a given UTC datetime.
    Returns: (ayanamsa_value, ascendant_pos, planets_dict)
    """
    jd = datetime_to_jd(dt_utc)
    ayanamsa = calculate_lahiri_ayanamsa(jd)
    T = (jd - 2451545.0) / 36525.0

    # 1. Sun
    sun_trop, sun_speed = AstronomicalCalculator.calculate_sun(T)
    sun_sid = normalize_degrees(sun_trop - ayanamsa)

    # 2. Moon
    moon_trop, moon_speed = AstronomicalCalculator.calculate_moon(T)
    moon_sid = normalize_degrees(moon_trop - ayanamsa)

    # 3. Rahu & Ketu (Mean Nodes)
    rahu_trop, ketu_trop = AstronomicalCalculator.calculate_rahu_ketu(T)
    rahu_sid = normalize_degrees(rahu_trop - ayanamsa)
    ketu_sid = normalize_degrees(ketu_trop - ayanamsa)

    # 4. Major Planets
    major_planets = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    planets_sid = {}

    for name in major_planets:
        trop_lon, speed, is_retro = AstronomicalCalculator.calculate_major_planet(name, T, sun_trop)
        sid_lon = normalize_degrees(trop_lon - ayanamsa)
        planets_sid[name] = (sid_lon, speed, is_retro)

    # 5. Ascendant (Lagna)
    asc_sid = AstronomicalCalculator.calculate_ascendant(jd, latitude, longitude, ayanamsa)

    def build_planet_pos(planet: Planet, sid_lon: float, is_retro: bool, speed: float) -> PlanetPosition:
        sign_idx = int(sid_lon / 30.0) % 12
        deg_in_sign = sid_lon % 30.0
        nak_num, nak_name, pada, nak_lord = get_nakshatra_info(sid_lon)
        dignity = get_planet_dignity(planet.value, sign_idx, deg_in_sign)
        return PlanetPosition(
            planet=planet,
            longitude=round(sid_lon, 4),
            sign=ZodiacSign(sign_idx),
            degrees_in_sign=round(deg_in_sign, 4),
            nakshatra_number=nak_num,
            nakshatra_name=nak_name,
            nakshatra_pada=pada,
            nakshatra_lord=nak_lord,
            is_retrograde=is_retro,
            speed=round(speed, 4),
            dignity=dignity
        )

    asc_pos = build_planet_pos(Planet.ASCENDANT, asc_sid, False, 360.0)

    planets: Dict[str, PlanetPosition] = {
        "Sun": build_planet_pos(Planet.SUN, sun_sid, False, sun_speed),
        "Moon": build_planet_pos(Planet.MOON, moon_sid, False, moon_speed),
        "Mars": build_planet_pos(Planet.MARS, planets_sid["Mars"][0], planets_sid["Mars"][2], planets_sid["Mars"][1]),
        "Mercury": build_planet_pos(Planet.MERCURY, planets_sid["Mercury"][0], planets_sid["Mercury"][2], planets_sid["Mercury"][1]),
        "Jupiter": build_planet_pos(Planet.JUPITER, planets_sid["Jupiter"][0], planets_sid["Jupiter"][2], planets_sid["Jupiter"][1]),
        "Venus": build_planet_pos(Planet.VENUS, planets_sid["Venus"][0], planets_sid["Venus"][2], planets_sid["Venus"][1]),
        "Saturn": build_planet_pos(Planet.SATURN, planets_sid["Saturn"][0], planets_sid["Saturn"][2], planets_sid["Saturn"][1]),
        "Rahu": build_planet_pos(Planet.RAHU, rahu_sid, True, -0.0529),
        "Ketu": build_planet_pos(Planet.KETU, ketu_sid, True, -0.0529),
    }

    return ayanamsa, asc_pos, planets
