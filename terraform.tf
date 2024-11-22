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
    # SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAE0FXwXoybNozcCBPiXNavs5YaP+uXeegZYYCnXtgjXqbTTeiWfp4gOoemm8QChXGDabYDZLw6CpKW4Q/RUOycgWgDaThj7z6J52nRPQAc6vQan1mmGRyN0DEfSx3BVe6dimZjKbuHrME7OfA3gi4KzJMJ2+u3CyS6ZrzyEXkzMQdhwnw== root@599d9fcd17b2"
    # SSH_PUBLIC_KEY = file(var.ssh_public_key_path)
    SSH_PUBLIC_KEY = "${file("id_ecdsa.pub")}"
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
    # private_key = "${file("/var/iac-dev-container-data/id_ecdsa")}"
    private_key = "${file("id_ecdsa")}"  # Change to a relative path
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
    # SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAE0FXwXoybNozcCBPiXNavs5YaP+uXeegZYYCnXtgjXqbTTeiWfp4gOoemm8QChXGDabYDZLw6CpKW4Q/RUOycgWgDaThj7z6J52nRPQAc6vQan1mmGRyN0DEfSx3BVe6dimZjKbuHrME7OfA3gi4KzJMJ2+u3CyS6ZrzyEXkzMQdhwnw== root@599d9fcd17b2"
    # SSH_PUBLIC_KEY = file(var.ssh_public_key_path)
    SSH_PUBLIC_KEY = "${file("id_ecdsa.pub")}"
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
    # private_key = "${file("/var/iac-dev-container-data/id_ecdsa")}"
    private_key = "${file("id_ecdsa")}"  # Change to a relative path
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