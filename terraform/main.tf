# Top-level Terraform configuration for OVH Landing Zone

module "ovh_landing_zone" {
  source = "./modules/ovh"

  ovh_endpoint           = var.ovh_endpoint
  ovh_project_id         = var.ovh_project_id
  ovh_application_key    = var.ovh_application_key
  ovh_application_secret = var.ovh_application_secret
  ovh_consumer_key       = var.ovh_consumer_key

}

# Optionally, output module outputs at the root level
output "kubeconfig" {
  value     = module.ovh_landing_zone.kubeconfig
  sensitive = true
}

output "object_storage_name" {
  value = module.ovh_landing_zone.object_storage_name
}

output "pgsql_host" {
  value = module.ovh_landing_zone.pgsql_host
}
output "pgsql_port" {
  value = module.ovh_landing_zone.pgsql_port
}
output "pgsql_uri" {
  value = module.ovh_landing_zone.pgsql_uri
}
output "pgsql_dbname" {
  value = module.ovh_landing_zone.pgsql_dbname
}
output "pgsql_cluster_id" {
  value = module.ovh_landing_zone.pgsql_cluster_id
}
