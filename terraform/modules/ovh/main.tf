terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = ">= 0.44.0"
    }
  }
}

resource "ovh_cloud_project_network_private" "vnet" {
  service_name = var.ovh_project_id
  name         = var.vnet_name
  regions      = [var.ovh_region]
}

# Subnet 1: Ingress (for ingress controllers or load balancer)
resource "ovh_cloud_project_network_private_subnet" "ingress" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = var.ovh_region
  start        = var.ingress_subnet_start
  end          = var.ingress_subnet_end
  network      = var.ingress_subnet_cidr
  dhcp         = true
  no_gateway   = false
}

# Subnet 2: App (Kubernetes nodes)
resource "ovh_cloud_project_network_private_subnet" "app" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = var.ovh_region
  start        = var.app_subnet_start
  end          = var.app_subnet_end
  network      = var.app_subnet_cidr
  dhcp         = true
  no_gateway   = false
}

# Subnet 3: Data (PostgreSQL, etc.)
resource "ovh_cloud_project_network_private_subnet" "data" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = var.ovh_region
  start        = var.data_subnet_start
  end          = var.data_subnet_end
  network      = var.data_subnet_cidr
  dhcp         = true
  no_gateway   = false
}

# Update Object Storage to supported resource
resource "ovh_cloud_project_storage" "storage" {
  service_name = var.ovh_project_id
  region_name  = var.ovh_region_short
  name         = var.object_storage_name
  versioning = {
    status = var.object_storage_versioning
  }
}

resource "ovh_cloud_project_gateway" "gateway" {
  service_name = var.ovh_project_id
  name       = var.gateway_name
  model      = var.gateway_model
  region     = var.ovh_region
  network_id = local.vnet_openstack_id
  subnet_id  = ovh_cloud_project_network_private_subnet.ingress.id
}

# Update Kubernetes Cluster resource and add node pool
resource "ovh_cloud_project_kube" "cluster" {
  service_name = var.ovh_project_id
  name         = var.k8s_cluster_name
  region       = var.ovh_region
  version      = var.k8s_version
  private_network_id = local.vnet_openstack_id
  nodes_subnet_id = ovh_cloud_project_network_private_subnet.app.id
  private_network_configuration {
      default_vrack_gateway              = ""
      private_network_routing_as_default = false
  }
  depends_on = [
    ovh_cloud_project_network_private_subnet.app
  ] 
}

resource "ovh_cloud_project_kube_nodepool" "default" {
  service_name  = ovh_cloud_project_kube.cluster.service_name
  kube_id      = ovh_cloud_project_kube.cluster.id
  name         = var.k8s_nodepool_name
  flavor_name  = var.k8s_nodepool_flavor
  desired_nodes = var.k8s_nodepool_desired_nodes
  max_nodes     = var.k8s_nodepool_max_nodes
  min_nodes     = var.k8s_nodepool_min_nodes
  autoscale     = var.k8s_nodepool_autoscale
}

resource "ovh_cloud_project_database" "pgsqldb" {
  service_name  = var.ovh_project_id
  description   = var.pgsql_description
  engine        = "postgresql"
  version       = var.pgsql_version
  plan          = var.pgsql_plan
  nodes {
    region      = var.ovh_region_short
    network_id  = local.vnet_openstack_id
    subnet_id   = ovh_cloud_project_network_private_subnet.data.id
  }
  flavor        = var.pgsql_flavor

  dynamic "ip_restrictions" {
    for_each = var.pgsql_ip_restrictions
    content {
      ip          = ip_restrictions.value.ip
      description = ip_restrictions.value.description
    }
  }
}

data "ovh_cloud_project_database" "pgsqldb_data" {
  service_name = var.ovh_project_id
  engine       = "postgresql"
  id           = ovh_cloud_project_database.pgsqldb.id
}

resource "ovh_cloud_project_database_database" "pgsqldb_database" {
  service_name = var.ovh_project_id
  engine      = data.ovh_cloud_project_database.pgsqldb_data.engine
  cluster_id  = data.ovh_cloud_project_database.pgsqldb_data.id
  name        = "dummydb"
}

# Outputs
output "kubeconfig" {
  value     = ovh_cloud_project_kube.cluster.kubeconfig
  sensitive = true
}

output "object_storage_name" {
  value = ovh_cloud_project_storage.storage.name
}

output "pgsql_host" {
  value = data.ovh_cloud_project_database.pgsqldb_data.endpoints[0].domain
}
output "pgsql_port" {
  value = data.ovh_cloud_project_database.pgsqldb_data.endpoints[0].port
}
output "pgsql_uri" {
  value = data.ovh_cloud_project_database.pgsqldb_data.endpoints[0].uri
}
output "pgsql_dbname" {
  value = ovh_cloud_project_database_database.pgsqldb_database.name
}
output "pgsql_cluster_id" {
  value = ovh_cloud_project_database.pgsqldb.id
}