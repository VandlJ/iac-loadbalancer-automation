# Define file paths
backend_ips_file = 'backend_ips.txt'
load_balancer_ip_file = 'lb_ip.txt'
inventory_file = 'ansible/inventory.yml'

# Read backend IPs from backend_ips.txt
try:
    with open(backend_ips_file, 'r') as f:
        # Read the file content, remove extra spaces, commas, and square brackets
        content = f.read().strip()  # Read and strip the content
        # Remove square brackets and split the IPs by commas
        backend_ips = [ip.strip().strip('"') for ip in content.strip('[]').split(',') if ip.strip()]
except FileNotFoundError:
    print(f"Error: {backend_ips_file} not found.")
    exit(1)

# Validate the content of backend_ips
if not backend_ips:
    print(f"Error: {backend_ips_file} does not contain any IPs.")
    exit(1)

# Read load balancer IP from lb_ip.txt
try:
    with open(load_balancer_ip_file, 'r') as f:
        # Read the single IP address and strip any extra spaces or quotes
        load_balancer_ip = f.read().strip().strip('"')
except FileNotFoundError:
    print(f"Error: {load_balancer_ip_file} not found.")
    exit(1)

# Validate the load balancer IP
if not load_balancer_ip:
    print(f"Error: {load_balancer_ip_file} does not contain a valid IP.")
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