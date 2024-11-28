# Dynamic Load Balancer with Terraform, Ansible, and Docker

## Overview
This project provides a fully automated setup for deploying a dynamic load balancer and backend services on OpenNebula, leveraging modern tools like:
- **Terraform**: For resource provisioning.
- **Ansible**: For software configuration and deployment.
- **Docker**: For containerization of services.

The solution includes:
-	An Apache-based load balancer.
-	Configurable backend server nodes.
-	Full automation for scaling and configuration.

## Features
- **Dynamic Scaling**: Modify the number of backend nodes via a single Terraform variable.
- **Infrastructure as Code (IaC)**: Reproducible, maintainable, and version-controlled infrastructure setup.
- **Automated Configuration Management**: Ansible ensures consistent environment setup across all nodes.
- **Lightweight Containerization**: Docker is used for deploying scalable services.

## Repository Structure

```bash
.devcontainer/
  Dockerfile                # Dockerfile for building the dev environment
  devcontainer.json         # Dev container configuration
  docker-compose.yml        # Docker Compose file for the containerized dev environment
  init-iac-dev.sh           # Script to initialize SSH keys in the dev container
.github/workflows/
  main.yml                  # GitHub Actions workflow for CI/CD
ansible/
  roles/
    backend/
      tasks/
        main_tasks.yml      # Backend-specific Ansible tasks
      templates/
        index.html.j2       # Jinja2 template for backend web content
    load_balancer/
      tasks/
        main_tasks.yml      # Load balancer-specific Ansible tasks
      templates/
        apache              # Apache configuration templates
  inventory                 # Ansible inventory file for host management
  playbook.yml              # Main playbook orchestrating tasks
terraform/
  terraform.tf              # Terraform configuration for OpenNebula
  terraform.tfvars          # User-defined variables for Terraform
  variables.tf              # Terraform variables file
apache.conf.tmpl            # Template for Apache load balancer config
README.md                   # This documentation file
```

## Prerequisites
Before getting started, ensure the following tools are installed on your system:
- **Docker**: For running the development environment.
- **Terraform**: For provisioning cloud resources.
- **Ansible**: For configuring nodes.

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/VandlJ/iac-loadbalancer-automation.git
cd iac-loadbalancer-automation
```

### Step 2: Start the Development Container
```bash
docker-compose up -d
```
This starts a pre-configured development environment using Docker.

### Step 3: Initialize and Apply Terraform
```bash
terraform init
terraform plan
terraform apply -auto-approve
```
This initializes, plans and applies confirguration for Terraform.

### Step 4: Configure the Infrastructure with Ansible
```bash
ansible-playbook -i ansible/inventory ansible/playbook.yml
```

## Configuration
To scale the number of backend servers, edit the variables.tf file in the Terraform configuration directory. For example:
```bash
variable "backend_count" {
  default = 3
}
```
After modifying the variable, reapply the Terraform configuration:
```bash
terraform apply -auto-approve
```