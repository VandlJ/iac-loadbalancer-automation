import json

# Open the inventory.json file and attempt to load the JSON data
try:
    with open('inventory.json') as f:
        terraform_output = json.load(f)
except json.JSONDecodeError as e:
    print(f"Failed to decode JSON: {e}")
    exit(1)

# Check the structure of terraform_output
print("Terraform output structure:", terraform_output)

# Ensure the keys are present in the output
if "backend_ips" in terraform_output and "load_balancer_ip" in terraform_output:
    backend_ips = terraform_output["backend_ips"]["value"]
    lb_ip = terraform_output["load_balancer_ip"]["value"]

    # Open the inventory.yml file for writing
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
else:
    print("Error: Missing required keys in Terraform output.")
    exit(1)