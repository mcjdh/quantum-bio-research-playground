import numpy as np
import matplotlib.pyplot as plt

# --- Physical Constants ---
h_bar = 1.054571817e-34  # Planck constant (J*s)
k_B = 1.380649e-23    # Boltzmann constant (J/K)
m_p = 1.67262192e-27    # Proton mass (kg)
eV_to_J = 1.60218e-19 # Conversion factor from electron-volts to Joules

# --- Simulation Parameters ---
# N_iterations = 10000  # Number of iterations for the simulation (REMOVED for this version)
proton_well_width_A = 0.5  # Approx. width of proton confinement well in Angstroms
proton_well_width = proton_well_width_A * 1e-10 # Convert to meters

# Temperature range
T_min = 270.0  # Minimum temperature (K)
T_max = 330.0  # Maximum temperature (K)
T_steps = 10   # Number of temperature steps

# Double-well potential parameters
V0_eV = 0.3 # Barrier height in electron-volts (Changed from 0.5)
V0 = V0_eV * eV_to_J  # Barrier height (Joules)
L_barrier_A = 0.4 # Barrier width for tunneling in Angstroms (Changed from 0.5)
L_barrier = L_barrier_A * 1e-10 # Barrier width (meters)

# --- Proton Ground State Energy Calculation ---
def calculate_proton_energy(mass, well_width):
    """
    Calculates the ground state energy of a particle in an infinite square well.
    E = (hbar^2 * pi^2) / (2 * m * a^2)

    Args:
        mass (float): Mass of the particle (kg).
        well_width (float): Width of the potential well (m).

    Returns:
        float: Ground state energy (J).
    """
    if well_width <= 0:
        raise ValueError("Well width must be positive.")
    return (h_bar**2 * np.pi**2) / (2 * mass * well_width**2)

# --- Potential Energy Function (Placeholder) ---
def potential_V(x, V0_barrier, L_width_barrier):
    """
    Placeholder for the potential energy function.
    Represents a simple square barrier.

    Args:
        x (float): Position.
        V0_barrier (float): Barrier height.
        L_width_barrier (float): Barrier width.

    Returns:
        float: Potential energy at position x.
    """
    if 0 < x < L_width_barrier: # Use L_width_barrier for consistency if this function were more complex
        return V0_barrier
    return 0.0

# --- WKB Tunneling Probability Function ---
def P_tunneling(E_particle, V0_barrier, L_width_barrier, mass):
    """
    Calculates the WKB tunneling probability.
    P_T = exp(-2 * (L_barrier / h_bar) * sqrt(2 * m * (V0_barrier - E_effective)))

    Args:
        E_particle (float): Particle's energy.
        V0_barrier (float): Barrier height.
        L_width_barrier (float): Barrier width for tunneling.
        mass (float): Mass of the particle.

    Returns:
        float: Tunneling probability.
               Returns 1.0 if E_particle >= V0_barrier (particle clears the barrier).
               Returns 0.0 if V0_barrier - E_effective <= 0 for WKB calculation after capping.
    """
    # If particle energy is at or above barrier, classical transition, not tunneling in this context.
    # WKB approximation is for E_particle < V0_barrier.
    # If E_particle >= V0_barrier, the particle can pass over the barrier.
    # We return 1.0, signifying high probability of transmission (though WKB itself doesn't strictly apply here).
    if E_particle >= V0_barrier:
        return 1.0 # Particle's energy is at or above the barrier height.

    # Cap energy for WKB formula to avoid issues if E_particle is extremely close to V0_barrier,
    # ensuring V0_barrier - E_for_WKB is positive and WKB is more applicable.
    E_for_WKB = min(E_particle, V0_barrier * 0.9999) # Adjusted cap

    potential_difference = V0_barrier - E_for_WKB # This should now be positive

    if potential_difference <= 0:
        # This case should ideally be caught by E_particle >= V0_barrier,
        # but as a safeguard for the sqrt.
        return 1.0 # Effectively, no barrier to tunnel through if E_for_WKB is that high.

    exponent = -2 * (L_width_barrier / h_bar) * np.sqrt(2 * mass * potential_difference)
    return np.exp(exponent)

# --- Classical Activation Probability Function ---
def P_classical(T, V0_barrier):
    """
    Calculates the classical activation probability (Arrhenius-like).
    P_C = exp(-V0 / (k_B * T))

    Args:
        T (float): Temperature (K).
        V0_barrier (float): Barrier height (J).

    Returns:
        float: Classical activation probability. Returns 0 if T <= 0.
    """
    if T <= 0:
        return 0.0
    exponent = -V0_barrier / (k_B * T)
    return np.exp(exponent)

