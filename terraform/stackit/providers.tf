terraform {
  required_providers {
    stackit = {
      source  = "stackitcloud/stackit"
      version = "0.59.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.35.0"
    }
  }
}

provider "stackit" {
  default_region = "eu01"
  service_account_key_path = var.service_account_key_path
  private_key_path         = var.private_key_path
}

provider "kubernetes" {
  host = yamldecode(stackit_ske_kubeconfig.ske_kubeconfig.kube_config).clusters[0].cluster.server
  client_certificate = base64decode(yamldecode(stackit_ske_kubeconfig.ske_kubeconfig.kube_config).users[0].user["client-certificate-data"])
  client_key = base64decode(yamldecode(stackit_ske_kubeconfig.ske_kubeconfig.kube_config).users[0].user["client-key-data"])
  cluster_ca_certificate = base64decode(yamldecode(stackit_ske_kubeconfig.ske_kubeconfig.kube_config).users[0].user["certificate-authority-data"])
}
