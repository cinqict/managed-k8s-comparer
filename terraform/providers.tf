terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
    ovh = {
      source  = "ovh/ovh"
      version = ">= 0.44.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "random" {}

provider "ovh" {
  endpoint           = var.ovh_endpoint != "" ? var.ovh_endpoint : "ovh-eu"
  application_key    = var.ovh_application_key != "" ? var.ovh_application_key : "dummy"
  application_secret = var.ovh_application_secret != "" ? var.ovh_application_secret : "dummy"
  consumer_key       = var.ovh_consumer_key != "" ? var.ovh_consumer_key : "dummy"
}