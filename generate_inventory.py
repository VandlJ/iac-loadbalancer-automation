import json

# Define file paths
backend_ips_file = 'backend_ips.json'
load_balancer_ip_file = 'lb_ip.json'
inventory_file = 'ansible/inventory.yml'

# Read backend IPs from backend_ips.json
try:
    with open(backend_ips_file, 'r') as f:
        # Parse JSON and validate it as a list of strings
        backend_ips = json.load(f)
        if not isinstance(backend_ips, list) or not all(isinstance(ip, str) for ip in backend_ips):
            raise ValueError(f"{backend_ips_file} does not contain a valid list of IPs.")
except FileNotFoundError:
    print(f"Error: {backend_ips_file} not found.")
    exit(1)
except (json.JSONDecodeError, ValueError) as e:
    print(f"Failed to decode JSON from {backend_ips_file}: {e}")
    exit(1)

# Read load balancer IP from lb_ip.json
try:
    with open(load_balancer_ip_file, 'r') as f:
        # Parse JSON and validate it as a string
        load_balancer_ip = json.load(f)
        if not isinstance(load_balancer_ip, str):
            raise ValueError(f"{load_balancer_ip_file} does not contain a valid IP address.")
except FileNotFoundError:
    print(f"Error: {load_balancer_ip_file} not found.")
    exit(1)
except (json.JSONDecodeError, ValueError) as e:
    print(f"Failed to decode JSON from {load_balancer_ip_file}: {e}")
    exit(1)

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

# Print the content of the inventory.yml file
try:
    with open(inventory_file, 'r') as f:
        print("\nContent of inventory.yml:")
        print(f.read())  # Print the file content
except FileNotFoundError:
    print(f"Error: {inventory_file} not found.")
except Exception as e:
    print(f"Error while reading {inventory_file}: {e}")

print(f"Ansible inventory file has been successfully generated at {inventory_file}.")