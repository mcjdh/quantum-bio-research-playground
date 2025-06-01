import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define physical constants
hbar = 1.054571817e-34  # J*s
k_B = 1.380649e-23    # J/K

# Placeholder function for decoherence time calculation
def calculate_decoherence_time(temperature, molecular_size_param, environment_coupling_strength, protection_strategy="None"):
    """
    Calculates a simplified decoherence time, incorporating protection strategies.

    Protection Strategies:
    - "None": No protection.
    - "Vibrational Assistance": Enhances coherence by a factor (e.g., 1.5x).
    - "Topology Optimization": Reduces environment coupling strength (e.g., by 30%).
    - "Correlation with Environment": Modifies temperature dependency (e.g., 1/T^0.5).
    - "Decoherence-Free Subspaces (DFS)": Significantly reduces coupling (e.g., by 85%).
    - "Quantum Zeno Effect": Enhances coherence time by a factor (e.g., 2x), simulating suppression of decoherence pathways.
    """
    if temperature <= 0: # Prevent division by zero for temperature
        # For non-positive temperatures, decoherence is often considered infinite or undefined
        # depending on the model. Here, we return infinity.
        return float('inf')
    if molecular_size_param <= 0 or environment_coupling_strength <= 0:
        # Similar handling for non-positive size or coupling, though typically these are positive.
        return float('inf')

    # Base decoherence rate calculation (inverse of decoherence time)
    base_decoherence_rate = temperature * molecular_size_param * environment_coupling_strength

    # Apply protection strategy modifications
    if protection_strategy == "Vibrational Assistance":
        # Assumes vibrational assistance enhances coherence time by a factor of 1.5
        # This means the decoherence rate is reduced by this factor.
        # Decoherence Time = Original Time * 1.5 => Rate = Original Rate / 1.5
        if base_decoherence_rate == 0: return float('inf') # Avoid division by zero if rate is already zero
        return 1.5 / base_decoherence_rate
    elif protection_strategy == "Topology Optimization":
        # Assumes topology optimization reduces coupling strength by 30%
        effective_coupling = environment_coupling_strength * 0.7
        if effective_coupling <=0 : return float('inf') # Avoid issues if coupling becomes non-positive
        return 1.0 / (temperature * molecular_size_param * effective_coupling)
    elif protection_strategy == "Correlation with Environment":
        # Modifies temperature dependency from 1/T to 1/T^0.5
        # This implies the rate's dependency on T changes.
        # Original rate ~ T, New rate ~ T^0.5
        # So, new_decoherence_time = 1 / (T^0.5 * molecular_size_param * environment_coupling_strength)
        if temperature <= 0: return float('inf') # Should be caught earlier, but good practice
        # Check if molecular_size_param or environment_coupling_strength are zero to avoid division by zero
        if molecular_size_param == 0 or environment_coupling_strength == 0:
             return float('inf')
        return 1.0 / (temperature**0.5 * molecular_size_param * environment_coupling_strength)
    elif protection_strategy == "Decoherence-Free Subspaces":
        # Assumes DFS reduces effective environment coupling strength significantly (e.g., by 85%)
        effective_coupling = environment_coupling_strength * 0.15
        if effective_coupling <= 0: return float('inf')
        # Check if temperature or molecular_size_param are zero to avoid division by zero
        if temperature == 0 or molecular_size_param == 0: # temperature check is redundant here due to earlier check
            return float('inf')
        return 1.0 / (temperature * molecular_size_param * effective_coupling)
    elif protection_strategy == "Quantum Zeno Effect":
        # Assumes Quantum Zeno Effect enhances coherence time by a factor of 2.0
        # This is a simplified model; true Zeno effect is more complex and depends on measurement frequency/strength.
        if base_decoherence_rate == 0: return float('inf')
        return 2.0 / base_decoherence_rate
    elif protection_strategy == "None":
        if base_decoherence_rate == 0: return float('inf')
        return 1.0 / base_decoherence_rate
    else:
        # Default to "None" behavior if an unknown strategy is provided
        print(f"Warning: Unknown protection strategy '{protection_strategy}'. Applying no protection.")
        if base_decoherence_rate == 0: return float('inf')
        return 1.0 / base_decoherence_rate


# Define parameter ranges
temperatures = np.linspace(270, 370, 10)  # Kelvin
molecular_sizes = np.logspace(1, 4, 10)  # Generic molecular size parameter
environments = {
    "water": 1.0,
    "lipid_membrane": 0.5,
    "protein_pocket": 0.1
}  # Placeholder environment coupling strengths
protection_strategies = ["None", "Vibrational Assistance", "Topology Optimization", "Correlation with Environment", "Decoherence-Free Subspaces", "Quantum Zeno Effect"]

def main():
    """
    Main function to run the simulation.
    Iterates through environments, temperatures, molecular sizes, and protection strategies.
    """
    results_data = {} # Store data for heatmaps: results_data[strategy][env][size_idx][temp_idx]
    print("Starting decoherence simulation with protection strategies...")

    for strategy in protection_strategies:
        print(f"\nSimulating with Protection Strategy: {strategy}")
        results_data[strategy] = {}
        for env_name, env_coupling_strength in environments.items():
            print(f"  Simulating environment: {env_name} (Coupling: {env_coupling_strength})")
            # Initialize a 2D array for storing results for this environment and strategy
            env_results_array = np.zeros((len(molecular_sizes), len(temperatures)))

            for j, temp in enumerate(temperatures):
                for i, size_param in enumerate(molecular_sizes):
                    decoherence_time = calculate_decoherence_time(temp, size_param, env_coupling_strength, strategy)
                    env_results_array[i, j] = decoherence_time
                    # Optional: print individual results for debugging
                    # print(f"    Temp: {temp:.2f} K, Size: {size_param:.2e}, Strategy: {strategy}, Decoherence Time: {decoherence_time:.2e} s")
            results_data[strategy][env_name] = env_results_array

    print("\nSimulation completed.")

    # Generate and save heatmaps
    # Ensure the output directory uses the current agent's path
    output_dir = "integration/20250531-173000-ProtectSim/analysis/"

    for strategy, strategy_data in results_data.items():
        for env_name, data_array in strategy_data.items():
            plt.figure(figsize=(10, 8))
            sns.heatmap(data_array,
                        xticklabels=[f"{t:.0f}" for t in temperatures],
                        yticklabels=[f"{s:.1e}" for s in molecular_sizes],
                        annot=False,
                        fmt=".2e",
                        cmap="viridis",
                        cbar_kws={'label': 'Decoherence Time (s)'}) # Updated label
            plt.xlabel("Temperature (K)")
            plt.ylabel("Molecular Size Parameter")
            plt.title(f"Decoherence Time: {env_name}\nStrategy: {strategy}")
            plt.gca().invert_yaxis()

            # Sanitize strategy name for filename
            safe_strategy_name = strategy.replace(' ', '_').replace('.', '')
            plot_filename = f"{output_dir}heatmap_{safe_strategy_name}_{env_name.replace(' ', '_')}.png"
            try:
                plt.savefig(plot_filename)
                print(f"Saved heatmap to {plot_filename}")
            except Exception as e:
                print(f"Error saving plot {plot_filename}: {e}")
            plt.close()

    return results_data

if __name__ == "__main__":
    simulation_results = main()
    print("\nHeatmap generation process completed.")
    # simulation_results now contains the nested dictionary structure

print("Script updated for protection strategies, new models, heatmap generation, and ready for execution.")
