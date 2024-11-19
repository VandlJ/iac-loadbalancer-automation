import json

with open('inventory.json') as f:
    terraform_output = json.load(f)

backend_ips = terraform_output["backend_ips"]["value"]
lb_ip = terraform_output["load_balancer_ip"]["value"]

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
