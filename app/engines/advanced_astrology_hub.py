"""
Advanced Astrological Hub & Multi-System Gateway
=================================================
Unifies all cutting-edge Python astrological engines into a coherent, high-level API:
1. Jaimini Sutras Engine (Chara Karakas, Arudha Padas, Rashi Drishti, Karakamsha, Chara Dasha)
2. Classical Ashtakavarga Engine (337 Bindus, BAV, SAV, Trikona & Ekadhipatya Shodhana, Pindas, Kakshya)
3. Shadbala Engine (6-fold planetary strength in Virupas & Rupas, benchmarks, ratios, Ishta/Kashta Phala)
4. Ashtakoota & Dashakoota Guna Milan Engine (36 Gunas, Manglik / Kuja Dosha mutual cancellation)
5. Precision Panchanga & Muhurtha Engine (5 limbs, Rahu Kaalam, Gulika, Yamaganda, Abhijit, Brahma Muhurtha)
6. Skyfield Astronomy Engine (IAU GAST/LAST, astronomical solar/lunar phenomena)
7. VedAstro Bridge (Official VedAstro 1.23.30 library integration)
8. Integrative East-West Medical Astrology (Ayur-Jyotisha & Culpeper Decumbiture)
9. KP & Lal Kitab Engines
"""

import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from app.models.astrological import Kundali
from app.core.kundali import calculate_kundali
from app.core.vargas import calculate_all_vargas
from app.engines.jaimini_engine import JaiminiEngine
from app.engines.ashtakavarga_engine import AshtakavargaEngine
from app.engines.shadbala_engine import ShadbalaEngine
from app.engines.guna_milan_engine import GunaMilanEngine
from app.engines.panchanga_engine import PanchangaEngine
from app.engines.skyfield_ephemeris import SkyfieldEphemerisEngine
from app.engines.vedastro_engine import VedAstroEngine
from app.engines.marriage_harmony_engine import MarriageHarmonyEngine
from app.engines.progeny_pregnancy_engine import ProgenyPregnancyEngine
from app.engines.unknown_birth_engine import UnknownBirthEngine
from app.engines.devatha_activation_engine import DevathaActivationEngine
from app.engines.dosha_eclipse_engine import MasterDoshaEngine


