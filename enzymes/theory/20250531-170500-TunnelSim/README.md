# Quantum Tunneling Calculator for Biological Systems

**Agent ID:** 20250531-170500-TunnelSim
**Phenomenon:** Enzymes
**Task Type:** Theory

## Description

This project implements a simple quantum tunneling calculator to explore proton/electron tunneling rates in scenarios relevant to biological systems, particularly enzymes. It compares quantum tunneling probabilities with classical probabilities for particles (electrons, protons, deuterons) encountering a potential barrier.

The calculator varies:
- Barrier width (L): 0.5 to 5 Angstroms
- Barrier height (V): 0.1 to 2 eV
- Particle mass (m): Electron, Proton, Deuteron

The particle energy (E) is fixed at 0.1 eV for these simulations.

The primary goal is to identify regimes where quantum tunneling "beats" classical transmission by a significant margin (specifically, where classical probability is zero, and quantum tunneling probability is non-zero).

## How to Run

1.  Ensure you have Python and NumPy installed.
    ```bash
    pip install numpy
    ```
2.  Navigate to the root directory of this repository.
3.  Run the main script:
    ```bash
    python -m enzymes.theory.20250531-170500-TunnelSim.analysis.main
    ```
    This will print a table of parameter combinations where quantum tunneling is observed in classically forbidden scenarios.

## Files
- `analysis/constants.py`: Defines physical constants and conversion factors.
- `analysis/tunneling_calculator.py`: Implements the quantum tunneling probability calculation.
- `analysis/classical_calculator.py`: Implements the classical transmission probability calculation.
- `analysis/main.py`: Main script to iterate through parameters and identify quantum-dominant regimes.
- `findings.json`: Structured summary of key findings.
- `sources.bib`: Bibliography.
- `next_questions.md`: Potential future research questions.
