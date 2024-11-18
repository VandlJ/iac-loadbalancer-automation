# Dynamic Load Balancer with Terraform, Ansible, and Docker

## Overview
This project automates the provisioning, configuration, and management of a dynamic infrastructure using:
- **Terraform**: For provisioning resources on OpenNebula.
- **Ansible**: For post-provisioning configuration and software setup.
- **Docker**: For containerizing the load balancer and backend services.

The setup includes a configurable load balancer (NGINX) and multiple backend nodes, all deployed on OpenNebula. 

## Features
- **Dynamic Scaling**: Easily adjust the number of backend nodes by modifying a single variable in Terraform.
- **Infrastructure as Code (IaC)**: Maintain reproducible infrastructure using Terraform and Ansible.
- **Automated Configuration**: Use Ansible to install required packages and configure services across nodes.
- **Containerization**: Use Docker for lightweight, scalable deployments.

## Repository Structure

```bash
ansible/                  # Ansible playbooks and roles
  inventory.yml           # Ansible inventory file (dynamic)
  playbook.yml            # Main Ansible playbook
  roles/                  # Ansible roles
    common/               # Example role for package installation
      tasks/
        main.yml          # Tasks to execute on nodes
docker-compose.yml        # Docker Compose file for dev container
Dockerfile                # Dockerfile for building dev environment
init-iac-dev.sh           # Script for initializing SSH keys in dev container
terraform.tf              # Terraform configuration file
README.md                 # This file
```

## Prerequisites
- **Docker**: For the development environment.
- **Terraform**: Installed in the container or locally.
- **Python 3**: For dynamic inventory generation.
- **Ansible**: Installed in the container.

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/iac-loadbalancer-automation.git
cd iac-loadbalancer-automation
```

### Step 2: Start the Development Container
```bash
docker-compose up -d
```
### Step 3: Provision Infrastructure with Terraform
```bash
terraform init
terraform apply -auto-approve
```

### Step 4: Generate Ansible Inventory
```bash
python3 generate_inventory.py
```

### Step 5: Configure Nodes with Ansible
```bash
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```

## Configuration
- Adjust the number of backend nodes by modifying `terraform.tf`:
```bash
variable "backend_count" {
  default = 3
}
```
- Update the Ansible playbook (`ansible/playbook.yml`) to include additional roles or tasks.