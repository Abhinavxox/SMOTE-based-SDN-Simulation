import json
import heapq

class OptimalPathFinder:
    def __init__(self, loss_file, delay_file):
        with open(loss_file, 'r') as file:
            self.loss_matrix = json.load(file)
        with open(delay_file, 'r') as file:
            self.delay_matrix = json.load(file)

    def find_optimal_path(self, source, dest):
        # Initialize the distance and previous node dictionaries
        distance = {}
        previous = {}
        for switch in self.loss_matrix.keys():
            distance[switch] = float('inf')
            previous[switch] = None
        distance[source] = 0

        # Initialize the priority queue with the source node
        queue = [(0, source)]

        # Loop until the queue is empty
        while queue:
            # Get the node with the smallest distance
            current_distance, current_node = heapq.heappop(queue)

            # If we've reached the destination, stop searching
            if current_node == dest:
                break

            # Loop through the neighbors of the current node
            for neighbor, loss in self.loss_matrix[current_node].items():
                # Calculate the new distance to the neighbor
                new_distance = distance[current_node] + loss + self.delay_matrix[current_node][neighbor]

                # If the new distance is smaller than the current distance, update the distance and previous node
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = current_node

                    # Add the neighbor to the priority queue
                    heapq.heappush(queue, (new_distance, neighbor))

        # Build the optimal path
        path = []
        current_node = dest
        while current_node != source:
            path.insert(0, current_node)
            current_node = previous[current_node]
        path.insert(0, source)

        # Calculate the total loss and delay of the optimal path
        total_loss = 0
        total_delay = 0
        for i in range(len(path) - 1):
            total_loss += self.loss_matrix[path[i]][path[i+1]]
            total_delay += self.delay_matrix[path[i]][path[i+1]]

        # Print the optimal path and its associated loss and delay metrics
        print(f"Optimal path from {source} to {dest}: {' -> '.join(path)}")
        print(f"Total loss: {total_loss * 100}%")
        print(f"Total delay: {total_delay * 100}%")

if __name__ == "__main__":
    loss_file = "./out/loss_matrix.json"  # Replace with your loss matrix file path
    delay_file = "./out/delay_matrix.json"  # Replace with your delay matrix file path
    finder = OptimalPathFinder(loss_file, delay_file)

    # Find the optimal path from h1 to h4
    finder.find_optimal_path('h1', 'h4')