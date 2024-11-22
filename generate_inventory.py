import json

# Define file paths
backend_ips_file = 'backend_ips.json'
load_balancer_ip_file = 'load_balancer_ip.json'
inventory_file = 'ansible/inventory.yml'

# Read backend IPs
try:
    with open(backend_ips_file, 'r') as f:
        backend_ips = json.load(f)
except FileNotFoundError:
    print(f"Error: {backend_ips_file} not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON from {backend_ips_file}: {e}")
    exit(1)

# Validate the content of backend_ips
if not isinstance(backend_ips, list) or not all(isinstance(ip, str) for ip in backend_ips):
    print(f"Error: {backend_ips_file} does not contain a valid list of IPs.")
    exit(1)

# Read load balancer IP
try:
    with open(load_balancer_ip_file, 'r') as f:
        load_balancer_ip = json.load(f)
except FileNotFoundError:
    print(f"Error: {load_balancer_ip_file} not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON from {load_balancer_ip_file}: {e}")
    exit(1)

# Validate the load balancer IP
if not isinstance(load_balancer_ip, str):
    print(f"Error: {load_balancer_ip_file} does not contain a valid string IP.")
    exit(1)

# Generate the inventory file
try:
    with open(inventory_file, 'w') as f:
        # Write all hosts
        f.write("---\nall:\n  hosts:\n")
        for ip in backend_ips:
            f.write(f"    {ip}:\n")
        f.write(f"    {load_balancer_ip}:\n")
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