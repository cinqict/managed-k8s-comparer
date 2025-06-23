data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

resource "azurerm_virtual_network" "main" {
  name                = var.vnet_name
  address_space       = [var.vnet_address_space]
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
}

resource "azurerm_subnet" "aks" {
  name                 = var.aks_subnet_name
  resource_group_name  = data.azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.aks_subnet_address_prefix]
}

resource "azurerm_subnet" "db" {
  name                 = var.db_subnet_name
  resource_group_name  = data.azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.db_subnet_address_prefix]

  delegation {
    name = var.db_delegation_name
    service_delegation {
      name = var.db_service_delegation_name
      actions = var.db_service_delegation_actions
    }
  }
}

resource "random_password" "psql" {
  length  = var.psql_password_length
  special = var.psql_password_special
}

resource "azurerm_private_dns_zone" "postgres" {
  name                = var.private_dns_zone_name
  resource_group_name = data.azurerm_resource_group.main.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres" {
  name                  = var.private_dns_zone_vnet_link_name
  resource_group_name   = data.azurerm_resource_group.main.name
  private_dns_zone_name = azurerm_private_dns_zone.postgres.name
  virtual_network_id    = azurerm_virtual_network.main.id
}

resource "azurerm_postgresql_flexible_server" "main" {
  name                   = var.psql_server_name
  resource_group_name    = data.azurerm_resource_group.main.name
  location               = data.azurerm_resource_group.main.location
  version                = var.psql_version
  administrator_login    = var.psql_admin_login
  administrator_password = random_password.psql.result
  storage_mb             = var.psql_storage_mb
  sku_name               = var.psql_sku_name
  delegated_subnet_id    = azurerm_subnet.db.id
  zone                   = var.psql_zone
  private_dns_zone_id    = azurerm_private_dns_zone.postgres.id
  public_network_access_enabled = var.psql_public_network_access_enabled
}

resource "azurerm_postgresql_flexible_server_database" "dummydb" {
  name      = var.psql_db_name
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = var.psql_db_charset
  collation = var.psql_db_collation
}

resource "azurerm_kubernetes_cluster" "main" {
  name                = var.aks_name
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  dns_prefix          = var.aks_dns_prefix

  default_node_pool {
    name       = var.aks_node_pool_name
    node_count = var.aks_node_count
    vm_size    = var.aks_vm_size
    vnet_subnet_id = azurerm_subnet.aks.id
    min_count  = var.aks_min_count
    max_count  = var.aks_max_count
    auto_scaling_enabled = var.aks_auto_scaling_enabled
  }

  network_profile {
    network_plugin     = var.aks_network_plugin
    service_cidr       = var.aks_service_cidr
    dns_service_ip     = var.aks_dns_service_ip
  }

  identity {
    type = var.aks_identity_type
  }
}

