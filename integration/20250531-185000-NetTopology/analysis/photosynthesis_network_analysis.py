import json

# Network definitions for 7-node systems based on photosynthesis_simulation_results.txt
# Nodes are 0 to 6.
# Excitation starts at node 0, trap at node 6 (N-1 for 7 nodes).

def get_linear_chain_edges(n=7):
    """Generates edges for a linear chain of n nodes."""
    edges = []
    for i in range(n - 1):
        edges.append((i, i + 1))
    return edges

def get_ring_edges(n=7):
    """Generates edges for a ring of n nodes."""
    edges = []
    for i in range(n - 1):
        edges.append((i, i + 1))
    edges.append((n - 1, 0)) # Close the ring
    return edges

def get_star_center_0_edges(n=7):
    """Generates edges for a star network with node 0 as the center."""
    if n <= 1:
        return []
    edges = []
    for i in range(1, n):
        edges.append((0, i))
    return edges

def get_star_center_mid_edges(n=7):
    """Generates edges for a star network with the middle node as the center."""
    if n <= 1:
        return []
    edges = []
    center_node = (n - 1) // 2
    for i in range(n):
        if i == center_node:
            continue
        edges.append((center_node, i))
    return edges

def get_adjacency_matrix(nodes, edges):
    """Creates an adjacency matrix from a list of nodes and edges."""
    adj_matrix = [[0] * len(nodes) for _ in range(len(nodes))]
    node_to_index = {node: i for i, node in enumerate(nodes)}
    for u, v in edges:
        u_idx, v_idx = node_to_index[u], node_to_index[v]
        adj_matrix[u_idx][v_idx] = 1
        adj_matrix[v_idx][u_idx] = 1 # Assuming undirected graph
    return adj_matrix

def get_degree_distribution(nodes, edges):
    """Calculates the degree of each node and the distribution."""
    degrees = {node: 0 for node in nodes}
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1

    dist = {}
    for degree in degrees.values():
        dist[degree] = dist.get(degree, 0) + 1
    return degrees, dist

def main():
    num_nodes = 7
    nodes = list(range(num_nodes))

    topologies = {
        "linear_chain": get_linear_chain_edges(num_nodes),
        "ring": get_ring_edges(num_nodes),
        "star_center_0": get_star_center_0_edges(num_nodes),
        "star_center_mid": get_star_center_mid_edges(num_nodes)
    }

    analysis_results = {}

    for name, edges in topologies.items():
        adj_matrix = get_adjacency_matrix(nodes, edges)
        degrees, deg_dist = get_degree_distribution(nodes, edges)
        analysis_results[name] = {
            "nodes": nodes,
            "edges": edges,
            "adjacency_matrix": adj_matrix,
            "degrees": degrees,
            "degree_distribution": deg_dist,
            "num_edges": len(edges)
        }
        print(f"--- {name} ---")
        print(f"Nodes: {nodes}")
        print(f"Edges: {edges}")
        print(f"Number of Edges: {len(edges)}")
        print(f"Degrees: {degrees}")
        print(f"Degree Distribution: {deg_dist}")
        # print(f"Adjacency Matrix:")
        # for row in adj_matrix:
        #     print(row)
        print("\n")

    # Store results in a JSON file for persistence
    output_path = "integration/20250531-185000-NetTopology/analysis/photosynthesis_topology_analysis.json"
    # Ensure the directory exists (this should be handled by the agent's environment or initial setup)
    # For now, assume it exists or this is run from a context where it can be created.

    # To make this runnable in the subtask, we'll just print the JSON content
    # instead of writing to a file that might not be easily accessible later.
    # In a real scenario, we'd write to `output_path`.
    print("--- JSON Output for analysis_results ---")
    # Creating the full path for the output file
    # The subtask environment should handle directory creation if it doesn't exist.
    # However, standard practice is to ensure directories are created before writing.
    # For this subtask, we will first try to ensure the directory exists.
    # If not, the file write will be relative to the current working directory of the script.

    # The task is to create the script, not run it and write its output here.
    # The content below would be for running it.
    # In this case, we want to print the JSON to stdout for capture.
    print(json.dumps(analysis_results, indent=2))

    # This would be for writing to a file:
    # with open(output_path, 'w') as f:
    #     json.dump(analysis_results, f, indent=2)
    # print(f"Analysis results saved to {output_path}")


if __name__ == "__main__":
    # This part is more for local execution.
    # The agent will likely call functions from this script or run it and capture stdout.
    # For now, the main() function just prints.
    main()
