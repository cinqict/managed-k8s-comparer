output "kubeconfig" {
  value     = ovh_cloud_project_kube.cluster.kubeconfig
  sensitive = true
}

output "object_storage_name" {
  value = ovh_cloud_project_storage.storage.name
}

output "pgsql_host" {
  value = data.ovh_cloud_project_database.pgsqldb_data.endpoints[0].domain
}
output "pgsql_port" {
  value = data.ovh_cloud_project_database.pgsqldb_data.endpoints[0].port
}
output "pgsql_uri" {
  value = data.ovh_cloud_project_database.pgsqldb_data.endpoints[0].uri
}
output "pgsql_dbname" {
  value = ovh_cloud_project_database_database.pgsqldb_database.name
}
output "pgsql_cluster_id" {
  value = ovh_cloud_project_database.pgsqldb.id
}