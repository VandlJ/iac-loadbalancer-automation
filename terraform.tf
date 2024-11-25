terraform {
  required_providers {
    opennebula = {
      source = "OpenNebula/opennebula"
      version = "~> 1.2"
    }
  }
}

provider "opennebula" {
  endpoint      = "${var.opennebula_endpoint}"
  username      = "${var.opennebula_username}"
  password      = "${var.opennebula_password}"
}

# Image resource for all VMs
#resource "opennebula_image" "os-image" {
#  name        = "Ubuntu Minimal 24.04"
#  datastore_id = 101
#  persistent  = false
#  path        = "https://marketplace.opennebula.io//appliance/44077b30-f431-013c-b66a-7875a4a4f528/download/0"
#  permissions = "600"
#}

# Configurable backend nodes
resource "opennebula_virtual_machine" "backend-node" {
  count        = var.backend_count
  name         = "backend-${count.index + 1}"
  description  = "Backend Node"
  cpu          = 1
  vcpu         = 1
  memory       = 1024
  permissions  = "600"
  group        = "users"

  context = {
    NETWORK  = "YES"
    HOSTNAME = "$NAME"
    #SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAE0FXwXoybNozcCBPiXNavs5YaP+uXeegZYYCnXtgjXqbTTeiWfp4gOoemm8QChXGDabYDZLw6CpKW4Q/RUOycgWgDaThj7z6J52nRPQAc6vQan1mmGRyN0DEfSx3BVe6dimZjKbuHrME7OfA3gi4KzJMJ2+u3CyS6ZrzyEXkzMQdhwnw== root@599d9fcd17b2" # Macbook
    SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAGzxIR5qjjHJwpFYyPOWd4mPsHkSPt2nn6wWgVWvz31BGLQRQHCFE5TIls0Y1ZHPgoA8nfkRArsX5HrancBYuXlIQBA4NgMeQIv4flGehgYjVjbS5l/6pDZZMdjyG8aSBw7f0zMCk5xepGNGv06GmZ8UkLhYjYBZ++7ekqWLhsUr3if9g== root@1b998b9312b3"
    #SSH_PUBLIC_KEY = file("id_ecdsa.pub")
  }

  os {
    arch = "x86_64"
    boot = "disk0"
  }

  disk {
    image_id = 687 # opennebula_image.os-image.id 
    target   = "vda"
    size     = 12000 
  }

  graphics {
    listen = "0.0.0.0"
    type   = "vnc"
  }

  nic {
    network_id = 3
  }

  connection {
    type = "ssh"
    user = "root"
    host = "${self.ip}"
    private_key = "${file("/var/iac-dev-container-data/id_ecdsa")}"
    #private_key = file("id_ecdsa")  # Change to a relative path
  }

  provisioner "remote-exec" {
    inline = [
      "export DEBIAN_FRONTEND=noninteractive", 
      "apt -y update",
      "apt -y upgrade",
     ]
  }

  provisioner "remote-exec" {
    inline = [
      "echo 'Hello, World!' >> /etc/my-message"
     ]
  }
}

# Load balancer (NGINX)
resource "opennebula_virtual_machine" "load-balancer" {
  name         = "nginx-load-balancer"
  description  = "NGINX Load Balancer"
  cpu          = 1
  vcpu         = 1
  memory       = 1024
  permissions  = "600"
  group        = "users"

  context = {
    NETWORK       = "YES"
    HOSTNAME      = "$NAME"
    #SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAE0FXwXoybNozcCBPiXNavs5YaP+uXeegZYYCnXtgjXqbTTeiWfp4gOoemm8QChXGDabYDZLw6CpKW4Q/RUOycgWgDaThj7z6J52nRPQAc6vQan1mmGRyN0DEfSx3BVe6dimZjKbuHrME7OfA3gi4KzJMJ2+u3CyS6ZrzyEXkzMQdhwnw== root@599d9fcd17b2" # Macbook
    SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAGzxIR5qjjHJwpFYyPOWd4mPsHkSPt2nn6wWgVWvz31BGLQRQHCFE5TIls0Y1ZHPgoA8nfkRArsX5HrancBYuXlIQBA4NgMeQIv4flGehgYjVjbS5l/6pDZZMdjyG8aSBw7f0zMCk5xepGNGv06GmZ8UkLhYjYBZ++7ekqWLhsUr3if9g== root@1b998b9312b3"
    #SSH_PUBLIC_KEY = file("id_ecdsa.pub")
  }

  os {
    arch = "x86_64"
    boot = "disk0"
  }

  disk {
    image_id = 687 # opennebula_image.os-image.id 
    target   = "vda"
    size     = 12000
  }

  nic {
    network_id = 3
  }

  connection {
    type        = "ssh"
    user        = "root"
    host        = "${self.ip}"
    private_key = "${file("/var/iac-dev-container-data/id_ecdsa")}"
    #private_key = file("id_ecdsa")  # Change to a relative path
  }
}

# Outputs
output "backend_ips" {
  description = "IP addresses of the backend VMs"
  value       = opennebula_virtual_machine.backend-node.*.ip
}

output "load_balancer_ip" {
  description = "IP address of the load balancer"
  value       = opennebula_virtual_machine.load-balancer.ip
}

resource "local_file" "ansible_inventory" {
  content = templatefile("inventory.tmpl",
    {
      vm_admin_user = var.vm_admin_user,
      load_balancer = [opennebula_virtual_machine.load-balancer.ip],
      backend_nodes = opennebula_virtual_machine.backend-node.*.ip,
      ssh_key = var.ssh_key
    })
  filename = "ansible/inventory"
}

resource "local_file" "apache_config" {
  content = templatefile("apache.conf.tmpl", 
  {
    backend_nodes = opennebula_virtual_machine.backend-node.*.ip
  })
  filename = "ansible/roles/load_balancer/templates/apache"
}
