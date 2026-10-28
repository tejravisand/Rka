"""
Mobile Numbers & Vehicle Numbers Harmony Engine.
Implements:
1. Mobile Number Numerology:
   - Total sum of 10-digit mobile numbers (single and compound Chaldean).
   - Repeated digits analysis (avoiding 4s, 8s or volatile clusters; favoring 1, 3, 5, 6).
   - Exact Favourable Mobile Number Totals & Compounds.
   - Exact Unfavourable / Inimical Mobile Number Totals to Avoid.
   - Recommended ending digit sequences.
   - Specific mobile number compatibility validator.
2. Vehicle Registration Number Numerology & Astrology:
   - 4th House (Vahana Bhava) & Venus (Vahana Karaka) planetary integration.
   - 4-digit vehicle plate sums & full alphanumeric Chaldean plate sums.
   - Exact Favourable Vehicle Plate Totals (Safety, smooth mechanics, resale prestige).
   - Exact Unfavourable / Dangerous Vehicle Plate Totals to Strictly Avoid (Accident risks, 8th/6th house clash).
   - Vahana Varna (Vehicle lucky colors & colors to avoid) and Directional Parking Vastu.
   - Specific vehicle plate compatibility validator.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from app.models.astrological import Kundali
from app.core.constants import SIGN_LORDS, ZODIAC_SANSKRIT
from app.engines.numerology_engine import (
    CHALDEAN_MAP,
    CHALDEAN_COMPOUNDS,
    NUMBER_RELATIONS,
    NUMBER_RULERS,
    LUCKY_ATTRIBUTES,
    reduce_to_single_digit
)
from app.engines.lifestyle_advisor import PLANET_COLORS


@dataclass
class MobileEvaluationResult:
    mobile_number: str
    total_digits_sum: int
    reduced_single_digit: int
    ruling_planet: str
    compound_vibration_meaning: str
    compatibility_verdict: str         # "SUPREMELY AUSPICIOUS", "FAVORABLE", "MODERATE / NEUTRAL", "UNFAVORABLE / AVOID"
    digit_clustering_notes: str        # Notes on repeated 4s, 8s, 9s, etc.
    recommendation: str


@dataclass
class MobileNumberGuidance:
    favourable_single_totals: List[int]
    favourable_compound_totals: List[int]
    unfavourable_single_totals: List[int]
    unfavourable_compound_totals: List[int]
    best_repeated_digits: List[int]
    digits_to_avoid_repeating: List[int]
    recommended_ending_patterns: List[str]
    strategic_usage_advice: str
    evaluated_custom_number: Optional[MobileEvaluationResult] = None


@dataclass
class VehiclePlateEvaluationResult:
    plate_number: str
    four_digit_sum: int
    four_digit_reduced: int
    full_alphanumeric_sum: int
    full_alphanumeric_reduced: int
    ruling_planet: str
    safety_and_fortune_verdict: str     # "EXCELLENT — SAFE & PRESTIGIOUS", "FAVORABLE", "MODERATE", "UNFAVORABLE / CAUTION"
    astrological_alignment: str        # Harmony with 4th Lord & Venus
    recommendation: str


@dataclass
class VehicleNumberGuidance:
    fourth_house_lord: str
    fourth_house_sign: str
    favourable_plate_single_sums: List[int]
    favourable_plate_compounds: List[int]
    unfavourable_plate_single_sums: List[int]
    unfavourable_plate_compounds: List[int]
    lucky_vehicle_colors: List[str]
    caution_vehicle_colors: List[str]
    auspicious_parking_direction: str
    strategic_vehicle_advice: str
    evaluated_custom_plate: Optional[VehiclePlateEvaluationResult] = None
    vehicle_ownership_diagnosis: str = ""
    four_wheeler_feasibility: str = ""
    remedy_for_vehicle_acquisition: str = ""


class NumberHarmonyEngine:
    """Calculates mobile and vehicle number vibrations, compatibility, and safety."""

    @classmethod
    def evaluate_mobile_number_guidance(
        cls,
        mulank: int,
        bhagyank: int,
        specific_mobile: Optional[str] = None
    ) -> MobileNumberGuidance:
        """
        Determines universally favourable and unfavourable mobile numbers based on client's
        Mulank (Birth Number) and Bhagyank (Destiny Number).
        """
        friendly_m = NUMBER_RELATIONS[mulank]["friendly"]
        inimical_m = NUMBER_RELATIONS[mulank]["inimical"]

        # Favourable single totals: Friendly to Mulank & universally benefic (1, 3, 5, 6)
        fav_singles = [n for n in [1, 3, 5, 6] if n in friendly_m or n == mulank]
        if not fav_singles:
            fav_singles = friendly_m[:3]

        # Inimical single totals
        unfav_singles = inimical_m

        # Auspicious Chaldean compounds for mobile numbers (reducing to 1, 3, 5, 6)
        fav_compounds = [14, 15, 19, 23, 24, 32, 33, 37, 41, 42, 45, 46, 50, 51]
        fav_compounds = [c for c in fav_compounds if reduce_to_single_digit(c) in fav_singles]

        # Dangerous compounds to avoid in mobile phones
        unfav_compounds = [13, 16, 18, 26, 28, 29, 43, 44, 48]

        # Repeated digits:
        best_repeats = [1, 5, 6, 3] if mulank not in [4, 8] else [5, 6, 7]
        avoid_repeats = [4, 8]  # 4 = Rahu (sudden disconnects, misunderstandings), 8 = Saturn (sluggish callbacks)
        if mulank == 8:
            avoid_repeats = [1, 4, 9]

        endings = [
            f"Ending with {fav_singles[0]} (e.g. ...{fav_singles[0]}{fav_singles[0]})",
            "Ascending doublets: ...23, ...37, ...45, ...56",
            "Royal Star combinations: ending in ...23, ...24, or ...33"
        ]

        advice = (
            f"For Mulank {mulank} (ruled by {NUMBER_RULERS[mulank]['planet'].split('(')[0]}), "
            f"your mobile phone is your primary commercial antenna. "
            f"Ensure the total 10-digit sum reduces to {', '.join(map(str, fav_singles))}. "
            f"Avoid SIM cards whose total sums to {', '.join(map(str, unfav_singles))} "
            f"or contains clustered triples of {', '.join(map(str, avoid_repeats))}."
        )

        custom_res = None
        if specific_mobile:
            custom_res = cls.evaluate_specific_mobile(specific_mobile, mulank, bhagyank)

        return MobileNumberGuidance(
            favourable_single_totals=fav_singles,
            favourable_compound_totals=fav_compounds[:8],
            unfavourable_single_totals=unfav_singles,
            unfavourable_compound_totals=unfav_compounds[:6],
            best_repeated_digits=best_repeats,
            digits_to_avoid_repeating=avoid_repeats,
            recommended_ending_patterns=endings,
            strategic_usage_advice=advice,
            evaluated_custom_number=custom_res
        )

    @classmethod
    def evaluate_specific_mobile(
        cls,
        mobile_str: str,
        mulank: int,
        bhagyank: int
    ) -> MobileEvaluationResult:
        """Evaluates a concrete 10-digit mobile phone number for compatibility."""
        clean_num = "".join(ch for ch in mobile_str if ch.isdigit())
        if not clean_num:
            clean_num = "9845012345"

        digit_sum = sum(int(d) for d in clean_num)
        single = reduce_to_single_digit(digit_sum)
        ruler = NUMBER_RULERS[single]["planet"]
        meaning = CHALDEAN_COMPOUNDS.get(digit_sum, f"Compound {digit_sum} reduces to {single}.")

        # Check clusters
        counts = {d: clean_num.count(d) for d in set(clean_num)}
        cluster_warnings = []
        if counts.get('4', 0) >= 3:
            cluster_warnings.append("High repetition of '4' (Rahu): Prone to sudden electronic glitches and miscommunications.")
        if counts.get('8', 0) >= 3:
            cluster_warnings.append("High repetition of '8' (Saturn): Causes chronic delays in incoming business deals.")
        if counts.get('2', 0) >= 4:
            cluster_warnings.append("Excessive '2' (Moon): Can trigger emotional indecision and mood swings.")

        friendly_m = NUMBER_RELATIONS[mulank]["friendly"]
        inimical_m = NUMBER_RELATIONS[mulank]["inimical"]

        if single in friendly_m and digit_sum not in [13, 16, 18, 26, 28]:
            verdict = "SUPREMELY AUSPICIOUS (Highly Harmonious with your Birth Number)"
            recom = "Retain this mobile number as your primary business and communication line."
        elif single not in inimical_m:
            verdict = "FAVORABLE / MODERATE (Steady Vibration)"
            recom = "Suitable for everyday personal usage; ensure important deals are finalized on lucky dates."
        else:
            verdict = "UNFAVORABLE / CAUTION (Inimical Vibration to your Birth Energy)"
            recom = f"Consider porting or changing to a SIM card whose total sums to {', '.join(map(str, friendly_m[:3]))}."

        cluster_text = " | ".join(cluster_warnings) if cluster_warnings else "Balanced digit distribution without adverse clusters."

        return MobileEvaluationResult(
            mobile_number=clean_num,
            total_digits_sum=digit_sum,
            reduced_single_digit=single,
            ruling_planet=ruler,
            compound_vibration_meaning=meaning,
            compatibility_verdict=verdict,
            digit_clustering_notes=cluster_text,
            recommendation=recom
        )

    @classmethod
    def evaluate_vehicle_guidance(
        cls,
        kundali: Kundali,
        mulank: int,
        bhagyank: int,
        specific_plate: Optional[str] = None
    ) -> VehicleNumberGuidance:
        """
        Determines favourable and unfavourable vehicle numbers based on 4th House (Vahana Bhava),
        Venus (Vahana Karaka), and client's numerological vibrations.
        """
        lagna_idx = kundali.ascendant.sign.value
        h4_idx = (lagna_idx + 3) % 12
        h8_idx = (lagna_idx + 7) % 12
        h6_idx = (lagna_idx + 5) % 12

        fourth_lord = SIGN_LORDS[h4_idx]
        eighth_lord = SIGN_LORDS[h8_idx]
        sixth_lord = SIGN_LORDS[h6_idx]

        planet_num_map = {
            "Sun": 1, "Moon": 2, "Jupiter": 3, "Rahu": 4,
            "Mercury": 5, "Venus": 6, "Ketu": 7, "Saturn": 8, "Mars": 9
        }

        fourth_num = planet_num_map.get(fourth_lord, 6)
        eighth_num = planet_num_map.get(eighth_lord, 8)
        sixth_num = planet_num_map.get(sixth_lord, 6)

        friendly_m = NUMBER_RELATIONS[mulank]["friendly"]
        inimical_m = NUMBER_RELATIONS[mulank]["inimical"]

        # Favourable vehicle single sums: Friendly with Mulank AND harmonious with 4th Lord
        fav_singles = [n for n in [1, 3, 5, 6] if (n in friendly_m or n == fourth_num) and n != eighth_num]
        if not fav_singles:
            fav_singles = [fourth_num] if fourth_num not in inimical_m else [5, 6]

        # Inimical/Dangerous single sums (8th house lord = accident risk, 6th = police/repairs, inimical to Mulank)
        unfav_singles = list(set([eighth_num, sixth_num] + inimical_m))
        if eighth_num in fav_singles:
            fav_singles.remove(eighth_num)

        fav_compounds = [14, 15, 19, 23, 24, 32, 33, 37, 41, 42, 45, 46]
        fav_compounds = [c for c in fav_compounds if reduce_to_single_digit(c) in fav_singles]

        # Dangerous vehicle compounds (13 = sudden transformation, 16 = accident/shatter, 18 = fire/collision, 26 = breakdown)
        unfav_compounds = [13, 16, 18, 26, 28, 44]

        # Colors from LifestyleAdvisor / 4th lord
        lucky_colors = PLANET_COLORS.get(fourth_lord, {}).get("primary", ["Pure White", "Silver", "Royal Blue"])
        avoid_colors = PLANET_COLORS.get(eighth_lord, {}).get("avoid", ["Matte Black", "Blood Red"])
        if eighth_lord in PLANET_COLORS:
            for ac in PLANET_COLORS[eighth_lord].get("primary", []):
                if ac not in avoid_colors and ac not in lucky_colors:
                    avoid_colors.append(ac)

        # Auspicious parking direction based on 4th house element
        element_dirs = {
            "Fire": "East / South-East (Clean, well-ventilated space)",
            "Earth": "South / South-West (Solid, stable covered garage)",
            "Air": "West / North-West (Open, airy carport)",
            "Water": "North / North-East (Pristine, shaded driveway)"
        }
        fourth_element = kundali.houses[3].sign.element
        parking_dir = element_dirs.get(fourth_element, "North-East / East")

        advice = (
            f"Your 4th House (Vahana Bhava) is in {ZODIAC_SANSKRIT[h4_idx]} ruled by {fourth_lord}. "
            f"To guarantee vehicular safety, low maintenance expenses, and high travel comfort, "
            f"your 4-digit plate number must sum to {', '.join(map(str, fav_singles))}. "
            f"STRICTLY AVOID totals reducing to {eighth_num} (ruled by your 8th Lord {eighth_lord} — accident trigger) "
            f"or compound {', '.join(map(str, unfav_compounds[:3]))}."
        )

        # Classical Shastric Diagnosis for 4-Wheeler Feasibility & Obstacles
        diag_points = []
        four_wheeler_status = "Supported for 4-Wheeler Acquisition"
        remedy_items = []

        fourth_lord_pos = kundali.planets.get(fourth_lord)
        fourth_lord_house = ((fourth_lord_pos.sign.value - lagna_idx) % 12) + 1 if fourth_lord_pos else 4

        if fourth_lord_house in [6, 8, 12]:
            four_wheeler_status = "Delayed / 2-Wheeler Commute Primary (Vahana Pratibandhaka)"
            if fourth_lord_house == 8:
                diag_points.append(
                    f"4th Lord {fourth_lord} in 8th House (Dusthana): Classically causes 'Vahana Pratibandhaka' "
                    f"(chronic postponement of 4-wheeler purchase, hesitation to handle heavy traffic/maintenance, favoring 2-wheelers or public commute)."
                )
                remedy_items.append(f"Feed green grass/palak to cows on Wednesdays to strengthen 4th Lord {fourth_lord}")
            elif fourth_lord_house == 6:
                diag_points.append(
                    f"4th Lord {fourth_lord} in 6th House: Susceptibility to vehicle loan disputes or frequent minor mechanical repairs."
                )
                remedy_items.append(f"Chant Kavacham of 4th Lord {fourth_lord} for vehicular dispute protection")
            elif fourth_lord_house == 12:
                diag_points.append(
                    f"4th Lord {fourth_lord} in 12th House: Higher vehicle depreciation or primary usage for outstation/relocation."
                )

        sat_pos = kundali.planets.get("Saturn")
        rahu_pos = kundali.planets.get("Rahu")
        sat_house = ((sat_pos.sign.value - lagna_idx) % 12) + 1 if sat_pos else 0
        rahu_house = ((rahu_pos.sign.value - lagna_idx) % 12) + 1 if rahu_pos else 0

        if sat_house == 1:
            diag_points.append(
                "Saturn in 1st House (Lagna): Instills simplicity, frugal pragmatism, and preference for basic functional mobility."
            )
        if rahu_house == 1:
            diag_points.append(
                "Rahu in 1st House (Lagna): Creates driving caution, traffic stress, or hesitation to manage personal luxury 4-wheelers."
            )

        if 16 in kundali.vargas:
            d16 = kundali.vargas[16]
            mars_d16 = d16.placements.get("Mars")
            if mars_d16 and mars_d16.dignity == "Debilitated":
                four_wheeler_status = "Delayed / 2-Wheeler Commute Primary (Vahana Pratibandhaka)"
                diag_points.append(
                    "In D16 Shodashamsha, Mars (motor vehicle karaka) is DEBILITATED (Neecha). "
                    "This blocks effortless 4-wheeler car manifestation until a strong benefic/Lagna-lord period arrives."
                )
                remedy_items.append("Recite Hanuman Chalisa on Tuesdays to pacify afflicted conveyance karaka Mars in D16")

        if not diag_points:
            diag_points.append("4th House (Vahana Bhava) and conveyance indicators are well-aligned for smooth personal vehicle ownership.")
            remedy_items.append("Keep a small silver token or Ganesha idol on the vehicle dashboard for travel safety")

        veh_diagnosis = " ".join(diag_points)
        veh_remedies = " | ".join(remedy_items)

        custom_res = None
        if specific_plate:
            custom_res = cls.evaluate_specific_vehicle_plate(specific_plate, kundali, mulank, bhagyank)

        return VehicleNumberGuidance(
            fourth_house_lord=fourth_lord,
            fourth_house_sign=ZODIAC_SANSKRIT[h4_idx],
            favourable_plate_single_sums=fav_singles,
            favourable_plate_compounds=fav_compounds[:8],
            unfavourable_plate_single_sums=unfav_singles,
            unfavourable_plate_compounds=unfav_compounds,
            lucky_vehicle_colors=lucky_colors[:4],
            caution_vehicle_colors=avoid_colors[:3],
            auspicious_parking_direction=parking_dir,
            strategic_vehicle_advice=advice,
            evaluated_custom_plate=custom_res,
            vehicle_ownership_diagnosis=veh_diagnosis,
            four_wheeler_feasibility=four_wheeler_status,
            remedy_for_vehicle_acquisition=veh_remedies
        )

    @classmethod
    def evaluate_specific_vehicle_plate(
        cls,
        plate_str: str,
        kundali: Kundali,
        mulank: int,
        bhagyank: int
    ) -> VehiclePlateEvaluationResult:
        """Evaluates an actual vehicle plate (e.g. 'KA 01 AB 1234' or '1234')."""
        clean_plate = plate_str.upper().strip()
        digits = [ch for ch in clean_plate if ch.isdigit()]
        if not digits:
            digits = ['1', '2', '3', '4']

        # 4-digit sum
        last_4_digits = digits[-4:] if len(digits) >= 4 else digits
        four_sum = sum(int(d) for d in last_4_digits)
        four_reduced = reduce_to_single_digit(four_sum)

        # Full alphanumeric Chaldean sum
        full_sum = 0
        for ch in clean_plate:
            if ch.isdigit():
                full_sum += int(ch)
            elif ch.isalpha():
                full_sum += CHALDEAN_MAP.get(ch, 0)

        full_reduced = reduce_to_single_digit(full_sum)
        ruler = NUMBER_RULERS[four_reduced]["planet"]

        # Check against 4th lord and 8th lord
        lagna_idx = kundali.ascendant.sign.value
        h4_idx = (lagna_idx + 3) % 12
        h8_idx = (lagna_idx + 7) % 12
        fourth_lord = SIGN_LORDS[h4_idx]
        eighth_lord = SIGN_LORDS[h8_idx]

        planet_num_map = {
            "Sun": 1, "Moon": 2, "Jupiter": 3, "Rahu": 4,
            "Mercury": 5, "Venus": 6, "Ketu": 7, "Saturn": 8, "Mars": 9
        }
        fourth_num = planet_num_map.get(fourth_lord, 6)
        eighth_num = planet_num_map.get(eighth_lord, 8)

        friendly_m = NUMBER_RELATIONS[mulank]["friendly"]
        inimical_m = NUMBER_RELATIONS[mulank]["inimical"]

        if four_reduced == eighth_num or four_sum in [13, 16, 18]:
            verdict = "DANGER / UNFAVORABLE (Accident Vulnerability & Mechanical Headaches)"
            recom = f"High collision/repair vibration. Remedy: Keep an energized Hanuman / Ganesha idol on the dashboard, avoid speeding on {NUMBER_RULERS[eighth_num]['planet'].split('(')[0]} days, or change plate."
        elif four_reduced in friendly_m or four_reduced == fourth_num:
            verdict = "EXCELLENT — SAFE, PRESTIGIOUS & MECHANICALLY SMOOTH"
            recom = "Plate aligns harmoniously with your 4th House of conveyance and birth vibration. Safe for long journeys."
        elif four_reduced not in inimical_m:
            verdict = "FAVORABLE / MODERATE (Stable Conveyance)"
            recom = "Adequate vehicular balance; keep vehicle clean and tie a small black/red thread on the chassis for protection."
        else:
            verdict = "UNFAVORABLE (Frequent Minor Scratches & Sluggish Resale)"
            recom = "Plate is in tension with your personal numbers. Drive with mindful vigilance."

        align_text = f"4-digit sum {four_sum} ({four_reduced}) governed by {ruler.split('(')[0]}; 4th Lord is {fourth_lord}."

        return VehiclePlateEvaluationResult(
            plate_number=clean_plate,
            four_digit_sum=four_sum,
            four_digit_reduced=four_reduced,
            full_alphanumeric_sum=full_sum,
            full_alphanumeric_reduced=full_reduced,
            ruling_planet=ruler,
            safety_and_fortune_verdict=verdict,
            astrological_alignment=align_text,
            recommendation=recom
        )
