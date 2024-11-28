# Dynamic Load Balancer with Terraform, Ansible, and Docker

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Repository Structure](#repository-structure)
4. [Demo](#demo) 
5. [Prerequisites](#prerequisites)  
6. [Setup Instructions](#setup-instructions)  
   - [Step 1: Clone the Repository](#step-1-clone-the-repository)  
   - [Step 2: Run Development Environment in Docker](#step-2-run-development-environment-in-docker)  
   - [Step 3: Initialize and Apply Terraform](#step-3-initialize-and-apply-terraform)  
   - [Step 4: Configure the Infrastructure with Ansible](#step-4-configure-the-infrastructure-with-ansible)  
7. [Configuration](#configuration)   

---

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

## Demo

To see the project in action, visit the deployed application in your browser here:
<a href="http://147.228.173.116" target="_blank">Load Balancer</a>

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

### Step 2: Run directory inside of Docker container

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
