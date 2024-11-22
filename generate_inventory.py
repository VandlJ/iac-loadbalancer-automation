import json

file_path = 'inventory.json'

# Check if the file exists and is not empty
try:
    with open(file_path, 'r') as f:
        # Skip the first line and load the rest as JSON
        content = f.readlines()[1:]  # Read lines starting from the second line
        content = ''.join(content)  # Join lines back into a single string

        # Debug: Print the content being parsed
        print("Content being parsed as JSON:")
        print(content)

        terraform_output = json.loads(content)
except FileNotFoundError:
    print(f"Error: File {file_path} not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
    exit(1)

# Extract values from the JSON
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