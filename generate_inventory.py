import json

# Load the Terraform output JSON
with open('inventory.json') as f:
    terraform_output = json.load(f)

# Extract the list of IP addresses
vm_ips = terraform_output["vm_ips"]["value"]

# Write the Ansible inventory file
with open('ansible/inventory.yml', 'w') as f:
    f.write("---\nall:\n  hosts:\n")
    for ip in vm_ips:
        f.write(f"    {ip}:\n")
    f.write("  vars:\n")
    f.write("    ansible_user: root\n")
    f.write("    ansible_ssh_private_key_file: /var/iac-dev-container-data/id_ecdsa\n")
