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

resource "opennebula_image" "os-image" {
  name = "Ubuntu Minimal 24.04"
  datastore_id = 101
  persistent = false
  path = "https://marketplace.opennebula.io//appliance/44077b30-f431-013c-b66a-7875a4a4f528/download/0"
  permissions = "600"
}

resource "opennebula_virtual_machine" "cluster-node" { 
  count = var.cluster_size
  name = "vmnode-${count.index + 1}"
  description = "Main node VM"
  cpu = 1
  vcpu = 1
  memory = 2048
  permissions = "600"
  group = "users"

  context = {
    NETWORK  = "YES"
    HOSTNAME = "$NAME"
    SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAE0FXwXoybNozcCBPiXNavs5YaP+uXeegZYYCnXtgjXqbTTeiWfp4gOoemm8QChXGDabYDZLw6CpKW4Q/RUOycgWgDaThj7z6J52nRPQAc6vQan1mmGRyN0DEfSx3BVe6dimZjKbuHrME7OfA3gi4KzJMJ2+u3CyS6ZrzyEXkzMQdhwnw== root@599d9fcd17b2"
    START_SCRIPT = "echo 'Byl jsem tady.' >> /etc/my-message"
  }
  os {
    arch = "x86_64"
    boot = "disk0"
  }
  disk {
    image_id = opennebula_image.os-image.id
    target   = "vda"
    size     = 12000 # 12GB
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
  }

  provisioner "file" {
    source = "provisioned-files/soubor-1.cfg"
    destination = "/etc/file-one.cfg"
  }

  provisioner "file" {
    source = "provisioned-files/soubor-2.cfg"
    destination = "/etc/file-two.cfg"
  }

  provisioner "remote-exec" {
    inline = [
      "export DEBIAN_FRONTEND=noninteractive", 
      "apt -y update",
      "apt -y upgrade",
      "apt -y install mc"
     ]
  }

  provisioner "remote-exec" {
    inline = [
      "echo 'Hello, World!' >> /etc/my-message"
     ]
  }
}

#----OUTPUTS----

output "vm_ips" {
  description = "IP addresses of the VMs"
  value = opennebula_virtual_machine.cluster-node.*.ip
}
