# Variables for Azure Resource Group and Networking
variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "rg-noudsavenije-devops"
}

variable "vnet_name" {
  description = "Name of the virtual network"
  type        = string
  default     = "landing-zone-vnet"
}

variable "vnet_address_space" {
  description = "Address space for the virtual network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "aks_subnet_name" {
  description = "Name of the AKS subnet"
  type        = string
  default     = "aks-subnet"
}

variable "aks_subnet_address_prefix" {
  description = "Address prefix for the AKS subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "db_subnet_name" {
  description = "Name of the DB subnet"
  type        = string
  default     = "db-subnet"
}

variable "db_subnet_address_prefix" {
  description = "Address prefix for the DB subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "db_delegation_name" {
  description = "Delegation name for DB subnet"
  type        = string
  default     = "psqlflexible"
}

variable "db_service_delegation_name" {
  description = "Service delegation name for DB subnet"
  type        = string
  default     = "Microsoft.DBforPostgreSQL/flexibleServers"
}

variable "db_service_delegation_actions" {
  description = "Service delegation actions for DB subnet"
  type        = list(string)
  default     = ["Microsoft.Network/virtualNetworks/subnets/action"]
}

# Variables for PostgreSQL
variable "psql_password_length" {
  description = "Length of the PostgreSQL admin password"
  type        = number
  default     = 20
}

variable "psql_password_special" {
  description = "Whether to use special characters in the password"
  type        = bool
  default     = true
}

variable "private_dns_zone_name" {
  description = "Name of the private DNS zone for PostgreSQL"
  type        = string
  default     = "privatelink.postgres.database.azure.com"
}

variable "private_dns_zone_vnet_link_name" {
  description = "Name of the private DNS zone VNet link"
  type        = string
  default     = "postgres-vnet-link"
}

variable "psql_server_name" {
  description = "Name of the PostgreSQL server"
  type        = string
  default     = "dummypsqlserver"
}

variable "psql_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15"
}

variable "psql_admin_login" {
  description = "PostgreSQL admin login name"
  type        = string
  default     = "psqladmin"
}

variable "psql_storage_mb" {
  description = "PostgreSQL storage in MB"
  type        = number
  default     = 32768
}

variable "psql_sku_name" {
  description = "PostgreSQL SKU name"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "psql_zone" {
  description = "Availability zone for PostgreSQL"
  type        = string
  default     = "3"
}

variable "psql_public_network_access_enabled" {
  description = "Enable public network access for PostgreSQL"
  type        = bool
  default     = false
}

variable "psql_db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "dummydb"
}

variable "psql_db_charset" {
  description = "Charset for the PostgreSQL database"
  type        = string
  default     = "UTF8"
}

variable "psql_db_collation" {
  description = "Collation for the PostgreSQL database"
  type        = string
  default     = "en_US.utf8"
}

# Variables for AKS
variable "aks_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "dummy-aks"
}

variable "aks_dns_prefix" {
  description = "DNS prefix for the AKS cluster"
  type        = string
  default     = "dummyaks"
}

variable "aks_node_pool_name" {
  description = "Name of the AKS node pool"
  type        = string
  default     = "default"
}

variable "aks_node_count" {
  description = "Number of nodes in the AKS node pool"
  type        = number
  default     = 1
}

variable "aks_vm_size" {
  description = "VM size for the AKS node pool"
  type        = string
  default     = "Standard_B4ms"
}

variable "aks_min_count" {
  description = "Minimum node count for autoscaling"
  type        = number
  default     = 1
}

variable "aks_max_count" {
  description = "Maximum node count for autoscaling"
  type        = number
  default     = 3
}

variable "aks_auto_scaling_enabled" {
  description = "Enable autoscaling for AKS node pool"
  type        = bool
  default     = true
}

variable "aks_network_plugin" {
  description = "Network plugin for AKS"
  type        = string
  default     = "azure"
}

variable "aks_service_cidr" {
  description = "Service CIDR for AKS"
  type        = string
  default     = "10.1.0.0/16"
}

variable "aks_dns_service_ip" {
  description = "DNS service IP for AKS"
  type        = string
  default     = "10.1.0.10"
}

variable "aks_identity_type" {
  description = "Identity type for AKS"
  type        = string
  default     = "SystemAssigned"
}
