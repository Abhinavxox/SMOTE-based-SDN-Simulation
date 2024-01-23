import json
import random

class LinkDelayCollector:
    def __init__(self, topology_file):
        self.delay_matrix = {}
        self.load_delay_matrix(topology_file)

    def load_delay_matrix(self, topology_file):
        with open(topology_file, 'r') as file:
            topology_data = json.load(file)

        for node in topology_data['nodes']:
            if node['type'] == 'switch':
                self.delay_matrix[node['name']] = {}

        for node in topology_data['nodes']:
            if node['type'] == 'switch':
                switch_name = node['name']
                for connection in node.get('connections', []):
                    dest_name = connection['name']
                    self.delay_matrix[switch_name][dest_name] = 0.0

    def simulate_delay(self):
        for switch, connections in self.delay_matrix.items():
            for dest, delay in connections.items():
                # Simulate delay with a random ratio between 0% and 10%
                self.delay_matrix[switch][dest] = round(random.uniform(0, 0.1), 4)

    def save_delay_matrix(self, output_file):
        with open(output_file, 'w') as file:
            json.dump(self.delay_matrix, file, indent=4)

    def print_delay_matrix(self):
        print("Delay Matrix:")
        for switch, connections in self.delay_matrix.items():
            for dest, delay in connections.items():
                print(f"  {switch} -> {dest}: {delay * 100}%")

if __name__ == "__main__":
    topology_file = "./out/data.json"  # Replace with your JSON file path
    collector = LinkDelayCollector(topology_file)

    # Simulate delay
    collector.simulate_delay()

    # Save the delay matrix to a JSON file
    output_file = "./out/delay_matrix.json"
    collector.save_delay_matrix(output_file)