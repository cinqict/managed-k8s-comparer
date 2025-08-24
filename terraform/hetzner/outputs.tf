output "network_id" {
  value = hcloud_network.private_network.id
}

output "master_node_ip" {
  value = hcloud_server.master_node.ipv4_address
}

output "pgsql_host" {
  value = hcloud_server.postgresql_server.ipv4_address
}
output "pgsql_port" {
  value = "5432"
}
output "pgsql_dbname" {
  value = var.db_name
}
output "pgsql_username" {
  value = var.db_user
}
output "pgsql_password" {
  value = random_password.postgresql.result
  sensitive = true
}