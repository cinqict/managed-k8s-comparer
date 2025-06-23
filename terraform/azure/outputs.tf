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

output "pgsql_port" {
  value = "5432" #azurerm_postgresql_flexible_server.main.port ## NOT SUPPORTED IN AZURE
}