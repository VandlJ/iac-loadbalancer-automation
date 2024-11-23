import json
import os

# Function to load JSON data from environment variables
def load_json_from_env(variable_name):
    data = os.getenv(variable_name)
    if data is None:
        print(f"Error: {variable_name} not found in environment variables.")
        exit(1)
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from {variable_name}: {e}")
        exit(1)

# Read backend IPs and load balancer IP from environment variables
print("Reading backend IPs...")
backend_ips = load_json_from_env("BACKEND_IPS")

# Validate the content of backend_ips
if not isinstance(backend_ips, list) or not all(isinstance(ip, str) for ip in backend_ips):
    print(f"Error: BACKEND_IPS does not contain a valid list of IPs.")
    exit(1)

print("Reading load balancer IP...")
load_balancer_ip = load_json_from_env("LB_IP")

# Validate the load balancer IP
if not isinstance(load_balancer_ip, str):
    print(f"Error: LB_IP is not a valid string IP.")
    exit(1)

# Define the inventory file path
inventory_file = 'ansible/inventory.yml'

# Generate the inventory file
try:
    with open(inventory_file, 'w') as f:
        # Write all hosts
        f.write("---\nall:\n  hosts:\n")
        for ip in backend_ips + [load_balancer_ip]:
            f.write(f"    {ip}:\n")
        f.write("  vars:\n    ansible_user: root\n    ansible_ssh_private_key_file: /var/iac-dev-container-data/id_ecdsa\n")
        
        # Write backends
        f.write("\nbackends:\n  hosts:\n")
        for ip in backend_ips:
            f.write(f"    {ip}:\n")
        
        # Write load balancer
        f.write("\nload_balancer:\n  hosts:\n")
        f.write(f"    {load_balancer_ip}:\n")
except Exception as e:
    print(f"Error while writing to {inventory_file}: {e}")
    exit(1)

print(f"Ansible inventory file has been successfully generated at {inventory_file}.")