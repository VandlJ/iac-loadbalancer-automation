import json
import os

# Check if inventory.json exists and is not empty
file_path = 'inventory.json'
if not os.path.exists(file_path):
    print("Error: inventory.json file does not exist.")
    exit(1)

if os.path.getsize(file_path) == 0:
    print("Error: inventory.json file is empty.")
    exit(1)

# Debug: Print file content
with open(file_path, 'r') as f:
    content = f.read()
    print("Content of inventory.json:")
    print(content)

# Parse JSON
try:
    terraform_output = json.loads(content)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
    exit(1)

# Process Terraform output
backend_ips = terraform_output["backend_ips"]["value"]
lb_ip = terraform_output["load_balancer_ip"]["value"]

# Generate Ansible inventory file
with open('ansible/inventory.yml', 'w') as f:
    f.write("---\nall:\n  hosts:\n")
    for ip in backend_ips:
        f.write(f"    {ip}:\n")
    f.write(f"    {lb_ip}:\n")
    f.write("  vars:\n    ansible_user: root\n    ansible_ssh_private_key_file: /var/iac-dev-container-data/id_ecdsa\n")
    f.write("\nbackends:\n  hosts:\n")
    for ip in backend_ips:
        f.write(f"    {ip}:\n")
    f.write("\nload_balancer:\n  hosts:\n")
    f.write(f"    {lb_ip}:\n")

print("Ansible inventory.yml file has been generated successfully.")