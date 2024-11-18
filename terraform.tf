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

resource "opennebula_virtual_machine" "vmnode-1" { 
  permissions = "600"
  name = "vmnode-1"
  description = "Main node VM"
  cpu = 1
  vcpu = 1
  memory = 2048
  group = "users"

  context = {
    NETWORK  = "YES"
    HOSTNAME = "$NAME"
    SSH_PUBLIC_KEY = "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBABfQJIhqxaahzznDkHKnWBYPnXkSYo3/uLcTYBpMzE3j4xvYlDOG/dUw7nHHYytuzcQ885VZrg8eJvf2/I84bGZ2QDHrH2/WV45qReBqRGoKmFPgYZwHmWa9bU4Rv0QYxGW6Io2f58GPH/w7VjcMu+K3xP91Im7XtjFQzRkr/3hsLrJTw== root@238ba4651c22"
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
  value = opennebula_virtual_machine.vmnode-1.ip
}
