import json

# Define file paths
input_file = 'inventory.json'
output_file = 'ansible/inventory.yml'

# Read and parse the inventory.json file
try:
    with open(input_file, 'r') as f:
        inventory_data = json.load(f)  # Parse the entire JSON file as a single object
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON from {input_file}: {e}")
    exit(1)

# Extract backend_ips and load_balancer_ip
try:
    backend_ips = inventory_data.get("backend_ips", {}).get("value", [])
    load_balancer_ip = inventory_data.get("load_balancer_ip", {}).get("value", "")

    # Validate backend_ips
    if not isinstance(backend_ips, list) or not all(isinstance(ip, str) for ip in backend_ips):
        raise ValueError(f"{input_file} contains invalid backend_ips.")
    
    # Validate load_balancer_ip
    if not isinstance(load_balancer_ip, str):
        raise ValueError(f"{input_file} contains invalid load_balancer_ip.")
except ValueError as e:
    print(e)
    exit(1)

# Generate the inventory.yml file
try:
    with open(output_file, 'w') as f:
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
    print(f"Error while writing to {output_file}: {e}")
    exit(1)

# Print the content of the inventory.yml file
try:
    with open(output_file, 'r') as f:
        print("\nContent of inventory.yml:")
        print(f.read())  # Print the file content
except FileNotFoundError:
    print(f"Error: {output_file} not found.")
except Exception as e:
    print(f"Error while reading {output_file}: {e}")

print(f"Ansible inventory file has been successfully generated at {output_file}.")