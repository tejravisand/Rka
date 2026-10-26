"""
VedAstro Integration Engine
===========================
Bridges the official 'vedastro' Python library into the Astrological project.
Provides Panchanga tables, Sarvashtakavarga (SAV & BAV), Shadbala, and Vedic
horoscope verification with in-memory caching and graceful rate-limit handling.
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

try:
    import vedastro as va
    VEDASTRO_AVAILABLE = True
except ImportError:
    va = None
    VEDASTRO_AVAILABLE = False


class VedAstroEngine:
    """
    High-level interface to the VedAstro Vedic Astrology Engine.
    Handles coordinate mapping, time formatting, API key configuration,
    and structured response parsing.
    """

    _cache: Dict[str, Any] = {}

    @classmethod
    def is_available(cls) -> bool:
        """Check if the vedastro library is installed and importable."""
        return VEDASTRO_AVAILABLE

    @classmethod
    def set_api_key(cls, api_key: str) -> bool:
        """
        Configure optional VedAstro API key to unlock unlimited API calls.
        """
        if not VEDASTRO_AVAILABLE:
            logger.warning("VedAstro library is not available.")
            return False
        try:
            va.Calculate.SetAPIKey(api_key)
            return True
        except Exception as e:
            logger.error(f"Failed to set VedAstro API key: {e}")
            return False

    @classmethod
    def init_from_env(cls):
        """Auto-configure API key from VEDASTRO_API_KEY environment variable if present."""
        key = os.environ.get("VEDASTRO_API_KEY")
        if key:
            cls.set_api_key(key)

    @classmethod
    def build_time_and_geo(
        cls,
        dt_local: datetime,
        tz_offset: float = 5.5,
        lat: float = 12.9716,
        lon: float = 77.5946,
        location_name: str = "Bengaluru"
    ) -> Tuple[Any, Any]:
        """
        Convert standard python datetime and location coordinates into
        VedAstro GeoLocation and Time objects.
        """
        if not VEDASTRO_AVAILABLE:
            raise RuntimeError("VedAstro library is not installed. Run 'pip install vedastro'.")

        # Format offset string: e.g. +05:30 or -04:00
        sign = "+" if tz_offset >= 0 else "-"
        abs_offset = abs(tz_offset)
        hrs = int(abs_offset)
        mins = int(round((abs_offset - hrs) * 60))
        offset_str = f"{sign}{hrs:02d}:{mins:02d}"

        # VedAstro format: "HH:MM DD/MM/YYYY +HH:MM"
        time_str = f"{dt_local.strftime('%H:%M %d/%m/%Y')} {offset_str}"

        geo = va.GeoLocation(location_name, float(lon), float(lat))
        time = va.Time(time_str, geo)
        return time, geo

    @classmethod
    def get_panchanga(
        cls,
        dt_local: datetime,
        tz_offset: float = 5.5,
        lat: float = 12.9716,
        lon: float = 77.5946,
        location_name: str = "Bengaluru",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieve complete Panchanga Table (Tithi, Vara, Nakshatra, Yoga, Karana,
        Sunrise, Sunset, Disha Shool, etc.) in a single call.
        """
        cache_key = f"panchanga_{dt_local.isoformat()}_{tz_offset}_{lat}_{lon}"
        if use_cache and cache_key in cls._cache:
            return cls._cache[cache_key]

        cls.init_from_env()

        try:
            time, _ = cls.build_time_and_geo(dt_local, tz_offset, lat, lon, location_name)
            data = va.Calculate.PanchangaTable(time)
            result = {
                "success": True,
                "data": data,
                "error": None
            }
        except Exception as e:
            result = {
                "success": False,
                "data": {},
                "error": str(e)
            }

        if use_cache and result["success"]:
            cls._cache[cache_key] = result
        return result

    @classmethod
    def get_sarvashtakavarga(
        cls,
        dt_local: datetime,
        tz_offset: float = 5.5,
        lat: float = 12.9716,
        lon: float = 77.5946,
        location_name: str = "Bengaluru",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieve Sarvashtakavarga (SAV) and Bhinnashtakavarga (BAV) chart scores
        for all planets and lagna in a single call.
        """
        cache_key = f"sav_{dt_local.isoformat()}_{tz_offset}_{lat}_{lon}"
        if use_cache and cache_key in cls._cache:
            return cls._cache[cache_key]

        cls.init_from_env()

        try:
            time, _ = cls.build_time_and_geo(dt_local, tz_offset, lat, lon, location_name)
            data = va.Calculate.SarvashtakavargaChart(time)
            result = {
                "success": True,
                "data": data,
                "error": None
            }
        except Exception as e:
            result = {
                "success": False,
                "data": {},
                "error": str(e)
            }

        if use_cache and result["success"]:
            cls._cache[cache_key] = result
        return result

    @classmethod
    def get_integrated_summary(
        cls,
        dt_local: datetime,
        tz_offset: float = 5.5,
        lat: float = 12.9716,
        lon: float = 77.5946,
        location_name: str = "Bengaluru"
    ) -> Dict[str, Any]:
        """
        Fetch integrated VedAstro dataset combining Panchanga and Sarvashtakavarga.
        """
        panchanga = cls.get_panchanga(dt_local, tz_offset, lat, lon, location_name)
        sav = cls.get_sarvashtakavarga(dt_local, tz_offset, lat, lon, location_name)

        return {
            "is_available": cls.is_available(),
            "panchanga": panchanga.get("data") if panchanga.get("success") else None,
            "panchanga_error": panchanga.get("error"),
            "ashtakavarga": sav.get("data") if sav.get("success") else None,
            "ashtakavarga_error": sav.get("error"),
        }
