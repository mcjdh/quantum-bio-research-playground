# Photosynthetic Network Simulation

This directory contains the code and results for simulating energy transfer in photosynthetic networks.

## Goal

The primary goal of this simulation was to model energy transfer through small networks of 7-10 nodes (specifically 7 nodes were simulated), incorporating variable coupling strengths and noise/decoherence effects. We aimed to identify network topologies and parameter configurations that can achieve greater than 90% energy transfer efficiency.

## Theoretical Basis

The simulation is based on the theoretical framework outlined in `../../theory/20250531-161000-PhotoTheory/README.md`. This includes:
- System Hamiltonian for coherent energy transfer.
- Lindblad master equation for modeling open quantum system dynamics. Trapping was modeled using an effective non-Hermitian Hamiltonian term (`H_eff = H_sys - 0.5j * k_trap * |T⟩⟨T|`), and dephasing was modeled using Lindblad jump operators (`C_k = sqrt(gamma_k) * |k⟩⟨k|`).

## Methodology

1.  **Network Definition**: Several network topologies for 7 nodes were defined:
    *   Linear Chain
    *   Ring
    *   Star (with center at node 0, or middle node)
2.  **Parameterization**: Simulations were run by varying:
    *   **Coupling Strengths (J)**: [50.0, 100.0] cm<sup>-1</sup>
    *   **Dephasing Rates (gamma_k)**: [0.05, 0.2] ps<sup>-1</sup> (uniform across sites)
    *   **Trap Rate (k_trap)**: [1.0] ps<sup>-1</sup> (at site N-1)
    *   **Site Energies**: Initial excitation site at 200 cm<sup>-1</sup>, trap site at 0 cm<sup>-1</sup>, other sites at 150 cm<sup>-1</sup>.
    *   **Initial State**: Excitation localized at site 0.
3.  **Simulation**: Quantum dynamics were simulated by numerically solving the master equation using `scipy.integrate.solve_ivp` for a duration of 50 ps.
4.  **Efficiency Calculation**: Efficiency was calculated as `1 - Tr(rho_final)`, representing the fraction of the initial population successfully transferred to the trap.

## Key Findings: High-Efficiency Configurations

The exploration yielded several configurations achieving over 90% energy transfer efficiency with 7 nodes. The top 3 configurations are:

1.  **Topology**: `linear_chain`
    *   **Coupling Strength (J)**: 100.0 cm<sup>-1</sup>
    *   **Dephasing Rate (gamma)**: 0.20 ps<sup>-1</sup>
    *   **Trap Rate (k_trap)**: 1.0 ps<sup>-1</sup>
    *   **Achieved Efficiency**: **97.60%**

2.  **Topology**: `ring`
    *   **Coupling Strength (J)**: 100.0 cm<sup>-1</sup>
    *   **Dephasing Rate (gamma)**: 0.20 ps<sup>-1</sup>
    *   **Trap Rate (k_trap)**: 1.0 ps<sup>-1</sup>
    *   **Achieved Efficiency**: **92.75%**

3.  **Topology**: `linear_chain`
    *   **Coupling Strength (J)**: 100.0 cm<sup>-1</sup>
    *   **Dephasing Rate (gamma)**: 0.05 ps<sup>-1</sup>
    *   **Trap Rate (k_trap)**: 1.0 ps<sup>-1</sup>
    *   **Achieved Efficiency**: **91.73%**

### Observations:
*   **Stronger coupling (100 cm<sup>-1</sup>)** was generally more effective than weaker coupling (50 cm<sup>-1</sup>) in the tested range for achieving high efficiency.
*   A **moderate dephasing rate (0.20 ps<sup>-1</sup>)** appeared in the top two configurations. This might suggest that some level of environmental noise could be beneficial, potentially aligning with Environment-Assisted Quantum Transport (ENAQT) principles where noise helps overcome localization or facilitates energy transfer. However, a more systematic scan of dephasing rates and analysis of population dynamics would be needed to confirm ENAQT. The third best result had lower dephasing (0.05 ps<sup>-1</sup>), indicating the relationship is not simple.
*   The **linear chain topology** yielded the highest efficiency in this specific set of simulations.

## Simulation Code and Data

-   `simulation.py`: The Python script containing the `QuantumNetwork` class, simulation logic, parameter exploration loop, and helper functions for topology generation.
-   `simulation_results.txt`: A CSV-like file containing the parameters and achieved efficiency for all simulated configurations.

## Future Work
*   Expand the range of parameters (nodes, coupling strengths, dephasing, site energies).
*   Implement more complex and biologically inspired topologies (e.g., FMO-like).
*   Perform a detailed analysis of population dynamics for high-efficiency cases to understand transport mechanisms.
*   Systematically investigate the role of dephasing to confirm or refute ENAQT.
*   Explore different initial excitation sites and trap locations.

EOF
