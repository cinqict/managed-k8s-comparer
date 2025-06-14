# OVH Landing Zone Terraform Configuration

# This is a starting point for provisioning a landing zone on OVH Cloud.
# It includes a virtual network, PostgreSQL, object storage, and a managed Kubernetes cluster.

terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = ">= 0.44.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "rg-noudsavenije-devops"
    storage_account_name = "noudstfbackend"
    container_name       = "ovhtfstate"
    key                  = "terraform.tfstate"
  }
}

provider "ovh" {
  endpoint           = var.ovh_endpoint
  application_key    = var.ovh_application_key
  application_secret = var.ovh_application_secret
  consumer_key       = var.ovh_consumer_key
}

# data "ovh_me" "myaccount" {}

# data "ovh_order_cart" "mycart" {
#   ovh_subsidiary = data.ovh_me.myaccount.ovh_subsidiary
# }

# data "ovh_order_cart_product_plan" "cloud" {
#   cart_id        = data.ovh_order_cart.mycart.id
#   price_capacity = "renew"
#   product        = "cloud"
#   plan_code      = "project.2018"
# }

# # Example: Create a Public Cloud Project (required for most OVH resources)
# resource "ovh_cloud_project" "main" {
#   ovh_subsidiary = data.ovh_order_cart.mycart.ovh_subsidiary
#   description    = "Landing Zone Project"

# 6955a9f3a47143e8b9f4c94f6dd97742
#   plan {
#     duration     = data.ovh_order_cart_product_plan.cloud.selected_price[0].duration
#     plan_code    = data.ovh_order_cart_product_plan.cloud.plan_code
#     pricing_mode = data.ovh_order_cart_product_plan.cloud.selected_price[0].pricing_mode
#   }
# }

# Example: Create a Network (Private Network)
resource "ovh_cloud_project_network_private" "vnet" {
  service_name = var.ovh_project_id
  name         = "landing-zone-vnet"
  regions      = ["GRA9"]
}

# Subnet 1: Ingress (for ingress controllers or load balancer)
resource "ovh_cloud_project_network_private_subnet" "ingress" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = "GRA9"
  start        = "192.168.10.10"
  end          = "192.168.10.200"
  network      = "192.168.10.0/24"
  dhcp         = true
  no_gateway   = false
}

# Subnet 2: App (Kubernetes nodes)
resource "ovh_cloud_project_network_private_subnet" "app" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = "GRA9"
  start        = "192.168.20.10"
  end          = "192.168.20.200"
  network      = "192.168.20.0/24"
  dhcp         = true
  no_gateway   = false
}

# Subnet 3: Data (PostgreSQL, etc.)
resource "ovh_cloud_project_network_private_subnet" "data" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = "GRA9"
  start        = "192.168.30.10"
  end          = "192.168.30.200"
  network      = "192.168.30.0/24"
  dhcp         = true
  no_gateway   = false
}

# Update Object Storage to supported resource
resource "ovh_cloud_project_storage" "storage" {
  service_name = var.ovh_project_id
  region_name  = "GRA"
  name         = "nhs-landingzone-bucket"
  versioning = {
    status = "enabled"
  }
}

resource "ovh_cloud_project_gateway" "gateway" {
  service_name = var.ovh_project_id
  name       = "gateway"
  model      = "s"
  region     = "GRA9"
  network_id = local.vnet_openstack_id
  subnet_id  = ovh_cloud_project_network_private_subnet.app.id
}

# Update Kubernetes Cluster resource and add node pool
resource "ovh_cloud_project_kube" "cluster" {
  service_name = var.ovh_project_id
  name         = "landing-zone-k8s"
  region       = "GRA9"
  version      = "1.31"
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
  name         = "default"
  flavor_name  = "b3-8"
  desired_nodes = 2
  max_nodes     = 3
  min_nodes     = 1
  autoscale     = true
}

resource "ovh_cloud_project_database" "pgsqldb" {
  service_name  = var.ovh_project_id
  description   = "my-first-postgresql"
  engine        = "postgresql"
  version       = "17"
  plan          = "essential"
  nodes {
    region      = "GRA"
    network_id  = local.vnet_openstack_id
    subnet_id   = ovh_cloud_project_network_private_subnet.data.id
  }
  flavor        = "db1-4"
  ip_restrictions {
    description = "ip 1"
    ip = "178.97.6.0/24"
  }
  ip_restrictions {
    description = "ip 2"
    ip = "178.97.7.0/24"
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

resource "ovh_cloud_project_database_user" "pgsqldb_user" {
  service_name = var.ovh_project_id
  engine      = data.ovh_cloud_project_database.pgsqldb_data.engine
  cluster_id  = data.ovh_cloud_project_database.pgsqldb_data.id
  name        = "dummyuser"
  password    = random_password.pgsql_password.result
  roles       = ["readwrite"]
  database_name = ovh_cloud_project_database_database.pgsqldb_database.name
}

resource "random_password" "pgsql_password" {
  length  = 16
  special = true
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
  value = data.ovh_cloud_project_database.pgsqldb_data.hostname
}
output "pgsql_user" {
  value = ovh_cloud_project_database_user.pgsqldb_user.user_name
}
output "pgsql_password" {
  value     = random_password.pgsql_password.result
  sensitive = true
}
output "pgsql_dbname" {
  value = ovh_cloud_project_database_database.pgsqldb_database.name
}
