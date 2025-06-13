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
  regions      = ["GRA11"]
}

# Subnet 1: Ingress (for ingress controllers or load balancer)
resource "ovh_cloud_project_network_private_subnet" "ingress" {
  service_name = var.ovh_project_id
  network_id   = ovh_cloud_project_network_private.vnet.id
  region       = "GRA11"
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
  region       = "GRA11"
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
  region       = "GRA11"
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

# Update Kubernetes Cluster resource and add node pool
resource "ovh_cloud_project_kube" "cluster" {
  service_name = var.ovh_project_id
  name         = "landing-zone-k8s"
  region       = "GRA9"
  version      = "1.31"
  # private_network_id = tolist(ovh_cloud_project_network_private.vnet.regions_attributes[*].openstackid)[0]
  # nodes_subnet_id = ovh_cloud_project_network_private_subnet.subnet.id
  # private_network_configuration {
  #     default_vrack_gateway              = ""
  #     private_network_routing_as_default = false
  # }
  # depends_on = [
  #   ovh_cloud_project_network_private.vnet
  # ] 
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

# Outputs
output "kubeconfig" {
  value     = ovh_cloud_project_kube.cluster.kubeconfig
  sensitive = true
}

output "object_storage_name" {
  value = ovh_cloud_project_storage.storage.name
}
