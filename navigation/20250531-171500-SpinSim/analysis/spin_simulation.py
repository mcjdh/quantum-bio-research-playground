import qutip
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# 1. Define physical constants
g_electron = 2.0023  # Electron g-factor
mu_B_MHz_uT = 0.013996  # Bohr magneton in MHz/uT

# 2. Define spin system parameters
# Two spin-1/2 particles
# Initial state: Singlet state (|ud> - |du>) / sqrt(2)
spin_up = qutip.basis(2, 0)
spin_down = qutip.basis(2, 1)
initial_state = (qutip.tensor(spin_up, spin_down) - qutip.tensor(spin_down, spin_up)).unit()

# 3. Construct spin operators
# Spin 1 operators
sx1 = qutip.tensor(qutip.sigmax(), qutip.qeye(2))
sy1 = qutip.tensor(qutip.sigmay(), qutip.qeye(2))
sz1 = qutip.tensor(qutip.sigmaz(), qutip.qeye(2))
# Spin 2 operators
sx2 = qutip.tensor(qutip.qeye(2), qutip.sigmax())
sy2 = qutip.tensor(qutip.qeye(2), qutip.sigmay())
sz2 = qutip.tensor(qutip.qeye(2), qutip.sigmaz())

# 6. Define projection operators
# Operator to project onto the initial singlet state
P_singlet = initial_state * initial_state.dag()


# Helper function to run simulation and get average singlet yield
def run_simulation(B_field_uT_val, gamma_val, tlist_val, initial_state_val, P_singlet_val):
    """
    Runs the spin simulation for a given B_field, gamma, and tlist.
    Returns the average singlet yield over the simulation time.
    """
    # Define Hamiltonian components
    g1 = 2.0023
    g2 = 2.0000
    w1 = g1 * mu_B_MHz_uT * B_field_uT_val
    w2 = g2 * mu_B_MHz_uT * B_field_uT_val
    H_Zeeman_val = w1 * sz1 + w2 * sz2
    H_val = H_Zeeman_val

    # Define collapse operators
    c_ops_val = [np.sqrt(gamma_val) * sz1, np.sqrt(gamma_val) * sz2]

    # Perform time evolution
    result = qutip.mesolve(H_val, initial_state_val, tlist_val, c_ops_val, [P_singlet_val], options=qutip.Options(store_final_state=True))

    # Calculate average singlet yield
    # Taking mean of all points except the first one (t=0) which is always 1.0 for singlet state
    if len(result.expect[0]) > 1:
        average_singlet_yield = np.mean(result.expect[0][1:])
    elif len(result.expect[0]) == 1: # single point in tlist
        average_singlet_yield = result.expect[0][0]
    else: # no points
        average_singlet_yield = 0
    return average_singlet_yield

# --- Main Parameter Sweep ---

# Define parameter ranges
gamma_values_MHz = np.logspace(-2, 2, 20)  # 0.01 MHz to 100 MHz decoherence rates
B0_uT = 50.0  # Baseline magnetic field strength in uT
dB_uT = 1.0  # Small change in magnetic field for sensitivity calculation in uT
n_steps_tlist = 200 # Number of steps for tlist

sensitivity_data = [] # To store (tau, sensitivity)

print("Starting parameter sweep for sensitivity analysis...")
for gamma_MHz in gamma_values_MHz:
    tau_us = 1.0 / gamma_MHz  # Lifetime in microseconds

    # Adjust simulation time based on lifetime
    # Simulate for roughly 10 characteristic lifetimes, or a minimum of 1us, max of 1000us
    t_final_us = np.clip(10.0 * tau_us, 1.0, 1000.0)
    tlist_sim = np.linspace(0, t_final_us, n_steps_tlist)

    print(f"Running for gamma = {gamma_MHz:.2e} MHz (tau = {tau_us:.2e} us), t_final = {t_final_us:.2e} us")

    # Simulate for B0
    Yield_B0 = run_simulation(B0_uT, gamma_MHz, tlist_sim, initial_state, P_singlet)

    # Simulate for B0 + dB
    Yield_B_plus_dB = run_simulation(B0_uT + dB_uT, gamma_MHz, tlist_sim, initial_state, P_singlet)

    # Calculate Sensitivity
    sensitivity = np.abs(Yield_B_plus_dB - Yield_B0) / dB_uT
    sensitivity_data.append((tau_us, sensitivity))
    print(f"  Yield (B0) = {Yield_B0:.4f}, Yield (B0+dB) = {Yield_B_plus_dB:.4f}, Sensitivity = {sensitivity:.4e} Yield/uT")

print("Parameter sweep finished.")

# Convert data to NumPy array for easier handling
sensitivity_data_np = np.array(sensitivity_data)
lifetimes_us = sensitivity_data_np[:, 0]
sensitivities = sensitivity_data_np[:, 1]

# 8. Data Storage and Plotting
# Determine script's directory to make paths robust
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save raw data to CSV
csv_filename = os.path.join(script_dir, "..", "raw_data", "sensitivity_data.csv")
# Ensure the target directory exists
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["lifetime_mus", "sensitivity_yield_per_uT"])
    for row in sensitivity_data:
        writer.writerow(row)
print(f"Sensitivity data saved to {csv_filename}")

# Create log-log plot of sensitivity vs. lifetime
plt.figure(figsize=(10, 6))
plt.loglog(lifetimes_us, sensitivities, 'o-')
plt.xlabel("Lifetime (µs)")
plt.ylabel("Sensitivity (Singlet Yield Change / µT)")
plt.title("Magnetometer Sensitivity vs. Spin Lifetime")
plt.grid(True, which="both", ls="--")
plot_filename = os.path.join(script_dir, "sensitivity_vs_lifetime.png")
plt.savefig(plot_filename)
print(f"Plot saved to {plot_filename}")

# To make the script runnable from command line if needed
if __name__ == '__main__':
    pass
