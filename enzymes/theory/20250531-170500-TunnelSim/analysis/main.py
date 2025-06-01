import numpy as np
from .constants import ELECTRON_MASS, PROTON_MASS, DEUTERON_MASS
from .tunneling_calculator import calculate_tunneling_probability
from .classical_calculator import calculate_classical_probability

def find_quantum_regimes():
    """
    Iterates through barrier parameters and particle masses to find regimes
    where quantum tunneling probability is significantly higher than classical probability.
    """
    particle_energy_eV = 0.1  # Fixed particle energy

    masses = {
        "Electron": ELECTRON_MASS,
        "Proton": PROTON_MASS,
        "Deuteron": DEUTERON_MASS
    }

    # Barrier width range: 0.5 to 5 Angstroms (steps of 0.5 A)
    barrier_widths_A = np.arange(0.5, 5.1, 0.5)

    # Barrier height range: 0.1 to 2 eV (steps of 0.1 eV)
    # Note: Particle energy is 0.1 eV.
    # Classical probability will be 1 if barrier_height_eV <= 0.1 eV, and 0 otherwise.
    barrier_heights_eV = np.arange(0.1, 2.1, 0.1)

    print(f"Particle Energy (E) = {particle_energy_eV:.2f} eV\n")
    print("Regimes where Quantum Probability (T_q) is >= 10x Classical Probability (T_c):")
    print("--------------------------------------------------------------------------------")
    print("Particle | Width (A) | Height (eV) | T_q      | T_c | Ratio (T_q/T_c)")
    print("--------------------------------------------------------------------------------")

    found_regimes = 0

    for name, mass_kg in masses.items():
        for width_A in barrier_widths_A:
            for height_eV in barrier_heights_eV:
                # Ensure height_eV is rounded to avoid floating point issues with comparisons
                height_eV_rounded = round(height_eV, 2)

                t_quantum = calculate_tunneling_probability(
                    barrier_width_A=width_A,
                    barrier_height_eV=height_eV_rounded,
                    particle_mass_kg=mass_kg,
                    particle_energy_eV=particle_energy_eV
                )

                t_classical = calculate_classical_probability(
                    barrier_height_eV=height_eV_rounded,
                    particle_energy_eV=particle_energy_eV
                )

                # Condition: T_q >= 10 * T_c
                # Handle T_c = 0 case: if T_c is 0, any T_q > 0 means quantum is infinitely greater.
                # We are looking for T_q to be "at least 10x" T_c.
                # If T_c = 1.0 (because E >= V), then T_q must be >= 10. This is impossible as T_q <= 1.
                # So, we are only interested in cases where T_c = 0.0 (i.e., E < V).
                # In this situation, any T_q > 0 would satisfy being "more" than T_c.
                # The problem asks "quantum beats classical by 10x or more".
                # If T_c = 0, and T_q > 0, then quantum has beaten classical.
                # The "10x" factor is tricky here. If T_c = 0, T_q / T_c is undefined or infinite.
                # Let's interpret "beats classical by 10x or more" as:
                # 1. If T_c > 0 (i.e. T_c = 1.0), then T_q >= 10 * T_c (impossible, as T_q <=1)
                # 2. If T_c = 0, then T_q > 0 (any non-zero tunneling in the classically forbidden region)
                #    For the "10x" part: if T_c = 0, perhaps a minimum T_q threshold? E.g. T_q >= 0.001?
                #    The problem states "Find regimes where quantum beats classical by 10x or more".
                #    If T_c = 0, classical rate is zero. Any non-zero quantum rate is infinitely larger.
                #    Let's assume this means T_c = 0 and T_q > 0.

                significant_quantum_effect = False
                ratio_str = "N/A"

                if t_classical == 0.0:
                    if t_quantum > 0: # Any quantum tunneling in classically forbidden region
                        significant_quantum_effect = True
                        ratio_str = "Inf (T_c=0)"
                # else T_classical is 1.0. For T_q >= 10 * T_c, T_q would need to be >= 10, which is not possible.
                # So we only care about the t_classical == 0.0 case.

                if significant_quantum_effect:
                    found_regimes +=1
                    print(f"{name:<8} | {width_A:<9.1f} | {height_eV_rounded:<11.2f} | {t_quantum:<8.2e} | {t_classical:<3.0f} | {ratio_str}")

    if found_regimes == 0:
        print("No regimes found where quantum probability significantly exceeds classical probability under the defined conditions (T_c=0 and T_q > 0).")
    else:
        print("--------------------------------------------------------------------------------")
        print(f"Found {found_regimes} parameter combinations meeting the criteria.")

if __name__ == '__main__':
    find_quantum_regimes()
