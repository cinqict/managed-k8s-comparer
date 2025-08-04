output "network_id" {
  value = hcloud_network.private_network.id
}

output "kubeconfig" {
  value     = data.external.kubeconfig.result.kubeconfig
  sensitive = true
}