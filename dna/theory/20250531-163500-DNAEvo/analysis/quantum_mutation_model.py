import random
import statistics # For calculating mean

# --- Constants and Helper Data ---
BASES = ['A', 'T', 'C', 'G']
TRANSITIONS = {
    'A': 'G', 'G': 'A',  # Purines
    'C': 'T', 'T': 'C'   # Pyrimidines
}
# For a given base, what are its transversion options
TRANSVERSIONS = {
    'A': ['C', 'T'], 'G': ['C', 'T'],
    'C': ['A', 'G'], 'T': ['A', 'G']
}

# --- 1. DNA Representation (Implicit: strings) ---

# --- 2. Initialization ---
def create_random_sequence(length):
    """Creates a random DNA sequence of a given length."""
    return "".join(random.choice(BASES) for _ in range(length))

def initialize_population(population_size, sequence_length):
    """Creates a population of random DNA sequences."""
    return [create_random_sequence(sequence_length) for _ in range(population_size)]

# --- 3. Classical Mutation ---
def classical_mutate(sequence, mutation_rate):
    """
    Applies classical mutation to a sequence.
    For each base, with mutation_rate probability, change it to one of the other 3 bases randomly.
    """
    mutated_sequence = list(sequence)
    for i in range(len(mutated_sequence)):
        if random.random() < mutation_rate:
            original_base = mutated_sequence[i]
            possible_mutations = [b for b in BASES if b != original_base]
            mutated_sequence[i] = random.choice(possible_mutations)
    return "".join(mutated_sequence)

# --- 4. Quantum-Inspired Mutation ---
def quantum_mutate(sequence, mutation_rate, transition_bias):
    """
    Applies quantum-inspired mutation to a sequence.
    - For each base, with mutation_rate probability, induce a mutation.
    - A mutated base has a transition_bias probability of being a transition (A <-> G, C <-> T)
      and (1 - transition_bias) of being a transversion, distributed among the two possible transversions.
    """
    mutated_sequence = list(sequence)
    for i in range(len(mutated_sequence)):
        if random.random() < mutation_rate:
            original_base = mutated_sequence[i]

            if random.random() < transition_bias:
                # Transition
                mutated_sequence[i] = TRANSITIONS[original_base]
            else:
                # Transversion
                mutated_sequence[i] = random.choice(TRANSVERSIONS[original_base])
    return "".join(mutated_sequence)

# --- 5. Fitness Function ---
def calculate_fitness(sequence, target_sequence):
    """
    Calculates the fitness of a sequence by comparing it to a target sequence.
    Fitness is the number of matching bases.
    """
    return sum(1 for i in range(len(sequence)) if sequence[i] == target_sequence[i])

