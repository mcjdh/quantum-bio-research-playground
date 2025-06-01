import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define physical constants
hbar = 1.054571817e-34  # J*s
k_B = 1.380649e-23    # J/K

# Placeholder function for decoherence time calculation
def calculate_decoherence_time(temperature, molecular_size_param, environment_coupling_strength):
    """
    Calculates a simplified decoherence time.
    This is a placeholder and will be refined.
    """
    if temperature <= 0 or molecular_size_param <= 0 or environment_coupling_strength <= 0:
        return float('inf') # Avoid division by zero or negative values, return infinity
    return 1.0 / (temperature * molecular_size_param * environment_coupling_strength)

# Define parameter ranges
temperatures = np.linspace(270, 370, 10)  # Kelvin
molecular_sizes = np.logspace(1, 4, 10)  # Generic molecular size parameter
environments = {
    "water": 1.0,
    "lipid_membrane": 0.5,
    "protein_pocket": 0.1
}  # Placeholder environment coupling strengths

def main():
    """
    Main function to run the simulation.
    """
    results_data = {} # Store data for heatmaps
    print("Starting decoherence simulation...")

    for env_name, env_coupling_strength in environments.items():
        print(f"\nSimulating environment: {env_name} (Coupling: {env_coupling_strength})")
        # Initialize a 2D array for storing results for this environment
        # Rows: molecular_sizes, Columns: temperatures
        env_results_array = np.zeros((len(molecular_sizes), len(temperatures)))

        for j, temp in enumerate(temperatures):
            for i, size_param in enumerate(molecular_sizes):
                decoherence_time = calculate_decoherence_time(temp, size_param, env_coupling_strength)
                env_results_array[i, j] = decoherence_time
                # Optional: print individual results for debugging
                # print(f"  Temp: {temp:.2f} K, Size: {size_param:.2e}, Decoherence Time: {decoherence_time:.2e} s")
        results_data[env_name] = env_results_array

    print("\nSimulation completed.")

    # Generate and save heatmaps
    output_dir = "integration/20240724-100000-Jules/analysis/" # Save in the same directory as the script

    for env_name, data_array in results_data.items():
        plt.figure(figsize=(10, 8))
        sns.heatmap(data_array,
                    xticklabels=[f"{t:.0f}" for t in temperatures],
                    yticklabels=[f"{s:.1e}" for s in molecular_sizes],
                    annot=False, # Could be True for smaller matrices
                    fmt=".2e",
                    cmap="viridis",
                    cbar_kws={'label': 'Decoherence Time (arbitrary units)'})
        plt.xlabel("Temperature (K)")
        plt.ylabel("Molecular Size Parameter")
        plt.title(f"Decoherence Time vs. Temperature and Molecular Size\n(Environment: {env_name})")
        plt.gca().invert_yaxis() # To have smaller molecular sizes at the bottom

        plot_filename = f"{output_dir}heatmap_{env_name.replace(' ', '_')}.png"
        try:
            plt.savefig(plot_filename)
            print(f"Saved heatmap to {plot_filename}")
        except Exception as e:
            print(f"Error saving plot {plot_filename}: {e}")
        plt.close() # Close the figure to free memory

    return results_data # Return the structured data

if __name__ == "__main__":
    simulation_results = main()
    print("\nHeatmap generation process completed.")
    # simulation_results now contains the 2D arrays directly

print("Script updated for heatmap generation and ready for execution.")
