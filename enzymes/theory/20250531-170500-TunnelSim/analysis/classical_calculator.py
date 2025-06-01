from .constants import EV_TO_JOULE # Though not strictly needed for direct eV comparison

def calculate_classical_probability(barrier_height_eV, particle_energy_eV=0.1):
    """
    Calculates the classical probability of a particle surmounting a potential barrier.

    Args:
        barrier_height_eV (float): Barrier height in electronvolts (eV).
        particle_energy_eV (float, optional): Energy of the particle in eV. Defaults to 0.1 eV.

    Returns:
        float: Classical probability (0.0 or 1.0).
    """
    if particle_energy_eV >= barrier_height_eV:
        return 1.0
    else:
        return 0.0

if __name__ == '__main__':
    # Test case 1: E < V (Classical probability should be 0)
    prob1 = calculate_classical_probability(barrier_height_eV=1.0, particle_energy_eV=0.1)
    print(f"Classical probability (E=0.1eV, V=1.0eV): {prob1}")

    # Test case 2: E = V (Classical probability should be 1)
    prob2 = calculate_classical_probability(barrier_height_eV=0.1, particle_energy_eV=0.1)
    print(f"Classical probability (E=0.1eV, V=0.1eV): {prob2}")

    # Test case 3: E > V (Classical probability should be 1)
    prob3 = calculate_classical_probability(barrier_height_eV=0.05, particle_energy_eV=0.1)
    print(f"Classical probability (E=0.1eV, V=0.05eV): {prob3}")

    # Test case 4: Using default particle energy
    prob4 = calculate_classical_probability(barrier_height_eV=0.5) # E defaults to 0.1eV
    print(f"Classical probability (E=default 0.1eV, V=0.5eV): {prob4}")
