import numpy as np
from scipy.integrate import solve_ivp
import itertools # For parameter combinations

# --- QuantumNetwork Class and Core Simulation Functions ---
class QuantumNetwork:
    def __init__(self, num_nodes, site_energies, coupling_matrix, trap_site_index, trap_rate, dephasing_rates):
        if not (2 <= num_nodes <= 15):
             pass
        if len(site_energies) != num_nodes:
            raise ValueError("Length of site_energies must match num_nodes.")
        if coupling_matrix.shape != (num_nodes, num_nodes):
            raise ValueError("Shape of coupling_matrix must be (num_nodes, num_nodes).")
        if not (0 <= trap_site_index < num_nodes):
            raise ValueError("trap_site_index is out of bounds.")

        self.num_nodes = num_nodes
        self.site_energies = np.array(site_energies, dtype=float)
        self.coupling_matrix = np.array(coupling_matrix, dtype=float)
        self.trap_site_index = trap_site_index
        self.trap_rate = float(trap_rate)

        if isinstance(dephasing_rates, (list, np.ndarray)):
            if len(dephasing_rates) != num_nodes:
                raise ValueError("Length of dephasing_rates list must match num_nodes.")
            self.dephasing_rates = np.array(dephasing_rates, dtype=float)
        elif isinstance(dephasing_rates, (int, float)):
            self.dephasing_rates = np.full(self.num_nodes, float(dephasing_rates), dtype=float)
        else:
            raise ValueError("dephasing_rates must be a list or a single number.")

        self.hamiltonian = self._build_hamiltonian()
        self.dephasing_jump_ops, self.dephasing_jump_ops_precomputed_sum_term = self._build_dephasing_jump_operators()
        self.H_eff_for_solver = self._build_effective_hamiltonian_for_trapping()

    def _build_hamiltonian(self):
        H = np.diag(self.site_energies).astype(complex)
        H += self.coupling_matrix.astype(complex)
        for i in range(self.num_nodes):
            if self.coupling_matrix[i,i] != 0.0:
                H[i,i] = self.site_energies[i]
        return H

    def get_hamiltonian(self):
        return self.hamiltonian

    def _build_dephasing_jump_operators(self):
        ops = []
        precomputed_sum_terms = []
        for k in range(self.num_nodes):
            if self.dephasing_rates[k] > 0:
                C_k_deph = np.zeros((self.num_nodes, self.num_nodes), dtype=complex)
                C_k_deph[k, k] = np.sqrt(self.dephasing_rates[k])
                ops.append(C_k_deph)
                precomputed_sum_terms.append(C_k_deph.conj().T @ C_k_deph)
        return ops, precomputed_sum_terms

    def get_dephasing_jump_operators(self):
        return self.dephasing_jump_ops, self.dephasing_jump_ops_precomputed_sum_term

    def _build_effective_hamiltonian_for_trapping(self):
        H_eff = self.hamiltonian.copy()
        if self.trap_rate > 0:
            P_T = np.zeros((self.num_nodes, self.num_nodes), dtype=complex)
            P_T[self.trap_site_index, self.trap_site_index] = 1.0
            H_eff -= 0.5j * self.trap_rate * P_T
        return H_eff

    def get_effective_hamiltonian(self):
        return self.H_eff_for_solver

    def master_equation_rhs(self, t, rho_vec):
        rho = rho_vec.reshape((self.num_nodes, self.num_nodes))
        d_rho_dt_coherent_trap = -1j * (self.H_eff_for_solver @ rho - rho @ self.H_eff_for_solver.conj().T)
        d_rho_dt_dephasing = np.zeros_like(rho, dtype=complex)
        jump_ops_list, precomputed_terms_list = self.dephasing_jump_ops, self.dephasing_jump_ops_precomputed_sum_term
        for i in range(len(jump_ops_list)):
            C_k = jump_ops_list[i]
            C_k_dag_C_k = precomputed_terms_list[i]
            d_rho_dt_dephasing += C_k @ rho @ C_k.conj().T
            d_rho_dt_dephasing -= 0.5 * (C_k_dag_C_k @ rho + rho @ C_k_dag_C_k)
        d_rho_dt = d_rho_dt_coherent_trap + d_rho_dt_dephasing
        return d_rho_dt.flatten()

