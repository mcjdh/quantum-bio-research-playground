# Key Formulas for Information Theory in Quantum Biology

## Classical Information Theory

**Shannon Entropy:**
For a discrete random variable X with probability distribution p(x):
H(X) = - Σ_x p(x) log_2 p(x)

**Mutual Information:**
I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y)

**Channel Capacity (Classical):**
C = max_{p(x)} I(X;Y)

## Quantum Information Theory

**Von Neumann Entropy:**
For a quantum state described by a density matrix ρ:
S(ρ) = -Tr(ρ log_2 ρ)

**Holevo Bound (χ quantity):**
For an ensemble of quantum states {ρ_x} prepared with probabilities {p_x}:
χ = S(Σ_x p_x ρ_x) - Σ_x p_x S(ρ_x)
The Holevo bound states that the accessible information I(X;Y) <= χ.

**Quantum Channel Capacity:**
Q = max_{p_x, ρ_x} χ
(This is a simplification; actual calculation can be complex, e.g., LSD theorem)
