provider "azurerm" {
  features {}
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "rg-noudsavenije-devops"
    storage_account_name = "noudstfbackend"
    container_name       = "azuretfstate"
    key                  = "terraform.tfstate"
  }
}

resource "azurerm_resource_group" "main" {
  name     = "rg-noudsavenije-devops"
  location = "westeurope"

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_virtual_network" "main" {
  name                = "landing-zone-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "db" {
  name                 = "db-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "dummypsqlserver"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "17"
  administrator_login    = "psqladmin"
  administrator_password = "YourStrongPassword123!"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  delegated_subnet_id    = azurerm_subnet.db.id
  zone                   = "1"
}

resource "azurerm_postgresql_flexible_server_database" "dummydb" {
  name      = "dummydb"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = "dummy-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "dummyaks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B4ms"
    vnet_subnet_id = azurerm_subnet.aks.id
    min_count  = 1
    max_count  = 3
    enable_auto_scaling = true
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    dns_service_ip = "10.0.10.10"
    service_cidr   = "10.0.10.0/24"
    docker_bridge_cidr = "172.17.0.1/16"
  }
}

output "kubeconfig" {
  value     = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive = true
}

output "pgsql_host" {
  value = azurerm_postgresql_flexible_server.main.fqdn
}

output "pgsql_dbname" {
  value = azurerm_postgresql_flexible_server_database.dummydb.name
}

output "pgsql_username" {
  value = azurerm_postgresql_flexible_server.main.administrator_login
}

output "pgsql_password" {
  value     = azurerm_postgresql_flexible_server.main.administrator_password
  sensitive = true
}

output "pgsql_server_name" {
  value = azurerm_postgresql_flexible_server.main.name
}