def run_simulation(network, rho_initial_flat, t_span, t_eval, rtol=1e-6, atol=1e-9):
    sol = solve_ivp(
        fun=network.master_equation_rhs,
        t_span=t_span,
        y0=rho_initial_flat,
        t_eval=t_eval,
        method='RK45',
        rtol=rtol,
        atol=atol
    )
    return sol

def calculate_efficiency(simulation_result, network_num_nodes, initial_total_population=1.0):
    if not simulation_result.success:
        return 0.0
    rho_final_flat = simulation_result.y[:, -1]
    rho_final = rho_final_flat.reshape((network_num_nodes, network_num_nodes))
    population_remaining = np.trace(rho_final).real
    efficiency = (initial_total_population - population_remaining) / initial_total_population
    return np.clip(efficiency, 0.0, 1.0)

def get_population_at_site(rho_matrix, site_index):
    return rho_matrix[site_index, site_index].real

# --- Topology Helper Functions ---
def create_linear_chain_coupling_matrix(num_nodes, coupling_strength, *args):
    matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes - 1):
        matrix[i, i+1] = coupling_strength
        matrix[i+1, i] = coupling_strength
    return matrix

def create_ring_coupling_matrix(num_nodes, coupling_strength, *args):
    matrix = create_linear_chain_coupling_matrix(num_nodes, coupling_strength)
    if num_nodes > 1:
        matrix[0, num_nodes-1] = coupling_strength
        matrix[num_nodes-1, 0] = coupling_strength
    return matrix

def create_star_coupling_matrix(num_nodes, center_node_idx, coupling_strength):
    if num_nodes < 2: return np.zeros((num_nodes, num_nodes))
    matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        if i == center_node_idx:
            continue
        matrix[center_node_idx, i] = coupling_strength
        matrix[i, center_node_idx] = coupling_strength
    return matrix

# --- Placeholder for Main Exploration Logic ---
# The main exploration logic will be appended in a subsequent step.
print("Core QuantumNetwork classes and functions defined.")

