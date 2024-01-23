import json
import random

class LinkLossCollector:
    def __init__(self, topology_file):
        self.loss_matrix = {}
        self.load_topology(topology_file)

    def load_topology(self, topology_file):
        with open(topology_file, 'r') as file:
            topology_data = json.load(file)

        for node in topology_data['nodes']:
            if node['type'] == 'switch':
                self.loss_matrix[node['name']] = {}

        for node in topology_data['nodes']:
            if node['type'] == 'switch':
                switch_name = node['name']
                for connection in node.get('connections', []):
                    dest_name = connection['name']
                    self.loss_matrix[switch_name][dest_name] = 0.0

    def simulate_packet_loss(self):
        for switch, connections in self.loss_matrix.items():
            for dest, loss in connections.items():
                # Simulate packet loss with a random ratio between 0% and 10%
                self.loss_matrix[switch][dest] = round(random.uniform(0, 0.1), 4)

    def save_loss_matrix(self, output_file):
        with open(output_file, 'w') as file:
            json.dump(self.loss_matrix, file, indent=4)

    def print_loss_matrix(self):
        print("Loss Matrix:")
        for switch, connections in self.loss_matrix.items():
            for dest, loss in connections.items():
                print(f"  {switch} -> {dest}: {loss * 100}%")

if __name__ == "__main__":
    topology_file = "./out/data.json"  # Replace with your JSON file path
    collector = LinkLossCollector(topology_file)

    # Simulate packet loss
    collector.simulate_packet_loss()

    # Save the loss matrix to a JSON file
    output_file = "./out/loss_matrix.json"
    collector.save_loss_matrix(output_file)