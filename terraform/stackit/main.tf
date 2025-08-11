## Virt network

## Subnet K8S

## Subnet DB

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
    class = var.postgres_storage_size
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
  kubernetes_version_min = var.kubernetes_cluster_version

  node_pools = [{
    name = var.kubernetes_node_pool_name
    machine_type = var.kubernetes_node_machine_type
    minimum = 1
    maximum = 1
    availability_zones = ["eu01-1"]
    os_version_min = "3815.2.5"
    os_name = "flatcar"
    volume_size = 32
    volume_type = "storage_premium_perf6"
  }]
}

resource "stackit_ske_kubeconfig" "ske_kubeconfig" {
  project_id   = var.project_id
  cluster_name = stackit_ske_cluster.ske_cluster.name
  refresh = var.kubernetes_config_refresh
}