# --- Main Exploration Logic (Appended) ---
if __name__ == "__main__":
    print("Starting main exploration logic...")
    NUM_NODES = 7
    INITIAL_EXCITATION_SITE = 0
    TRAP_SITE = NUM_NODES - 1

    site_energies_template = np.full(NUM_NODES, 150.0)
    site_energies_template[TRAP_SITE] = 0.0
    site_energies_template[INITIAL_EXCITATION_SITE] = 200.0

    if INITIAL_EXCITATION_SITE == TRAP_SITE:
        site_energies_template[INITIAL_EXCITATION_SITE] = 50.0

    T_START = 0
    T_END = 50.0 # Simulation time in ps
    NUM_TIME_POINTS = 200
    t_eval_points = np.linspace(T_START, T_END, NUM_TIME_POINTS)

    coupling_strengths_to_test = [50.0, 100.0]  # cm^-1
    dephasing_rates_to_test = [0.05, 0.2]     # ps^-1
    trap_rates_to_test = [1.0]                # ps^-1

    topologies_to_define = [
        {"name": "linear_chain", "func": create_linear_chain_coupling_matrix, "center_arg_idx": -1},
        {"name": "ring", "func": create_ring_coupling_matrix, "center_arg_idx": -1},
        {"name": "star_center_0", "func": create_star_coupling_matrix, "center_arg_idx": 0},
        {"name": "star_center_mid", "func": create_star_coupling_matrix, "center_arg_idx": NUM_NODES // 2},
    ]

    valid_topologies = []
    for topo_def in topologies_to_define:
        if topo_def["center_arg_idx"] != -1:
            center_idx = topo_def["center_arg_idx"]
            if center_idx >= NUM_NODES:
                print(f"Skipping topology {topo_def['name']} as center_idx {center_idx} is out of bounds for {NUM_NODES} nodes.")
                continue
        valid_topologies.append(topo_def)

    results = []
    run_counter = 0
    max_runs = 50 # Safety break

    print(f"Starting topology and parameter exploration for {NUM_NODES} nodes...")
    print(f"Initial excitation: site {INITIAL_EXCITATION_SITE}, Trap: site {TRAP_SITE}")
    print(f"ItSite E: {site_energies_template[INITIAL_EXCITATION_SITE]}, TrapSite E: {site_energies_template[TRAP_SITE]}, OtherSites E: {site_energies_template[1 if INITIAL_EXCITATION_SITE !=1 and TRAP_SITE !=1 else (NUM_NODES // 2)]}")
    print("---")

    param_combinations = list(itertools.product(valid_topologies, coupling_strengths_to_test, dephasing_rates_to_test, trap_rates_to_test))

    for topo_def, J_coupling, dephasing_rate, trap_rate in param_combinations:
        if run_counter >= max_runs:
            print(f"Reached max_runs ({max_runs}). Stopping exploration.")
            break
        run_counter += 1

        topology_name = topo_def["name"]
        coupling_func = topo_def["func"]
        current_site_energies = site_energies_template.copy()

        if topo_def["center_arg_idx"] != -1:
            center_node_index = topo_def["center_arg_idx"]
            coupling_matrix = coupling_func(NUM_NODES, center_node_index, J_coupling)
        else:
            coupling_matrix = coupling_func(NUM_NODES, J_coupling)

        print(f"Run {run_counter}: Testing: Topo='{topology_name}', J={J_coupling:.1f}, Deph={dephasing_rate:.2f}, TrapR={trap_rate:.1f}")

        try:
            network = QuantumNetwork(
                num_nodes=NUM_NODES,
                site_energies=current_site_energies,
                coupling_matrix=coupling_matrix,
                trap_site_index=TRAP_SITE,
                trap_rate=trap_rate,
                dephasing_rates=dephasing_rate
            )

            rho_initial = np.zeros((NUM_NODES, NUM_NODES), dtype=complex)
            rho_initial[INITIAL_EXCITATION_SITE, INITIAL_EXCITATION_SITE] = 1.0
            initial_trace = np.trace(rho_initial).real

            sim_result = run_simulation(network, rho_initial.flatten(), (T_START, T_END), t_eval_points, rtol=1e-5, atol=1e-8)

            if sim_result.success:
                efficiency = calculate_efficiency(sim_result, network.num_nodes, initial_total_population=initial_trace)
                results.append({
                    "topology": topology_name, "J_coupling": J_coupling, "dephasing_rate": dephasing_rate,
                    "trap_rate": trap_rate, "efficiency": efficiency, "sim_message": sim_result.message, "status": sim_result.status
                })
                # print(f"  => Efficiency: {efficiency:.4f} ({(efficiency*100):.2f}%) Status: {sim_result.status}")
                print(f"  => Efficiency: {efficiency:.4f}")
            else:
                # print(f"  => Sim FAILED: {sim_result.message} (Status: {sim_result.status})")
                results.append({
                    "topology": topology_name, "J_coupling": J_coupling, "dephasing_rate": dephasing_rate,
                    "trap_rate": trap_rate, "efficiency": 0.0, "sim_message": sim_result.message, "status": sim_result.status
                })
                print(f"  => Sim FAILED: {sim_result.message}")


        except Exception as e:
            print(f"  => ERROR during simulation: {e}")
            results.append({
                "topology": topology_name, "J_coupling": J_coupling, "dephasing_rate": dephasing_rate,
                "trap_rate": trap_rate, "efficiency": -1.0, "sim_message": str(e), "status": -99 # Custom error status
            })

    print("\n--- Exploration Summary (Top 10 by Efficiency) ---")
    if results:
        successful_runs = [r for r in results if r['efficiency'] > 0.0001] # Filter very low/failed
        sorted_results = sorted(successful_runs, key=lambda x: x["efficiency"], reverse=True)
        if not sorted_results:
            print("No sufficiently efficient configurations found.")
        for i, res in enumerate(sorted_results[:10]):
            print(f"{i+1}. Topo: {res['topology']}, J={res['J_coupling']:.1f}, Deph={res['dephasing_rate']:.2f}, Trap={res['trap_rate']:.1f} => Eff: {res['efficiency']:.4f}")
    else:
        print("No results to display.")

    # Storing results to a file
    try:
        with open("photosynthesis/network_simulation/simulation_results.txt", "w") as f:
            if not results:
                f.write("No simulation results.\n")
            else:
                f.write("Topology,Coupling,DephasingRate,TrapRate,Efficiency,Message,Status\n")
                for res in results:
                    f.write(f"{res['topology']},{res['J_coupling']},{res['dephasing_rate']},{res['trap_rate']},{res['efficiency']},{res['sim_message']},{res.get('status', 'N/A')}\n")
            print("\nFull results logged to photosynthesis/network_simulation/simulation_results.txt")
    except Exception as e:
        print(f"Error writing results to file: {e}")
