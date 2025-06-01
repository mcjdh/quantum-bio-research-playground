# DNA Mutation Simulation: Quantum Tunneling vs. Classical Activation

This simulation models and compares the probabilities of proton transfer in DNA base pairs via quantum tunneling and classical thermal activation. Such proton transfers are a potential mechanism for tautomeric mutations.

## Simulation Overview

The simulation calculates:
1.  **Proton Ground State Energy (E_proton)**: Energy of a proton confined in a 1D potential well of a given width (approximating its initial localization).
2.  **Quantum Tunneling Probability (P_tunneling)**: Calculated using the WKB approximation for a square potential barrier of a given height (V0) and width (L_barrier). This probability is temperature-independent in the current model.
3.  **Classical Activation Probability (P_classical)**: Calculated using an Arrhenius-like formula, dependent on temperature and the barrier height (V0).

The script then compares P_tunneling and P_classical across a range of biologically relevant temperatures.

## Key Parameters Used
- Proton confinement well width (`proton_well_width_A`): 0.5 Å
- Potential barrier height (`V0_eV`): 0.3 eV
- Potential barrier width (`L_barrier_A`): 0.4 Å
- Temperature range: 270K to 330K

## How to Run
Navigate to the `dna/20250531-172500-MutationSim/analysis/` directory and run:
```sh
python dna_mutation_simulation.py
```

## Main Finding
For the parameters chosen, quantum tunneling is found to be the dominant mechanism for proton transfer compared to classical thermal activation across the entire simulated temperature range (270K-330K). The tunneling probability can be over an order of magnitude greater than the classical probability, especially at lower physiological temperatures.

This suggests that quantum effects could play a significant role in spontaneous mutation rates if these parameters are representative of actual proton transfer barriers in DNA.

## Output Files
The simulation generates:
- `dna/20250531-172500-MutationSim/analysis/simulation_results.csv`: A CSV file containing temperatures, P_tunneling, P_classical, and their ratio.
- `dna/20250531-172500-MutationSim/analysis/tunneling_vs_classical_plot.png`: A plot visualizing the comparison of P_tunneling and P_classical versus temperature.
