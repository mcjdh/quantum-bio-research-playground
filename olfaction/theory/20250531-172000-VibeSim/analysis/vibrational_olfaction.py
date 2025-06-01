import numpy as np
import csv
import os

# Physical constants
ATOMIC_MASSES_AMU = {
    'H': 1.00784,  # Mass of Hydrogen in amu
    'D': 2.01410,  # Mass of Deuterium in amu
    'C': 12.0107,  # Mass of Carbon in amu
    'O': 15.999,   # Mass of Oxygen in amu
    'N': 14.0067,  # Mass of Nitrogen in amu
    'S': 32.065    # Mass of Sulfur in amu
}
AMU_TO_KG = 1.66053906660e-27  # Conversion factor from amu to kg
SPEED_OF_LIGHT_CM_S = 2.99792458e10  # Speed of light in cm/s
H_PLANCK = 6.62607015e-34 # Planck's constant in J*s

def calculate_reduced_mass(m1_amu, m2_amu):
    """Calculates reduced mass in kg given two masses in amu."""
    # m1_kg and m2_kg are calculated inside the function if m1_amu, m2_amu are provided.
    # If m1_kg, m2_kg are directly provided, they should be used.
    # For this script, we will always call it with AMU, so conversion is internal.
    m1_kg_val = m1_amu * AMU_TO_KG
    m2_kg_val = m2_amu * AMU_TO_KG
    reduced_mass_kg = (m1_kg_val * m2_kg_val) / (m1_kg_val + m2_kg_val)
    return reduced_mass_kg

def calculate_sho_frequency_hz(reduced_mass_kg, k_Nm):
    """
    Calculates the vibrational frequency of a simple harmonic oscillator in Hz.

    Parameters:
    reduced_mass_kg (float): Reduced mass in kilograms.
    k_Nm (float): Bond strength (force constant) in N/m.

    Returns:
    float: Vibrational frequency in Hz.
    """
    if reduced_mass_kg <= 0:
        raise ValueError("Reduced mass must be positive.")
    if k_Nm < 0: # k_Nm can be 0 for non-bonded atoms, though SHO model might not apply well.
        raise ValueError("Bond strength k cannot be negative.")

    frequency_hz = (1 / (2 * np.pi)) * np.sqrt(k_Nm / reduced_mass_kg)
    return frequency_hz

def convert_hz_to_wavenumber(frequency_hz):
    """Converts frequency from Hz to wavenumbers (cm^-1)."""
    wavenumber_cm_inv = frequency_hz / SPEED_OF_LIGHT_CM_S
    return wavenumber_cm_inv

def compare_isotope_frequencies(molecule_name, bond_type, k_Nm, m1_amu, m2_amu_isotope1, m2_amu_isotope2, isotope1_label="Isotope1", isotope2_label="Isotope2"):
    """
    Calculates and prints vibrational frequencies for two isotopes of a bond.
    m1_symbol is the symbol of the common atom, m2_symbol_isotope1 and m2_symbol_isotope2 are the symbols of the isotopes.
    This function is not directly used by the new CSV processing logic in main,
    but kept for potential direct isotopic comparison utilities.
    The main logic handles H/D substitution directly.
    """

    # Isotope 1
    m1_val_amu = ATOMIC_MASSES_AMU[m1_symbol]
    m2_val_amu_isotope1 = ATOMIC_MASSES_AMU[m2_symbol_isotope1]
    reduced_mass_iso1_kg = calculate_reduced_mass(m1_val_amu, m2_val_amu_isotope1)
    freq_iso1_hz = calculate_sho_frequency_hz(reduced_mass_iso1_kg, k_Nm)
    freq_iso1_cm_inv = convert_hz_to_wavenumber(freq_iso1_hz)

    # Isotope 2
    m2_val_amu_isotope2 = ATOMIC_MASSES_AMU[m2_symbol_isotope2]
    reduced_mass_iso2_kg = calculate_reduced_mass(m1_val_amu, m2_val_amu_isotope2)
    freq_iso2_hz = calculate_sho_frequency_hz(reduced_mass_iso2_kg, k_Nm)
    freq_iso2_cm_inv = convert_hz_to_wavenumber(freq_iso2_hz)

    print(f"Frequencies for {molecule_name} ({bond_type}):")
    print(f"  {isotope1_label} ({m2_val_amu_isotope1:.3f} amu): {freq_iso1_hz:.2e} Hz ({freq_iso1_cm_inv:.2f} cm^-1)")
    print(f"  {isotope2_label} ({m2_val_amu_isotope2:.3f} amu): {freq_iso2_hz:.2e} Hz ({freq_iso2_cm_inv:.2f} cm^-1)")
    print(f"  Frequency ratio ({isotope1_label}/{isotope2_label}): {freq_iso1_hz/freq_iso2_hz:.3f}")

    return (freq_iso1_cm_inv, freq_iso2_cm_inv)

