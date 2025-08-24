output "kubeconfig" {
  description = "Kubeconfig for StackIt managed Kubernetes cluster"
  value       = stackit_ske_kubeconfig.main.kubeconfig
  sensitive   = true
}

output "pgsql_host" {
  description = "PostgreSQL host"
  value       = stackit_postgresflex_instance.main.host
}

output "pgsql_dbname" {
  description = "PostgreSQL database name"
  value       = stackit_postgresflex_database.main.name
}

output "pgsql_username" {
  description = "PostgreSQL username"
  value       = stackit_postgresflex_user.main.username
}

output "pgsql_password" {
  description = "PostgreSQL password"
  value       = stackit_postgresflex_user.main.password
  sensitive   = true
}

output "pgsql_server_name" {
  description = "PostgreSQL server name"
  value       = stackit_postgresflex_instance.main.name
}

output "pgsql_port" {
  description = "PostgreSQL port"
  value       = stackit_postgresflex_instance.main.port
}