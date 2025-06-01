# Decoherence Time Simulation in Biological Conditions

## Overview
This simulation explores decoherence times for quantum systems under varying conditions of temperature, molecular size, and different biological environments. The goal is to understand how these factors might influence the persistence of quantum effects in biological contexts.

## Parameters Explored
The simulation varied the following parameters:
*   **Temperature**: 270K to 370K (physiological range).
*   **Molecular Size**: A generic parameter explored on a logarithmic scale from 10 to 10,000 (arbitrary units), representing a range from smaller molecules to larger complexes.
*   **Environments**:
    *   Water (Coupling strength: 1.0)
    *   Lipid Membrane (Coupling strength: 0.5)
    *   Protein Pocket (Coupling strength: 0.1)
    The coupling strengths are placeholder values for this initial simulation.

## Methodology
A Python script (`analysis/decoherence_simulation.py`) was used to perform the simulation. It employs a simplified, placeholder model for calculating decoherence time based on the formula: `Decoherence Time = 1.0 / (Temperature * Molecular_Size_Parameter * Environment_Coupling_Strength)`. This model is illustrative and serves as a basis for future refinement.

## Results
The simulation generated heatmap plots for each environment, visualizing the calculated decoherence times across the ranges of temperature and molecular size. These "quantum survival zones" (areas with longer decoherence times) can be found in the `analysis/` folder. Key output files include:
*   `analysis/heatmap_water.png`
*   `analysis/heatmap_lipid_membrane.png`
*   `analysis/heatmap_protein_pocket.png`

## Initial Observations
Based on the simplified model:
*   Decoherence times generally decrease with increasing temperature.
*   Decoherence times generally decrease with increasing molecular size parameter.
*   The 'protein pocket' environment, with its lower assumed coupling strength in this model, exhibited significantly longer decoherence times compared to 'water' or 'lipid membranes'. This suggests that such environments might be more conducive to sustaining quantum coherence. Conversely, 'water', with the highest coupling, showed the shortest decoherence times.

These observations are preliminary and depend heavily on the chosen model and parameters.
