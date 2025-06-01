import math
from .constants import HBAR, ANGSTROM_TO_METER, EV_TO_JOULE

def calculate_tunneling_probability(barrier_width_A, barrier_height_eV, particle_mass_kg, particle_energy_eV=0.1):
    """
    Calculates the tunneling probability for a particle across a potential barrier.

    Args:
        barrier_width_A (float): Barrier width in Angstroms.
        barrier_height_eV (float): Barrier height in electronvolts (eV).
        particle_mass_kg (float): Mass of the particle in kilograms.
        particle_energy_eV (float, optional): Energy of the particle in eV. Defaults to 0.1 eV.

    Returns:
        float: Tunneling probability (between 0 and 1), or 0.0 if V <= E.
    """
    # Convert inputs to SI units
    L_m = barrier_width_A * ANGSTROM_TO_METER
    V_J = barrier_height_eV * EV_TO_JOULE
    E_J = particle_energy_eV * EV_TO_JOULE

    if V_J <= E_J: # Classically, particle would pass over the barrier
        # For this simplified model, if E >= V, tunneling isn't the primary mechanism.
        # Return 1.0 to indicate it passes, though this isn't "tunneling".
        # A more nuanced model might return a very small number or handle differently.
        # However, the problem asks for tunneling *rates*, implying E < V.
        # If we are only interested in tunneling, and classical is 1, then T should be < 1
        # For E >= V, classical probability is 1. We are looking for quantum > 10x classical.
        # So, if E>=V, tunneling probability is not what we are interested in.
        # Let's return a very small number to ensure it doesn't dominate.
        # Or, more simply, the formula for k becomes problematic (sqrt of negative).
        # For E < V, (V-E) is positive.
        return 0.0 # Or handle as an error / specific case if V_J <= E_J

    # Calculate k (wave number inside the barrier)
    # k = sqrt(2 * m * (V - E)) / hbar
    try:
        k = math.sqrt(2 * particle_mass_kg * (V_J - E_J)) / HBAR
    except ValueError: # Should not happen if V_J > E_J
        return 0.0

    # Calculate tunneling probability
    # T = exp(-2 * k * L)
    try:
        tunneling_prob = math.exp(-2 * k * L_m)
    except OverflowError: # Result too large to represent as float (i.e., exp(very large negative) -> 0)
        tunneling_prob = 0.0

    return tunneling_prob

if __name__ == '__main__':
    from .constants import ELECTRON_MASS, PROTON_MASS
    # Test case 1: Electron
    width_A = 1.0  # Angstroms
    height_eV = 1.0 # eV
    energy_eV = 0.1 # eV
    prob_electron = calculate_tunneling_probability(width_A, height_eV, ELECTRON_MASS, energy_eV)
    print(f"Tunneling probability for electron (L={width_A} A, V={height_eV} eV, E={energy_eV} eV): {prob_electron:.4e}")

    # Test case 2: Proton, wider/higher barrier
    width_A_p = 2.0  # Angstroms
    height_eV_p = 2.0 # eV
    prob_proton = calculate_tunneling_probability(width_A_p, height_eV_p, PROTON_MASS, energy_eV)
    print(f"Tunneling probability for proton (L={width_A_p} A, V={height_eV_p} eV, E={energy_eV} eV): {prob_proton:.4e}")

    # Test case 3: V <= E
    prob_classical_pass = calculate_tunneling_probability(1.0, 0.05, ELECTRON_MASS, 0.1)
    print(f"Tunneling probability for electron (V < E): {prob_classical_pass:.4e}")
