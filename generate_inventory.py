import json
import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python3 generate_inventory.py 'terraform output -json'")
    exit(1)

# Function to load JSON from a file or stdin
def load_json_from_input():
    try:
        return json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from input: {e}")
        exit(1)

# Load the Terraform output JSON
terraform_output = load_json_from_input()

# Extract backend IPs and load balancer IP
try:
    backend_ips = terraform_output["backend_ips"]["value"]
    load_balancer_ip = terraform_output["load_balancer_ip"]["value"]
except KeyError as e:
    print(f"Error: Missing key in JSON input - {e}")
    exit(1)

# Validate the backend IPs (ensure it's a list of strings)
if not isinstance(backend_ips, list) or not all(isinstance(ip, str) for ip in backend_ips):
    print(f"Error: backend_ips does not contain a valid list of IPs.")
    exit(1)

# Validate the load balancer IP (ensure it's a string)
if not isinstance(load_balancer_ip, str):
    print(f"Error: load_balancer_ip is not a valid string IP.")
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