## General
variable "project_id" {
  description = "ID of the StackIT Project"
  type        = string
  default     = "cdae8eed-9d4f-49d4-a059-9fe987c52735"
}
variable "service_account_key_path" {
  default = "./stackit_sa_pub_key.pem"
}
variable "private_key_path" {
  default = "./stackit_sa_priv_key.pem"
}

## Network
variable "network_name" {
  default = "landing_zone_vnet"
}

## Postgres
variable "postgres_acl" {
  default = ["193.148.160.0/19", "45.129.40.0/21"]
}
variable "postgres_backup_schedule" {
  default = "0 0 1 1 *"
}
variable "postgres_flavor_cpu" {
  default = 2
}
variable "postgres_flavor_ram" {
  default = 4
}
variable "postgres_instance_name" {
  default = "dummypsqlserver"
}
variable "postgres_replicas" {
  default = 1
}
variable "postgres_storage_class" {
  default = "premium-perf2-stackit"
}
variable "postgres_storage_size" {
  default = 5
}
variable "postgres_version" {
  default = "15"
}
variable "postgres_database_name" {
  default = "dummydb"
}
variable "postgres_user_name" {
  default = "psqladmin"
}
variable "postgres_user_roles" {
  default = ["login", "createdb"]
}

## Kubernetes
variable "kubernetes_cluster_name" {
  default = "dummy-ske"
}
variable "kubernetes_node_pool_name" {
  default = "default"
}
variable "kubernetes_node_machine_type" {
  default = "c1.2"
}
variable "kubernetes_node_min" {
  default = 1
}
variable "kubernetes_node_max" {
  default = 2
}
variable "kubernetes_availability_zones" {
  default = "eu-01-3"
}
variable "kubernetes_config_refresh" {
  default = true
}
