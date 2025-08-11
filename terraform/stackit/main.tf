## Virt network
resource "stackit_network" "network" {
  project_id = var.project_id
  name       = var.network_name
}

## NIC K8s
resource "stackit_network_interface" "k8s_interface" {
  project_id         = var.project_id
  network_id         = stackit_network.network.id
  allowed_addresses  = stackit_ske_cluster.ske_cluster.pod_address_ranges
}

## NIC DB
resource "stackit_network_interface" "db_interface" {
  project_id         = var.project_id
  network_id         = stackit_network.network.id
}

## Public IP
resource "stackit_public_ip" "public_ip" {
  project_id           = var.project_id
  network_interface_id = stackit_network.network.id
}

## postgres DB
resource "stackit_postgresflex_instance" "postgres_instance" {
  acl = var.postgres_acl
  backup_schedule = var.postgres_backup_schedule
  flavor          = {
    cpu = var.postgres_flavor_cpu
    ram = var.postgres_flavor_ram
  }
  name            = var.postgres_instance_name
  project_id      = var.project_id
  replicas        = var.postgres_replicas
  storage         = {
    class = var.postgres_storage_class
    size  = var.postgres_storage_size
  }
  version         = var.postgres_version
}

resource "stackit_postgresflex_database" "postgres_database" {
  instance_id = stackit_postgresflex_instance.postgres_instance.instance_id
  name        = var.postgres_database_name
  owner       = var.postgres_user_name
  project_id  = var.project_id
}

resource "stackit_postgresflex_user" "postgres_user" {
  instance_id = stackit_postgresflex_instance.postgres_instance.instance_id
  project_id  = var.project_id
  roles       = var.postgres_user_roles
  username    = var.postgres_user_name
}

## K8s cluster
resource "stackit_ske_cluster" "ske_cluster" {
  project_id = var.project_id
  name = var.kubernetes_cluster_name
  node_pools = [{
    name = var.kubernetes_node_pool_name
    machine_type = var.kubernetes_node_machine_type
    minimum = var.kubernetes_node_min
    maximum = var.kubernetes_node_max
    availability_zones = var.kubernetes_availability_zones
  }]
}

resource "stackit_ske_kubeconfig" "ske_kubeconfig" {
  project_id   = var.project_id
  cluster_name = stackit_ske_cluster.ske_cluster.name
  refresh = var.kubernetes_config_refresh
}
