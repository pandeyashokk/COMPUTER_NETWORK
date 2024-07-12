import heapq

def dijkstra(graph, start):
    # Priority queue to hold the vertices to explore
    priority_queue = []
    # Push the starting node with distance 0
    heapq.heappush(priority_queue, (0, start))
    
    # Dictionary to hold the shortest distance to each node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while priority_queue:
        # Pop the vertex with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # Check if the popped node's distance is greater than the known shortest distance
        if current_distance > distances[current_node]:
            continue

        # Explore the neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

start_node = 'A'
shortest_distances = dijkstra(graph, start_node)
print("Shortest distances from node", start_node, ":", shortest_distances)
