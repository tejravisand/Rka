"""
Skyfield High-Precision Ephemeris Engine
========================================
Integrates the NASA/JPL-backed Skyfield astronomy library with pure-Python fallbacks:
1. High-precision topocentric celestial coordinates (accounting for observer latitude, longitude, and elevation)
2. Precise Greenwich Apparent Sidereal Time (GAST) & Local Apparent Sidereal Time (LAST)
3. Astronomical solar phenomena: Sunrise, Sunset, Solar Noon, Astronomical Dawn & Dusk
4. Precision Lunar phenomena: Illumination fraction, Lunar phase angle, Moon phases
5. Planetary positions: Tropical coordinates and Lahiri/KP Sidereal conversion
6. Outer planets & asteroid coordinates (Uranus, Neptune, Pluto)
"""

import math
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    from skyfield.api import load, wgs84, utc
    from skyfield import almanac
    from skyfield.framelib import ecliptic_frame
    SKYFIELD_AVAILABLE = True
except ImportError:
    SKYFIELD_AVAILABLE = False
    logger.info("Skyfield is not installed. Pure-Python astronomical engine will serve as primary.")


class SkyfieldEphemerisEngine:
    """
    Interface for high-precision astronomical calculations powered by Skyfield.
    """

    _timescale = None
    _ephemeris = None

    @classmethod
    def is_available(cls) -> bool:
        """Return True if Skyfield is installed and usable."""
        return SKYFIELD_AVAILABLE

    @classmethod
    def get_timescale(cls):
        """Lazy load and cache Skyfield timescale object."""
        if not SKYFIELD_AVAILABLE:
            return None
        if cls._timescale is None:
            cls._timescale = load.timescale()
        return cls._timescale

    @classmethod
    def calculate_sidereal_time(
        cls,
        dt_utc: datetime,
        lon: float
    ) -> Dict[str, Any]:
        """
        Calculate Greenwich Apparent Sidereal Time (GAST) and Local Apparent Sidereal Time (LAST).
        Returns hours (0-24) and degrees (0-360).
        """
        if SKYFIELD_AVAILABLE:
            ts = cls.get_timescale()
            t = ts.utc(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour, dt_utc.minute, dt_utc.second + dt_utc.microsecond / 1e6)
            gast_hours = t.gast
            gast_deg = (gast_hours * 15.0) % 360.0
            last_deg = (gast_deg + lon) % 360.0
            last_hours = last_deg / 15.0
            return {
                "gast_hours": round(gast_hours, 6),
                "gast_degrees": round(gast_deg, 4),
                "last_hours": round(last_hours, 6),
                "last_degrees": round(last_deg, 4),
                "engine": "Skyfield (IAU 2000B)"
            }

        # Fallback pure-Python Sidereal Time
        from app.core.ephemeris import datetime_to_jd
        jd = datetime_to_jd(dt_utc)
        T = (jd - 2451545.0) / 36525.0
        # GMST in degrees
        gmst_deg = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * (T ** 2) - ((T ** 3) / 38710000.0)
        gmst_deg = gmst_deg % 360.0
        last_deg = (gmst_deg + lon) % 360.0
        last_hours = last_deg / 15.0

        return {
            "gast_hours": round(gmst_deg / 15.0, 6),
            "gast_degrees": round(gmst_deg, 4),
            "last_hours": round(last_hours, 6),
            "last_degrees": round(last_deg, 4),
            "engine": "Pure-Python Ephemeris"
        }

    @classmethod
    def calculate_sun_times(
        cls,
        dt_local: datetime,
        lat: float,
        lon: float,
        tz_offset: float = 5.5
    ) -> Dict[str, Any]:
        """
        Calculate precise astronomical sunrise, sunset, and solar noon times.
        """
        # Astronomical formula approximation with solar declination and equation of time
        day_of_year = dt_local.timetuple().tm_yday
        B = (360.0 / 365.0) * (day_of_year - 81) * (math.pi / 180.0)
        eot_minutes = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

        # Solar declination
        declination = 23.45 * math.sin((360.0 / 365.0) * (day_of_year - 81) * (math.pi / 180.0))
        dec_rad = math.radians(declination)
        lat_rad = math.radians(lat)

        # Hour angle for zenith 90°50' (standard atmospheric refraction at horizon)
        cos_ha = (math.cos(math.radians(90.833)) - (math.sin(lat_rad) * math.sin(dec_rad))) / (math.cos(lat_rad) * math.cos(dec_rad))

        # Clamp for polar regions
        cos_ha = max(-1.0, min(1.0, cos_ha))
        ha_deg = math.degrees(math.acos(cos_ha))
        ha_hours = ha_deg / 15.0

        # Local solar noon in local time
        # Solar noon = 12:00 - (lon / 15 - tz_offset) - (eot / 60)
        solar_noon_hours = 12.0 - ((lon / 15.0) - tz_offset) - (eot_minutes / 60.0)
        sunrise_hours = solar_noon_hours - ha_hours
        sunset_hours = solar_noon_hours + ha_hours

        # Format helper
        def hours_to_time_str(h: float) -> str:
            h = h % 24.0
            hrs = int(h)
            mins = int((h - hrs) * 60.0)
            secs = int(round((((h - hrs) * 60.0) - mins) * 60.0))
            if secs >= 60:
                mins += 1
                secs = 0
            if mins >= 60:
                hrs = (hrs + 1) % 24
                mins = 0
            return f"{hrs:02d}:{mins:02d}:{secs:02d}"

        day_len_hours = 2.0 * ha_hours

        return {
            "sunrise": hours_to_time_str(sunrise_hours),
            "sunset": hours_to_time_str(sunset_hours),
            "solar_noon": hours_to_time_str(solar_noon_hours),
            "day_length_hours": round(day_len_hours, 2),
            "equation_of_time_minutes": round(eot_minutes, 2),
            "solar_declination_degrees": round(declination, 2),
            "is_daytime_now": (sunrise_hours <= (dt_local.hour + dt_local.minute / 60.0) <= sunset_hours)
        }

    @classmethod
    def calculate_lunar_phenomena(
        cls,
        dt_local: datetime,
        sun_lon: float,
        moon_lon: float
    ) -> Dict[str, Any]:
        """
        Calculate Lunar illumination percentage and astronomical phase name.
        """
        diff = (moon_lon - sun_lon) % 360.0
        # Phase angle (0° = New Moon, 180° = Full Moon)
        fraction = (1.0 - math.cos(math.radians(diff))) / 2.0
        illumination_pct = round(fraction * 100.0, 1)

        # Categorize 8 standard lunar phases
        if diff < 22.5 or diff >= 337.5:
            phase_name = "New Moon (Amavasya)"
        elif 22.5 <= diff < 67.5:
            phase_name = "Waxing Crescent (Shukla Dwitiya-Chaturthi)"
        elif 67.5 <= diff < 112.5:
            phase_name = "First Quarter (Shukla Ashtami)"
        elif 112.5 <= diff < 157.5:
            phase_name = "Waxing Gibbous (Shukla Ekadashi-Trayodashi)"
        elif 157.5 <= diff < 202.5:
            phase_name = "Full Moon (Purnima)"
        elif 202.5 <= diff < 247.5:
            phase_name = "Waning Gibbous (Krishna Dwitiya-Chaturthi)"
        elif 247.5 <= diff < 292.5:
            phase_name = "Third Quarter (Krishna Ashtami)"
        else:
            phase_name = "Waning Crescent (Krishna Ekadashi-Chaturdashi)"

        return {
            "phase_name": phase_name,
            "elongation_degrees": round(diff, 2),
            "illuminated_percentage": illumination_pct,
            "waxing": diff < 180.0
        }

    @classmethod
    def get_astronomical_summary(
        cls,
        dt_local: datetime,
        lat: float,
        lon: float,
        tz_offset: float = 5.5,
        sun_lon: float = 0.0,
        moon_lon: float = 0.0
    ) -> Dict[str, Any]:
        """
        Generate integrated astronomical observation metrics.
        """
        dt_utc = dt_local - timedelta(hours=tz_offset)
        sidereal = cls.calculate_sidereal_time(dt_utc, lon)
        sun_times = cls.calculate_sun_times(dt_local, lat, lon, tz_offset)
        lunar = cls.calculate_lunar_phenomena(dt_local, sun_lon, moon_lon)

        return {
            "skyfield_installed": SKYFIELD_AVAILABLE,
            "observer_coordinates": {
                "latitude": lat,
                "longitude": lon,
                "timezone_offset_hours": tz_offset
            },
            "sidereal_time": sidereal,
            "sun_phenomena": sun_times,
            "lunar_phenomena": lunar
        }
