terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    stackit = {
      source  = "stackitcloud/stackit"
      version = ">= 0.60.0"
    }
  }

  backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

provider "stackit" {
  default_region      = "eu01"
  service_account_key = var.stackit_service_account_key
  private_key         = var.stackit_private_key
}

provider "random" {}