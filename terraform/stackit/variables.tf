## General
variable "project_id" {
  description = "ID of the StackIT Project"
  type        = string
  default     = "cdae8eed-9d4f-49d4-a059-9fe987c52735"
}

## Network
variable "network_name" {
  default = ""
}

## Postgres
variable "postgres_acl" {
  default = ""
}
variable "postgres_backup_schedule" {
  default = ""
}
variable "postgres_flavor_cpu" {
  default = ""
}
variable "postgres_flavor_ram" {
  default = ""
}
variable "postgres_instance_name" {
  default = ""
}
variable "postgres_replicas" {
  default = ""
}
variable "postgres_storage_class" {
  default = ""
}
variable "postgres_storage_size" {
  default = ""
}
variable "postgres_version" {
  default = ""
}
variable "postgres_database_name" {
  default = ""
}
variable "postgres_user_name" {
  default = ""
}
variable "postgres_user_roles" {
  default = ""
}

## Kubernetes
variable "kubernetes_cluster_name" {
  default = ""
}
variable "kubernetes_node_pool_name" {
  default = ""
}
variable "kubernetes_node_machine_type" {
  default = ""
}
variable "kubernetes_node_min" {
  default = ""
}
variable "kubernetes_node_max" {
  default = ""
}
variable "kubernetes_availability_zones" {
  default = ""
}
variable "kubernetes_config_refresh" {
  default = ""
}