# --- 6. Evolutionary Loop ---
def run_evolution(population_size, sequence_length, generations, target_sequence,
                  classical_mutation_rate, quantum_mutation_rate, transition_bias,
                  use_quantum_mutations=True, trial_id=0, quiet=False):
    """
    Runs the evolutionary simulation.
    Set quiet=True to suppress per-generation logging for multi-trial runs.
    """
    population = initialize_population(population_size, sequence_length)
    fitness_history_avg = []
    fitness_history_max = []

    for gen in range(generations):
        fitness_scores = [calculate_fitness(ind, target_sequence) for ind in population]
        avg_fitness = sum(fitness_scores) / population_size
        max_fitness = max(fitness_scores)
        fitness_history_avg.append(avg_fitness)
        fitness_history_max.append(max_fitness)

        sorted_population = [ind for _, ind in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]
        num_parents = population_size // 2
        parents = sorted_population[:num_parents]

        offspring_population = []
        if not parents: # Handle case where no parents are selected (e.g. all fitness 0)
            parents = [create_random_sequence(sequence_length) for _ in range(num_parents if num_parents > 0 else 1)]


        for i in range(num_parents):
            offspring_population.append(parents[i])
            offspring_population.append(parents[i])

        if population_size % 2 != 0 and parents:
             offspring_population.append(parents[0])

        # Ensure offspring population is full in case num_parents was 0
        while len(offspring_population) < population_size:
            offspring_population.append(create_random_sequence(sequence_length))


        mutated_offspring = []
        for individual in offspring_population:
            mutated_ind = classical_mutate(individual, classical_mutation_rate)
            if use_quantum_mutations:
                mutated_ind = quantum_mutate(mutated_ind, quantum_mutation_rate, transition_bias)
            mutated_offspring.append(mutated_ind)

        population = mutated_offspring

        if not quiet and (gen % (generations // 10 if generations >=10 else 1) == 0 or gen == generations -1) :
            print(f"Trial {trial_id} - Gen {gen}: Max Fitness = {max_fitness}, Avg Fitness = {avg_fitness:.2f} ({'Q' if use_quantum_mutations else 'C'})")

        if max_fitness == sequence_length:
            if not quiet:
                print(f"Trial {trial_id} - Target sequence achieved at generation {gen}! ({'Q' if use_quantum_mutations else 'C'})")
            # Fill remaining history if ended early
            for _ in range(generations - 1 - gen):
                fitness_history_avg.append(avg_fitness)
                fitness_history_max.append(max_fitness)
            break

    return fitness_history_avg, fitness_history_max

# --- 7. Main Simulation ---
if __name__ == "__main__":
    # Parameters
    POPULATION_SIZE = 100
    SEQUENCE_LENGTH = 50
    GENERATIONS = 100 # Reduced for brevity in multi-trial, can be increased
    CLASSICAL_MUTATION_RATE = 0.05
    QUANTUM_MUTATION_RATE = 0.05
    TRANSITION_BIAS = 0.75
    NUM_TRIALS = 5 # Number of trials to average

    print(f"Running {NUM_TRIALS} trials for each scenario.")
    print(f"Params: Pop={POPULATION_SIZE}, SeqLen={SEQUENCE_LENGTH}, Gens={GENERATIONS}, CMRate={CLASSICAL_MUTATION_RATE}, QMRate={QUANTUM_MUTATION_RATE}, TBias={TRANSITION_BIAS}")
    print(f"Max possible fitness: {SEQUENCE_LENGTH}\n")

    all_classical_final_max_fitness = []
    all_classical_final_avg_fitness = []
    all_quantum_final_max_fitness = []
    all_quantum_final_avg_fitness = []

    for i in range(NUM_TRIALS):
        print(f"--- Trial {i+1} of {NUM_TRIALS} ---")
        TARGET_SEQUENCE = create_random_sequence(SEQUENCE_LENGTH)
        print(f"Target for Trial {i+1}: {TARGET_SEQUENCE}")

        # Run with Classical Mutations Only
        classical_avg_hist, classical_max_hist = run_evolution(
            population_size=POPULATION_SIZE, sequence_length=SEQUENCE_LENGTH, generations=GENERATIONS,
            target_sequence=TARGET_SEQUENCE, classical_mutation_rate=CLASSICAL_MUTATION_RATE,
            quantum_mutation_rate=0, transition_bias=TRANSITION_BIAS, use_quantum_mutations=False,
            trial_id=i+1, quiet=True # Suppress per-generation logs for trials
        )
        all_classical_final_max_fitness.append(classical_max_hist[-1])
        all_classical_final_avg_fitness.append(classical_avg_hist[-1])
        print(f"Trial {i+1} Classical: Final Max Fitness = {classical_max_hist[-1]}, Final Avg Fitness = {classical_avg_hist[-1]:.2f}")

        # Run with Classical + Quantum Mutations
        quantum_avg_hist, quantum_max_hist = run_evolution(
            population_size=POPULATION_SIZE, sequence_length=SEQUENCE_LENGTH, generations=GENERATIONS,
            target_sequence=TARGET_SEQUENCE, classical_mutation_rate=CLASSICAL_MUTATION_RATE,
            quantum_mutation_rate=QUANTUM_MUTATION_RATE, transition_bias=TRANSITION_BIAS, use_quantum_mutations=True,
            trial_id=i+1, quiet=True # Suppress per-generation logs for trials
        )
        all_quantum_final_max_fitness.append(quantum_max_hist[-1])
        all_quantum_final_avg_fitness.append(quantum_avg_hist[-1])
        print(f"Trial {i+1} Quantum:   Final Max Fitness = {quantum_max_hist[-1]}, Final Avg Fitness = {quantum_avg_hist[-1]:.2f}")
        print("-" * 30)

    # Calculate Averages
    avg_classical_max_f = statistics.mean(all_classical_final_max_fitness) if all_classical_final_max_fitness else 0
    avg_classical_avg_f = statistics.mean(all_classical_final_avg_fitness) if all_classical_final_avg_fitness else 0
    avg_quantum_max_f = statistics.mean(all_quantum_final_max_fitness) if all_quantum_final_max_fitness else 0
    avg_quantum_avg_f = statistics.mean(all_quantum_final_avg_fitness) if all_quantum_final_avg_fitness else 0

    print("\n--- Averaged Results Over All Trials ---")
    print(f"Classical Model (Avg over {NUM_TRIALS} trials):")
    print(f"  Average Final Max Fitness: {avg_classical_max_f:.2f}")
    print(f"  Average Final Avg Fitness: {avg_classical_avg_f:.2f}")

    print(f"\nQuantum Model (Avg over {NUM_TRIALS} trials):")
    print(f"  Average Final Max Fitness: {avg_quantum_max_f:.2f}")
    print(f"  Average Final Avg Fitness: {avg_quantum_avg_f:.2f}")

    print("\n--- Overall Comparison ---")
    if avg_quantum_max_f > avg_classical_max_f:
        print("Quantum model achieved a higher average maximum fitness.")
    elif avg_classical_max_f > avg_quantum_max_f:
        print("Classical model achieved a higher average maximum fitness.")
    else:
        print("Both models achieved a similar average maximum fitness.")

    if avg_quantum_avg_f > avg_classical_avg_f:
        print("Quantum model achieved a higher average 'average population' fitness.")
    elif avg_classical_avg_f > avg_quantum_avg_f:
        print("Classical model achieved a higher average 'average population' fitness.")
    else:
        print("Both models achieved a similar average 'average population' fitness.")

    print(f"\nNote: These results are based on {NUM_TRIALS} trials with SEQUENCE_LENGTH={SEQUENCE_LENGTH} and GENERATIONS={GENERATIONS}.")
    print("Evolution is stochastic. More trials and longer runs might be needed for robust conclusions.")
    print("Target sequence length (max possible fitness):", SEQUENCE_LENGTH)
