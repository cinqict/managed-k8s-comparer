# Networking
resource "stackit_network" "main" {
  project_id = var.stackit_project_id
  name       = "main-network"
  routed     = true
  labels = {
    "env" = "benchmark"
  }
}

# StackIt Kubernetes Engine (SKE) Cluster
resource "stackit_ske_cluster" "main" {
  project_id             = var.stackit_project_id
  name                   = "main-k8s"
  kubernetes_version_min = "1.33"

  network = {
    id = stackit_network.main.network_id
  }

  node_pools = [
    {
      name               = "main-node-pool"
      machine_type       = "g1.3"
      minimum            = 1
      maximum            = 3
      availability_zones = ["eu01-1"]
      os_version_min     = "3815.2.5"
      os_name            = "flatcar"
      volume_size        = 32
      volume_type        = "storage_premium_perf6"
    }
  ]

  maintenance = {
    enable_kubernetes_version_updates    = true
    enable_machine_image_version_updates = true
    start                               = "01:00:00Z"
    end                                 = "02:00:00Z"
  }
}

resource "stackit_ske_kubeconfig" "main" {
  cluster_name = stackit_ske_cluster.main.name
  project_id   = var.stackit_project_id
}

# Database
resource "stackit_postgresflex_instance" "main" {
  project_id      = var.stackit_project_id
  name            = "main-pgsql-flex"
  acl             = ["0.0.0.0/0"] # Adjust for your needs
  backup_schedule = "00 00 * * *"
  flavor = {
    cpu = 2
    ram = 4
  }
  replicas = 1
  storage = {
    class = "premium-perf6-stackit"
    size  = 20
  }
  version = 15
}

resource "stackit_postgresflex_user" "main" {
  project_id  = var.stackit_project_id
  instance_id = stackit_postgresflex_instance.main.id
  username    = "appuser"
  roles       = ["login","createdb"]
}

resource "stackit_postgresflex_database" "main" {
  project_id  = var.stackit_project_id
  instance_id = stackit_postgresflex_instance.main.id
  name        = "appdb"
  owner       = "appuser"
}