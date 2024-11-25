variable "opennebula_endpoint"  {
    description = "Open Nebula endpoint URL"
    default = "https://nuada.zcu.cz/RPC2"
}
variable "opennebula_username"  {
    description = "Open Nebula username"
}
variable "opennebula_password"  {
    description = "Open Nebula login token"
}
variable "backend_count" {
  description = "Number of cluster nodes"
  default = 2
}
variable "ssh_public_key_path" {
  default = "/var/iac-dev-container-data/id_ecdsa.pub"
}
variable "vm_admin_user" {
  description = "Ansible user for SSH connections"
  type        = string
  default     = "root"
}
variable "ssh_key" {
  description = "Ansible SSH key for connection"
  default = "/var/iac-dev-container-data/id_ecdsa"
}

