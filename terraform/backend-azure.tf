terraform {
  backend "azurerm" {
    resource_group_name  = "rg-noudsavenije-devops"
    storage_account_name = "noudstfbackend"
    container_name       = "azuretfstate"
    key                  = "terraform.tfstate"
  }
}