# --- Main Simulation Loop ---
def run_simulation():
    """
    Main simulation loop.
    Calculates proton energy, then iterates through temperatures to compare
    P_tunneling and P_classical.
    """
    temperatures = np.linspace(T_min, T_max, T_steps)

    # Calculate proton's ground state energy in the confinement well
    E_proton = calculate_proton_energy(m_p, proton_well_width)
    E_proton_eV = E_proton / eV_to_J

    # Calculate Tunneling Probability (temperature-independent in this model)
    pt_tunnel = P_tunneling(E_proton, V0, L_barrier, m_p)

    # Lists to store data for CSV and plotting
    results_temperatures = []
    results_pt_tunnel_list = []
    results_pc_T_list = []
    results_ratio_list = []

    print("--- Initial Parameters ---")
    print(f"Proton Confinement Well Width: {proton_well_width_A} Angstroms ({proton_well_width:.2e} m)")
    print(f"Proton Ground State Energy (E_proton): {E_proton:.3e} J ({E_proton_eV:.3f} eV)")
    print(f"Potential Barrier Height (V0): {V0:.3e} J ({V0_eV:.3f} eV)")
    print(f"Potential Barrier Width (L_barrier): {L_barrier_A} Angstroms ({L_barrier:.1e} m)")
    print(f"Calculated P_tunneling (constant): {pt_tunnel:.3e}")
    print("-" * 70)
    print("--- Temperature Dependent Probabilities & Ratio ---")
    header = f"{'Temp (K)':<10} | {'P_tunnel':<12} | {'P_classical(T)':<15} | {'Ratio (Pt/Pc)':<15}"
    print(header)
    print("-" * len(header))

    for T_current in temperatures:
        pc_T = P_classical(T_current, V0)
        ratio_pt_pc = pt_tunnel / pc_T if pc_T > 0 else float('inf')

        results_temperatures.append(T_current)
        results_pt_tunnel_list.append(pt_tunnel)
        results_pc_T_list.append(pc_T)
        results_ratio_list.append(ratio_pt_pc)

        print(f"{T_current:<10.1f} | {pt_tunnel:<12.3e} | {pc_T:<15.3e} | {ratio_pt_pc:<15.3e}")

    print("-" * len(header))
    print("Simulation finished.")

    # Save results to CSV
    csv_file_path = 'dna/20250531-172500-MutationSim/analysis/simulation_results.csv'
    # Ensure directory exists (it should, as the script is in analysis/)
    # For robustness, one might add: os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    # But here we assume the 'analysis' directory is already there.

    header_csv = "Temperature_K,P_tunneling,P_classical,Ratio_Tunnel_to_Classical\n"
    with open(csv_file_path, 'w') as f:
        f.write(header_csv)
        for i in range(len(results_temperatures)):
            f.write(f"{results_temperatures[i]:.2f},{results_pt_tunnel_list[i]:.6e},{results_pc_T_list[i]:.6e},{results_ratio_list[i]:.6e}\n")
    print(f"\nResults saved to {csv_file_path}")

    # Generate and save plot
    plot_file_path = 'dna/20250531-172500-MutationSim/analysis/tunneling_vs_classical_plot.png'
    plt.figure(figsize=(10, 6))
    plt.plot(results_temperatures, results_pt_tunnel_list, label=f'P_tunneling ({pt_tunnel:.2e})', linestyle='--', marker='x')
    plt.plot(results_temperatures, results_pc_T_list, label='P_classical(T)', marker='o')

    plt.xlabel('Temperature (K)')
    plt.ylabel('Probability')
    plt.yscale('log') # Use logarithmic scale for y-axis
    plt.title('Quantum Tunneling vs. Classical Activation in DNA Mutation')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5) # Add grid for better readability

    plt.savefig(plot_file_path)
    print(f"Plot saved to {plot_file_path}")
    # plt.show() # Uncomment to display plot interactively if needed

    return temperatures, pt_tunnel, results_pc_T_list, E_proton # results_pc_T_list is all_classical_probs_T

if __name__ == "__main__":
    # Run the simulation
    sim_temperatures, const_P_tunnel, sim_classical_probs_T, E_p = run_simulation()

    # Summary print remains useful
    print(f"\nSummary (from main):")
    print(f"  Proton Energy used for Tunneling: {E_p:.3e} J ({E_p/eV_to_J:.3f} eV)")
    print(f"  Constant Tunneling Probability (P_tunnel): {const_P_tunnel:.3e}")
    print(f"  Classical Probabilities (P_classical(T)) varied from {sim_classical_probs_T[0]:.3e} at {sim_temperatures[0]:.1f}K")
    print(f"  to {sim_classical_probs_T[-1]:.3e} at {sim_temperatures[-1]:.1f}K.")

    print("\nScript dna_mutation_simulation.py executed successfully, results saved.")
