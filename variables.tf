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
  default = 3
}