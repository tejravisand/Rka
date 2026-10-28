# Rka - Astrological Consultation & Analysis Engine

An advanced astrological computational engine and consultation platform supporting Parashara, Jaimini, KP, Lal Kitab, Numerology, VedAstro, Skyfield (NASA JPL Astronomy), Vedic Medical Astrology, Western Iatromathematics, Ashtakoota Guna Milan, and multi-method astrological dossiers.

## Advanced Astrological Python Capabilities Available

### 1. High-Precision Ephemeris & Astronomy
- **Skyfield (NASA/JPL DE Ephemeris)**: Precision celestial mechanics, topocentric observer coordinates, Greenwich Apparent Sidereal Time (GAST), Local Apparent Sidereal Time (LAST), solar noon, equation of time, solar declination, lunar illumination percentage, and lunar phase angles.
- **Pure-Python Astronomical Engine**: High-precision VSOP-compatible planetary longitudes, Lahiri Ayanamsa, and Ascendant calculation with zero external C/C++ compiler dependencies.
- **VedAstro Integration**: Official Python `vedastro` library integration for Sarvashtakavarga (SAV/BAV), Panchanga verification, and cloud-backed Shadbala calculations.

### 2. Jaimini Astrology Engine (`app/engines/jaimini_engine.py`)
- **7 & 8 Chara Karakas**: Atmakaraka (AK), Amatyakaraka (AmK), Bhratrikaraka (BK), Matrikaraka (MK), Putrakaraka (PK), Gnatikaraka (GK), and Darakaraka (DK) with AK-AmK Raja Yoga detection.
- **12 Arudha Padas**: Full calculation from Arudha Lagna (AL) and Upapada Lagna (UL / A12) to Rajya Pada (A10) and Dhana Pada (A2) incorporating classical Jaimini 10th-house and 4th-house exception rules.
- **Jaimini Rashi Drishti (Sign Aspects)**: Movable aspects Fixed (except adjacent), Fixed aspects Movable (except adjacent), and Dual signs aspecting each other.
- **Karakamsha & Swamsha**: Navamsha D9 sign placement of Atmakaraka, 12th from Karakamsha analysis, and Ishta Devata determination.
- **Chara Dasha Engine**: Savya (Direct) and Apasavya (Reverse) sign dasha progressions and durations.
- **Argala & Virodhargala**: Primary (2nd, 4th, 11th) and secondary (5th) intervention vs obstruction analysis.

### 3. Complete Parashari Ashtakavarga Engine (`app/engines/ashtakavarga_engine.py`)
- **Bhinna Ashtakavarga (BAV)**: Exact BPHS rules for Sun (48), Moon (49), Mars (39), Mercury (54), Jupiter (56), Venus (52), and Saturn (39) bindus across all 12 signs.
- **Sarvashtakavarga (SAV)**: Aggregated 337 total bindus across 12 houses with strength classification and financial flow ratio (10th vs 11th vs 12th).
- **Trikona Shodhana**: Triplicity reduction (Fire, Earth, Air, Water).
- **Ekadhipatya Shodhana**: Dual lordship reduction across shared planetary ownership.
- **Shodhita Pindas**: Classical Rashi Pinda, Graha Pinda, and Yoga Pinda calculations.
- **Kakshya Micro-Timing**: 8 sub-divisions of 3°45' per sign (Saturn to Lagna) for micro-transit analysis.

### 4. Six-Fold Shadbala Engine (`app/engines/shadbala_engine.py`)
- **Sthana Bala (Positional)**: Uccha Bala (0-60 Virupas), Saptavargaja Bala (across 7 vargas), Ojhayugmarashi Bala, Kendra Bala, and Drekana Bala.
- **Dig Bala (Directional)**: Exact Virupas based on angular distance from directional power cusps (1st, 4th, 7th, 10th).
- **Kaala Bala (Temporal)**: Natonnata Bala (diurnal/nocturnal), Paksha Bala (waxing/waning), Tribhaga, and Ayana Bala.
- **Cheshta Bala (Motional)**: Retrogradation (Vakra) and orbital velocity strength.
- **Naisargika Bala (Natural)**: Inherent luminosity Virupas (Sun to Saturn).
- **Drik Bala (Aspectual)**: Benefic drishti additions and malefic subtractions.
- **Total Virupas & Rupas**: Evaluated against classical minimum requirements (Sun: 6.5R, Moon: 6.0R, Mars: 5.0R, Mercury: 7.0R, Jupiter: 6.5R, Venus: 5.5R, Saturn: 5.0R), strength ratios, rankings, and Ishta/Kashta Phala.

### 5. Ashtakoota & Dashakoota Guna Milan Engine (`app/engines/guna_milan_engine.py`)
- **36-Point Classical Guna Milan**:
  - Varna Kuta (1 pt - Spiritual & ego harmony)
  - Vashya Kuta (2 pts - Mutual magnetism & instinctual rapport)
  - Tara Kuta (3 pts - Destiny, health & fortune)
  - Yoni Kuta (4 pts - Biological & sexual compatibility with 14 animal totems and sworn-enemy checks)
  - Graha Maitri Kuta (5 pts - Psychological & mental friendship)
  - Gana Kuta (6 pts - Temperament: Deva, Manushya, Rakshasa)
  - Bhakoot Kuta (7 pts - Emotional bonding & wealth with classical 2/12, 6/8, 5/9 dosha cancellations)
  - Nadi Kuta (8 pts - Genetic & bio-energy health: Adi, Madhya, Antya with classical cancellations)
- **Dashakoota Extras**: Mahendra, Stree Deergha, Rajju, and Vedha.
- **Manglik / Kuja Dosha**: Multi-perspective evaluation (Lagna, Moon, Venus) with mutual cancellation rules.

### 6. Precision Panchanga & Muhurtha Engine (`app/engines/panchanga_engine.py`)
- **Five Limbs of Time**: Tithi (with percentage and deity), Vara (weekday lord), Nakshatra (pada and lord), Yoga (27 solar-lunar sum yogas), and Karana (4 fixed + 7 repeating chara with Vishti/Bhadra alerts).
- **Auspicious & Inauspicious Muhurthas**: Rahu Kaalam, Yamaganda, Gulika Kaalam, Abhijit Muhurtha, and Brahma Muhurtha calculations.

### 7. Integrative East-West Medical Astrology
- Cross-system clinical synthesis combining Vedic Ayur-Jyotisha (Tridosha, Sapta Dhatu, Kaala Purusha, D30 Arishta) with Nicholas Culpeper's Western Medical Astrology (Galenic-Hippocratic 4 humors, Decumbiture Ptolemaic aspects, cures by sympathy/antipathy).

### 8. Unified Master Gateway (`app/engines/advanced_astrology_hub.py`)
- One-call master API aggregating all engines into a single structured consultation dossier.

---

## Installation & Setup

```bash
pip install -r requirements.txt
```

## Running the Engines

### 1. Run Advanced Astrological Python Showcase
```bash
python generate_advanced_astrology_dossier.py
```

### 2. Run Main Natal & Medical Profile
```bash
python app/main.py
```

### 3. Run Unit Tests (56 Automated Tests)
```bash
python -m unittest discover -s tests
```

---

## Installed Python Astrological Libraries Status
- **VedAstro (`vedastro>=1.23.30`)**: Active
- **Skyfield (`skyfield>=1.50.0`)**: Active
- **NumPy (`numpy>=1.24.0`)**: Active
- **ReportLab (`reportlab>=4.0.0`)**: Active
- **Pure-Python BPHS Native Suite**: Active
