import numpy as np
import matplotlib.pyplot as plt

# --- Classical Sensing Limit (Standard Quantum Limit - SQL) ---
def estimate_parameter_sql(N_probes, sensitivity_per_probe=1.0):
    """
    Estimates the precision of a parameter using N independent classical probes.
    The error typically scales as 1/sqrt(N).
    This represents the Standard Quantum Limit (SQL) for uncorrelated probes.
    Returns the uncertainty (delta_phi).
    """
    if N_probes <= 0:
        return np.inf
    return sensitivity_per_probe / np.sqrt(N_probes)

# --- Quantum Sensing Limit (Heisenberg Limit - HL) ---
def estimate_parameter_heisenberg(N_probes, sensitivity_per_probe=1.0):
    """
    Estimates the precision of a parameter using N entangled quantum probes.
    The error can, in ideal cases, scale as 1/N.
    This represents the Heisenberg Limit (HL).
    Returns the uncertainty (delta_phi).
    """
    if N_probes <= 0:
        return np.inf
    return sensitivity_per_probe / N_probes

# --- Information Bandwidth Conceptualization ---
# Bandwidth can be related to how many distinct states of a parameter
# can be resolved within a given time, or the rate of information gain.
# If precision in estimating a parameter 'phi' is delta_phi,
# the number of distinguishable states in a range R is R / delta_phi.
# Information content can be log2(Number of distinguishable states).

def information_from_precision(parameter_range, precision_delta_phi):
    """
    Estimates information content based on precision.
    I = log2(Range / delta_phi)
    """
    if precision_delta_phi <= 0 or parameter_range <= 0:
        return 0
    num_distinguishable_states = parameter_range / precision_delta_phi
    if num_distinguishable_states <= 1: # Cannot distinguish more than one state means no info
        return 0
    return np.log2(num_distinguishable_states)

# --- Simplified Biological Sensor Model ---
# Let's imagine a sensor trying to detect a concentration 'c'.
# The sensor has 'N' receptor sites (probes).
# Each interaction provides some information.

# Scenario:
# Classical: Each receptor acts independently.
# Quantum: Receptors might use some form of entanglement or collective quantum effect.

def compare_sensing_limits_and_information(max_probes=100, parameter_range=1.0, sensitivity=1.0):
    """
    Compares SQL and HL, and calculates associated information.
    Generates data for plotting.
    """
    n_values = np.arange(1, max_probes + 1)

    uncertainty_sql = [estimate_parameter_sql(n, sensitivity) for n in n_values]
    uncertainty_hl = [estimate_parameter_heisenberg(n, sensitivity) for n in n_values]

    info_sql = [information_from_precision(parameter_range, delta_phi) for delta_phi in uncertainty_sql]
    info_hl = [information_from_precision(parameter_range, delta_phi) for delta_phi in uncertainty_hl]

    return n_values, uncertainty_sql, uncertainty_hl, info_sql, info_hl

def plot_sensing_comparison(n_values, uncertainty_sql, uncertainty_hl, info_sql, info_hl, filename_prefix="sensor_comparison"):
    """Plots the comparison of sensing limits and information content."""

    # Plot 1: Uncertainty vs Number of Probes
    plt.figure(figsize=(10, 5))
    plt.plot(n_values, uncertainty_sql, label='SQL (Error ~ 1/√N)', linestyle='--')
    plt.plot(n_values, uncertainty_hl, label='Heisenberg Limit (Error ~ 1/N)', linestyle='-')
    plt.xlabel('Number of Probes/Receptors (N)')
    plt.ylabel('Uncertainty (Δφ)')
    plt.title('Sensing Precision: SQL vs Heisenberg Limit')
    plt.yscale('log')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig(f"{filename_prefix}_precision.png")
    plt.close()

    # Plot 2: Information Content vs Number of Probes
    plt.figure(figsize=(10, 5))
    plt.plot(n_values, info_sql, label='Information with SQL', linestyle='--')
    plt.plot(n_values, info_hl, label='Information with Heisenberg Limit', linestyle='-')
    plt.xlabel('Number of Probes/Receptors (N)')
    plt.ylabel('Information Content (bits)')
    plt.title('Information Gain from Sensing: SQL vs Heisenberg Limit')
    # plt.yscale('log') # Information gain might not always be log scale beneficial here
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig(f"{filename_prefix}_information.png")
    plt.close()

    print(f"Generated plots: {filename_prefix}_precision.png and {filename_prefix}_information.png")

