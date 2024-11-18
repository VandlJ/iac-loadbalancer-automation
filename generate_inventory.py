import json

# Load the Terraform output JSON
with open('inventory.json') as f:
    terraform_output = json.load(f)

# Extract the IP address from the Terraform output
vm_ip = terraform_output["vm_ips"]["value"]

# Write the Ansible inventory file
with open('ansible/inventory.yml', 'w') as f:
    f.write("---\nall:\n  hosts:\n")
    f.write(f"    {vm_ip}:\n")
    f.write("  vars:\n")
    f.write("    ansible_user: root\n")
    f.write("    ansible_ssh_private_key_file: /var/iac-dev-container-data/id_ecdsa\n")
