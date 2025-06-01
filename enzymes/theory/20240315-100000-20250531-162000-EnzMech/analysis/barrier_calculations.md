# Framework for Barrier Height Calculation and Tunneling Analysis

This document outlines the conceptual approach and considerations for calculating potential energy barrier heights and assessing quantum tunneling contributions in the enzyme designs sketched in `enzyme_sketches.md`.

## 1. Computational Strategy: QM/MM

For realistic enzyme systems, a Quantum Mechanics/Molecular Mechanics (QM/MM) approach is generally the most suitable.

*   **QM Region:**
    *   Includes the substrate atoms directly involved in the reaction (e.g., the C-H bond being broken, the acceptor atom).
    *   Key catalytic residues (e.g., acid/base groups, atoms forming the donor/acceptor).
    *   The relevant part of any cofactor.
    *   Typically 50-200 atoms.
    *   **Method:** Density Functional Theory (DFT) is a good balance of accuracy and cost. Recommended functionals include M06-2X, ωB97X-D, or B3LYP-D3. Basis sets like 6-31G*(d,p) or def2-SVP/def2-TZVP.
*   **MM Region:**
    *   The rest of the enzyme and surrounding solvent (water molecules).
    *   **Force Field:** Standard protein force fields like AMBER, CHARMM, OPLS.

## 2. Identifying the Reaction Coordinate and Transition State (TS)

*   **Initial Path Finding:** For a proposed reaction (e.g., hydride transfer), an initial reaction path can be explored using methods like Nudged Elastic Band (NEB) or string methods within the QM/MM framework. This involves creating a series of images connecting the reactant and product states.
*   **Transition State Optimization:** The highest energy point along the approximate path is then used as a starting guess for a full TS optimization. This requires finding a first-order saddle point on the potential energy surface (one imaginary frequency).
*   **Intrinsic Reaction Coordinate (IRC):** Following the IRC from the optimized TS confirms that it connects the intended reactant and product states.
*   **Barrier Height (V0 or ΔE‡):** Calculated as `E(TS) - E(Reactant)`. Zero-point vibrational energy (ZPVE) corrections should be included.

## 3. Incorporating Protein Dynamics

Tunneling is highly sensitive to donor-acceptor distance. Static TS calculations might not capture the "tunneling-ready" conformations.

*   **Molecular Dynamics (MD) Simulations:** Perform QM/MM MD simulations to sample conformational space.
*   **Umbrella Sampling or Metadynamics:** Along a chosen reaction coordinate (e.g., D-A distance) to map out the free energy surface (Potential of Mean Force - PMF). The barrier height is derived from the PMF.
*   **Identifying "Reactive Conformations":** Analyze trajectories to find structures where the D-A distance is particularly short, even if they are transient. These are the configurations from which tunneling is most likely.

## 4. Estimating Tunneling Probability and Rate Constants

Once a barrier height (V0) and shape (implicitly from the PES scan or TS analysis) are known:

*   **Simplified Models (for quick estimation based on QM/MM data):**
    *   **Eckart Barrier Model:**
        *   Requires: `V0` (barrier height), energy difference between reactant and product, and a parameter related to barrier width/curvature (can be estimated from the imaginary frequency at the TS).
        *   The transmission coefficient `κ(E)` can be calculated.
    *   **Bell Correction (1D):** A simpler correction based on the imaginary frequency (`ν‡`) from the TS calculation:
            `κ_Bell = (h|ν‡| / 2πkT) / sin(h|ν‡| / 2πkT)` (for `h|ν‡|/2kT < π`)
            This primarily accounts for tunneling *through the top* of the barrier.

*   **More Advanced Methods (if computational resources allow):**
    *   **Variational Transition State Theory with Multidimensional Tunneling Corrections (VTST/MT):** E.g., Small Curvature Tunneling (SCT) or Large Curvature Tunneling (LCT). This considers tunneling paths that deviate from the MEP. These are implemented in codes like Polyrate or Gaussian.
    *   **Path Integral Methods (e.g., RPMD, Centroid MD):** These can explicitly include nuclear quantum effects in simulations.

## 5. Parameters for a Hypothetical Calculation (Example: Hydride Transfer)

*   **System:** An enzyme active site model (from PDB or homology model).
*   **QM Region Example:** Substrate (e.g., alcohol), NAD+ cofactor, catalytic Asp residue.
*   **Reaction:** Hydride transfer from C1 of substrate to C4N of NAD+.
*   **Key Distances:**
    *   `d1`: Distance between hydride (H) on substrate and C4N of NAD+.
    *   `d2`: Distance between H and the C1 of substrate.
    *   Reaction coordinate could be `d1 - d2`.
*   **Expected Barrier Height (Classical):** 10-20 kcal/mol (typical for enzyme C-H activation).
*   **Tunneling Particle Mass:** ~1.008 amu (for hydride, though effective mass can vary).
*   **Software for QM/MM:** Gaussian + AMBER, or ORCA + CHARMM.

This framework provides a roadmap from conceptual design to quantitative assessment of tunneling contributions. The actual implementation would require significant computational expertise and resources.
