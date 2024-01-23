import requests
from requests.auth import HTTPBasicAuth

def get_topology_information(odl_ip, odl_port, odl_username, odl_password):
    url = f'http://{odl_ip}:{odl_port}/restconf/operational/network-topology:network-topology'
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth(odl_username, odl_password)

    try:
        response = requests.get(url, headers=headers, auth=auth, timeout=5)
        response.raise_for_status()

        data = response.json()
        return data.get('network-topology', {}).get('topology', [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve topology information. Error: {e}")
        return None

def print_topology_information(topology):
    for node in topology:
        print(f"Node: {node.get('node-id')}")
        for link in node.get('link', []):
            print(f"  Link: {link.get('link-id')}")
            print(f"    Source: {link.get('source', {}).get('source-node')} ({link.get('source', {}).get('source-tp')})")
            print(f"    Destination: {link.get('destination', {}).get('dest-node')} ({link.get('destination', {}).get('dest-tp')})")
            print()

if __name__ == '__main__':
    odl_ip = '127.0.0.1'  # Replace with your ODL controller IP
    odl_port = '8101'  # Replace with your ODL controller port
    odl_username = 'admin'  # Replace with your ODL username
    odl_password = 'admin'  # Replace with your ODL password

    topology_information = get_topology_information(odl_ip, odl_port, odl_username, odl_password)

    if topology_information:
        print_topology_information(topology_information)
