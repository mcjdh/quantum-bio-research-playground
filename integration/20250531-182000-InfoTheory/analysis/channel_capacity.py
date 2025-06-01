import numpy as np

def shannon_entropy(p_vector):
    """Calculates Shannon entropy for a probability vector."""
    p_vector = np.array(p_vector)
    p_vector = p_vector[p_vector > 0] # Avoid log(0)
    return -np.sum(p_vector * np.log2(p_vector))

def classical_channel_capacity_binary_symmetric(p_error):
    """
    Calculates capacity of a Binary Symmetric Channel (BSC).
    C = 1 - H(p_error), where H is the binary entropy function.
    """
    if p_error < 0 or p_error > 1:
        raise ValueError("Error probability must be between 0 and 1.")
    if p_error == 0 or p_error == 1:
        return 1.0
    return 1.0 - (-p_error * np.log2(p_error) - (1 - p_error) * np.log2(1 - p_error))

def von_neumann_entropy(density_matrix):
    """Calculates Von Neumann entropy for a density matrix."""
    rho = np.array(density_matrix)
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-9] # Avoid log(0) for zero eigenvalues
    return -np.sum(eigenvalues * np.log2(eigenvalues))

def holevo_quantity(p_states, density_matrices):
    """
    Calculates the Holevo quantity for an ensemble of quantum states.
    χ = S(Σ_x p_x ρ_x) - Σ_x p_x S(ρ_x)
    p_states: list of probabilities p_x
    density_matrices: list of density matrices ρ_x
    """
    if not np.isclose(sum(p_states), 1.0):
        raise ValueError("Probabilities must sum to 1.")
    if len(p_states) != len(density_matrices):
        raise ValueError("Number of probabilities must match number of density matrices.")

    avg_rho = np.zeros_like(density_matrices[0], dtype=complex)
    for p, rho in zip(p_states, density_matrices):
        avg_rho += p * np.array(rho)

    s_avg_rho = von_neumann_entropy(avg_rho)

    sum_s_rho_x = 0
    for p, rho in zip(p_states, density_matrices):
        sum_s_rho_x += p * von_neumann_entropy(rho)

    return s_avg_rho - sum_s_rho_x

if __name__ == '__main__':
    # Example Usage: Classical Binary Symmetric Channel
    p_error_classical = 0.1
    capacity_bsc = classical_channel_capacity_binary_symmetric(p_error_classical)
    print(f"Classical BSC Capacity (p_error={p_error_classical}): {capacity_bsc:.4f} bits")

    p_error_classical_noisy = 0.5
    capacity_bsc_noisy = classical_channel_capacity_binary_symmetric(p_error_classical_noisy)
    print(f"Classical BSC Capacity (p_error={p_error_classical_noisy}): {capacity_bsc_noisy:.4f} bits (completely noisy)")

    # Example Usage: Quantum Channel (simplified Holevo quantity example)
    # Consider a quantum channel that transmits one of two non-orthogonal states
    # |0> or |+> = (|0> + |1>)/sqrt(2) with equal probability (p=0.5 each)

    # Density matrix for |0>: [[1, 0], [0, 0]]
    rho0 = np.array([[1, 0], [0, 0]])
    # Density matrix for |+>: [[0.5, 0.5], [0.5, 0.5]]
    rho_plus = np.array([[0.5, 0.5], [0.5, 0.5]])

    states = [rho0, rho_plus]
    probabilities = [0.5, 0.5]

    holevo_chi = holevo_quantity(probabilities, states)
    print(f"Holevo quantity for example quantum states: {holevo_chi:.4f} bits")

    # Example: Two orthogonal states |0> and |1>
    rho1 = np.array([[0,0],[0,1]])
    states_orthogonal = [rho0, rho1]
    holevo_chi_orthogonal = holevo_quantity(probabilities, states_orthogonal)
    print(f"Holevo quantity for orthogonal states |0>, |1>: {holevo_chi_orthogonal:.4f} bits (should be 1 bit for p=0.5)")

    # Example: States for a trine ensemble (symmetric, 120 degrees apart on Bloch sphere)
    # For simplicity, we'll use pre-calculated density matrices for states that might
    # lead to a Holevo quantity greater than classical capacity for certain encodings.
    # These are illustrative and not directly from a biological system.
    psi_0 = np.array([1, 0]) # |0>
    psi_1 = np.array([-1/2, np.sqrt(3)/2]) # e^{i 2pi/3} |0> + ...
    psi_2 = np.array([-1/2, -np.sqrt(3)/2])# e^{i 4pi/3} |0> + ...

    # This is not correct for trine states, need to use density matrices
    # rho_trine_0 = np.outer(psi_0, psi_0.conj())
    # rho_trine_1 = np.outer(psi_1, psi_1.conj())
    # rho_trine_2 = np.outer(psi_2, psi_2.conj())
    # states_trine = [rho_trine_0, rho_trine_1, rho_trine_2]
    # prob_trine = [1/3, 1/3, 1/3]
    # holevo_trine = holevo_quantity(prob_trine, states_trine)
    # print(f"Holevo quantity for trine states: {holevo_trine:.4f} bits")
    # The trine example above is a bit complex for a quick demo without proper state defs.
    # The key is that Holevo quantity sets the upper bound on accessible information.

    print("\nNote: This script provides basic functions. Real quantum channel capacity calculations")
    print("can be more complex, involving optimization over input states and POVMs.")
