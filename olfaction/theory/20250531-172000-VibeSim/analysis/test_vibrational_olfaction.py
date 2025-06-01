import unittest
import numpy as np

# Assuming vibrational_olfaction.py is in the same directory or accessible via PYTHONPATH
# For direct execution, we might need to adjust path or run as module
from vibrational_olfaction import (
    calculate_reduced_mass,
    calculate_sho_frequency_hz,
    convert_hz_to_wavenumber,
    ATOMIC_MASSES_AMU, # For direct use of constants like AMU_TO_KG if needed by tests
    AMU_TO_KG,
    SPEED_OF_LIGHT_CM_S
)

class TestVibrationalOlfaction(unittest.TestCase):

    def test_calculate_reduced_mass(self):
        # Test C-H bond
        m_C_amu = ATOMIC_MASSES_AMU['C']
        m_H_amu = ATOMIC_MASSES_AMU['H']

        # Manual calculation for C-H
        # m_C_kg = 12.0107 * 1.66053906660e-27
        # m_H_kg = 1.00784 * 1.66053906660e-27
        # expected_rm_CH_kg = (m_C_kg * m_H_kg) / (m_C_kg + m_H_kg)
        # For simplicity, use the function's own constants for self-consistency in test value
        m_C_kg = m_C_amu * AMU_TO_KG
        m_H_kg = m_H_amu * AMU_TO_KG
        expected_rm_CH_kg = (m_C_kg * m_H_kg) / (m_C_kg + m_H_kg)

        self.assertAlmostEqual(calculate_reduced_mass(m_C_amu, m_H_amu), expected_rm_CH_kg, places=35)

        # Test O-D bond
        m_O_amu = ATOMIC_MASSES_AMU['O']
        m_D_amu = ATOMIC_MASSES_AMU['D']
        m_O_kg = m_O_amu * AMU_TO_KG
        m_D_kg = m_D_amu * AMU_TO_KG
        expected_rm_OD_kg = (m_O_kg * m_D_kg) / (m_O_kg + m_D_kg)
        self.assertAlmostEqual(calculate_reduced_mass(m_O_amu, m_D_amu), expected_rm_OD_kg, places=35)

    def test_calculate_sho_frequency_hz(self):
        # Test with known values (e.g., typical C-H stretch)
        # For C-H: reduced mass ~0.94 amu = 1.560e-27 kg
        # k_CH ~ 450 N/m
        rm_CH_kg = calculate_reduced_mass(ATOMIC_MASSES_AMU['C'], ATOMIC_MASSES_AMU['H']) # Use previously tested function
        k_CH = 450  # N/m

        # Expected: (1/(2*pi)) * sqrt(450 / 1.560e-27)
        # This will be approx 8.9e13 Hz
        expected_freq_hz = (1 / (2 * np.pi)) * np.sqrt(k_CH / rm_CH_kg)
        calculated_freq_hz = calculate_sho_frequency_hz(rm_CH_kg, k_CH)
        self.assertAlmostEqual(calculated_freq_hz, expected_freq_hz, places=10) # places depends on precision

        # Test zero bond strength
        self.assertAlmostEqual(calculate_sho_frequency_hz(rm_CH_kg, 0), 0.0)


    def test_calculate_sho_frequency_hz_error_handling(self):
        with self.assertRaises(ValueError):
            calculate_sho_frequency_hz(0, 450) # Zero reduced mass
        with self.assertRaises(ValueError):
            calculate_sho_frequency_hz(-1e-27, 450) # Negative reduced mass
        with self.assertRaises(ValueError):
            calculate_sho_frequency_hz(1e-27, -100) # Negative bond strength


    def test_convert_hz_to_wavenumber(self):
        freq_hz = 8.9e13  # Approx C-H stretch in Hz
        # Expected: 8.9e13 / 2.99792458e10 cm/s = 2968.7 cm^-1
        expected_wavenumber = freq_hz / SPEED_OF_LIGHT_CM_S
        calculated_wavenumber = convert_hz_to_wavenumber(freq_hz)
        self.assertAlmostEqual(calculated_wavenumber, expected_wavenumber, places=1) # Precision based on input

    def test_isotope_effect_ratio(self):
        # For H vs D, mass ratio is approx 1:2. Frequency ratio should be sqrt(2):1 ~ 1.414
        k_test = 500 # N/m
        m_common_amu = 12 # e.g., Carbon

        rm_XH_kg = calculate_reduced_mass(m_common_amu, ATOMIC_MASSES_AMU['H'])
        freq_XH_hz = calculate_sho_frequency_hz(rm_XH_kg, k_test)

        rm_XD_kg = calculate_reduced_mass(m_common_amu, ATOMIC_MASSES_AMU['D'])
        freq_XD_hz = calculate_sho_frequency_hz(rm_XD_kg, k_test)

        # Theoretical ratio: sqrt(rm_XD_kg / rm_XH_kg) which is also freq_XH_hz / freq_XD_hz
        # Or more simply: sqrt( (m_common*m_D)/(m_common+m_D) / (m_common*m_H)/(m_common+m_H) )
        # This should be close to sqrt( m_D / m_H ) if m_common is large, or more precisely sqrt(mu_D / mu_H)
        # where mu_D is reduced mass with D, mu_H is reduced mass with H.

        # We expect freq(X-H) / freq(X-D) to be approx. sqrt(reduced_mass(X-D) / reduced_mass(X-H))
        # This is not sqrt(m_D/m_H) directly but involves the common atom.
        # The ratio freq_XH / freq_XD is what is calculated by compare_isotope_frequencies

        # freq_XH / freq_XD = sqrt(k/rm_XH) / sqrt(k/rm_XD) = sqrt(rm_XD / rm_XH)
        expected_ratio = np.sqrt(rm_XD_kg / rm_XH_kg)

        # Check against the actual frequency ratio
        self.assertAlmostEqual(freq_XH_hz / freq_XD_hz, expected_ratio, places=5)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
