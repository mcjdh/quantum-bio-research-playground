# Olfaction Vibration Frequency Analysis (Agent: 20250531-172000-VibeSim)

## 🎯 Mission
This project explores the potential link between molecular vibrational frequencies and smell perception, focusing on Turin's theory of olfaction. It uses a simple harmonic oscillator (SHO) model to calculate vibrational frequencies for various odorant molecules and examines the effects of isotopic substitution (H vs. D).

## 🛠️ Methodology

1.  **Project Setup**:
    *   A dedicated directory (`olfaction/theory/20250531-172000-VibeSim/`) was created following the `ORCHESTRATION.md` guidelines.
    *   Files for documentation (`README.md`, `findings.json`, `sources.bib`, `next_questions.md`) and analysis (`analysis/`, `raw_data/`) were initialized.

2.  **Core Logic (`analysis/vibrational_olfaction.py`)**:
    *   A Python script was developed to calculate vibrational frequencies.
    *   **SHO Model**: Frequency `v = (1 / (2 * pi)) * sqrt(k / mu)`, where `k` is the bond force constant and `mu` is the reduced mass of the two atoms forming the bond.
    *   **Isotope Comparison**: The script specifically calculates and compares frequencies for bonds containing Hydrogen versus Deuterium.
    *   **Constants**: Standard atomic masses (H, D, C, O, N, S) and physical constants (AMU to kg, speed of light) are used. Frequencies are reported in Hz and cm⁻¹.

3.  **Data Compilation (`raw_data/odorant_data.csv`)**:
    *   A dataset of 50+ odorant molecule entries was compiled. Each entry includes:
        *   Molecule name
        *   Smell category
        *   A characteristic bond type (e.g., O-H, C=O, C-H)
        *   Symbols of the two atoms in the bond
        *   Typical bond strength (force constant `k` in N/m) for the bond type.
    *   This data allows for systematic calculation across a range of odorants.

4.  **Calculations and Analysis (`analysis/vibrational_olfaction.py`)**:
    *   The script reads the `odorant_data.csv`.
    *   For each molecule/bond:
        *   Calculates the reduced mass.
        *   Calculates the vibrational frequency in Hz and cm⁻¹.
        *   If the bond contains Hydrogen, it also calculates the frequency for the Deuterated equivalent and the frequency ratio (H/D).
    *   Results are printed to the console, including a preliminary grouping by smell category.

5.  **Unit Tests (`analysis/test_vibrational_olfaction.py`)**:
    *   Unit tests were written using Python's `unittest` module to verify the correctness of:
        *   Reduced mass calculation.
        *   SHO frequency calculation (including error handling for invalid inputs).
        *   Conversion from Hz to wavenumbers.
        *   Isotope effect frequency ratios.
    *   All tests passed, ensuring the reliability of the core calculations.

## 📈 Preliminary Observations (Illustrative)
(Actual detailed findings are based on script output and summarized in `findings.json`)

*   O-H bonds (e.g., in alcohols, phenols, carboxylic acids) consistently show high frequencies (~3000-3700 cm⁻¹). Deuteration (O-D) shifts these significantly to lower frequencies (~2200-2700 cm⁻¹), with H/D frequency ratios around 1.35-1.38.
*   C=O bonds (e.g., in ketones, aldehydes, esters, carboxylic acids) show strong absorptions in the ~1650-1800 cm⁻¹ range. Isotope effects here are generally not from H/D unless an alpha-hydrogen is considered, which was not the primary focus for C=O itself.
*   C-H bonds (aliphatic, aromatic, aldehyde) have frequencies in the ~2800-3100 cm⁻¹ range. Deuteration (C-D) shifts these to ~2000-2300 cm⁻¹, with H/D ratios around 1.35-1.4.
*   S-H bonds (thiols) are seen around ~2500-2600 cm⁻¹.
*   N-H bonds (amines, amides like indole) are around ~3100-3500 cm⁻¹.

Correlations between these frequencies/ratios and specific smell categories require more detailed statistical analysis beyond the scope of the current script's direct output. However, the generated data provides a foundation for such analysis. For example, molecules with strong "minty" smells (e.g., Menthol) often feature O-H bonds, while "fruity" smells (e.g., Isoamyl Acetate, Ethyl Butyrate) often feature C=O bonds. The question is whether the *specific frequency values* or *deuteration shifts* within these bond types show finer correlations.

## 📂 File Structure
```
olfaction/theory/20250531-172000-VibeSim/
├── README.md
├── findings.json
├── sources.bib
├── next_questions.md
├── analysis/
│   ├── vibrational_olfaction.py
│   └── test_vibrational_olfaction.py
└── raw_data/
    └── odorant_data.csv
```
