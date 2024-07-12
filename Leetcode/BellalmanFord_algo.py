def bellman_ford(graph, start):
    # Step 1: Initialize distances from start to all other nodes as infinity
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Step 2: Relax all edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node].items():
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight

    # Step 3: Check for negative-weight cycles
    for node in graph:
        for neighbor, weight in graph[node].items():
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative-weight cycle")

    return distances

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'
shortest_distances = bellman_ford(graph, start_node)
print("Shortest distances from node", start_node, ":", shortest_distances)
