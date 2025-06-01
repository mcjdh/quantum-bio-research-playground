import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Define physical constants
hbar = 1.054571817e-34  # J*s
k_B = 1.380649e-23    # J/K

# Placeholder function for decoherence time calculation
def calculate_decoherence_time(temperature, molecular_size_param, environment_coupling_strength, protection_strategy="None"):
    if temperature <= 0: return float('inf')
    if molecular_size_param <= 0 or environment_coupling_strength <= 0: return float('inf')

    base_decoherence_rate = temperature * molecular_size_param * environment_coupling_strength

    if protection_strategy == "Vibrational Assistance":
        if base_decoherence_rate == 0: return float('inf')
        return 1.5 / base_decoherence_rate
    elif protection_strategy == "Topology Optimization":
        effective_coupling = environment_coupling_strength * 0.7
        if effective_coupling <=0 : return float('inf')
        return 1.0 / (temperature * molecular_size_param * effective_coupling)
    elif protection_strategy == "Correlation with Environment":
        if temperature <= 0: return float('inf')
        if molecular_size_param == 0 or environment_coupling_strength == 0: return float('inf')
        return 1.0 / (temperature**0.5 * molecular_size_param * environment_coupling_strength)
    elif protection_strategy == "Decoherence-Free Subspaces":
        effective_coupling = environment_coupling_strength * 0.15
        if effective_coupling <= 0: return float('inf')
        if temperature == 0 or molecular_size_param == 0: return float('inf')
        return 1.0 / (temperature * molecular_size_param * effective_coupling)
    elif protection_strategy == "Quantum Zeno Effect":
        if base_decoherence_rate == 0: return float('inf')
        return 2.0 / base_decoherence_rate
    elif protection_strategy == "None":
        if base_decoherence_rate == 0: return float('inf')
        return 1.0 / base_decoherence_rate
    else:
        print(f"Warning: Unknown protection strategy '{protection_strategy}'. Applying no protection.")
        if base_decoherence_rate == 0: return float('inf')
        return 1.0 / base_decoherence_rate

# Define parameter ranges
temperatures_k = np.linspace(270, 370, 50)  # Kelvin, 50 points for a smoother curve

# Fixed parameters for this specific phase diagram
# Let's choose a mid-range molecular size and a common environment
FIXED_MOLECULAR_SIZE = 100  # Example: molecular_sizes = np.logspace(1, 4, 10) -> pick one
FIXED_ENV_NAME = "water"
FIXED_ENV_COUPLING = 1.0 # environments = {"water": 1.0, "lipid_membrane": 0.5, "protein_pocket": 0.1}
FIXED_PROTECTION_STRATEGY = "None"

# Output directory for the current agent
OUTPUT_DIR = "integration/20250531-173500-BoundarySim/analysis/"

def main():
    print(f"Generating Temperature vs. Coherence Time plot for:")
    print(f"  Molecular Size: {FIXED_MOLECULAR_SIZE}")
    print(f"  Environment: {FIXED_ENV_NAME} (Coupling: {FIXED_ENV_COUPLING})")
    print(f"  Protection Strategy: {FIXED_PROTECTION_STRATEGY}")

    coherence_times_s = []
    for temp_k in temperatures_k:
        decoherence_time = calculate_decoherence_time(temp_k, FIXED_MOLECULAR_SIZE, FIXED_ENV_COUPLING, FIXED_PROTECTION_STRATEGY)
        coherence_times_s.append(decoherence_time)

    # Create DataFrame for easy viewing and potential CSV export
    results_df = pd.DataFrame({
        "Temperature_K": temperatures_k,
        "Coherence_Time_s": coherence_times_s
    })

    print("\nResults Data:")
    print(results_df)

    # Save data to CSV
    csv_filename = f"{OUTPUT_DIR}temp_vs_coherence_data_{FIXED_ENV_NAME}_{FIXED_PROTECTION_STRATEGY}.csv"
    results_df.to_csv(csv_filename, index=False)
    print(f"Saved data to {csv_filename}")

    # Generate line plot
    plt.figure(figsize=(10, 6))
    plt.plot(results_df["Temperature_K"], results_df["Coherence_Time_s"], marker='o', linestyle='-')

    plt.xlabel("Temperature (K)")
    plt.ylabel("Coherence Time (s)")
    plt.title(f"Temperature vs. Coherence Time\nSize: {FIXED_MOLECULAR_SIZE}, Env: {FIXED_ENV_NAME}, Protection: {FIXED_PROTECTION_STRATEGY}")
    plt.yscale('log') # Coherence times can vary widely
    plt.grid(True, which="both", ls="-")

    plot_filename = f"{OUTPUT_DIR}plot_temp_vs_coherence_{FIXED_ENV_NAME}_{FIXED_PROTECTION_STRATEGY}.png"
    plt.savefig(plot_filename)
    print(f"Saved plot to {plot_filename}")
    plt.close()

    # Identify a "cliff edge" - e.g., where coherence time drops below 1 picosecond (1e-12 s)
    # This is an example threshold.
    cliff_threshold_s = 1e-12
    cliff_point = results_df[results_df["Coherence_Time_s"] < cliff_threshold_s]

    if not cliff_point.empty:
        cliff_temp = cliff_point["Temperature_K"].iloc[0]
        cliff_time = cliff_point["Coherence_Time_s"].iloc[0]
        print(f"\nCliff Edge Analysis (Threshold: {cliff_threshold_s:.1e} s):")
        print(f"  Coherence time drops below threshold at approx. {cliff_temp:.2f} K (Time: {cliff_time:.2e} s)")
        # This information will be used for findings.json
    else:
        print(f"\nCliff Edge Analysis (Threshold: {cliff_threshold_s:.1e} s):")
        print(f"  Coherence time did not drop below the threshold in the simulated range.")

if __name__ == "__main__":
    main()
    print("\nScript execution completed.")
