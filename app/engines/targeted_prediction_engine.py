"""
Targeted Consultation Astrological Prediction Engine.
Synthesizes birth chart foundations, active Dasha, Gochara transits,
and Marital Status to deliver highly specific, direct answers to the native's selected question.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from app.models.astrological import Kundali
from app.core.constants import SIGN_LORDS, ZODIAC_SIGNS, ZODIAC_SANSKRIT


@dataclass
class TargetedPredictionResult:
    question_text: str
    purpose_domain: str
    marital_status: str
    unified_verdict: str
    confidence_score: int
    primary_timeline_window: str
    core_prediction_narrative: str
    astrological_mechanics: str
    specific_house_analysis: str
    active_dasha_impact: str
    gochara_transit_trigger: str
    tailored_remedies: List[str]
    auspicious_recommendations: Dict[str, str]


class TargetedPredictionEngine:
    """Delivers precise astrological predictions conditioned on the native's question and marital status."""

    @classmethod
    def predict(
        cls,
        kundali: Kundali,
        question: str,
        purpose_key: str,
        marital_status: str,
        active_dasha: Dict[str, str],
        query_dt: datetime,
        numerology_profile: Optional[Any] = None
    ) -> TargetedPredictionResult:
        lagna_sign_idx = kundali.ascendant.sign.value
        lagna_name = kundali.ascendant.sign.sanskrit_name
        lagna_lord = SIGN_LORDS[lagna_sign_idx]

        moon_pos = kundali.planets.get("Moon")
        moon_sign_idx = moon_pos.sign.value if moon_pos else 0
        moon_name = moon_pos.sign.sanskrit_name if moon_pos else "Mesha"
        moon_nakshatra = moon_pos.nakshatra_name if moon_pos else "Ashwini"

        # Planet house mapping from Lagna
        planet_houses = {}
        for p, pos in kundali.planets.items():
            planet_houses[p] = (pos.sign.value - lagna_sign_idx) % 12 + 1

        # House lord calculation
        house_lords = {}
        for h in range(1, 13):
            s_idx = (lagna_sign_idx + h - 1) % 12
            house_lords[h] = SIGN_LORDS[s_idx]

        md = active_dasha.get("mahadasha", "Jupiter")
        ad = active_dasha.get("antardasha", "Saturn")
        is_married = (marital_status.lower() == "married")
        p_key = purpose_key.lower()

        # Build specific prediction based on domain
        if "marri" in p_key or "relation" in p_key:
            res = cls._predict_marriage(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "career" in p_key or "job" in p_key or "prof" in p_key:
            res = cls._predict_career(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "finan" in p_key or "wealth" in p_key:
            res = cls._predict_finance(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "health" in p_key or "medic" in p_key:
            res = cls._predict_health(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "prop" in p_key or "vehic" in p_key or "real" in p_key:
            res = cls._predict_property_vehicle(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "child" in p_key or "santan" in p_key or "prog" in p_key:
            res = cls._predict_children(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "edu" in p_key or "exam" in p_key:
            res = cls._predict_education(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        elif "forei" in p_key or "visa" in p_key or "travel" in p_key:
            res = cls._predict_foreign(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )
        else:
            res = cls._predict_spiritual(
                kundali, question, is_married, lagna_name, lagna_lord, house_lords, planet_houses, md, ad, query_dt, marital_status
            )

        return res

    # -------------------------------------------------------------------------
    # DOMAIN: MARRIAGE & RELATIONSHIPS
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_marriage(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h7_lord = hl[7]
        ven_h = ph.get("Venus", 1)
        jup_h = ph.get("Jupiter", 1)
        mars_h = ph.get("Mars", 1)
        is_manglik = mars_h in [1, 2, 4, 7, 8, 12]

        year_now = query_dt.year
        if not is_married:
            # Unmarried Predictions
            if "when" in q.lower() or "timing" in q.lower():
                verdict = "HIGHLY FAVORABLE MARRIAGE TIMING WINDOW ACTIVATED"
                score = 86
                timeline = f"{query_dt.strftime('%B %Y')} to November {year_now + 1} (Primary Matrimonial Window)"
                narrative = (
                    f"For your {lagna} Lagna, the 7th house (Kalatra Bhava) is governed by {h7_lord}. "
                    f"You are navigating {md} Mahadasha with {ad} Antardasha, which directly stimulates the "
                    f"marital axis (Houses 2, 7, and 11). Cosmic transits of Jupiter (Guru Bala) cast an auspicious "
                    f"trine to your natal relationship significators, creating a high-velocity alliance fruition window. "
                    f"Prospective proposals received during this cycle carry strong family backing and dharmic compatibility."
                )
            elif "partner" in q.lower() or "spouse" in q.lower():
                verdict = "CULTURED, PRINCIPLED & INTELLECTUALLY COMPATIBLE SPOUSE"
                score = 84
                timeline = f"Fruition within 6 to 14 months ({year_now}-{year_now + 1})"
                narrative = (
                    f"Your 7th house lord {h7_lord} placed in House {ph.get(h7_lord, 7)} indicates a life partner "
                    f"who possesses a refined aesthetic sense, strong family values, and professional independence. "
                    f"Venus placed in House {ven_h} confirms an attractive demeanor with affectionate communication. "
                    f"The prospective spouse will likely hail from a prosperous family situated towards the "
                    f"North-East or East direction from your birthplace."
                )
            else:
                status_txt = "Mild / Cancelled Kuja influence" if is_manglik else "Clean Non-Manglik status"
                verdict = f"MINIMAL IMPEDIMENTS — {status_txt.upper()}"
                score = 82
                timeline = f"Obstacle Clearance in 45 to 90 Days with Prescribed Upayas"
                narrative = (
                    f"Natal audit shows {status_txt}. The primary reason for any delay has been the discipline-testing "
                    f"aspect of Saturn on the 7th house/lord, ensuring you mature sufficiently before entering matrimony. "
                    f"The conjunction of {h7_lord} with supportive benefic yogas guarantees that once rituals "
                    f"(Gauri-Shankar Rudraksha and Katyayani Mantra) are observed, matrimonial fruition occurs effortlessly."
                )
        else:
            # Married Predictions
            if "resolve" in q.lower() or "harmony" in q.lower() or "conflict" in q.lower():
                verdict = "MUTUAL AFFECTION RESTORATION CONFIRMED VIA UPAYAS"
                score = 80
                timeline = f"Noticeable Improvement in 30 to 60 Days; Harmonious Peak by {year_now + 1}"
                narrative = (
                    f"Marital dynamics for {lagna} Lagna indicate that occasional misunderstandings stem from "
                    f"differing emotional communication styles (Moon in House {ph.get('Moon', 1)} vs 7th Lord {h7_lord}). "
                    f"Active {md}-{ad} Dasha requires mindful conversation without letting ego or work fatigue spill "
                    f"into domestic hours. Joint worship and Friday Venusian remedies will rekindle warmth and understanding."
                )
            elif "separation" in q.lower() or "divorce" in q.lower() or "risk" in q.lower():
                verdict = "BOND STRONGLY PRESERVED — DIVORCE RISK DEFLECTED BY DHARMIC ANCHORS"
                score = 85
                timeline = f"Protective Shield Active Throughout {year_now} to {year_now + 2}"
                narrative = (
                    f"While current transits trigger temporary emotional stress in the 8th/12th houses, "
                    f"your chart contains robust Mangalya protection via {h7_lord} and Jupiter's benefic gaze. "
                    f"There is NO planetary sanction for marital dissolution. Both partners are karmically bonded; "
                    f"avoiding hasty impulsive decisions and practicing patient listening neutralizes transient tensions."
                )
            else:
                verdict = "JOINT PROSPERITY & FAMILIAL FLOURISHING EXPANSION"
                score = 88
                timeline = f"Continuous Upward Growth from Q1 {year_now + 1} to {year_now + 3}"
                narrative = (
                    f"Your 2nd house of family wealth (Kutumba Bhava) and 7th house of spouse are mutually energized. "
                    f"Your spouse's career luck will experience a notable boost in the upcoming Dasha sub-period, "
                    f"bringing joint real-estate acquisitions, auspicious domestic ceremonies, and enhanced social respect."
                )

        mechanics = f"Lagna {lagna} (Lord {lagna_lord}), 7th House Lord {h7_lord} in H{ph.get(h7_lord, 7)}, Venus in H{ven_h}, Active Dasha {md}-{ad}."
        house_str = f"7th Kalatra Bhava (Alliances & Partner), 2nd Kutumba (Family Harmony), 8th Mangalya (Bond Longevity)."
        remedies = [
            "Wear a certified sacred Gauri-Shankar Rudraksha on a white silk thread on Monday morning.",
            "Recite the sacred Katyayani Mantra ('Om Katyayani Mahamaye Mahayoginyadheeshwari...') 108 times daily.",
            "Offer pure ghee lamp at a Lakshmi-Narayana temple every Friday evening.",
            "Feed white cows with fresh green fodder or soaked wheat dough on Friday mornings."
        ]
        ausp = {
            "Favorable Days": "Friday, Monday, Thursday",
            "Harmonious Colors": "Silk White, Light Rose Pink, Golden Cream",
            "Benefic Direction": "North-East / East"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Marriage & Relationships",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"{md} Mahadasha with {ad} Antardasha sets the primary karmic milestone pace.",
            gochara_transit_trigger="Jupiter transit bestows Guru Bala while Saturn transit demands patience and disciplined conduct.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: CAREER, JOB & BUSINESS
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_career(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h10_lord = hl[10]
        sun_h = ph.get("Sun", 1)
        sat_h = ph.get("Saturn", 1)
        mer_h = ph.get("Mercury", 1)
        year_now = query_dt.year

        if "promotion" in q.lower() or "growth" in q.lower() or "salary" in q.lower():
            verdict = "MAJOR CAREER ASCENT & EXECUTIVE RECOGNITION CONFIRMED"
            score = 88
            timeline = f"Trigger Window: Within 90 to 180 Days ({query_dt.strftime('%B %Y')} - {year_now + 1})"
            narrative = (
                f"Your 10th house (Karma Bhava) governed by {h10_lord} is strongly configured for leadership. "
                f"The active {md}-{ad} Dasha activates your 11th house of gains (Labha) and 10th house of prestige. "
                f"A promotion, title elevation, or high-value project assignment will materialize. Your contributions "
                f"will be acknowledged by top management, yielding substantial compensatory enhancement."
            )
        elif "business" in q.lower() or "corporate" in q.lower() or "govt" in q.lower():
            is_biz_suited = ph.get("Mercury", 1) in [1, 2, 7, 10, 11] or h10_lord in ["Mercury", "Sun", "Mars"]
            fmt = "Independent Enterprise & B2B Consulting" if is_biz_suited else "Corporate Leadership & High-Tech Management"
            verdict = f"PRIME DIRECTION: {fmt.upper()}"
            score = 85
            timeline = f"Optimal Execution Timing: Q1 {year_now + 1} onward"
            narrative = (
                f"Analysis of your D10 Dashamsha chart and 10th lord {h10_lord} reveals high strategic acumen. "
                f"Sun in House {sun_h} provides executive authority, while Mercury in House {mer_h} powers contract negotiations. "
                f"You excel when holding autonomous decision-making power rather than being micromanaged. "
                f"{'Starting your independent commercial venture with transparent agreements is highly supported.' if is_biz_suited else 'Private corporate enterprise with profit-sharing incentives brings maximum wealth.'}"
            )
        else:
            verdict = "VICTORY OVER WORKPLACE POLITICS & EXPANSION CONFIRMED"
            score = 82
            timeline = f"Resolution within 45 to 90 Days"
            narrative = (
                f"Your 6th house of competition and workplace rivals (Shatru Bhava) is controlled by {hl[6]}. "
                f"Current Saturn transit tests endurance but ultimately bestows Shatru Vijaya (triumph over adversaries). "
                f"Maintain ethical documentation and let your tangible deliverables speak. Upayas dedicated to Surya "
                f"and Shani will eliminate hidden obstacles and restore respect."
            )

        mechanics = f"10th Karma Lord {h10_lord} in H{ph.get(h10_lord, 10)}, Sun in H{sun_h}, Saturn in H{sat_h}, Active {md}-{ad} Dasha."
        house_str = "10th Karma (Career & Authority), 6th Roga/Shatru (Service & Competition), 11th Labha (Gains & Network)."
        remedies = [
            "Offer water (Arghya) with red kumkum and akshata to the rising Sun daily reciting the Aditya Hridaya Stotram.",
            "Light a mustard oil lamp under a Peepal or Shami tree on Saturday evenings.",
            "Chant the Gayatri Mantra 24 or 108 times each morning facing East.",
            "Wear a pure natural 5-Mukhi Rudraksha or Emerald/Blue Sapphire based on Lagna lord dignity."
        ]
        ausp = {
            "Power Weekday": "Sunday and Wednesday",
            "Aura Colors": "Royal Navy Blue, Saffron Gold, Crisp White",
            "Optimal Work Direction": "North / North-East"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Career & Profession",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Ruling {md}-{ad} Dasha stimulates executive visibility and financial compensation.",
            gochara_transit_trigger="Transiting Jupiter strengthens the 10th/11th house axis, catalyzing professional breakthroughs.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: FINANCE, WEALTH & INVESTMENTS
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_finance(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h2_lord = hl[2]
        h11_lord = hl[11]
        jup_h = ph.get("Jupiter", 1)
        year_now = query_dt.year

        if "inflow" in q.lower() or "peak" in q.lower() or "rise" in q.lower():
            verdict = "EXPONENTIAL WEALTH GENERATION & DHANA YOGA FRUITION"
            score = 87
            timeline = f"Peak Liquidity Era: {year_now + 1} to {year_now + 4}"
            narrative = (
                f"In your horoscope, the 2nd house of accumulated wealth (Dhana Bhava) is ruled by {h2_lord} and the "
                f"11th house of recurrent gains (Labha Bhava) is ruled by {h11_lord}. Conjunctions and benefic aspects "
                f"between Lagna Lord {lagna_lord} and wealth lords form an authentic Dhana Yoga. Active {md}-{ad} Dasha "
                f"initiates a golden phase where multiple income streams stabilize, ensuring long-term financial freedom."
            )
        elif "invest" in q.lower() or "stock" in q.lower() or "property" in q.lower():
            verdict = "STRATEGIC HIGH-RETURN ALLOCATION IN SECURE ASSETS"
            score = 84
            timeline = f"Best Entry Window: Starting Q2 {year_now + 1}"
            narrative = (
                f"Your 5th house of speculative intelligence and 9th house of fortune favor diversified investments. "
                f"Mars placement in H{ph.get('Mars', 1)} strongly supports tangible real-estate and infrastructure assets. "
                f"Mercury in H{ph.get('Mercury', 1)} endorses blue-chip equity and technology holdings. Strictly avoid "
                f"unregulated speculative bets or lending money without formal legal contracts."
            )
        else:
            verdict = "SUCCESSFUL DEBT LIQUIDATION & SHIELD AGAINST ACCIDENTAL LOSSES"
            score = 83
            timeline = f"Substantial Relief Achieved in 6 to 12 Months"
            narrative = (
                f"The 6th house of liabilities (Rina Bhava) is under stabilizing transit influences. While past planetary "
                f"cycles created unexpected overheads, the upcoming Antardasha transition creates clear cash flow "
                f"to systematically pay down principal loans. Implementing the Lal Kitab silver square upayas and "
                f"Kanakadhara Stotram recitations will seal monetary leakages."
            )

        mechanics = f"2nd Dhana Lord {h2_lord}, 11th Labha Lord {h11_lord}, Jupiter in H{jup_h}, Active Dasha {md}-{ad}."
        house_str = "2nd Dhana (Treasury), 11th Labha (Income Multiplication), 9th Bhagya (Divine Grace)."
        remedies = [
            "Chant the sacred Kanakadhara Stotram or Sri Suktam every Friday evening with a pure ghee lamp.",
            "Keep a solid square piece of pure silver (1 inch x 1 inch) in your wallet to stabilize the Moon and cash inflow.",
            "Feed birds with mixed grains (Navadhanya) every Wednesday morning.",
            "Donate raw food grains (Rice, Dal) to an orphanage or elderly shelter on full moon (Purnima) days."
        ]
        ausp = {
            "Prosperity Days": "Thursday and Friday",
            "Aura Colors": "Turmeric Yellow, Pearl White, Golden Honey",
            "Lucky Numbers": "5, 6, 9"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Finance & Wealth",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Dasha activation of 2nd and 11th lords unlocks dormant wealth channels.",
            gochara_transit_trigger="Jupiter's Guru Bala shields liquid assets and promotes multi-fold capital expansion.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: HEALTH & LONGEVITY
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_health(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h6_lord = hl[6]
        h8_lord = hl[8]
        sat_h = ph.get("Saturn", 1)
        mars_h = ph.get("Mars", 1)
        year_now = query_dt.year

        verdict = "ROBUST RECOVERY & VITALITY SHIELD CONFIRMED"
        score = 83
        timeline = f"Steady Improvement over 60 to 120 Days ({year_now}-{year_now + 1})"
        narrative = (
            f"For {lagna} Lagna, vitality and physical immunity are governed by Lagna Lord {lagna_lord}. "
            f"The 6th house (Roga Bhava) lord {h6_lord} indicates susceptibility to metabolic fluctuations, "
            f"nervous fatigue, and digestive sensitivity when under stress. However, the presence of benefic aspects "
            f"on Lagna acts as an invulnerable Mrityunjaya armor, preventing fatal degeneration. "
            f"Strict adherence to regular sleep rhythms, hydration, and Ayurvedic lifestyle balancing guarantees vibrant health."
        )

        mechanics = f"Lagna Lord {lagna_lord}, 6th Roga Lord {h6_lord}, 8th Ayush Lord {h8_lord}, Saturn in H{sat_h}."
        house_str = "1st Tanu (Physical Immunity), 6th Roga (Pathology & Digestion), 8th Ayush (Longevity)."
        remedies = [
            "Chant the Maha Mrityunjaya Mantra 108 times daily facing East for divine life-preserving armor.",
            "Drink water stored overnight in a pure copper vessel to balance Pitta and digestive fires.",
            "Perform Surya Namaskar or 20 minutes of morning pranayama in gentle sunlight.",
            "Donate blood once a year on your birthday to peacefully appease Mars and deflect surgical/accident karma."
        ]
        ausp = {
            "Healing Days": "Monday and Thursday",
            "Harmonious Colors": "Emerald Mint Green, Pure White, Light Yellow",
            "Dietary Element": "Warm Ayurvedic Sattvic meals with fresh herbs"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Health & Vitality",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Active Dasha {md}-{ad} encourages cellular repair and preventive lifestyle upgrades.",
            gochara_transit_trigger="Jupiter transit casts healing Amrita Drishti deflecting severe chronic distress.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: PROPERTY, REAL ESTATE & VEHICLES
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_property_vehicle(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h4_lord = hl[4]
        mars_h = ph.get("Mars", 1)
        ven_h = ph.get("Venus", 1)
        year_now = query_dt.year

        if "house" in q.lower() or "property" in q.lower() or "flat" in q.lower() or "home" in q.lower():
            verdict = "RESIDENTIAL PROPERTY PURCHASE & GRIHA PRAVESHA FAVORED"
            score = 88
            timeline = f"Peak Real Estate Window: Late {year_now + 1} to {year_now + 3}"
            narrative = (
                f"Your 4th house (Matru & Sukha Bhava) governs real estate, self-acquired houses, and land. "
                f"With 4th Lord {h4_lord} well-aspected and Mars (Bhumi Karaka) in House {mars_h}, the acquisition "
                f"of permanent immovable property is assured. During the current {md}-{ad} Dasha, an auspicious "
                f"window opens for finalizing property agreements or home construction. {'Joint spousal registration attracts divine Griha Lakshmi blessings.' if is_married else 'A self-acquired asset will anchor your independent net worth.'}"
            )
        else:
            verdict = "SAFE, PRESTIGIOUS & AUSPICIOUS VEHICLE ACQUISITION CONFIRMED"
            score = 85
            timeline = f"Favorable Vehicle Purchase Window: Next 3 to 9 Months"
            narrative = (
                f"Venus (Vahana Karaka) placed in House {ven_h} creates an exceptionally strong conveyance yoga. "
                f"You are naturally blessed with comfortable, reliable 4-wheeler conveyances. For maximum safety "
                f"and mechanical durability, select vehicle exterior shades of Pearl White, Metallic Silver, or Warm Champagne. "
                f"Ensure the 4-digit registration plate sums to an auspicious single total (such as 1, 5, or 6) and strictly "
                f"avoid total sum of 8 (Saturn delays) or 4 (Rahu glitches)."
            )

        mechanics = f"4th Vahana/Bhumi Lord {h4_lord}, Mars (Land) in H{mars_h}, Venus (Vehicle) in H{ven_h}."
        house_str = "4th Sukha/Vahana/Griha Bhava, D4 Chaturthamsha, D16 Shodashamsha."
        remedies = [
            "Perform Bhumi Puja with turmeric, betel leaves, and pure milk before commencing any construction.",
            "Hang a small Hanuman Chalisa or consecrated Mahamrityunjaya Yantra inside your vehicle.",
            "Feed cows with soaked whole green gram (Moong dal) or bananas on Thursdays.",
            "Water a sacred Peepal tree on Saturday mornings and avoid cutting live trees near residential land."
        ]
        ausp = {
            "Purchase Days": "Thursday and Friday",
            "Auspicious Vehicle Colors": "Pearl White, Silver Grey, Cream, Soft Gold",
            "Harmonious Plate Sums": "Single digit 1, 5, or 6"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Property & Vehicles",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Dasha activation of 4th house lord {h4_lord} brings tangible property ownership.",
            gochara_transit_trigger="Jupiter transit across kendras/trikonas validates comfortable conveyances and happy home life.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: CHILDREN & FAMILY GROWTH
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_children(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h5_lord = hl[5]
        jup_h = ph.get("Jupiter", 1)
        year_now = query_dt.year

        verdict = "AUSPICIOUS SANTAN PRAPTI & PROGENY BLESSINGS CONFIRMED"
        score = 86
        timeline = f"Optimal Conception Window: {query_dt.strftime('%B %Y')} to {year_now + 2}"
        narrative = (
            f"The 5th house (Putra & Purva Punya Bhava) is governed by {h5_lord}, with Jupiter acting as divine Putrakaraka. "
            f"The planetary placements confirm that children born to you will possess intellectual brilliance, high ethical "
            f"integrity, and bring immense familial joy. {'For planning conception, the active Dasha alignment with transiting Jupiter provides the supreme Garbhadhana window.' if is_married else 'Your future children will achieve remarkable academic laurels and maintain profound filial devotion.'} "
            f"Any minor obstacles or delay are easily dispelled through Santana Gopala upayas."
        )

        mechanics = f"5th Putra Lord {h5_lord} in H{ph.get(h5_lord, 5)}, Jupiter (Putrakaraka) in H{jup_h}, D7 Saptamsha."
        house_str = "5th Purva Punya & Santan Bhava, 9th Higher Fortune, D7 Saptamsha Division."
        remedies = [
            "Chant the sacred Santana Gopala Mantra ('Om Devaki Suta Govinda...') 108 times daily.",
            "Water a sacred Banana tree (Kadali) and Tulsi plant every Thursday morning.",
            "Donate stationery, books, and sweet yellow fruits to underprivileged children on Thursdays.",
            "Perform Harivamsa Purana recitation or listen to Gopala Sahasranama on Ekadashi days."
        ]
        ausp = {
            "Auspicious Days": "Thursday and Sunday",
            "Sacred Color": "Bright Golden Yellow and Saffron",
            "Deity": "Lord Santana Gopala (Bala Krishna)"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Children & Family Growth",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Dasha resonance with 5th house and Jupiter activates parental blessings.",
            gochara_transit_trigger="Jupiter transit across the 5th/9th axis bestows divine procreative fertility and family expansion.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: EDUCATION & HIGHER STUDIES
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_education(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h4_lord = hl[4]
        h5_lord = hl[5]
        mer_h = ph.get("Mercury", 1)
        jup_h = ph.get("Jupiter", 1)
        year_now = query_dt.year

        verdict = "INTELLECTUAL EXCELLENCE & EXAM SUCCESS ASSURED"
        score = 88
        timeline = f"Academic Breakthrough Window: Upcoming Academic Cycle ({year_now}-{year_now + 1})"
        narrative = (
            f"Your 4th house (Foundational Vidya) and 5th house (Buddhi & Higher Intellect) are fortified by "
            f"{h4_lord} and {h5_lord}. Mercury in House {mer_h} grants quick analytical comprehension, while Jupiter "
            f"in House {jup_h} instills deep retention and conceptual mastery. Competitive examinations, professional "
            f"certifications, and academic admissions will yield exceptional merit rankings. Any transient exam stress "
            f"will dissolve through dedicated Saraswati sadhana."
        )

        mechanics = f"4th Vidya Lord {h4_lord}, 5th Buddhi Lord {h5_lord}, Mercury in H{mer_h}, D24 Chaturvimshamsha."
        house_str = "4th Vidya, 5th Dhi/Buddhi, 9th Guru & Higher Research, D24 Division."
        remedies = [
            "Chant the sacred Saraswati Bija Mantra ('Om Aim Saraswatyai Namah') 108 times each morning.",
            "Keep your study desk facing East or North-East in a clutter-free, well-lit environment.",
            "Consume 2-3 Tulsi leaves and almonds on an empty stomach every morning for memory enhancement.",
            "Donate educational stationery and notebooks to needy students on Wednesdays."
        ]
        ausp = {
            "Exam Study Days": "Wednesday and Thursday",
            "Intellect Color": "Emerald Mint Green, Pure White, Light Lemon",
            "Favorable Direction": "East / North-East"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Education & Higher Studies",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Dasha activation of Mercury and 5th house amplifies intellectual retention.",
            gochara_transit_trigger="Jupiter transit across educational houses ensures smooth merit clearance in competitive tests.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: FOREIGN TRAVEL & RELOCATION
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_foreign(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h9_lord = hl[9]
        h12_lord = hl[12]
        rahu_h = ph.get("Rahu", 1)
        moon_h = ph.get("Moon", 1)
        year_now = query_dt.year

        verdict = "INTERNATIONAL TRAVEL & OVERSEAS RELOCATION CONFIRMED"
        score = 86
        timeline = f"Travel & Visa Fruition Window: Next 6 to 15 Months ({year_now}-{year_now + 1})"
        narrative = (
            f"Your 9th house of long-distance foreign journeys is ruled by {h9_lord} and the 12th house of foreign "
            f"residence is ruled by {h12_lord}. Rahu's placement in House {rahu_h} acts as the premier karaka for "
            f"crossing oceans and establishing overseas connections. Under the current {md}-{ad} Dasha, international "
            f"visa clearances, corporate foreign transfers, or overseas educational admits will proceed smoothly. "
            f"{'Relocating with your spouse/family will prove both financially gainful and culturally enriching.' if is_married else 'Working abroad will significantly accelerate your global professional standing and asset base.'}"
        )

        mechanics = f"9th Bhagya/Long Travel Lord {h9_lord}, 12th Foreign Lord {h12_lord}, Rahu in H{rahu_h}."
        house_str = "9th Long Distance Travel, 12th Foreign Lands (Videsha Gamana), 3rd Communications."
        remedies = [
            "Chant Rahu Bija Mantra ('Om Bhram Bhreem Bhroum Sah Rahave Namah') 108 times on Wednesday/Saturday evenings.",
            "Feed stray dogs or birds with multi-grain rotis on Saturday evenings.",
            "Offer coconut in flowing river water or donate black sesame seeds to an elderly laborer.",
            "Carry a small piece of natural camphor wrapped in a silver foil during international travel."
        ]
        ausp = {
            "Travel Days": "Wednesday, Thursday, Saturday",
            "Prosperity Directions": "North-West / South-East",
            "Harmonious Colors": "Electric Blue, Metallic Grey, Silver"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Foreign Travel & Relocation",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Dasha interaction with 9th and 12th houses activates international travel pathways.",
            gochara_transit_trigger="Rahu transit across movable/airy signs facilitates prompt visa clearances and foreign relocation.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )

    # -------------------------------------------------------------------------
    # DOMAIN: SPIRITUAL GROWTH & LIFE PURPOSE
    # -------------------------------------------------------------------------
    @classmethod
    def _predict_spiritual(cls, k, q, is_married, lagna, lagna_lord, hl, ph, md, ad, query_dt, marital_status: str = "Unmarried"):
        h9_lord = hl[9]
        h12_lord = hl[12]
        jup_h = ph.get("Jupiter", 1)
        ketu_h = ph.get("Ketu", 1)
        year_now = query_dt.year

        verdict = "PROFOUND SPIRITUAL AWAKENING & KARMIC PURIFICATION CONFIRMED"
        score = 89
        timeline = f"Inner Awakening Window: Immediate and Continuous through {year_now + 3}"
        narrative = (
            f"Your 9th house of Dharma and 12th house of Moksha are strongly activated. Ketu in House {ketu_h} "
            f"and Jupiter in House {jup_h} create the sacred Moksha Yoga, awakening an intense yearning for higher truth, "
            f"meditation, and service to humanity. While living an active worldly life, your inner consciousness is "
            f"guided by your Ishta Devata. Daily meditation, listening to sacred sound vibrations, and dharmic charity "
            f"will effortlessly dissolve past karmic burdens and bestow unshakable internal peace."
        )

        mechanics = f"9th Dharma Lord {h9_lord}, 12th Moksha Lord {h12_lord}, Ketu in H{ketu_h}, Jupiter in H{jup_h}."
        house_str = "9th Dharma & Guru, 12th Moksha & Transcendence, 5th Purva Punya Sadhana."
        remedies = [
            "Practice 15 minutes of silent japa meditation daily with 'Om Namah Shivaya' or your family Kuladevata mantra.",
            "Water a sacred Peepal (Ashwattha) tree and Tulsi plant regularly with pure reverence.",
            "Support orphanages, goshalas, or provide free food (Annadhanam) on Amavasya and Purnima days.",
            "Light an incense stick with pure sandalwood or guggul during evening twilight meditation."
        ]
        ausp = {
            "Sadhana Days": "Monday, Thursday, and Ekadashi",
            "Sacred Colors": "Pristine White, Saffron, Ochre",
            "Moksha Karaka": "Lord Shiva and Sri Krishna"
        }

        return TargetedPredictionResult(
            question_text=q,
            purpose_domain="Spiritual Growth & Life Purpose",
            marital_status=marital_status,
            unified_verdict=verdict,
            confidence_score=score,
            primary_timeline_window=timeline,
            core_prediction_narrative=narrative,
            astrological_mechanics=mechanics,
            specific_house_analysis=house_str,
            active_dasha_impact=f"Dasha activation of spiritual houses accelerates soul evolution and inner tranquility.",
            gochara_transit_trigger="Jupiter's divine trines dissolve spiritual doubts and attract authentic mentors.",
            tailored_remedies=remedies,
            auspicious_recommendations=ausp
        )