def discuss_bandwidth_limitations():
    discussion = """
    Bandwidth Limitations in Biological Sensors:

    Information Theoretic Perspective:
    - Bandwidth relates to the rate at which a sensor can acquire and transmit information
      about a changing environment.
    - Higher precision (lower uncertainty Δφ for a parameter φ) allows for more distinguishable
      states within a given range, increasing the information content per measurement (log2(Range/Δφ)).
    - Faster measurement times or more measurements per unit time contribute to higher bandwidth.

    Classical Sensors (SQL-limited):
    - If each sensing element (e.g., receptor molecule) acts independently, the precision scales
      as 1/√N (where N is the number of elements or measurements).
    - To double precision (halve uncertainty), N must be quadrupled. This imposes a soft limit
      on achievable bandwidth due to resource constraints (number of receptors, energy, time).

    Quantum-Enhanced Sensors (potentially HL-limited):
    - If sensing elements can be entangled or utilize other collective quantum effects, precision
      could ideally scale as 1/N (Heisenberg Limit).
    - This offers a significant advantage: doubling precision only requires doubling N.
    - This could translate to:
        * Higher information content for the same N.
        * Faster attainment of a desired precision.
        * Sensing subtle changes that are below the noise floor for classical sensors.

    Biological Context & Challenges:
    - While true Heisenberg-limited sensing is challenging even in controlled lab settings,
      biological systems might employ quantum effects that offer some advantages over purely
      classical, independent receptor models.
    - Examples:
        * Cooperative binding in hemoglobin (not strictly quantum sensing, but shows collective effects).
        * Radical pair mechanism in magnetoreception: the lifetime and coherence of entangled
          radical pairs could determine the precision of magnetic field sensing. Longer coherence
          allows for more interaction time, effectively increasing 'N' in a temporal sense.
        * Photosynthetic light harvesting: rapid and efficient energy transfer could be seen as
          optimizing the 'bandwidth' of light capture.
    - Limitations in biological systems:
        * Decoherence: Maintaining quantum states (like entanglement) in warm, wet environments is hard.
        * Readout: Efficiently extracting the information from a quantum state can be non-trivial.
        * Energy costs: Creating and maintaining quantum states might have metabolic costs.

    Quantifying the "Information Advantage":
    - The plots generated by this script illustrate the potential information gain if HL can be
      approached compared to SQL. The 'advantage' is the difference (e.g., info_hl - info_sql)
      or ratio (info_hl / info_sql) for a given N.
    - Real biological systems might operate somewhere between these two ideal limits. Identifying
      where they lie and what mechanisms allow them to potentially surpass classical SQL is key.
    """
    print(discussion)

if __name__ == '__main__':
    num_probes = 200 # Max number of probes/receptors for simulation
    param_range = 1.0 # e.g., concentration range from 0 to 1 arbitrary units
    sensitivity_per_probe = 0.5 # Intrinsic sensitivity of each probe element

    n_vals, u_sql, u_hl, inf_sql, inf_hl = compare_sensing_limits_and_information(
        max_probes=num_probes,
        parameter_range=param_range,
        sensitivity=sensitivity_per_probe
    )

    # Define a path for saving plots within the agent's analysis folder
    # This path needs to be adjusted if the script is not run from the root of the repo
    # For the subtask, assume it's run from a location where this path is valid.
    # When running locally, ensure 'integration/20250531-182000-InfoTheory/analysis/' exists
    # or adjust the path. For subtask, it will create it in current dir.
    # The main task will later specify where these files should be.
    plot_filename_prefix = "sensor_comparison_output" # Files will be saved where script is run

    plot_sensing_comparison(n_vals, u_sql, u_hl, inf_sql, inf_hl, filename_prefix=plot_filename_prefix)

    print("\n--- Discussion ---")
    discuss_bandwidth_limitations()

    print(f"\nExample: For N={num_probes} probes:")
    print(f"  SQL: Uncertainty={u_sql[-1]:.4f}, Information={inf_sql[-1]:.4f} bits")
    print(f"  HL:  Uncertainty={u_hl[-1]:.4f}, Information={inf_hl[-1]:.4f} bits")
    if inf_sql[-1] > 0 :
        print(f"  Information Advantage (HL/SQL Ratio): {inf_hl[-1]/inf_sql[-1]:.2f}")
    else:
        print(f"  Information Advantage (HL/SQL Ratio): N/A (SQL info is zero or negative)")
