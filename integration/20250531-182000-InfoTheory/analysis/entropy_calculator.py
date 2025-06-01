import numpy as np

def shannon_entropy(p_vector):
    """
    Calculates Shannon entropy for a probability distribution.
    H(X) = - Σ_x p(x) log_2 p(x)
    Args:
        p_vector (list or np.array): A list of probabilities.
    Returns:
        float: The Shannon entropy in bits.
    """
    p_vector = np.array(p_vector)
    if not np.isclose(np.sum(p_vector), 1.0):
        raise ValueError("Probabilities must sum to 1.")
    if np.any(p_vector < 0) or np.any(p_vector > 1):
        raise ValueError("Probabilities must be between 0 and 1.")

    p_vector = p_vector[p_vector > 1e-9] # Avoid log(0) for zero probabilities
    return -np.sum(p_vector * np.log2(p_vector))

def von_neumann_entropy(density_matrix):
    """
    Calculates Von Neumann entropy for a quantum state described by a density matrix.
    S(ρ) = -Tr(ρ log_2 ρ)
    Args:
        density_matrix (np.array): A density matrix.
    Returns:
        float: The Von Neumann entropy in bits.
    """
    rho = np.array(density_matrix, dtype=complex)
    # Check if it's a valid density matrix (Hermitian, trace 1, positive semi-definite)
    if not np.allclose(rho, rho.conj().T):
        raise ValueError("Density matrix must be Hermitian.")
    if not np.isclose(np.trace(rho), 1.0):
        raise ValueError("Density matrix must have trace 1.")

    eigenvalues = np.linalg.eigvalsh(rho) # eigvalsh for Hermitian matrices
    if np.any(eigenvalues < -1e-9): # Check for negative eigenvalues (within tolerance)
        # Small negative eigenvalues can occur due to numerical precision for zero eigenvalues.
        # Filter them if they are very close to zero.
        if not np.all(eigenvalues[eigenvalues < -1e-9] > -1e-6 ): # if any are significantly negative
             raise ValueError("Density matrix must be positive semi-definite (no significant negative eigenvalues).")
        eigenvalues[eigenvalues < 0] = 0 # Set small negatives to zero for log calculation

    eigenvalues = eigenvalues[eigenvalues > 1e-9] # Avoid log(0) for zero eigenvalues
    if len(eigenvalues) == 0: # If all eigenvalues were zero (e.g. for a zero matrix, though trace should be 1)
        return 0.0
    return -np.sum(eigenvalues * np.log2(eigenvalues))

if __name__ == '__main__':
    # Example Usage: Shannon Entropy
    classical_dist_uniform = [0.25, 0.25, 0.25, 0.25]
    h_uniform = shannon_entropy(classical_dist_uniform)
    print(f"Shannon Entropy for uniform distribution {classical_dist_uniform}: {h_uniform:.4f} bits (should be 2)")

    classical_dist_skewed = [0.7, 0.1, 0.1, 0.1]
    h_skewed = shannon_entropy(classical_dist_skewed)
    print(f"Shannon Entropy for skewed distribution {classical_dist_skewed}: {h_skewed:.4f} bits")

    classical_dist_certain = [1.0, 0.0, 0.0, 0.0]
    h_certain = shannon_entropy(classical_dist_certain)
    print(f"Shannon Entropy for certain distribution {classical_dist_certain}: {h_certain:.4f} bits (should be 0)")

    print("\n---")

    # Example Usage: Von Neumann Entropy
    # Pure state |0>: rho = [[1, 0], [0, 0]]
    rho_pure_0 = np.array([[1, 0], [0, 0]])
    s_pure_0 = von_neumann_entropy(rho_pure_0)
    print(f"Von Neumann Entropy for pure state |0> (rho=[[1,0],[0,0]]): {s_pure_0:.4f} bits (should be 0)")

    # Maximally mixed state for a qubit: rho = 0.5 * Identity
    rho_mixed_qubit = np.array([[0.5, 0], [0, 0.5]])
    s_mixed_qubit = von_neumann_entropy(rho_mixed_qubit)
    print(f"Von Neumann Entropy for maximally mixed qubit (rho=[[0.5,0],[0,0.5]]): {s_mixed_qubit:.4f} bits (should be 1)")

    # Another pure state |+>: rho = [[0.5, 0.5], [0.5, 0.5]]
    rho_plus = np.array([[0.5, 0.5], [0.5, 0.5]])
    s_plus = von_neumann_entropy(rho_plus)
    print(f"Von Neumann Entropy for pure state |+> (rho=[[0.5,0.5],[0.5,0.5]]): {s_plus:.4f} bits (should be ~0)")

    # A mixed state (e.g., from partial trace or noise)
    # Example: 75% |0><0| + 25% |1><1|
    rho_partially_mixed = np.array([[0.75, 0], [0, 0.25]])
    s_partially_mixed = von_neumann_entropy(rho_partially_mixed)
    print(f"Von Neumann Entropy for rho=[[0.75,0],[0,0.25]]: {s_partially_mixed:.4f} bits (should be H(0.75, 0.25))")
    # H(0.75, 0.25) = -(0.75 log2 0.75 + 0.25 log2 0.25) = 0.8113

    # Example of a qutrit state
    rho_qutrit_mixed = np.array([[0.5, 0, 0], [0, 0.3, 0], [0, 0, 0.2]])
    s_qutrit_mixed = von_neumann_entropy(rho_qutrit_mixed)
    print(f"Von Neumann Entropy for qutrit rho=diag(0.5,0.3,0.2): {s_qutrit_mixed:.4f} bits")
    # H(0.5, 0.3, 0.2) = 1.4855

    print("\nConsider a hypothetical biological process:")
    # Initial state (e.g., a well-defined quantum state, low entropy)
    rho_initial = np.array([[0.9, 0.1j], [-0.1j, 0.1]]) # Example slightly mixed state
    # Ensure it's valid (Hermitian, trace 1 - this one is not trace 1 as written)
    # Let's make it valid:
    rho_initial = np.array([[0.9, 0.1j], [-0.1j, 0.1]])
    # Normalize trace if not 1, for demonstration (real systems should have trace 1 states)
    # This is actually not a good state, let's use a better one
    # rho_initial = np.array([[0.9, 0.05j * np.sqrt(2)], [-0.05j * np.sqrt(2), 0.1]]) # Still not guaranteed PSD

    # Let's use a state that is definitely PSD and trace 1
    # Start with a pure state and mix it slightly
    psi_initial = np.array([np.sqrt(0.9), np.sqrt(0.1) * 1j])
    rho_initial_pure = np.outer(psi_initial, psi_initial.conj())
    # Mix with identity
    epsilon = 0.05
    rho_initial = (1-epsilon) * rho_initial_pure + epsilon * np.eye(2)/2

    s_initial = von_neumann_entropy(rho_initial)
    print(f"S(initial_state): {s_initial:.4f} bits")

    # Final state (e.g., after decoherence or interaction, higher entropy)
    rho_final = np.array([[0.6, 0], [0, 0.4]]) # Decohered to a diagonal state
    s_final = von_neumann_entropy(rho_final)
    print(f"S(final_state - decohered): {s_final:.4f} bits")
    print(f"Change in entropy: {s_final - s_initial:.4f} bits")
