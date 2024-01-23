graph = {
  "nodes": [
    {
      "type": "switch",
      "name": "s1",
      "mac": "00:00:00:00:00:01",
      "connections": [
        {
          "type": "host",
          "name": "h1",
          "mac": "6a:01:2c:29:3f:db",
          "port": 3,
          "delay": "19.978"
        },
        {
          "type": "switch",
          "name": "s2",
          "mac": "00:00:00:00:00:02",
          "port": 1,
          "delay": "5.123"
        },
        {
          "type": "switch",
          "name": "s3",
          "mac": "00:00:00:00:00:03",
          "port": 2,
          "delay": "10.456"
        }
      ]
    },
    {
      "type": "switch",
      "name": "s2",
      "mac": "00:00:00:00:00:04",
      "connections": [
        {
          "type": "host",
          "name": "h2",
          "mac": "1a:e6:78:40:f0:3e",
          "port": 2,
          "delay": "14.827"
        },
        {
          "type": "switch",
          "name": "s1",
          "mac": "00:00:00:00:00:05",
          "port": 1,
          "delay": "4.591"
        },
        {
          "type": "switch",
          "name": "s4",
          "mac": "00:00:00:00:00:06",
          "port": 3,
          "delay": "3.256"
        }
      ]
    },
    {
      "type": "switch",
      "name": "s3",
      "mac": "00:00:00:00:00:07",
      "connections": [
        {
          "type": "host",
          "name": "h3",
          "mac": "4e:97:00:3e:b1:91",
          "port": 3,
          "delay": "7.123"
        },
        {
          "type": "switch",
          "name": "s1",
          "mac": "00:00:00:00:00:08",
          "port": 1,
          "delay": "9.456"
        },
        {
          "type": "switch",
          "name": "s4",
          "mac": "00:00:00:00:00:09",
          "port": 2,
          "delay": "8.789"
        }
      ]
    },
    {
      "type": "switch",
      "name": "s4",
      "mac": "00:00:00:00:00:10",
      "connections": [
        {
          "type": "host",
          "name": "h4",
          "mac": "86:aa:c3:64:d4:cd",
          "port": 2,
          "delay": "2.345"
        },
        {
          "type": "switch",
          "name": "s2",
          "mac": "00:00:00:00:00:11",
          "port": 1,
          "delay": "1.678"
        },
        {
          "type": "switch",
          "name": "s3",
          "mac": "00:00:00:00:00:12",
          "port": 3,
          "delay": "3.012"
        }
      ]
    }
  ]
}


delay_matrix = {
    's1': {'h1': 0.0813, 's2': 0.0916, 's3': 0.0946},
    's2': {'h2': 0.023, 's1': 0.0608, 's4': 0.049},
    's3': {'h3': 0.0789, 's1': 0.0854, 's4': 0.0125},
    's4': {'h4': 0.0027, 's2': 0.0023, 's3': 0.0141}
}

loss_matrix = {
    's1': {'h1': 0.0558, 's2': 0.0161, 's3': 0.0673},
    's2': {'h2': 0.0979, 's1': 0.0417, 's4': 0.0057},
    's3': {'h3': 0.0797, 's1': 0.095, 's4': 0.01},
    's4': {'h4': 0.0679, 's2': 0.0143, 's3': 0.0472}
}

start = 'h1'
end = 'h4'

import heapq
#optimal qoe pathfinder using loss and delay matrix

def find_optimal_path(source, dest):
    # Initialize the distance and previous node dictionaries
    distance = {}
    previous = {}
    for switch in loss_matrix.keys():
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
        for neighbor, delay in delay_matrix[current_node].items():
            if neighbor not in loss_matrix:
                continue  # Skip if the neighbor is not a switch
            if current_node not in loss_matrix[neighbor]:
                continue  # Skip if there is no corresponding loss value for the neighbor
            # Calculate the new distance to the neighbor
            new_distance = distance[current_node] + loss_matrix[neighbor][current_node] + delay

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
        total_loss += loss_matrix[path[i]][path[i+1]]
        total_delay += delay_matrix[path[i]][path[i+1]]

    # Print the optimal path and its associated loss and delay metrics
    print(f"Optimal path from {source} to {dest}: {' -> '.join(path)}")
    print(f"Total loss: {total_loss * 100}%")
    print(f"Total delay: {total_delay * 100}%")

if __name__ == '__main__':
    find_optimal_path(start, end)