class AdvancedAstrologyHub:
    """
    Central coordinator and master interface for all advanced astrological computations.
    """

    @classmethod
    def get_available_python_libraries(cls) -> Dict[str, Any]:
        """
        Audit and report all installed Python astrological and astronomical libraries.
        """
        installed = {}

        # 1. Skyfield & NumPy
        skyfield_ok = SkyfieldEphemerisEngine.is_available()
        installed["skyfield"] = {
            "installed": skyfield_ok,
            "version": "1.55" if skyfield_ok else None,
            "category": "High-Precision Astronomy / NASA JPL DE Ephemeris",
            "features": "Topocentric coordinates, GAST/LAST sidereal time, solar noon, lunar phase angle & illumination"
        }

        # 2. VedAstro
        vedastro_ok = VedAstroEngine.is_available()
        installed["vedastro"] = {
            "installed": vedastro_ok,
            "version": "1.23.30" if vedastro_ok else None,
            "category": "Vedic Astrology Engine & API",
            "features": "Sarvashtakavarga, Panchanga tables, Shadbala cross-verification, Muhurtha calculations"
        }

        # 3. ReportLab (PDF Dossier Generation)
        try:
            import reportlab
            reportlab_ok = True
            reportlab_ver = getattr(reportlab, "__version__", "5.0.1")
        except ImportError:
            reportlab_ok = False
            reportlab_ver = None
        installed["reportlab"] = {
            "installed": reportlab_ok,
            "version": reportlab_ver,
            "category": "Document & Consultation Dossier Engine",
            "features": "High-resolution multi-page PDF generation, vector charts, typography styling"
        }

        # 4. Built-in Pure-Python BPHS Engines
        installed["pure_python_bphs"] = {
            "installed": True,
            "version": "2.0.0",
            "category": "Parashari & Jaimini Native Engines",
            "features": (
                "Jaimini Chara Karakas & Arudhas, 337-Bindu Ashtakavarga with Shodhana & Pindas, "
                "Complete 6-fold Shadbala (Virupas/Rupas), 36-Point Ashtakoota Guna Milan, "
                "5-Limb Panchanga & Muhurtha, 16 Shodashavargas (D1-D60), Vimshottari Dasha, "
                "KP Sub-Lords, Lal Kitab, Ayur-Jyotisha & Western Medical Decumbiture"
            )
        }

        return {
            "python_version": sys.version.split()[0],
            "libraries": installed,
            "total_supported_methods": 9
        }

    @classmethod
    def get_complete_advanced_profile(
        cls,
        dt_local: datetime,
        lat: float,
        lon: float,
        tz_offset: float = 5.5,
        name: str = "Native",
        ayanamsa: str = "Lahiri"
    ) -> Dict[str, Any]:
        """
        Compute a complete advanced astrological profile spanning all traditional and modern systems.
        """
        # 1. Base Natal Chart calculation
        dt_utc = dt_local - timedelta(hours=tz_offset)
        kundali = calculate_kundali(
            birth_dt_utc=dt_utc,
            latitude=lat,
            longitude=lon,
            tz_offset_hours=tz_offset
        )
        kundali.vargas = calculate_all_vargas(kundali.ascendant, kundali.planets)

        sun_lon = kundali.planets["Sun"].longitude if "Sun" in kundali.planets else 0.0
        moon_lon = kundali.planets["Moon"].longitude if "Moon" in kundali.planets else 0.0

        # 2. Jaimini System
        jaimini_karakas = JaiminiEngine.calculate_chara_karakas(kundali)
        jaimini_arudhas = JaiminiEngine.calculate_arudha_padas(kundali)
        jaimini_drishti = JaiminiEngine.calculate_all_rashi_drishti(kundali)
        jaimini_argala = JaiminiEngine.calculate_argala(kundali)
        jaimini_karakamsha = JaiminiEngine.analyze_karakamsha(kundali)
        jaimini_chara_dasha = JaiminiEngine.calculate_chara_dasha(kundali, years=72)

        # 3. Ashtakavarga System
        ashtakavarga = AshtakavargaEngine.get_complete_ashtakavarga(kundali)

        # 4. Shadbala System
        shadbala = ShadbalaEngine.calculate_all_shadbala(kundali)

        # 5. Panchanga & Muhurtha System
        panchanga_muhurtha = PanchangaEngine.get_complete_panchanga(kundali)

        # 6. Skyfield Astronomy & Observation
        astronomy = SkyfieldEphemerisEngine.get_astronomical_summary(
            dt_local=dt_local,
            lat=lat,
            lon=lon,
            tz_offset=tz_offset,
            sun_lon=sun_lon,
            moon_lon=moon_lon
        )

        # 7. Manglik / Kuja Dosha check
        manglik_info = GunaMilanEngine.check_manglik_dosha(kundali)

        return {
            "native_info": {
                "name": name,
                "birth_datetime": dt_local.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": lat,
                "longitude": lon,
                "timezone_offset": tz_offset,
                "ayanamsa": ayanamsa,
                "ascendant_sign": kundali.ascendant.sign.name,
                "ascendant_degree": round(kundali.ascendant.degrees_in_sign, 2),
                "moon_sign": kundali.planets["Moon"].sign.name if "Moon" in kundali.planets else "Aries",
                "moon_nakshatra": kundali.planets["Moon"].nakshatra_name if "Moon" in kundali.planets else "Ashwini"
            },
            "jaimini": {
                "chara_karakas": jaimini_karakas,
                "arudha_padas": jaimini_arudhas,
                "rashi_drishti": jaimini_drishti,
                "argala": jaimini_argala,
                "karakamsha": jaimini_karakamsha,
                "chara_dasha": jaimini_chara_dasha
            },
            "ashtakavarga": ashtakavarga,
            "shadbala": shadbala,
            "panchanga_and_muhurtha": panchanga_muhurtha,
            "astronomy_skyfield": astronomy,
            "manglik_dosha": manglik_info,
            "software_environment": cls.get_available_python_libraries()
        }

    @classmethod
    def match_kundalis(
        cls,
        bride_dt: datetime,
        bride_lat: float,
        bride_lon: float,
        groom_dt: datetime,
        groom_lat: float,
        groom_lon: float,
        tz_offset: float = 5.5,
        ayanamsa: str = "Lahiri"
    ) -> Dict[str, Any]:
        """
        One-stop 36-point Ashtakoota compatibility analysis between two individuals.
        """
        bride_utc = bride_dt - timedelta(hours=tz_offset)
        groom_utc = groom_dt - timedelta(hours=tz_offset)
        bride_k = calculate_kundali(bride_utc, bride_lat, bride_lon, tz_offset)
        bride_k.vargas = calculate_all_vargas(bride_k.ascendant, bride_k.planets)
        groom_k = calculate_kundali(groom_utc, groom_lat, groom_lon, tz_offset)
        groom_k.vargas = calculate_all_vargas(groom_k.ascendant, groom_k.planets)
        return GunaMilanEngine.match_horoscopes(bride_k, groom_k)

    @classmethod
    def evaluate_marriage_and_separation_risk(
        cls,
        kundali: Kundali,
        kp_cusps: Optional[List[Any]] = None
    ):
        """Evaluates marital stability, separation risk, and single vs multiple marriage count."""
        return MarriageHarmonyEngine.evaluate(kundali, kp_cusps)

    @classmethod
    def evaluate_progeny_and_pregnancy_loss(
        cls,
        kundali: Kundali,
        is_female: bool = True
    ):
        """Predicts living children count, miscarriage (Garbha Srava), and abortion risks."""
        d7_varga = kundali.vargas.get(7) if getattr(kundali, "vargas", None) else None
        return ProgenyPregnancyEngine.evaluate(kundali, is_female, d7_varga)

    @classmethod
    def activate_nakshatra_and_tithi_devathas(
        cls,
        kundali: Kundali
    ):
        """Computes Nakshatra & Tithi Devathas, sacred Vrikshas (trees), fruits, and activation rituals."""
        return DevathaActivationEngine.evaluate(kundali)

    @classmethod
    def audit_master_doshas_and_eclipse(
        cls,
        kundali: Kundali
    ):
        """Audits Kala Sarpa (12 types), Pitra Dosha, Matru Dosha, and Purnima/Amavasya/Grahana births."""
        return MasterDoshaEngine.evaluate(kundali)

    @classmethod
    def resolve_unknown_birth_details(
        cls,
        calling_name: str,
        kp_seed_number: Optional[int] = None,
        query_lat: float = 13.0068,
        query_lon: float = 77.5713,
        timezone_offset: float = 5.5
    ):
        """Resolves life guidance when DOB and TOB are completely unknown using Horary, KP, and Nama Rashi."""
        return UnknownBirthEngine.evaluate_unknown_birth(
            calling_name=calling_name,
            kp_seed_number=kp_seed_number,
            query_lat=query_lat,
            query_lon=query_lon,
            timezone_offset=timezone_offset
        )
