import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# --- Physical Constants ---
h_bar = 1.054571817e-34  # Planck constant (J*s)
k_B = 1.380649e-23    # Boltzmann constant (J/K)
m_p = 1.67262192e-27    # Proton mass (kg)
eV_to_J = 1.60218e-19 # Conversion factor from electron-volts to Joules

# --- Simulation Parameters for this version ---
FIXED_TEMPERATURE_K = 310.0  # Body temperature (K)
proton_well_width_A = 0.5  # Approx. width of proton confinement well in Angstroms
proton_well_width = proton_well_width_A * 1e-10 # Convert to meters

# Barrier height (can be kept as in original or adjusted if needed)
V0_eV = 0.3
V0 = V0_eV * eV_to_J  # Barrier height (Joules)

# Barrier width (L_barrier_A) will be varied - this is our "System Size" proxy
L_barrier_A_min = 0.1  # Min barrier width in Angstroms
L_barrier_A_max = 1.0  # Max barrier width in Angstroms
L_barrier_A_steps = 50 # Number of steps

# Output directory for the current agent
OUTPUT_DIR = "integration/20250531-173500-BoundarySim/analysis/"
# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


# --- Proton Ground State Energy Calculation ---
def calculate_proton_energy(mass, well_width):
    if well_width <= 0:
        raise ValueError("Well width must be positive.")
    return (h_bar**2 * np.pi**2) / (2 * mass * well_width**2)

# --- WKB Tunneling Probability Function ---
def P_tunneling(E_particle, V0_barrier, L_width_barrier_m, mass):
    if E_particle >= V0_barrier:
        return 1.0
    E_for_WKB = min(E_particle, V0_barrier * 0.9999)
    potential_difference = V0_barrier - E_for_WKB
    if potential_difference <= 0:
        return 1.0
    exponent = -2 * (L_width_barrier_m / h_bar) * np.sqrt(2 * mass * potential_difference)
    return np.exp(exponent)

# --- Classical Activation Probability Function ---
def P_classical(T, V0_barrier):
    if T <= 0:
        return 0.0
    exponent = -V0_barrier / (k_B * T)
    return np.exp(exponent)

# --- Main Simulation Loop ---
def run_simulation():
    barrier_widths_A = np.linspace(L_barrier_A_min, L_barrier_A_max, L_barrier_A_steps)
    barrier_widths_m = barrier_widths_A * 1e-10

    E_proton = calculate_proton_energy(m_p, proton_well_width)
    E_proton_eV = E_proton / eV_to_J

    # Calculate Classical Probability (constant for fixed temperature)
    pc_classical = P_classical(FIXED_TEMPERATURE_K, V0)

    results_barrier_widths_A = []
    results_pt_tunnel_list = []
    results_pc_classical_list = [] # Will be constant
    results_ratio_list = []

    print("--- Initial Parameters ---")
    print(f"Fixed Temperature: {FIXED_TEMPERATURE_K} K")
    print(f"Proton Confinement Well Width: {proton_well_width_A} Angstroms ({proton_well_width:.2e} m)")
    print(f"Proton Ground State Energy (E_proton): {E_proton:.3e} J ({E_proton_eV:.3f} eV)")
    print(f"Potential Barrier Height (V0): {V0:.3e} J ({V0_eV:.3f} eV)")
    print(f"Classical Activation Probability P_classical({FIXED_TEMPERATURE_K}K): {pc_classical:.3e}")
    print("-" * 70)
    print("--- Barrier Width Dependent Probabilities & Ratio ---")
    header = f"{'L_barrier (A)':<15} | {'P_tunnel':<12} | {'P_classical':<15} | {'Advantage (Pt/Pc)':<20}"
    print(header)
    print("-" * len(header))

    for L_A, L_m in zip(barrier_widths_A, barrier_widths_m):
        pt_tunnel = P_tunneling(E_proton, V0, L_m, m_p)
        ratio_pt_pc = pt_tunnel / pc_classical if pc_classical > 1e-200 else float('inf') # Avoid division by zero if Pc is extremely small

        results_barrier_widths_A.append(L_A)
        results_pt_tunnel_list.append(pt_tunnel)
        results_pc_classical_list.append(pc_classical)
        results_ratio_list.append(ratio_pt_pc)

        print(f"{L_A:<15.2f} | {pt_tunnel:<12.3e} | {pc_classical:<15.3e} | {ratio_pt_pc:<20.3e}")

    print("-" * len(header))
    print("Simulation finished.")

    # Create DataFrame
    results_df = pd.DataFrame({
        "Barrier_Width_A": results_barrier_widths_A,
        "P_tunneling": results_pt_tunnel_list,
        "P_classical_fixed_T": results_pc_classical_list,
        "Quantum_Advantage_Ratio": results_ratio_list
    })

    # Save results to CSV
    csv_filename = os.path.join(OUTPUT_DIR, f"system_size_vs_quantum_advantage_T{FIXED_TEMPERATURE_K:.0f}K.csv")
    results_df.to_csv(csv_filename, index=False)
    print(f"Results saved to {csv_filename}")

    # Generate and save plot
    plot_filename = os.path.join(OUTPUT_DIR, f"plot_system_size_vs_quantum_advantage_T{FIXED_TEMPERATURE_K:.0f}K.png")
    plt.figure(figsize=(10, 6))
    plt.plot(results_df["Barrier_Width_A"], results_df["Quantum_Advantage_Ratio"], marker='o', linestyle='-')

    plt.xlabel("Barrier Width (Angstrom) [System Size Proxy]")
    plt.ylabel("Quantum Advantage (P_tunnel / P_classical)")
    plt.yscale('log')
    plt.title(f"System Size (Barrier Width) vs. Quantum Advantage in DNA Tunneling\n(Fixed T = {FIXED_TEMPERATURE_K}K, V0 = {V0_eV}eV, Well Width = {proton_well_width_A}A)")
    plt.grid(True, which="both", ls="-", alpha=0.5)

    plt.savefig(plot_filename)
    print(f"Plot saved to {plot_filename}")
    plt.close()

    # Identify a "cliff edge" - e.g., where quantum advantage drops below 10 (tunneling is 10x classical)
    cliff_threshold_advantage = 10.0 # Example, can be adjusted
    cliff_point = results_df[results_df["Quantum_Advantage_Ratio"] < cliff_threshold_advantage]

    if not cliff_point.empty:
        cliff_width = cliff_point["Barrier_Width_A"].iloc[0]
        cliff_advantage = cliff_point["Quantum_Advantage_Ratio"].iloc[0]
        print(f"Cliff Edge Analysis (Advantage Threshold: < {cliff_threshold_advantage:.1f}):")
        print(f"  Quantum advantage drops below threshold at approx. Barrier Width {cliff_width:.2f} A (Advantage: {cliff_advantage:.2e})")
    else:
        print(f"Cliff Edge Analysis (Advantage Threshold: < {cliff_threshold_advantage:.1f}):")
        print(f"  Quantum advantage did not drop below the threshold in the simulated range.")


if __name__ == "__main__":
    run_simulation()
    print("Script phase2_dna_size_advantage_sim.py executed successfully.")