if __name__ == '__main__':
    print("Vibrational Olfaction Analysis from CSV Data")
    print("=" * 50)

    # Determine the correct path to the CSV file relative to the script's location
    # Script is in 'analysis', data is in 'raw_data'
    script_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(script_dir, '..', 'raw_data', 'odorant_data.csv')

    # Fallback if __file__ is not defined (e.g. running in some interactive environments)
    if not script_dir:
        # This assumes the script is run from the 'analysis' directory as per instructions
        csv_file_path = '../raw_data/odorant_data.csv'


    all_results = []

    try:
        with open(csv_file_path, 'r', newline='') as infile:
            reader = csv.DictReader(infile)
            for row_num, row in enumerate(reader):
                molecule_name = row['molecule_name']
                smell_category = row['smell_category']
                bond_type = row['bond_type']
                atom1_sym = row['atom1_symbol'].strip()
                atom2_sym = row['atom2_symbol'].strip()

                try:
                    bond_strength_Nm = float(row['bond_strength_Nm'])
                except ValueError:
                    print(f"Warning: Could not parse bond_strength_Nm '{row['bond_strength_Nm']}' for {molecule_name}. Skipping row.")
                    continue

                if atom1_sym not in ATOMIC_MASSES_AMU or atom2_sym not in ATOMIC_MASSES_AMU:
                    print(f"Warning: Atom symbol not found in ATOMIC_MASSES_AMU for {molecule_name} ({atom1_sym}-{atom2_sym}). Skipping.")
                    continue

                m1_amu = ATOMIC_MASSES_AMU[atom1_sym]
                m2_amu = ATOMIC_MASSES_AMU[atom2_sym]

                rm_kg = calculate_reduced_mass(m1_amu, m2_amu)
                freq_hz = calculate_sho_frequency_hz(rm_kg, bond_strength_Nm)
                freq_cm_inv = convert_hz_to_wavenumber(freq_hz)

                result_entry = {
                    "molecule": molecule_name,
                    "category": smell_category,
                    "bond": bond_type,
                    "atom1": atom1_sym,
                    "atom2": atom2_sym,
                    "k_Nm": bond_strength_Nm,
                    "original_freq_cm_inv": freq_cm_inv,
                    "deuterated_freq_cm_inv": None,
                    "ratio": None
                }

                print(f"\nMolecule: {molecule_name} ({smell_category})")
                print(f"  Bond: {bond_type} ({atom1_sym}-{atom2_sym}), k = {bond_strength_Nm} N/m")
                print(f"  Calculated Frequency: {freq_hz:.2e} Hz ({freq_cm_inv:.2f} cm^-1)")

                # Isotopic substitution if one atom is Hydrogen
                deuterated_atom_sym = None
                original_partner_atom_amu = None
                original_H_atom_amu = None

                if atom1_sym == 'H' and atom2_sym != 'D': # Ensure we are not trying to deuterate Deuterium itself if D is atom1
                    deuterated_atom_sym = atom2_sym
                    original_partner_atom_amu = m2_amu
                    original_H_atom_amu = m1_amu
                elif atom2_sym == 'H' and atom1_sym != 'D':
                    deuterated_atom_sym = atom1_sym
                    original_partner_atom_amu = m1_amu
                    original_H_atom_amu = m2_amu

                if deuterated_atom_sym:
                    m_D_amu = ATOMIC_MASSES_AMU['D']

                    # Calculate frequency for deuterated bond
                    # One atom is Deuterium, the other is `deuterated_atom_sym`
                    rm_D_kg = calculate_reduced_mass(original_partner_atom_amu, m_D_amu)
                    freq_D_hz = calculate_sho_frequency_hz(rm_D_kg, bond_strength_Nm)
                    freq_D_cm_inv = convert_hz_to_wavenumber(freq_D_hz)

                    ratio = freq_hz / freq_D_hz if freq_D_hz != 0 else 0

                    result_entry["deuterated_freq_cm_inv"] = freq_D_cm_inv
                    result_entry["ratio"] = ratio

                    original_bond_label = f"{deuterated_atom_sym}-H"
                    deuterated_bond_label = f"{deuterated_atom_sym}-D"

                    print(f"  Isotopic Comparison ({original_bond_label} vs {deuterated_bond_label}):")
                    print(f"    {original_bond_label}: {freq_cm_inv:.2f} cm^-1")
                    print(f"    {deuterated_bond_label}: {freq_D_cm_inv:.2f} cm^-1")
                    print(f"    Frequency Ratio ({original_bond_label}/{deuterated_bond_label}): {ratio:.3f}")

                all_results.append(result_entry)

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        print("Please ensure the path is correct and the script is run from the 'analysis' directory.")
        # Exit if file not found, as no analysis can be done.
        exit()
    except Exception as e:
        print(f"An error occurred during CSV processing: {e}")
        exit()

    print("\n\n" + "=" * 50)
    print("Simple Analysis: Frequencies by Smell Category")
    print("=" * 50)

    unique_categories = sorted(list(set(r['category'] for r in all_results)))

    for category in unique_categories:
        print(f"\nCategory: {category}")
        category_results = [r for r in all_results if r['category'] == category]
        if not category_results:
            print("  No data for this category.")
            continue

        for res in category_results:
            output_str = f"  - {res['molecule']} ({res['bond']}): {res['original_freq_cm_inv']:.2f} cm^-1"
            if res['deuterated_freq_cm_inv'] is not None:
                output_str += f" (D-substituted: {res['deuterated_freq_cm_inv']:.2f} cm^-1, Ratio: {res['ratio']:.3f})"
            print(output_str)

    print("\n" + "=" * 50)
    print("End of Analysis")
