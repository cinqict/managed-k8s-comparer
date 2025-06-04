# OVH Landing Zone Terraform Configuration

# This is a starting point for provisioning a landing zone on OVH Cloud.
# It includes a virtual network, PostgreSQL, object storage, and a managed Kubernetes cluster.

terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = ">= 0.44.0"
    }
  }
}

provider "ovh" {
  endpoint           = var.ovh_endpoint
  application_key    = var.ovh_application_key
  application_secret = var.ovh_application_secret
  consumer_key       = var.ovh_consumer_key
}

# Example: Create a Public Cloud Project (required for most OVH resources)
resource "ovh_cloud_project" "main" {
  description = "Landing Zone Project"
}

# Example: Create a Network (Private Network)
resource "ovh_cloud_project_network_private" "vnet" {
  service_name = ovh_cloud_project.main.id
  name         = "landing-zone-vnet"
  regions      = ["GRA"] # Change to your preferred region
}

# Example: Create a PostgreSQL Managed Database
resource "ovh_cloud_project_database_postgresql" "db" {
  service_name = ovh_cloud_project.main.id
  description  = "Landing Zone PostgreSQL"
  plan         = "essential"
  version      = "15"
  nodes {
    region = "GRA"
    flavor = "db1-7"
  }
}

# Example: Create Object Storage
resource "ovh_cloud_project_storage" "bucket" {
  service_name = ovh_cloud_project.main.id
  name         = "landingzone-bucket"
  region       = "GRA"
  container    = true
}

# Example: Create a Managed Kubernetes Cluster
resource "ovh_cloud_project_kube" "cluster" {
  service_name = ovh_cloud_project.main.id
  name         = "landing-zone-k8s"
  region       = "GRA"
  version      = "1.29"
  private_network_id = ovh_cloud_project_network_private.vnet.id
  private_network_configuration {
    default_vrack_gateway = true
  }
  node_pool {
    name       = "default"
    flavor_id  = "b2-7"
    desired_nodes = 2
    max_nodes     = 3
    min_nodes     = 1
    autoscale     = true
  }
}

# IAM Groups (Roles) for the Landing Zone
resource "ovh_iam_policy" "group" {
  for_each    = toset(var.iam_groups)
  name        = each.value
  description = "${each.value} group for landing zone access"
  policy      = file("${path.module}/policies/${each.value}.json")
}

# Outputs
output "kubeconfig" {
  value = ovh_cloud_project_kube.cluster.kubeconfig
  sensitive = true
}

output "postgresql_uri" {
  value = ovh_cloud_project_database_postgresql.db.uri
  sensitive = true
}

output "object_storage_name" {
  value = ovh_cloud_project_storage.bucket.name
}
