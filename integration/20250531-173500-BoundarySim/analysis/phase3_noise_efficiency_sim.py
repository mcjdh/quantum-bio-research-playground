import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Define physical constants
hbar = 1.054571817e-34  # J*s
k_B = 1.380649e-23    # J/K

# Placeholder function for decoherence time calculation (same as phase1)
def calculate_decoherence_time(temperature, molecular_size_param, environment_coupling_strength, protection_strategy="None"):
    # Assuming "None" protection for simplicity in this noise analysis
    # More complex: could analyze noise impact under different protection strategies
    if protection_strategy != "None":
        print(f"Warning: This simulation for noise vs efficiency uses 'None' protection strategy, ignoring '{protection_strategy}'.")

    if temperature <= 0: return float('inf')
    if molecular_size_param <= 0 or environment_coupling_strength <= 0: return float('inf') # Coupling strength as noise can't be zero or neg for this formula

    base_decoherence_rate = temperature * molecular_size_param * environment_coupling_strength

    if base_decoherence_rate == 0: return float('inf')
    return 1.0 / base_decoherence_rate

# Fixed parameters for this specific phase diagram
FIXED_TEMPERATURE_K = 310.0  # e.g., Body temperature
FIXED_MOLECULAR_SIZE = 100   # Example fixed molecular size parameter
FIXED_PROTECTION_STRATEGY = "None" # Focus on intrinsic effect of noise

# Varied parameter: Environment Coupling Strength (as Noise Level)
env_coupling_strengths = np.logspace(-2, 2, 50)  # Range from 0.01 to 100

# Output directory for the current agent
OUTPUT_DIR = "integration/20250531-173500-BoundarySim/analysis/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print(f"Generating Noise Level (Env. Coupling) vs. Efficiency (Coherence Time) plot for:")
    print(f"  Fixed Temperature: {FIXED_TEMPERATURE_K} K")
    print(f"  Fixed Molecular Size: {FIXED_MOLECULAR_SIZE}")
    print(f"  Protection Strategy: {FIXED_PROTECTION_STRATEGY}")

    coherence_times_s_as_efficiency = []
    for coupling_strength in env_coupling_strengths:
        decoherence_time = calculate_decoherence_time(
            FIXED_TEMPERATURE_K,
            FIXED_MOLECULAR_SIZE,
            coupling_strength,
            FIXED_PROTECTION_STRATEGY
        )
        coherence_times_s_as_efficiency.append(decoherence_time)

    # Create DataFrame
    results_df = pd.DataFrame({
        "Environment_Coupling_Strength_Noise": env_coupling_strengths,
        "Coherence_Time_Efficiency_s": coherence_times_s_as_efficiency
    })

    print("Results Data:")
    print(results_df)

    # Save data to CSV
    csv_filename = os.path.join(OUTPUT_DIR, f"noise_vs_efficiency_T{FIXED_TEMPERATURE_K:.0f}_Size{FIXED_MOLECULAR_SIZE}.csv")
    results_df.to_csv(csv_filename, index=False)
    print(f"Saved data to {csv_filename}")

    # Generate line plot
    plt.figure(figsize=(10, 6))
    plt.plot(results_df["Environment_Coupling_Strength_Noise"], results_df["Coherence_Time_Efficiency_s"], marker='o', linestyle='-')

    plt.xlabel("Environment Coupling Strength (Noise Level)")
    plt.ylabel("Coherence Time (Efficiency Proxy) (s)")
    plt.xscale('log')
    plt.yscale('log')
    plt.title(f"Noise Level vs. Efficiency\n(Fixed T={FIXED_TEMPERATURE_K}K, Size={FIXED_MOLECULAR_SIZE}, Protection={FIXED_PROTECTION_STRATEGY})")
    plt.grid(True, which="both", ls="-")

    plot_filename = os.path.join(OUTPUT_DIR, f"plot_noise_vs_efficiency_T{FIXED_TEMPERATURE_K:.0f}_Size{FIXED_MOLECULAR_SIZE}.png")
    plt.savefig(plot_filename)
    print(f"Saved plot to {plot_filename}")
    plt.close()

    # Identify a "cliff edge" - e.g., where efficiency drops by a factor of 100 from its max
    max_efficiency = results_df["Coherence_Time_Efficiency_s"].max()
    cliff_threshold_efficiency = max_efficiency / 100

    # Filter for points where efficiency is already below the max (to avoid issues at the start)
    # and then find the first point that drops below the threshold
    relevant_points = results_df[results_df["Coherence_Time_Efficiency_s"] < max_efficiency * 0.99] # Ensure we are past the peak
    cliff_point = relevant_points[relevant_points["Coherence_Time_Efficiency_s"] < cliff_threshold_efficiency]

    if not cliff_point.empty:
        cliff_noise_level = cliff_point["Environment_Coupling_Strength_Noise"].iloc[0]
        cliff_efficiency_val = cliff_point["Coherence_Time_Efficiency_s"].iloc[0]
        print(f"Cliff Edge Analysis (Efficiency drops to <1/100th of max):")
        print(f"  Max Efficiency (Coherence Time): {max_efficiency:.2e} s")
        print(f"  Efficiency drops below threshold ({cliff_threshold_efficiency:.2e} s) at approx. Noise Level (Coupling Strength) {cliff_noise_level:.2e}")
    else:
        print(f"Cliff Edge Analysis (Efficiency drops to <1/100th of max):")
        print(f"  Max Efficiency (Coherence Time): {max_efficiency:.2e} s")
        print(f"  Efficiency did not drop below the threshold ({cliff_threshold_efficiency:.2e} s) in the simulated range, or behavior is too flat.")

if __name__ == "__main__":
    main()
    print("Script phase3_noise_efficiency_sim.py executed successfully.")
