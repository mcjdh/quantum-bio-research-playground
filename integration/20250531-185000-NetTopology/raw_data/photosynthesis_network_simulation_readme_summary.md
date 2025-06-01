# Summary from photosynthesis/network_simulation/README.md

## Goal
Simulate energy transfer in 7-node networks (linear chain, ring, star) to find topologies and parameters for >90% efficiency.

## Theoretical Basis
- System Hamiltonian for coherent energy transfer.
- Lindblad master equation for open quantum system dynamics.

## Key Findings: High-Efficiency Configurations (7 nodes)
1.  **Topology**: `linear_chain`
    *   **Coupling Strength (J)**: 100.0 cm<sup>-1</sup>
    *   **Dephasing Rate (gamma)**: 0.20 ps<sup>-1</sup>
    *   **Achieved Efficiency**: **97.60%**

2.  **Topology**: `ring`
    *   **Coupling Strength (J)**: 100.0 cm<sup>-1</sup>
    *   **Dephasing Rate (gamma)**: 0.20 ps<sup>-1</sup>
    *   **Achieved Efficiency**: **92.75%**

3.  **Topology**: `linear_chain`
    *   **Coupling Strength (J)**: 100.0 cm<sup>-1</sup>
    *   **Dephasing Rate (gamma)**: 0.05 ps<sup>-1</sup>
    *   **Achieved Efficiency**: **91.73%**

## Observations:
*   Stronger coupling (100 cm<sup>-1</sup>) was generally more effective.
*   Moderate dephasing rate (0.20 ps<sup>-1</sup>) in top configurations suggests potential ENAQT.
*   Linear chain topology yielded the highest efficiency.
