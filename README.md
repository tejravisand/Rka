# Rka - Astrological Consultation & Analysis Engine

An advanced astrological computational engine and consultation platform supporting Parashara, KP, Lal Kitab, Numerology, VedAstro, Vedic Medical Astrology, Western Iatromathematics, and multi-method astrological dossiers.

## Features
- **Integrative East-West Medical Astrology**: Cross-system clinical synthesis combining:
  - Consensus diagnostic alerts where ancient Vedic and Western traditions converge.
  - Unified therapeutic protocols uniting Ayurvedic Rasayanas with Nicholas Culpeper's Western medical herbalism.
- **Vedic Medical Astrology (Ayur-Jyotisha & BPHS Traditions)**: Comprehensive Parashari health diagnostics including:
  - Tridosha constitutional analysis (Vata, Pitta, Kapha Prakriti & Vikriti).
  - Sapta Dhatu tissue status (Rasa, Rakta, Mamsa, Meda, Asthi, Majja, Shukra).
  - Trika Bhavas (6th Roga, 8th Randhra/Mrityu, 12th Vyaya) & Maraka/Badhaka health triggers.
  - Kaala Purusha 12-zone anatomical vulnerability mapping (Head to Feet).
  - D30 Trimshamsha Arishta and karmic disease propensities.
  - Classical Ayur-Jyotisha Chikitsa: Ayurvedic Rasayanas, Ahara (dietary guidelines), gemstone safety cautions, and healing mantras (Maha Mrityunjaya & Dhanvantari).
- **Western Medical Astrology (Iatromathematics & Culpeper Traditions)**:
  - Tropical (Sayana) zodiac conversion from Sidereal ephemeris.
  - Galenic-Hippocratic Four Humors (Choleric, Sanguine, Melancholic, Phlegmatic) & primary qualities (Hot/Cold, Moist/Dry).
  - Homo Signorum (Zodiacal Man: Head-to-toe organ rulership in Tropical framework).
  - Decumbiture Ptolemaic aspects (conjunctions, squares, oppositions, trines).
  - Nicholas Culpeper's Herbal Pharmacopeia (Cures by Sympathy and Antipathy).
- **VedAstro Integration**: Full integration with the `vedastro` Python library for Sarvashtakavarga (SAV/BAV), Panchanga tables, Shadbala, and cross-verification.
- **Vedic & KP Astrology**: Precise planetary calculations, Vimshottari dasha, houses, aspects, and cuspal engines.
- **Lal Kitab & Remedial Systems**: Varshaphala, debt analysis, and customized remedial measures.
- **Numerology & Name Tuning**: Commercial name vibration analysis, Chaldean & Pythagorean harmony.
- **Dossier & Report Generation**: Automated HTML and PDF consultation dossier generation.
- **QA Consultation Web Application**: Interactive questionnaire and recommendation console.

## Installation & Setup
```bash
pip install -r requirements.txt
```

## Run Main Astrological & Medical Profile
```bash
python app/main.py
```

## Run Unit Tests
```bash
python -m unittest discover -s tests
```

## Branches
- `main`: Production and release branch.
- `tejravi`: Development and feature branch.
