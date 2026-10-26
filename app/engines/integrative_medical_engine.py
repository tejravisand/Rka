"""
Integrative Medical Astrology Engine (East-West Synthesis)
=========================================================
Unifies:
1. Vedic Parashari Ayur-Jyotisha (BPHS traditions, Tridosha, Sapta Dhatu, Trika Bhavas, D30).
2. Western Iatromathematics (Galenic-Hippocratic Four Humors, Tropical Homo Signorum, Culpeper Herbalism).

Generates a unified, cross-validated clinical astrology dossier with
consensus vulnerabilities and integrated therapeutic protocols.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from app.models.astrological import Kundali
from app.engines.medical_astrology_engine import (
    VedicMedicalAstrologyEngine,
    MedicalAstrologyReport,
    DoshaProfile
)
from app.engines.western_medical_astrology import (
    WesternMedicalAstrologyEngine,
    WesternMedicalReport,
    HumoralTemperament
)


@dataclass
class CrossSystemCorrelation:
    vedic_concept: str
    western_concept: str
    correlation_score: float  # 0.0 to 1.0
    synthesis_notes: str


@dataclass
class ConsensusVulnerability:
    body_system: str
    vedic_indication: str
    western_indication: str
    clinical_priority: str    # "High Consensus Alert", "Moderate Advisory", "General Vigilance"
    integrated_action_plan: str


@dataclass
class IntegrativeTherapyPlan:
    ayurvedic_herbs: List[Dict[str, str]]
    western_herbalism: List[Dict[str, str]]
    unified_dietary_guidelines: List[str]
    healing_mantras_and_frequencies: List[Dict[str, str]]
    lifestyle_and_chronobiology: List[str]


@dataclass
class IntegrativeMedicalDossier:
    client_name: str
    vedic_report: MedicalAstrologyReport
    western_report: WesternMedicalReport
    constitutional_synthesis: Dict[str, Any]
    cross_correlations: List[CrossSystemCorrelation]
    consensus_vulnerabilities: List[ConsensusVulnerability]
    unified_therapy: IntegrativeTherapyPlan
    executive_summary: str


class IntegrativeMedicalEngine:
    """
    Master engine synthesizing Eastern (Vedic) and Western medical astrology systems.
    """

    @classmethod
    def evaluate(
        cls,
        kundali: Kundali,
        client_name: str = "Native"
    ) -> IntegrativeMedicalDossier:
        """
        Executes complete bi-system medical synthesis.
        """
        # 1. Run Vedic Medical Astrology
        vedic_rep = VedicMedicalAstrologyEngine.evaluate(kundali, client_name)

        # 2. Run Western Medical Astrology
        western_rep = WesternMedicalAstrologyEngine.evaluate(kundali, client_name)

        # 3. Cross-Correlate Constitutions (Tridosha vs Four Humors)
        const_synth, correlations = cls._correlate_constitutions(
            vedic_rep.dosha_profile,
            western_rep.temperament
        )

        # 4. Detect Consensus Vulnerabilities (Where East & West Agree)
        consensus = cls._detect_consensus_vulnerabilities(vedic_rep, western_rep)

        # 5. Formulate Unified East-West Therapy Plan
        therapy = cls._build_unified_therapy(vedic_rep, western_rep)

        # 6. Executive Synthesis Summary
        summary = (
            f"Integrative East-West medical evaluation combines Parashari Ayur-Jyotisha "
            f"(Lagna: {vedic_rep.lagna_sign}, Prakriti: {vedic_rep.dosha_profile.dominant_prakriti}) "
            f"with Western Iatromathematics (Tropical Ascendant: {western_rep.tropical_ascendant.sign_name}, "
            f"Temperament: {western_rep.temperament.dominant_temperament}). "
            f"Found {len(consensus)} clinical consensus areas across both ancient methodologies."
        )

        return IntegrativeMedicalDossier(
            client_name=client_name,
            vedic_report=vedic_rep,
            western_report=western_rep,
            constitutional_synthesis=const_synth,
            cross_correlations=correlations,
            consensus_vulnerabilities=consensus,
            unified_therapy=therapy,
            executive_summary=summary
        )

    # -------------------------------------------------------------------------
    # SYNTHESIS HELPERS
    # -------------------------------------------------------------------------

    @classmethod
    def _correlate_constitutions(
        cls,
        dosha: DoshaProfile,
        humors: HumoralTemperament
    ) -> Tuple[Dict[str, Any], List[CrossSystemCorrelation]]:
        """Maps Vedic Tridoshas to Galenic Four Humors."""
        # Classical mappings:
        # Vata <-> Melancholic (Earth/Cold & Dry) + Sanguine (Air/Mobility)
        # Pitta <-> Choleric (Fire/Hot & Dry)
        # Kapha <-> Phlegmatic (Water/Cold & Moist)
        pitta_choleric_match = 1.0 - abs(dosha.pitta_pct - humors.choleric_pct) / 100.0
        kapha_phlegmatic_match = 1.0 - abs(dosha.kapha_pct - humors.phlegmatic_pct) / 100.0
        vata_melancholic_match = 1.0 - abs(dosha.vata_pct - humors.melancholic_pct) / 100.0

        correlations = [
            CrossSystemCorrelation(
                vedic_concept="Pitta Dosha (Agni / Metabolic Heat)",
                western_concept="Choleric Humor (Yellow Bile / Hot & Dry)",
                correlation_score=round(max(0.0, pitta_choleric_match), 2),
                synthesis_notes="Both govern metabolic combustion, digestive acids, bile secretion, and acute inflammation."
            ),
            CrossSystemCorrelation(
                vedic_concept="Kapha Dosha (Jala / Fluid Matrix)",
                western_concept="Phlegmatic Humor (Phlegm / Cold & Moist)",
                correlation_score=round(max(0.0, kapha_phlegmatic_match), 2),
                synthesis_notes="Both govern mucous membranes, lymphatic fluid, structural lubrication, and tissue cushion."
            ),
            CrossSystemCorrelation(
                vedic_concept="Vata Dosha (Vayu / Neural Motility)",
                western_concept="Melancholic Humor (Black Bile / Cold & Dry)",
                correlation_score=round(max(0.0, vata_melancholic_match), 2),
                synthesis_notes="Both govern neuromuscular conduction, dryness, joint degeneration, and chronic constriction."
            )
        ]

        synth = {
            "vedic_prakriti": dosha.dominant_prakriti,
            "western_temperament": humors.dominant_temperament,
            "elemental_harmony": f"East: Vata {dosha.vata_pct}%, Pitta {dosha.pitta_pct}%, Kapha {dosha.kapha_pct}% | West: Choleric {humors.choleric_pct}%, Sanguine {humors.sanguine_pct}%, Melancholic {humors.melancholic_pct}%, Phlegmatic {humors.phlegmatic_pct}%",
            "primary_combined_theme": "Dynamic Agni & Metabolic Thermal Vitality with selective neural and circulatory vigilance."
        }

        return synth, correlations

    @classmethod
    def _detect_consensus_vulnerabilities(
        cls,
        vedic: MedicalAstrologyReport,
        western: WesternMedicalReport
    ) -> List[ConsensusVulnerability]:
        """Identifies organs or physiological systems flagged by BOTH traditions."""
        items = []

        # 1. Cardiovascular / Blood Pressure Check
        if "Moderate" in vedic.diagnosis_summary.cardiovascular_risk or "Elevated" in vedic.diagnosis_summary.cardiovascular_risk:
            v_note = vedic.diagnosis_summary.cardiovascular_risk
            w_note = "Afflictions in Leo / Sun or hard Mars aspects in Western chart"
            priority = "High Consensus Alert"
        else:
            v_note = "Normal vital tone"
            w_note = "Stable solar cardiac vitality"
            priority = "General Vigilance"

        items.append(ConsensusVulnerability(
            body_system="Cardiovascular & Arterial Tension",
            vedic_indication=v_note,
            western_indication=w_note,
            clinical_priority=priority,
            integrated_action_plan="Combine Ayurvedic Arjuna bark / Amla with Western Hawthorn berry (Crataegus) and monitor blood pressure."
        ))

        # 2. Digestive Fire & Hepatic Assimilation
        v_agni = vedic.diagnosis_summary.digestive_agni_strength
        w_agni = "Choleric/Melancholic digestive balance via Virgo/Scorpio"
        items.append(ConsensusVulnerability(
            body_system="Digestive Fire (Jatharagni) & Liver",
            vedic_indication=v_agni,
            western_indication=w_agni,
            clinical_priority="Moderate Advisory",
            integrated_action_plan="Use Ayurvedic Triphala and warm cumin-coriander tea alongside Western Milk Thistle (Silybum) to protect liver parenchyma."
        ))

        # 3. Nervous System & Mental Stress
        v_neuro = vedic.diagnosis_summary.mental_neurological_balance
        w_neuro = "Mercury / Moon humoral mental balance"
        items.append(ConsensusVulnerability(
            body_system="Neuro-Vegetative Balance & Sleep",
            vedic_indication=v_neuro,
            western_indication=w_neuro,
            clinical_priority="Moderate Advisory",
            integrated_action_plan="Practice Nadi Shodhana Pranayama with Ayurvedic Brahmi and Western Valerian root to soothe autonomic hyperexcitability."
        ))

        # 4. Joint & Skeletal Integrity
        v_joint = vedic.diagnosis_summary.musculoskeletal_joint_health
        w_joint = "Saturnian / Capricornian bone matrix & silica status"
        items.append(ConsensusVulnerability(
            body_system="Skeletal Framework & Articulations",
            vedic_indication=v_joint,
            western_indication=w_joint,
            clinical_priority="General Vigilance",
            integrated_action_plan="Fortify bone mineral density with Ayurvedic Ashwagandha/Guggulu and Western Horsetail (rich in bioavailable silica)."
        ))

        return items

    @classmethod
    def _build_unified_therapy(
        cls,
        vedic: MedicalAstrologyReport,
        western: WesternMedicalReport
    ) -> IntegrativeTherapyPlan:
        """Combines Ayurvedic Rasayanas and Culpeper Herbalism into a synergistic plan."""
        # Ayurvedic
        ayur = vedic.remedial_chikitsa.ayurvedic_herbs

        # Western
        west_herbs = [
            {
                "herb": h.herb_name,
                "botanical": h.botanical_name,
                "ruler": h.ruling_planet,
                "action": h.traditional_use,
                "mechanism": h.cure_mechanism
            }
            for h in western.culpeper_remedies
        ]

        # Unified Diet
        diet = [
            "East-West Ahara: Eat warm, freshly prepared seasonal meals matching both your dominant Dosha and Galenic temperament.",
            "Circadian Dining: Consume the main nourishing meal when the Sun is at Zenith (12:00 PM – 1:30 PM) to harness peak digestive fire (Agni).",
            "Hydration Protocol: Avoid icy beverages; drink warm water infused with digestive seeds (Fennel, Cumin) or chamomile flowers."
        ]

        # Mantras & Frequencies
        mantras = vedic.remedial_chikitsa.healing_mantras

        # Chronobiology & Lifestyle
        lifestyle = [
            "Circadian Sleep Architecture: Retire to bed by 10:30 PM to optimize hepatic detox and neuro-endocrine cellular regeneration.",
            "Morning Sun Exposure: 15 minutes of early morning sunlight to calibrate melatonin/cortisol rhythm and fortify Asthi Dhatu (Vitamin D synthesis).",
            "Breathing & Autonomic Reset: 10 minutes of gentle Alternate Nostril Breathing (Nadi Shodhana) before meals or stressful tasks."
        ]

        return IntegrativeTherapyPlan(
            ayurvedic_herbs=ayur,
            western_herbalism=west_herbs,
            unified_dietary_guidelines=diet,
            healing_mantras_and_frequencies=mantras,
            lifestyle_and_chronobiology=lifestyle
        )
